import importlib.util
from pathlib import Path

MODULE = Path(__file__).parents[1] / "verifier" / "verify.py"
spec = importlib.util.spec_from_file_location("verify", MODULE)
verify_module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(verify_module)


def claim(dependencies, findings=None):
    return {
        "claim_id": "test",
        "dependencies": dependencies,
        "findings": findings or [],
    }


def test_missing_required_dependency_fails_closed(tmp_path):
    result = verify_module.verify(claim([
        {"id": "raw-data", "required": True, "availability": "missing"}
    ]), tmp_path)
    assert result["status"] == "INCOMPLETE"


def test_complete_dependencies_are_not_automatically_verified(tmp_path):
    result = verify_module.verify(claim([
        {"id": "methods", "required": True, "availability": "available"}
    ]), tmp_path)
    assert result["status"] == "UNVERIFIABLE"


def test_explicit_reconstruction_can_verify(tmp_path):
    result = verify_module.verify(claim(
        [{"id": "methods", "required": True, "availability": "available"}],
        [{"test": "T6", "result": "PASS", "evidence": "recomputed", "interpretation": "matched"}],
    ), tmp_path)
    assert result["status"] == "VERIFIED"


def test_digest_drift_is_inconsistent(tmp_path):
    artifact = tmp_path / "raw.csv"
    artifact.write_text("changed", encoding="utf-8")
    result = verify_module.verify(claim([
        {
            "id": "raw-data", "required": True, "availability": "available",
            "source": "raw.csv", "sha256": "0" * 64
        }
    ]), tmp_path)
    assert result["status"] == "INCONSISTENT"


def test_declared_identifier_conflict_is_inconsistent(tmp_path):
    result = verify_module.verify(claim(
        [{"id": "sequence-id", "required": True, "availability": "available"}],
        [{
            "test": "T3",
            "result": "FAIL",
            "evidence": "artifact A and artifact B assert different versioned identifiers",
            "interpretation": "review required",
        }],
    ), tmp_path)
    assert result["status"] == "INCONSISTENT"
    assert result["blockers"]["declared_conflicts"] == ["T3"]


def test_integrity_conflict_outranks_missing_dependency(tmp_path):
    result = verify_module.verify(claim(
        [{"id": "raw-data", "required": True, "availability": "missing"}],
        [{
            "test": "T3", "result": "FAIL", "evidence": "identifier mismatch",
            "interpretation": "review required"
        }],
    ), tmp_path)
    assert result["status"] == "INCONSISTENT"
    assert result["blockers"]["unresolved_dependencies"] == ["raw-data"]


def test_reconstruction_failure_is_inconsistent(tmp_path):
    result = verify_module.verify(claim(
        [{"id": "raw-data", "required": True, "availability": "available"}],
        [{
            "test": "T6", "result": "FAIL", "evidence": "recomputed value diverged",
            "interpretation": "claim derivation did not reproduce"
        }],
    ), tmp_path)
    assert result["status"] == "INCONSISTENT"
