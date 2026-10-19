# Cycle C13 — Anchored spectra II: which sets of integers are spectra?

**Branch:** B (invented operations; continues C06) · **Status:** complete
**Experiments:** EXP-C13-01 … EXP-C13-09 · **Claims:** CLM-C13-01 … CLM-C13-12
**Proofs:** `proofs/lean/Infinity/C13_Spectra.lean` (25 theorems incl. 13 main results, standard axioms only, no `sorry`),
`proofs/paper/C13.md` (Theorems 1–6) · **Module:** `systems/anchored.py`

## Step 1 — Hypotheses

Question: *an anchored magma has x ⋆ 0 = x + 1 on ℤ/N; the spectrum of a law is
the set of N admitting a model. C06 showed spectra such as the powers of two,
the odd numbers and the golden-ratio moduli, all closed under coprime
products. Which sets of integers are spectra?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C13-1 | *(bold)* Every anchored spectrum is closed under divisors. | Inventor | **refuted** — x = x(x(xx)) has models of every size except 2 (Lean); violations are common |
| H-C13-2 | *(bold)* Laws with an infinite, non-trivial affine spectrum are affinely rigid. | Inventor | **refuted** — 146 of 147 tested laws from infinite classes have non-affine models |
| H-C13-3 | Affine spectra are root sets of polynomial systems: divisor- and CRT-closed, finite ones are divisor sets, infinite ones classical. | Explorer | **proved** (Theorem 1); 152 spectra, no exception |
| H-C13-4 | The W-family (xy)z = x(y W(z)) is rigid with spectrum {N : a·c_W(a) ≡ 1 solvable}. | Formal Verifier | **proved in Lean** for every W; 0 mismatches for 23 terms, N ≤ 9 |
| H-C13-5 | *(bold)* A one-variable law has spectrum {1} or a cofinite spectrum. | Skeptic | **refuted** — x = (xx)x has spectrum {1, 2} |
| H-C13-6 | A sound offset-closure procedure proves most of CLM-C06-10 and is never contradicted by SAT. | Formal Verifier | **confirmed** — 16 of 17 laws; 0 contradictions in 1,245 checks |

## Step 2 — Definitions

Anchored magma, spectrum Spec(E); affine table x ⋆ y = x + a·y + 1 (under the
anchor these are all tables αx + βy + γ); the *affine system* of a law (the
coefficient differences of both sides evaluated as linear forms over ℤ[a]);
the *affine spectrum* Aff(E) ⊆ Spec(E); *affinely rigid* (all models affine);
*translation table* x ⋆ y = x + 1 + κ(y); c_W(a) = Σ_{leaves} a^{right depth};
offset congruence closure (proofs/paper/C13.md, Theorem 6).

## Step 3 — Falsification design

Each bold hypothesis named its refuting object: a law with a model of size N
but none of some d | N (H-C13-1); a non-affine model of a law from an infinite
affine class (H-C13-2); a one-variable law with a finite non-trivial spectrum
(H-C13-5); a model count different from the root count (H-C13-4); a SAT model
of a size not dividing a closure bound (H-C13-6). SAT runs record UNKNOWN
instead of guessing; composite sizes are skipped only when all their proper
divisors already have models (no violation is then possible).

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C13-01 | 18,581 laws (3 variables, ≤ 4 leaves/side) → 2,400 affine systems → 27 spectra; 75,625 laws (2 variables, ≤ 5 leaves) → 3,631 systems → 125 spectra. Every finite spectrum is Div(L) (80 values of L ≤ 328). Infinite ones: odd numbers, 3 ∤ N, −1/2/3 squares (A008784, A057126, A057125), A034017, A089270, A004613, A058529, A192453, A354467, forms of discriminant −7, −11, 13; 29 conditions (plastic, tribonacci, tetranacci, Φ₅, …; four of them quadratic) give sequences **not in the OEIS** |
| EXP-C13-02 | 147 laws (3 shortest per infinite class, classes selected by the ℚ-gcd), N ≤ 8, affine tables blocked: **146 have non-affine models**, all at every N = 6, 7, 8; 0 UNKNOWN. (First run: a faulty filter also let in 52 laws from finite classes and reported 198 of 199 — corrected after the Skeptic's review.) |
| EXP-C13-03 | W-family: 23 terms, N ≤ 9: model counts = root counts, all models affine (0 mismatches); 16 polynomials c_W |
| EXP-C13-04 | the 17 laws of CLM-C06-10, N ≤ 12: all spectra as conjectured; only non-affine model: x(yz) = y((yx)z) at N = 2 |
| EXP-C13-05 | 300 random 2-variable laws, N ≤ 9: **81 violate divisor-closure**; pairs (8,2), (6,3), (6,2), (9,3), (4,2), (8,4); 9 laws with UNKNOWN |
| EXP-C13-06 | 150 random 3-variable laws: 29 violations (of 62 with models); 80 random pairs of laws: 17 violations (of 34 with models); 0 UNKNOWN |
| EXP-C13-07 | all 253 one-variable laws (≤ 5 leaves), N ≤ 12: 213 all N, 9 trivial, **24 divisor-closure violations** (missing {2}, {3} or {2,3}), left combs with spectra Div(2), Div(3), Div(4) |
| EXP-C13-08 | offset closure: exact spectra for **16 of 17** laws of CLM-C06-10; exact finite spectrum Div(g) for **6,912** of the 18,581 3-variable laws (6,045 trivial); soundness: 1,245 SAT/affine checks, 0 contradictions |
| EXP-C13-09 | Skeptic cross-checks: cube-law models N = 3..60, W-family on 42 six-leaf terms (N ≤ 6), six atlas identifications vs. direct definitions to N = 1000 — all pass |

Two runs were stopped for exceeding the 15-minute budget (EXP-C13-02 first
version: 4 laws per class, N ≤ 9, 2·10⁶ conflicts; EXP-C13-05 first version:
600 laws, N ≤ 10) and replaced by the documented smaller runs. After a
container restart experiments 01–08 were re-run on the final code, with
run times moved to the volatile `timings` field so that result hashes are
reproducible.

## Step 6 — Analysis

* **Affine spectra are arithmetic, and single laws reach far into number
  theory.** A law's affine models form the root set of a polynomial system, so
  its affine spectrum is a "local" set (determined by prime powers): divisor
  sets for coprime systems, and residue conditions for the others. Among laws
  of at most four or five leaves one already finds quadratic reciprocity sets
  (−1, 2, 3 squares; golden ratio; Eisenstein), cyclotomic sets (prime factors
  1 mod 4, ±1 mod 8, 1 mod 12; −1 a fourth power) and cubic/quartic sets that
  the OEIS does not list.
* **But affine spectra are only lower bounds.** Short laws are weak; 146 of the
  147 tested laws from infinite classes have non-affine models, usually at every
  size beyond a small threshold.
* **Rigidity comes from a right-normed shape.** If the law is
  (xy)z = x V(y, z), the substitution z = 0 gives x ⋆ σ(y) = x ⋆ y + 1, and an
  orbit-counting argument forces a translation table (Theorem 2). For
  V = y W(z) a shift equation then forces linearity (Theorem 3), so the true
  spectrum is the root set of a·c_W(a) − 1 — every gap-free polynomial with
  constant term 1 occurs. This generalises C06's golden law to n-bonacci laws.
* **Divisor-closure fails, and fails often.** The anchor pins only column 0;
  a one-variable law can be blocked at N = 2 by the row of 0 alone while every
  larger size has room for a model (Theorem 5). In random samples a third to a
  half of the laws with a non-trivial model violate divisor-closure (81 of 251,
  29 of 62, 17 of 34 pairs). What survives is closure under
  coprime products (C06 Theorem 8) and divisor-closure for rigid laws.
* **Finite spectra can be proved mechanically.** The hand proofs of Theorem 4
  use only law instances at small elements, the anchor and functionality of the
  table; offset congruence closure automates exactly this and is sound by
  construction (Theorem 6).

## Step 7 — Proofs and counterexamples

Lean (`C13_Spectra.lean`, all standard axioms): `translation_form`,
`right_normed_translation`, `linear_of_shift`, `golden_law_models` (C06
Theorem 6, which C06 left as a Lean target), `golden_law_model_of_root`,
`T1.eval_affine`, `T1.cpoly_eq`, `w_family_models`, `w_family_model_of_root`,
`law13_size_dvd_three`, `law13_model_three`, `law12_size_dvd_two`,
`law12_model_two`, `cube_law_no_two`, `cubeOp_model`. Written: Theorems 1–6
of `proofs/paper/C13.md`. Counterexamples: x = x(x(xx)) (H-C13-1, H-C13-2),
x = (xx)x (H-C13-5).

## Step 8 — Comparison with existing mathematics (Historian)

* The arithmetic sets are classical: OEIS entries A005408, A001651, A008784,
  A057126, A057125, A034017, A089270, A004613, A058529, A192453, A354467,
  A244779, A244780, A243656, A225771 (read; their names state the same
  conditions). Roots of the tribonacci polynomial modulo primes are studied by
  Klaška and Skula (Fibonacci Quart. 48, 2010) and Moree and Noubissie
  ([arXiv:2205.06685](https://arxiv.org/pdf/2205.06685)); the composite-modulus
  sets of the tribonacci, plastic and Φ₅ laws are not in the OEIS.
* Spectra of varieties (sets of sizes of finite algebras) are a classical
  topic: W. Taylor, "Maltsev conditions and spectra", J. Austral. Math. Soc.
  (1980); K. Kearnes' work on spectra. A variety's spectrum is closed under all
  products; anchored spectra are closed only under coprime products, and we
  found no treatment of spectra with a successor anchor.
* Reducing identities to conditions on affine (linear) representations is
  standard for quasigroups and medial groupoids (Toyoda–Bruck). The anchor
  leaves one parameter, which is what makes the atlas computable.
* Offset congruence closure is a variant of congruence closure with integer
  offsets (difference logic), a standard decision-procedure technique; its use
  as a prover of spectrum bounds is the lab's. Not benchmarked against
  finite-model finders (Mace4, Paradox).
* Novelty: W-family theorem and the anchored realisations — POTENTIALLY NOVEL
  (small); Theorem 1 — rediscovery-level elementary facts.

## Step 9 — Applications

None claimed. The offset-closure procedure is a reusable, sound tool for
bounding sizes of finite models of identities with a successor constant; it
proved 6,912 spectra in under a minute, but it was not compared with general
finite-model finders, so no improvement over existing tools is claimed.

## Step 10 — Documentation

`record.yaml` (12 claims, 9 experiments, 9 journal entries). Textbook: Chapter 8, "Which sets
of integers are spectra?" (Volume 3). The status of CLM-C06-10 changes: 16 of
its 17 laws are now proved (CLM-C13-04, CLM-C13-06).

## Next directions

1. Prove the last case of CLM-C06-10, x(yz) = y((yx)z).
2. Which arithmetic sets are *true* spectra of rigid laws? Realise "−1 is a
   square mod N" by a rigid law.
3. Prove that one-variable laws have finite or cofinite spectra (CLM-C13-10).
4. Search larger laws for a sparse non-affine spectrum other than Laver's.
5. Submit the tribonacci-law and plastic-number spectra to the OEIS (human
   decision).
