# Batch 1.1 — hardening sprint (project plan)

*Owner: the Director (acting as project manager). Started 2026-10-19 after
the batch-1 report. Status is updated as work lands; the final state is
summarised in `reports/RESEARCH_REPORT_batch1.md` (section "Batch 1.1").*

## Why this sprint

The batch-1 report names its own weaknesses:

1. 26 "potentially novel" claims of C11–C20 were never audited by the
   Historian, and one of them (CLM-C14-06) was already found to be published.
2. 64 PROVEN claims rest on written proofs alone.
3. The shared modules of `systems/` changed during the review integration, and
   no full reproducibility check has been run since.
4. The open problems left over from the refuted conjecture CLM-C05-09 are
   cheap to attack by computation.
5. Corrections are scattered over records, READMEs and chapters, with no
   single place to read them.

The sprint attacks these in order of value per unit of effort, before any new
research cycle starts.

## Backlog

| id | goal | owner | acceptance criterion | status |
|---|---|---|---|---|
| G1 | Novelty audit of the potentially novel claims of C11–C20 | Historian (agent) | `reviews/historian_C11_C20.md` with a verdict and the sources actually read for every claim; labels updated in the records | in progress |
| G2 | Lean formalisation of high-weight written proofs: uniqueness of the forced anchored table (CLM-C17-05), structure of affine spectra (CLM-C13-01 a–c, f), the arithmetic core of the deficit bound (CLM-C19-15); stretch: skew binary (CLM-C10-07) | Formal Verifier (agent) | new Lean files compile with standard axioms only; records name exactly what is formal | in progress |
| G3 | Reproducibility audit of every experiment (`lab verify --dry`, cycle by cycle) | Director | every CHANGED or ERROR result explained and fixed or recorded | in progress |
| G4 | Decide laws 677 and 1313 at orders 8 and 10 (SAT; UNSAT certified by DRUP + drat-trim) | Director | a recorded experiment; every answer certified or reported UNKNOWN | in progress |
| G5 | Corrections log: a generated textbook appendix listing every change made after review, from the audit log | Director | `textbook/src/generated/` appendix, built into the PDF | planned |
| G6 | Infrastructure: `python -m lab check` (record validation, duplicate keys, proof links), tests for the report and catalogue code | Director | `pytest` covers the new code; `lab check` passes | planned |

## Not in this sprint (and why)

- **Rauzy-window computations for C08** — research-level; needs its own
  cycle.
- **A proof of the Zeckendorf recursion (CLM-C19-05)** — open-ended; a
  candidate for batch 2 now that a provable reference method exists.
- **New research cycles** — wait until the batch-1 claims are hardened.

## Risks

- Session rate limits have interrupted agents twice. Mitigation: at most two
  agents at a time, commits after every landed item, and agents resumable from
  their transcripts.
- CPU: 4 cores are shared by the reproducibility run, the SAT work and the
  agents' checks. Mitigation: `nice`, one heavy job per agent.
