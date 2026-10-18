"""Generate the catalogue volumes of the textbook from the claim database.

Three unnumbered chapters are written to ``textbook/src/generated/``:

* ``v06_results.md``  - Volume 6: verified theorems, supported claims and conjectures, by cycle;
* ``v09_failures.md`` - Volume 9: refuted hypotheses with their counterexamples;
* ``v10_open.md``     - Volume 10: open problems (unproven claims and next directions of every cycle).

The text is generated, never edited by hand, so the catalogue always agrees with ``db/claims``.
"""

from __future__ import annotations

import re
from collections import defaultdict

from . import db, records
from .paths import TEXTBOOK

OUT = TEXTBOOK / "src" / "generated"

_SPECIAL = re.compile(r"([\\`*_\[\]<>#|$~^])")


def esc(s) -> str:
    """Escape Markdown/TeX-active characters in database text and collapse whitespace."""
    s = " ".join(str(s or "").split())
    return _SPECIAL.sub(r"\\\1", s)


def _proof_kind(c: dict) -> str:
    pc = (c.get("proof_check") or "").lower()
    if pc.startswith("lean"):
        return "Lean"
    if "computer-assisted" in pc:
        return "computer-assisted"
    return "written"


def _by_cycle(claims):
    out = defaultdict(list)
    for c in claims:
        out[c.get("cycle", "?")].append(c)
    return dict(sorted(out.items()))


def _titles() -> dict:
    return {r["cycle"]: r.get("title", "") for r in records.load_all()}


def results_volume(claims) -> str:
    titles = _titles()
    lines = ["# Catalogue of results {.unnumbered}", "",
             "*Volume 6 — New conjectures and verified theorems. Generated from the claim database "
             "(`python -m lab catalogue`); every entry links to its record in `db/claims/`.*", "",
             "Proof kinds: **Lean** — machine-checked; **computer-assisted** — a finite certificate checked by a "
             "program; **written** — a complete written proof in `proofs/paper/`. Novelty labels are those of the "
             "Historian's audit; *rediscovery* means the result is in the literature.", ""]
    keep = [c for c in claims if c["verification"] in ("PROVEN", "COMPUTATIONALLY SUPPORTED", "CONJECTURE")]
    for cyc, cs in _by_cycle(keep).items():
        lines += [f"## {cyc} — {esc(titles.get(cyc, ''))}", ""]
        for label, head in (("PROVEN", "Theorems"), ("COMPUTATIONALLY SUPPORTED", "Computationally supported"),
                            ("CONJECTURE", "Conjectures")):
            sel = [c for c in cs if c["verification"] == label]
            if not sel:
                continue
            lines += [f"**{head}.**", ""]
            for c in sel:
                kind = f" ({_proof_kind(c)})" if label == "PROVEN" else ""
                nov = c.get("novelty", "NOT ASSESSED")
                lines.append(f"* **{c['id']}**{kind}, {nov.lower()}: {esc(c.get('title') or c.get('statement'))}.")
            lines.append("")
    return "\n".join(lines)


def failures_volume(claims) -> str:
    titles = _titles()
    lines = ["# Failed theories and counterexamples {.unnumbered}", "",
             "*Volume 9 — Failed theories and mathematical counterexamples. Generated from the claim database.*", "",
             "Every bold hypothesis the laboratory proposed and refuted is kept here with the counterexample that "
             "refuted it. Failures are part of the record: several of them (the Fibonacci pattern of Chapter 2, "
             "the non-rational complexity of Chapter 5, the odd and golden spectra of Chapter 7) led directly "
             "to the positive results of the book.", ""]
    sel = [c for c in claims if c["verification"] in ("REFUTED", "INCONCLUSIVE")]
    for cyc, cs in _by_cycle(sel).items():
        lines += [f"## {cyc} — {esc(titles.get(cyc, ''))}", ""]
        for c in cs:
            tag = "refuted" if c["verification"] == "REFUTED" else "inconclusive"
            lines.append(f"* **{c['id']}** ({tag}). *Claimed:* {esc(c.get('statement') or c.get('title'))}")
            ce = c.get("counterexample")
            if ce:
                if isinstance(ce, list):
                    ce = "; ".join(map(str, ce))
                lines.append(f"  *Counterexample:* {esc(ce)}")
            elif c.get("limitations"):
                lines.append(f"  *Status:* {esc(c['limitations'])}")
        lines.append("")
    return "\n".join(lines)


def open_volume(claims) -> str:
    lines = ["# Open problems {.unnumbered}", "",
             "*Volume 10 — Open problems and future research. Generated from the claim database and the cycle "
             "records.*", "",
             "## Unproven claims", "",
             "Each of these is supported by the evidence cited in its record but has no proof. A proof or a "
             "counterexample would settle it.", ""]
    for c in claims:
        if c["verification"] in ("COMPUTATIONALLY SUPPORTED", "CONJECTURE"):
            ev = ", ".join(c.get("evidence") or [])
            lines.append(f"* **{c['id']}** ({c['verification'].lower()}): {esc(c.get('statement') or c.get('title'))}"
                         + (f" *Evidence:* {esc(ev)}." if ev else ""))
    lines += ["", "## Directions proposed by the research cycles", ""]
    for r in records.load_all():
        nd = r.get("next_directions") or []
        if not nd:
            continue
        lines.append(f"**{r['cycle']} — {esc(r.get('title', ''))}.**")
        lines.append("")
        for d in nd:
            lines.append(f"* {esc(d)}")
        lines.append("")
    return "\n".join(lines)


def build() -> list[str]:
    claims = sorted(db.all_records("claim"), key=lambda c: c["id"])
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for name, text in (("v06_results.md", results_volume(claims)), ("v09_failures.md", failures_volume(claims)),
                       ("v10_open.md", open_volume(claims))):
        p = OUT / name
        p.write_text(text.rstrip() + "\n", encoding="utf-8")
        written.append(str(p.relative_to(TEXTBOOK.parent)))
    return written
