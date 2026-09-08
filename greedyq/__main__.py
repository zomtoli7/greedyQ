"""CLI for greedyQ's dependency-light Python reference implementation."""

import argparse
import functools
import http.server
import json
import sys
import webbrowser
from pathlib import Path

from .build import build, load_study
from .server import serve
from .runtime import Store
from .validator import validate
from .deployment import preflight
from .exporter import generate as generate_export
from .preregistration import generate as generate_preregistration


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
    for name in ("validate", "build", "preregister", "export-surveydown", "preflight"):
        item = sub.add_parser(name); item.add_argument("study_dir", nargs="?", default=".")
    preview = sub.add_parser("preview"); preview.add_argument("study_dir", nargs="?", default="."); preview.add_argument("--port", type=int, default=4173); preview.add_argument("--no-open", action="store_true")
    run = sub.add_parser("run"); run.add_argument("study_dir", nargs="?", default="."); run.add_argument("--port", type=int, default=4180); run.add_argument("--database"); run.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            study, parsed, config = load_study(args.study_dir)
            report = validate(parsed, config, study / "survey.qmd", study / "greedyq.yml")
            show_report(report); return 0 if report["status"] == "passed" else 1
        if args.command == "preflight":
            report = preflight(args.study_dir); show_report(report); return 0 if report["status"] == "passed" else 1
        if args.command in ("preregister", "export-surveydown"):
            study, parsed, config = load_study(args.study_dir)
            report = validate(parsed, config, study / "survey.qmd", study / "greedyq.yml")
            show_report(report)
            if report["status"] != "passed": return 1
            if args.command == "preregister":
                result = generate_preregistration(study, config); print("Preregistration draft created: %s" % result["markdown"])
            else:
                output, _ = generate_export(study, parsed, config); print("Native surveydown export created: %s" % output)
            return 0
        report, model = build(args.study_dir)
        show_report(report)
        if report["status"] != "passed": return 1
        study = Path(args.study_dir).resolve()
        print("Preview created: %s" % (study / "preview.html"))
        if args.command == "build": return 0
        if args.command == "run":
            _, _, config = load_study(study)
            database = Path(args.database).resolve() if args.database else study / ".greedyq/runtime.sqlite3"
            server = serve(model, config, Store(database), args.port)
            url = "http://localhost:%d/study" % args.port
            print("Respondent test server: %s" % url); print("Test data: %s" % database); print("Press Control-C to stop the server.")
            if not args.no_open: webbrowser.open(url)
            try: server.serve_forever()
            except KeyboardInterrupt: print("\nRespondent test server stopped.")
            finally: server.server_close()
            return 0
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(study))
        server = http.server.ThreadingHTTPServer(("localhost", args.port), handler)
        url = "http://localhost:%d/preview.html" % args.port
        print("Open %s" % url); print("Press Control-C to stop the preview server.")
        if not args.no_open: webbrowser.open(url)
        try: server.serve_forever()
        except KeyboardInterrupt: print("\nPreview server stopped.")
        finally: server.server_close()
    except (ValueError, OSError) as exc:
        print("Could not prepare the preview: %s" % exc, file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
