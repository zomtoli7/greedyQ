"""Generate an independent native surveydown project and compatibility report."""

import json
import re
import shutil
from pathlib import Path


CUSTOM_TYPES = {
    "audio", "video", "rank_order", "side_by_side", "nps", "timing",
    "constant_sum", "pick_group_rank", "drill_down", "custom",
}

APP_HEADER = '''# Generated independently by greedyQ {version}.
# Review and test this native surveydown export before fielding.
library(shiny)
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()
server <- function(input, output, session) {{
{bindings}
  sd_server(db = db)
}}
shiny::shinyApp(ui = ui, server = server)
'''


def _r(value):
    """Encode the small scalar/vector subset used by generated R code."""
    if value is None:
        return "NULL"
    if value is True:
        return "TRUE"
    if value is False:
        return "FALSE"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "c(" + ", ".join(_r(item) for item in value) + ")"
    return json.dumps(str(value), ensure_ascii=False)


def _named_values(items):
    return "c(" + ", ".join(f"{_r(item['label'])} = {_r(item['value'])}" for item in items) + ")"


def _safe_id(value):
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def _custom_call(question):
    qid = question["id"]
    return f"sd_output({_r(qid)}, type = \"question\")"


def _condition_r(expression, derived_fields=frozenset()):
    """Translate the deliberately small greedyQ condition language to safe R."""
    expression = str(expression or "").strip()
    parts = re.split(r"\s+(and|or)\s+", expression)
    if len(parts) > 1:
        rendered = [_condition_r(part, derived_fields) if part not in ("and", "or") else ("&" if part == "and" else "|") for part in parts]
        return "(" + " ".join(rendered) + ")"
    answered = re.fullmatch(r"(not\s+)?answered\(([a-z][a-z0-9_]*)\)", expression)
    if answered:
        return ("!" if answered.group(1) else "") + f"sd_is_answered({_r(answered.group(2))})"
    comparison = re.fullmatch(r"([a-z][a-z0-9_]*)\s*(==|!=|<=|>=|<|>)\s*(.+)", expression)
    if not comparison:
        raise ValueError(f"Unsupported export condition: {expression}")
    field, operator, raw = comparison.groups()
    raw = raw.strip()
    if raw[:1] in ("'", '"') and raw[-1:] == raw[:1]:
        value = _r(raw[1:-1])
    elif re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        value = raw
    else:
        raise ValueError(f"Unsupported export condition value: {raw}")
    source = field if field in derived_fields else f"sd_value({_r(field)})"
    return f"({source} {operator} {value})"


def _workflow_bindings(config):
    randomizations = config.get("randomization", []) or []
    derived = {item.get("store", {}).get("condition_as") for item in randomizations}
    derived.discard(None)
    lines = []
    for randomization in randomizations:
        field = randomization.get("store", {}).get("condition_as")
        conditions = list((randomization.get("conditions") or {}).keys())
        if field and conditions:
            lines.extend([
                f"  {field} <- sample({_r(conditions)}, 1)",
                f"  sd_store_value({field})",
            ])
    show_rules = config.get("logic", {}).get("show", []) or []
    if show_rules:
        formulas = [f"{_condition_r(rule.get('if'), derived)} ~ {_r(rule.get('question') or rule.get('page'))}" for rule in show_rules]
        lines.append("  sd_show_if(\n    " + ",\n    ".join(formulas) + "\n  )")
    # Randomized page branches are represented by sd_show_if() above. Emitting
    # the same derived-field branch as a global sd_skip_if() would make it true
    # from the first page and could jump past all preceding pages.
    skip_rules = [
        rule for rule in sorted(config.get("logic", {}).get("skip", []) or [], key=lambda item: -item.get("priority", 0))
        if not any(re.search(rf"\b{re.escape(field)}\b", str(rule.get("if", ""))) for field in derived)
    ]
    if skip_rules:
        formulas = [f"{_condition_r(rule.get('if'), derived)} ~ {_r(rule.get('to'))}" for rule in skip_rules]
        lines.append("  sd_skip_if(\n    " + ",\n    ".join(formulas) + "\n  )")
    validation_rules = config.get("logic", {}).get("validate", []) or []
    if validation_rules:
        formulas = [f"{_condition_r(rule.get('if'), derived)} ~ {_r(rule.get('message', 'Please review this answer.'))}" for rule in validation_rules]
        lines.append("  sd_stop_if(\n    " + ",\n    ".join(formulas) + "\n  )")
    return "\n".join(lines)


def _replace_question_block(text, question):
    qid = re.escape(str(question["id"]))
    pattern = re.compile(
        r"```\{r\}\s*\n(?P<body>\s*sd_question\s*\((?:(?!```)[\s\S])*?\bid\s*=\s*['\"]"
        + qid + r"['\"](?:(?!```)[\s\S])*?\)\s*)```"
    )
    replacement = "```{r}\n" + _custom_call(question) + "\n```"
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise ValueError(f"Could not locate custom-control question block: {question['id']}")
    return updated


def _remove_scalar_arguments(text, question_id, names):
    """Remove greedyQ-only scalar arguments from one preserved native call."""
    qid = re.escape(str(question_id))
    pattern = re.compile(
        r"```\{r\}\s*\n(?P<body>\s*sd_question\s*\((?:(?!```)[\s\S])*?\bid\s*=\s*['\"]"
        + qid + r"['\"](?:(?!```)[\s\S])*?\)\s*)```",
        re.S,
    )
    match = pattern.search(text)
    if not match:
        return text
    body = match.group("body")
    for name in names:
        body = re.sub(r",\s*" + re.escape(name) + r"\s*=\s*[^,)\n]+", "", body)
    return text[:match.start("body")] + body + text[match.end("body"):]


def _rewrite_nav_extensions(text):
    """Translate safe navigation subsets and remove greedyQ-only arguments."""
    pattern = re.compile(r"(```\{r\}\s*\n)(?P<body>\s*sd_nav\s*\((?:(?!```)[\s\S])*?\)\s*)(```)")
    def replace(match):
        body = match.group("body")
        previous = re.search(r"previous_mode\s*=\s*['\"](show|hide|disable)['\"]", body)
        next_mode = re.search(r"next_mode\s*=\s*['\"](show|hide|disable)['\"]", body)
        body = re.sub(r",?\s*previous_mode\s*=\s*['\"](?:show|hide|disable)['\"]", "", body)
        body = re.sub(r",?\s*next_mode\s*=\s*['\"](?:show|hide|disable)['\"]", "", body)
        body = re.sub(r",?\s*next_delay_seconds\s*=\s*[^,)\n]+", "", body)
        additions = []
        if previous and previous.group(1) != "show" and "show_previous" not in body:
            additions.append("show_previous = FALSE")
        if next_mode and next_mode.group(1) != "show" and "show_next" not in body:
            additions.append("show_next = FALSE")
        if additions:
            separator = "" if re.search(r"\(\s*\)\s*$", body) else ", "
            body = re.sub(r"\)\s*$", separator + ", ".join(additions) + ")", body)
        return match.group(1) + body.rstrip() + "\n" + match.group(3)
    return pattern.sub(replace, text)


def _force_preview_mode(text):
    """Keep generated native projects safe for local review by default."""
    close = text.find("\n---", 4)
    if close < 0:
        raise ValueError("Native Surveydown export requires YAML front matter.")
    header, remainder = text[:close], text[close:]
    if not re.search(r"(?m)^format:\s*", header):
        header = header.replace("---\n", "---\nformat: html\n", 1)
    text = header + remainder
    pattern = re.compile(r"(?m)^(survey-settings:\s*\n)((?:[ \t]+.*(?:\n|$))*)")
    match = pattern.search(text)
    if not match:
        raise ValueError("Native Surveydown export requires a survey-settings YAML section.")
    body = match.group(2)
    if re.search(r"(?m)^\s+mode:\s*", body):
        body = re.sub(r"(?m)^(\s+)mode:\s*.*$", r"\1mode: preview", body, count=1)
    else:
        body = "  mode: preview\n" + body
    text = text[:match.start()] + match.group(1) + body + text[match.end():]
    close = text.find("\n---", 4)
    first_page = re.search(r"(?m)^---\s+[A-Za-z][A-Za-z0-9_-]*\s*$", text[close + 4:])
    prefix_end = close + 4 + (first_page.start() if first_page else 0)
    prefix = text[:prefix_end]
    if not re.search(r"library\(\s*surveydown\s*\)", prefix):
        setup = "\n\n```{r}\nlibrary(surveydown)\n```\n\n"
        text = text[:close + 4] + setup + text[close + 4:].lstrip("\n")
    return text


def _output_binding(question):
    qid = _safe_id(question["id"])
    qtype = question["type"]
    output_id = f"gq_{qid}_output"
    value_id = f"gq_{qid}_value"
    options = question.get("options", [])
    rows = question.get("rows", [])
    columns = question.get("columns", [])
    groups = question.get("groups", [])

    if qtype in ("audio", "video"):
        tag = "audio" if qtype == "audio" else "video"
        attrs = [f"src = {_r(question.get('src', ''))}", "controls = NA"]
        if qtype == "video" and question.get("poster"):
            attrs.append(f"poster = {_r(question['poster'])}")
        ui = f"tags${tag}({', '.join(attrs)}, style = 'max-width:100%;')"
        value = "reactive(NULL)"
    elif qtype == "nps":
        lo, hi = int(question.get("min", 0)), int(question.get("max", 10))
        ui = f"radioButtons({_r(qid)}, NULL, choices = c({', '.join(map(str, range(lo, hi + 1)))}), inline = TRUE)"
        value = f"reactive(input${qid})"
    elif qtype == "rank_order":
        controls = []
        for item in options:
            iid = f"{qid}_{_safe_id(str(item['value']))}"
            controls.append(f"selectInput({_r(iid)}, {_r(item['label'])}, choices = 1:{len(options)})")
        ui = "tagList(" + ", ".join(controls) + ")"
        pairs = ", ".join(f"{_r(str(i['value']))} = input${qid}_{_safe_id(str(i['value']))}" for i in options)
        value = f"reactive(list({pairs}))"
    elif qtype == "constant_sum":
        controls = []
        for item in options:
            iid = f"{qid}_{_safe_id(str(item['value']))}"
            controls.append(f"numericInput({_r(iid)}, {_r(item['label'])}, value = 0, min = 0)")
        ui = "tagList(" + ", ".join(controls) + ")"
        pairs = ", ".join(f"{_r(str(i['value']))} = input${qid}_{_safe_id(str(i['value']))}" for i in options)
        value = f"reactive(list({pairs}))"
    elif qtype == "side_by_side":
        controls, pairs = [], []
        for column in columns:
            for row in rows:
                iid = f"{qid}_{_safe_id(str(column['value']))}_{_safe_id(str(row['value']))}"
                controls.append(f"selectInput({_r(iid)}, {_r(column['label'] + ' — ' + row['label'])}, choices = {_named_values(options)})")
                pairs.append(f"{_r(str(column['value']) + '.' + str(row['value']))} = input${iid}")
        ui = "tagList(" + ", ".join(controls) + ")"
        value = "reactive(list(" + ", ".join(pairs) + "))"
    elif qtype == "pick_group_rank":
        controls, pairs = [], []
        for item in options:
            base = f"{qid}_{_safe_id(str(item['value']))}"
            controls.extend([
                f"selectInput({_r(base + '_group')}, {_r(item['label'] + ' — group')}, choices = {_named_values(groups)})",
                f"numericInput({_r(base + '_rank')}, {_r(item['label'] + ' — rank')}, value = 1, min = 1)",
            ])
            pairs.append(f"{_r(str(item['value']))} = reactiveValuesToList(input)[c({_r(base + '_group')}, {_r(base + '_rank')})]")
        ui = "tagList(" + ", ".join(controls) + ")"
        value = "reactive(list(" + ", ".join(pairs) + "))"
    elif qtype == "drill_down":
        ui = f"selectInput({_r(qid)}, NULL, choices = {_named_values(options)})"
        value = f"reactive(input${qid})"
    elif qtype == "timing":
        ui = "tags$span('Timing is recorded by the generated server binding.')"
        value = "local({ started <- Sys.time(); reactive({ invalidateLater(1000); as.numeric(difftime(Sys.time(), started, units = 'secs')) }) })"
    else:  # custom: portable fallback based on its confirmed options
        ui = f"selectInput({_r(qid)}, NULL, choices = {_named_values(options)})" if options else f"textInput({_r(qid)}, NULL)"
        value = f"reactive(input${qid})"

    label = question.get("label") or question["id"]
    return (
        f"  output${output_id} <- renderUI({{ {ui} }})\n"
        f"  {value_id} <- {value}\n"
        "  sd_question_custom(\n"
        f"    id = {_r(question['id'])},\n"
        f"    label = {_r(label)},\n"
        f"    output = uiOutput({_r(output_id)}),\n"
        f"    value = {value_id}\n"
        "  )"
    )


def generate(study_dir, parsed, config):
    study_dir = Path(study_dir)
    output = study_dir / "export/surveydown"
    output.mkdir(parents=True, exist_ok=True)
    source = _rewrite_nav_extensions(_force_preview_mode((study_dir / "survey.qmd").read_text()))
    custom_questions = []
    for page in parsed.get("pages", []):
        for question in page.get("questions", []):
            if question.get("type") in CUSTOM_TYPES:
                custom_questions.append(question)
                source = _replace_question_block(source, question)
            elif question.get("type") == "numeric":
                source = _remove_scalar_arguments(source, question["id"], ("min", "max", "step"))
            elif question.get("type") in ("matrix", "matrix_multiple"):
                source = _remove_scalar_arguments(source, question["id"], ("mobile_columns",))
    (output / "survey.qmd").write_text(source)
    for name in ("consent.md", "consent(kor).md"):
        if (study_dir / name).is_file():
            shutil.copyfile(study_dir / name, output / name)
    for directory in ("images", "assets", "design"):
        source_directory = study_dir / directory
        if source_directory.is_dir():
            shutil.copytree(source_directory, output / directory, dirs_exist_ok=True)

    bindings = "\n".join(filter(None, [_workflow_bindings(config), *(_output_binding(question) for question in custom_questions)]))
    (output / "app.R").write_text(APP_HEADER.format(version=config.get("greedyq_version", config.get("spec_version", "0.2")), bindings=bindings))

    features = [
        {"id": "qmd_pages_and_native_questions", "classification": "directly_portable", "note": "Native surveydown question and page syntax is preserved."},
        {"id": "safe_preview_mode", "classification": "directly_portable", "note": "The generated native project starts in Surveydown preview mode; switch to database mode only after review."},
    ]
    if custom_questions:
        features.append({
            "id": "greedyq_custom_controls", "classification": "generated_custom",
            "questions": [q["id"] for q in custom_questions],
            "note": "greedyQ-only controls were translated to sd_question_custom() plus generated Shiny bindings. Review their behavior before fielding.",
        })
    if config.get("logic"):
        features.append({"id": "declarative_logic", "classification": "generated_unverified", "note": "Display, skip, and stop rules were translated to native Surveydown helpers and require behavioral review."})
    if config.get("randomization"):
        features.append({"id": "random_assignment", "classification": "generated_unverified", "note": "Assignment was translated to a stored native random draw; fixed-block balance and greedyQ persistence equivalence are not claimed."})
    if config.get("consent"):
        features.append({"id": "consent_ledger", "classification": "greedyq_only", "note": "Displayed consent is preserved; the event ledger is not."})
    bounded_numeric = [q["id"] for page in parsed.get("pages", []) for q in page.get("questions", []) if q.get("type") == "numeric" and (q.get("min") is not None or q.get("max") is not None or q.get("step") is not None)]
    if bounded_numeric:
        features.append({"id": "numeric_input_bounds", "classification": "generated_unverified", "questions": bounded_numeric, "note": "Native Surveydown 1.3.0 does not accept greedyQ numeric min/max/step widget arguments; equivalent stop rules must be reviewed."})
    extended_nav = [page["id"] for page in parsed.get("pages", []) if any(key in page.get("nav", {}) for key in ("previous_mode", "next_mode", "next_delay_seconds"))]
    if extended_nav:
        features.append({"id": "extended_navigation", "classification": "generated_unverified", "pages": extended_nav, "note": "Hidden navigation is translated; disabled-button and timed-delay states have no native Surveydown 1.3.0 equivalent and require review."})
    if any(q.get("orientation") == "vertical" for page in parsed.get("pages", []) for q in page.get("questions", [])):
        features.append({"id": "vertical_slider", "classification": "generated_unverified", "note": "Review the exported slider presentation before fielding."})
    mismatch_classes = {"generated_custom", "generated_unverified", "greedyq_only", "unsupported"}
    mismatches = [item["note"] for item in features if item["classification"] in mismatch_classes]
    classes = ("directly_portable", "generated_custom", "generated_unverified", "greedyq_only", "unsupported")
    counts = {key: sum(item["classification"] == key for item in features) for key in classes}
    report = {
        "report_version": "0.2", "generator_status": "generated_unverified",
        "study_id": config.get("study", {}).get("id"), "spec_version": config.get("spec_version"),
        "summary": counts, "features": features, "material_mismatches": mismatches,
        "equivalence_claimed": not mismatches,
    }
    (output / "compatibility-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return output, report
