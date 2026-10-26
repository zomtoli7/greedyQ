"""CLI for greedyQ's dependency-light Python reference implementation."""

import argparse
import functools
import http.server
import json
import sys
import webbrowser
from pathlib import Path

from .build import build, load_study
from .validator import validate
from .deployment import preflight
from .exporter import generate as generate_export
from .preregistration import generate as generate_preregistration


def show_report(report, stage="preview"):
    errors=[item for item in report.get("issues",[]) if item.get("severity","error")!="warning"]
    warnings=[item for item in report.get("issues",[]) if item.get("severity")=="warning"]
    if report["status"] == "passed":
        print("Your survey passed validation." if stage=="preview" else "Local deployment package checks passed. This does not verify a live connection or approve collection.")
    else:
        print("Your survey needs %d change(s) before %s:" % (len(errors),stage))
    for issue in errors:
        print("- %s (%s)" % (issue["message"],str(issue.get("file","study folder"))))
    if warnings:
        print("Warnings (%d; review separately from blocking errors):" % len(warnings))
        for issue in warnings:print("- "+issue["message"])


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python3 -m greedyq", description="Validate and preview a greedyQ study without installing dependencies.")
    sub = parser.add_subparsers(dest="command", required=True)
    init=sub.add_parser("init");init.add_argument("study_dir");init.add_argument("--id",required=True);init.add_argument("--profile",required=True);init.add_argument("--module",action="append",default=[]);init.add_argument("--title",default="Untitled research draft");init.add_argument("--organization",default="Research team");init.add_argument("--language",default="en")
    for name in ('cbc-validate','cbc-build'):
        item=sub.add_parser(name,help='Check a CBC design or create an account-free browser preview')
        item.add_argument('study_dir');item.add_argument('--workbook')
        if name=='cbc-build':item.add_argument('--output')
    for name in ("validate", "build", "preregister", "export-surveydown", "preflight"):
        item = sub.add_parser(name); item.add_argument("study_dir", nargs="?", default=".")
        if name=="preflight":
            item.add_argument("--stage",choices=("package","deployment"),default="package");item.add_argument("--deployment-index")
    preview = sub.add_parser("preview"); preview.add_argument("study_dir", nargs="?", default="."); preview.add_argument("--port", type=int, default=4173); preview.add_argument("--no-open", action="store_true")
    run = sub.add_parser("run",help="Serve the canonical JavaScript respondent runtime locally"); run.add_argument("study_dir", nargs="?", default="."); run.add_argument("--port", type=int, default=4180); run.add_argument("--database"); run.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command in ('cbc-validate','cbc-build'):
            from .cbc import load_design,import_design,build_preview,inspect_design,MAX_FILE
            if args.command=='cbc-build':
                target,model=build_preview(args.study_dir,args.output,args.workbook)
                print('CBC design checked. Open %s in a browser. Preview only; live CBC collection is not enabled.' % target)
            else:
                if args.workbook:
                    source=Path(args.workbook)
                    if source.stat().st_size>MAX_FILE:raise ValueError('The workbook is too large.')
                    config=json.loads((Path(args.study_dir)/'study.design.json').read_text());model=import_design(config,workbook=source.read_bytes())
                else:model=load_design(args.study_dir)
                print(json.dumps({'status':'passed','design_sha256':model['design_sha256'],'blocks':len(model['blocks']),'tasks':sum(len(b['tasks']) for b in model['blocks']),'live_collection':False,'inspection':inspect_design(model)}))
            return 0
        if args.command == "init":
            from .scaffold import initialize
            root=initialize(args.study_dir,args.id,args.profile,args.module,args.title,args.organization,args.language)
            print("Draft created. Open %s and review the opening and ending pages. No questions or approvals were invented." % (root/"preview.html"));return 0
        if args.command == "validate":
            study, parsed, config = load_study(args.study_dir)
            report = validate(parsed, config, study / "survey.qmd", study / "greedyq.yml")
            show_report(report); return 0 if report["status"] == "passed" else 1
        if args.command == "preflight":
            report = preflight(args.study_dir,stage=args.stage,deployment_index=args.deployment_index); show_report(report,"deployment"); return 0 if report["status"] == "passed" else 1
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
        if args.command == "run" and args.database:
            raise ValueError("run now serves the canonical browser runtime. It uses local browser test storage; --database is not supported. Python Store/serve remain developer reference tools, not the participant UI.")
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(study))
        server = http.server.ThreadingHTTPServer(("localhost", args.port), handler)
        url = "http://localhost:%d/%s" % (args.port,"index.html" if args.command=="run" else "preview.html")
        print("Open %s" % url); print("Press Control-C to stop the preview server.")
        if not args.no_open: webbrowser.open(url)
        try: server.serve_forever()
        except KeyboardInterrupt: print("\nPreview server stopped.")
        finally: server.server_close()
    except (ValueError, OSError) as exc:
        print("Could not prepare the preview: %s" % exc, file=sys.stderr); return 1


if __name__ == "__main__":
    sys.exit(main())
