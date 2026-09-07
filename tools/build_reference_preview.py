#!/usr/bin/env python3
"""Compatibility wrapper for the QMD-driven greedyQ preview builder."""

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from greedyq.build import build  # noqa: E402


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
    report, _ = build(study_dir)
    if report["status"] != "passed":
        for issue in report["issues"]:
            print("- " + issue["message"], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
