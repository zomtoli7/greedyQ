"""Create a draft study without inventing questionnaire or approval decisions."""
import hashlib
import json
import re
from pathlib import Path

from tools.resolve_guide import resolve
from .build import build

ROOT=Path(__file__).resolve().parents[1]


def initialize(destination, study_id, profile, modules=(), title='Untitled research draft', organization='Research team', language='en'):
    if not re.fullmatch(r'[a-z][a-z0-9_]{1,63}',study_id):raise ValueError('Choose a study ID with lowercase letters, digits and underscores.')
    if language not in ('en','ko','zh-CN','zh-TW'):raise ValueError('Choose en, ko, zh-CN or zh-TW.')
    lock=resolve(profile,list(modules))
    root=Path(destination).resolve()
    if root.exists():raise FileExistsError('Choose a new folder; existing study files are never overwritten by init.')
    root.mkdir(parents=True);state=root/'.greedyq';state.mkdir()
    release=lock['greedyq_release'];version='draft-1'
    labels={'en':('Welcome','Thank you','Draft preview only. Participant information and questions are not finalized.'),'ko':('설문에 오신 것을 환영합니다','감사합니다','검토용 초안입니다. 참여 안내와 문항은 아직 확정되지 않았습니다.'),'zh-CN':('欢迎参加问卷','谢谢','仅供草稿预览。参与说明和题目尚未确定。'),'zh-TW':('歡迎參加問卷','謝謝','僅供草稿預覽。參與說明和題目尚未確定。')}[language]
    q=lambda value:json.dumps(value,ensure_ascii=False)
    (root/'survey.qmd').write_text(f'''---
title: {q(title)}
greedyq:
  spec_version: "0.2"
  version: {q(release)}
  organization: {q(organization)}
  language: {language}
survey-settings:
  start-page: welcome
---

--- welcome

# {labels[0]}

{labels[2]}

--- complete

# {labels[1]}
''')
    (root/'greedyq.yml').write_text(f'''spec_version: "0.2"
study:
  id: {study_id}
  title: {q(title)}
  version: {version}
  status: draft
respondents:
  source: direct_link
  mode: test
outcomes:
  complete:
    page: complete
    lifecycle_state: completed
''')
    (root/'study-plan.md').write_text('# Study draft\n\n[한국어](./study-plan(kor).md)\n\nThe opening and ending pages are ready for review. The questionnaire, participant information, recruitment and data-handling decisions remain unresolved. Tell your AI the first question, or explicitly ask it to prepare a draft. This is a local preview, not an approved live study.\n')
    (root/'study-plan(kor).md').write_text('# 연구 초안\n\n[English](./study-plan.md)\n\n시작·종료 페이지만 검토할 수 있습니다. 문항·참여 안내·모집·데이터 처리 결정은 미정입니다. AI에게 첫 문항을 알려주거나 명시적으로 초안을 요청하세요. 승인된 실제 연구가 아니라 로컬 미리보기입니다.\n')
    consent='consent' in lock['modules']
    if consent:
        (root/'consent.md').write_text('# Participant information draft\n\n[한국어](./consent(kor).md)\n\nUNRESOLVED: The researcher must confirm purpose, tasks, duration, risks, data handling, withdrawal and contacts before this notice is written and approved. Do not use this placeholder for recruitment.\n')
        (root/'consent(kor).md').write_text('# 참여 안내 초안\n\n[English](./consent.md)\n\n미정: 연구자가 목적·과제·시간·위험·데이터 처리·철회·연락처를 확정한 뒤 안내문을 작성하고 승인해야 합니다. 이 임시 문구로 모집하지 마세요.\n')
    def write(path,data):(root/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    write('.greedyq/guide-lock.json',lock)
    write('greedyq.study.json',{'schema_version':'0.2','study_id':study_id,'study_version':version,'object':lock['object'],'profile':profile,'modules':lock['modules'],'origin':{'mode':'new'},'language':language,'entry_points':{'survey':'survey.qmd','config':'greedyq.yml','preview':'preview.html','study_plan':'study-plan.md','consent':'consent.md' if consent else None,'guide_lock':'.greedyq/guide-lock.json'}})
    base={'schema_version':'0.2','study_id':study_id}
    write('.greedyq/decision-log.json',{**base,'append_only':True,'decisions':[]})
    pending={'decision_id':'open_research_design','topic':'Study decisions','question':'What questions, participant information and data-handling choices do you approve?','blocking_scopes':['deployment','fielding'],'status':'open'}
    write('.greedyq/unresolved-decisions.json',{**base,'items':[pending]})
    write('.greedyq/study-state.json',{**base,'study_version':version,'guide_version':release,'spec_version':'0.2','mode':'agent','phase':'questionnaire','status':'in_progress','checkpoint':'none','gates':{gate:{'status':'pending'} for gate in ('design','instrument','analysis','preregistration','deployment','fielding')},'confirmed_decision_ids':[],'unresolved_decision_ids':['open_research_design'],'assumptions':[],'artifact_paths':['survey.qmd','greedyq.yml','study-plan.md'],'next_question':'What is your first question?'} )
    write('.greedyq/validation-report.json',{**base,'study_version':version,'overall_status':'incomplete','checks':[],'manual_gates':[]})
    sources=['survey.qmd','greedyq.yml','study-plan.md','study-plan(kor).md']+(['consent.md','consent(kor).md'] if consent else [])
    write('.greedyq/generation-manifest.json',{**base,'study_version':version,'guide_version':release,'spec_version':'0.2','artifacts':[{'path':name,'kind':'source','sha256':hashlib.sha256((root/name).read_bytes()).hexdigest(),'status':'generated','based_on_decision_ids':[]} for name in sources],'external_operations':[]})
    report,model=build(root)
    if report['status']!='passed':raise ValueError(report['summary'])
    return root
