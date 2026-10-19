# Project Infinity — an autonomous mathematical research laboratory

This repository is a working research lab: it invents mathematical systems,
runs falsifiable experiments on them, proves (or refutes) what it can — in Lean 4
where feasible — checks novelty against the literature, and writes up the
verified results as a living textbook:

> **Beyond Conventional Mathematics: An Experimental Journey into AI-Discovered Mathematical Systems**

Everything is reproducible and append-only: experiments are deterministic
scripts with hashed results, every change to a claim's status is kept in an
audit log, and refuted hypotheses are preserved alongside proven theorems.

## Batch 1 at a glance (cycles C01–C20)

| | |
|---|---|
| research cycles | 20, over five foundational systems (A–E) |
| experiments | 113 deterministic scripts, 203 recorded runs |
| claims | 225 — 131 PROVEN, 39 COMPUTATIONALLY SUPPORTED, 4 CONJECTURE, 49 REFUTED, 2 INCONCLUSIVE |
| novelty | 103 REDISCOVERY, 52 POTENTIALLY NOVEL (not a priority claim), 70 not assessed |
| formal proofs | 194 Lean 4 + Mathlib theorems in 15 files, standard axioms only |
| independent review | Skeptic verdicts on 217 of 225 claims; 2 of the lab's own claims refuted, 1 withdrawn, 1 novelty downgraded, 3 code bugs fixed |
| textbook | *Beyond Conventional Mathematics*, version 1: 21 chapters in 10 volumes (`textbook/build/book.pdf`) |

The full report, with the ten required items and an honest list of
limitations, is [`reports/RESEARCH_REPORT_batch1.md`](reports/RESEARCH_REPORT_batch1.md).

## Where to look

| What | Where |
|---|---|
| Research report (batch 1 summary) | [`reports/RESEARCH_REPORT_batch1.md`](reports/RESEARCH_REPORT_batch1.md); tables in [`reports/REPORT_DATA.md`](reports/REPORT_DATA.md) |
| Discovery index (theorems, conjectures, refutations, rediscoveries, novelty) | [`DISCOVERY_INDEX.md`](DISCOVERY_INDEX.md) |
| Research journal (chronological, append-only) | [`journal/JOURNAL.md`](journal/JOURNAL.md) |
| Full discovery database (human-readable) | [`db/DATABASE.md`](db/DATABASE.md); JSON records in `db/claims/`, `db/experiments/` |
| Research cycles (10-step reports) | [`research/cycles/INDEX.md`](research/cycles/INDEX.md) |
| Foundational systems A–E (axioms, objects, operations) | [`research/systems/SYSTEMS.md`](research/systems/SYSTEMS.md) |
| Lean 4 + Mathlib proofs | `proofs/lean/Infinity/` (status in `proofs/lean_results.json`) |
| Written proofs | `proofs/paper/` |
| Independent reviews (Skeptic, Historian) | `reviews/` |
| Textbook source / build (HTML, PDF) | `textbook/src/`, `textbook/build/` |
| How to resume the research | [`CONTINUATION.md`](CONTINUATION.md) |

## Verification vocabulary

Every claim carries two independent labels.

* **Verification:** PROVEN (Lean-checked, computer-assisted with a stated trust
  base, or a written proof — the `proof_check` field says which),
  COMPUTATIONALLY SUPPORTED, CONJECTURE, REFUTED (with counterexample),
  INCONCLUSIVE.
* **Novelty:** REDISCOVERY (with references), POTENTIALLY NOVEL (nothing
  equivalent found in the sources searched — never a priority claim),
  NOT ASSESSED.

## Running the lab

```bash
pip install -r requirements.txt          # exact versions: requirements-lock.txt
python -m lab status                     # counts of claims, experiments, journal entries
python -m lab run EXP-C08-03             # re-run one experiment (results/ + db/ + audit log)
python -m lab run --cycle C01            # re-run a whole cycle
python -m lab run --dry EXP-C08-03       # re-run without recording anything
python -m lab verify --cycle C08         # re-run a cycle and compare result hashes (--dry: do not record)
python -m lab check                      # consistency checks (records, links, database, result hashes); must report 0 errors
python -m lab lean                       # check all Lean files (needs elan + Mathlib cache)
python -m lab sync                       # import cycle records, render index/journal/database
python -m lab catalogue                  # regenerate the catalogue volumes and the corrections log of the textbook
python -m lab report                     # batch statistics + report tables (reports/)
python -m lab book                       # build textbook HTML + PDF (--no-pdf: HTML only)
python -m pytest -q tests/               # infrastructure tests
```

Lean setup: install elan, then `cd proofs/lean && lake exe cache get`
(toolchain pinned in `proofs/lean/lean-toolchain`, Mathlib pinned in
`lake-manifest.json`).

## Layout

```
lab/          infrastructure: registry (db.py), runner, records sync, renderers,
              Lean checker, OEIS cache, property profiler, sequence tools, book builder
systems/      implementations of the mathematical systems (rewriting, exchange,
              circle products, magmas, ...)
experiments/  one script per experiment (EXP-Cnn-mm), deterministic
results/      raw results with environment, code hashes and result hashes
research/     systems definitions and per-cycle reports + machine-readable records
proofs/       Lean project and written proofs
db/, journal/ append-only database, audit log and journal
cache/oeis/   cached OEIS answers used in novelty checks
textbook/     the living textbook
```
