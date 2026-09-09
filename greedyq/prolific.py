"""Pure validation and normalization for Prolific-compatible launch parameters."""

from urllib.parse import parse_qs, urlencode, urlparse

REQUIRED = ("PROLIFIC_PID", "STUDY_ID", "SESSION_ID")


def synthetic_launch(session_id, study_id):
    """Return deterministic, visibly synthetic identifiers for test deployments."""
    clean_session = str(session_id).replace("-", "_")
    clean_study = "".join(char if char.isalnum() or char in "_-" else "_" for char in str(study_id))
    return {
        "PROLIFIC_PID": "GQ_TEST_%s" % clean_session,
        "STUDY_ID": "GQ_TEST_%s" % clean_study,
        "SESSION_ID": "GQ_TEST_%s" % clean_session,
    }


def parse_launch(url_or_query, mode="test"):
    parsed = urlparse(url_or_query)
    query = parsed.query if parsed.query else url_or_query.lstrip("?")
    values = {key: items[-1] for key, items in parse_qs(query, keep_blank_values=True).items()}
    issues = []
    for key in REQUIRED:
        value = values.get(key, "")
        if not value: issues.append({"code": "GQ020", "message": "%s is required for a Prolific launch." % key})
        elif len(value) > 200: issues.append({"code": "GQ020", "message": "%s is too long." % key})
    if mode not in ("test", "production"):
        issues.append({"code": "GQ020", "message": "Respondent mode must be test or production."})
    return {"status": "passed" if not issues else "failed", "mode": mode, "identifiers": {key: values.get(key) for key in REQUIRED}, "issues": issues}


def completion_url(base_url, completion_code):
    if not base_url.startswith("https://"):
        raise ValueError("Prolific completion URLs must use HTTPS.")
    if not completion_code or len(completion_code) > 100:
        raise ValueError("A valid Prolific completion code is required.")
    separator = "&" if "?" in base_url else "?"
    return base_url + separator + urlencode({"cc": completion_code})
