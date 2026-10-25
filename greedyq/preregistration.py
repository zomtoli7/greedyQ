"""Generate deterministic preregistration drafts without external submission."""

import hashlib
import json
from pathlib import Path
from .osf_fields import FIELDS, SOURCE, CHECKED


def _hash(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(study_dir, config):
    study_dir = Path(study_dir); output = study_dir / "preregistration"; output.mkdir(exist_ok=True)
    previous=output/'preregistration.json'
    if previous.exists() and json.loads(previous.read_text()).get('researcher_approved'):
        raise ValueError('Retain the approved draft and choose a new draft version before regenerating.')
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
    json_path = output / "preregistration.json"
    # Only explicit per-field prose is promoted to the human-readable draft.
    # Existing structured decisions remain in JSON; never guess their mapping.
    fields = prereg.get("fields", {})
    if not isinstance(fields, dict) or any(k not in {f[0] for f in FIELDS} for k in fields):
        raise ValueError("Use documented OSF field identifiers in preregistration.fields.")
    if any(not isinstance(v, str) for v in fields.values()):
        raise ValueError("Preregistration field drafts must be plain text.")
    fields = {"title": data["title"] or "", **fields}
    missing = [key for key, _, _ in FIELDS if not fields.get(key, "").strip()]
    data.update({"delivery": "draft_files_only", "template_source": SOURCE,
                 "template_checked": CHECKED, "fields": fields, "incomplete_fields": missing})
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    md_path = output / ("osf-preregistration.md" if data["adapter"] == "osf_preregistration" else "preregistration.md")
    kor_path = md_path.with_name(md_path.stem + "(kor).md")
    for korean, path, counterpart in ((False, md_path, kor_path), (True, kor_path, md_path)):
        md = "# " + ("사전등록 초안" if korean else "Preregistration draft") + "\n\n"
        md += f"[{('English' if korean else '한국어')}](./{counterpart.name})\n\n"
        md += ("검토용 초안 — 등록·승인되지 않았습니다. OSF 로그인이나 제출은 수행하지 않습니다.\n\n" if korean else "DRAFT — NOT REGISTERED OR APPROVED. No OSF login or submission is performed.\n\n")
        md += f"[OSF template]({SOURCE}) · {CHECKED}\n\n"
        if korean:
            md += "확정 답변은 입력한 원문을 그대로 보존합니다. 번역이 필요하면 연구자의 검토를 받으세요.\n\n"
        else:
            md += "Confirmed answers are preserved in their supplied language. Researcher review is required for translations.\n\n"
        for key, en, ko in FIELDS:
            md += f"## {ko if korean else en} ({key})\n\n"
            md += fields.get(key, "").strip() or ("확인 필요 — 연구자가 답변하거나 해당 없음을 확인해야 합니다." if korean else "TO CONFIRM — provide an answer or explicitly confirm not applicable.")
            md += "\n\n"
        path.write_text(md)
    covered = [name for name in ("survey.qmd", "greedyq.yml", "consent.md") if (study_dir / name).is_file()]
    manifest = {"schema_version": "0.2", "status": "draft_unapproved", "artifacts": [{"path": name, "sha256": _hash(study_dir / name)} for name in covered] + [{"path": str(p.relative_to(study_dir)), "sha256": _hash(p)} for p in (json_path, md_path, kor_path)]}
    manifest_path = output / "artifact-manifest.json"; manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return {"json": json_path, "markdown": md_path, "korean": kor_path, "manifest": manifest_path, "ready_for_submission": False}
