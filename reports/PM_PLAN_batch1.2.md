# Batch 1.2 — "find more": certified spectra of the open ETP laws (project plan)

*Owner: the Director (project manager). Started 2026-10-20 at the user's request "find more". Status is
updated as work lands.*

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
| B4 | Law 677 at order 12 (open in every source; premise of the ETP's last open finite implication) | Director | a certified answer, or the open problem reduced to an explicit list of hard cases | running — EXP-C05-11 (recorded): 138 of 195 cases refuted, 57 hard (CLM-C05-20); a probe refutes all 57 when the table is also a Latin square, so EXP-C05-13 splits each hard case into its quasigroup and non-quasigroup parts; the non-quasigroup parts are the hard ones |
| B5 | Record, review (Skeptic spot check), write up | Director, Skeptic | claims, chapter 6, report and README updated | running — claims CLM-C05-15 to -20 recorded, proofs/paper/C05.md Theorems 11, 12, Proposition 13 written |

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
  (the smallest known has order 55).
