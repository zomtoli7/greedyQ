"""Local respondent runtime with durable SQLite sessions."""

import json
import secrets
import sqlite3
import threading
import time
import uuid


TERMINAL = {"completed", "screened_out", "consent_refused", "withdrawn", "technical_error"}


class Store:
    def __init__(self, path):
        self.path = str(path); self.lock = threading.RLock(); self._init()

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        db.row_factory = sqlite3.Row; db.execute("pragma foreign_keys=on"); db.execute("pragma journal_mode=wal")
        return db

    def _init(self):
        with self.connect() as db:
            db.executescript("""
            create table if not exists sessions(id text primary key,study_id text not null,study_version text not null,spec_version text not null,current_page text not null,is_test integer not null,lifecycle_state text not null,created_at real not null,updated_at real not null,terminal_at real);
            create table if not exists answers(session_id text not null references sessions(id) on delete cascade,question_id text not null,value text,answered_at real not null,primary key(session_id,question_id));
            create table if not exists consent_events(id integer primary key autoincrement,session_id text not null references sessions(id) on delete cascade,consent_id text not null,consent_version text not null,document_sha256 text not null,decision text not null,occurred_at real not null);
            create table if not exists assignments(session_id text not null references sessions(id) on delete cascade,randomization_id text not null,condition_name text not null,method text not null,block_id text,draw_id text not null,spec_version text not null,assigned_at real not null,primary key(session_id,randomization_id));
            create table if not exists lifecycle_events(id integer primary key autoincrement,session_id text not null references sessions(id) on delete cascade,from_state text,to_state text not null,page_id text,metadata text not null,occurred_at real not null);
            create table if not exists data_requests(id integer primary key autoincrement,session_id text not null references sessions(id) on delete cascade,request_type text not null,status text not null,requested_at real not null);
            """)

    def create(self, model, config):
        sid=str(uuid.uuid4()); now=time.time(); study=config.get("study",{})
        with self.connect() as db:
            db.execute("insert into sessions values(?,?,?,?,?,?,?,?,?,null)",(sid,model["study_id"],study.get("version","draft"),config.get("spec_version","0.2"),model["start_page"],1,"created",now,now))
            db.execute("insert into lifecycle_events(session_id,from_state,to_state,page_id,metadata,occurred_at) values(?,?,?,?,?,?)",(sid,None,"created",model["start_page"],"{}",now))
        return sid

    def state(self, sid):
        with self.connect() as db:
            session=db.execute("select * from sessions where id=?",(sid,)).fetchone()
            if not session:return None
            answers={r["question_id"]:json.loads(r["value"]) for r in db.execute("select question_id,value from answers where session_id=?",(sid,))}
            assignment=db.execute("select * from assignments where session_id=? order by assigned_at limit 1",(sid,)).fetchone()
            return {"session":dict(session),"answers":answers,"condition":assignment["condition_name"] if assignment else None}

    def transition(self, sid, page, answers, model, config):
        pages={p["id"]:p for p in model["pages"]}; consent=config.get("consent",{}); now=time.time()
        with self.lock, self.connect() as db:
            db.execute("begin immediate")
            session=db.execute("select * from sessions where id=?",(sid,)).fetchone()
            if not session: db.rollback(); raise ValueError("This survey session could not be found.")
            if session["lifecycle_state"] in TERMINAL: db.rollback(); return self.state(sid)
            if session["current_page"]!=page: db.rollback(); raise ValueError("This page is no longer current. Refresh the survey and try again.")
            current=pages[page]; existing={r["question_id"]:json.loads(r["value"]) for r in db.execute("select question_id,value from answers where session_id=?",(sid,))}
            combined={**existing,**answers}; condition_row=db.execute("select condition_name from assignments where session_id=? limit 1",(sid,)).fetchone(); condition=condition_row[0] if condition_row else None
            visible=[q for q in current.get("questions",[]) if matches(q.get("show_if"),combined,condition)]
            for q in visible:
                value=answers.get(q["id"], existing.get(q["id"]))
                missing=value is None or value=="" or value==[] or (q.get("type") in ("matrix", "matrix_multiple") and any(row["value"] not in (value or {}) for row in q.get("rows",[])))
                if q.get("required") and missing:
                    db.rollback(); raise ValueError("Please answer: %s" % q["label"])
                if value is not None and q.get("min") is not None and float(value)<q["min"]: db.rollback(); raise ValueError("%s must be at least %s."%(q["label"],q["min"]))
                if value is not None and q.get("max") is not None and float(value)>q["max"]: db.rollback(); raise ValueError("%s must be at most %s."%(q["label"],q["max"]))
            consent_q=consent.get("confirmation_question")
            accepted=session["lifecycle_state"] in ("consented","in_progress")
            if page==next((p["id"] for p in model["pages"] if any(q["id"]==consent_q for q in p.get("questions",[]))),None):
                decision="accepted" if answers.get(consent_q)==consent.get("accept_value") else "refused"
                db.execute("insert into consent_events(session_id,consent_id,consent_version,document_sha256,decision,occurred_at) values(?,?,?,?,?,?)",(sid,consent.get("id","consent"),str(consent.get("version","unknown")),consent.get("sha256","0"*64),decision,now)); accepted=decision=="accepted"
            if not accepted and page not in (model["start_page"], current["id"]): db.rollback(); raise ValueError("Consent is required before research answers can be saved.")
            for q in visible:
                if q["id"] in answers and q["id"]!=consent_q:
                    db.execute("insert into answers values(?,?,?,?) on conflict(session_id,question_id) do update set value=excluded.value,answered_at=excluded.answered_at",(sid,q["id"],json.dumps(answers[q["id"]]),now))
            if logic_clear(config):
                visible_ids={q["id"] for q in visible}
                for q in current.get("questions",[]):
                    if q["id"] not in visible_ids: db.execute("delete from answers where session_id=? and question_id=?",(sid,q["id"]))
            randomizations=config.get("randomization",[]) or []
            for rnd in randomizations:
                if (rnd.get("assignment_point") or {}).get("after_page")==page and not condition:
                    counts={name:db.execute("select count(*) from assignments where randomization_id=? and condition_name=?",(rnd["id"],name)).fetchone()[0] for name in rnd["conditions"]}
                    minimum=min(counts.values()); candidates=[name for name,count in counts.items() if count==minimum]; condition=secrets.choice(candidates)
                    total=sum(counts.values()); block=str(total//int(rnd.get("block_size",len(candidates))))
                    db.execute("insert into assignments values(?,?,?,?,?,?,?,?)",(sid,rnd["id"],condition,rnd.get("method","simple"),block,secrets.token_hex(8),config.get("spec_version","0.2"),now))
            target=next_for(current,combined,condition)
            if not target or target not in pages: db.rollback(); raise ValueError("The next survey page is not configured correctly.")
            target_page=pages[target]; new_state=target_page.get("terminal") or ("in_progress" if accepted else "created")
            if new_state=="withdrawn" and combined.get("deletion_request")=="yes":
                db.execute("delete from answers where session_id=?",(sid,)); db.execute("delete from assignments where session_id=?",(sid,)); db.execute("insert into data_requests(session_id,request_type,status,requested_at) values(?,?,?,?)",(sid,"deletion","recorded",now))
            db.execute("update sessions set current_page=?,lifecycle_state=?,updated_at=?,terminal_at=? where id=?",(target,new_state,now,now if new_state in TERMINAL else None,sid))
            db.execute("insert into lifecycle_events(session_id,from_state,to_state,page_id,metadata,occurred_at) values(?,?,?,?,?,?)",(sid,session["lifecycle_state"],new_state,target,"{}",now)); db.commit()
        return self.state(sid)


def matches(rule, answers, condition):
    if not rule:return True
    if "all" in rule:return all(matches(r,answers,condition) for r in rule["all"])
    if "any" in rule:return any(matches(r,answers,condition) for r in rule["any"])
    actual=condition if rule.get("field")=="condition" else answers.get(rule.get("field"))
    for key,fn in (("equals",lambda a,b:a==b),("not_equals",lambda a,b:a!=b),("lt",lambda a,b:float(a)<b),("lte",lambda a,b:float(a)<=b),("gt",lambda a,b:float(a)>b),("gte",lambda a,b:float(a)>=b)):
        if key in rule:
            try:return fn(actual,rule[key])
            except (TypeError,ValueError):return False
    return False


def next_for(page, answers, condition):
    for route in page.get("routes",[]):
        if matches(route["when"],answers,condition):return route["to"]
    return page.get("next")


def parse_form(page, form):
    result={}
    for q in page.get("questions",[]):
        if q["type"] in ("matrix", "matrix_multiple"):
            if q["type"] == "matrix_multiple": rows={r["value"]:[scalar(v) for v in form.get("%s:%s"%(q["id"],r["value"]),[])] for r in q.get("rows",[])}; rows={k:v for k,v in rows.items() if v}
            else: rows={r["value"]:form.get("%s:%s"%(q["id"],r["value"]),[None])[0] for r in q.get("rows",[])}; rows={k:scalar(v) for k,v in rows.items() if v is not None}
            if rows:result[q["id"]]=rows
        elif q["type"]=="mc_multiple":
            if q["id"] in form:result[q["id"]]=[scalar(v) for v in form[q["id"]]]
        elif q["id"] in form:result[q["id"]]=scalar(form[q["id"]][0])
    return result


def scalar(value):
    try:return int(value)
    except (ValueError,TypeError):
        try:return float(value)
        except (ValueError,TypeError):return value


def logic_clear(config):
    return config.get("logic",{}).get("hidden_answer_policy","clear_on_hide")=="clear_on_hide"
