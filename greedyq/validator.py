"""Deterministic, researcher-readable validation for greedyQ v0.2 studies."""

import hashlib
import json
import re
from pathlib import Path
from .randomization import plan_problem, ordering_problems, boundary_problems, option_plan, page_plan
from .redirects import redirect_plan
from .compiler import condition as parse_condition
from .prolific import integration_plan


SUPPORTED_TYPES = {"text", "textarea", "numeric", "mc", "mc_multiple", "mc_buttons", "mc_multiple_buttons", "mc_image", "mc_multiple_image", "select", "slider", "slider_numeric", "date", "daterange", "matrix", "matrix_multiple", "audio", "video", "rank_order", "side_by_side", "nps", "timing", "constant_sum", "pick_group_rank", "drill_down", "custom"}
ID = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
FRONT_KEYS = {"title", "greedyq", "theme-settings", "survey-settings", "system-messages"}
NAMESPACE_KEYS = {
    "greedyq": {"spec_version", "version", "organization", "language"},
    "theme-settings": {"theme", "barposition", "barcolor", "footer", "footer-left", "footer-center", "footer-right"},
    "survey-settings": {"show-previous", "use-cookies", "all-required", "start-page", "highlight-unanswered", "capture-metadata", "required", "shuffled", "all-shuffled"},
    "system-messages": {"previous", "next", "required"},
}


def _item(code, message, path, line=None, severity="error", technical=None):
    item = {"code": code, "severity": severity, "message": message, "file": str(path)}
    if line: item["line"] = line
    if technical: item["technical_detail"] = technical
    return item


def validate(parsed, config, qmd_path="survey.qmd", config_path="greedyq.yml"):
    issues = []
    try: integration_plan(config)
    except (ValueError,TypeError) as exc: issues.append(_item('GQ020',str(exc),config_path))
    try: option_plan(parsed)
    except ValueError as exc: issues.append(_item("GQ007", str(exc), qmd_path))
    try: page_plan(parsed, config)
    except ValueError as exc: issues.append(_item("GQ007", str(exc), config_path))
    randomizations=config.get("randomization",[])
    if not isinstance(randomizations,list) or any(not isinstance(r,dict) for r in randomizations):
        return {"schema_version":"0.2","status":"failed","summary":"1 error(s), 0 warning(s)","issues":[_item("GQ007","randomization must be a list of assignment objects.",config_path)]}
    if any(not isinstance(r.get(k,{}),dict) for r in randomizations for k in ("conditions","store","assignment_point")):
        return {"schema_version":"0.2","status":"failed","summary":"1 error(s), 0 warning(s)","issues":[_item("GQ007","Random assignment conditions, store, and assignment_point must be objects.",config_path)]}
    pages = parsed.get("pages", [])
    page_ids = [p.get("id") for p in pages]
    known_pages = set(page_ids)
    questions = [q for p in pages for q in p.get("questions", [])]
    question_ids = [q.get("id") for q in questions]
    known_questions = set(question_ids)
    front = parsed.get("front_matter", {})
    for key in front:
        if key not in FRONT_KEYS:
            issues.append(_item("GQ003", "The survey header uses '%s', which is not a supported setting." % key, qmd_path, 1))
    for namespace,defaults in {'theme-settings':{'theme':'default','barposition':'top','footer':'','footer-left':'','footer-center':'','footer-right':''},'survey-settings':{'use-cookies':True,'highlight-unanswered':False,'capture-metadata':False}}.items():
        for key,default in defaults.items():
            if key in front.get(namespace,{}) and front[namespace][key]!=default:
                issues.append(_item('GQ120',"Setting '%s.%s' is not fully implemented in the browser runtime; review the compatibility audit."%(namespace,key),qmd_path,severity='warning'))
    for namespace, allowed in NAMESPACE_KEYS.items():
        value = front.get(namespace, {})
        if isinstance(value, dict):
            for key in value:
                if key not in allowed:
                    issues.append(_item("GQ003", "The '%s' section uses the unsupported setting '%s'." % (namespace, key), qmd_path, 1))
    if parsed.get("front_matter", {}).get("greedyq", {}).get("spec_version") != "0.2":
        issues.append(_item("GQ003", "Set the survey specification version to 0.2.", qmd_path, 1))
    if config.get("spec_version") != "0.2":
        issues.append(_item("GQ003", "Set the study settings version to 0.2.", config_path, 1))
    organization = front.get("greedyq", {}).get("organization")
    if front.get('greedyq', {}).get('language', 'en') not in ('en','ko','zh-CN','zh-TW'):
        issues.append(_item('GQ003', 'Choose en, ko, zh-CN or zh-TW for greedyq.language.', qmd_path, 1))
    if organization is not None and (not isinstance(organization, str) or not organization.strip() or len(organization) > 120):
        issues.append(_item("GQ003", "Set greedyq.organization to the researcher-facing organization or team name (1–120 characters).", qmd_path, 1))
    greedyq_version = front.get("greedyq", {}).get("version")
    if not isinstance(greedyq_version, str) or not re.fullmatch(r"0\.2_\d{4}-\d{2}-\d{2}_[0-9a-f]{7,12}", greedyq_version):
        issues.append(_item("GQ003", "Set greedyq.version to the exact release identifier shown at the top of the greedyQ repository (for example, 0.2_2026-09-09_abcdef0).", qmd_path, 1))
    for value in sorted({x for x in page_ids if page_ids.count(x) > 1}):
        issues.append(_item("GQ001", "The page name '%s' is used more than once. Give every page a unique name." % value, qmd_path))
    for value in sorted({x for x in question_ids if x and question_ids.count(x) > 1}):
        issues.append(_item("GQ001", "The question name '%s' is used more than once. Give every question a unique name." % value, qmd_path))
    for page in pages:
        if re.search(r"<\s*/?\s*[A-Za-z][^>]*>", page.get("body", "")):
            issues.append(_item("GQ003", "Page '%s' contains raw HTML. Use ordinary Markdown so the preview remains safe and portable." % page["id"], qmd_path))
    for q in questions:
        line = q.get("_line")
        if not q.get("id"):
            issues.append(_item("GQ001", "A question is missing its id. Add a short unique name such as 'age'.", qmd_path, line)); continue
        if not ID.fullmatch(str(q["id"])):
            issues.append(_item("GQ001", "The question id '%s' must begin with a letter and contain only lowercase letters, numbers, '_' or '-'." % q["id"], qmd_path, line))
        if not q.get("type"):
            issues.append(_item("GQ003", "Question '%s' is missing its type." % q["id"], qmd_path, line))
        elif q["type"] not in SUPPORTED_TYPES:
            issues.append(_item("GQ003", "Question '%s' uses the unsupported type '%s'." % (q["id"], q["type"]), qmd_path, line))
        if not q.get("label"):
            issues.append(_item("GQ003", "Question '%s' needs participant-facing wording in label." % q["id"], qmd_path, line))
        if q.get("type") in {"mc", "mc_multiple", "mc_buttons", "mc_multiple_buttons", "mc_image", "mc_multiple_image", "select", "slider", "matrix", "matrix_multiple"} and not q.get("options"):
            issues.append(_item("GQ003", "Question '%s' needs at least one answer choice." % q["id"], qmd_path, line))
        if q.get("type") in {"matrix", "matrix_multiple"} and not q.get("rows"):
            issues.append(_item("GQ003", "Matrix question '%s' needs at least one row." % q["id"], qmd_path, line))
        if q.get("type") in {"matrix", "matrix_multiple"} and q.get("mobile_columns", 3) not in (2, 3):
            issues.append(_item("GQ003", "Matrix question '%s' mobile_columns must be 2 or 3." % q["id"], qmd_path, line))
        if q.get("type") in {"audio", "video"} and not q.get("src"):
            issues.append(_item("GQ003", "Media control '%s' needs a safe source in src." % q["id"], qmd_path, line))
        if q.get("type") in {"mc_image", "mc_multiple_image"} and len(q.get("images", [])) != len(q.get("options", [])):
            issues.append(_item("GQ003", "Image question '%s' needs exactly one image for each answer choice." % q["id"], qmd_path, line))
        if q.get("direction") not in (None, "horizontal", "vertical"):
            issues.append(_item("GQ003", "Question '%s' uses an unsupported button direction." % q["id"], qmd_path, line))
        if q.get("resize") not in (None, "none", "both", "horizontal", "vertical"):
            issues.append(_item("GQ003", "Question '%s' uses an unsupported textarea resize setting." % q["id"], qmd_path, line))
        for dimension in ("width", "height"):
            if q.get(dimension) is not None and not re.fullmatch(r"\d+(?:\.\d+)?(?:px|%|rem|em|vw|vh)", str(q[dimension])):
                issues.append(_item("GQ003", "Question '%s' needs a safe CSS %s such as '100%%' or '120px'." % (q["id"], dimension), qmd_path, line))
        for image in q.get("images", []):
            if not (str(image).startswith("https://") or re.fullmatch(r"(?!/)(?!.*\.\.)[A-Za-z0-9_./-]+", str(image))):
                issues.append(_item("GQ003", "Image question '%s' contains an unsafe image path." % q["id"], qmd_path, line))
        for media_key in ("src", "poster"):
            media = q.get(media_key)
            if media is not None and not (str(media).startswith("https://") or re.fullmatch(r"(?!/)(?!.*\.\.)[A-Za-z0-9_./-]+", str(media))):
                issues.append(_item("GQ003", "Media control '%s' contains an unsafe %s path." % (q["id"], media_key), qmd_path, line))
        if q.get("type") in {"audio", "video"} and q.get("autoplay") and not q.get("muted"):
            issues.append(_item("GQ003", "Media control '%s' may autoplay only when muted." % q["id"], qmd_path, line))
        if q.get("type") in {"rank_order", "constant_sum", "pick_group_rank", "drill_down"} and len(q.get("options", [])) < 2:
            issues.append(_item("GQ003", "Question '%s' needs at least two items." % q["id"], qmd_path, line))
        if q.get("type") == "side_by_side" and (not q.get("rows") or not q.get("options") or not q.get("columns")):
            issues.append(_item("GQ003", "Side-by-side question '%s' needs rows, columns, and answer choices." % q["id"], qmd_path, line))
        if q.get("type") == "pick_group_rank" and len(q.get("groups", [])) < 2:
            issues.append(_item("GQ003", "Pick, group, and rank question '%s' needs at least two groups." % q["id"], qmd_path, line))
        if q.get("type") == "constant_sum" and (not isinstance(q.get("total", 100), (int, float)) or q.get("total", 100) <= 0):
            issues.append(_item("GQ003", "Constant-sum question '%s' needs a positive total." % q["id"], qmd_path, line))
        if q.get("type") == "custom" and q.get("base_type") not in SUPPORTED_TYPES - {"custom", "timing", "audio", "video"}:
            issues.append(_item("GQ003", "Custom question '%s' must name a supported response control in base_type." % q["id"], qmd_path, line))
        if q.get("type") == "slider_numeric" and isinstance(q.get("default"), list) and len(q["default"]) not in (1, 2):
            issues.append(_item("GQ003", "Numeric slider '%s' default must contain one value or two range endpoints." % q["id"], qmd_path, line))
        if q.get("type") == "slider" and len(q.get("options", [])) < 2:
            issues.append(_item("GQ003", "Slider question '%s' needs at least two ordered choices." % q["id"], qmd_path, line))
        if q.get("type") == "slider_numeric" and q.get("min") is not None and q.get("max") is not None and q["min"] >= q["max"]:
            issues.append(_item("GQ003", "Numeric slider '%s' needs a maximum greater than its minimum." % q["id"], qmd_path, line))
        if q.get("orientation") not in (None, "horizontal", "vertical"):
            issues.append(_item("GQ003", "Question '%s' uses an unsupported slider orientation." % q["id"], qmd_path, line))
        if any(item.get("_looks_reversed") for item in q.get("options", []) + q.get("rows", [])):
            issues.append(_item("GQ011", "Question '%s' appears to put stored codes on the left. Write each choice as \"Displayed label\" = \"stored_value\"." % q["id"], qmd_path, line))
        for arg in q.get("unsupported_arguments", []):
            issues.append(_item("GQ003", "Question '%s' uses '%s', which this preview does not support yet." % (q["id"], arg), qmd_path, line))
        for collection in ("options", "rows", "columns", "groups"):
            values = [item.get("value") for item in q.get(collection, [])]
            if len(values) != len(set(map(str, values))):
                issues.append(_item("GQ011", "Question '%s' repeats a stored value in its %s. Every stored value must be unique." % (q["id"], collection), qmd_path, line))
    for page in pages:
        nav = page.get("nav", {})
        for key in ("previous_mode", "next_mode"):
            if nav.get(key) not in (None, "show", "hide", "disable"):
                issues.append(_item("GQ003", "Page '%s' uses an unsupported %s. Choose show, hide, or disable." % (page["id"], key), qmd_path, page.get("_nav_line")))
        delay = nav.get("next_delay_seconds", 0)
        if not isinstance(delay, (int, float)) or delay < 0 or delay > 86400:
            issues.append(_item("GQ003", "Page '%s' needs next_delay_seconds between 0 and 86400." % page["id"], qmd_path, page.get("_nav_line")))
    overlap = sorted(known_pages & known_questions)
    for value in overlap:
        issues.append(_item("GQ001", "'%s' is used for both a page and a question. Use a different name for one of them." % value, qmd_path))
    settings = parsed.get("front_matter", {}).get("survey-settings", {})
    start = settings.get("start-page", page_ids[0] if page_ids else None)
    if start not in known_pages:
        issues.append(_item("GQ002", "The starting page '%s' does not exist." % start, qmd_path))
    for required in settings.get("required", []) or []:
        if required not in known_questions:
            issues.append(_item("GQ002", "The required-question list refers to '%s', but that question does not exist." % required, qmd_path))
    logic = config.get("logic", {})
    choices = {q["id"]: {str(item.get("value")) for item in q.get("options", [])} for q in questions if q.get("id")}
    derived_fields = {item.get("store", {}).get("condition_as") for item in config.get("randomization", []) or []}
    derived_fields.discard(None)
    def check_condition(condition, rule_id=None):
        before=len(issues)
        def inspect(node):
            if 'all' in node or 'any' in node:
                for child in node.get('all',node.get('any',[])):inspect(child)
            elif 'not' in node:inspect(node['not'])
            elif 'unsupported' in node or not re.fullmatch(r'[a-z][a-z0-9_]*',node.get('field','')) or any(k in node and type(node[k]) not in (int,float) for k in ('lt','lte','gt','gte')):
                issues.append(_item('GQ011','Use a supported condition, for example contains(tools, \"other\"), length(tools) >= 2, age >= 18 or answered(question). Arbitrary expressions are not executed.',config_path))
            elif node['field'] not in known_questions and node['field'] not in derived_fields and node['field']!='condition':
                issues.append(_item('GQ011',"A condition refers to '%s', but that question does not exist."%node['field'],config_path))
            if 'length' in node and (not isinstance(node['length'],dict) or any(type(v) not in (int,float) for v in node['length'].values())):
                issues.append(_item('GQ011','length() must compare a collection length with a number.',config_path))
            if 'contains' in node or 'in' in node:
                literals=node.get('in',[node.get('contains')])
                if not isinstance(literals,list) or any(isinstance(v,(dict,list)) for v in literals):issues.append(_item('GQ011','Membership requires scalar stored values.',config_path))
                elif choices.get(node.get('field')):
                    for v in literals:
                        if v is not None and str(v) not in choices[node['field']]:issues.append(_item('GQ011',"A condition compares '%s' with '%s', which is not one of its stored answer values."%(node['field'],v),config_path))
            if 'length' in node:
                q=next((q for q in questions if q.get('id')==node.get('field')),{})
                if (q.get('base_type') if q.get('type')=='custom' else q.get('type')) not in ('text','textarea','mc_multiple','mc_multiple_buttons','mc_multiple_image','select_multiple','slider','date'):
                    issues.append(_item('GQ011','length() requires text or a multiple-selection question.',config_path))
            if 'contains' in node:
                q=next((q for q in questions if q.get('id')==node.get('field')),{})
                if (q.get('base_type') if q.get('type')=='custom' else q.get('type')) not in ('mc_multiple','mc_multiple_buttons','mc_multiple_image','select_multiple'):issues.append(_item('GQ011','contains() requires a multiple-selection question.',config_path))
        inspect(parse_condition(condition))
        for field, literal in re.findall(r"\b([a-z][a-z0-9_]*)\s*(?:==|!=)\s*['\"]([^'\"]+)['\"]", str(condition or "")):
            if field not in known_questions and field not in derived_fields:
                issues.append(_item("GQ011", "A condition refers to '%s', but that question does not exist." % field, config_path))
            elif choices.get(field) and literal not in choices[field]:
                issues.append(_item("GQ011", "A condition compares '%s' with '%s', which is not one of its stored answer values." % (field, literal), config_path))
        if rule_id:
            for item in issues[before:]:item['message']="Rule '%s': %s"%(rule_id,item['message'])
    for rule in logic.get("show", []) or []:
        target = rule.get("question") or rule.get("page")
        known = known_questions if rule.get("question") else known_pages
        if target not in known:
            issues.append(_item("GQ002", "A display rule refers to '%s', but it does not exist." % target, config_path))
        check_condition(rule.get("if"),rule.get("id") or rule.get("question") or rule.get("from"))
    for rule in logic.get("skip", []) or []:
        if rule.get("from") not in known_pages:
            issues.append(_item("GQ002", "A route starts from missing page '%s'." % rule.get("from"), config_path))
        if rule.get("to") not in known_pages:
            issues.append(_item("GQ002", "A route points to missing page '%s'." % rule.get("to"), config_path))
        check_condition(rule.get("if"),rule.get("id") or rule.get("question") or rule.get("from"))
    for page in pages:
        target = (page.get("nav") or {}).get("page_next")
        if target and target not in known_pages:
            issues.append(_item("GQ002", "Page '%s' continues to missing page '%s'." % (page["id"], target), qmd_path, page.get("_nav_line")))
    for rule in logic.get('validate',[]) or []:
        check_condition(rule.get('if'),rule.get('id') or rule.get('question') or rule.get('from'))
        if rule.get('question') not in known_questions:issues.append(_item('GQ002','A validation rule refers to a missing question.',config_path))
    for outcome, value in (config.get("outcomes", {}) or {}).items():
        if value.get("page") not in known_pages:
            issues.append(_item("GQ002", "The '%s' ending points to missing page '%s'." % (outcome, value.get("page")), config_path))
    if len(config.get("randomization", []) or []) > 1:
        issues.append(_item("GQ007", "Only one between-subject random assignment is supported per study.", config_path))
    for randomization in config.get("randomization", []) or []:
        problem = plan_problem(randomization)
        if problem: issues.append(_item("GQ007", problem, config_path))
        after = (randomization.get("assignment_point") or {}).get("after_page")
        if after not in known_pages:
            issues.append(_item("GQ002", "Random assignment refers to missing page '%s'." % after, config_path))
        if len(randomization.get("conditions", {})) < 2:
            issues.append(_item("GQ007", "Random assignment '%s' needs at least two conditions." % randomization.get("id"), config_path))
        if not randomization.get("persistence_key") or not randomization.get("store", {}).get("condition_as"):
            issues.append(_item("GQ007", "Random assignment '%s' must save each participant's condition so it cannot change on resume." % randomization.get("id"), config_path))
    for problem in boundary_problems(parsed, config) + ordering_problems(parsed, config):
        issues.append(_item("GQ007", problem, config_path))
    consent = config.get("consent")
    if consent:
        confirmation = consent.get("confirmation_question")
        if confirmation not in known_questions:
            issues.append(_item("GQ006", "Consent refers to missing question '%s'." % confirmation, config_path))
        else:
            question = next(q for q in questions if q.get("id") == confirmation)
            values = [item.get("value") for item in question.get("options", [])]
            if consent.get("accept_value") not in values:
                issues.append(_item("GQ006", "The configured consent answer '%s' is not an option in question '%s'." % (consent.get("accept_value"), confirmation), config_path))
    for name, outcome in (config.get("outcomes", {}) or {}).items():
        try: redirect_plan(outcome)
        except ValueError as exc: issues.append(_item("GQ009", str(exc), config_path))
        redirect = outcome.get("redirect")
        if redirect and not str(redirect).startswith("https://"):
            issues.append(_item("GQ009", "The '%s' redirect must use a secure https address." % name, config_path))
    errors = [item for item in issues if item["severity"] == "error"]
    return {"schema_version": "0.2", "status": "passed" if not errors else "failed", "summary": "%d error(s), %d warning(s)" % (len(errors), len(issues)-len(errors)), "issues": issues}


STATE_CONTRACTS = {
    "study-state.json": {"schema_version", "study_id", "study_version", "guide_version", "spec_version", "mode", "phase", "status", "checkpoint", "gates", "confirmed_decision_ids", "unresolved_decision_ids", "assumptions", "artifact_paths"},
    "decision-log.json": {"schema_version", "study_id", "append_only", "decisions"},
    "unresolved-decisions.json": {"schema_version", "study_id", "items"},
    "generation-manifest.json": {"schema_version", "study_id", "study_version", "guide_version", "spec_version", "artifacts", "external_operations"},
    "validation-report.json": {"schema_version", "study_id", "study_version", "overall_status", "checks", "manual_gates"},
}


def validate_state_artifacts(study_dir):
    """Check durable AI-state contracts and generation-manifest hashes."""
    root = Path(study_dir)
    state = root / ".greedyq"
    issues = []
    for name, required in STATE_CONTRACTS.items():
        path = state / name
        if not path.is_file():
            issues.append(_item("GQ012", "The study is missing its %s record." % name, path))
            continue
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            issues.append(_item("GQ012", "%s is not valid JSON." % name, path))
            continue
        missing = sorted(required - set(data)) if isinstance(data, dict) else sorted(required)
        if missing:
            issues.append(_item("GQ012", "%s is missing: %s." % (name, ", ".join(missing)), path))
        if isinstance(data, dict) and data.get("schema_version") != "0.2":
            issues.append(_item("GQ012", "%s must use schema_version 0.2." % name, path))
        if name == "generation-manifest.json" and isinstance(data, dict):
            for artifact in data.get("artifacts", []):
                relative, expected = artifact.get("path"), artifact.get("sha256")
                target = (root / str(relative or "")).resolve()
                if not relative or not target.is_relative_to(root.resolve()) or not target.is_file():
                    issues.append(_item("GQ012", "The generation manifest refers to a missing artifact: %s." % relative, path))
                elif expected and hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                    issues.append(_item("GQ012", "The generated artifact '%s' changed after its manifest was recorded." % relative, path))
    return {"status": "passed" if not issues else "failed", "issues": issues}
