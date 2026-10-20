# Reproducibility audit — batch 1.1 (G3)

*2026-10-19/20. Every experiment recorded in batch 1 was re-run from its script with
`python -m lab verify --dry` (nothing recorded) and its result hash compared with the hash of
its last recorded run. Result hashes exclude only the `timings` entry (see `lab/runner.py`).*

## Result

**113 experiments re-run; 112 reproduced their result hash exactly; 1 changed (EXP-C19-04).**
No experiment raised an error. The one change was a defect of the experiment, not of the
mathematics; it is fixed, the experiment was re-recorded, and the fixed version reproduces.

| cycle | experiments | identical | changed | wall time (s) |
|---|---|---|---|---|
| C01 | 8 | 8 | — | 46 |
| C02 | 7 | 7 | — | 67 |
| C03 | 4 | 4 | — | 71 |
| C04 | 10 | 10 | — | 252 |
| C05 | 7 | 7 | — | 3350 |
| C06 | 4 | 4 | — | 355 |
| C07 | 3 | 3 | — | 436 |
| C08 | 7 | 7 | — | 368 |
| C09 | 4 | 4 | — | 14 |
| C10 | 4 | 4 | — | 39 |
| C11 | 9 | 9 | — | 34 |
| C12 | 6 | 6 | — | 86 |
| C13 | 9 | 9 | — | 551 |
| C14 | 7 | 7 | — | 286 |
| C15 | 5 | 5 | — | 116 |
| C16 | 5 | 5 | — | 266 |
| C17 | 3 | 3 | — | 1791 |
| C18 | 5 | 5 | — | 26 |
| C19 | 5 | 4 | EXP-C19-04 | 1165 |
| C20 | 1 | 1 | — | 1 |
| **total** | **113** | **112** | **1** | **≈ 2.5 h** |

Wall times are on a shared 4-core container, under `nice`, while other jobs ran; they are
indicative only. The run was split in two (C01–C19 and the start of C17 in part 1; C17 and C05
in part 2) because background jobs of the agent harness are stopped after two hours; C17 was
re-run in full in part 2.

## The change: EXP-C19-04

EXP-C19-04 (out-of-sample tests of the Zeckendorf-game recursion) stored the wall-clock times of
its benchmark (`greedy_s`, `recursion_s`) and a "speed" line with those times inside the hashed
results, so no re-run could ever reproduce its hash. The mathematical results were identical
(0 mismatches on 6,272 n, the same OEIS answers, the same asymptotic ratios). Fix: the times
moved under `timings`; the summary no longer quotes them. The experiment was re-recorded and a
second dry run reproduced the new hash. `python -m lab check` now warns about any float field
whose name looks like a duration (`*_s`, `*_seconds`, `runtime`, `elapsed`, …) outside
`timings`; a scan of all 114 result files found no other case.

## Other findings of the audit

- **Hash checks of the stored files.** `lab check` recomputes every result file's hash. The
  runner hashes the Python objects, and 13 experiments return dictionaries with integer keys,
  which JSON turns into strings and sorts differently; `lab check` therefore tries the key
  types that are ambiguous (`check.results_hash_matches`). With that, all 114 stored hashes are
  re-derived from the files.
- **The one historical non-code change.** The audit log records 44 re-runs in batch 1 whose
  results changed; 43 followed a change of the script or of `systems/` (listed with their cause
  in the textbook's Corrections log). The exception, EXP-C02-06 on 2026-10-18, depended on an
  external OEIS lookup; OEIS answers have been served from `cache/oeis/` since.
- **New in batch 1.1.** EXP-C05-08 (laws 677 and 1313 at orders 8 and 10) was recorded for the
  first time in this sprint and is not part of the audit; its 401 UNSAT answers are each backed
  by a DRAT proof that drat-trim verified during the run.

## Environment

Python 3.13.16, PySAT 1.9.dev16 (CaDiCaL 1.5.3, Glucose 4), the versions in
`requirements-lock.txt`; drat-trim built from source for EXP-C05-06 (see `CONTINUATION.md`).
Command used: `python -m lab verify --cycle Cnn --dry` per cycle, and
`python -m lab verify EXP-C05-01 … EXP-C05-07 --dry` for C05. The log is not kept in the
repository; this report and the audit log (`db/audit_log.jsonl`) are the record.
