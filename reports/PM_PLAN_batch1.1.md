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
| G1 | Novelty audit of the potentially novel claims of C11–C20 | Historian (agent) | `reviews/historian_C11_C20.md` with a verdict and the sources actually read for every claim; labels updated in the records | **done** — 4 relabelled REDISCOVERY (C17-05, and C11-04, C11-09, C14-07 partly), 20 novelty bases corrected, Klimov 2026 found for C16; new claim CLM-C17-08 |
| G2 | Lean formalisation of high-weight written proofs: uniqueness of the forced anchored table (CLM-C17-05), structure of affine spectra (CLM-C13-01 a–c, f), the arithmetic core of the deficit bound (CLM-C19-15); stretch: skew binary (CLM-C10-07) | Formal Verifier (agent) | new Lean files compile with standard axioms only; records name exactly what is formal | **done** — all four targets and the stretch, plus C13-01 (d), (e); C10-07 and C13-01 are now fully formal |
| G3 | Reproducibility audit of every experiment (`lab verify --dry`, cycle by cycle) | Director | every CHANGED or ERROR result explained and fixed or recorded | **done** — 113 of 113 re-run, 112 identical; EXP-C19-04 kept wall-clock times in its hashed results, fixed, re-recorded and re-verified ([REPRODUCIBILITY_batch1.1.md](REPRODUCIBILITY_batch1.1.md)) |
| G4 | Decide laws 677 and 1313 at orders 8 and 10 (SAT; UNSAT certified by DRUP + drat-trim) | Director | a recorded experiment; every answer certified or reported UNKNOWN | **done** — no models at 8 or 10 for either law; 284 of 284 case CNFs UNSAT with drat-trim-verified DRAT proofs (EXP-C05-08; Lemmas 7–9 and Theorem 10 of proofs/paper/C05.md); 677 at 8 is a rediscovery (Mace4, ETP paper) |
| G5 | Corrections log: a generated textbook appendix listing every change made after review, from the audit log | Director | `textbook/src/generated/` appendix, built into the PDF | **done** — `appendix_corrections.md` (116 field changes on 81 claims, 44 changed re-runs with their cause) |
| G6 | Infrastructure: `python -m lab check` (record validation, duplicate keys, proof links), tests for the report and catalogue code | Director | `pytest` covers the new code; `lab check` passes | **done** — `lab check` (records, anchors, database, result hashes, journal, timing fields) found 5 broken proof links and a sync bug that had duplicated 32 journal lines; 24 tests pass |

## Added during the sprint

- **G7 — independent review of the sprint's results** (Skeptic, agent): the row-period proof for CLM-C17-08,
  Lemmas 7–9 and the encoding of EXP-C05-08 with an independent re-computation, the two PROVEN claims that had no
  independent review (CLM-C05-10, CLM-C19-15), and the fidelity of the new Lean statements. **Done**
  ([skeptic_batch1.1.md](../reviews/skeptic_batch1.1.md)): nothing refuted, no gap; the row-period proof completed
  and machine-checked (CLM-C17-08 → PROVEN, `C17_RowPeriod.lean`); 677 and 1313 re-decided independently; two
  record corrections (CLM-C05-13 citation, CLM-C05-10 re-check wording). The review was interrupted once by a
  container restart and resumed from its transcript.

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

## Outcome (2026-10-20)

All seven items are done; the summary with numbers is the section "Batch 1.1" of
[`RESEARCH_REPORT_batch1.md`](RESEARCH_REPORT_batch1.md). Carried over to batch 2, in the order the
evidence suggests:

1. Laws 677 and 1313 at orders 12 and 14 (195 and 373 cases per law with the split of EXP-C05-08), and a
   certified search for finite models of 677 that violate 255 — the ETP's open finite implication.
2. A Lean proof of Laver's theorem (existence of the Laver tables), which would make CLM-C17-05 and
   CLM-C17-08 unconditional.
3. The remaining 60 PROVEN claims with written proofs only, starting with those the textbook builds on.
4. Rauzy-window computations for C08 and a proof of the Zeckendorf recursion (CLM-C19-05): research items.
5. For a human: the unread decisive sources (Capocelli 1989, Lakshmanan 1981, Kobayashi–Katsura–Shikishima-Tsuji
   2001), and the decisions whether to contact P. Klimov about CLM-C16-07 and to submit sequences to the OEIS.

