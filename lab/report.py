"""Compute the quantitative part of a batch research report from the database."""

from __future__ import annotations

from collections import Counter

from . import db, records
from .paths import REPORTS
from .render import lean_status
from .util import now_iso, read_json


def proof_kind(proof_check: str) -> str:
    """Coarse class of a PROVEN claim's evidence, read from its proof_check text."""
    pc = proof_check.lower()
    lean = "lean" in pc
    written = "written" in pc or "by hand" in pc or "proved (" in pc
    computed = "computer-assisted" in pc
    if pc.startswith("published theorem") or "read verbatim" in pc:
        return "published proof (literature)"
    if pc.startswith("lean 4 (complete"):
        return "Lean (complete)"
    if lean and not (written or computed):
        return "Lean (complete)"
    if lean:
        return "Lean + written or computational parts"
    if computed:
        return "computer-assisted"
    return "written proof"


def skeptic_verdicts() -> dict:
    """Claim id -> list of (review file, verdict) read from the verdict tables of reviews/skeptic_*.md."""
    import re
    from .paths import ROOT
    pat = re.compile(r"^\|\s*(CLM-C\d\d-\d\d)\b(?:[^|\\]|\\.)*\|\s*\*\*([^*]+)\*\*")   # a cell may contain escaped pipes
    out: dict = {}
    for f in sorted((ROOT / "reviews").glob("skeptic_*.md")):
        for line in f.read_text().splitlines():
            m = pat.match(line)
            if m:
                out.setdefault(m.group(1), []).append((f.name, m.group(2).strip()))
    return out


def review_state(proof_check: str, verdicts=()) -> str:
    """Whether a non-formal proof was re-checked by someone other than its author (the proof_check text, or an
    UPHELD verdict in a Skeptic review table)."""
    pc = proof_check.lower()
    if "awaiting independent" in pc:
        return "awaiting independent review"
    if "skeptic-reviewed" in pc or "by the skeptic" in pc or "skeptic review" in pc or \
            any(v.upper().startswith("UPHELD") for _, v in verdicts):
        return "independently reviewed"
    return "no review recorded"


def stats() -> dict:
    claims = db.all_records("claim")
    exps = db.all_records("experiment")
    recs = records.load_all()
    v = Counter(c["verification"] for c in claims)
    n = Counter(c.get("novelty", "NOT ASSESSED") for c in claims)
    proof_checks = Counter()
    review = Counter()
    verdicts = skeptic_verdicts()
    for c in claims:
        if c["verification"] != "PROVEN":
            continue
        kind = proof_kind(c.get("proof_check") or "")
        proof_checks[kind] += 1
        if kind != "Lean (complete)":
            review[review_state(c.get("proof_check") or "", verdicts.get(c["id"], ()))] += 1
    verdict_counts = Counter(v.split(" (")[0].split(" —")[0].strip() for vs in verdicts.values() for _, v in vs[-1:])
    unreviewed = sorted(c["id"] for c in claims if c["id"] not in verdicts)
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
        "proven_not_fully_formal_by_review": dict(review),
        "skeptic_verdicts": {"claims_with_a_verdict": len(verdicts), "latest_verdicts": dict(verdict_counts),
                             "claims_without_a_verdict": unreviewed},
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


# ---------------------------------------------------------------------------------------------- markdown tables
def _esc(s) -> str:
    return " ".join(str(s or "").split()).replace("|", "\\|")


def render_tables() -> str:
    """Markdown with the quantitative items of the batch report, generated from the database."""
    s = stats()
    claims = sorted(db.all_records("claim"), key=lambda c: c["id"])
    exps = db.all_records("experiment")
    recs = sorted(records.load_all(), key=lambda r: r["cycle"])
    out = [f"# Batch report — generated data ({s['generated']})", "",
           "Generated by `python -m lab report` from `db/` and `research/cycles/`; do not edit by hand.", ""]
    out += ["## 1. Experiments", "",
            f"{s['experiments']} experiments recorded ({s['experiment_runs']} recorded runs) in {s['cycles']} "
            f"cycles ({s['cycles_complete']} complete).", "",
            "| cycle | experiments |", "|---|---|"]
    by_cycle = {}
    for e in exps:
        by_cycle.setdefault(e.get("cycle", e["id"][4:7]), []).append(e["id"])
    for cyc in sorted(by_cycle):
        out.append(f"| {cyc} | {len(by_cycle[cyc])} |")
    out += ["", "## 2. Systems and cycles investigated", "", "| cycle | title | systems | claims |", "|---|---|---|---|"]
    n_claims = {}
    for c in claims:
        n_claims[c.get("cycle")] = n_claims.get(c.get("cycle"), 0) + 1
    for r in recs:
        out.append(f"| {r['cycle']} | {_esc(r.get('title'))} | {', '.join(r.get('systems') or [])} | "
                   f"{n_claims.get(r['cycle'], 0)} |")
    out += ["", "## Verification and novelty status", "", "| status | claims |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in sorted(s["verification"].items())]
    out += ["", "| novelty | claims |", "|---|---|"] + [f"| {k} | {v} |" for k, v in sorted(s["novelty"].items())]
    out += ["", "| proof kind (PROVEN claims) | claims |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in sorted(s["proven_by_check"].items())]
    out += ["", "Classes are read from each claim's `proof_check` text; \"parts\" means that some steps",
            "of the proof are written or computational rather than formal.", "",
            "| review of the PROVEN claims that are not fully formal | claims |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in sorted(s["proven_not_fully_formal_by_review"].items())]
    sv = s["skeptic_verdicts"]
    out += ["", f"Independent Skeptic reviews (`reviews/skeptic_*.md`) gave a verdict on {sv['claims_with_a_verdict']} "
            f"of the {s['claims']} claims:", "", "| latest verdict | claims |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in sorted(sv["latest_verdicts"].items())]
    out += ["", "Claims without a Skeptic verdict: " + (", ".join(sv["claims_without_a_verdict"]) or "none") + "."]
    out += ["", f"Lean: {s['lean_files_verified']} files verified, {s['lean_theorems']} theorems (standard axioms "
            f"only).", ""]

    def table(title, sel, extra=None):
        rows = [f"## {title}", "", f"{len(sel)} claims.", "", "| id | title | verification | novelty |"
                + (f" {extra[0]} |" if extra else ""), "|---|---|---|---|" + ("---|" if extra else "")]
        for c in sel:
            rows.append(f"| {c['id']} | {_esc(c.get('title'))} | {c['verification']} | {c.get('novelty')} |"
                        + (f" {_esc(extra[1](c))} |" if extra else ""))
        return rows + [""]

    out += table("3. Verified theorems (PROVEN)", [c for c in claims if c["verification"] == "PROVEN"],
                 ("proof check", lambda c: (c.get("proof_check") or "")[:120]))
    out += table("4. Conjectures and computationally supported claims",
                 [c for c in claims if c["verification"] in ("CONJECTURE", "COMPUTATIONALLY SUPPORTED")])
    out += table("5. Refuted hypotheses", [c for c in claims if c["verification"] == "REFUTED"],
                 ("counterexample", lambda c: str(c.get("counterexample") or "")[:140]))
    out += table("6. Rediscoveries", [c for c in claims if c.get("novelty") == "REDISCOVERY"])
    out += table("7. Potentially novel findings", [c for c in claims if c.get("novelty") == "POTENTIALLY NOVEL"],
                 ("basis", lambda c: (c.get("novelty_basis") or "")[:160]))
    out += table("8. Performance claims (algorithmic)", [c for c in claims if c.get("type") == "algorithmic"],
                 ("improvement", lambda c: (f"{c.get('improvement')}: {c['improvement_detail']}"
                                             if c.get("improvement_detail") else str(c.get("improvement")))[:200]))
    out += table("Inconclusive", [c for c in claims if c["verification"] == "INCONCLUSIVE"])
    out += ["## 9. Unresolved problems and next directions (from the cycle records)", ""]
    for r in recs:
        for d in r.get("next_directions") or []:
            out.append(f"* {_esc(d)}")
    return "\n".join(out) + "\n"


def write_markdown(path=None) -> str:
    path = path or REPORTS / "REPORT_DATA.md"
    path.write_text(render_tables(), encoding="utf-8")
    return str(path)
