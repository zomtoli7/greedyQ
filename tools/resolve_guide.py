#!/usr/bin/env python3
"""Resolve and verify one greedyQ profile plus capability modules."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "guide-index.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(profile: str, requested_modules: list[str]) -> dict:
    registry = json.loads(REGISTRY_PATH.read_text())
    components = registry["components"]
    if profile not in components or components[profile]["kind"] != "profile":
        raise ValueError(f"unknown profile: {profile}")
    for module in requested_modules:
        if module not in components or components[module]["kind"] != "module":
            raise ValueError(f"unknown module: {module}")

    resolved: list[str] = []
    active: set[str] = set()

    def add(component_id: str) -> None:
        if component_id in active:
            raise ValueError(f"dependency cycle at {component_id}")
        if component_id in resolved:
            return
        if component_id not in components:
            raise ValueError(f"missing dependency: {component_id}")
        active.add(component_id)
        for dependency in components[component_id]["dependencies"]:
            add(dependency)
        active.remove(component_id)
        resolved.append(component_id)

    add(profile)
    for module in sorted(set(requested_modules)):
        add(module)

    resolved_set = set(resolved)
    for component_id in resolved:
        conflicts = resolved_set.intersection(components[component_id]["conflicts"])
        if conflicts:
            raise ValueError(f"{component_id} conflicts with {sorted(conflicts)}")

    resolved_components = []
    resolved_files = []
    for component_id in resolved:
        component = components[component_id]
        manifest_path = ROOT / component["manifest"]
        if digest(manifest_path) != component["manifest_sha256"]:
            raise ValueError(f"manifest hash mismatch: {component['manifest']}")
        resolved_components.append({key: component[key] for key in ("id", "kind", "version", "manifest", "manifest_sha256")})
        for file in component["files"]:
            if digest(ROOT / file["path"]) != file["sha256"]:
                raise ValueError(f"file hash mismatch: {file['path']}")
            resolved_files.append({"component": component_id, **file})

    return {
        "schema_version": "0.2",
        "greedyq_release": registry["release"],
        "registry_sha256": digest(REGISTRY_PATH),
        "object": components[profile]["object_name"],
        "profile": profile,
        "modules": sorted(component_id for component_id in resolved if components[component_id]["kind"] == "module"),
        "resolved_components": resolved_components,
        "resolved_files": resolved_files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True)
    parser.add_argument("--module", action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(resolve(args.profile, args.module), indent=2) + "\n"
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
