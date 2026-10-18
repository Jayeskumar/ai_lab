"""Command-line interface: ``python -m lab <command>``."""

from __future__ import annotations

import argparse
import sys

from . import db, records, render, runner
from .paths import JOURNAL_ENTRIES
from .util import append_jsonl, now_iso, read_jsonl


def cmd_run(args):
    scripts = runner.discover()
    ids = list(args.ids)
    if args.cycle:
        ids += [i for i, p in scripts.items() if i.startswith(f"EXP-{args.cycle}-")]
    if args.all:
        ids = sorted(scripts)
    if not ids:
        print("nothing to run; known experiments:", ", ".join(sorted(scripts)))
        return 1
    failed = 0
    for i in ids:
        out = runner.run(i, record=not args.dry)
        failed += out["error"] is not None
    return 1 if failed else 0


def cmd_verify(args):
    """Re-run every experiment and compare result hashes with the last recorded run."""
    scripts = runner.discover()
    ids = sorted(scripts) if not args.cycle else [i for i in sorted(scripts) if i.startswith(f"EXP-{args.cycle}-")]
    changed, errors = [], []
    for i in ids:
        rec = db.load("experiment", i)
        before = rec and (rec.get("runs") or [{}])[-1].get("results_sha256")
        out = runner.run(i, record=not args.dry, quiet=True)
        if out["error"]:
            errors.append(i)
        elif before and before != out["results_sha256"]:
            changed.append(i)
        print(f"{i}: {'ERROR' if out['error'] else ('same' if before == out['results_sha256'] else 'CHANGED' if before else 'new')}")
    print(f"verify: {len(ids)} experiments, {len(changed)} changed, {len(errors)} errors")
    return 1 if (changed or errors) else 0


def cmd_sync(args):
    records.sync()
    render.render_all()
    return 0


def cmd_lean(args):
    from . import lean_runner
    data = lean_runner.check_all(only=args.files or None, force=args.force)
    bad = [k for k, v in data["files"].items() if not v.get("ok") and not v.get("missing")]
    return 1 if bad else 0


def cmd_status(args):
    claims = db.all_records("claim")
    exps = db.all_records("experiment")
    from collections import Counter
    v = Counter(c["verification"] for c in claims)
    n = Counter(c.get("novelty") for c in claims)
    recs = records.load_all()
    print(f"cycles: {len(recs)} ({sum(r.get('status') == 'complete' for r in recs)} complete)")
    print(f"experiments: {len(exps)} recorded, {len(runner.discover())} scripts")
    print(f"claims: {len(claims)}")
    for s in db.VERIFICATION_STATUSES:
        print(f"  {s:28s} {v.get(s, 0)}")
    for s in db.NOVELTY_STATUSES:
        print(f"  {s:28s} {n.get(s, 0)}")
    print(f"journal entries: {len(read_jsonl(JOURNAL_ENTRIES))}")
    return 0


def cmd_journal(args):
    entry = {"key": f"manual-{now_iso()}", "cycle": args.cycle, "agent": args.agent, "kind": args.kind,
             "text": args.text, "refs": args.refs or [], "ts": now_iso()}
    append_jsonl(JOURNAL_ENTRIES, entry)
    print("journal entry appended:", entry["key"])
    return 0


def cmd_oeis(args):
    from . import oeis
    terms = [int(x) for x in args.terms.replace(" ", "").split(",") if x]
    print(oeis.novelty_check(terms))
    return 0


def cmd_report(args):
    from . import report
    s = report.write()
    import json
    print(json.dumps({k: v for k, v in s.items() if k != "potentially_novel"}, indent=1))
    print("potentially novel:", len(s["potentially_novel"]))
    return 0


def cmd_book(args):
    from . import book, catalogue
    for f in catalogue.build():
        print(f"[catalogue] wrote {f}")
    return book.build(pdf=not args.no_pdf)


def cmd_catalogue(args):
    from . import catalogue
    for f in catalogue.build():
        print(f"[catalogue] wrote {f}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m lab", description="Project Infinity research lab")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run experiments")
    r.add_argument("ids", nargs="*")
    r.add_argument("--cycle")
    r.add_argument("--all", action="store_true")
    r.add_argument("--dry", action="store_true", help="do not record results")
    r.set_defaults(func=cmd_run)
    v = sub.add_parser("verify", help="re-run experiments and compare result hashes")
    v.add_argument("--cycle")
    v.add_argument("--dry", action="store_true")
    v.set_defaults(func=cmd_verify)
    s = sub.add_parser("sync", help="sync cycle records into db/journal and render indexes")
    s.set_defaults(func=cmd_sync)
    l = sub.add_parser("lean", help="check Lean proof files")
    l.add_argument("files", nargs="*")
    l.add_argument("--force", action="store_true")
    l.set_defaults(func=cmd_lean)
    st = sub.add_parser("status", help="summary counts")
    st.set_defaults(func=cmd_status)
    j = sub.add_parser("journal", help="append a manual journal entry")
    j.add_argument("--cycle", required=True)
    j.add_argument("--agent", required=True)
    j.add_argument("--kind", required=True)
    j.add_argument("--text", required=True)
    j.add_argument("--refs", nargs="*")
    j.set_defaults(func=cmd_journal)
    o = sub.add_parser("oeis", help="look up a comma-separated integer sequence")
    o.add_argument("terms")
    o.set_defaults(func=cmd_oeis)
    rp = sub.add_parser("report", help="write reports/batch_statistics.json from the database")
    rp.set_defaults(func=cmd_report)
    b = sub.add_parser("book", help="build the textbook (HTML + PDF)")
    b.add_argument("--no-pdf", action="store_true")
    b.set_defaults(func=cmd_book)
    c = sub.add_parser("catalogue", help="regenerate the catalogue volumes (results, failures, open problems)")
    c.set_defaults(func=cmd_catalogue)
    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
