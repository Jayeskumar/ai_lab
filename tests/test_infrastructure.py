"""Tests for the lab infrastructure (registry, audit trail, property profiler)."""

import json

import numpy as np
import pytest

from lab import db, props


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setitem(db._DIRS, "experiment", tmp_path / "experiments")
    monkeypatch.setitem(db._DIRS, "claim", tmp_path / "claims")
    monkeypatch.setattr(db, "AUDIT_LOG", tmp_path / "audit.jsonl")
    return tmp_path


def _claim(**kw):
    base = {"type": "conjecture", "title": "t", "statement": "s", "verification": "CONJECTURE",
            "novelty": "NOT ASSESSED"}
    base.update(kw)
    return base


def test_claim_history_and_audit_are_append_only(tmp_db):
    db.save("claim", "CLM-T-01", _claim(), "tester", "create")
    db.save("claim", "CLM-T-01", _claim(verification="REFUTED", counterexample="x=1"), "skeptic", "found cex")
    rec = db.load("claim", "CLM-T-01")
    assert rec["verification"] == "REFUTED"
    changes = [h for h in rec["history"] if h.get("field") == "verification"]
    assert changes and changes[0]["old"] == "CONJECTURE" and changes[0]["new"] == "REFUTED"
    audit = [json.loads(x) for x in (tmp_db / "audit.jsonl").read_text().splitlines()]
    assert any(a.get("field") == "verification" and a["old"] == "CONJECTURE" for a in audit)


def test_missing_fields_are_never_erased(tmp_db):
    db.save("claim", "CLM-T-02", _claim(notes="keep me"), "a")
    db.save("claim", "CLM-T-02", _claim(), "b")  # update without 'notes'
    assert db.load("claim", "CLM-T-02")["notes"] == "keep me"


def test_proven_requires_proof_and_refuted_requires_counterexample(tmp_db):
    with pytest.raises(db.ValidationError):
        db.save("claim", "CLM-T-03", _claim(verification="PROVEN"), "a")
    with pytest.raises(db.ValidationError):
        db.save("claim", "CLM-T-04", _claim(verification="REFUTED"), "a")
    with pytest.raises(db.ValidationError):
        db.save("claim", "CLM-T-05", _claim(verification="PROVEN", proof="paper.md#1"), "a")
    db.save("claim", "CLM-T-05", _claim(verification="PROVEN", proof="paper.md#1", proof_check="lean"), "a")


def test_idempotent_save_produces_no_events(tmp_db):
    db.save("claim", "CLM-T-06", _claim(), "a")
    assert db.save("claim", "CLM-T-06", _claim(), "a") == []


def test_profile_group_and_nonassociative():
    n = 5
    Z = np.add.outer(np.arange(n), np.arange(n)) % n
    p = props.profile_table(Z)
    assert p["associative"]["holds"] and p["commutative"]["holds"]
    assert p["identity"]["element"] == 0 and p["inverses"]["holds"]
    S = (np.subtract.outer(np.arange(n), np.arange(n))) % n  # a-b: not associative
    q = props.profile_table(S)
    assert not q["associative"]["holds"]
    a, b, c = q["associative"]["counterexample"]
    assert S[S[a, b], c] != S[a, S[b, c]]


def test_profile_function_counterexample_is_genuine():
    res = props.profile_function(lambda a, b: a - b, range(4))
    a, b, c = res["associative"]["counterexample"][0]
    assert (a - b) - c != a - (b - c)
