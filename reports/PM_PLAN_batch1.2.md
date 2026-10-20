# Batch 1.2 — "find more": certified spectra of the open ETP laws (project plan)

*Owner: the Director (project manager). Started and finished 2026-10-20 at the user's request "find more".*

## Outcome

- **Law 501 solved:** its spectrum is exactly the orders n ≡ 0, 1 (mod 4) (CLM-C05-22) — written proof, Lean
  proof of the necessity, construction checked to 100, not found in any source.
- **26 new certified gaps** (orders 8-13) for twelve laws, and complete spectra: up to 10 for the 13 laws x = y∗T,
  up to 13 for 467, 704 and the six laws x = y∗(S∗y).
- **Law 677 at order 12:** no quasigroup model; the open question is reduced to 51 explicit CNFs about
  non-quasigroups.
- **Lean:** quasigroup forcing for x = y∗(S∗y), 704 and 883; the 501 parity theorem; certificates for the law-474
  counterexample and the order-12 model of 501.
- **One self-refuted conjecture** (CLM-C05-18, law 474), kept with its refutation; a restricted conjecture
  (CLM-C05-21) remains.
- **Review:** the Skeptic upheld every claim (two with corrections to their evidence) and found no encoding bug;
  the Historian corrected the lab's statement about the smallest non-right-cancellative model of 677 (25, not 55).

## Why this direction

Batch 1.1 showed that a complete case split (proofs/paper/C05.md, Lemma 8) with implied division clauses and
DRAT certificates decides orders that plain SAT could not. The method applies to every law of the form
x = y * T, which covers 13 of the 15 open ETP laws of cycle C05; EXP-C05-03 had left 15 of their orders n <= 10
undecided. The Historian checked first which of these orders anyone has settled.

## Backlog

| id | goal | owner | acceptance criterion | status |
|---|---|---|---|---|
| B1 | Decide the 15 open pairs (law, n <= 10) with the general case split, with 13 controls of known answer | Director | EXP-C05-09 recorded; every verdict certified or UNKNOWN; all controls agree | **done** — EXP-C05-09: all 15 pairs have no model (1,239 case CNFs, every proof verified); 13 of 13 controls agree; with EXP-C05-12 (every order n <= 7 re-certified) the spectra up to 10 of all 13 laws are complete (CLM-C05-15, -17) |
| B2 | Latest state of the literature on these spectra | Historian (agent) | `reviews/historian_spectra_2026.md`; labels updated | **done** — nothing newer than Le Floch's July 2025 notes except for 677 (ETP Zulip): 677 at order 10 was known (Brox, Jan 2025), so CLM-C05-12 is a rediscovery; no source decides any B1/B3 target; 677 at 12 and 14 is open everywhere |
| B3 | Next orders (11-13) of the quasigroup laws 1076, 1110, 1279, 1286, 1313 | Director | EXP-C05-10 recorded | **done** — EXP-C05-10: all 9 open pairs have no model (1,797 case CNFs, every proof verified); 2 of 2 decision controls and 21 of 21 known-model checks agree; spectra of the six laws x = y(Sy) complete up to 13 (CLM-C05-16) |
| B4 | Law 677 at order 12 (open in every source; premise of the ETP's last open finite implication) | Director | a certified answer, or the open problem reduced to an explicit list of hard cases | **done (reduction, not a decision)** — EXP-C05-11: 138 of 195 cases refuted (CLM-C05-20); EXP-C05-13: all 57 quasigroup parts and 6 non-quasigroup parts refuted, so 677 has no quasigroup model of order 12 and the question is reduced to 51 non-quasigroup CNFs (CLM-C05-24); a missing-value split and implied 'star' clauses did not decide the hardest one |
| B7 | The open orders 11-13 of the laws not forced to be quasigroups (467, 501, 670, 704, 883, 907) | Director | probes for all eight pairs; EXP-C05-14 for the decidable ones | **done** — 467 and 704 have no model of order 12 (EXP-C05-14, CLM-C05-25); 501/11 and 501/12 settled by B8; 670/12, 670/13, 883/12, 907/12 handed on (hard cases in the probes) |
| B8 | Law 501 (found during B7): the complete spectrum | Director, Formal Verifier (agent), Historian (agent) | proof, Lean, computation, novelty check | **done** — spectrum exactly n ≡ 0, 1 (mod 4) (CLM-C05-22): written proof, Lean necessity `law501_card_mod_four`, EXP-C05-15; POTENTIALLY NOVEL (Historian: not found anywhere; the sign identity is a case of the Janssen–Zappa parity relation) |
| B5 | Record, review (Skeptic spot check), write up | Director, Skeptic | claims, chapter 6, report and README updated | **done** — claims CLM-C05-15 to -25 recorded; proofs/paper/C05.md Lemmas 7′, 7″, 9′, Theorems 11, 12, 14-16, Proposition 13; Skeptic review `reviews/skeptic_batch1.2.md` (every claim upheld, 11 problems fixed); Historian checks `reviews/historian_677_nonqg.md`, `reviews/historian_501.md`; textbook chapter 6, report and README updated |

## Decisions

- Law 1313 at order 14 was dropped from EXP-C05-10 after its first case exceeded the 4-million-conflict budget
  (373 cases would take days at that rate); it needs the same finer split as 677 at order 12.
- Laws 1516 and 1719 have another shape (x = (yy)·T); 1516 at order 10 (a caveated "no" on the ETP Zulip, 2024)
  needs a different case split and is not in this batch.
- A pattern in the data — every law x = y·T here without a model of order 2 has none of orders 6 and 10 either —
  was first recorded as a general conjecture (no model of order ≡ 2 mod 4 for any law x = y·T without a model of
  order 2, CLM-C05-18). Checked against the lab's own census the same day, it is false: law 474,
  x = y(x(y(xy))), has a model of order 6. It is kept as REFUTED, and only the restricted form for the 12 open
  laws remains a conjecture (CLM-C05-21).
- The decision control 1083 at order 12 of EXP-C05-10 was replaced after a partial run: the known model (a direct
  product) lies in case 189 of 195 and the earlier cases need up to 1.6 million conflicts each, about a day in all.
  It was replaced by a direct check that every known model at orders 11-13 satisfies the CNF of its case
  (`systems.magma_split.admits`) and by two cheap decision controls (1110 and 1279 at order 11). The targets'
  results were unaffected (hash-identical CNFs, read back from checkpoints).
- Law 677 at order 12: since all 57 hard cases are easy for quasigroups, the open question is whether a model of
  order 12 that is *not* a quasigroup exists. The Historian was asked for structural results on such models
  (the smallest known has order 25, M. Reinke, Nov 2025 — not 55 as our notes said; corrected in CLM-C05-14).
- The probes of B7 found a model of 501 of order 12, which no product of known orders gives. Analysing it, rather
  than adding 501 to a long search, gave the complete spectrum (B8) in under an hour, including a Lean proof of
  the hard half.
- 670/12, 670/13, 883/12 and 907/12 are left as hand-offs: in the probes several sampled case CNFs were undecided
  at 300,000 conflicts (883 also at 1,000,000 with Latin columns, which Lemma 7″ allows).
