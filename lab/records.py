"""Synchronise human-written cycle records into the database and journal.

Each research cycle lives in ``research/cycles/<CNN>_<slug>/`` and contains

* ``README.md``   -- the full ten-step cycle report (prose), and
* ``record.yaml`` -- the machine-readable record: claims, experiment
  interpretations, journal entries and next directions.

``sync()`` is idempotent: it only writes when something changed, and every
change is recorded in the audit log by :mod:`lab.db`.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from . import db
from .paths import CYCLES, JOURNAL_ENTRIES
from .util import append_jsonl, canonical_json, now_iso, read_jsonl

CLAIM_FIELDS = (
    "type", "title", "statement", "verification", "novelty", "novelty_basis", "proof", "lean",
    "evidence", "references", "counterexample", "improvement", "applications", "related",
    "skeptic", "system", "notes", "limitations", "proof_check",
)
EXPERIMENT_FIELDS = (
    "analysis", "proof_attempts", "counterexamples", "verification", "novelty", "applications",
    "related", "future", "theory",
)
JOURNAL_KINDS = (
    "hypothesis", "experiment", "result", "failure", "rejection", "pattern", "surprise",
    "contradiction", "disagreement", "direction", "revision", "proof", "novelty", "infrastructure",
    "decision", "review",
)


def cycle_dirs() -> list[Path]:
    return sorted(p for p in CYCLES.iterdir() if p.is_dir() and (p / "record.yaml").exists()) if CYCLES.exists() else []


def load_record(cycle_dir: Path) -> dict:
    rec = yaml.safe_load((cycle_dir / "record.yaml").read_text(encoding="utf-8"))
    rec["_dir"] = cycle_dir
    return rec


def load_all() -> list[dict]:
    return [load_record(d) for d in cycle_dirs()]


def _strip(v):
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, list):
        return [_strip(x) for x in v]
    if isinstance(v, dict):
        return {k: _strip(x) for k, x in v.items()}
    return v


def sync(verbose: bool = True) -> dict:
    stats = {"claims_changed": 0, "experiments_changed": 0, "journal_added": 0, "warnings": []}
    journal = read_jsonl(JOURNAL_ENTRIES)
    known_keys = {e["key"]: e for e in journal}
    for rec in load_all():
        cyc = rec["cycle"]
        actor = f"sync:{cyc}"
        for c in rec.get("claims", []) or []:
            fields = {k: _strip(c[k]) for k in CLAIM_FIELDS if k in c}
            fields["cycle"] = cyc
            fields.setdefault("novelty", "NOT ASSESSED")
            reason = _strip(c.get("change_reason", "cycle record sync"))
            ev = db.save("claim", c["id"], fields, actor, reason)
            stats["claims_changed"] += bool(ev)
        for e in rec.get("experiments", []) or []:
            if db.load("experiment", e["id"]) is None:
                stats["warnings"].append(f"{e['id']} interpreted in {cyc} but never run")
                continue
            fields = {k: _strip(e[k]) for k in EXPERIMENT_FIELDS if k in e}
            if fields:
                ev = db.save("experiment", e["id"], fields, actor, _strip(e.get("change_reason", "cycle record sync")))
                stats["experiments_changed"] += bool(ev)
        for j in rec.get("journal", []) or []:
            key = j["key"]
            entry = {
                "key": key, "cycle": cyc, "agent": j["agent"], "kind": j["kind"],
                "text": _strip(j["text"]), "refs": j.get("refs", []),
            }
            if j["kind"] not in JOURNAL_KINDS:
                stats["warnings"].append(f"journal {key}: unknown kind {j['kind']}")
            if key in known_keys:
                old = known_keys[key]
                if canonical_json({k: old.get(k) for k in entry}) != canonical_json(entry):
                    # journal is append-only: record the revision as a new entry
                    n = sum(1 for k in known_keys if k.startswith(key + "#rev")) + 1
                    rev = dict(entry, key=f"{key}#rev{n}", kind="revision", ts=now_iso(),
                               text=f"[revision of {key}] " + entry["text"])
                    append_jsonl(JOURNAL_ENTRIES, rev)
                    known_keys[rev["key"]] = rev
                    stats["journal_added"] += 1
                continue
            entry["ts"] = j.get("ts") or now_iso()
            append_jsonl(JOURNAL_ENTRIES, entry)
            known_keys[key] = entry
            stats["journal_added"] += 1
    if verbose:
        print(f"sync: {stats['claims_changed']} claims changed, {stats['experiments_changed']} experiments "
              f"changed, {stats['journal_added']} journal entries added")
        for w in stats["warnings"]:
            print("  warning:", w)
    return stats
