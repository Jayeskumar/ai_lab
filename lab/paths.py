"""Canonical filesystem locations used by the lab."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DB = ROOT / "db"
EXP_DB = DB / "experiments"
CLAIM_DB = DB / "claims"
AUDIT_LOG = DB / "audit_log.jsonl"

EXPERIMENTS = ROOT / "experiments"
RESULTS = ROOT / "results"
SYSTEMS = ROOT / "systems"

RESEARCH = ROOT / "research"
CYCLES = RESEARCH / "cycles"

JOURNAL_DIR = ROOT / "journal"
JOURNAL_ENTRIES = JOURNAL_DIR / "entries.jsonl"
JOURNAL_MD = JOURNAL_DIR / "JOURNAL.md"

PROOFS = ROOT / "proofs"
LEAN_PROJECT = PROOFS / "lean"
LEAN_RESULTS = PROOFS / "lean_results.json"
PAPER_PROOFS = PROOFS / "paper"

TEXTBOOK = ROOT / "textbook"
BENCHMARKS = ROOT / "benchmarks"
REPORTS = ROOT / "reports"
CHECKPOINTS = ROOT / "checkpoints"
CACHE = ROOT / "cache"
OEIS_CACHE = CACHE / "oeis"

DISCOVERY_INDEX = ROOT / "DISCOVERY_INDEX.md"
DATABASE_MD = DB / "DATABASE.md"


def rel(path) -> str:
    """Path relative to the repository root, as a POSIX string."""
    return Path(path).resolve().relative_to(ROOT).as_posix()
