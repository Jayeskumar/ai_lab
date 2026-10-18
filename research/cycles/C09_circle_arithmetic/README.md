# Cycle C09 — Arithmetic of Knuth's circle semigroup

**Branch:** C × B (cross-branch: an invented operation from C08 studied as an arithmetic) · **Status:** complete
**Experiments:** EXP-C09-01 … EXP-C09-04 · **Claims:** CLM-C09-01 … CLM-C09-08
**Proofs:** `proofs/paper/C09.md`

## Step 1 — Hypotheses

C08 proved that Knuth's Fibonacci product ∘ is associative. A new commutative
semigroup (ℕ≥1, ∘) therefore exists — *what is its arithmetic?* Which numbers
are "circle primes" (not a∘b), how many are there, and is factorisation unique?

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C09-1 | Circle irreducibles thin out like primes (density → 0). | Inventor | **refuted** (density ≥ 1/φ², proved) |
| H-C09-2 | Factorisation into circle irreducibles is unique. | Inventor (bold) | **refuted** (8 = 1∘1∘1 = 2∘2) |
| H-C09-3 | The norm N(n) = ν(n)ν′(n) is multiplicative and detects structure. | Inventor | proved |
| T-C09-A | Reducible ⇒ conjugate in the product zone (ψ³, ψ²). | Formal Verifier | proved + 0 violations to 10⁶ |
| T-C09-B | Factorisation lengths satisfy |ν′(n)| < |ψ|^r. | Formal Verifier | proved + 0 violations to 2·10⁵ |
| C-C09-5 | Irreducible density → 1/φ². | Explorer | conjecture |

## Step 2 — Definitions

Shadow n* = ⌊(n+1)/φ⌋, ν(n) = nφ + n*, ν′(n) = nψ + n*, norm
N(n) = n*² + n·n* − n²; exact integer formulas a∘b = ab + ab* + a*b.
`systems/circle_arith.py` (validated against the digit definition on 89,401
pairs and against OEIS A101330 via C08).

## Step 3 — Falsification design

Enumerate every product ≤ 10⁶; compute all factorisations ≤ 2·10⁵; test the
two window theorems against every n in range (any reducible number outside the
zone, or any over-long factorisation, would refute them).

## Steps 4–5 — Execution

| Experiment | Outcome |
|---|---|
| EXP-C09-01 | ≤ 10⁶: 539,392 irreducible / 460,608 reducible; irreducible density 0.600, 0.577, 0.562, 0.549, 0.539 at 10²…10⁶. First irreducibles 1, 2, 4, 6, 7, 9, 10, 12, 14, 15, …; reducibles not in the OEIS; irreducibles agree with A026273 for 24 terms and then diverge (40 = 4∘4) |
| EXP-C09-02 | 75,332 of n ≤ 2·10⁵ have ≥ 2 factorisations; the first is **8 = 1∘1∘1 = 2∘2**; factorisations of different lengths are common (29,577); max elasticity 2.5 (n = 196,405) |
| EXP-C09-03 | N(a∘b) = N(a)N(b) on all a, b ≤ 400; max |N(n)|/n = 1.382 (= √5/φ); norm ±1 exactly at 1, 2, 3, 5, 8, 13, … (Fibonacci) |
| EXP-C09-04 | **0 counterexamples** to the window obstruction up to 10⁶; forced-irreducible density 0.381966 = 1/φ²; irreducible fraction inside the zone 0.316 → 0.255 (10³ → 10⁶); 0 violations of the length bound |

## Step 6 — Analysis

The embedding ν: (ℕ, ∘) → (ℤ[φ], ×) explains everything:
* Fibonacci numbers are the *units* (ν(F_k) = φ^k); 1 and 2 are the atoms
  generating them, and their factorisations are those of the numerical
  semigroup ⟨2, 3⟩ — hence non-uniqueness already at 8.
* The conjugate coordinate ν′ is multiplicative and confined to a window of
  length 1; products are confined to a sub-window of length 1/φ, so a fixed
  proportion 1/φ² of all integers can *never* be products. Circle primes are
  therefore far more common than ordinary primes.
* Factorisation lengths are bounded by the size of the conjugate (|ν′| < |ψ|^r).

## Step 7 — Proofs and counterexamples

Written proofs of Theorems 1, 3, 4 (`proofs/paper/C09.md`), resting on the C08
theorem. Counterexample to H-C09-2: 8. H-C09-1 refuted by Theorem 3.

## Step 8 — Comparison with existing mathematics

* The ring ℤ[φ] (units ±φ^k, UFD) and Weyl equidistribution are classical.
* Knuth's product and its table: Knuth (1988), Arnoux (1989), OEIS A101330.
* We found no study of irreducibles or factorisation in (ℕ, ∘): the
  irreducible and reducible sequences are not in the OEIS (the A026273 near-match
  is explained by the Beatty structure of 1∘b and breaks at 40). The structural
  results are elementary consequences of Arnoux's embedding; novelty
  provisionally **POTENTIALLY NOVEL** (Theorem 3, Theorem 4) pending the
  Historian audit; the factorisation theory of numerical-semigroup-like
  submonoids of rings of integers is a mature field, so related results may
  exist under other names.

## Step 9 — Applications

None practical claimed. The window obstruction is a cheap *irreducibility
certificate* (one floor computation) — an example of a conjugate-embedding
test that also certifies non-membership in product sets for other Pisot
numeration systems.

## Step 10 — Documentation

`record.yaml`; textbook Volume 4 chapter "Primes of an invented multiplication".

## Next directions

1. Prove Conjecture 5 (almost every n in the product zone is reducible).
2. Characterise the circle irreducibles in terms of the prime factorisation of
   ν(n) in ℤ[φ] plus a unit-adjustment window condition.
3. Repeat for other associative circle products (Pell s ≥ 1, tribonacci s ≥ 3).
