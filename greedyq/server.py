"""Server-rendered local browser application for respondent testing."""

import html
import json
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from .runtime import Store, matches, parse_form


CSS="""body{margin:0;background:#f5f7fb;color:#172033;font:16px/1.55 system-ui}.top{background:#fff;border-bottom:1px solid #dfe3eb;padding:14px}.top div{max-width:760px;margin:auto;font-size:20px;font-weight:800}.card{max-width:760px;margin:38px auto;background:#fff;border:1px solid #dfe3eb;border-radius:16px;padding:clamp(24px,5vw,52px);box-shadow:0 8px 24px #1018280f}h1{font-size:clamp(27px,4vw,38px)}fieldset{border:0;padding:0;margin:32px 0}legend{font-weight:700;margin-bottom:12px}.choice{display:block;border:1px solid #dfe3eb;border-radius:10px;padding:13px;margin:8px 0}.choice:has(input:checked){border-color:#315c8a;background:#f2f7fc}input[type=text],input[type=number],input[type=date],select,textarea{width:100%;box-sizing:border-box;padding:11px;border:1px solid #b9c1ce;border-radius:9px;font:inherit}textarea{min-height:110px}.matrix{overflow:auto}.matrix table{border-collapse:collapse;width:100%}.matrix th,.matrix td{padding:9px;border-bottom:1px solid #ddd;text-align:center}.matrix th:first-child{text-align:left}.btn{background:#315c8a;color:#fff;border:0;border-radius:9px;padding:11px 18px;font-weight:700;font:inherit}.error{background:#fff1f0;color:#b42318;border-left:4px solid #b42318;padding:12px}.meta{color:#667085;font-size:13px}.required{color:#b42318}@media(max-width:820px){.card{margin:16px 10px;padding:24px}}"""


def esc(value): return html.escape(str(value if value is not None else ""), quote=True)


def question_block(q, saved):
    rule=html.escape(json.dumps(q.get("show_if"),separators=(",",":")) if q.get("show_if") else "",quote=True)
    return '<div class="question-block" data-rule="%s">%s</div>'%(rule,question_html(q,saved))


def question_html(q, saved):
    required='<span class="required"> *</span>' if q.get("required") else ""; out=['<fieldset><legend>%s%s</legend>'%(esc(q["label"]),required)]
    value=saved.get(q["id"])
    if q["type"]=="custom":
        base=dict(q);base["type"]=q.get("base_type","text");return question_html(base,saved)
    if q["type"]=="rank_order":
        for option in q.get("options",[]):out.append('<label class="choice">%s <select name="%s:%s"><option value="">Rank</option>%s</select></label>'%(esc(option["label"]),esc(q["id"]),esc(option["value"]),''.join('<option value="%s">%s</option>'%(i,i) for i in range(1,len(q["options"])+1))))
    elif q["type"]=="nps":
        for number in range(int(q.get("min",0)),int(q.get("max",10))+1):out.append('<label class="choice"><input type="radio" name="%s" value="%s"> %s</label>'%(esc(q["id"]),number,number))
    elif q["type"]=="timing":out.append('<input type="hidden" name="%s" value="0">'%esc(q["id"]))
    elif q["type"]=="constant_sum":
        for option in q.get("options",[]):out.append('<label class="choice">%s <input type="number" min="0" name="%s:%s" value="0"></label>'%(esc(option["label"]),esc(q["id"]),esc(option["value"])))
    elif q["type"]=="side_by_side":
        for column in q.get("columns",[]):
            out.append('<h3>%s</h3><div class="matrix"><table>'%esc(column["label"]))
            for row in q.get("rows",[]):out.append('<tr><th>%s</th>%s</tr>'%(esc(row["label"]),''.join('<td><label><input type="radio" name="%s:%s:%s" value="%s"> %s</label></td>'%(esc(q["id"]),esc(column["value"]),esc(row["value"]),esc(option["value"]),esc(option["label"])) for option in q.get("options",[]))))
            out.append('</table></div>')
    elif q["type"]=="pick_group_rank":
        for option in q.get("options",[]):out.append('<div class="choice"><strong>%s</strong><select name="%s:%s:group"><option value="">Group</option>%s</select><input type="number" min="1" name="%s:%s:rank" placeholder="Rank"></div>'%(esc(option["label"]),esc(q["id"]),esc(option["value"]),''.join('<option value="%s">%s</option>'%(esc(group["value"]),esc(group["label"])) for group in q.get("groups",[])),esc(q["id"]),esc(option["value"])))
    elif q["type"]=="drill_down":out.append('<select name="%s">%s</select>'%(esc(q["id"]),''.join('<option value="%s">%s</option>'%(esc(option["value"]),esc(option["label"])) for option in q.get("options",[]))))
    elif q["type"] in ("mc","mc_multiple","slider"):
        kind="checkbox" if q["type"]=="mc_multiple" else "radio"; selected=value if isinstance(value,list) else [value]
        for option in q.get("options",[]):out.append('<label class="choice"><input type="%s" name="%s" value="%s" %s> %s</label>'%(kind,esc(q["id"]),esc(option["value"]),"checked" if option["value"] in selected else "",esc(option["label"])))
    elif q["type"]=="select":
        out.append('<select name="%s"><option value="">%s</option>'%(esc(q["id"]),esc(q.get("placeholder","Choose one"))))
        for option in q.get("options",[]):out.append('<option value="%s" %s>%s</option>'%(esc(option["value"]),"selected" if option["value"]==value else "",esc(option["label"])))
        out.append('</select>')
    elif q["type"] in ("matrix", "matrix_multiple"):
        out.append('<div class="matrix"><table><tr><th>Statement</th>'+''.join('<th>%s</th>'%esc(o["label"]) for o in q["options"])+"</tr>")
        kind="checkbox" if q["type"]=="matrix_multiple" else "radio"
        for row in q["rows"]:out.append('<tr><th>%s</th>%s</tr>'%(esc(row["label"]),''.join('<td><input aria-label="%s: %s" type="%s" name="%s:%s" value="%s" %s></td>'%(esc(row["label"]),esc(o["label"]),kind,esc(q["id"]),esc(row["value"]),esc(o["value"]),"checked" if (o["value"] in (value or {}).get(row["value"],[]) if q["type"]=="matrix_multiple" else (value or {}).get(row["value"])==o["value"]) else "") for o in q["options"])))
        out.append('</table></div>')
    elif q["type"] in ("audio", "video"):
        attrs=' controls' if q.get("controls",True) else ''
        attrs+=' muted' if q.get("muted") else ''
        attrs+=' loop' if q.get("loop") else ''
        if q["type"]=="audio":out.append('<audio aria-label="%s" src="%s"%s></audio>'%(esc(q["label"]),esc(q.get("src","")),attrs))
        else:out.append('<video aria-label="%s" src="%s" poster="%s"%s style="width:100%%"></video>'%(esc(q["label"]),esc(q.get("src","")),esc(q.get("poster","")),attrs))
        if q.get("caption"):out.append('<p class="meta">%s</p>'%esc(q["caption"]))
    elif q["type"]=="textarea":out.append('<textarea name="%s" placeholder="%s">%s</textarea>'%(esc(q["id"]),esc(q.get("placeholder","")),esc(value)))
    else:
        kind="number" if q["type"] in ("numeric","slider_numeric") else "date" if q["type"]=="date" else "text"
        bounds=(' min="%s"'%q["min"] if q.get("min") is not None else '')+(' max="%s"'%q["max"] if q.get("max") is not None else '')
        out.append('<input type="%s" name="%s" value="%s" placeholder="%s"%s>'%(kind,esc(q["id"]),esc(value),esc(q.get("placeholder","")),bounds))
    out.append('</fieldset>');return ''.join(out)


def make_handler(model, config, store):
    pages={p["id"]:p for p in model["pages"]}
    class Handler(BaseHTTPRequestHandler):
        def sid(self):
            jar=cookies.SimpleCookie(self.headers.get("Cookie")); morsel=jar.get("greedyq_session"); return morsel.value if morsel else None
        def send_html(self, body, status=200, sid=None):
            data=body.encode();self.send_response(status);self.send_header("Content-Type","text/html; charset=utf-8");self.send_header("Content-Length",str(len(data)));self.send_header("Content-Security-Policy","default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'");self.send_header("Cache-Control","no-store");self.send_header("Referrer-Policy","no-referrer");self.send_header("X-Content-Type-Options","nosniff")
            if sid:self.send_header("Set-Cookie","greedyq_session=%s; HttpOnly; SameSite=Lax; Path=/"%sid)
            self.end_headers();self.wfile.write(data)
        def do_HEAD(self):
            if urlparse(self.path).path not in ("/", "/study", "/health"): self.send_error(404); return
            self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Security-Policy","default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"); self.send_header("Cache-Control","no-store"); self.send_header("Referrer-Policy","no-referrer"); self.send_header("X-Content-Type-Options","nosniff"); self.end_headers()
        def do_GET(self):
            path=urlparse(self.path).path
            if path=="/health":self.send_response(200);self.end_headers();self.wfile.write(b"ok");return
            if path not in ("/","/study"):self.send_error(404);return
            sid=self.sid();state=store.state(sid) if sid else None
            if not state:sid=store.create(model,config);state=store.state(sid)
            page=pages[state["session"]["current_page"]]; answers=state["answers"]
            message=parse_qs(urlparse(self.path).query).get("error",[""])[0]
            terminal=page.get("terminal"); form=''.join(question_block(q,answers) for q in page.get("questions",[]))
            if not terminal:form='<form method="post" action="/answer">%s<button class="btn" type="submit">%s</button></form>'%(form,esc(page.get("next_label",model.get("messages",{}).get("next","Continue"))))
            else:form='<p class="meta">Survey outcome: %s</p>'%esc(terminal)
            script="""<script>(()=>{const scalar=v=>/^-?\\d+(\\.\\d+)?$/.test(v)?Number(v):v;const val=n=>{const es=[...document.querySelectorAll(`[name='${CSS.escape(n)}']`)];const c=es.find(e=>e.checked);if(c)return scalar(c.value);const e=es[0];return e&&!['radio','checkbox'].includes(e.type)?scalar(e.value):null};const ok=r=>{if(!r)return true;if(r.all)return r.all.every(ok);if(r.any)return r.any.some(ok);const a=val(r.field);if('equals'in r)return a===r.equals;if('not_equals'in r)return a!==r.not_equals;if('lt'in r)return a!==null&&Number(a)<r.lt;if('lte'in r)return a!==null&&Number(a)<=r.lte;if('gt'in r)return a!==null&&Number(a)>r.gt;if('gte'in r)return a!==null&&Number(a)>=r.gte;return false};const update=()=>document.querySelectorAll('.question-block').forEach(x=>{const r=x.dataset.rule?JSON.parse(x.dataset.rule):null;x.hidden=!ok(r);x.querySelectorAll('input,select,textarea').forEach(e=>e.disabled=x.hidden)});document.addEventListener('input',update);document.addEventListener('change',update);update()})()</script>"""
            body='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title><style>%s</style></head><body><header class="top"><div>greedyQ <span class="meta">LOCAL RESPONDENT TEST</span></div></header><main class="card"><p class="meta">%s</p><h1>%s</h1><div>%s</div>%s%s</main>%s</body></html>'%(esc(model["title"]),CSS,esc(model["title"]),esc(page["title"]),esc(page.get("body","")),('<p class="error">%s</p>'%esc(message)) if message else '',form,script)
            self.send_html(body,sid=sid)
        def do_POST(self):
            if urlparse(self.path).path!="/answer":self.send_error(404);return
            sid=self.sid();state=store.state(sid) if sid else None
            if not state:self.send_html('<p class="error">Your session expired. Return to the survey start.</p>',409);return
            length=int(self.headers.get("Content-Length","0"));form=parse_qs(self.rfile.read(length).decode(),keep_blank_values=True);page=pages[state["session"]["current_page"]]
            try:store.transition(sid,page["id"],parse_form(page,form),model,config);self.send_response(303);self.send_header("Location","/study");self.end_headers()
            except ValueError as exc:self.send_response(303);self.send_header("Location","/study?"+urlencode({"error":str(exc)}));self.end_headers()
        def log_message(self,format,*args): pass
    return Handler


def serve(model,config,store,port=4180):
    server=ThreadingHTTPServer(("localhost",port),make_handler(model,config,store));return server
