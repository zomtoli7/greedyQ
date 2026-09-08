"""Build normalized artifacts and the fixed browser-native runtime bundle."""

import json
import re
from pathlib import Path

from .compiler import compile_preview
from .parser import parse_qmd
from .validator import validate
from .yaml_min import loads as load_yaml


ROOT = Path(__file__).resolve().parents[1]


def load_study(study_dir):
    study_dir = Path(study_dir).resolve()
    qmd = study_dir / "survey.qmd"
    settings = study_dir / "greedyq.yml"
    if not qmd.is_file(): raise FileNotFoundError("survey.qmd was not found in %s" % study_dir)
    if not settings.is_file(): raise FileNotFoundError("greedyq.yml was not found in %s" % study_dir)
    parsed = parse_qmd(qmd)
    config = load_yaml(settings.read_text())
    return study_dir, parsed, config


def build(study_dir, write=True):
    study_dir, parsed, config = load_study(study_dir)
    report = validate(parsed, config, "survey.qmd", "greedyq.yml")
    if report["status"] != "passed": return report, None
    model = compile_preview(parsed, config)
    if write:
        internal = study_dir / ".greedyq"; internal.mkdir(exist_ok=True)
        normalized = {"schema_version": "0.2", "source": "survey.qmd", "front_matter": parsed["front_matter"], "pages": [{k:v for k,v in p.items() if not k.startswith("_")} for p in parsed["pages"]]}
        (internal / "normalized-survey.json").write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n")
        (internal / "validation-report.runtime.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        (study_dir / "preview-model.json").write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n")
        payload = json.dumps(model, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        pattern = r'(<script id="greedyq-model" type="application/json">).*?(</script>)'
        browser = ROOT / "templates/browser"
        for source, destination in (("preview.html", "preview.html"), ("respondent.html", "index.html")):
            template = (browser / source).read_text()
            html, count = re.subn(pattern, lambda match: match.group(1) + payload + match.group(2), template, count=1, flags=re.S)
            if count != 1: raise RuntimeError("Browser template model marker is missing or duplicated in %s." % source)
            (study_dir / destination).write_text(html)
        (study_dir / "studio.html").write_bytes((browser / "studio.html").read_bytes())
        (study_dir / "greedyq-core.js").write_bytes((ROOT / "web/greedyq-core.js").read_bytes())
        (study_dir / "greedyq-runtime.css").write_bytes((ROOT / "web/greedyq-runtime.css").read_bytes())
        migrations = study_dir / "supabase/migrations"; migrations.mkdir(parents=True, exist_ok=True)
        (migrations / "002_browser_rpc.sql").write_bytes((ROOT / "templates/supabase/002_browser_rpc.sql").read_bytes())
    return report, model
