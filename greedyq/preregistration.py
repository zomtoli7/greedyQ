"""Generate deterministic preregistration drafts without external submission."""

import hashlib
import json
from pathlib import Path


def _hash(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(study_dir, config):
    study_dir = Path(study_dir); output = study_dir / "preregistration"; output.mkdir(exist_ok=True)
    prereg = config.get("preregistration", {})
    decisions = prereg.get("decisions", {})
    unresolved = prereg.get("unresolved_decisions", []) or []
    data = {
        "schema_version": "0.2", "adapter": prereg.get("adapter", "generic_markdown"),
        "status": "draft_unapproved", "study_id": config.get("study", {}).get("id"),
        "study_version": config.get("study", {}).get("version"), "title": config.get("study", {}).get("title"),
        "hypotheses": decisions.get("hypotheses", []), "design": decisions.get("design", {}),
        "sampling": decisions.get("sampling", {}), "exclusions": decisions.get("exclusions", {}),
        "analysis": decisions.get("analysis", {}), "registry": {"submitted": False, "verified": False, "registration_id": None, "url": None},
        "unresolved_decisions": unresolved, "researcher_approved": False, "fielding_allowed": False,
    }
    json_path = output / "preregistration.json"; json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    def section(name, value): return "## %s\n\n```json\n%s\n```\n" % (name, json.dumps(value, ensure_ascii=False, indent=2))
    md = "# %s\n\n**Status: DRAFT — NOT SUBMITTED OR APPROVED**\n\n" % (data["title"] or "Study preregistration")
    for name in ("hypotheses", "design", "sampling", "exclusions", "analysis", "unresolved_decisions"):
        md += section(name.replace("_", " ").title(), data[name]) + "\n"
    md_path = output / ("osf-preregistration.md" if data["adapter"] == "osf_preregistration" else "preregistration.md"); md_path.write_text(md)
    covered = [name for name in ("survey.qmd", "greedyq.yml", "consent.md") if (study_dir / name).is_file()]
    manifest = {"schema_version": "0.2", "status": "draft_unapproved", "artifacts": [{"path": name, "sha256": _hash(study_dir / name)} for name in covered] + [{"path": str(json_path.relative_to(study_dir)), "sha256": _hash(json_path)}, {"path": str(md_path.relative_to(study_dir)), "sha256": _hash(md_path)}]}
    manifest_path = output / "artifact-manifest.json"; manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return {"json": json_path, "markdown": md_path, "manifest": manifest_path, "ready_for_submission": not unresolved}
