# Cycle C05 — Spectra of single-identity magma varieties

**Branch:** B (invented composition rules) · **Status:** complete
**Experiments:** EXP-C05-01 … EXP-C05-06 · **Claims:** CLM-C05-01 … CLM-C05-09
**Proofs:** `proofs/lean/Infinity/C05_Magmas.lean`, `proofs/paper/C05.md`
**Toolkit:** `systems/magma.py` (terms, identities, exact SAT encoding, isomorphism classes, affine models)

## Step 1 — Hypotheses

System B assumes nothing about a binary operation except that it is total.
Research question: *can a single invented identity t(x, y) = x — with no
other axioms — force arithmetic restrictions on the number of elements of a
finite model?*

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C05-1 | *(bold)* Every identity t = x has spectrum {1} or all n. | Inventor | **refuted** (law 167; 61 of 115 identities have restricted spectra on n ≤ 6) |
| H-C05-Q | *(bold)* Every nontrivial identity t = x forces its finite models to be quasigroups. | Inventor | **refuted** (a 4-element non-Latin model of law 167; 18 identities with non-quasigroup models of order ≤ 3) |
| H-C05-A | *(bold)* Full spectrum ⇔ affine models x∗y = ax + by + c over every ℤ_n (tested on n ≤ 6). | Inventor | **refuted** (x = (yx)(x(yy)): NAND is an order-2 model, no affine model over ℤ₂) |
| H-C05-2 | Restricted spectra are classical design spectra (Mendelsohn, Steiner, Euler's 36 officers…). | Explorer | partly supported |
| H-C05-3 | The open spectra of the ETP notes can be extended by SAT to n ≤ 12. | Verifier | see EXP-C05-03 |

## Step 2 — Definitions

Terms, identities, models, *spectrum* (set of orders of finite models),
*nontrivial* identities (x occurs in t but is neither its leftmost nor its
rightmost leaf — otherwise a projection is a model of every order, or only
n = 1 is possible) and the exact SAT encoding are in `proofs/paper/C05.md`
(Lemma 0). Identities are taken up to renaming; mirror images (t read
right-to-left) have equal spectra.

## Step 3 — Falsification design

* Exhaustive census of **all 115 nontrivial two-variable identities t = x
  with 2–4 operations**, SAT model existence for n = 1..7 (each UNSAT/SAT
  answer recorded; budgets bounded, UNKNOWN reported as such).
* Model enumeration up to isomorphism to test quasigroup forcing (H-C05-Q).
* Affine-model search over ℤ_n for every identity (H-C05-A).
* SAT with a *sound* implied constraint (rows of the Cayley table are
  permutations for laws x = y∗(…), Lemma 1) to push open ETP spectra to n ≤ 12,
  cross-checking every size already stated in the literature.
* Every satisfiable answer is re-verified in Python, and every new membership
  is re-certified by Lean's kernel (`decide`).

## Steps 4–5 — Implementation and execution

Reproduce with `python -m lab run --cycle C05` (EXP-C05-02/04/05/06 read the
results of earlier C05 experiments; EXP-C05-06 needs a `drat-trim` binary,
built from github.com/marijnheule/drat-trim with `gcc -O2`, path in
`DRAT_TRIM`). Lean: `proofs/lean/Infinity/C05_Magmas.lean`.

| Experiment | What it did | Outcome |
|---|---|---|
| EXP-C05-01 | all 115 nontrivial two-variable identities t = x (2, 15, 98 with 2, 3, 4 operations); SAT for n = 1..6 (budget 1e6); isomorphism classes for n ≤ 3 | 11 spectrum patterns: 52 full on 1..6, 2 with only n = 1 there, **61 restricted**; 1 UNKNOWN (law 167 at n = 6 — excluded by the Lean theorem); mirror pairs always agree; 18 identities have non-quasigroup models of order ≤ 3 |
| EXP-C05-02 | the 63 non-full identities: spectra extended to n = 7, 8 (sound row/column-permutation constraints, budget 5e5); all models up to isomorphism for n ≤ 5; a battery of 10 classical laws tested on every model | 15 patterns on 1..8 (table below); 52/63 identities have only quasigroup models for n ≤ 5; reproduces every spectrum fragment stated in the ETP notes for these laws |
| EXP-C05-03 | 15 laws with *unknown* spectrum in the ETP notes; SAT for n = 2..10 (budget 1e6), every model re-verified; comparison with every size stated in the notes | 0 disagreements with the notes; new facts in the Frontier table |
| EXP-C05-04 | Lean `decide` certificates for the memberships flagged by EXP-C05-03 | 9 tables re-solved, re-verified and emitted; all 9 checked by Lean's kernel |
| EXP-C05-05 | affine models x∗y = ax + by + c over ℤ_n, n ≤ 6, for all 115 identities | **H-C05-A refuted**: 4 identities (2 mirror pairs) are full on 1..6 but have affine models only of orders {1, 5} or {1, 2, 5}; 39 restricted identities have spectrum members without affine models; 0 inconsistencies |
| EXP-C05-06 | DRUP proofs (Glucose 4) checked by drat-trim for the non-memberships flagged by EXP-C05-03 | 48/48 refutations VERIFIED |

**Spectrum patterns on n = 1..8 (EXP-C05-02; 1 = model exists, 0 = none, ? = undecided within budget).**

| Pattern 1..8 | # | Representative (ETP number) | Small models (n ≤ 5) | Matches ETP notes / classical |
|---|---|---|---|---|
| 10111011 | 16 | y(x(xy)) = x (63, Dupont), y((xx)y) = x (115) | one class each at n = 3, 4, 5; medial quasigroups | 115: conjectured N∖{2, 6} |
| 10110010 | 4 | y(x(yy)) = x (66) | quasigroups (2 classes at n = 3, 4), not all idempotent: Mendelsohn systems twisted by the involutive squaring map | {0, 1 mod 3}∖{6} (proved, ETP) |
| 10110011 | 2 | y((x(yx))y) = x (1083) | quasigroups, not Mendelsohn | notes: contains 1,3,4,7,8,9 |
| 11011011 | 8 | y((xy)(yy)) = x (883) | quasigroups | notes: contains {1, 2 mod 3} |
| 10001011 | 8 | y(x(x(yy))) = x (467), y(y((xx)y)) = x (704) | quasigroups, medial | notes: starting 1,5,7,8 |
| 1000101? | 4 | y(x((yx)y)) = x (677), y(((yx)x)y) = x (1313) | idempotent quasigroups | 677: *no sizes in the notes* |
| 10001000 | 2 | y((x(xy))y) = x (1076) | idempotent quasigroups | notes: 1,5, not 6, 7 |
| 1010001? | 2 | y((yx)(xy)) = x (907) | Steiner quasigroup at n = 3 | notes: 1,3,7,9,13; not 2,4,5,6 |
| 10011001 | 2 | y(y(x(xy))) = x (501) | non-quasigroup models (15 classes at n = 4) | notes: contains 1,4,5,8,9 |
| 10011011 | 2 | y((y(xx))y) = x (1110) | quasigroups | notes: 1,4,5,7,8,9 |
| 100110?? | 2 | y(x((xy)y)) = x (670) | non-quasigroup models | notes: 1,4,5, not 6, 7 |
| 10011??1 | 1 | (yx)(xy) = x (167) | 58 classes at n = 4, non-quasigroups | {0, 1 mod 4} (Theorem 2) |
| 10101111 | 4 | y(x(y(xy))) = x (474) | non-quasigroups | N∖{2, 4} (ETP) |
| 10111111 | 4 | (yx)((xy)y) = x (1685) | some non-quasigroups | N∖{2} (ETP) |
| 1000001? | 2 | y(((xy)x)y) = x (1286) | none of order 2..6 | notes: starting 1, 7 |

## Step 6 — Analysis

* **A single invented identity can impose arithmetic on the size of the
  world.** More than half of the nontrivial identities with ≤ 4 operations
  forbid some orders; the forbidden sets are congruence conditions (mod 3,
  mod 4), finite exceptions ({2}, {2, 4}, {2, 6}) and sparse sets (law 1286:
  nothing between 2 and 6). Several coincide with classical design spectra:
  Mendelsohn (law 66), Steiner (law 907's small models are Steiner
  quasigroups), and the "Euler 36 officers" pattern N∖{2, 6} (law 115).
* **Mechanism.** Laws of the form x = y∗(…) make rows permutations
  (Lemma 1); the extra structure (idempotence, semisymmetry, mediality)
  visible in the small models is what produces congruence conditions, as in
  the orbit-counting proof for law 167.
* **Quasigroup forcing is not the explanation** (H-C05-Q refuted): laws 167,
  501, 670, 474 have non-quasigroup models yet restricted spectra.
* **Linear (affine) models do not explain full spectra** (H-C05-A refuted):
  NAND satisfies x = (yx)(x(yy)) although no affine operation on ℤ₂ does.
* **Defect noted.** EXP-C05-02's grouping of identities by "identical model
  sets" compared first-found representative tables rather than canonical
  forms, so its group count (58) is not meaningful and is not used.

### Frontier: open ETP laws pushed to n ≤ 10 (EXP-C05-03/04/06)

EXP-C05-03 decided, for 15 laws listed with unknown spectrum in Le Floch's
notes, every n ≤ 10 except the UNKNOWN entries below (budget 1e6 conflicts),
with **0 disagreements** with any size stated in the notes. Reading the
notes' phrase "starting with a, b, …" as settling every size up to the last
one listed, the facts **not stated in the notes** are:

| ETP law | New memberships (Lean-certified table, EXP-C05-04) | New non-memberships (DRUP proof checked by drat-trim, EXP-C05-06) | Still undecided (n ≤ 10) |
|---|---|---|---|
| 467 x = y(x(x(yy))) | 9 | — | 10 |
| 501 x = y(y(x(xy))) | — | 2, 3, 6, 7 | 10 |
| 677 x = y(x((yx)y)) | **5, 7, 9** (notes give no sizes) | **2, 3, 4, 6** | 8, 10 |
| 883 x = y((xy)(yy)) | — | 3, 6 | 9 |
| 1076 x = y((x(xy))y) | — | 8 | 9, 10 |
| 1083 x = y((x(yx))y) | — | 2, 5, 6 | 10 |
| 1286 x = y(((xy)x)y) | **9** | — | 8, 10 |
| 1313 x = y(((yx)x)y) | 9 | — | 8, 10 |
| 1516 x = (yy)(x(xy)) | 9 | — | 10 |
| 1719 x = (yy)((xx)y) | — | 2 (supports the notes' guess N∖{2}) | — |

Laws 670, 704, 907, 1110, 1279: everything we decided was already in the
notes (our UNKNOWNs: 670 at 8–10, 704 at 9–10, 907 at 8–10, 1110 at 10,
1279 at 9–10). Full per-size status: `results/EXP-C05-03.json`.

## Step 7 — Proofs, certificates and counterexamples

* **Lean** (`C05_Magmas.lean`, standard axioms only):
  `law167_card_mod_four` (every finite model of x = (yx)(xy) has order
  ≡ 0, 1 mod 4 — via a fixed-point-free involution on `Sym2`),
  `left_mul_bijective_of_law`, models `T4_law167`, `T5_law167`,
  `T4_not_latin` (refutes H-C05-Q), `no_law167_order2`, `no_law66_order2`,
  `nand2_law` + `no_affine_model_mod2` (refute H-C05-A), and nine frontier
  certificates `E467_order9_law`, `E677_order5/7/9_law`, `E883_order10_law`,
  `E1286_order9_law`, `E1313_order9_law`, `E1516_order9_law`,
  `E1719_order10_law`.
* **Written:** Lemma 0 (exact SAT encoding), Lemma 1 (path translations
  bijective), Lemma 4 (soundness of the added constraints)
  (`proofs/paper/C05.md`).
* **Computer-assisted, independently checked:** EXP-C05-06 re-solved all 48
  UNSAT instances flagged by EXP-C05-03 (a superset of the new
  non-memberships) with Glucose 4 proof logging; **drat-trim verified all 48
  DRUP refutations**. The trust base for a non-membership is then drat-trim,
  the CNF generator (Lemma 0, cross-checked against brute force) and the
  soundness of the added constraints (Lemma 4 / Lean
  `left_mul_bijective_of_law`). Other UNSAT entries of EXP-C05-01/02
  (e.g. in the pattern table) are solver-trusted only.

## Step 9 — Applications (Application Researcher)

* *Designs from one equation.* A single identity is a compact generator of
  combinatorial designs: solving law 66 or 907 by SAT produces Mendelsohn or
  Steiner-type systems, which underlie round-robin and tournament scheduling
  and experimental designs. This is a known approach (quasigroup
  constructions of designs); no benchmark against dedicated design
  algorithms was run.
* *A certification pipeline for finite algebra.* "SAT model → Lean `decide`
  certificate" and "SAT refutation → DRUP proof → drat-trim" removes the
  solver from the trust base for both directions of a spectrum question. It
  is reusable for any finite-model existence question in the lab.

## Step 10 — Documentation

`record.yaml` (claims, experiment interpretations, journal). Textbook:
Volume 2/3 chapter "One identity, many worlds: spectra of invented laws".

## Next directions

1. Decide the remaining sizes (law 1286 at 8 and 10; law 677 at 8, 10) with
   stronger symmetry breaking (fix the cycle type of row 0) and certify.
2. Conjecture-level patterns to test further: law 677 and 1313 spectra
   start 1, 5, 7, 9 (odd n ≥ 5?); law 1286 starts 1, 7, 9.
3. Order-5 laws and three-variable identities (the ETP notes treat order ≤ 4).
4. Formalise in Lean the general orbit-counting principle behind law 167
   for other laws with a "pair map" of finite order.

## Step 8 — Comparison with existing mathematics (Historian)

* **Spectra of order ≤ 4 laws were studied by the Equational Theories
  Project (ETP).** The write-up "Spectra of order-3 equations" (Lean Zulip,
  attributed in Le Floch's notes to Ben Gunby-Mann) proves: law 66,
  x = y(x(yy)), has spectrum {n ≡ 0,1 mod 3}∖{6} (Mendelsohn triple systems);
  law 167, x = (yx)(xy), has spectrum {n ≡ 0,1 mod 4}; law 168 (central
  groupoids, Knuth) has spectrum {k²}. B. Le Floch's notes "Spectrum of
  equational laws" (Lean Zulip, `spectrum.pdf`) treat all 741 classes of order
  ≤ 4 and list 48 laws with possibly non-full spectrum, many with "unknown
  spectrum starting with …". The ETP paper (arXiv:2512.07087, Sec. 9)
  separates full from non-full spectra and defers detailed spectra to a
  forthcoming publication.
* Hence the **census itself is a REDISCOVERY**: the patterns we found
  independently (before reading the notes) agree with the ETP knowledge.
  What this cycle adds: (i) a machine-checked (Lean) proof of the necessity
  half of the law-167 theorem; (ii) SAT-decided spectrum memberships for open
  laws at sizes the notes do not state, with Lean certificates for the
  memberships (EXP-C05-03/04); (iii) the refutations of H-C05-Q and H-C05-A in
  this family.
* Classical spectra used for comparison: Mendelsohn triple systems
  (v ≡ 0,1 mod 3, v ≠ 6; N. S. Mendelsohn 1971); Steiner triple systems
  (v ≡ 1,3 mod 6; Kirkman 1847); pairs of orthogonal Latin squares (all n
  except 2, 6; Bose–Shrikhande–Parker 1959–60); Stein quasigroups
  (Bennett–Mendelsohn, Bull. Austral. Math. Soc.).
