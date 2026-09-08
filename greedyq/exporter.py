"""Generate an independent native surveydown project and compatibility report."""

import json
import shutil
from pathlib import Path


APP_R = '''# Generated independently by greedyQ {version}.\n# Review and test this native surveydown export before use.\nlibrary(surveydown)\n\ndb <- sd_db_connect()\nui <- sd_ui()\nserver <- function(input, output, session) {{\n  sd_server(db = db)\n}}\nshiny::shinyApp(ui = ui, server = server)\n'''


def generate(study_dir, parsed, config):
    study_dir = Path(study_dir); output = study_dir / "export/surveydown"; output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(study_dir / "survey.qmd", output / "survey.qmd")
    for name in ("consent.md", "consent(kor).md"):
        if (study_dir / name).is_file(): shutil.copyfile(study_dir / name, output / name)
    (output / "app.R").write_text(APP_R.format(version=config.get("spec_version", "0.2")))
    features = [{"id": "qmd_pages_and_questions", "classification": "directly_portable", "note": "Supported question and page syntax is preserved."}]
    if config.get("logic"): features.append({"id": "declarative_logic", "classification": "generated", "note": "Review native reactive behavior before fielding."})
    if config.get("randomization"): features.append({"id": "random_assignment", "classification": "greedyq_only", "note": "The base app.R does not claim equivalent persisted assignment."})
    if config.get("consent"): features.append({"id": "consent_ledger", "classification": "greedyq_only", "note": "Displayed consent is preserved; the event ledger is not."})
    mismatches = [item["note"] for item in features if item["classification"] in ("greedyq_only", "unsupported")]
    counts = {key: sum(item["classification"] == key for item in features) for key in ("directly_portable", "generated", "greedyq_only", "unsupported")}
    report = {"report_version": "0.2", "generator_status": "generated_unverified", "study_id": config.get("study", {}).get("id"), "spec_version": config.get("spec_version"), "summary": counts, "features": features, "material_mismatches": mismatches, "equivalence_claimed": not mismatches}
    (output / "compatibility-report.json").write_text(json.dumps(report, indent=2) + "\n")
    return output, report
