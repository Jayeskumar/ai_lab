"""Tests for the batch 1.1 infrastructure: `lab check`, the journal sync, proof-kind and review classification,
Skeptic verdict parsing and the generated corrections log."""

import json

import pytest

from lab import catalogue, check, db, records, report
from lab.util import sha256_obj


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setitem(db._DIRS, "experiment", tmp_path / "experiments")
    monkeypatch.setitem(db._DIRS, "claim", tmp_path / "claims")
    monkeypatch.setattr(db, "AUDIT_LOG", tmp_path / "audit.jsonl")
    return tmp_path


def _write_record(root, cycle, text):
    d = root / "research" / "cycles" / f"{cycle}_test"
    d.mkdir(parents=True, exist_ok=True)
    (d / "record.yaml").write_text(text, encoding="utf-8")
    return d


# ------------------------------------------------------------------ anchors and strict YAML
def test_slug_follows_github_rules():
    assert check.slug("Theorem 7 (CLM-C19-14) — an O(log² n)-move method for L(n)") == \
        "theorem-7-clm-c19-14--an-olog-n-move-method-for-ln"
    assert check.slug("Theorem 3 (CLM-C09-03) — the window obstruction and density 1/φ²") == \
        "theorem-3-clm-c09-03--the-window-obstruction-and-density-1φ"
    assert check.slug("Law 167, x = (y∗x)∗(x∗y)") == "law-167-x--yxxy"


def test_anchors_number_duplicates_and_skip_code(tmp_path):
    f = tmp_path / "p.md"
    f.write_text("# A\n\n## Proof\n\n```\n# not a heading\n```\n\n## Proof\n", encoding="utf-8")
    assert check.anchors(f) == {"a", "proof", "proof-1"}


def test_strict_yaml_rejects_duplicate_keys():
    assert check.load_strict("a: 1\nb: [1, 2]\n") == {"a": 1, "b": [1, 2]}
    with pytest.raises(check.DuplicateKeyError):
        check.load_strict("claims:\n  - id: X\n    change_reason: one\n    change_reason: two\n")


# ------------------------------------------------------------------ result hashes
def test_results_hash_survives_int_keys_and_detects_edits():
    results = {"by_n": {2: "a", 10: "b"}, "named": {"10": 1, "2": 2}, "summary": ["s"], "timings": {"t": 1.5}}
    stored = sha256_obj({k: v for k, v in results.items() if k != "timings"})
    read_back = json.loads(json.dumps(results))           # int keys become strings
    assert sha256_obj({k: v for k, v in read_back.items() if k != "timings"}) != stored
    assert check.results_hash_matches(read_back, stored)
    read_back["named"]["2"] = 3
    assert not check.results_hash_matches(read_back, stored)


# ------------------------------------------------------------------ record checks
def test_check_records_reports_broken_references(tmp_db, tmp_path, monkeypatch):
    monkeypatch.setattr(records, "CYCLES", tmp_path / "research" / "cycles")
    monkeypatch.setattr(check, "ROOT", tmp_path)
    monkeypatch.setattr(check.runner, "discover", lambda: {"EXP-C01-01": tmp_path / "e.py"})
    (tmp_path / "proofs").mkdir()
    (tmp_path / "proofs" / "p.md").write_text("## Theorem 1 (CLM-C01-01) — fine\n", encoding="utf-8")
    _write_record(tmp_path, "C01", """cycle: C01
claims:
  - id: CLM-C01-01
    type: theorem
    title: t
    statement: s
    verification: PROVEN
    proof: proofs/p.md#theorem-1-clm-c01-01--fine
    proof_check: written proof
    evidence: [EXP-C01-01]
  - id: CLM-C01-02
    type: theorem
    title: t
    statement: s
    verification: PROVEN
    proof: proofs/p.md#no-such-heading
    proof_check: written proof
    evidence: [EXP-C01-09]
    related: [CLM-C01-07, proofs/missing.md]
journal:
  - key: C01-01
    agent: A
    kind: result
    text: x
  - key: C01-01
    agent: A
    kind: musing
    text: y
""")
    rep = check.Report()
    claims = check.check_records(rep)
    assert set(claims) == {"CLM-C01-01", "CLM-C01-02"}
    text = "\n".join(rep.errors)
    assert "no heading with anchor #no-such-heading" in text
    assert "unknown experiment EXP-C01-09" in text
    assert "unknown claim CLM-C01-07" in text
    assert "missing file proofs/missing.md" in text
    assert "duplicate journal key C01-01" in text
    assert "unknown kind 'musing'" in text
    assert not any("CLM-C01-01." in e for e in rep.errors)


def test_check_records_rejects_duplicate_yaml_keys(tmp_db, tmp_path, monkeypatch):
    monkeypatch.setattr(records, "CYCLES", tmp_path / "research" / "cycles")
    monkeypatch.setattr(check.runner, "discover", lambda: {})
    _write_record(tmp_path, "C02", "cycle: C02\ncycle: C02\n")
    rep = check.Report()
    check.check_records(rep)
    assert any("duplicate key 'cycle'" in e for e in rep.errors)


# ------------------------------------------------------------------ journal sync (regression: repeated revisions)
def test_sync_appends_one_revision_per_change(tmp_db, tmp_path, monkeypatch):
    journal = tmp_path / "entries.jsonl"
    monkeypatch.setattr(records, "CYCLES", tmp_path / "research" / "cycles")
    monkeypatch.setattr(records, "JOURNAL_ENTRIES", journal)
    rec = "cycle: C03\njournal:\n  - key: C03-01\n    agent: A\n    kind: {kind}\n    text: {text}\n"
    _write_record(tmp_path, "C03", rec.format(kind="result", text="first"))
    assert records.sync(verbose=False)["journal_added"] == 1
    assert records.sync(verbose=False)["journal_added"] == 0
    _write_record(tmp_path, "C03", rec.format(kind="result", text="second"))
    assert records.sync(verbose=False)["journal_added"] == 1
    assert records.sync(verbose=False)["journal_added"] == 0          # the old bug appended it again on every sync
    _write_record(tmp_path, "C03", rec.format(kind="correction", text="second"))
    assert records.sync(verbose=False)["journal_added"] == 0          # a kind change alone is not a revision
    keys = [json.loads(line)["key"] for line in journal.read_text().splitlines()]
    assert keys == ["C03-01", "C03-01#rev1"]
    rep = check.Report()
    monkeypatch.setattr(check, "JOURNAL_ENTRIES", journal)
    check.check_journal(rep)
    assert rep.errors == []


def test_check_journal_flags_repeated_revisions(tmp_path, monkeypatch):
    j = tmp_path / "entries.jsonl"
    rows = [{"key": "C04-01", "kind": "result", "text": "a"},
            {"key": "C04-01#rev1", "kind": "revision", "text": "[revision of C04-01] b"},
            {"key": "C04-01#rev2", "kind": "revision", "text": "[revision of C04-01] b"}]
    j.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    monkeypatch.setattr(check, "JOURNAL_ENTRIES", j)
    rep = check.Report()
    check.check_journal(rep)
    assert rep.errors == ["journal: C04-01#rev2 repeats the previous version of C04-01 unchanged"]


# ------------------------------------------------------------------ report classification
@pytest.mark.parametrize("text, kind", [
    ("Lean 4 (complete) - every part; the written argument was checked too", "Lean (complete)"),
    ("Lean 4 kernel decide on explicit tables", "Lean (complete)"),
    ("computer-assisted - uniqueness Lean-checked; wrap-around evaluated for N <= 4096",
     "Lean + written or computational parts"),
    ("written proof with a Lean-checked arithmetic core", "Lean + written or computational parts"),
    ("computer-assisted - DRUP proofs checked by drat-trim", "computer-assisted"),
    ("published theorem (Laver) - statement read verbatim", "published proof (literature)"),
    ("written proof (proofs/paper/C01.md Theorem 1)", "written proof"),
])
def test_proof_kind(text, kind):
    assert report.proof_kind(text) == kind


def test_skeptic_verdicts_and_review_state(tmp_path, monkeypatch):
    import lab.paths
    (tmp_path / "reviews").mkdir()
    (tmp_path / "reviews" / "skeptic_test.md").write_text(
        "| claim | verdict |\n|---|---|\n"
        "| CLM-C05-11 (no models of orders 8 \\| 10) | **UPHELD** | fine |\n"
        "| CLM-C05-12 (x) | **GAP** | step 3 |\n", encoding="utf-8")
    monkeypatch.setattr(lab.paths, "ROOT", tmp_path)
    v = report.skeptic_verdicts()
    assert v == {"CLM-C05-11": [("skeptic_test.md", "UPHELD")], "CLM-C05-12": [("skeptic_test.md", "GAP")]}
    assert report.review_state("written proof", v["CLM-C05-11"]) == "independently reviewed"
    assert report.review_state("written proof", v["CLM-C05-12"]) == "no review recorded"
    assert report.review_state("written proof, awaiting independent review", ()) == "awaiting independent review"


# ------------------------------------------------------------------ corrections log
def test_corrections_volume_lists_status_changes(tmp_db, tmp_path, monkeypatch):
    monkeypatch.setattr(records, "CYCLES", tmp_path / "none")
    monkeypatch.setattr(catalogue, "AUDIT_LOG", db.AUDIT_LOG)
    monkeypatch.setattr(catalogue, "JOURNAL_ENTRIES", tmp_path / "journal.jsonl")
    base = {"type": "conjecture", "title": "t", "statement": "s", "verification": "CONJECTURE"}
    db.save("claim", "CLM-C07-01", base, "a", "create")
    db.save("claim", "CLM-C07-01", dict(base, verification="REFUTED", counterexample="n = 5"), "skeptic",
            "Skeptic review - counterexample n = 5")
    db.save("claim", "CLM-C07-01", dict(base, verification="REFUTED", counterexample="n = 5", notes="x"), "a",
            "a note only")
    text = catalogue.corrections_volume()
    assert "* **CLM-C07-01**" in text
    assert "verification CONJECTURE → REFUTED" in text and "counterexample none → n = 5" not in text
    assert "counterexample revised" in text and "*Reason:* Skeptic review - counterexample n = 5" in text
    assert "a note only" not in text
    assert "| Skeptic review | 1 |" in text


def test_timing_fields_inside_hashed_results_are_flagged():
    results = {"benchmark": [{"n": 10, "greedy_s": 0.12, "p_divides_s": True}], "s": 2.5,
               "timings": {"total_s": 3.0}, "rows": [{"elapsed": 1.0, "count": 3}]}
    assert check._timing_like(results) == ["/benchmark[]/greedy_s", "/rows[]/elapsed"]
