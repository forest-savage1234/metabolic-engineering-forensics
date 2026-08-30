#!/usr/bin/env python3
"""Fail-closed verifier for bounded metabolic-engineering claim manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

FINAL = {"VERIFIED", "INCOMPLETE", "INCONSISTENT", "UNVERIFIABLE"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify(manifest: dict[str, Any], root: Path) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    required = [d for d in manifest.get("dependencies", []) if d.get("required")]

    unresolved = []
    inconsistent = []
    checked_hashes = 0

    for dep in required:
        availability = dep.get("availability", "unknown")
        if availability != "available":
            unresolved.append(dep["id"])
            continue

        source = dep.get("source")
        expected = dep.get("sha256")
        if expected and source:
            p = root / source
            if not p.is_file():
                unresolved.append(dep["id"])
                continue
            checked_hashes += 1
            if sha256(p).lower() != expected.lower():
                inconsistent.append(dep["id"])

    if unresolved:
        findings.append({
            "test": "T2",
            "result": "UNRESOLVED",
            "evidence": ", ".join(unresolved),
            "interpretation": "One or more required dependencies are not available for verification."
        })
    else:
        findings.append({
            "test": "T2", "result": "PASS", "evidence": "all required dependencies available",
            "interpretation": "The manifest declares closure over required dependencies."
        })

    if inconsistent:
        findings.append({
            "test": "T4", "result": "FAIL", "evidence": ", ".join(inconsistent),
            "interpretation": "Observed artifact bytes do not match the recorded reference state."
        })
    elif checked_hashes:
        findings.append({
            "test": "T4", "result": "PASS", "evidence": f"{checked_hashes} digest(s) matched",
            "interpretation": "Checked artifact bytes match their recorded source state."
        })

    # Fail closed. A VERIFIED result requires explicit reconstruction evidence;
    # dependency availability alone is never sufficient.
    explicit_reconstruction = any(
        f.get("test") == "T6" and f.get("result") == "PASS"
        for f in manifest.get("findings", [])
    )

    if inconsistent:
        status = "INCONSISTENT"
    elif unresolved:
        status = "INCOMPLETE"
    elif not explicit_reconstruction:
        status = "UNVERIFIABLE"
    else:
        status = "VERIFIED"

    assert status in FINAL
    return {
        "claim_id": manifest.get("claim_id"),
        "status": status,
        "generated_findings": findings,
        "principle": "Status concerns evidentiary reconstruction, not biological truth."
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    with args.manifest.open(encoding="utf-8") as fh:
        manifest = json.load(fh)
    print(json.dumps(verify(manifest, args.root), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
