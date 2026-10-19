# Cycle C16 — Fibonacci dynamics in invented finite algebras

**Branch:** E (System E2 — an independent experimental system: order-2 recurrences in finite magmas)
· **Status:** complete
**Experiments:** EXP-C16-01 … EXP-C16-05 · **Claims:** CLM-C16-01 … CLM-C16-19
**Proofs:** `proofs/paper/C16.md` (Theorems 1–11, Computation 12),
`proofs/lean/Infinity/C16_Dynamics.lean` (6 theorems, standard axioms only)
· **Module:** `systems/magma_dynamics.py`

## Step 1 — Hypotheses

Question: *in a finite magma, the pair (x_{k−1}, x_k) determines
x_{k+1} = x_k ⋆ x_{k−1}. How long can such "Fibonacci sequences" cycle, and what
do the laws of the magma do to the dynamics?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C16-1 | *(bold)* As for Pisano periods, the maximal period is ≤ n² − 1, attained only by quasigroups. | Inventor | **refuted** — x ⋆ y = 1 − y has period 4 = n² |
| H-C16-2 | The pair map is a permutation iff every left translation is a bijection; (n!)^n such tables. | Formal Verifier | **proved** (Lean) — Golomb's criterion |
| H-C16-3 | Full-period tables are de Bruijn cycles: (n!)^n / n² of them. | Formal Verifier | **proved**; 1, 24, 20736 confirmed |
| H-C16-4 | *(bold)* For Laver tables the maximal period is a power of 2. | Inventor | **true**, degenerately: it is 2 (proved) |
| H-C16-5 | *(bold)* No quasigroup is full-period (max n² − 1 for quasigroups). | Inventor | **refuted** at n = 5 (3360 tables) |
| H-C16-6 | A full period forces a parity condition; even-order group isotopes always violate it. | Formal Verifier | **proved** |
| H-C16-7 | Affine magmas with a fixed point have period = order of a companion matrix (anchored = Pisano). | Formal Verifier | **proved** |
| H-C16-8 | *(bold)* Every affine magma's maximal period equals the order of its 3×3 matrix. | Explorer | supported (300/300) |
| H-C16-9 | Nim-multiplication on [0, 2^(2^k)) has maximal period π(2^(2^k) − 1). | Formal Verifier | **proved** (40, 360) |
| H-C16-10 | Magma Fibonacci generators are not competitive PRNGs. | Application Researcher | confirmed (no improvement) |
| H-C16-11 | Random sampling beats exact search for finding full-period quasigroups. | Explorer | supported |

## Step 2 — Definitions

Pair map P(a, b) = (b, b ⋆ a) on M × M; *period* = cycle length; *full-period*
table: one cycle through all n² pairs; *transient* = steps until the orbit is
periodic. Every function M × M → M is the feedback of exactly one magma, so these
are precisely the order-2 feedback shift registers over n letters.

## Step 3 — Falsification design

Each hypothesis named its refuting object: a period n² (H-C16-1); a permutation
pair map with a non-bijective row (H-C16-2); a count ≠ (n!)^n/n² (H-C16-3); a
Laver table whose maximal period is not a power of 2 (H-C16-4); one full-period
quasigroup (H-C16-5); a full-period table violating the parity, or a full-period
even-order group isotope (H-C16-6); a period ≠ matrix order (H-C16-7/8/9); a
magma generator passing the battery (H-C16-10). Counts at n ≤ 5 were obtained by
two independent methods.

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C16-01 | all magmas of order 2, 3 and row-permutation magmas of order 4: max period n²; permutations (n!)^n; full-period tables 1, 24, 20736 = (n!)^n/n², none a quasigroup; quasigroup maximum n² − 1; 3330 classes of order 3 (A001329) |
| EXP-C16-02 | all Latin squares of order ≤ 5: full-period quasigroups 0, 0, 0, **3360** (28 classes; DFS agrees); verified examples for every n = 6…16; coprime products 30 … 72; even-order group isotopes never full-period |
| EXP-C16-03 | Laver A_0…A_10: one fixed point + N − 1 two-cycles, transients ≤ 5; anchored x + y + 1 = Fibonacci mod N; odd/golden laws = companion orders; 300/300 affine = 3×3 order; nimbers 40, 360; groups S3 8, D4 6, Q8 6, A4 16, S4 18 |
| EXP-C16-04 | PRNG battery: PCG64 passes; magma generators fail (low byte, low-bit period 3, or too regular) |
| EXP-C16-05 | DFS and SAT fail from n = 9 within budget; sampling succeeds at rates ≈ 1/n²; partial n = 6 count ≥ 1136 |

## Step 6 — Analysis

* **The general picture is classical once translated.** Magma pair maps are
  exactly order-2 feedback shift registers, so the permutation criterion and the
  full-period count are Golomb's and de Bruijn's results in new clothes — an
  honest rediscovery that also refuted the Pisano-inspired guess.
* **Laws shape the dynamics.** Idempotency creates n fixed points; anchored
  associativity turns the recurrence into the Fibonacci numbers mod N; the odd and
  golden laws of C06 give companion-matrix periods; anchored left-distributivity
  (Laver tables) collapses everything to period ≤ 2.
* **Quasigroups are special for small n only.** A full-period quasigroup is a
  cycle in which every pair occurs once at distance 1 *and* at distance 2. None
  exists for n ≤ 4, then 3360 appear at n = 5 and examples exist up to 16. A
  parity argument explains why isotopes of groups of even order can never work,
  while isotopes of cyclic groups of odd order often do.

## Step 7 — Proofs and counterexamples

Lean: `pairMap_injective_iff`, `pairMap_bijective_iff`, `mirrorMap_eq`,
`pairMap_fixed_iff`, `top_two_cycle`, `anchored_fibonacci`. Written: Theorems 1–11,
Computation 12. Computer-assisted: Theorem 5 (orders 2–5 exhaustive by two
methods; certificates for 6–16). Counterexamples: x ⋆ y = 1 − y (H-C16-1); the
order-5 cycle 0,0,1,0,2,2,0,3,3,1,2,1,4,0,4,4,2,3,2,4,1,1,3,4,3 (H-C16-5).

## Step 8 — Comparison with existing mathematics (Historian)

* Nonsingular feedback shift registers and the q-ary criterion: S. W. Golomb,
  *Shift Register Sequences* (1967); the correspondence with factors of the de
  Bruijn graph, e.g. [arXiv:1911.06670](https://arxiv.org/pdf/1911.06670).
  **REDISCOVERY.**
* Number of de Bruijn cycles (k!)^(k^(m−1))/k^m: van Aardenne-Ehrenfest and de
  Bruijn (1951), BEST theorem;
  [Wikipedia](https://en.wikipedia.org/wiki/De_Bruijn_sequence). **REDISCOVERY.**
* Periods of linear recurrences modulo N (Ward 1933, Wall 1960); Fibonacci
  lengths of groups — S. W. Knox, *Fibonacci Quart.* 30 (1992) 116–120
  ([scan](https://www.mathstat.dal.ca/FQ/Scanned/30-2/knox.pdf)): period 6 for
  dihedral groups, matching D4 here; H. Campbell, P. Campbell,
  [Irish Math. Soc. Bull. 56 (2005)](https://www.maths.tcd.ie/pub/ims/bull56/GiG5602.pdf).
  **REDISCOVERY.**
* Related but different: Tuscan-k squares (Etzion, Golomb, Taylor, *Adv. Appl.
  Math.* 10 (1989)); de Bruijn cycles with distance constraints
  ([D. West's problem page](https://dwest.web.illinois.edu/regs/debruijn2.html));
  universal cycles ([debruijnsequence.org](https://debruijnsequence.org/db/home)).
  No statement of the distance-1/2 characterisation of full-period quasigroups,
  of the counts 0, 0, 0, 3360, or of the even-order isotope obstruction was found.
  **POTENTIALLY NOVEL** (small).
* Laver tables: surveys ([arXiv:1810.00548](https://arxiv.org/pdf/1810.00548),
  [Wikipedia](https://en.wikipedia.org/wiki/Laver_table)) do not mention
  Fibonacci-type recurrences. **POTENTIALLY NOVEL** (small; easy consequence of
  Laver's monotonicity).
* OEIS: the odd- and golden-law period sequences and the order-3 period
  distribution have no match.

**Batch 1.1 update (2026-10-19, [Historian audit](../../../reviews/historian_C11_C20.md)).** P. Klimov,
*Universal Fibonacci sequences and UFS-groupoids* ([arXiv:2604.05754](https://arxiv.org/abs/2604.05754), 2026),
studies the full-period tables of this cycle (his finite UFS-groupoids with periodic universal sequence) and poses
as open (Problems 7.3–7.5) whether one can be left-cancellative, a left quasigroup or a quasigroup. CLM-C16-07
answers this positively (the Historian re-checked the order-5 example); the distance-2 criterion CLM-C16-05 is not
in his paper. Whether to tell the author is left to the human readers of this record.

## Step 9 — Applications

Tested honestly against PCG64 and an LCG (EXP-C16-04): **no improvement**. The
maximal period of any order-2 recurrence on n symbols is n² (65536 for bytes),
and affine generators modulo 2^32 inherit the low-bit weaknesses of lagged
Fibonacci generators (lowest bit of period 3; Fibonacci numbers are not uniformly
distributed modulo 2^k). Full-period quasigroups might be of interest for
sequence design (every pair once at distances 1 and 2), but no application was
tested.

## Step 10 — Documentation

`record.yaml` (19 claims, journal). Textbook: Chapter 18, "Fibonacci dynamics in
invented algebras" (Volume 7).

## Next directions

1. Prove that full-period quasigroups exist for every n ≥ 5 (CLM-C16-10).
2. Count those of order 6; compare with L(n)/n².
3. Prove CLM-C16-13 and explain the Laver transient bound 5.
4. Which laws force short periods, beyond idempotency and anchored left-distributivity?
