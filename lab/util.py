"""Small shared helpers: timestamps, canonical JSON, hashing, environment."""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import platform
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from .paths import ROOT


def now_iso() -> str:
    """Current UTC time, second precision, ISO-8601 with a trailing Z."""
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _default(o):
    if isinstance(o, (set, frozenset)):
        return sorted(o, key=repr)
    if isinstance(o, tuple):
        return list(o)
    if isinstance(o, Fraction):
        return f"{o.numerator}/{o.denominator}"
    if isinstance(o, Path):
        return o.as_posix()
    # numpy scalars / arrays without importing numpy eagerly
    if hasattr(o, "tolist"):
        return o.tolist()
    if hasattr(o, "item"):
        return o.item()
    raise TypeError(f"not JSON serialisable: {type(o).__name__}")


def to_json(obj, indent=2) -> str:
    return json.dumps(obj, indent=indent, sort_keys=True, ensure_ascii=False, default=_default)


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=_default)


def sha256_obj(obj) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_files(paths) -> str:
    h = hashlib.sha256()
    for p in sorted(Path(x) for x in paths):
        h.update(p.relative_to(ROOT).as_posix().encode())
        h.update(b"\0")
        h.update(p.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def read_json(path, default=None):
    p = Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))


def write_json(path, obj) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(to_json(obj) + "\n", encoding="utf-8")
    tmp.replace(p)


def append_jsonl(path, obj) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(canonical_json(obj) + "\n")


def read_jsonl(path) -> list:
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def git_head() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or None
    except Exception:
        return None


def env_info() -> dict:
    info = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_head": git_head(),
    }
    try:                                     # the external proof checker of the C05 case splits, if present
        from systems.magma_split import _sha256_file, drat_path
        checker = drat_path()
        info["drat_trim_sha256"] = _sha256_file(checker) if checker else None
    except Exception:
        info["drat_trim_sha256"] = None
    for mod in ("numpy", "sympy", "scipy", "networkx", "pysat", "z3"):
        try:
            m = __import__(mod)
            info[mod] = getattr(m, "__version__", None) or getattr(m, "get_version_string", lambda: "?")()
        except Exception:
            info[mod] = None
    return info
