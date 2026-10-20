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
| B1 | Decide the 15 open pairs (law, n <= 10) with the general case split, with 13 controls of known answer | Director | EXP-C05-09 recorded; every verdict certified or UNKNOWN; all controls agree | running — 14 of 15 decided (all: no model), 13 of 13 controls agree; 670 at order 10 running |
| B2 | Latest state of the literature on these spectra | Historian (agent) | `reviews/historian_spectra_2026.md`; labels updated | **done** — nothing newer than Le Floch's July 2025 notes except for 677 (ETP Zulip): 677 at order 10 was known (Brox, Jan 2025), so CLM-C05-12 is a rediscovery; no source decides any B1/B3 target; 677 at 12 and 14 is open everywhere |
| B3 | Next orders (11-13) of the quasigroup laws 1076, 1110, 1279, 1286, 1313 | Director | EXP-C05-10 recorded | running — 1076, 1110, 1279, 1313 have no model of order 12 |
| B4 | Law 677 at order 12 (open in every source; premise of the ETP's last open finite implication) | Director | a certified answer, or the open problem reduced to an explicit list of hard cases | probing — some cases need > 3 million conflicts; next: a cheap triage of all 195 cases, then a finer split of the hard ones |
| B5 | Record, review (Skeptic spot check), write up | Director, Skeptic | claims, chapter 6, report and README updated | planned |

## Decisions

- Law 1313 at order 14 was dropped from EXP-C05-10 after its first case exceeded the 4-million-conflict budget
  (373 cases would take days at that rate); it needs the same finer split as 677 at order 12.
- Laws 1516 and 1719 have another shape (x = (yy)·T); 1516 at order 10 (a caveated "no" on the ETP Zulip, 2024)
  needs a different case split and is not in this batch.
- A pattern in the data — every law x = y·T here without a model of order 2 has none of orders 6 and 10 either —
  is recorded as a conjecture (no model of order ≡ 2 mod 4), not as a result. It is false for laws of other
  shapes: 1719 has no model of order 2 but one of order 6.
