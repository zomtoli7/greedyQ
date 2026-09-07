#!/usr/bin/env python3
"""Build the golden reference preview by injecting only its JSON model."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
template = (ROOT / "templates/preview/preview.html").read_text()
model_path = ROOT / "examples/complete-study/preview-model.json"
model = json.loads(model_path.read_text())
payload = json.dumps(model, ensure_ascii=False, separators=(",", ":"))
pattern = r'(<script id="greedyq-model" type="application/json">).*?(</script>)'
output, count = re.subn(pattern, lambda m: m.group(1) + payload + m.group(2), template, count=1, flags=re.S)
if count != 1:
    raise SystemExit("greedyq-model marker missing or duplicated")
(ROOT / "examples/complete-study/preview.html").write_text(output)
