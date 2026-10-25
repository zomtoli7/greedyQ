"""Declarative HTTPS-only terminal redirects; no arbitrary URL expressions."""
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


def redirect_plan(outcome):
    if not outcome.get('redirect'): return None
    url = outcome['redirect']
    if not isinstance(url,str): raise ValueError('Redirect must be a fixed HTTPS URL.')
    parts=urlsplit(url)
    if parts.scheme!='https' or not parts.hostname or parts.username or parts.password or re.search(r'[\s\\<>]',url):
        raise ValueError('Redirect must be a fixed HTTPS URL without credentials.')
    params=outcome.get('redirect_params',{})
    if not isinstance(params,dict) or any(not isinstance(v,str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,63}',str(k)) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,63}',v) for k,v in params.items()):
        raise ValueError('Redirect parameters must map approved output names to input URL parameter names.')
    if any(v=='gq_preview' or re.search(r'token|secret|password|key',v,re.I) for v in [*params,*params.values()]):
        raise ValueError('Do not forward credentials in redirect parameters.')
    if params and (parts.fragment or set(params).intersection(k for k,_ in parse_qsl(parts.query))):
        raise ValueError('Dynamic redirects must not have a fragment or duplicate fixed query keys.')
    delay=outcome.get('redirect_delay')
    if delay is not None and (type(delay) is not int or delay<0 or delay>3600): raise ValueError('Redirect delay must be an integer from 0 to 3600 seconds.')
    newtab=outcome.get('redirect_newtab',False)
    if type(newtab) is not bool: raise ValueError('redirect_newtab must be true or false.')
    if newtab and delay is not None: raise ValueError('New-tab redirects require a click, not an automatic timer.')
    return {'url':url,'params':params,'delay':delay,'newtab':newtab,'label':str(outcome.get('redirect_label','Continue to the next website'))}


def redirect_url(plan, query):
    parts=urlsplit(plan['url']); supplied=parse_qsl(query.lstrip('?'),keep_blank_values=True)
    result=dict(parse_qsl(parts.query,keep_blank_values=True))
    for output,source in plan['params'].items():
        values=[v for k,v in supplied if k==source]
        if len(values)!=1 or not values[0]: raise ValueError('Required return-link parameter is missing or repeated.')
        result[output]=values[0]
    return urlunsplit((parts.scheme,parts.netloc,parts.path,urlencode(result),parts.fragment))
