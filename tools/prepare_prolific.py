#!/usr/bin/env python3
"""Prepare standard Prolific setup fields offline; never create or publish studies."""
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from greedyq.build import load_study
from greedyq.validator import validate
from greedyq.prolific import integration_plan

def prepare(study,survey_url):
    root,parsed,config=load_study(study)
    if validate(parsed,config)['status']!='passed':raise ValueError('Resolve survey validation issues first.')
    plan=integration_plan(config)
    if not plan:raise ValueError('Choose respondents.source: prolific first.')
    url=urlsplit(survey_url)
    if url.scheme!='https' or not url.netloc or url.username or url.password or url.query or url.fragment:raise ValueError('Use the deployed HTTPS survey URL without identifiers, query parameters or credentials.')
    return {'status':'draft_not_published','respondent_mode':config.get('respondents',{}).get('mode','test'),'base_survey_url':survey_url,'record_ids':'URL parameters','parameter_names':['PROLIFIC_PID','STUDY_ID','SESSION_ID'],
      'api_external_study_url':survey_url+'?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}',
      'prolific':plan,'not_performed':['Prolific account connection','study creation','payment','publication','recruitment','submission approval']}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('study');parser.add_argument('--url',required=True);parser.add_argument('--output',required=True);args=parser.parse_args()
    output=Path(args.output)
    if output.exists():raise SystemExit('Choose a new output path to preserve previous setup records.')
    output.write_text(json.dumps(prepare(args.study,args.url),ensure_ascii=False,indent=2)+'\n')
    print('Prolific setup fields prepared: '+str(output))
