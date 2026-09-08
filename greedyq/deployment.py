"""Offline preflight for the static Vercel and Supabase handoff bundle."""

import json
from pathlib import Path


REQUIRED_STATIC = ("index.html", "preview.html", "studio.html", "greedyq-core.js", "greedyq-runtime.css", "vercel.json", ".env.example")
REQUIRED_RPC = ("greedyq_resume_session", "greedyq_save_session", "greedyq_assign_condition", "greedyq_register_external", "greedyq_withdraw_session")


def preflight(study_dir):
    root = Path(study_dir); issues = []
    for name in REQUIRED_STATIC:
        if not (root / name).is_file(): issues.append({"code": "GQ030", "message": "Missing deployment file: %s" % name})
    try:
        vercel = json.loads((root / "vercel.json").read_text())
        if vercel.get("framework") not in (None, "static"): issues.append({"code": "GQ030", "message": "Vercel must serve the static bundle without a framework runtime."})
    except (OSError, ValueError): issues.append({"code": "GQ030", "message": "vercel.json is missing or invalid."})
    migrations = "\n".join(path.read_text() for path in sorted((root / "supabase/migrations").glob("*.sql"))) if (root / "supabase/migrations").is_dir() else ""
    for rpc in REQUIRED_RPC:
        if rpc not in migrations: issues.append({"code": "GQ031", "message": "Supabase migration does not define %s." % rpc})
    for path in root.glob("**/*"):
        if path.is_file() and path.stat().st_size < 2_000_000:
            text = path.read_text(errors="ignore")
            if "service_role" in text.lower() and path.suffix in (".html", ".js", ".json"): issues.append({"code": "GQ032", "message": "A browser artifact mentions a service-role credential: %s" % path.relative_to(root)})
    return {"status": "passed" if not issues else "failed", "issues": issues}
