# Cycle C12 — Relational one-heap games

**Branch:** D (structures defined by relations; D1 games) · **Status:** complete
**Experiments:** EXP-C12-01 … EXP-C12-06 · **Claims:** CLM-C12-01 … CLM-C12-13
**Proofs:** `proofs/paper/C12.md` (Theorems 1–8) · **Lean:** `proofs/lean/Infinity/C12_Games.lean`
**Code:** `systems/relational_games.py`, `experiments/C12/`

System D asks for structures in which only relations matter. A one-heap game is
the purest example: a position n has a set of options, and the Sprague–Grundy
value g(n) = mex{g(m) : m an option} is defined from the option relation alone.
This cycle takes familiar arithmetic *relations* (divides, is coprime to, is a
submask of, differs by a square, …) as move rules and asks which relations
produce structured value sequences.

## Step 1 — Hypotheses

| ID | Hypothesis | Outcome |
|---|---|---|
| H-C12-0 (Explorer, exploratory) | Every game in the catalogue is eventually periodic, eventually arithmetic-periodic, or has a closed form in a number-theoretic function | **inconclusive**: 13 of 19 games fit; subtract-a-square/-triangular are *provably* not (arithmetic-)periodic, but "no closed form" is not a theorem (CLM-C12-09) |
| H-C12-1 (Inventor, bold) | For the six divisibility/coprimality games, g(n) depends only on the prime signature of n | **refuted** for 5 of 6 (g(2) ≠ g(3) in G01); true only for "move to a proper divisor" (g = Ω) (CLM-C12-10) |
| H-C12-2 (Inventor, bold) | Subtraction games with sparse move sets (squares, triangular numbers, Fibonacci numbers, primes) keep a positive density of P-positions | **refuted** for squares and triangular numbers (density 0, Theorem 7); open for Fibonacci and primes (CLM-C12-11) |
| H-C12-3 (Explorer) | The Grundy function of G03 "subtract a divisor 1 < d < n" is v₂(n) up to finitely many exceptional odd parts | **proved** (computer-assisted, Theorem 8; CLM-C12-04) |
| H-C12-4 | Closed forms for the arithmetic games (v₂, Ω, prime index, popcount, logarithms; splitting parity; powers of k) | proved (Theorems 1–6) |

## Step 2 — Definitions

19 games (`experiments/C12/games_catalog.py`); each move goes to a smaller position.

| Game | Move from n | Relation |
|---|---|---|
| G01 / G02 | n → n − d, d \| n, d < n / d ≤ n | divisibility |
| G03 | n → n − d, d \| n, 1 < d < n ("Deleting Divisors") | divisibility |
| G04 | n → d, d \| n, d < n | divisibility |
| G05 / G06 | n → m, 1 ≤ m < n, gcd(m, n) = 1 / > 1 | coprimality |
| G08 – G12 | n → n − s, s a square / Fibonacci number / power of 2, 3, 4 / prime / triangular number | additive set |
| G13 | n → proper binary submask of n | bitwise |
| G16 / G17 / G18 | split n = a + b with gcd(a, b) = 1 / a \| b / a ≠ b (Grundy's game) | splitting |
| G19 / G20 | n → n mod k (1 ≤ k < n) / n → ⌊n/k⌋ (2 ≤ k ≤ n) | Euclidean division |

(G07 "subtract k coprime to n" is shown to coincide with G05.) Values are exact
(`systems/relational_games.py`: generic mex solver, a bitset solver for
subtraction games, a vectorised solver for splitting games).

## Step 3 — Falsification design

* Census (EXP-C12-01): period and arithmetic-period detection with a guard
  against end-of-range artefacts (tail ≥ 3 periods *and* ≥ half the range).
* Every conjectured closed form is compared term by term with the exact values
  over the whole computed range (EXP-C12-02, EXP-C12-06); structure theorems are
  tested on fresh instances (k = 2..20 for powers of k, 40 random splitting
  relations).
* Bold hypotheses get explicit counterexample searches (EXP-C12-05) or density
  measurements at five scales (EXP-C12-03).
* Novelty: OEIS look-up of every Grundy and P-position sequence, with the matched
  names read (EXP-C12-04), plus literature checks (Step 8).

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C12-01 (census, 19 games) | 5 eventually periodic (powers of 2, 3, 4: periods 3, 2, 5; G16, G17: period 2), 0 arithmetic-periodic, 14 neither within range. Maxima: G01 16, G02 17, G03 16, G04 16, G13 16, G08 74, G09 14, G11 11, G12 110 (n ≤ 10⁵); G05 669, G06 2499, G18 65, G19 11 (n ≤ 5000); G20 14 (n ≤ 2·10⁴). The first run reported spurious periods (G09 with preperiod 99970; constant tails of G19/G20); the detector was fixed and the census re-run — both runs are on record |
| EXP-C12-02 (closed forms) | 0 mismatches in every check: G01 = v₂, G02 = v₂ + 1, G04 = Ω, G13 = popcount (n ≤ 10⁵); G05 = prime index, G19, G06 (g(2k) = k − 1, odd bound, P = {1} ∪ primes) (n ≤ 5000); G07 = G05 (n ≤ 1500); G20 = ⌊log₂ n⌋ (n ≤ 2·10⁴); G03 P-positions (n ≤ 10⁵); powers of k = {1, k} for k = 2..20 (n ≤ 2·10⁴); 40 random splitting relations (n ≤ 1500). Largest g(m)/m for odd m ≤ 5000 in G06: 0.24985 |
| EXP-C12-03 (sparse sets, n ≤ 2·10⁵) | P-density at N = 1.25·10⁴ → 2·10⁵: squares 0.0538 → 0.0222, triangular 0.0344 → 0.0116, Fibonacci 0.1685 → 0.1804, primes 0.1347 → 0.1549. Max Grundy value: squares 36 → 95, triangular 50 → 144, Fibonacci 13 → 14, primes 11 throughout |
| EXP-C12-04 (OEIS) | 18 of 19 Grundy sequences match an entry (the G10c match is a spurious shifted window of A014586; G19 is A099396 shifted by one); only G03 matches nothing, for both its Grundy and its P-position sequence |
| EXP-C12-05 (signatures) | counterexamples: G01 (2, 3: g = 1, 0), G02 (2, 3: 2, 1), G03 (4, 9: 1, 0), G05 (2, 3: 1, 2), G06 (6, 10: 2, 4); G04 depends only on the signature (n ≤ 5000) |
| EXP-C12-06 (G03 Grundy function) | the closed form F of Theorem 8 equals g on [0, 10⁵] (0 mismatches); 96 positions with g ≠ v₂, all with odd part ≤ 15 (by odd part 1: 16, 3: 15, 5: 13, 7: 11, 9: 11, 11: 11, 13: 9, 15: 10); max \|g − v₂\| off the odd powers of 2 is 2; records at 4, 6, 12, 24, 64, 96, 256 and then 5·2^a (a = 6..14); inductive-step certificate (odd parts ≤ 15, 13 ≤ a ≤ 100): 0 failures; random mex checks: 0/3000 even and 0/1000 odd n |

## Step 6 — Analysis

* **Arithmetic relations give arithmetic values.** Divisibility games are
  governed by v₂ and Ω, coprimality by the smallest prime factor, bitwise and
  quotient games by popcount and logarithms. The proofs are all of one shape: a
  chain of options realises every smaller value, and a valuation argument rules
  out the value itself.
* **One forbidden move changes the game.** G01 (subtract any proper divisor)
  has g = v₂ exactly; forbidding d = 1 (G03) makes the odd powers of 2 losing
  and perturbs the values on numbers whose odd part is at most 15 — but nowhere
  else (Theorem 8). The perturbation is bounded (|g − v₂| ≤ 2 except at the odd
  powers of 2) and eventually a constant shift for each exceptional odd part
  (−2 for 3, +2 for 5, +1 for 7–15, −1 or a P-position for 1).
* **Splitting is rigid.** Every splitting game in which each heap can be split
  has g = [n even]: every play has exactly n − 1 moves. Grundy's game escapes
  only because heaps 1 and 2 cannot be split.
* **Sparse additive sets are wild.** Squares and triangular numbers give
  density-zero P-sets (counts grow roughly like N^0.67 and N^0.61 between
  N = 10⁵ and 2·10⁵, from the measured densities), so no periodicity is
  possible. Primes and Fibonacci numbers behave differently: maximal values that
  stop growing within range (11 and 14) and P-densities that do not decay (Fibonacci 0.169 → 0.180, primes
  0.135 → 0.155).

## Step 7 — Proofs and counterexamples

Written proofs: Theorems 1–8 in `proofs/paper/C12.md`. Machine-checked in Lean 4
with Mathlib (no `sorry`, no `native_decide`, axioms `propext`, `Classical.choice`,
`Quot.sound` only): uniqueness of Grundy functions (`IsGrundy.unique`), the
characterisation of P-positions (`IsGrundy.zero_pset`, `IsPSet.unique`), the
residue lemma (`residue_grundy`) with the power-of-2 corollary
(`power_of_two_grundy`), the splitting parity theorem (`split_parity`) and the
P-positions of G03 (`g03_pset`, `g03_P_positions`). Theorem 8 is
computer-assisted: exact computation for n ≤ 10⁵, a written inductive step for
odd parts ≥ 17, and a shift-invariance argument plus a finite certificate for
odd parts ≤ 15 (trust base stated in the proof; awaiting Skeptic review).
Counterexamples for H-C12-1 are in EXP-C12-05.

## Step 8 — Literature (Historian)

* Sprague–Grundy theory (Sprague 1935, Grundy 1939); Berlekamp, Conway & Guy,
  *Winning Ways* (subtraction games, take-and-break games, Grundy's game).
* Iannucci & Larsson, "Game values of arithmetic functions" (arXiv:2101.07608,
  2021): maliquot (Theorem 1 = G04), saliquot (Theorem 2 = G02), totative
  (Theorem 5 = G05/G07), nontotative (Theorem 6: values of G06 plus one),
  residue-throw-divisor (Theorem 12 = G19, proof left to the reader there).
* G03 is Codeforces 1537D "Deleting Divisors" (2021) — its P-positions are the
  official solution. G01's win/loss version is the "Divisor Game" puzzle
  (LeetCode 1025).
* Subtract-a-square: its P-set is a maximal square-difference-free set, so it has
  density zero by Furstenberg–Sárközy (Wikipedia "Square-difference-free set";
  Eppstein, FUN 2018); polynomial version: Kamae–Mendès France 1978.
* OEIS: A014586 (squares), A019509 (triangular), A014588 (Fibonacci; P-density
  ≤ 1/5 by Pond and Howells 1965, cited in A001581), A014589 (primes: a(n) ≤ 11
  for n ≤ 10⁹ per the entry), A002188 (Grundy's game), A279119 (G06), and
  Flammenkamp's 1997 dissertation on long periods in subtraction games (cited
  in those entries).

**Verdict.** Theorems 1–7 and the prime-bound observation are **rediscoveries**
(an honest reading: the Historian downgraded G03's P-positions from "potentially
novel" to rediscovery after finding the Codeforces problem). The complete Grundy
function of G03 (Theorem 8) was found neither in the OEIS nor in these sources:
**potentially novel**, not a priority claim. The Lean formalisation of the
Grundy framework and of the G03 P-positions is new work but not new
mathematics.

## Step 9 — Applications (Application Researcher)

* Closed forms replace the dynamic programme over all smaller positions
  (Θ(n log n) for the divisor games, Θ(n²) for the coprimality games) by a direct
  evaluation (O(log n) bit operations for v₂, popcount and logarithms; a
  factorisation and a prime count for the prime-index forms) — and, through XOR,
  solve *sums* of games. Example: the multi-heap version of "Deleting Divisors"
  is not solved by the P-positions alone but is solved by Theorem 8 (XOR the
  values). This is a qualitative gain; no benchmark was run and no
  performance improvement is claimed.
* The P-positions of subtract-a-square are a greedy maximal
  square-difference-free set (A030193) — a link to additive combinatorics that
  is classical.
* No practical application beyond recreational and competitive-programming
  games was identified.

## Step 10 — Documentation

`record.yaml` (claims CLM-C12-01 … 13, journal C12-01 … 12); proofs in
`proofs/paper/C12.md` and `proofs/lean/Infinity/C12_Games.lean`; proposed
textbook placement: Volume 5 ("Mathematical Transformations and
Relationships"), chapter "Games defined by relations".

## Next directions

1. Boundedness of subtract-a-prime (≤ 11) and subtract-a-Fibonacci (≤ 14) Grundy values; is the Fibonacci P-density converging (≤ 1/5)?
2. The "forbidden move" phenomenon: for which d₀ does forbidding "subtract d₀" in G01 give a finite-exception perturbation of v₂ as in Theorem 8?
3. G06 odd values: prove g(m) < m/4 for odd m (max ratio 0.24985 for m ≤ 5000) or connect to Iannucci–Larsson's partial results.
4. Formalise Theorem 8 in Lean (the certificate is finite once the shift-invariance lemma is formalised).
