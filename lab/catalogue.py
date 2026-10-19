"""Generate the catalogue volumes of the textbook from the claim database.

Four unnumbered chapters are written to ``textbook/src/generated/``:

* ``v06_results.md``  - Volume 6: verified theorems, supported claims and conjectures, by cycle;
* ``v09_failures.md`` - Volume 9: refuted hypotheses with their counterexamples;
* ``v10_open.md``     - Volume 10: open problems (unproven claims and next directions of every cycle);
* ``appendix_corrections.md`` - the corrections log: every change of a claim's status, novelty or wording after
  its creation, with the recorded reason (from ``db/audit_log.jsonl``), and every re-run that changed a result.

The text is generated, never edited by hand, so the catalogue always agrees with ``db/claims``.
"""

from __future__ import annotations

import re
from collections import defaultdict

from . import db, records
from .paths import AUDIT_LOG, JOURNAL_ENTRIES, TEXTBOOK
from .report import proof_kind
from .util import read_jsonl

OUT = TEXTBOOK / "src" / "generated"

_SPECIAL = re.compile(r"([\\`*_\[\]<>#|$~^])")


def esc(s) -> str:
    """Escape Markdown/TeX-active characters in database text and collapse whitespace."""
    s = " ".join(str(s or "").split())
    return _SPECIAL.sub(r"\\\1", s)


_KIND_LABEL = {"Lean (complete)": "Lean", "Lean + written or computational parts": "Lean + written",
               "computer-assisted": "computer-assisted", "written proof": "written",
               "published proof (literature)": "literature"}


def _proof_kind(c: dict) -> str:
    return _KIND_LABEL[proof_kind(c.get("proof_check") or "")]


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
             "Proof kinds: **Lean** — machine-checked; **Lean + written** — a written proof whose core steps are "
             "machine-checked; **computer-assisted** — a finite certificate checked by a program; **written** — a "
             "complete written proof in `proofs/paper/`; **literature** — a published theorem whose statement the "
             "lab read. Novelty labels are those of the Historian's audit; *rediscovery* means the result is in the "
             "literature.", ""]
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


CORRECTION_FIELDS = ("verification", "novelty", "type", "improvement", "title", "statement", "counterexample")
_SHORT = ("verification", "novelty", "type", "improvement")


def _source(reason: str) -> str:
    r = reason.lower()
    for key, label in (("skeptic", "Skeptic review"), ("historian", "Historian audit"), ("lab check", "lab check"),
                       ("batch 1.1", "batch 1.1 sprint")):
        if key in r:
            return label
    return "research cycle" if r in ("", "cycle record sync") else "Director"


def corrections_volume() -> str:
    events = [a for a in read_jsonl(AUDIT_LOG)
              if a.get("event") == "changed" and a.get("kind") == "claim" and a.get("field") in CORRECTION_FIELDS]
    # one entry per claim, time stamp and reason
    groups = defaultdict(list)
    for a in events:
        groups[(a["id"], a["ts"], a.get("reason", ""))].append(a)
    by_cycle = defaultdict(list)
    for (cid, ts, reason), evs in sorted(groups.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        by_cycle[cid.split("-")[1]].append((cid, ts, reason, evs))
    sources = defaultdict(set)
    for (cid, _, reason), _evs in groups.items():
        sources[_source(reason)].add(cid)
    lines = ["# Appendix — Corrections log {.unnumbered}", "",
             "*Generated from the append-only audit log `db/audit_log.jsonl` (`python -m lab catalogue`).*", "",
             f"Every change of a claim's verification status, novelty label, type, improvement status, title, "
             f"statement or counterexample made after the claim was first recorded: {len(events)} field changes "
             f"in {len(groups)} entries on {len({k[0] for k in groups})} claims. Changes to the supporting texts "
             f"(analysis, proof notes, novelty bases, references) are in the audit log but not listed here.", "",
             "| source of the change | claims affected |", "|---|---|"]
    for src in sorted(sources, key=lambda k: -len(sources[k])):
        lines.append(f"| {src} | {len(sources[src])} |")
    lines.append("")
    titles = _titles()
    for cyc, items in sorted(by_cycle.items()):
        lines += [f"## {cyc} — {esc(titles.get(cyc, ''))}", ""]
        for cid, ts, reason, evs in items:
            parts = []
            for a in evs:
                f = a["field"]
                if f in _SHORT:
                    parts.append(f"{f} {esc(a.get('old') or 'none')} → {esc(a.get('new'))}")
                elif f == "title":
                    parts.append(f"title revised (was: {esc(a.get('old'))})")
                else:
                    parts.append(f"{f} revised")
            why = esc(reason) if reason and reason != "cycle record sync" else "no reason recorded"
            lines.append(f"* **{cid}**, {ts[:10]}: " + "; ".join(parts) + f". *Reason:* {why}")
        lines.append("")
    lines += ["## Experiment results that changed on a re-run", "",
              "A re-run whose result hash differs from the previous run of the same experiment. The runner records "
              "the hash of the script and of `systems/` with every run, so the cause can be read off.", "",
              "| experiment | re-run | what changed since the previous run |", "|---|---|---|"]
    for e in db.all_records("experiment"):
        runs = e.get("runs") or []
        for prev, cur in zip(runs, runs[1:]):
            if prev.get("results_sha256") == cur.get("results_sha256"):
                continue
            pc, cc = prev.get("code") or {}, cur.get("code") or {}
            what = [w for w, k in (("script", "sha256"), ("systems/", "systems_sha256")) if pc.get(k) != cc.get(k)]
            lines.append(f"| {e['id']} | {(cur.get('started') or '')[:16].replace('T', ' ')} | "
                         f"{' and '.join(what) if what else 'no code change recorded (external data, e.g. an OEIS lookup)'} |")
    lines += ["", "## Corrections recorded in the journal", ""]
    for j in read_jsonl(JOURNAL_ENTRIES):
        if j.get("kind") == "correction":
            lines.append(f"* **{j['key']}** ({j.get('cycle')}): {esc(j.get('text'))}")
    return "\n".join(lines)


def build() -> list[str]:
    claims = sorted(db.all_records("claim"), key=lambda c: c["id"])
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    for name, text in (("v06_results.md", results_volume(claims)), ("v09_failures.md", failures_volume(claims)),
                       ("v10_open.md", open_volume(claims)), ("appendix_corrections.md", corrections_volume())):
        p = OUT / name
        p.write_text(text.rstrip() + "\n", encoding="utf-8")
        written.append(str(p.relative_to(TEXTBOOK.parent)))
    return written
