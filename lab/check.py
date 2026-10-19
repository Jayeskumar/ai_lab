"""Consistency checks over the whole lab: ``python -m lab check``.

The checks are read-only. Each finding is an *error* (the lab is inconsistent:
a broken reference, an invalid record, a corrupted result file) or a
*warning* (something to look at: a record not yet synced, a result produced
by an older version of its script). The command fails if there is an error.

Checked:

* every ``record.yaml`` parses, with duplicate mapping keys rejected (plain
  YAML silently keeps the last value, which once hid a lost ``change_reason``);
* claim ids are unique, belong to the record's cycle and pass
  :func:`lab.db.validate_claim`; journal keys are unique and their kinds known;
* every reference resolves: ``evidence`` and ``related`` ids, ``proof`` files
  and their ``#anchor`` (a GitHub-style heading slug), ``lean`` files;
* the database agrees with the records (``lab sync`` has been run) and has no
  claim that no record mentions;
* the journal has unique keys and no revision that repeats the version before it;
* every result file is intact (its stored hash is the hash of its results),
  matches the last run recorded in the database, and was produced by the
  current version of its script.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import db, records, runner
from .paths import JOURNAL_ENTRIES, RESULTS, ROOT, rel
from .util import canonical_json, read_json, read_jsonl, sha256_file, sha256_obj

CLAIM_ID = re.compile(r"^CLM-(C\d\d)-\d\d$")
EXP_ID = re.compile(r"^EXP-(C\d\d)-\d\d$")


def _rel(path) -> str:
    try:
        return rel(path)
    except ValueError:      # outside the repository (tests)
        return str(path)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


# ------------------------------------------------------------------ YAML with duplicate keys rejected
class DuplicateKeyError(yaml.YAMLError):
    pass


class _StrictLoader(yaml.SafeLoader):
    pass


def _strict_mapping(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise DuplicateKeyError(f"duplicate key {key!r} at line {key_node.start_mark.line + 1}")
        seen.add(key)
    return loader.construct_mapping(node, deep=deep)


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _strict_mapping)


def load_strict(text: str):
    return yaml.load(text, Loader=_StrictLoader)


# ------------------------------------------------------------------ Markdown anchors
def slug(heading: str) -> str:
    """GitHub's anchor for a Markdown heading: lower case; keep letters, marks, decimal digits, connector
    punctuation, hyphens and spaces (Ruby's [\\p{Word}\\- ], so superscripts such as the 2 in n^2 are dropped);
    spaces to hyphens."""
    keep = (c for c in heading.strip().lower()
            if c in "- " or unicodedata.category(c)[0] in "LM" or unicodedata.category(c) in ("Nd", "Pc"))
    return "".join(keep).replace(" ", "-")


def anchors(path: Path) -> set[str]:
    out, seen = set(), {}
    in_code = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            s = slug(m.group(1))
            k = seen.get(s, 0)
            out.add(s if k == 0 else f"{s}-{k}")
            seen[s] = k + 1
    return out


# ------------------------------------------------------------------ checks
def _check_reference(ref: str, where: str, rep: Report, claims: set, experiments: set, cache: dict) -> None:
    if CLAIM_ID.match(ref):
        if ref not in claims:
            rep.error(f"{where}: unknown claim {ref}")
        return
    if EXP_ID.match(ref):
        if ref not in experiments:
            rep.error(f"{where}: unknown experiment {ref}")
        return
    if ref.startswith(("http://", "https://")) or " " in ref:
        return  # a URL or a free-text note
    path, _, anchor = ref.partition("#")
    p = ROOT / path
    if not p.exists():
        rep.error(f"{where}: missing file {path}")
        return
    if anchor and p.suffix == ".md":
        if p not in cache:
            cache[p] = anchors(p)
        if anchor not in cache[p]:
            rep.error(f"{where}: no heading with anchor #{anchor} in {path}")


def check_records(rep: Report) -> dict:
    """Parse and cross-check the cycle records; returns {claim id: (cycle, fields)}."""
    parsed = []
    for d in records.cycle_dirs():
        f = d / "record.yaml"
        try:
            rec = load_strict(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            rep.error(f"{_rel(f)}: {exc}")
            continue
        if not isinstance(rec, dict) or not rec.get("cycle"):
            rep.error(f"{_rel(f)}: no 'cycle' field")
            continue
        if not d.name.startswith(rec["cycle"] + "_"):
            rep.error(f"{_rel(f)}: cycle {rec['cycle']} does not match the directory name")
        parsed.append((f, rec))

    scripts = runner.discover()
    experiments = set(scripts) | {r["id"] for r in db.all_records("experiment")}
    claims: dict[str, tuple[str, dict]] = {}
    for f, rec in parsed:
        for c in rec.get("claims") or []:
            cid = c.get("id", "")
            m = CLAIM_ID.match(cid)
            if not m:
                rep.error(f"{_rel(f)}: malformed claim id {cid!r}")
                continue
            if m.group(1) != rec["cycle"]:
                rep.error(f"{_rel(f)}: claim {cid} filed under cycle {rec['cycle']}")
            if cid in claims:
                rep.error(f"{_rel(f)}: duplicate claim id {cid}")
            fields = {k: records._strip(c[k]) for k in records.CLAIM_FIELDS if k in c}
            fields.setdefault("novelty", "NOT ASSESSED")
            claims[cid] = (rec["cycle"], fields)
            try:
                db.validate_claim({**fields, "id": cid})
            except db.ValidationError as exc:
                rep.error(f"{_rel(f)}: {exc}")

    cache: dict = {}
    journal_keys: set[str] = set()
    for f, rec in parsed:
        for c in rec.get("claims") or []:
            cid = c.get("id", "?")
            for ref in c.get("evidence") or []:
                if not EXP_ID.match(str(ref)):
                    rep.error(f"{cid}.evidence: {ref!r} is not an experiment id")
                elif ref not in experiments:
                    rep.error(f"{cid}.evidence: unknown experiment {ref}")
                elif ref not in scripts:
                    rep.warn(f"{cid}.evidence: {ref} has no script")
            for ref in c.get("related") or []:
                _check_reference(str(ref), f"{cid}.related", rep, set(claims), experiments, cache)
            if c.get("proof"):
                _check_reference(str(c["proof"]), f"{cid}.proof", rep, set(claims), experiments, cache)
            for ref in c.get("lean") or []:
                if not (ROOT / ref).exists():
                    rep.error(f"{cid}.lean: missing file {ref}")
        for e in rec.get("experiments") or []:
            if e.get("id") not in experiments:
                rep.warn(f"{_rel(f)}: experiment {e.get('id')} interpreted but never run")
            for ref in e.get("related") or []:
                _check_reference(str(ref), f"{e.get('id')}.related", rep, set(claims), experiments, cache)
        for j in rec.get("journal") or []:
            key = j.get("key")
            if key in journal_keys:
                rep.error(f"{_rel(f)}: duplicate journal key {key}")
            journal_keys.add(key)
            if j.get("kind") not in records.JOURNAL_KINDS:
                rep.error(f"{_rel(f)}: journal {key}: unknown kind {j.get('kind')!r}")
            for ref in j.get("refs") or []:
                _check_reference(str(ref), f"journal {key}", rep, set(claims), experiments, cache)
    return claims


def check_database(rep: Report, claims: dict) -> None:
    for c in db.all_records("claim"):
        cid = c["id"]
        if cid not in claims:
            rep.warn(f"db claim {cid} is not in any record")
            continue
        cycle, fields = claims[cid]
        stale = sorted(k for k, v in {**fields, "cycle": cycle}.items()
                       if canonical_json(c.get(k)) != canonical_json(v))
        if stale:
            rep.warn(f"db claim {cid} differs from its record in {', '.join(stale)} (run `python -m lab sync`)")
    for cid in sorted(set(claims) - {c["id"] for c in db.all_records("claim")}):
        rep.warn(f"claim {cid} is not in the database (run `python -m lab sync`)")


def _int_like(k) -> bool:
    return isinstance(k, str) and k.lstrip("-").isdigit() and str(int(k)) == k


def results_hash_matches(results: dict, stored: str, max_ambiguous: int = 10) -> bool:
    """Does the stored hash match the results read back from JSON?

    The runner hashes the Python objects, and a dict with int keys is sorted numerically there but comes back from
    JSON with string keys, sorted as strings. So every dict whose keys all look like integers, and whose numeric and
    string orders differ, may have had either kind of key; all combinations are tried (up to 2^max_ambiguous).
    """
    stable = {k: v for k, v in results.items() if k not in runner.VOLATILE_KEYS}
    ambiguous = []

    def scan(o):
        if isinstance(o, dict):
            if len(o) > 1 and all(_int_like(k) for k in o) and sorted(o) != sorted(o, key=int):
                ambiguous.append(id(o))
            for v in o.values():
                scan(v)
        elif isinstance(o, list):
            for v in o:
                scan(v)

    scan(stable)
    if len(ambiguous) > max_ambiguous:
        choices = [set(), set(ambiguous)]
    else:
        choices = [{a for i, a in enumerate(ambiguous) if mask >> i & 1} for mask in range(1 << len(ambiguous))]

    def convert(o, as_int):
        if isinstance(o, dict):
            return {(int(k) if id(o) in as_int else k): convert(v, as_int) for k, v in o.items()}
        if isinstance(o, list):
            return [convert(v, as_int) for v in o]
        return o

    return any(sha256_obj(convert(stable, c)) == stored for c in choices)


_TIMING_KEY = re.compile(r"(_s|_ms|_sec|_secs|_seconds|seconds|runtime|elapsed|wall_time)$", re.I)


def _timing_like(results: dict) -> list[str]:
    """Paths of float fields whose names look like durations, outside the unhashed 'timings' entry."""
    found = set()

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if path == "" and k in runner.VOLATILE_KEYS:
                    continue
                if isinstance(v, float) and _TIMING_KEY.search(str(k)):
                    found.add(f"{path}/{k}")
                walk(v, f"{path}/{k}")
        elif isinstance(o, list):
            for v in o:
                walk(v, path + "[]")

    walk(results, "")
    return sorted(found)


def check_results(rep: Report) -> None:
    scripts = runner.discover()
    for e in db.all_records("experiment"):
        eid = e["id"]
        f = RESULTS / f"{eid}.json"
        data = read_json(f)
        if data is None:
            rep.error(f"{eid}: recorded but results/{eid}.json is missing")
            continue
        for where in _timing_like((data.get("results") or {})):
            rep.warn(f"results/{eid}.json: {where} looks like a wall-clock time inside the hashed results "
                     f"(put it under 'timings')")
        if not results_hash_matches(data.get("results") or {}, data.get("results_sha256")):
            rep.error(f"results/{eid}.json: stored hash does not match its results (file edited by hand?)")
        last = (e.get("runs") or [{}])[-1]
        if last.get("results_sha256") != data.get("results_sha256"):
            rep.error(f"{eid}: results file and last recorded run have different hashes")
        if data.get("error"):
            rep.warn(f"{eid}: the last recorded run failed")
        script = scripts.get(eid)
        if script is None:
            rep.warn(f"{eid}: recorded, but its script is gone")
        elif (data.get("code") or {}).get("sha256") != sha256_file(script):
            rep.warn(f"{eid}: script changed since the recorded run ({_rel(script)}); re-run or verify it")
    recorded = {e["id"] for e in db.all_records("experiment")}
    for eid in sorted(set(scripts) - recorded):
        rep.warn(f"{eid}: script never run with recording")


def check_journal(rep: Report) -> None:
    keys, versions = set(), {}
    for e in read_jsonl(JOURNAL_ENTRIES):
        key = e.get("key")
        if key in keys:
            rep.error(f"journal: duplicate key {key}")
        if e.get("kind") not in records.JOURNAL_KINDS:
            rep.error(f"journal: {key} has unknown kind {e.get('kind')!r}")
        keys.add(key)
        base, sep, _ = key.partition("#rev")
        text = e.get("text", "")
        if sep and text.startswith(f"[revision of {base}] "):
            text = text[len(f"[revision of {base}] "):]
        if sep and versions.get(base) == text:
            rep.error(f"journal: {key} repeats the previous version of {base} unchanged")
        versions[base] = text


def run_all() -> Report:
    rep = Report()
    claims = check_records(rep)
    check_database(rep, claims)
    check_results(rep)
    check_journal(rep)
    return rep
