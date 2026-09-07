"""Parse the supported surveydown-style QMD subset into a normalized model."""

import re
from pathlib import Path

from .yaml_min import loads as load_yaml


PAGE_RE = re.compile(r"^---\s+([A-Za-z][A-Za-z0-9_-]*)\s*$", re.M)
FENCE_RE = re.compile(r"```\{r\}\s*\n(.*?)```", re.S)
CALL_RE = re.compile(r"\b(sd_question|sd_nav)\s*\(")


class ParseError(ValueError):
    def __init__(self, message, line=None):
        self.line = line
        super().__init__(("Line %d: " % line if line else "") + message)


def _split_top(text, separator=","):
    result, start, depth, quote, escape = [], 0, 0, None, False
    for i, char in enumerate(text):
        if quote:
            if escape: escape = False
            elif char == "\\" and quote == '"': escape = True
            elif char == quote: quote = None
        elif char in "\"'": quote = char
        elif char in "([{" : depth += 1
        elif char in ")]}" : depth -= 1
        elif char == separator and depth == 0:
            result.append(text[start:i].strip()); start = i + 1
    result.append(text[start:].strip())
    return [item for item in result if item]


def _unquote(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        body = text[1:-1]
        return bytes(body, "utf-8").decode("unicode_escape") if "\\" in body else body
    if text in ("TRUE", "True"): return True
    if text in ("FALSE", "False"): return False
    if text in ("NULL", "null"): return None
    if re.fullmatch(r"-?\d+", text): return int(text)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", text): return float(text)
    return text


def _vector(text, line):
    if not (text.startswith("c(") and text.endswith(")")):
        raise ParseError("Options and rows must use c(...).", line)
    values = []
    for item in _split_top(text[2:-1]):
        pieces = _split_equals(item)
        if pieces is None:
            value = _unquote(item); values.append({"label": str(value), "value": value})
        else:
            label, value = pieces
            option = {"label": str(_unquote(label)), "value": _unquote(value)}
            if re.fullmatch(r"[a-z][a-z0-9_]*", label) and value[:1] in "\"'" and " " in str(option["value"]):
                option["_looks_reversed"] = True
            values.append(option)
    return values


def _split_equals(text):
    depth, quote, escape = 0, None, False
    for i, char in enumerate(text):
        if quote:
            if escape: escape = False
            elif char == "\\" and quote == '"': escape = True
            elif char == quote: quote = None
        elif char in "\"'": quote = char
        elif char in "([{" : depth += 1
        elif char in ")]}" : depth -= 1
        elif char == "=" and depth == 0: return text[:i].strip(), text[i + 1:].strip()
    return None


def _call_args(body, line):
    found = CALL_RE.search(body)
    if not found: return None, {}
    name, start = found.group(1), found.end()
    depth, quote, escape, end = 1, None, False, None
    for i in range(start, len(body)):
        char = body[i]
        if quote:
            if escape: escape = False
            elif char == "\\" and quote == '"': escape = True
            elif char == quote: quote = None
        elif char in "\"'": quote = char
        elif char == "(": depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0: end = i; break
    if end is None: raise ParseError("The %s call is missing a closing parenthesis." % name, line)
    if body[end + 1:].strip(): raise ParseError("Only one supported call is allowed in each R block.", line)
    args = {}
    for item in _split_top(body[start:end]):
        pair = _split_equals(item)
        if pair is None: raise ParseError("Every %s argument must have a name." % name, line)
        key, raw = pair
        if key in args: raise ParseError("Argument '%s' appears more than once." % key, line)
        args[key] = _vector(raw, line) if key in ("option", "options", "row", "rows") else _unquote(raw)
    return name, args


def _plain_copy(section):
    text = FENCE_RE.sub("", section)
    heading = re.search(r"^#\s+(.+?)\s*$", text, re.M)
    title = heading.group(1).strip() if heading else None
    if heading: text = text[:heading.start()] + text[heading.end():]
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title, text


def parse_qmd(path):
    text = Path(path).read_text()
    if not text.startswith("---\n"): raise ParseError("The file must begin with YAML front matter.", 1)
    close = text.find("\n---", 4)
    if close < 0: raise ParseError("The YAML front matter is not closed.", 1)
    front = load_yaml(text[4:close])
    body = text[close + 4:].lstrip("\n")
    matches = list(PAGE_RE.finditer(body))
    if not matches: raise ParseError("No survey pages were found. Add a line such as '--- welcome'.")
    pages = []
    for index, match in enumerate(matches):
        page_id = match.group(1)
        section = body[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(body)]
        title, copy = _plain_copy(section)
        page = {"id": page_id, "title": title or page_id.replace("_", " ").title(), "body": copy, "questions": []}
        section_start = text[:close + 4].count("\n") + body[:match.end()].count("\n") + 1
        for fence in FENCE_RE.finditer(section):
            line = section_start + section[:fence.start()].count("\n") + 1
            name, args = _call_args(fence.group(1).strip(), line)
            if name == "sd_question":
                q = {"id": args.pop("id", None), "type": args.pop("type", None), "label": args.pop("label", None), "_line": line}
                if "option" in args: q["options"] = args.pop("option")
                if "options" in args: q["options"] = args.pop("options")
                if "row" in args: q["rows"] = args.pop("row")
                if "rows" in args: q["rows"] = args.pop("rows")
                if "label_select" in args: q["placeholder"] = args.pop("label_select")
                for key in ("placeholder", "min", "max"):
                    if key in args: q[key] = args.pop(key)
                if args: q["unsupported_arguments"] = sorted(args)
                page["questions"].append(q)
            elif name == "sd_nav":
                page["nav"] = args; page["_nav_line"] = line
            elif fence.group(1).strip():
                raise ParseError("This R block does not contain sd_question() or sd_nav().", line)
        pages.append(page)
    return {"front_matter": front, "pages": pages, "source": str(path)}
