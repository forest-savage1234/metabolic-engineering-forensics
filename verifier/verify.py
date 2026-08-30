#!/usr/bin/env python3
"""Fail-closed verifier for bounded metabolic-engineering claim manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

FINAL = {"VERIFIED", "INCOMPLETE", "INCONSISTENT", "UNVERIFIABLE"}
CONFLICT_TESTS = {"T3", "T4"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify(manifest: dict[str, Any], root: Path) -> dict[str, Any]:
    generated: list[dict[str, str]] = []
    declared_findings = manifest.get("findings", [])
    required = [d for d in manifest.get("dependencies", []) if d.get("required")]

    unresolved: list[str] = []
    byte_conflicts: list[str] = []
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
                byte_conflicts.append(dep["id"])

    generated.append({
        "test": "T2",
        "result": "UNRESOLVED" if unresolved else "PASS",
        "evidence": ", ".join(unresolved) if unresolved else "all required dependencies declared available",
        "interpretation": (
            "One or more required dependencies are not available for verification."
            if unresolved else
            "The manifest declares availability closure over required dependencies; reconstruction is evaluated separately."
        ),
    })

    if byte_conflicts:
        generated.append({
            "test": "T4", "result": "FAIL", "evidence": ", ".join(byte_conflicts),
            "interpretation": "Observed artifact bytes do not match the recorded reference state."
        })
    elif checked_hashes:
        generated.append({
            "test": "T4", "result": "PASS", "evidence": f"{checked_hashes} digest(s) matched",
            "interpretation": "Checked artifact bytes match their recorded source state."
        })

    explicit_conflicts = [
        f for f in declared_findings
        if f.get("test") in CONFLICT_TESTS and f.get("result") == "FAIL"
    ]
    reconstruction_pass = any(
        f.get("test") == "T6" and f.get("result") == "PASS"
        for f in declared_findings
    )
    reconstruction_fail = any(
        f.get("test") == "T6" and f.get("result") == "FAIL"
        for f in declared_findings
    )

    # Verdict precedence is deliberately fail-closed. An observed integrity conflict
    # outranks missing evidence; missing evidence outranks absence of reconstruction.
    if byte_conflicts or explicit_conflicts or reconstruction_fail:
        status = "INCONSISTENT"
    elif unresolved:
        status = "INCOMPLETE"
    elif not reconstruction_pass:
        status = "UNVERIFIABLE"
    else:
        status = "VERIFIED"

    blockers = {
        "unresolved_dependencies": unresolved,
        "byte_state_conflicts": byte_conflicts,
        "declared_conflicts": [f.get("test") for f in explicit_conflicts],
        "reconstruction_failed": reconstruction_fail,
        "reconstruction_passed": reconstruction_pass,
    }

    assert status in FINAL
    return {
        "claim_id": manifest.get("claim_id"),
        "status": status,
        "blockers": blockers,
        "generated_findings": generated,
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
