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
  sd_server(db = db)
{bindings}
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
    return (
        "sd_question_custom(\n"
        f"  id = {_r(qid)},\n"
        f"  label = {_r(question.get('label') or qid)},\n"
        f"  output = {_r('gq_' + _safe_id(qid) + '_output')},\n"
        f"  value = {_r('gq_' + _safe_id(qid) + '_value')}\n"
        ")"
    )


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

    return (
        f"  output${output_id} <- renderUI({{ {ui} }})\n"
        f"  {value_id} <- {value}"
    )


def generate(study_dir, parsed, config):
    study_dir = Path(study_dir)
    output = study_dir / "export/surveydown"
    output.mkdir(parents=True, exist_ok=True)
    source = (study_dir / "survey.qmd").read_text()
    custom_questions = []
    for page in parsed.get("pages", []):
        for question in page.get("questions", []):
            if question.get("type") in CUSTOM_TYPES:
                custom_questions.append(question)
                source = _replace_question_block(source, question)
    (output / "survey.qmd").write_text(source)
    for name in ("consent.md", "consent(kor).md"):
        if (study_dir / name).is_file():
            shutil.copyfile(study_dir / name, output / name)
    for directory in ("images", "assets", "design"):
        source_directory = study_dir / directory
        if source_directory.is_dir():
            shutil.copytree(source_directory, output / directory, dirs_exist_ok=True)

    bindings = "\n".join(_output_binding(question) for question in custom_questions)
    (output / "app.R").write_text(APP_HEADER.format(version=config.get("greedyq_version", config.get("spec_version", "0.2")), bindings=bindings))

    features = [{"id": "qmd_pages_and_native_questions", "classification": "directly_portable", "note": "Native surveydown question and page syntax is preserved."}]
    if custom_questions:
        features.append({
            "id": "greedyq_custom_controls", "classification": "generated_custom",
            "questions": [q["id"] for q in custom_questions],
            "note": "greedyQ-only controls were translated to sd_question_custom() plus generated Shiny bindings. Review their behavior before fielding.",
        })
    if config.get("logic"):
        features.append({"id": "declarative_logic", "classification": "greedyq_only", "note": "Declarative greedyQ display and route logic is not yet translated to native Shiny behavior."})
    if config.get("randomization"):
        features.append({"id": "random_assignment", "classification": "greedyq_only", "note": "The base app.R does not claim equivalent persisted assignment."})
    if config.get("consent"):
        features.append({"id": "consent_ledger", "classification": "greedyq_only", "note": "Displayed consent is preserved; the event ledger is not."})
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
