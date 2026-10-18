"""Experiment runner.

An experiment is a Python file under ``experiments/`` that defines

    META = {"id": "EXP-C01-01", "cycle": "C01", "title": ..., "agent": ...,
            "question": ..., "hypothesis": ..., "assumptions": [...],
            "methodology": ..., "falsification": ...}      # a literal dict

    def run() -> dict: ...

``run()`` must be deterministic (seed every random generator).  Anything that
is legitimately non-deterministic (wall-clock timings) must be returned under
the key ``"timings"``; it is stored but excluded from the reproducibility hash.
A ``"summary"`` key (list of short strings) is copied to the database record.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
import time
import traceback
from pathlib import Path

from . import db
from .paths import EXPERIMENTS, RESULTS, ROOT, SYSTEMS, rel
from .util import env_info, now_iso, sha256_file, sha256_files, sha256_obj, write_json, read_json

VOLATILE_KEYS = ("timings",)


def _literal_meta(path: Path) -> dict | None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "META" for t in node.targets):
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                return None
    return None


def discover() -> dict[str, Path]:
    """Map experiment id -> script path."""
    found: dict[str, Path] = {}
    for p in sorted(EXPERIMENTS.rglob("*.py")):
        if p.name.startswith("_"):
            continue
        meta = _literal_meta(p)
        if meta and str(meta.get("id", "")).startswith("EXP-"):
            if meta["id"] in found:
                raise RuntimeError(f"duplicate experiment id {meta['id']}: {found[meta['id']]} and {p}")
            found[meta["id"]] = p
    return found


def _import(path: Path):
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    name = "exp_" + path.stem + "_" + str(abs(hash(path)))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def artifact_path(exp_id: str, name: str) -> Path:
    return RESULTS / "artifacts" / exp_id / name


def save_artifact(exp_id: str, name: str, obj) -> dict:
    """Store a large JSON artifact next to the results; return a reference."""
    p = artifact_path(exp_id, name if name.endswith(".json") else name + ".json")
    write_json(p, obj)
    return {"file": rel(p), "sha256": sha256_file(p)}


def run(exp_id: str, record: bool = True, quiet: bool = False) -> dict:
    scripts = discover()
    if exp_id not in scripts:
        raise KeyError(f"unknown experiment {exp_id}; known: {', '.join(sorted(scripts))}")
    path = scripts[exp_id]
    mod = _import(path)
    meta = dict(mod.META)
    started = now_iso()
    t0 = time.perf_counter()
    try:
        results = mod.run()
        error = None
    except Exception:  # record failures too -- failed runs are data
        results = {}
        error = traceback.format_exc()
    runtime = time.perf_counter() - t0
    finished = now_iso()
    stable = {k: v for k, v in results.items() if k not in VOLATILE_KEYS}
    res_hash = sha256_obj(stable)
    systems_files = [p for p in SYSTEMS.rglob("*.py")]
    code = {
        "file": rel(path),
        "sha256": sha256_file(path),
        "systems_sha256": sha256_files(systems_files) if systems_files else None,
        "command": f"python -m lab run {exp_id}",
    }
    out_path = RESULTS / f"{exp_id}.json"
    previous = read_json(out_path)
    reproduced = None
    if previous is not None and previous.get("error") is None and error is None:
        reproduced = previous.get("results_sha256") == res_hash
    payload = {
        "id": exp_id,
        "meta": meta,
        "started": started,
        "finished": finished,
        "runtime_s": round(runtime, 3),
        "code": code,
        "env": env_info(),
        "error": error,
        "results": results,
        "results_sha256": res_hash,
    }
    if record:
        write_json(out_path, payload)
        db.append_run(exp_id, {
            "started": started, "finished": finished, "runtime_s": round(runtime, 3),
            "code": code, "results_file": rel(out_path), "results_sha256": res_hash,
            "summary": results.get("summary"), "error": error is not None,
            "reproduced": reproduced,
        }, meta)
    if not quiet:
        status = "ERROR" if error else "ok"
        rep = "" if reproduced is None else (" (reproduced previous hash)" if reproduced else " (RESULT HASH CHANGED)")
        print(f"[{exp_id}] {status} in {runtime:.2f}s{rep}")
        for line in results.get("summary", []) or []:
            print("   ", line)
        if error:
            print(error)
    payload["reproduced"] = reproduced
    return payload
