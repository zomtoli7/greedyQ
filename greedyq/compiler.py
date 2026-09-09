"""Compile parsed QMD and greedyq.yml into the browser preview model."""

import re


OPS = (("!=", "not_equals"), ("<=", "lte"), (">=", "gte"), ("==", "equals"), ("<", "lt"), (">", "gt"))


def _literal(raw):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'": return raw[1:-1]
    if re.fullmatch(r"-?\d+", raw): return int(raw)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", raw): return float(raw)
    if raw.lower() == "true": return True
    if raw.lower() == "false": return False
    return raw


def condition(expression):
    """Convert the safe comparison subset to preview predicates."""
    expression = str(expression).strip()
    for connector, key in ((" and ", "all"), (" or ", "any")):
        if connector in expression:
            return {key: [condition(part) for part in expression.split(connector)]}
    for token, key in OPS:
        if token in expression:
            field, value = expression.split(token, 1)
            field = field.strip()
            if field == "assignment_condition": field = "condition"
            return {"field": field, key: _literal(value)}
    return {"unsupported": expression}


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
    front = parsed["front_matter"]
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
        page["questions"] = []
        for source_question in source["questions"]:
            q = {key: value for key, value in source_question.items() if not key.startswith("_") and key != "unsupported_arguments"}
            for collection in ("options", "rows", "columns", "groups"):
                if collection in q:
                    q[collection] = [{key: value for key, value in item.items() if not key.startswith("_")} for item in q[collection]]
            q["required"] = q.get("id") in required
            for rule in shows:
                if rule.get("question") == q.get("id"): q["show_if"] = condition(rule.get("if", ""))
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
                routes.append({"when": condition(rule.get("if", "")), "to": rule.get("to")})
        if routes: page["routes"] = routes
        if page["id"] in terminal_by_page:
            page.pop("next", None); page["terminal"] = terminal_by_page[page["id"]]
        pages.append(page)

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
        "title": config.get("study", {}).get("title", front.get("title", "greedyQ Survey")),
        "organization": front.get("greedyq", {}).get("organization", "Research team"),
        "start_page": start,
        "brand_color": front.get("theme-settings", {}).get("barcolor", "#315c8a"),
        "messages": {
            "previous": front.get("system-messages", {}).get("previous", "Previous"),
            "next": front.get("system-messages", {}).get("next", "Continue"),
            "required": front.get("system-messages", {}).get("required", "Please answer the required questions before continuing."),
        },
        "conditions": conditions,
        "progress_paths": paths,
        "pages": pages,
        "runtime_policy": {
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
    return model
