"""Command-line interface for greedyQ's zero-install reference implementation."""

import argparse
import functools
import http.server
import json
import sys
import webbrowser
from pathlib import Path

from .build import build, load_study
from .validator import validate


def show_report(report):
    if report["status"] == "passed":
        print("Your survey passed validation.")
        return
    print("Your survey needs %d change(s) before preview:" % len(report["issues"]))
    for issue in report["issues"]:
        location = str(issue["file"]) + ((":" + str(issue["line"])) if issue.get("line") else "")
        print("- %s (%s)" % (issue["message"], location))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python3 -m greedyq", description="Validate and preview a greedyQ study without installing dependencies.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "build"):
        item = sub.add_parser(name); item.add_argument("study_dir", nargs="?", default=".")
    preview = sub.add_parser("preview"); preview.add_argument("study_dir", nargs="?", default="."); preview.add_argument("--port", type=int, default=4173); preview.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            study, parsed, config = load_study(args.study_dir)
            report = validate(parsed, config, study / "survey.qmd", study / "greedyq.yml")
            show_report(report); return 0 if report["status"] == "passed" else 1
        report, model = build(args.study_dir)
        show_report(report)
        if report["status"] != "passed": return 1
        study = Path(args.study_dir).resolve()
        print("Preview created: %s" % (study / "preview.html"))
        if args.command == "build": return 0
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(study))
        server = http.server.ThreadingHTTPServer(("localhost", args.port), handler)
        url = "http://localhost:%d/preview.html" % args.port
        print("Open %s" % url); print("Press Control-C to stop the preview server.")
        if not args.no_open: webbrowser.open(url)
        server.serve_forever()
    except (ValueError, OSError) as exc:
        print("Could not prepare the preview: %s" % exc, file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
