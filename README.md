# Project Infinity — an autonomous mathematical research laboratory

This repository is a working research lab: it invents mathematical systems,
runs falsifiable experiments on them, proves (or refutes) what it can — in Lean 4
where feasible — checks novelty against the literature, and writes up the
verified results as a living textbook:

> **Beyond Conventional Mathematics: An Experimental Journey into AI-Discovered Mathematical Systems**

Everything is reproducible and append-only: experiments are deterministic
scripts with hashed results, every change to a claim's status is kept in an
audit log, and refuted hypotheses are preserved alongside proven theorems.

## At a glance (cycles C01–C20, after batches 1.1 and 1.2)

| | |
|---|---|
| research cycles | 20, over five foundational systems (A–E) |
| experiments | 121 deterministic scripts, 214 recorded runs; all 113 batch-1 experiments re-run in batch 1.1, 112 identical (the 113th fixed) |
| claims | 241 — 147 PROVEN, 37 COMPUTATIONALLY SUPPORTED, 5 CONJECTURE, 50 REFUTED, 2 INCONCLUSIVE |
| novelty | 115 REDISCOVERY, 55 POTENTIALLY NOVEL (not a priority claim), 71 not assessed |
| formal proofs | 364 Lean 4 + Mathlib theorems in 23 files, standard axioms only |
| independent review | Skeptic verdicts on 224 of 230 claims; every PROVEN claim that is not fully formal (121) independently reviewed; 2 of the lab's own claims refuted, 1 withdrawn |
| textbook | *Beyond Conventional Mathematics*, version 1.2: 21 chapters in 10 volumes and a generated corrections log (`textbook/build/book.pdf`) |

**Batch 1.1** (a hardening sprint run by the Director as project manager; plan and outcome in
[`reports/PM_PLAN_batch1.1.md`](reports/PM_PLAN_batch1.1.md)) decided the two open orders of ETP laws
677 and 1313 — no models of order 8 or 10, every case certified by drat-trim — formalised four batch-1
proofs in Lean, completed and machine-checked a proof that the anchored left-distributive instance has a model only at
powers of 2 (CLM-C17-08, a rediscovery), audited the novelty of C11–C20 (four relabelled rediscoveries), re-ran
every experiment ([`reports/REPRODUCIBILITY_batch1.1.md`](reports/REPRODUCIBILITY_batch1.1.md)), and added
`python -m lab check`, which found and fixed five broken proof links and a journal-duplication bug.

**Batch 1.2** ("find more"; plan and outcome in [`reports/PM_PLAN_batch1.2.md`](reports/PM_PLAN_batch1.2.md))
went back to the open spectra of the Equational Theories Project. It determined the complete spectrum of ETP law
501, x = y(y(x(xy))): exactly the orders n ≡ 0, 1 (mod 4) (CLM-C05-22; the necessity proved in Lean). It
certified 26 gaps that no source we found states, at orders 8–13 for twelve laws. It completed the spectra up to
order 10 of the 13 laws x = y∗T, and up to 13 for eight of them. It showed that law 677 has no quasigroup model
of order 12, reducing that open order to 51 explicit CNFs. It refuted one of its own conjectures the day it was
made (law 474). The Skeptic upheld every claim (`reviews/skeptic_batch1.2.md`).

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
