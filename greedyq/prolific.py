"""Pure validation and normalization for Prolific-compatible launch parameters."""

from urllib.parse import parse_qs, urlencode, urlparse
import re

REQUIRED = ("PROLIFIC_PID", "STUDY_ID", "SESSION_ID")


def parse_launch(url_or_query, mode="test", expected_study_id=None):
    parsed = urlparse(url_or_query)
    query = parsed.query if parsed.query else url_or_query.lstrip("?")
    parameters = parse_qs(query, keep_blank_values=True)
    values = {key: items[0] for key, items in parameters.items()}
    issues = []
    for key in REQUIRED:
        value = values.get(key, "")
        if not value: issues.append({"code": "GQ020", "message": "%s is required for a Prolific launch." % key})
        elif len(value) > 200: issues.append({"code": "GQ020", "message": "%s is too long." % key})
        elif not re.fullmatch(r'[A-Za-z0-9_-]+',value): issues.append({'code':'GQ020','message':'%s contains invalid characters.'%key})
        elif mode=='production' and not re.fullmatch(r'[a-fA-F0-9]{24}',value): issues.append({'code':'GQ020','message':'%s must be a 24-character Prolific ID in production.'%key})
        if len(parameters.get(key,[]))>1:issues.append({'code':'GQ020','message':'%s must occur exactly once.'%key})
    if expected_study_id and values.get('STUDY_ID')!=expected_study_id:issues.append({'code':'GQ020','message':'The Prolific study ID does not match this survey.'})
    if 'prolific_token' in parameters:issues.append({'code':'GQ020','message':'Signed Prolific launches require server-side verification, which is not enabled.'})
    if 'gq_preview' in parameters and (mode!='test' or len(parameters['gq_preview'])!=1 or not re.fullmatch(r'[a-f0-9]{64}',values.get('gq_preview',''))):
        issues.append({'code':'GQ020','message':'A repeat preview requires one valid test-only grant.'})
    if mode not in ("test", "production"):
        issues.append({"code": "GQ020", "message": "Respondent mode must be test or production."})
    return {"status": "passed" if not issues else "failed", "mode": mode, "identifiers": {key: values.get(key) for key in REQUIRED}, "issues": issues}


def resolve_launch(url_or_query, mode="test", expected_study_id=None):
    """Allow a parameter-free direct launch only in test mode."""
    parsed = parse_launch(url_or_query, mode, expected_study_id)
    if parsed["status"] == "passed": return {**parsed, "source": "prolific"}
    query = urlparse(url_or_query).query or url_or_query.lstrip('?')
    if mode == "test" and not any(key in parse_qs(query,keep_blank_values=True) for key in (*REQUIRED,'prolific_token','gq_preview')):
        return {"status": "passed", "mode": mode, "source": "direct_test", "identifiers": None, "issues": []}
    return {**parsed, "source": "invalid"}


def completion_url(base_url, completion_code):
    if not base_url.startswith("https://"):
        raise ValueError("Prolific completion URLs must use HTTPS.")
    if not completion_code or len(completion_code) > 100:
        raise ValueError("A valid Prolific completion code is required.")
    separator = "&" if "?" in base_url else "?"
    return base_url + separator + urlencode({"cc": completion_code})


def integration_plan(config):
    """Reviewed standard URL integration; no API credential or recruitment side effect."""
    respondents=config.get('respondents',{})
    if respondents.get('source')!='prolific':return None
    mode=respondents.get('mode','test');settings=respondents.get('prolific',{})
    if not isinstance(settings,dict):raise ValueError('respondents.prolific must be an object.')
    if any(k not in ('study_id','completion_paths_reviewed','screening_mode') for k in settings):raise ValueError('Unsupported Prolific setting; use the standard URL integration.')
    study_id=settings.get('study_id')
    if study_id is not None and not re.fullmatch(r'[a-fA-F0-9]{24}',str(study_id)):raise ValueError('Set respondents.prolific.study_id to the 24-character Prolific study ID.')
    if mode=='production' and not study_id:raise ValueError('Set respondents.prolific.study_id before Prolific production collection.')
    if respondents.get('duplicate_policy','resume') not in ('resume','block'):raise ValueError('Prolific duplicate policy must be resume or block; repeated submissions are not enabled.')
    screening=settings.get('screening_mode','none')
    if screening not in ('none','prescreener_validation','custom'):raise ValueError('Choose none, prescreener_validation or custom for Prolific screening_mode.')
    if type(settings.get('completion_paths_reviewed',False)) is not bool:raise ValueError('completion_paths_reviewed must record a boolean researcher review.')
    if mode=='production' and not settings.get('completion_paths_reviewed'):raise ValueError('Review Prolific completion paths before production collection.')
    paths={};codes=[]
    for key,outcome in config.get('outcomes',{}).items():
        url=outcome.get('redirect')
        if not url:
            if mode=='production':raise ValueError('Each Prolific outcome needs its own configured completion path: '+key)
            continue
        parts=urlparse(url);params=parse_qs(parts.query,keep_blank_values=True)
        if parts.scheme!='https' or parts.netloc not in ('app.prolific.com','app.prolific.co') or parts.path!='/submissions/complete' or parts.fragment or set(params)!={'cc'} or len(params['cc'])!=1:
            raise ValueError('Use the exact Prolific HTTPS completion URL with a single cc parameter: '+key)
        code=params['cc'][0]
        if not re.fullmatch(r'[A-Za-z0-9_-]{2,100}',code):raise ValueError('Invalid Prolific completion code: '+key)
        if mode=='production' and (not re.fullmatch(r'[A-Za-z0-9]{2,100}',code) or re.search(r'EXAMPLE|PLACEHOLDER|TEST',code,re.I)):
            raise ValueError('Replace fixture completion codes with codes from your Prolific study: '+key)
        if code in codes:raise ValueError('Use distinct Prolific codes for distinct outcomes.')
        codes.append(code);paths[key]={'page':outcome.get('page',key),'status':outcome.get('lifecycle_state',key),'url':url,'code':code}
    if mode=='production' and not any(p['status']=='completed' for p in paths.values()):raise ValueError('A Prolific completion path is required before production collection.')
    if mode=='production' and screening=='none' and any(p['status']=='screened_out' for p in paths.values()):raise ValueError('Review Prolific screening_mode before using a screen-out path.')
    return {'study_id':study_id,'identity_verification':'url_parameters_only','screening_mode':screening,'completion_paths_reviewed':settings.get('completion_paths_reviewed',False),'paths':paths}
