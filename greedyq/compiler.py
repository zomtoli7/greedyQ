"""Compile parsed QMD and greedyq.yml into the browser preview model."""

import re
import ast
from .randomization import option_plan, page_plan
from .redirects import redirect_plan
from .localization import translate
from .prolific import integration_plan


OPS = (("!=", "not_equals"), ("<=", "lte"), (">=", "gte"), ("==", "equals"), ("<", "lt"), (">", "gt"))


def split_condition(text, connector):
    parts=[];start=0;quote=None;escaped=False
    for i,char in enumerate(text):
        if escaped:escaped=False;continue
        if char=='\\' and quote:escaped=True;continue
        if quote:
            if char==quote:quote=None
        elif char in "\"'":quote=char
        elif text.startswith(connector,i):parts.append(text[start:i]);start=i+len(connector)
    return parts+[text[start:]]


def _literal(raw):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'": return raw[1:-1]
    if re.fullmatch(r"-?\d+", raw): return int(raw)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", raw): return float(raw)
    if raw.lower() == "true": return True
    if raw.lower() == "false": return False
    return raw


def condition(expression):
    """Parse a whitelist of expressions; never evaluate Python or R code."""
    def field(node):
        if not isinstance(node,ast.Name):raise ValueError()
        return 'condition' if node.id=='assignment_condition' else node.id
    def literal(node):
        if isinstance(node,ast.Constant) and type(node.value) in (str,int,float,bool,type(None)):return node.value
        if isinstance(node,ast.Name):
            return {'true':True,'false':False,'null':None}.get(node.id,node.id)
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub) and isinstance(node.operand,ast.Constant) and type(node.operand.value) in (int,float):return -node.operand.value
        if isinstance(node,(ast.List,ast.Tuple)):return [literal(item) for item in node.elts]
        raise ValueError()
    def convert(node):
        if isinstance(node,ast.BoolOp):return {'all' if isinstance(node.op,ast.And) else 'any':[convert(v) for v in node.values]}
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.Not):
            child=convert(node.operand)
            if 'answered' in child:return {**child,'answered':not child['answered']}
            return {'not':child}
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and not node.keywords:
            if node.func.id=='answered' and len(node.args)==1:return {'field':field(node.args[0]),'answered':True}
            if node.func.id=='contains' and len(node.args)==2:return {'field':field(node.args[0]),'contains':literal(node.args[1])}
        if isinstance(node,ast.Compare) and len(node.ops)==1:
            op=node.ops[0];right=literal(node.comparators[0]);left=node.left
            if isinstance(op,(ast.In,ast.NotIn)):
                if not isinstance(right,list):raise ValueError()
                result={'field':field(left),'in':right}
                return {'not':result} if isinstance(op,ast.NotIn) else result
            names={ast.Eq:'equals',ast.NotEq:'not_equals',ast.Lt:'lt',ast.LtE:'lte',ast.Gt:'gt',ast.GtE:'gte'}
            key=names.get(type(op))
            if key is None or isinstance(right,list):raise ValueError()
            if isinstance(left,ast.Call) and isinstance(left.func,ast.Name) and left.func.id=='length' and len(left.args)==1 and not left.keywords:
                return {'field':field(left.args[0]),'length':{key:right}}
            return {'field':field(left),key:right}
        raise ValueError()
    if len(str(expression)) > 4096:return {'unsupported':str(expression).strip()}
    try:return convert(ast.parse(str(expression).strip(),mode='eval').body)
    except (SyntaxError,ValueError,RecursionError,TypeError):return {'unsupported':str(expression).strip()}


def _constraint(question, rules):
    for rule in rules:
        if rule.get("question") != question["id"]: continue
        expression = str(rule.get("if", ""))
        match = re.fullmatch(r"\s*%s\s*>\s*(-?\d+(?:\.\d+)?)\s*" % re.escape(question["id"]), expression)
        if match: question["max"] = float(match.group(1))
        low = re.search(r"%s\s*<\s*(-?\d+(?:\.\d+)?)" % re.escape(question["id"]), expression)
        high = re.search(r"%s\s*>\s*(-?\d+(?:\.\d+)?)" % re.escape(question["id"]), expression)
        if low and high:
            question["min"] = float(low.group(1)); question["max"] = float(high.group(1))


def compile_preview(parsed, config):
    derived = [r.get("store",{}).get("condition_as") for r in config.get("randomization",[]) or []]
    def predicate(expression):
        for field in filter(None,derived): expression=re.sub(r"\b"+re.escape(field)+r"\b", "assignment_condition",str(expression))
        return condition(expression)
    front = parsed["front_matter"]
    prolific = integration_plan(config)
    language = front.get('greedyq', {}).get('language', 'en')
    option_plans = option_plan(parsed)
    survey_settings = front.get("survey-settings", {})
    required = set(survey_settings.get("required", []))
    logic = config.get("logic", {})
    shows = logic.get("show", []) or []
    skips = sorted(logic.get("skip", []) or [], key=lambda x: x.get("priority", 0), reverse=True)
    validations = logic.get("validate", []) or []
    outcomes = config.get("outcomes", {})
    terminal_by_page = {item.get("page"): item.get("lifecycle_state", key) for key, item in outcomes.items()}
    pages = []
    source_pages = parsed["pages"]
    for index, source in enumerate(source_pages):
        page = {key: source[key] for key in ("id", "title", "body")}
        for rule in shows:
            if rule.get("page")==page["id"]: page["show_if"]=predicate(rule.get("if",""))
        page["questions"] = []
        for source_question in source["questions"]:
            q = {key: value for key, value in source_question.items() if not key.startswith("_") and key != "unsupported_arguments"}
            for collection in ("options", "rows", "columns", "groups"):
                if collection in q:
                    q[collection] = [{key: value for key, value in item.items() if not key.startswith("_")} for item in q[collection]]
            q["required"] = bool(survey_settings.get("all-required", False)) or q.get("id") in required
            if q["id"] in option_plans: q["shuffle_items"] = option_plans[q["id"]]
            for rule in shows:
                if rule.get("question") == q.get("id"): q["show_if"] = predicate(rule.get("if", ""))
            _constraint(q, validations)
            if any(rule.get("question") == q.get("id") and ("not answered(%s)" % q.get("id")) in str(rule.get("if", "")) for rule in validations):
                q["required"] = True
            if q.get("id") == "age" and q.get("type") == "numeric" and "min" not in q:
                q["min"] = 0
            if q.get("min") is not None and float(q["min"]).is_integer(): q["min"] = int(q["min"])
            if q.get("max") is not None and float(q["max"]).is_integer(): q["max"] = int(q["max"])
            page["questions"].append(q)
        nav = source.get("nav", {})
        page["show_previous"] = bool(nav.get("show_previous", survey_settings.get("show-previous", True)))
        page["previous_mode"] = nav.get("previous_mode", "show" if page["show_previous"] else "hide")
        page["next_mode"] = nav.get("next_mode", "show")
        page["next_delay_seconds"] = nav.get("next_delay_seconds", 0)
        if nav.get("page_next"): page["next"] = nav["page_next"]
        elif index + 1 < len(source_pages): page["next"] = source_pages[index + 1]["id"]
        else: page["next"] = None
        if nav.get("label_next"): page["next_label"] = nav["label_next"]
        routes = []
        for rule in skips:
            if rule.get("from") == page["id"]:
                routes.append({"when": predicate(rule.get("if", "")), "to": rule.get("to")})
        if routes: page["routes"] = routes
        checks=[{"question":r.get("question"),"when":predicate(r.get("if","")),"message":r.get("message",translate(language,"Please review this answer."))} for r in validations if any(q["id"]==r.get("question") for q in page["questions"])]
        if checks:page["checks"]=checks
        if page["id"] in terminal_by_page:
            page.pop("next", None); page["terminal"] = terminal_by_page[page["id"]]
            outcome=next(o for o in outcomes.values() if o.get("page")==page["id"])
            redirect=redirect_plan(outcome)
            if redirect: page["redirect"]=redirect
        pages.append(page)

    for rule in config.get("question_order", []):
        next(p for p in pages if p["id"] == rule["page"])["shuffle_questions"] = list(rule["questions"])

    randomizations = config.get("randomization", []) or []
    conditions = ["default"]
    assignment_page = None
    if randomizations:
        first = randomizations[0]
        conditions = list((first.get("conditions") or {}).keys()) or conditions
        assignment_page = (first.get("assignment_point") or {}).get("after_page")

    by_id = {page["id"]: page for page in pages}
    def route_for(page, assigned):
        for route in page.get("routes", []):
            rule = route["when"]
            if rule.get("field") == "condition" and rule.get("equals") == assigned: return route["to"]
        return page.get("next")
    paths = {}
    start = survey_settings.get("start-page", pages[0]["id"])
    for assigned in conditions:
        path, current = [], start
        while current in by_id and current not in path:
            path.append(current)
            if by_id[current].get("terminal"): break
            current = route_for(by_id[current], assigned)
        paths[assigned] = path
    model = {
        "study_id": config.get("study", {}).get("id", "greedyq_preview"),
        "study_version": config.get("study", {}).get("version", "unknown"),
        "greedyq_version": front.get("greedyq", {}).get("version"),
        "title": config.get("study", {}).get("title", front.get("title", translate(language, "greedyQ Survey"))),
        "organization": front.get("greedyq", {}).get("organization", translate(language, "Research team")),
        "language": language,
        "start_page": start,
        "brand_color": front.get("theme-settings", {}).get("barcolor", "#315c8a"),
        "messages": {
            "previous": front.get("system-messages", {}).get("previous", translate(language, "Previous")),
            "next": front.get("system-messages", {}).get("next", translate(language, "Continue")),
            "required": front.get("system-messages", {}).get("required", translate(language, "Please answer the required questions before continuing.")),
        },
        "conditions": conditions,
        "progress_paths": paths,
        "pages": pages,
        "runtime_policy": {
            **({'prolific':prolific} if prolific else {}),
            "mode": config.get("respondents", {}).get("mode", "test"),
            "consent": ({
                "question": config.get("consent", {}).get("confirmation_question"),
                "accept_value": config.get("consent", {}).get("accept_value"),
                "refusal_outcome": config.get("consent", {}).get("refusal_outcome"),
            } if config.get("consent") else None),
            "respondent_source": config.get("respondents", {}).get("source", "direct_link"),
            "duplicate_policy": config.get("respondents", {}).get("duplicate_policy", "resume"),
        },
    }
    if assignment_page: model["assignment_page"] = assignment_page
    if randomizations: model["randomization"] = first
    shuffled_pages = page_plan(parsed, config)
    if shuffled_pages: model["shuffle_pages"] = shuffled_pages
    return model
