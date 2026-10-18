"""Check Lean 4 proof files and record the outcome.

The Lean sources live in the Lake project ``proofs/lean`` (Mathlib dependency,
toolchain pinned in ``proofs/lean/lean-toolchain``).  A file counts as
*verified* only if

* ``lake env lean <file>`` exits with status 0,
* the output contains no ``sorry`` warning, and
* every ``#print axioms`` report lists only the standard axioms
  (``propext``, ``Classical.choice``, ``Quot.sound``).  Use of
  ``Lean.ofReduceBool`` (``native_decide``) is allowed but flagged, since it
  trusts the compiler in addition to the kernel.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
from pathlib import Path

from .paths import LEAN_PROJECT, LEAN_RESULTS, rel
from .util import now_iso, read_json, sha256_file, write_json

STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def _lake() -> str | None:
    cand = shutil.which("lake") or str(Path.home() / ".elan" / "bin" / "lake")
    return cand if Path(cand).exists() else None


def lean_files() -> list[Path]:
    src = LEAN_PROJECT / "Infinity"
    return sorted(src.rglob("*.lean")) if src.exists() else []


def _axioms(output: str) -> tuple[set[str], list[str]]:
    used: set[str] = set()
    for m in re.finditer(r"depends on axioms: \[([^\]]*)\]", output):
        used |= {a.strip() for a in m.group(1).split(",") if a.strip()}
    nonstd = sorted(a for a in used if a not in STANDARD_AXIOMS and a != "Lean.ofReduceBool")
    return used, nonstd


def check_file(path: Path, timeout: int = 1800) -> dict:
    lake = _lake()
    if lake is None:
        return {"ok": False, "error": "lake not found (install elan; see CONTINUATION.md)"}
    env = dict(os.environ)
    env["PATH"] = str(Path(lake).parent) + os.pathsep + env.get("PATH", "")
    t0 = time.perf_counter()
    try:
        proc = subprocess.run([lake, "env", "lean", str(path.resolve())], cwd=LEAN_PROJECT, capture_output=True,
                              text=True, timeout=timeout, env=env)
        out = (proc.stdout or "") + (proc.stderr or "")
        code = proc.returncode
    except subprocess.TimeoutExpired:
        out, code = "TIMEOUT", -1
    dt = time.perf_counter() - t0
    has_sorry = "declaration uses 'sorry'" in out or "sorryAx" in out
    used, nonstd = _axioms(out)
    ok = code == 0 and not has_sorry and not nonstd and "error" not in out.lower().split("warning")[0][:0]
    # a non-zero exit code already signals errors; keep the check explicit:
    ok = code == 0 and not has_sorry and not nonstd
    theorems = re.findall(r"^(?:theorem|lemma)\s+([^\s:({\[]+)", path.read_text(encoding="utf-8"), flags=re.M)
    return {
        "ok": ok,
        "exit_code": code,
        "seconds": round(dt, 2),
        "sha256": sha256_file(path),
        "sorry": has_sorry,
        "axioms_used": sorted(used),
        "nonstandard_axioms": nonstd,
        "native_decide": "Lean.ofReduceBool" in used,
        "theorems": theorems,
        "output_tail": out[-4000:],
        "checked": now_iso(),
    }


def check_all(only: list[str] | None = None, force: bool = False) -> dict:
    data = read_json(LEAN_RESULTS, {}) or {}
    files = data.get("files", {})
    toolchain = (LEAN_PROJECT / "lean-toolchain").read_text().strip() if (LEAN_PROJECT / "lean-toolchain").exists() else None
    for p in lean_files():
        key = rel(p)
        if only and not any(o in key for o in only):
            continue
        prev = files.get(key)
        if prev and not force and prev.get("sha256") == sha256_file(p) and prev.get("ok"):
            print(f"[lean] {key}: unchanged, previously verified")
            continue
        res = check_file(p)
        files[key] = res
        flag = "VERIFIED" if res["ok"] else "FAILED"
        extra = " (uses native_decide)" if res.get("native_decide") else ""
        print(f"[lean] {key}: {flag}{extra} in {res.get('seconds')}s; theorems: {', '.join(res.get('theorems', []))}")
        if not res["ok"]:
            print(res.get("output_tail", "")[-2500:])
    for key in list(files):
        if not (LEAN_PROJECT.parent.parent / key).exists():
            files[key]["missing"] = True
    data = {"toolchain": toolchain, "updated": now_iso(), "files": files}
    write_json(LEAN_RESULTS, data)
    return data
