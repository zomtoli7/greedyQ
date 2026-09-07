#!/usr/bin/env python3
"""Build the deterministic greedyQ guide registry from component manifests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "registry" / "guide-index.source.json"
OUTPUT = ROOT / "registry" / "guide-index.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(SOURCE.read_text())
    components: dict[str, dict] = {}
    for manifest_path in source.pop("component_manifests"):
        absolute_manifest = ROOT / manifest_path
        manifest = json.loads(absolute_manifest.read_text())
        component_id = manifest["id"]
        if component_id in components:
            raise ValueError(f"duplicate component: {component_id}")
        files = []
        for relative in manifest["normative_files"]:
            absolute = ROOT / relative
            if not absolute.is_file():
                raise FileNotFoundError(relative)
            files.append({"path": relative, "sha256": digest(absolute)})
        components[component_id] = {
            key: manifest[key]
            for key in ("id", "kind", "version")
        }
        if "object_name" in manifest:
            components[component_id]["object_name"] = manifest["object_name"]
        components[component_id].update({
            "manifest": manifest_path,
            "manifest_sha256": digest(absolute_manifest),
            "dependencies": manifest["dependencies"],
            "conflicts": manifest["conflicts"],
            "files": files,
        })
    output = {**source, "components": dict(sorted(components.items()))}
    OUTPUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
