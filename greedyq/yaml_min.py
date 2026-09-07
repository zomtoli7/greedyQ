"""Small safe YAML subset used by greedyQ fixtures and generated studies.

This intentionally does not support tags, anchors, aliases, or executable values.
"""

import json
import re


class YamlError(ValueError):
    pass


def _commentless(line):
    quote = None
    for i, char in enumerate(line):
        if char in "\"'":
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        elif char == "#" and quote is None and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def _split_inline(value):
    parts, start, quote, depth = [], 0, None, 0
    for i, char in enumerate(value):
        if char in "\"'":
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        elif quote is None:
            if char in "[{": depth += 1
            elif char in "]}": depth -= 1
            elif char == "," and depth == 0:
                parts.append(value[start:i].strip()); start = i + 1
    parts.append(value[start:].strip())
    return [part for part in parts if part]


def scalar(value):
    value = value.strip()
    if not value:
        return None
    if value.startswith("[") and value.endswith("]"):
        return [scalar(part) for part in _split_inline(value[1:-1])]
    if value.startswith("{") and value.endswith("}"):
        result = {}
        for part in _split_inline(value[1:-1]):
            if ":" not in part: raise YamlError("Invalid inline object")
            key, item = part.split(":", 1)
            result[str(scalar(key))] = scalar(item)
        return result
    if value[:1] == value[-1:] and value[:1] in "\"'":
        if value[0] == '"':
            try: return json.loads(value)
            except json.JSONDecodeError as exc: raise YamlError(str(exc))
        return value[1:-1].replace("''", "'")
    low = value.lower()
    if low in ("true", "yes"): return True
    if low in ("false", "no"): return False
    if low in ("null", "~"): return None
    if re.fullmatch(r"-?\d+", value): return int(value)
    if re.fullmatch(r"-?(?:\d+\.\d*|\d*\.\d+)", value): return float(value)
    return value


def loads(text):
    rows = []
    for number, raw in enumerate(text.splitlines(), 1):
        clean = _commentless(raw).rstrip()
        if not clean.strip() or clean.lstrip().startswith("---"):
            continue
        indent = len(clean) - len(clean.lstrip(" "))
        if "\t" in raw[:indent]: raise YamlError("Tabs are not allowed on line %d" % number)
        rows.append((indent, clean.strip(), number))
    if not rows: return {}

    def block(index, indent):
        is_list = rows[index][1].startswith("- ") or rows[index][1] == "-"
        out = [] if is_list else {}
        while index < len(rows):
            level, content, number = rows[index]
            if level < indent: break
            if level > indent: raise YamlError("Unexpected indentation on line %d" % number)
            if is_list:
                if not content.startswith("-"): break
                item = content[1:].strip()
                if not item:
                    if index + 1 >= len(rows) or rows[index + 1][0] <= level:
                        out.append(None); index += 1; continue
                    value, index = block(index + 1, rows[index + 1][0]); out.append(value); continue
                if ":" in item and not item.startswith(("'", '"')):
                    key, value = item.split(":", 1)
                    obj = {key.strip(): scalar(value)}
                    index += 1
                    if index < len(rows) and rows[index][0] > level:
                        child_indent = rows[index][0]
                        while index < len(rows) and rows[index][0] == child_indent and not rows[index][1].startswith("-"):
                            child, index = block(index, child_indent)
                            if not isinstance(child, dict): raise YamlError("Expected object after list item")
                            obj.update(child)
                            if index >= len(rows) or rows[index][0] <= level: break
                    out.append(obj); continue
                out.append(scalar(item)); index += 1; continue
            if content.startswith("-"): break
            if ":" not in content: raise YamlError("Expected key: value on line %d" % number)
            key, value = content.split(":", 1); key = key.strip()
            if not key: raise YamlError("Missing key on line %d" % number)
            index += 1
            if value.strip(): out[key] = scalar(value); continue
            if index < len(rows) and rows[index][0] > level:
                out[key], index = block(index, rows[index][0])
            else: out[key] = {}
        return out, index

    result, end = block(0, rows[0][0])
    if end != len(rows): raise YamlError("Could not parse YAML near line %d" % rows[end][2])
    return result
