"""Offline preflight for the static Vercel and Supabase handoff bundle."""

import json
import hashlib
import re
from pathlib import Path


REQUIRED_STATIC = ("index.html", "preview.html", "studio.html", "results.html", "api/results.js", "greedyq-core.js", "greedyq-runtime.css", "supabase-connection-test.html", "vercel.json", ".env.example")
REQUIRED_RPC = ("greedyq_create_session", "greedyq_resume_session", "greedyq_save_session", "greedyq_assign_condition", "greedyq_register_external", "greedyq_withdraw_session", "respondent_source")
REQUIRED_DATA_SAFETY = ("enable row level security", "research_data_deleted", "gq_answers", "gq_consent_events", "gq_lifecycle_events")


def preflight(study_dir, stage="package", deployment_index=None):
    if stage not in ("package", "deployment"): raise ValueError("Unknown preflight stage.")
    root = Path(study_dir).resolve(); issues = []
    from .validator import validate_state_artifacts
    from .build import build
    issues.extend(validate_state_artifacts(root)["issues"])
    descriptor = None
    try:
        descriptor = json.loads((root / "greedyq.study.json").read_text())
        if not isinstance(descriptor, dict): raise ValueError("Expected a study object.")
        for key in ("study_id", "study_version", "profile", "entry_points"):
            if not descriptor.get(key): raise ValueError("Missing " + key)
        for key in ("survey", "config", "study_plan", "guide_lock"):
            relative = descriptor["entry_points"].get(key)
            target = (root / str(relative or "")).resolve()
            if not relative or not target.is_relative_to(root) or not target.is_file():
                raise ValueError("Missing or unsafe study entry: " + key)
        consent = descriptor["entry_points"].get("consent")
        if consent:
            target = (root / consent).resolve()
            if not target.is_relative_to(root) or not target.is_file(): raise ValueError("Missing consent document.")
        lock = json.loads((root / descriptor["entry_points"]["guide_lock"]).read_text())
        if lock.get("profile") != descriptor["profile"]: raise ValueError("Study profile and guide lock disagree.")
        for name in ("study-state.json", "decision-log.json", "unresolved-decisions.json", "generation-manifest.json", "validation-report.json"):
            record=json.loads((root/'.greedyq'/name).read_text())
            if record.get('study_id') != descriptor['study_id']: raise ValueError("Study identity disagrees in " + name)
            if record.get('study_version',descriptor['study_version']) != descriptor['study_version']:raise ValueError("Study version disagrees in " + name)
        state=json.loads((root/'.greedyq/study-state.json').read_text())
        if state.get('guide_version') != lock.get('greedyq_release'):raise ValueError("Study state and guide release disagree.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        issues.append({"code":"GQ012", "message":"Incomplete study package: " + str(error)})
    try:
        validation, model = build(root, write=False)
        issues.extend(validation["issues"])
        if model is not None:
            if descriptor and descriptor["study_id"] != model["study_id"]:
                issues.append({"code":"GQ012", "message":"Study identity and compiled survey disagree."})
            candidate=Path(deployment_index) if deployment_index else root/'index.html'
            candidate_html=candidate.read_text()
            deployment_match=re.search(r'<script[^>]+id="greedyq-deployment"[^>]*>(.*?)</script>',candidate_html,re.S)
            candidate_model=re.search(r'<script[^>]+id="greedyq-model"[^>]*>(.*?)</script>',candidate_html,re.S)
            if not candidate_model or json.loads(candidate_model.group(1)) != model:
                issues.append({"code":"GQ030", "message":"The deployment candidate does not contain the current validated survey model."})
            connection=json.loads(deployment_match.group(1)) if deployment_match else {}
            connected=connection.get('mode')=='supabase' and re.fullmatch(r'https://[a-z0-9-]+[.]supabase[.]co/?',connection.get('supabase_url','')) and bool(connection.get('supabase_anon_key'))
            if not connected:
                issues.append({"code":"GQ030", "severity":"error" if stage == "deployment" else "warning", "message":"This is a local preview. Answers are not sent to the researcher; configure and verify the live connection before deployment."})
        if stage == "deployment":
            state=json.loads((root/'.greedyq/study-state.json').read_text())
            pending=json.loads((root/'.greedyq/unresolved-decisions.json').read_text())
            for gate in ("instrument", "deployment"):
                if state.get("gates",{}).get(gate,{}).get("status") != "approved":
                    issues.append({"code":"GQ012", "message":"Researcher approval is pending: " + gate})
            if any(item.get("status")=="open" and "deployment" in item.get("blocking_scopes",[]) for item in pending.get("items",[])):
                issues.append({"code":"GQ012", "message":"Resolve the open deployment decisions before deployment."})
    except (OSError, ValueError, KeyError, TypeError) as error:
        issues.append({"code":"GQ012", "message":"The survey package could not be checked: " + str(error)})
    for name in REQUIRED_STATIC:
        if not (root / name).is_file(): issues.append({"code": "GQ030", "message": "Missing deployment file: %s" % name})
    try:
        vercel = json.loads((root / "vercel.json").read_text())
        if vercel.get("framework") not in (None, "static"): issues.append({"code": "GQ030", "message": "Vercel must serve the static bundle without a framework runtime."})
    except (OSError, ValueError): issues.append({"code": "GQ030", "message": "vercel.json is missing or invalid."})
    migrations = "\n".join(path.read_text() for path in sorted((root / "supabase/migrations").glob("*.sql"))) if (root / "supabase/migrations").is_dir() else ""
    migration_paths = sorted((root / "supabase/migrations").glob("[0-9][0-9][0-9]_*.sql"))
    numbers = [int(re.match(r"(\d{3})_", path.name).group(1)) for path in migration_paths]
    if [p.name for p in migration_paths] != ["001_initial.sql","002_browser_rpc.sql","003_results_dashboard.sql","004_randomization.sql","005_prolific.sql","006_withdrawal_preview.sql","007_answer_snapshot.sql","008_terminal_timestamp.sql"]:
        issues.append({"code":"GQ013","message":"The complete canonical migration set 001–008 is required."})
    if numbers != sorted(set(numbers)):
        issues.append({"code": "GQ013", "message": "Supabase migration numbers must be unique and ordered."})
    manifest_path = root / "supabase/migrations/manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
        recorded = {item["name"]: item["sha256"] for item in manifest.get("migrations", [])}
        for path in migration_paths:
            if recorded.get(path.name) != hashlib.sha256(path.read_bytes()).hexdigest():
                issues.append({"code": "GQ013", "message": "Supabase migration checksum does not match: %s" % path.name})
    except (OSError, ValueError, KeyError):
        issues.append({"code": "GQ013", "message": "Supabase migration manifest is missing or invalid."})
    for rpc in REQUIRED_RPC:
        if rpc not in migrations: issues.append({"code": "GQ013", "message": "Supabase migration does not define %s." % rpc})
    for token in REQUIRED_DATA_SAFETY:
        if token not in migrations.lower(): issues.append({"code": "GQ013", "message": "Supabase migrations are missing the required data-safety contract: %s." % token})
    for path in root.glob("**/*"):
        if path.is_file() and path.stat().st_size < 2_000_000:
            text = path.read_text(errors="ignore")
            if "service_role" in text.lower() and "api" not in path.relative_to(root).parts and path.suffix in (".html", ".js", ".json"): issues.append({"code": "GQ032", "message": "A browser artifact mentions a service-role credential: %s" % path.relative_to(root)})
    return {"status": "failed" if any(item.get("severity", "error") != "warning" for item in issues) else "passed", "issues": issues}
