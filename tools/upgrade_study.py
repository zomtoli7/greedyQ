#!/usr/bin/env python3
"""Upgrade a draft into a new folder; never alter its original or deploy it."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from greedyq.build import load_study, build
from greedyq.exporter import generate as export_survey
from greedyq.preregistration import generate as draft
from tools.resolve_guide import resolve


def upgrade(source, destination, profile=None, modules=None):
    source=Path(source).resolve(); destination=Path(destination).resolve()
    if destination.exists() or source==destination or source in destination.parents:
        raise ValueError('Choose a new destination outside the original study folder.')
    _,parsed,config=load_study(source)
    if config.get('respondents',{}).get('mode')=='production':
        raise ValueError('Live studies require a separately reviewed migration; this command upgrades drafts only.')
    if any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Resolve symbolic links explicitly before upgrading.')
    lock_path=source/'.greedyq/guide-lock.json'
    prior=json.loads(lock_path.read_text()) if lock_path.exists() else {}
    profile=profile or prior.get('profile')
    if not profile: raise ValueError('Choose the study profile explicitly; it will not be inferred.')
    lock=resolve(profile,modules if modules is not None else prior.get('modules',[]))
    release=re.search(r'^- \*\*Current release:\*\* `([^`]+)`',(ROOT/'README.md').read_text(),re.M).group(1)
    text=(source/'survey.qmd').read_text()
    front_end=text.find('\n---',4)
    header=text[:front_end]
    old=parsed['front_matter'].get('greedyq',{}).get('version')
    updated,count=re.subn(r'(?m)^(\s+version:\s*)["\']?'+re.escape(str(old))+r'["\']?\s*$',lambda m:m.group(1)+json.dumps(release),header)
    if count!=1: raise ValueError('Cannot safely locate the unique greedyq.version field.')
    excluded=[]
    def ignore(folder,names):
        blocked=[n for n in names if n in ('.git','.vercel','node_modules','__pycache__') or n.startswith('.env') or n.endswith(('.sqlite3','.sqlite3-wal','.sqlite3-shm','.db','.zip'))]
        excluded.extend(str((Path(folder)/n).relative_to(source)) for n in blocked)
        return blocked
    shutil.copytree(source,destination,ignore=ignore)
    internal=destination/'.greedyq'; internal.mkdir(exist_ok=True)
    report={'status':'building','original_unchanged':True,'from_release':old,'to_release':release,'excluded':excluded,'external_changes':False,'review_required':True}
    report_path=internal/'upgrade-report.json'
    try:
        (destination/'survey.qmd').write_text(updated+text[front_end:])
        history=Path(tempfile.mkdtemp(prefix='before-upgrade-',dir=internal))
        for path in list(internal.glob('*.json')):
            shutil.move(str(path),str(history/path.name))
        (internal/'guide-lock.json').write_text(json.dumps(lock,indent=2)+'\n')
        validation,model=build(destination)
        if validation['status']!='passed': raise ValueError('Updated study needs source changes: '+validation['summary'])
        _,newparsed,newconfig=load_study(destination)
        export_survey(destination,newparsed,newconfig)
        if newconfig.get('preregistration'): draft(destination,newconfig)
        report.update(status='preview_ready_review_required',source_sha256=hashlib.sha256((source/'survey.qmd').read_bytes()).hexdigest(),runtime_sha256=hashlib.sha256((destination/'greedyq-core.js').read_bytes()).hexdigest())
    except Exception as error:
        report.update(status='failed_do_not_deploy',error=str(error));raise
    finally:
        report_path.write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('destination');parser.add_argument('--profile');parser.add_argument('--module',action='append')
    args=parser.parse_args()
    print(json.dumps(upgrade(args.source,args.destination,args.profile,args.module),indent=2))
