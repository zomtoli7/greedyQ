"""Reference assignment and question-order algorithms; injectable draws for conformance."""
import secrets
import re


def plan_problem(plan):
    if not isinstance(plan, dict): return "Random assignment must be an object."
    if not re.fullmatch(r"[a-z][a-z0-9_]*",str(plan.get("id",""))): return "Random assignment needs a stable lowercase ID."
    if set(plan)-{"id","method","unit","conditions","block_size","assignment_point","persistence_key","source_file","store"}: return "Random assignment contains unsupported settings."
    if plan.get("method") not in ("simple", "fixed_block"): return "Choose simple or fixed_block random assignment."
    if plan.get("unit") != "respondent" or plan.get("persistence_key") != "session_id":
        return "Random assignment currently requires respondent units and session_id persistence."
    weights = plan.get("conditions")
    if not isinstance(weights, dict) or len(weights) < 2 or any(type(w) is not int or w < 1 for w in weights.values()) or sum(weights.values()) > 1000:
        return "Condition weights must be positive integers with a total no greater than 1000."
    if any(not re.fullmatch(r"[a-z][a-z0-9_]*",str(k)) for k in weights): return "Condition IDs must use lowercase letters, digits, and underscores."
    if plan.get("method") == "fixed_block":
        size = plan.get("block_size")
        if type(size) is not int or not 2 <= size <= 1000 or size % sum(weights.values()):
            return "Block size must be a multiple of the total condition weights, between 2 and 1000."
    elif "block_size" in plan:
        return "Simple random assignment must not specify block_size."
    return None


def shuffle(items, randbelow=secrets.randbelow):
    result = list(items)
    for i in range(len(result) - 1, 0, -1):
        j = randbelow(i + 1)
        result[i], result[j] = result[j], result[i]
    return result


def draw(plan, sequence, randbelow=secrets.randbelow):
    """sequence is durable private allocation state, never inferred from surviving answers."""
    problem = plan_problem(plan)
    if problem: raise ValueError(problem)
    weights = dict(sorted(plan["conditions"].items()))
    if plan["method"] == "simple":
        n = randbelow(sum(weights.values()))
        for condition, weight in weights.items():
            n -= weight
            if n < 0: return condition, None
    if not sequence.get("remaining"):
        repeats = plan["block_size"] // sum(weights.values())
        sequence["remaining"] = shuffle([c for c, w in weights.items() for _ in range(w * repeats)], randbelow)
        sequence["block"] = sequence.get("block", 0) + 1
    return sequence["remaining"].pop(0), str(sequence["block"])


def question_order(page, randbelow=secrets.randbelow):
    ids = [q["id"] for q in page.get("questions", [])]
    selected = page.get("shuffle_questions", [])
    shuffled = iter(shuffle(selected, randbelow))
    return [next(shuffled) if q in selected else q for q in ids]


SHUFFLE_TYPES = {"mc", "mc_buttons", "mc_multiple", "mc_multiple_buttons", "matrix"}


def option_plan(parsed):
    """Surveydown public shuffled/all-shuffled syntax; one-based positions."""
    settings = parsed.get("front_matter", {}).get("survey-settings", {})
    questions = {q["id"]: q for p in parsed["pages"] for q in p["questions"]}
    plans = {}
    if type(settings.get("all-shuffled", False)) is not bool:
        raise ValueError("all-shuffled must be true or false.")
    if settings.get("all-shuffled"):
        plans = {k: None for k, q in questions.items() if q["type"] in SHUFFLE_TYPES}
    entries = settings.get("shuffled", [])
    if not isinstance(entries, list): raise ValueError("shuffled must be a list.")
    seen = set()
    for entry in entries:
        if isinstance(entry, str): key, positions = entry, None
        elif isinstance(entry, dict) and len(entry) == 1: key, positions = next(iter(entry.items()))
        else: raise ValueError("Each shuffled entry must name one question.")
        if key in seen: raise ValueError("Do not repeat a question in shuffled.")
        seen.add(key)
        if key not in questions or questions[key]["type"] not in SHUFFLE_TYPES:
            raise ValueError("shuffled supports mc, mc_buttons, mc_multiple, mc_multiple_buttons and matrix.")
        plans[key] = positions
    result = {}
    for key, positions in plans.items():
        q = questions[key]
        items = q.get("rows" if q["type"] == "matrix" else "options", [])
        indices = list(range(1, len(items) + 1)) if positions is None else []
        for part in ([] if positions is None else positions if isinstance(positions, list) else [positions]):
            if type(part) is int: indices.append(part)
            elif isinstance(part, str) and re.fullmatch(r"[1-9]\d*-[1-9]\d*", part):
                a, b = map(int, part.split("-"))
                if a > b or b > len(items): raise ValueError("Shuffle positions must be inside the question and ascending.")
                indices.extend(range(a, b + 1))
            else: raise ValueError("Use positive positions or ascending ranges for shuffled.")
        if not indices or len(set(indices)) != len(indices) or any(i < 1 or i > len(items) for i in indices):
            raise ValueError("Shuffle positions must be distinct and inside the question.")
        result[key] = [items[i - 1]["value"] for i in indices]
    return result


def option_order(question, randbelow=secrets.randbelow):
    items = question.get("rows" if question["type"] == "matrix" else "options", [])
    selected = question.get("shuffle_items", [])
    shuffled = iter(shuffle(selected, randbelow))
    return [next(shuffled) if item["value"] in selected else item["value"] for item in items]


def page_plan(parsed, config):
    selected = config.get("page_order", [])
    if not isinstance(selected, list) or any(not isinstance(p, str) for p in selected):
        raise ValueError("page_order must be a list of page IDs.")
    if not selected: return []
    pages = parsed["pages"]; ids = [p["id"] for p in pages]
    if parsed.get("front_matter",{}).get("survey-settings",{}).get("start-page",ids[0])!=ids[0]:
        raise ValueError("Page shuffling must start at the fixed opening page.")
    if len(selected) < 2 or len(set(selected)) != len(selected) or any(p not in ids for p in selected):
        raise ValueError("Choose at least two distinct existing pages for page_order.")
    positions = sorted(ids.index(p) for p in selected)
    if positions != list(range(positions[0], positions[-1] + 1)) or positions[0] == 0 or positions[-1] == len(ids)-1:
        raise ValueError("Shuffle one contiguous group between fixed opening and ending pages.")
    protected = {o.get("page") for o in config.get("outcomes", {}).values()}
    consent = config.get("consent", {}).get("confirmation_question")
    protected.update(p["id"] for p in pages if any(q["id"] == consent for q in p["questions"]))
    for r in config.get("randomization", []):
        protected.add(r.get("assignment_point", {}).get("after_page"))
        protected.update(r.get("assignment_point", {}).get("before_condition_pages", []))
    if protected.intersection(selected): raise ValueError("Keep consent, assignment, condition and ending pages fixed.")
    members = [p for p in pages if p["id"] in selected]
    if any(p.get("nav", {}).get("page_next") for p in members):
        raise ValueError("Shuffled pages must use automatic next-page navigation.")
    if config.get("logic", {}).get("skip") or config.get("logic", {}).get("show"):
        raise ValueError("Page shuffling currently requires an independent linear survey without skip/show rules.")
    # Prevent incoming explicit links from bypassing the first shuffled page.
    if any(p.get("nav", {}).get("page_next") for p in pages):
        raise ValueError("Remove explicit incoming links to shuffled pages.")
    return [p for p in ids if p in selected]


def page_order(model, randbelow=secrets.randbelow):
    selected = model.get("shuffle_pages", [])
    randomized = iter(shuffle(selected, randbelow))
    return [next(randomized) if p["id"] in selected else p["id"] for p in model["pages"]]


def ordering_problems(parsed, config):
    problems, seen = [], set()
    pages = {p["id"]: p for p in parsed["pages"]}
    rules = config.get("question_order", [])
    if not isinstance(rules, list): return ["question_order must be a list of page/question groups."]
    for rule in rules:
        if not isinstance(rule, dict):
            problems.append("Each question_order entry must identify a page and questions."); continue
        page, selected = pages.get(rule.get("page")), rule.get("questions")
        if set(rule)-{"page","questions"}:
            problems.append("Question shuffling contains unsupported settings.")
        if not page or rule.get("page") in seen:
            problems.append("Question shuffling requires one group per existing page."); continue
        seen.add(rule["page"])
        ids = [q["id"] for q in page["questions"]]
        if not isinstance(selected, list) or len(selected) < 2 or any(not isinstance(x, str) or x not in ids for x in selected) or len(set(selected)) != len(selected):
            problems.append("Choose at least two distinct questions on the same page to shuffle."); continue
        consent = config.get("consent", {}).get("confirmation_question")
        if consent in ids:
            problems.append("Keep the consent page in its approved fixed order.")
        # Conditional source/target relationships must not be reversed by shuffling.
        import re
        for show in config.get("logic", {}).get("show", []) or []:
            refs = re.findall(r"[a-z][a-z0-9_]*", str(show.get("if", "")))
            if show.get("question") in ids and any(ref in ids for ref in refs) and (show.get("question") in selected or any(ref in selected for ref in refs)):
                problems.append("Keep dependent questions and their same-page trigger questions outside shuffled groups.")
    return problems


def boundary_problems(parsed, config):
    ids=[p["id"] for p in parsed["pages"]]; problems=[]
    consent=config.get("consent",{}).get("confirmation_question")
    consent_page=next((p["id"] for p in parsed["pages"] if any(q["id"]==consent for q in p["questions"])),None)
    for plan in config.get("randomization",[]) or []:
        after=plan.get("assignment_point",{}).get("after_page")
        if after not in ids: continue
        if consent_page and ids.index(after)<ids.index(consent_page): problems.append("Place random assignment after consent, not before it.")
        targets=plan.get("assignment_point",{}).get("before_condition_pages",[])
        if not isinstance(targets,list) or not targets or any(t not in ids or ids.index(t)<=ids.index(after) for t in targets):
            problems.append("List the condition pages after the assignment boundary.")
    return problems
