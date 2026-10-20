# Cycle C05 — Spectra of single-identity magma varieties

**Branch:** B (invented composition rules) · **Status:** complete
**Experiments:** EXP-C05-01 … EXP-C05-07 · **Claims:** CLM-C05-01 … CLM-C05-10
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
| H-C05-3 | The open spectra of the ETP notes can be extended by SAT (planned n ≤ 12, run to n ≤ 10). | Verifier | **supported**: 0 disagreements with the notes; new memberships and gaps in the Frontier table |

## Step 2 — Definitions

Terms, identities, models, *spectrum* (set of orders of finite models),
*nontrivial* identities (x occurs in t but is neither its leftmost nor its
rightmost leaf — otherwise a projection is a model of every order, or only
n = 1 is possible) and the exact SAT encoding are in `proofs/paper/C05.md`
(Lemma 0). Identities are taken up to renaming; mirror images (t read
right-to-left) have equal spectra.

## Step 3 — Falsification design

* Exhaustive census of **all 115 nontrivial two-variable identities t = x
  with 2–4 operations**, SAT model existence for n = 1..6, and n = 7, 8 for
  the non-full ones (budgets bounded, UNKNOWN reported as such).
* Model enumeration up to isomorphism to test quasigroup forcing (H-C05-Q).
* Affine-model search over ℤ_n for every identity (H-C05-A).
* SAT with a *sound* implied constraint (rows of the Cayley table are
  permutations for laws x = y∗(…), Lemma 1) to push open ETP spectra to n ≤ 10,
  cross-checking every size already stated in the literature.
* Every satisfiable answer is re-verified in Python, and every new membership
  is re-certified by Lean's kernel (`decide`).

## Steps 4–5 — Implementation and execution

Reproduce with `python -m lab run --cycle C05`; requirements and the
drat-trim build are in **Reproducibility** below. Lean:
`proofs/lean/Infinity/C05_Magmas.lean`.

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
| 1000101? | 4 | y(x((yx)y)) = x (677), y(((yx)x)y) = x (1313) | idempotent quasigroups | 677: *no sizes in the notes*; both have order-16 models (EXP-C05-07) |
| 10001000 | 2 | y((x(xy))y) = x (1076) | idempotent quasigroups | notes: 1,5, not 6, 7 |
| 1010001? | 2 | y((yx)(xy)) = x (907) | Steiner quasigroup at n = 3 | notes: 1,3,7,9,13; not 2,4,5,6 |
| 10011001 | 2 | y(y(x(xy))) = x (501) | non-quasigroup models (15 classes at n = 4) | notes: contains 1,4,5,8,9 |
| 10011011 | 2 | y((y(xx))y) = x (1110) | quasigroups | notes: 1,4,5,7,8,9 |
| 100110?? | 2 | y(x((xy)y)) = x (670) | non-quasigroup models | notes: 1,4,5, not 6, 7 |
| 10011??1 | 1 | (yx)(xy) = x (167) | 58 classes at n = 4, non-quasigroups | {0, 1 mod 4} (Theorem 2; it decides the two '?' - no models of orders 6, 7) |
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
with **0 disagreements** with any size stated in the notes. The facts **not
stated in the notes** — reading "starting with a, b, …" as settling every
size up to the last one listed, and taking into account the notes' lists of
laws without models of order 2 (or of order 3) and their Gaussian-integer
models of law 467 (all odd k² + l², k and l of different parities) — are:

| ETP law | New memberships (Lean-certified table, EXP-C05-04) | New non-memberships (DRUP proof checked by drat-trim, EXP-C05-06) | Still undecided (n ≤ 10) |
|---|---|---|---|
| 501 x = y(y(x(xy))) | — | 3, **6, 7** | 10 |
| 677 x = y(x((yx)y)) | **5, 7, 9** (notes give no sizes) | 3, 4, **6** | 8, 10 |
| 883 x = y((xy)(yy)) | — | **6** | 9 |
| 1076 x = y((x(xy))y) | — | **8** | 9, 10 |
| 1083 x = y((x(yx))y) | — | **5, 6** | 10 |
| 1286 x = y(((xy)x)y) | **9** | — | 8, 10 |
| 1313 x = y(((yx)x)y) | **9** | — | 8, 10 |
| 1516 x = (yy)(x(xy)) | **9** | — | 10 |

Bold: orders n ≥ 5. Gaps at orders 3 and 4 are new only relative to the
notes; ETP finite-magma searches probably settle them. Everything else we
decided was already in the notes: all of laws 467 (its certified order-9
model is covered by the notes' construction on ℤ[i]/(3), see
`proofs/paper/C05.md`, Remark 5), 670, 704, 907, 1110, 1279 and 1719, the
order-2 gaps of 501, 677, 1083 and the order-3 gap of 883. Further UNKNOWNs:
467 at 10, 670 at 8–10, 704 at 9–10, 907 at 8–10, 1110 at 10, 1279 at 9–10.
Full per-size status: `results/EXP-C05-03.json`. (Correction recorded in
journal C05-13: a first version of this table also counted 467 at order 9,
the order-2 gaps and 883's order-3 gap as new.)

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

**Batch 1.1 update (2026-10-19) — orders 8 and 10 of laws 677 and 1313.** EXP-C05-08 decides both
orders for both laws: no models (Theorem 10 of [proofs/paper/C05.md](../../../proofs/paper/C05.md)). A complete
case split (Lemma 8: idempotent or not, then the cycle type of the row of an element with the fewest fixed
points) gives 45 CNFs per law at n = 8 and 97 at n = 10; with implied division clauses (Lemma 9) and, for 1313,
Latin columns (Lemma 7 — finite models of 1313 are quasigroups, proved in Lean), all 284 are UNSAT and every DRAT
proof (40.5 million lines) was verified by drat-trim. So both laws have exactly the orders 1, 5, 7, 9 up to 10
(CLM-C05-12, CLM-C05-13). 677 at order 8 was already known — Mace4 exhausts size 8 (ETP paper,
[arXiv:2512.07087](https://arxiv.org/abs/2512.07087) §7.3.1) — so CLM-C05-11 is a rediscovery with a new
certificate. Law 677 is the premise of the ETP's last open finite implication, 677 ⇒ 255
([blueprint chapter](https://teorth.github.io/equational_theories/blueprint/677-chapter.html)); there is no
counterexample of order 8 or 10.

**Batch 1.2 update (2026-10-20) — "find more".** Plan and decisions:
[reports/PM_PLAN_batch1.2.md](../../../reports/PM_PLAN_batch1.2.md); proofs: Theorems 11-14, Proposition 13 and
Lemmas 7′, 7″ of [proofs/paper/C05.md](../../../proofs/paper/C05.md).

* `systems/magma_split.py` generalises the case split to every law x = y*T (13 of the 15 open laws), with the
  division clauses descending on both sides and, for laws whose models are quasigroups (Lean:
  `right_mul_bijective_of_law`, `law883_right_bijective`, `law704_right_bijective`), Latin columns.
* **Law 501 has exactly the orders n ≡ 0, 1 (mod 4)** (CLM-C05-22, EXP-C05-15): x□y = x(xy) is a semi-symmetric
  quasigroup with square translations, and a sign count on (x, y) ↦ (y, x□y) (order 3) forces n(n−1)/2 even;
  square roots of x□y = −x−y over Z_n or Z_2×Z_2×Z_{n/4} give the models.
* **New certified gaps:** 15 at orders 8-10 (CLM-C05-15, EXP-C05-09), 9 at orders 11-13 for the quasigroup laws
  (CLM-C05-16, EXP-C05-10), and 467, 704 at order 12 (EXP-C05-14). Spectra are now complete up to 10 for all 13
  laws (CLM-C05-17) and up to 13 for the six laws x = y*(S*y).
* **677 at order 12** (open in every source): 138 of 195 cases refuted (EXP-C05-11, CLM-C05-20); the other 57
  are split by right cancellation in EXP-C05-13.
* A general conjecture drawn from the data (no model of order 2 mod 4) was refuted by the census the same day
  (law 474, CLM-C05-18); the restricted form for the 12 laws is CLM-C05-21.

## Step 8 — Comparison with existing mathematics (Historian)

* **Spectra of order ≤ 4 laws were studied by the Equational Theories
  Project (ETP).** The write-up "Spectra of order-3 equations" (Lean Zulip upload;
  Le Floch's notes cite "Ben Gunby-Mann's notes" for law 167 — we take this
  to be that write-up) proves: law 66,
  x = y(x(yy)), has spectrum {n ≡ 0,1 mod 3}∖{6} (Mendelsohn triple systems);
  law 167, x = (yx)(xy), has spectrum {n ≡ 0,1 mod 4}; law 168 (central
  groupoids, Knuth) has spectrum {k²}. B. Le Floch's notes "Spectra of
  equational laws" (ETP, July 10, 2025; Lean Zulip, `spectrum.pdf`) treat all
  741 classes of order ≤ 4 and list 48 laws with possibly non-full spectrum —
  31 without models of order 2, 14 with models of order 2 but none of
  order 3 — many with "unknown spectrum starting with …". The ETP paper (arXiv:2512.07087, Sec. 9)
  separates full from non-full spectra and defers detailed spectra to a
  forthcoming publication.
* Hence the **census itself is a REDISCOVERY**: the patterns we found
  independently (before reading the notes) agree with the ETP knowledge.
  What this cycle adds: (i) a machine-checked (Lean) proof of the necessity
  half of the law-167 theorem; (ii) memberships and gaps for open laws at
  orders the notes do not state (Frontier table), certified by Lean
  (memberships) and drat-trim (gaps); (iii) the refutations of H-C05-Q and
  H-C05-A in this family.
* Classical spectra used for comparison: Mendelsohn triple systems
  (v ≡ 0,1 mod 3, v ≠ 6; N. S. Mendelsohn 1971); Steiner triple systems
  (v ≡ 1,3 mod 6; Kirkman 1847); pairs of orthogonal Latin squares (all n
  except 2, 6; Bose–Shrikhande–Parker 1959–60); Stein quasigroups
  (Bennett–Mendelsohn, Bull. Austral. Math. Soc.).

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
Chapter 6, `textbook/src/06_magma_laws.md` (Volume 2).

## Reproducibility

* **Python:** `systems/magma.py` needs `numpy` and `python-sat` (versions used:
  numpy 2.5.3, python-sat 1.9.dev16; model search uses CaDiCaL 1.5.3, proof
  logging Glucose 4). Budgets are conflict counts, so runs are deterministic
  for a fixed solver version; UNKNOWN entries may change with another version.
* **Order:** EXP-C05-02 and -05 read `results/EXP-C05-01.json`; EXP-C05-04 and
  -06 read `results/EXP-C05-03.json`. Recorded runtimes on the shared,
  heavily loaded container: 155 s, 670 s, 2796 s, 243 s, 9 s, 218 s for
  EXP-C05-01 … -06.
* **drat-trim** (only EXP-C05-06 needs it):

  ```bash
  mkdir -p ~/tools/drat && cd ~/tools/drat
  curl -sSfL https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c -o drat-trim.c
  gcc -O2 -o drat-trim drat-trim.c
  export DRAT_TRIM="$HOME/tools/drat/drat-trim"
  ```

  The source was taken from the `master` branch on 2026-10-18; the commit
  hash was not recorded. The file used has 1501 lines, header "Last edit:
  April 21, 2024", SHA-256
  `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`, and was
  compiled with gcc 13.3.0. EXP-C05-06 looks for the checker in `$DRAT_TRIM`,
  then `drat-trim` on `PATH`, then this session's scratchpad path (absent
  elsewhere); without a checker it records "checker unavailable" and
  certifies nothing.
* **pypdf** was installed (`pip install pypdf`) only to extract the text of
  the two ETP PDFs while reading the literature; no experiment or module
  imports it.

## Review (2026-10-18) and follow-up EXP-C05-07

The independent Skeptic review (`reviews/skeptic_C05_C08_C12.md`) upheld
CLM-C05-01 … 08 — its own CNF encodings, solved with CaDiCaL 1.9.5 and
Kissat 4.0.4, reproduce the 115-identity census and all 15 claimed gaps (the
13 gaps with n ≤ 6 even without the extra Latin-row and symmetry-breaking
constraints). It **refuted CLM-C05-09**: laws 677 and 1313 have models of
order 16, linear over GF(16). EXP-C05-07 then searched linear models over
every GF(q), q ≤ 128, for all 15 open laws (CLM-C05-10): 0 conflicts with SAT,
DRUP gaps or the notes; even orders for 14 of the 15 laws; law 670 at n = 9
settled. The blind spot was methodological: EXP-C05-05 tried affine models
only over ℤ_n, whose additive group is cyclic.

## Next directions

1. ~~Decide the remaining sizes up to 10~~ (done in batches 1.1 and 1.2). Next: law 677 at order 12 (the
   non-quasigroup parts of EXP-C05-13) and 14; 1313 at 14; 670 at 12, 13; 883 and 907 at 12 (hard cases above
   300,000 conflicts in the probes); law 1516 at 10 (shape x = (yy)*T, needs its own split).
2. Prove or refute CLM-C05-21 for the 11 laws other than 501; the sign argument of Theorem 14 needs a derived
   semi-symmetric operation whose translations have known signs, which the simple invariants (signs of rows,
   columns and squaring over all known models) do not provide.
3. ~~Test the conjecture spec(677) = spec(1313) = {1} ∪ {odd n ≥ 5}~~ —
   refuted by the Skeptic: both laws have linear models of order 16 over
   GF(16) (CLM-C05-09). Which odd orders occur is open (law 1286 starts
   1, 7, 9).
4. Order-5 laws and three-variable identities (the ETP notes treat order ≤ 4).
5. Formalise in Lean the general orbit-counting principle behind law 167
   for other laws with a "pair map" of finite order.
