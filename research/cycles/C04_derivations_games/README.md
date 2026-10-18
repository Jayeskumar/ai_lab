# Cycle C04 — Derivation lengths, random descent and rewriting games

**Branch:** A meets D (transformation systems as games) · **Status:** complete
**Experiments:** EXP-C04-01 … EXP-C04-10 · **Claims:** CLM-C04-01 … CLM-C04-16
**Proofs:** `proofs/lean/Infinity/C04_Derivations.lean` (19 theorems, standard axioms only),
`proofs/paper/C04.md` · **Module:** `systems/derivations.py`

## Step 1 — Hypotheses

Question: *for a single rewriting rule, how long are derivations, when does the
order of rewriting not matter, and what games do rules define?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C04-0 | *(bold)* A rule l → r with \|l\| ≤ 3 terminates iff l is not a factor of r. | Inventor | true for \|r\| ≤ 3, **refuted** for \|r\| ≤ 5 (ab → bbaa) |
| H-C04-G | Every terminating rule has linear, quadratic or exponential complexity given by a linear recurrence. | Explorer | classes hold; **recurrence part refuted** (aab → ba) |
| H-C04-1 | *(bold)* Random descent iff the lhs is unbordered. | Inventor | "if" proved in Lean; "only if" **refuted** (aa → a) |
| H-C04-2 | Random descent iff critical peaks join with equal-length derivations. | Explorer | 0 disagreements; follows from van Oostrom's theorem |
| H-C04-3 | Every one-rule system has a constant-step potential; confluence ⇔ RD (terminating). | Formal Verifier | **proved** |
| H-C04-4 | RD games: Grundy value = D(w) mod 2. | Explorer | proved |
| H-C04-5/7 | Unary lhs rules are take-and-break (octal) games. | Explorer | proved; Dawson's Kayles, Officers, Treblecross … |
| H-C04-6 | *(bold)* Grundy values never exceed 3. | Inventor | **refuted** (a¹⁴ under aa → b has value 4) |
| H-C04-L/8 | aab → ba: D(n) = n − 1 − κ(n); equals OEIS A247983 shifted. | Explorer | proved |

## Step 2 — Definitions

One-rule systems, normal forms, D(w)/d(w), derivational complexity D(n),
random descent (all maximal derivations from a word have the same length *and*
end in the same normal form), length uniformity (same length only), borders,
critical peaks, rewriting games (a move = one rewrite; normal play),
Sprague–Grundy values: see `proofs/paper/C04.md`.

## Step 3 — Falsification design

Every rule with |l|, |r| ≤ 3 (196) and the extended family |r| ≤ 5 (868) was
classified by *checkable certificates*; derivation graphs were explored
exhaustively from all words up to length 10–17; each bold hypothesis had an
explicit refutation target (a non-trivial non-terminating rule, a bordered RD
rule, a non-rational complexity, a Grundy value ≥ 4).

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C04-01 | 196 rules: 162 terminating (70 length-decreasing, 70 length-preserving, 20 linear interpretations, 2 factor counts), 34 non-terminating — **all 34 have l as a factor of r**; 0 unknown, 0 bad certificates |
| EXP-C04-02 | 868 rules (\|r\| ≤ 5): 472 terminating, 388 non-terminating, 8 undecided; **18 non-terminating rules with l not a factor of r** (H-C04-0 refuted; ab → bbaa: aab → abbaa → bb·aab·aa) |
| EXP-C04-03 | complexity of the 162 terminating rules (55 symmetry classes): 140 linear, 14 quadratic, 4 exponential, 4 non-rational (aab → ba class); simple closed forms for 54 classes, e.g. ⌊n²/4⌋ (ab → ba), ⌊n(n−1)/6⌋ (aab → aba), ⌊n²/8⌋ (aab → baa), 2^(n−1) − 1 (ab → bba) |
| EXP-C04-04 | aab → ba: D(n) = n − 1 − min{k : 2^k + k ≥ n} confirmed for all words up to length 21 and as an identity to n = 20000; stalls exactly at n = 2^k + k + 1 (4, 7, 12, 21, 38, …) |
| EXP-C04-05 | 84 unbordered rules: all RD; 78 bordered: 18 RD (H-C04-1 refuted), 60 neither RD nor confluent; critical-peak criterion agrees in all 162 cases |
| EXP-C04-06 | constant-step potential verified for 5365 rules on 470,927 steps (0 violations); 770 bordered length-preserving rules (\|l\| = 4, 5): every confluent one is length-uniform; 126 are length-uniform but not confluent |
| EXP-C04-07 | 162 games: parity theorem holds for all RD rules; run decomposition holds for all 58 unary-lhs rules; max Grundy ≤ 3 on words ≤ 10 |
| EXP-C04-08 | word games = run games (n ≤ 20) = octal recursions (n ≤ 3000): aa → b = Dawson's Kayles (period 34 from 53, Guy–Smith window verified), aaa → aba = 0.4 (period 34), aa → ab = Officers, aaa → b = 0.007, aaa → ab = 0.06 (no period ≤ 300 up to 3000) |
| EXP-C04-09 | OEIS: quadratic/exponential classes and octal sequences are known (A002620, A001840, A130519, A000225, A002187, A046695, A395248); **0.06 Grundy values: no match**; aab → ba complexity matches A247983 (a different definition!) |
| EXP-C04-10 | A247983(n) = n − max{j : 2^j + j ≤ n+1} = D(n+2): 0 mismatches for n ≤ 1500 (n+80-bit arithmetic) |

## Step 6 — Analysis

* **Termination** in this tiny family is almost trivial (only self-embedding
  rules loop), but already at |r| = 4 a rule (ab → bbaa) loops without
  containing its own left side — the gap the bold hypothesis fell into.
* **One rule = one invariant.** Every one-rule system has a potential that
  changes by the same nonzero constant at each step. So the *length* of a
  derivation is determined by its endpoints, and for one-rule systems
  "the order does not matter" (random descent) is *equivalent* to confluence.
  Unbordered left sides (no self-overlap) are the simplest sufficient
  condition — now fully formalised in Lean.
* **Complexity** in the family is linear, quadratic or exponential, but not
  always rational: aab → ba behaves like a binary counter with a sink, giving
  D(n) = n − log₂ n + O(1). Unexpectedly the same numbers count how many terms
  of Σ 1/(h 2^h) are needed to approximate log 2 to n bits (OEIS A247983).
* **Games.** Random-descent rules give trivial parity games. Unary left sides
  give the classical octal games — Dawson's Kayles, Officers, Treblecross — so a
  single rule of size 2 → 2 (aa → ab) already encodes a famous open problem.

## Step 7 — Proofs and counterexamples

Lean (all standard axioms): `random_descent`, `steps_length_unique`,
`unbordered_diamond`, `unbordered_random_descent`, `length_changing_unique`,
`inv_step`, `normal_iff_inv_zero`, `derivation_length_eq_inv`, `p_positions`
(+ helpers). Written: Theorems 1–10 in `proofs/paper/C04.md`.
Counterexamples: ab → bbaa (H-C04-0), aa → a (H-C04-1), aab → ba (H-C04-G,
non-rational), a¹⁴ under aa → b (H-C04-6).

## Step 8 — Comparison with existing mathematics (Historian)

* Random descent and its local criterion: V. van Oostrom, "Random descent",
  RTA 2007 (LNCS 4533, 314–328); formalised in Isabelle (arXiv:1802.08437).
  Our Lean development is an independent re-formalisation. **REDISCOVERY.**
* ab → ba (n²/4) and ab → bba (exponential) are standard examples of
  derivational complexity (Kobayashi; Métivier's conjecture, solved by
  Bertrand, TCS 1994: length-preserving one-rule systems have derivations of
  length ≤ n²/4, attained by ba → ab — our census agrees). **REDISCOVERY.**
* Octal games as rows of pins (Dawson's Kayles, Officers, Treblecross 0.007,
  0.06); Guy–Smith periodicity theorem; Officers, 0.007 and 0.06 have unknown
  ultimate periodicity (Officers searched to 1.4·10^14 values). **REDISCOVERY.**
* Constant-step potential / confluence ⇔ RD for one-rule systems: a quick
  search found no statement (closest: the structure of derivations of
  length-preserving one-rule systems, Inf. & Comput. 2015). **Not assessed.**
* aab → ba complexity and the identity with A247983: no prior statement found;
  OEIS A247983 has no formula. **POTENTIALLY NOVEL** (small).
* The 0.06 Grundy sequence is absent from the OEIS (potential OEIS entry).

## Step 9 — Applications

* *Strategy-independent cost.* For one-rule systems the number of rewrite
  steps between two configurations is an invariant (Theorem 2), so the cost of
  a one-rule normalisation is predictable without simulating it; for
  unbordered rules even the bound "every run ≤ the first run" holds.
* *Complexity estimates.* Closed forms such as ⌊n²/4⌋, ⌊n²/8⌋, 2^(n−1) − 1 and
  n − log₂ n + O(1) give exact worst-case costs of these local transformation
  processes (e.g. bubble-sort-like swaps, doubling processes, binary-counter
  carries).
* *Game design / testing.* Rewriting games provide compact encodings of hard
  octal games; Officers is a 2-letter, 1-rule system. No practical
  improvement claimed.

## Step 10 — Documentation

`record.yaml` (claims, journal). Textbook: Volume 2/5 ("Derivations as
quantities", "Games from rewriting").

## Next directions

1. Decide termination of aab → ababa and aab → babaa (matrix interpretations?).
2. Structure of the rewriting games of aba → u / bab → u (alternating runs).
3. Derivational complexity for |l| = 4: does a non-rational class beyond
   n − Θ(log n) appear? Are there polynomial degrees ≥ 3 for non-length-preserving rules?
4. Submit the 0.06 Grundy sequence and the A247983 formula to the OEIS (human
   decision).
