#!/usr/bin/env python3
"""Synchronize the literal canonical bundle embedded in both full AI guides."""

from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- GREEDYQ_BUNDLE_START -->"
END = "<!-- GREEDYQ_BUNDLE_END -->"
FILES = (
    ("docs/preview-ui-spec.md", "markdown", False),
    ("templates/preview/preview.html", "html", True),
    ("examples/complete-study/supabase/migrations/001_initial.sql", "sql", False),
    ("examples/complete-study/vercel.json", "json", False),
    ("schemas/ai/study-state.schema.json", "json", False),
    ("schemas/ai/decision-log.schema.json", "json", False),
    ("schemas/ai/unresolved-decisions.schema.json", "json", False),
    ("schemas/ai/generation-manifest.schema.json", "json", False),
    ("schemas/preview-model.schema.json", "json", False),
)


def make_bundle() -> str:
    parts = [START, "", "### Canonical file manifest", ""]
    parts += [
        "| FILE | SHA-256 | Study data may be replaced |",
        "| --- | --- | --- |",
    ]
    records = []
    for relative, language, replaceable in FILES:
        data = (ROOT / relative).read_bytes()
        digest = sha256(data).hexdigest()
        records.append((relative, language, data.decode("utf-8"), digest))
        flag = "yes" if replaceable else "no"
        parts.append(f"| `{relative}` | `{digest}` | `{flag}` |")
    for relative, language, source, digest in records:
        parts += [
            "",
            f"### FILE: `{relative}`",
            "",
            f"SHA-256: `{digest}`",
            "",
            f"```{language}",
            source.rstrip("\n"),
            "```",
        ]
    return "\n".join(parts + ["", END])


def update(path: Path, embedded: str) -> None:
    text = path.read_text(encoding="utf-8")
    before, found, remainder = text.partition(START)
    if not found or END not in remainder:
        raise SystemExit(f"bundle markers missing in {path}")
    _, _, after = remainder.partition(END)
    path.write_text(before + embedded + after, encoding="utf-8")


bundle = make_bundle()
for guide in ("guides/greedyq-guide.md", "guides/greedyq-guide(kor).md"):
    update(ROOT / guide, bundle)
