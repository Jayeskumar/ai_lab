"""Compute the quantitative part of a batch research report from the database."""

from __future__ import annotations

from collections import Counter

from . import db, records
from .paths import REPORTS
from .render import lean_status
from .util import now_iso, read_json


def stats() -> dict:
    claims = db.all_records("claim")
    exps = db.all_records("experiment")
    recs = records.load_all()
    v = Counter(c["verification"] for c in claims)
    n = Counter(c.get("novelty", "NOT ASSESSED") for c in claims)
    proof_checks = Counter()
    for c in claims:
        if c["verification"] != "PROVEN":
            continue
        pc = (c.get("proof_check") or "").lower()
        if pc.startswith("lean"):
            proof_checks["Lean-verified"] += 1
        elif "computer-assisted" in pc:
            proof_checks["computer-assisted"] += 1
        else:
            proof_checks["written proof"] += 1
    systems = Counter()
    for c in claims:
        systems[c.get("system") or "?"] += 1
    lean = lean_status()
    lean_theorems = sum(len(x.get("theorems", [])) for k, x in lean.items() if x.get("ok") and "C00" not in k)
    runs = sum(len(e.get("runs", [])) for e in exps)
    algo = [c for c in claims if c.get("type") == "algorithmic"]
    return {
        "generated": now_iso(),
        "cycles": len(recs),
        "cycles_complete": sum(r.get("status") == "complete" for r in recs),
        "experiments": len(exps),
        "experiment_runs": runs,
        "claims": len(claims),
        "verification": dict(v),
        "novelty": dict(n),
        "proven_by_check": dict(proof_checks),
        "claims_by_system": dict(systems),
        "lean_files_verified": sum(1 for k, x in lean.items() if x.get("ok") and "C00" not in k),
        "lean_theorems": lean_theorems,
        "algorithmic_claims": {c["id"]: c.get("improvement") for c in algo},
        "potentially_novel": [(c["id"], c["title"], c["verification"]) for c in claims
                              if c.get("novelty") == "POTENTIALLY NOVEL"],
    }


def write(path=None) -> dict:
    s = stats()
    path = path or REPORTS / "batch_statistics.json"
    from .util import write_json
    write_json(path, s)
    return s
