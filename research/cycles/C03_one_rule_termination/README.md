# Cycle C03 — Termination of one-rule string rewriting 0^p 1^q → 1^r 0^s

**Branch:** A (objects and transformations without numbers) · **Status:** complete
**Experiments:** EXP-C03-01 … EXP-C03-04 · **Claims:** CLM-C03-01 … CLM-C03-11
**Proofs:** `proofs/lean/Infinity/C03_Termination.lean`, `proofs/paper/C03.md`

## Step 1 — Hypotheses

Research question: *for the simplest non-trivial transformation systems — one
rule moving a block of 0s past a block of 1s while multiplying them — when do
all transformation sequences stop?*

| ID | Hypothesis | Proposer | Fate |
|---|---|---|---|
| H-C03-1 | Terminates iff some letter count never grows (s ≤ p or r ≤ q). | Inventor (naive) | refuted via the literature (Zantema's problem 0011 → 111000 terminates) |
| H-C03-2 | Terminates iff r < 2q or s < 2p. | Director (first guess) | **refuted**: 011 → 11100 loops (Lean-verified) |
| H-C03-3 | Non-terminating iff r > q, s > p and (r ≥ 2q or s ≥ 2p). | Explorer, after the first 28 loops | **inconclusive** — strong evidence against: e.g. 0011 → 11100000 terminates from every tested start |
| H-C03-4 | Non-terminating iff (r ≥ 2q ∧ s ≥ 2p) or (s ≥ 2p ∧ q < r < 2q ∧ p ∣ s) or (r ≥ 2q ∧ p < s < 2p ∧ q ∣ r). | Explorer, after the s = 4 vs s = 5 surprise | **computationally supported**, 0 contradictions on 625 rules |

## Step 2 — Definitions

Words over {0,1}; one rule ℓ = 0^p 1^q → ρ = 1^r 0^s (p, q, r, s ≥ 1). A *loop*
is a derivation u →⁺ x u y; a *matrix interpretation* assigns d × d matrices
over ℕ to the letters (Hofbauer–Waldmann 2006). The reverse-complement map
φ(w) gives the symmetry (p, q, r, s) ↦ (q, p, s, r). Regions:
*count-decreasing* (s < p or r < q), *conserving* (s = p or r = q),
*both-growing* (s > p and r > q).

## Step 3 — Falsification design

Every hypothesis makes a prediction for every rule. A loop certificate
falsifies "terminating"; a matrix-interpretation certificate (or a published
termination proof) falsifies "non-terminating". Both kinds of certificates are
re-checked independently of the search that found them. "Terminates from u"
is certified by a finite reachable set (the both-growing rules lengthen words,
so cycles are impossible).

## Steps 4–5 — Implementation and execution

`systems/srs_termination.py`: forward-closure loop search (right and left
extensions), strategy-based loop search, exhaustive vectorised
matrix-interpretation search with exact re-check, loop lifting along
0 → 0^p, mirroring along φ, bounded evidence. Reproduce:
`python -m lab run --cycle C03`.

| Experiment | Outcome |
|---|---|
| EXP-C03-01 | 256 rules (≤ 4): 220 terminating (156 count-decreasing + 62 conserving with matrix certificates, 2 conserving by proof), 28 loops, 8 unknown. Contradictions: H-C03-1 0, **H-C03-2 12**, H-C03-3 0. |
| EXP-C03-02 | 625 rules (≤ 5) with a second (strategy) loop finder: 525 terminating, 71 loops (56 by closures, 15 by strategies), 29 unknown. **H-C03-2 35 contradictions**; H-C03-3 0. No both-growing rule admits a matrix interpretation (d = 2 entries ≤ 4, d = 3 upper-triangular ≤ 3). |
| EXP-C03-03 | Divisibility: 49 base loops (1, q, r, k) (q ≤ 5), 147 lifted loops verified; on 66 test rules loops are found **exactly** when p ∣ s; all 36 non-multiples terminate from every start 0^a 1^b (a ≤ 3p, b ≤ 3q+2) and every word of length ≤ 12; 5 unknowns of EXP-C03-02 resolved as looping by mirror images; 24 remain, all predicted terminating by H-C03-4; **H-C03-4: 0 contradictions on 625 rules**. |
| EXP-C03-04 | All 75 base rules (1, q, r, k), q ≤ 6, q < r < 2q, k ≤ 6, loop; 225 lifts verified. Largest loop: 0 1^42 →⁹³³² … (rule 0 1^6 → 1^7 0^6, final word 56,035 letters). |

Loop sizes for r = q + 1 (start 0 1^{q(q+1)} for q ≥ 4, rightmost strategy):
k = 2: 16, 32, 64 steps for q = 4, 5, 6; k = 6: 260, 1556, 9332 steps.

## Step 6 — Analysis

* **Letter counts are not the story.** Rules in which both counts grow can
  terminate (Zantema's problem) and rules with r < 2q can loop (011 → 11100).
* **The doubling region always loops** with a two-step loop.
* **Divisibility.** In the boundary regions (exactly one of r ≥ 2q, s ≥ 2p)
  the behaviour depends on whether the produced block is a whole number of
  consumed blocks: 0011 → 11100000 (s = 5) appears terminating while
  0011 → 111000000 (s = 6) loops. The *lifting lemma* explains the looping side:
  the morphism 0 → 0^p carries every loop of 0 1^q → 1^r 0^k onto a loop of
  0^p 1^q → 1^r 0^{kp}. For non-multiples the leftover s mod p zeros at the
  front of each produced block seem to starve the process — unproved.
* **Loops can be long**: k^q-type growth in the base family; strategy-based
  search found loops that breadth-first closure search (≤ 40 letters) missed.
* **Hard terminating cases resist simple certificates**: no matrix
  interpretation exists in the searched tiers for any both-growing rule,
  consistent with Zantema's problem being non-simply-terminating.

## Step 7 — Proofs and counterexamples

Lean (`C03_Termination.lean`, standard axioms only): `terminating_of_count_lt`,
`terminating_swap`, `not_terminating_of_loop`, `step_map`/`loop_map`,
`not_terminating_double`, `not_terminating_0_11`. Written proof: conservation
theorem (s = p or r = q). Computer-assisted: 601 of the 625 rules with
parameters ≤ 5 are classified with proof — 525 terminating by Theorems 1–2,
76 non-terminating by re-checked loop certificates (71 found directly, 5 as
mirror images). Counterexample to H-C03-2: 011 → 11100.

## Step 8 — Comparison with existing mathematics (Historian)

* The family was **completely characterised** by H. Zantema and A. Geser,
  "A complete characterization of termination of 0^p 1^q → 1^r 0^s" (RTA 1995,
  LNCS 914; AAECC 11(1):1–25, 2000, doi:10.1007/s002009900019). The journal
  version introduces a termination method for hard cases and gives derivation
  complexities for the simply terminating ones. Geser, Waldmann and Wenzel
  (WST 2016) cite it for decidability of termination of one-rule SRS with
  ℓ ∈ 0*1*. Zantema's problem 0011 → 111000 is terminating (A. Geser, "A
  Solution to Zantema's Problem", Passau MIP-9314, 1993; first automated proof
  via RFC match-bounds).
* **We could not access the theorem statement** (publisher, zbMATH and Utrecht
  repository pages were not retrievable from this environment). Whether H-C03-4
  coincides with the published characterisation is therefore *unverified*; if
  it differs, the published theorem takes precedence and H-C03-4 is wrong.
* Long loops in one-rule SRS: Geser, Hofbauer, Waldmann, "Loops of
  superexponential lengths in one-rule string rewriting" (RTA 2002).
* Matrix interpretations: Hofbauer–Waldmann (RTA 2006). Substitution/morphism
  closure of rewriting and the self-embedding criterion are folklore.
* Novelty: **REDISCOVERY** for the termination status of every rule
  (the problem is solved in the literature); our certificates, the lifting
  explanation of divisibility, and the loop-size data are independent
  re-derivations, not new theorems.

## Step 9 — Applications

Termination analysis is a core task of program verification and of rewriting
tools (the Termination Competition; AProVE, TTT2, matchbox). This cycle
reproduces their three pillars at small scale — loop finding, interpretation
search, certificate checking — and adds one cheap, general trick worth
reusing: **lifting non-termination proofs along letter morphisms** (one base
loop certifies infinitely many rules). Honest limitation: nothing here proves a
hard terminating case; that needs match-bounds or the Zantema–Geser method.

## Step 10 — Documentation

`record.yaml` (claims, journal). Textbook: Volume 1 (transformations) and
Volume 9 (refuted hypotheses: H-C03-1, H-C03-2).

## Next directions

1. Obtain the Zantema–Geser theorem statement and compare with H-C03-4.
2. Implement RFC match-bounds to *prove* termination of the 24 open rules
   (≤ 5), starting with 0011 → 111000 and 0011 → 11100000.
3. Prove that every base rule 0 1^q → 1^r 0^k (q < r < 2q, k ≥ 2) loops,
   e.g. from 0 1^{q(q+1)} along the rightmost strategy; explain the k^q loop
   lengths.
4. Lean: formalise the conservation theorem (s = p).
