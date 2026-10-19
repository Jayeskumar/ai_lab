# Cycle C20 — Open problems revisited

**Branch:** A (transformation systems) · **Status:** complete
**Experiments:** EXP-C20-01 · **Claims:** CLM-C20-01 … CLM-C20-04
**Proofs:** `proofs/paper/C20.md` (Theorems 1–2, Corollary 3)

## Step 1 — Hypotheses

The last cycle of the batch attacks problems that earlier cycles left open.

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C20-1 | The 8 one-rule systems left undecided by C04 (classes aab → ababa, aab → babaa) terminate. | Inventor | **proved** (termination itself is a rediscovery: barren rules) |
| H-C20-2 | Their derivational complexities are 2^(n−2) − 1 and max_b b·(2^⌊(n−b)/2⌋ − 1). | Explorer | **proved** |
| H-C20-3 | C03's Conjecture 4.6 agrees with the published Zantema–Geser characterisation. | Historian | **confirmed** — the Historian found the scanned report; its Theorem 1.1 is equivalent to the conjecture (REDISCOVERY) |

## Step 2 — Definitions

Run encoding w = a^{x₀} b a^{x₁} ⋯ b a^{x_m}; units (surplus a's in non-final
runs); journeys (the chain of rightmost steps that carries a unit, resp. a
pair, to the right); random descent (C04).

## Step 3 — Falsification design

Strategy independence is a strong check: random descent predicts that the
rightmost and the leftmost strategy give the same length on every word, and
that both equal the exact maximal derivation length. Any discrepancy, any
word not terminating within 10⁶ steps, or any mismatch with the closed forms
would refute the analysis.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C20-01 | all 8 rules, all words of length ≤ 12: 0 non-terminating, 0 strategy mismatches, 0 mismatches with the exhaustive maximum (n ≤ 8); D(n) = 2^(n−2) − 1 and D(n) = max_b b(2^⌊(n−b)/2⌋ − 1) exactly; the per-word formula for aab → babaa matches every word |

## Step 6 — Analysis

Random descent turns a termination problem into a question about *one*
strategy, and the run encoding turns that strategy into tokens moving right.
A single surplus a (aab → ababa) or a pair of a's (aab → babaa) travels until
it is absorbed; every journey at most doubles the number of b's, which gives
exponential but exactly computable derivation lengths.

## Step 7 — Proofs and counterexamples

Theorems 1–2 and Corollary 3 of `proofs/paper/C20.md`. With them all 868 rules
of the C04 extended census are classified (480 terminating, 388 not).

## Step 8 — Comparison with existing mathematics (Historian)

* Both rules are *right barren* in McNaughton's sense, and barren one-rule
  systems terminate (R. McNaughton, RPI reports 94-18, 95-15; A. Geser,
  "Termination of string rewriting rules that have one pair of overlaps",
  ICASE Report 2002-33, Theorems 3.2–3.3,
  [NASA NTRS](https://ntrs.nasa.gov/api/citations/20020088729/downloads/20020088729.pdf)).
  Termination is a **REDISCOVERY**. The report proves linear derivation
  lengths only for its non-barren case; our exact exponential complexities
  were not found (**POTENTIALLY NOVEL**, small).
* A 2026 survey still lists termination of general one-rule string rewriting
  as open ([arXiv:2608.19397](https://arxiv.org/pdf/2608.19397)).
* Zantema–Geser, *A complete characterization of termination of
  0^p1^q → 1^r0^s*, AAECC 11 (2000) 1–25 (tech. report UU-CS-1994-44). The
  Director's retrieval attempts failed (HTTP 403, a Cloudflare challenge,
  HTTP 500); the Historian later found the scanned report on an older archive
  host ([ics-archive](https://ics-archive.science.uu.nl/research/techreps/repo/CS-1994/1994-44.pdf)).
  Its Theorem 1.1 is equivalent to C03's Conjecture 4.6 (equivalence checked by
  case analysis and on all parameters ≤ 40): CLM-C20-04 and CLM-C03-10 are
  **REDISCOVERY**, PROVEN by the published proof
  (`reviews/historian_C03_C10.md`, item 20).

## Step 9 — Applications

None claimed.

## Step 10 — Documentation

`record.yaml` (4 claims). Textbook: Chapter 21 (Volume 10). C04's record was
updated (CLM-C04-03 now PROVEN).

## Next directions

1. Complexity classes of all terminating barren one-rule systems with |l| ≤ 4.
2. Formalise Theorems 1–2 in Lean.

*(The first version of this list asked for the Zantema–Geser theorem; the
Historian has since obtained and compared it — see Step 8.)*
