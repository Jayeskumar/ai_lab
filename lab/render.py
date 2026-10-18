"""Render the database and journal into human-readable Markdown."""

from __future__ import annotations

from collections import Counter, defaultdict

from . import db, records
from .paths import (CHECKPOINTS, CYCLES, DATABASE_MD, DISCOVERY_INDEX, JOURNAL_ENTRIES, JOURNAL_MD,
                    LEAN_RESULTS, rel)
from .util import now_iso, read_json, read_jsonl, write_json


def _one_line(s, n=160):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _claim_row(c):
    ev = ", ".join(c.get("evidence", []) or [])
    return (f"| {c['id']} | {_one_line(c['title'], 90)} | {c['verification']} | {c.get('novelty', 'NOT ASSESSED')} "
            f"| {ev} |")


def _table(claims, proof_column=False):
    if not claims:
        return "_None yet._\n"
    if proof_column:
        out = ["| Claim | Title | Proof check | Novelty | Evidence |", "|---|---|---|---|---|"]
        out += [f"| {c['id']} | {_one_line(c['title'], 90)} | {_one_line(c.get('proof_check'), 60)} | "
                f"{c.get('novelty', 'NOT ASSESSED')} | {', '.join(c.get('evidence', []) or [])} |" for c in claims]
        return "\n".join(out) + "\n"
    out = ["| Claim | Title | Verification | Novelty | Evidence |", "|---|---|---|---|---|"]
    out += [_claim_row(c) for c in claims]
    return "\n".join(out) + "\n"


def lean_status() -> dict:
    data = read_json(LEAN_RESULTS, {}) or {}
    return data.get("files", {})


def render_index() -> str:
    claims = db.all_records("claim")
    by_v = defaultdict(list)
    for c in claims:
        by_v[c["verification"]].append(c)
    novel = [c for c in claims if c.get("novelty") == "POTENTIALLY NOVEL"]
    redisc = [c for c in claims if c.get("novelty") == "REDISCOVERY"]
    algo = [c for c in claims if c.get("type") == "algorithmic"]
    counts = Counter(c["verification"] for c in claims)
    ncounts = Counter(c.get("novelty", "NOT ASSESSED") for c in claims)
    lines = [
        "# Discovery Index",
        "",
        f"_Generated {now_iso()} by `python -m lab sync` from `db/claims/`. Do not edit by hand._",
        "",
        "Every claim carries two independent labels: a **verification status** (PROVEN, COMPUTATIONALLY "
        "SUPPORTED, CONJECTURE, REFUTED, INCONCLUSIVE) and a **novelty status** (REDISCOVERY, POTENTIALLY "
        "NOVEL, NOT ASSESSED). A claim may therefore appear in more than one section below.",
        "",
        "## Summary",
        "",
        "| Verification status | Claims |", "|---|---|",
        *[f"| {s} | {counts.get(s, 0)} |" for s in db.VERIFICATION_STATUSES],
        "",
        "| Novelty status | Claims |", "|---|---|",
        *[f"| {s} | {ncounts.get(s, 0)} |" for s in db.NOVELTY_STATUSES],
        "",
        "## 1. Verified theorems (PROVEN)",
        "",
        _table(by_v["PROVEN"], proof_column=True),
        "## 2. Unproven conjectures (CONJECTURE and COMPUTATIONALLY SUPPORTED)",
        "",
        _table(by_v["CONJECTURE"] + by_v["COMPUTATIONALLY SUPPORTED"]),
        "## 3. Potentially novel ideas",
        "",
        "Novelty means only that no equivalent was found in the sources searched (recorded per claim in "
        "`novelty_basis`). It is never a confirmed priority claim.",
        "",
        _table(novel),
        "## 4. Rediscovered existing mathematics",
        "",
        _table(redisc),
        "## 5. Practical algorithmic results",
        "",
    ]
    if algo:
        lines += ["| Claim | Title | Outcome | Verification | Evidence |", "|---|---|---|---|---|"]
        for c in algo:
            lines.append(f"| {c['id']} | {_one_line(c['title'], 90)} | {c.get('improvement', '?')} | "
                         f"{c['verification']} | {', '.join(c.get('evidence', []) or [])} |")
        lines.append("")
    else:
        lines.append("_None yet._\n")
    lines += ["## 6. Refuted hypotheses", "", _table(by_v["REFUTED"]),
              "## 7. Inconclusive", "", _table(by_v["INCONCLUSIVE"])]
    return "\n".join(lines)


def render_journal() -> str:
    entries = read_jsonl(JOURNAL_ENTRIES)
    lines = ["# Research Journal", "",
             "_Rendered from the append-only log `journal/entries.jsonl`. Entries are never edited or "
             "removed; corrections appear as later `revision` entries._", ""]
    current = None
    for e in entries:
        if e.get("cycle") != current:
            current = e.get("cycle")
            lines += ["", f"## {current}", ""]
        refs = ", ".join(e.get("refs", []) or [])
        lines.append(f"### [{e['ts']}] {e['agent']} — {e['kind']} (`{e['key']}`)")
        lines.append("")
        lines.append(e["text"])
        if refs:
            lines.append("")
            lines.append(f"*Evidence:* {refs}")
        lines.append("")
    return "\n".join(lines)


def _field(name, value):
    if value in (None, "", [], {}):
        return []
    if isinstance(value, list):
        if all(isinstance(x, str) and len(x) < 140 for x in value):
            return [f"- **{name}:** " + "; ".join(value)]
        return [f"- **{name}:**"] + [f"  - {_one_line(x, 400)}" for x in value]
    if isinstance(value, dict):
        return [f"- **{name}:** `{value}`"]
    text = str(value).strip()
    if "\n" in text or len(text) > 200:
        return [f"- **{name}:**", "", "  " + text.replace("\n", "\n  "), ""]
    return [f"- **{name}:** {text}"]


def render_database() -> str:
    lines = ["# Discovery Database (human-readable dump)", "",
             f"_Generated {now_iso()} from `db/`. The JSON records are authoritative; every change is in "
             "`db/audit_log.jsonl`._", "", "## Claims", ""]
    for c in db.all_records("claim"):
        lines += [f"### {c['id']}: {c['title']}", ""]
        for k in ("cycle", "type", "system", "verification", "proof_check", "novelty", "improvement", "statement",
                  "proof", "lean",
                  "evidence", "counterexample", "novelty_basis", "references", "applications", "limitations",
                  "related", "skeptic", "notes"):
            lines += _field(k, c.get(k))
        hist = c.get("history", [])
        if len(hist) > 1:
            lines.append("- **status history:**")
            for h in hist:
                if h.get("event") == "changed" and h.get("field") in ("verification", "novelty", "improvement"):
                    lines.append(f"  - {h['ts']} {h['field']}: {h.get('old')} → {h.get('new')} ({h.get('actor')}; "
                                 f"{_one_line(h.get('reason'), 200)})")
        lines.append("")
    lines += ["## Experiments", ""]
    for e in db.all_records("experiment"):
        lines += [f"### {e['id']}: {e.get('title', '')}", ""]
        for k in ("cycle", "agent", "question", "hypothesis", "assumptions", "methodology", "falsification",
                  "theory", "summary", "analysis", "proof_attempts", "counterexamples", "verification", "novelty",
                  "applications", "related", "future"):
            lines += _field(k, e.get(k))
        runs = e.get("runs", [])
        if runs:
            last = runs[-1]
            lines.append(f"- **runs:** {len(runs)}; last {last.get('finished')} "
                         f"({last.get('runtime_s')} s), results sha256 `{str(last.get('results_sha256'))[:16]}…`, "
                         f"code `{(last.get('code') or {}).get('file')}`")
        lines.append("")
    return "\n".join(lines)


def render_cycle_index() -> str:
    lines = ["# Research Cycles", "", "| Cycle | Title | Branch | Status | Experiments | Claims |",
             "|---|---|---|---|---|---|"]
    for rec in records.load_all():
        d = rec["_dir"]
        lines.append(f"| [{rec['cycle']}]({d.name}/README.md) | {rec.get('title', '')} | {rec.get('branch', '')} | "
                     f"{rec.get('status', '')} | {len(rec.get('experiments', []) or [])} | "
                     f"{len(rec.get('claims', []) or [])} |")
    return "\n".join(lines) + "\n"


def checkpoint(next_priorities=None) -> dict:
    recs = records.load_all()
    claims = db.all_records("claim")
    exps = db.all_records("experiment")
    state = {
        "updated": now_iso(),
        "cycles_complete": [r["cycle"] for r in recs if r.get("status") == "complete"],
        "cycles_in_progress": [r["cycle"] for r in recs if r.get("status") not in (None, "complete")],
        "experiments": {e["id"]: (e.get("runs") or [{}])[-1].get("results_sha256") for e in exps},
        "claims": {c["id"]: [c["verification"], c.get("novelty")] for c in claims},
        "lean": {k: v.get("ok") for k, v in lean_status().items()},
        "next_priorities": next_priorities if next_priorities is not None else
        [d for r in recs for d in (r.get("next_directions") or [])][-30:],
    }
    write_json(CHECKPOINTS / "state.json", state)
    return state


def render_all() -> None:
    DISCOVERY_INDEX.write_text(render_index() + "\n", encoding="utf-8")
    JOURNAL_MD.write_text(render_journal() + "\n", encoding="utf-8")
    DATABASE_MD.write_text(render_database() + "\n", encoding="utf-8")
    CYCLES.mkdir(parents=True, exist_ok=True)
    (CYCLES / "INDEX.md").write_text(render_cycle_index(), encoding="utf-8")
    checkpoint()
    print(f"rendered {rel(DISCOVERY_INDEX)}, {rel(JOURNAL_MD)}, {rel(DATABASE_MD)}, research/cycles/INDEX.md, "
          f"checkpoints/state.json")
