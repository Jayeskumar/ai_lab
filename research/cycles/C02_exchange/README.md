# Cycle C02 — Exchange systems: positional numeration as normal forms

**Branch:** A → C (from transformations to representations) · **Status:** complete
**Experiments:** EXP-C02-01 … EXP-C02-06 · **Claims:** CLM-C02-01 … CLM-C02-10
**Proofs:** `proofs/lean/Infinity/C02_Exchange.lean`, `proofs/paper/C02.md`

## Step 1 — Hypotheses

C01 showed that a multiset of tokens *is* a count. Research question: *if
tokens live on levels and may be exchanged by local rules, do positional
numeration systems — and their "value" — emerge without being assumed?*

| ID | Hypothesis | Proposer |
|---|---|---|
| H-C02-0 | b tokens → 1 token one level up turns unary n into base-b digits, independent of the order of exchanges. | Inventor |
| H-C02-F | The Fibonacci exchanges ([k]+[k+1] → [k+2], 2[k] → [k+1]+[k−2], boundary rules) always reach the Zeckendorf representation. | Inventor |
| H-C02-1 | A carry rule m[k] → Σ b_j[k+j] terminates from every unary start iff Σ b_j < m; the emergent base is the positive root r of Σ b_j r^j = m. | Explorer |
| H-C02-2 | Representations respect the radix order. | Explorer |
| H-C02-4 | *(bold)* Every terminating rule gives each integer exactly one stable representation. | Inventor |
| H-C02-4′ | *(after refutation)* Uniqueness holds iff the reduced carry polynomial is primitive (and irreducible). | Skeptic |

## Step 2 — Definitions

Configurations, carry rules, carry polynomial, emergent base, value, stable
configurations, the upward sweep and its window map: `proofs/paper/C02.md`.
The *value* V(c) = Σ c_k r^k is not assumed — it is the (unique up to scale)
invariant of the exchange rule, discovered by solving m w_k = Σ b_j w_{k+j}.

## Step 3 — Falsification design

Exhaustive derivation graphs (all exchange orders) for small inputs; a survey
of all 189 carry rules with m ≤ 4, J ≤ 3, b_j ≤ 3; rigorous non-termination
certificates (recurring or dominated windows of a monotone map); exact
algebraic-number arithmetic (minimal polynomials, integer matrices) to search
for two stable configurations of equal value.

## Steps 4–5 — Implementation and execution

`systems/exchange.py` (batch-firing stabilisation, general rule-schema
explorer, Fibonacci rules). Reproduce: `python -m lab run --cycle C02`.

| Experiment | Outcome |
|---|---|
| EXP-C02-01 | 134 exhaustive derivation graphs (b = 2..5, n ≤ 40) + fast checks n ≤ 20000: unique normal form = base-b digits, all derivations of length (n − s_b(n))/(b − 1); 0 failures |
| EXP-C02-02 | Fibonacci exchanges: unary n ≤ 40 and all 2167 configurations of value ≤ 26 reach the Zeckendorf representation, no cycles; min/max derivation lengths recorded |
| EXP-C02-03 | 189 carry rules: exactly the 31 with Σ b < m terminate; all 158 others carry a certificate of an infinite derivation; 0 radix-order inversions up to n = 3000 |
| EXP-C02-04 | **H-C02-4 refuted** for 4 rules (e.g. 4[k] → 2[k+1]: "2" and "10" both have value 2); merge-and-stabilise addition: 0 failures in 62,000 trials |
| EXP-C02-05 | **H-C02-4′ confirmed**: 28 rules with primitive irreducible reduced polynomial are collision-free over *all* stable configurations; the 3 non-primitive ones collide; 0 violations |
| EXP-C02-06 | OEIS: base-3/2 representations = A024629 (rational base), shortest Fibonacci derivation = A219641 (n − z(n)); longest Fibonacci derivation lengths and the representations in bases r ≈ 1.3028 (3[k] → [k+1]+[k+2]) and others: no OEIS match. One hit (A089881, twin primes) is a spurious shifted-window coincidence. |

## Step 6 — Analysis

* **Value is emergent.** The exchange rule alone determines the weights:
  w_k = r^k with r the positive root of the carry polynomial. Integer bases
  (rule b → 1), rational bases (p → q, r = p/q), quadratic bases
  (3 → 1+1, r = (−1+√13)/2 ≈ 1.3028), and Fibonacci weights all arise.
* **The abelian property** makes the order of exchanges irrelevant for carry
  rules: one diamond lemma gives uniqueness of normal forms, of derivation
  length and of the firing vector.
* **Termination is decided by Σ b vs m.** B < m: always terminates. B > m:
  the value bound kills termination for large n. B = m: a *glider* — the
  uniform-firing window T = (tail sums of b) — travels upward forever
  (observed for all 28 such rules).
* **Uniqueness is arithmetic.** It fails exactly when the reduced carry
  polynomial has a common factor; with a primitive irreducible polynomial it
  is a Gauss-lemma consequence (now Lean-verified).
* The Fibonacci system is *not* abelian: derivation lengths range from
  n − z(n) to a much larger maximum (e.g. 17..34 for n = 20).

## Step 7 — Proofs and counterexamples

Lean: `exists_large_coeff`, `digits_unique` (uniqueness theorem's core).
Written proofs: Theorems 1–8 in `proofs/paper/C02.md`. Computer-assisted:
non-termination certificates for 158 rules. Counterexample: 4[k] → 2[k+1].

## Step 8 — Comparison with existing mathematics (Historian)

* Abelian property: chip-firing / abelian sandpiles (Dhar 1990; Björner,
  Lovász, Shor 1991; abelian networks, Bond–Levine). **REDISCOVERY.**
* Rule p → q: rational base numeration of Akiyama, Frougny and Sakarovitch
  (2008); OEIS A024629. **REDISCOVERY.**
* Fibonacci exchanges = the **Zeckendorf game** (Baird-Smith, Epstein, Flint,
  Miller, arXiv:1809.04881): termination and the shortest game N − Z(N) are
  theirs; the longest game is studied by Cusenza et al. (closed form for
  general N reported open). **REDISCOVERY**; our longest-game values for
  N ≤ 40 are not in the OEIS.
* Uniqueness theorem: the Gauss-lemma argument is classical in the theory of
  canonical number systems / generalized radix representations (Kovács,
  Pethő; Akiyama et al.); likely known for this family. **Not assessed**,
  flagged for the Historian audit.
* Termination dichotomy, uniform glider for B = m: not found in a quick look;
  **not assessed**.

## Step 9 — Applications

* *Counters and arithmetic by local rules:* merge-and-stabilise adds numbers
  in any abelian exchange system without a global carry algorithm; this is
  the sandpile-monoid structure and is natural for asynchronous/distributed
  hardware where only local exchanges are possible. Not benchmarked here
  (cost of counting is studied in cycle C10).
* *Exotic bases with unique digits* (e.g. r ≈ 1.3028 with digits 0..2) give
  redundancy-free encodings whose length grows as log_r n; whether that is
  useful for coding is examined in cycle C11.

## Step 10 — Documentation

`record.yaml` (claims, journal). Textbook: Volume 1 Chapter 2
("Numeration from exchange").

## Next directions

1. Prove the B = m conjecture (a spreading lemma for the sweep).
2. Closed form / growth of the longest Fibonacci exchange (Zeckendorf game).
3. Lean: formalise the abelian property and the termination dichotomy.
4. Which carry rules give *regular* languages of representations?
