#!/usr/bin/env python3
"""Build a golden reference preview by injecting only its JSON model."""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build(study_dir: Path) -> None:
    template = (ROOT / "templates/preview/preview.html").read_text()
    model = json.loads((study_dir / "preview-model.json").read_text())
    payload = json.dumps(model, ensure_ascii=False, separators=(",", ":"))
    pattern = r'(<script id="greedyq-model" type="application/json">).*?(</script>)'
    output, count = re.subn(pattern, lambda match: match.group(1) + payload + match.group(2), template, count=1, flags=re.S)
    if count != 1:
        raise SystemExit("greedyq-model marker missing or duplicated")
    (study_dir / "preview.html").write_text(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--study-dir",
        type=Path,
        default=ROOT / "examples" / "complete-study",
        help="Directory containing preview-model.json",
    )
    args = parser.parse_args()
    study_dir = args.study_dir if args.study_dir.is_absolute() else ROOT / args.study_dir
    build(study_dir)


if __name__ == "__main__":
    main()
