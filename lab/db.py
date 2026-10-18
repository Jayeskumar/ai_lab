"""Append-only research database.

Every record (experiment or claim) is a JSON file ``db/<kind>s/<ID>.json``.
Records are never deleted.  Every change of a top-level field is written to

* the record's own ``history`` list (old value, new value, actor, reason), and
* the global append-only audit log ``db/audit_log.jsonl``.

Fields that are absent from an update keep their previous value, so a later
sync can never silently erase a finding.
"""

from __future__ import annotations

from .paths import AUDIT_LOG, CLAIM_DB, EXP_DB
from .util import append_jsonl, canonical_json, now_iso, read_json, write_json

VERIFICATION_STATUSES = (
    "PROVEN",                     # a valid proof has been verified
    "COMPUTATIONALLY SUPPORTED",  # experiments support it, no proof
    "CONJECTURE",                 # precise claim awaiting proof
    "REFUTED",                    # counterexample or contradiction found
    "INCONCLUSIVE",               # insufficient evidence
)
NOVELTY_STATUSES = (
    "REDISCOVERY",        # equivalent mathematics already exists
    "POTENTIALLY NOVEL",  # no equivalent found in the sources searched
    "NOT ASSESSED",
)
CLAIM_TYPES = ("theorem", "conjecture", "hypothesis", "observation", "algorithmic", "construction")
IMPROVEMENT_STATUSES = ("IMPROVEMENT", "MIXED", "NO IMPROVEMENT", "NOT APPLICABLE")

_DIRS = {"experiment": EXP_DB, "claim": CLAIM_DB}
_UNTRACKED = {"history", "runs"}


class ValidationError(ValueError):
    pass


def path_for(kind: str, rid: str):
    return _DIRS[kind] / f"{rid}.json"


def load(kind: str, rid: str) -> dict | None:
    return read_json(path_for(kind, rid))


def all_records(kind: str) -> list[dict]:
    d = _DIRS[kind]
    if not d.exists():
        return []
    return [read_json(p) for p in sorted(d.glob("*.json"))]


def validate_claim(rec: dict) -> None:
    v = rec.get("verification")
    if v not in VERIFICATION_STATUSES:
        raise ValidationError(f"{rec.get('id')}: verification {v!r} not in {VERIFICATION_STATUSES}")
    n = rec.get("novelty", "NOT ASSESSED")
    if n not in NOVELTY_STATUSES:
        raise ValidationError(f"{rec.get('id')}: novelty {n!r} not in {NOVELTY_STATUSES}")
    t = rec.get("type")
    if t not in CLAIM_TYPES:
        raise ValidationError(f"{rec.get('id')}: type {t!r} not in {CLAIM_TYPES}")
    imp = rec.get("improvement")
    if imp is not None and imp not in IMPROVEMENT_STATUSES:
        raise ValidationError(f"{rec.get('id')}: improvement {imp!r} not in {IMPROVEMENT_STATUSES}")
    if v == "PROVEN" and not (rec.get("proof") or rec.get("lean")):
        raise ValidationError(f"{rec.get('id')}: PROVEN requires a 'proof' reference or 'lean' file")
    if v == "PROVEN" and not rec.get("proof_check"):
        raise ValidationError(f"{rec.get('id')}: PROVEN requires 'proof_check' (how the proof was verified)")
    if v == "REFUTED" and not rec.get("counterexample"):
        raise ValidationError(f"{rec.get('id')}: REFUTED requires a 'counterexample'")
    for key in ("id", "title", "statement"):
        if not rec.get(key):
            raise ValidationError(f"claim missing {key!r}: {rec}")


def save(kind: str, rid: str, update: dict, actor: str, reason: str = "") -> list[dict]:
    """Create or update a record; return the list of change events."""
    if kind == "claim":
        merged_preview = {**(load(kind, rid) or {}), **update, "id": rid}
        validate_claim(merged_preview)
    old = load(kind, rid)
    ts = now_iso()
    events: list[dict] = []
    if old is None:
        rec = dict(update)
        rec["id"] = rid
        rec["history"] = [{"ts": ts, "actor": actor, "event": "created", "reason": reason}]
        events.append({"ts": ts, "kind": kind, "id": rid, "actor": actor, "event": "created",
                       "reason": reason, "new": {k: v for k, v in rec.items() if k not in _UNTRACKED}})
    else:
        rec = dict(old)
        for key, new_val in update.items():
            if key in _UNTRACKED:
                continue
            old_val = old.get(key)
            if canonical_json(old_val) != canonical_json(new_val):
                rec[key] = new_val
                ev = {"ts": ts, "actor": actor, "event": "changed", "field": key,
                      "old": old_val, "new": new_val, "reason": reason}
                rec.setdefault("history", []).append(ev)
                events.append({"kind": kind, "id": rid, **ev})
    if events:
        write_json(path_for(kind, rid), rec)
        for ev in events:
            append_jsonl(AUDIT_LOG, ev)
    return events


def append_run(rid: str, run_summary: dict, meta: dict, actor: str = "runner") -> None:
    """Record one execution of an experiment (creating the record if needed)."""
    rec = load("experiment", rid)
    base = {k: meta.get(k) for k in ("cycle", "title", "agent", "question", "hypothesis",
                                     "assumptions", "methodology", "falsification") if k in meta}
    if rec is None:
        save("experiment", rid, base, actor, reason="first run of experiment script")
        rec = load("experiment", rid)
    else:
        changed = {k: v for k, v in base.items() if canonical_json(rec.get(k)) != canonical_json(v)}
        if changed:
            save("experiment", rid, changed, actor, reason="experiment META changed in script")
            rec = load("experiment", rid)
    rec.setdefault("runs", []).append(run_summary)
    for k in ("code", "results_file", "results_sha256", "summary"):
        if k in run_summary:
            rec[k] = run_summary[k]
    write_json(path_for("experiment", rid), rec)
    append_jsonl(AUDIT_LOG, {"ts": run_summary.get("finished", now_iso()), "kind": "experiment", "id": rid,
                             "actor": actor, "event": "run", "results_sha256": run_summary.get("results_sha256"),
                             "reproduced": run_summary.get("reproduced")})
