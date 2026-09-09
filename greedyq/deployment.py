"""Offline preflight for the static Vercel and Supabase handoff bundle."""

import json
import hashlib
import re
from pathlib import Path


REQUIRED_STATIC = ("index.html", "preview.html", "studio.html", "results.html", "api/results.js", "greedyq-core.js", "greedyq-runtime.css", "supabase-connection-test.html", "vercel.json", ".env.example")
REQUIRED_RPC = ("greedyq_create_session", "greedyq_resume_session", "greedyq_save_session", "greedyq_assign_condition", "greedyq_register_external", "greedyq_withdraw_session", "respondent_source")
REQUIRED_DATA_SAFETY = ("enable row level security", "research_data_deleted", "gq_answers", "gq_consent_events", "gq_lifecycle_events")


def preflight(study_dir):
    root = Path(study_dir); issues = []
    for name in REQUIRED_STATIC:
        if not (root / name).is_file(): issues.append({"code": "GQ030", "message": "Missing deployment file: %s" % name})
    try:
        vercel = json.loads((root / "vercel.json").read_text())
        if vercel.get("framework") not in (None, "static"): issues.append({"code": "GQ030", "message": "Vercel must serve the static bundle without a framework runtime."})
    except (OSError, ValueError): issues.append({"code": "GQ030", "message": "vercel.json is missing or invalid."})
    migrations = "\n".join(path.read_text() for path in sorted((root / "supabase/migrations").glob("*.sql"))) if (root / "supabase/migrations").is_dir() else ""
    migration_paths = sorted((root / "supabase/migrations").glob("[0-9][0-9][0-9]_*.sql"))
    numbers = [int(re.match(r"(\d{3})_", path.name).group(1)) for path in migration_paths]
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
    return {"status": "passed" if not issues else "failed", "issues": issues}
