# Skeptic review — batch 1.2 (cycle C05: spectra of the ETP laws x = y∗T)

Independent Mathematical Skeptic, 2026-10-20. I produced none of the results under review. Everything below was
checked by me; where I could not check something I say so (§8).

**Scope.** The original brief covered CLM-C05-15 to -21 as committed at `3c88c05`. The coordinator later added
CLM-C05-22 (Theorem 14, law 501), CLM-C05-23 (Lemma 7″, laws 704 and 883) and the refutation of CLM-C05-18. I
read those at `093d2bf`, `8e01251`, `d22d2e7` and `23b6176` (the HEAD when I finished). Other agents were
committing to the repository while I worked. Line numbers below refer to `23b6176`.

**Method and constraints.** I used one process at a time (EXP-C05-13 and -14 were running on the other cores),
about 25 CPU-minutes in all. My scripts and outputs are in
`/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/skeptic12/` (listed in §9). They
are outside the repository because the brief allowed me to change only this file. The independent encoder
(`indep.py`) does not import `systems.*`, `lab.*` or any experiment. Only three audit scripts import
`systems.magma_split`, and they do so on purpose: they rebuild the lab's CNFs, compare their hashes and test the
lab's encoding on known models.

## 0. Verdicts

| Claim | Verdict | Main evidence (this review) | Record change recommended |
|---|---|---|---|
| CLM-C05-15 (15 gaps at orders 8–10) | **UPHELD** | 13 of the 15 pairs re-decided with my own encoder, my own implementation of Lemma 8 with a different layout, and Glucose 4; every case UNSAT, with 1,045 Glucose DRUP proofs that drat-trim verified (§2). 501/10 also follows from Theorem 14, whose proof I checked (§5.1). 670/10 not re-decided (45 CPU-min in the lab). | proof_check: add the independent re-decision. |
| CLM-C05-16 (9 gaps at orders 11–13; spectra up to 13 of six laws) | **UPHELD WITH CORRECTIONS** | 1076/11, 1313/11 and 1279/12 re-decided independently (473 cases, all UNSAT, every proof verified). The 1,823 records of EXP-C05-10 are byte-identical to their checkpoint files. 27 checkpointed cases re-solved from scratch give identical results, and 25 rebuilt CNFs have identical hashes. Every member order is backed by an explicit table (§3.1). | The proof of Theorem 12 and the proof_check must say that the 1,797 target results come from checkpoints of earlier runs. Make the provenance airtight (§3.3). |
| CLM-C05-17 (spectra up to 10 of 13 laws) | **UPHELD WITH CORRECTIONS** | Every one of the 117 entries was audited (§3.1): all 72 gaps are certified, and 44 of the 45 members have an explicit table that I re-checked. **501 at order 8 had no stored table**: EXP-C05-03 stores none, 501 has no linear model of order 8, and products are impossible. It is now covered by the construction of EXP-C05-15, which I rebuilt, and by my own SAT model (§9). | proof_check (record.yaml:296) and C05.md:267 name EXP-C05-03 as a source of tables, but it has none. Cite EXP-C05-15 or a stored table for 501/8, and EXP-C05-04 (Lean) or the product 2 × 5 for 883/10. |
| CLM-C05-18 (refuted) | **refutation UPHELD** | My own evaluator checks the order-6 table of law 474. Law 474 has no model of order 2 (all 16 tables tried). The Lean table `E474_order6` is the same as the table in the record. | none |
| CLM-C05-19 (laws x = y∗(S∗y) have only quasigroup models) | **UPHELD** | Proof read line by line. I compiled `C05_QuasigroupLaws.lean` (exit 0, standard axioms only). The six instances match the ETP equations (checked against the ETP equation list). | none |
| CLM-C05-20 (677 at order 12 ⇔ one of 57 CNFs is satisfiable) | **UPHELD** | I re-derived every count and both structural consequences from EXP-C05-11 (§3.2). 25 rebuilt CNFs have identical hashes. | none (optional: archive the 57 CNFs, §7 P9) |
| CLM-C05-21 (conjecture: no model of order ≡ 2 mod 4) | **stays CONJECTURE**, no counterexample | The affine search over Z_14, Z_18, Z_22, Z_26 and Z_6 × Z_3 found nothing, and **can never succeed**: such a model would have a quotient of order 2 (§4). An orbit-SAT search at order 14 with prescribed automorphisms found no model (§4). | limitations (record.yaml:337): fix one sentence and add the quotient remark (§7 P6). |
| CLM-C05-22 (spectrum of 501 = {n ≡ 0, 1 mod 4}) | **UPHELD** (minor wording) | Every step of the written proof checked (§5.1). I compiled `C05_Law501.lean` (exit 0, standard axioms only) and read it against the paper. I rebuilt the construction my own way for all 50 orders up to 100, and checked the sign identity on every semi-symmetric quasigroup of orders 2–5 and on 227 more. The identity is a special case of a general parity relation for Latin squares (§5.1, remark). | wording (§7 P7); novelty: the Historian should check the Latin-square parity literature. |
| CLM-C05-23 (704 and 883 are quasigroup laws) | **UPHELD** | Both arguments checked. The Lean statements say what the claim says, and the file compiles. | none |

Nothing is refuted. **I found no unsound clause, off-by-one or wrong variable in the encoding** (§1). The
corrections concern evidence and provenance, not mathematics.

---

## 1. Soundness of the encoding (task 1)

Code read: `systems/magma.py` (`MagmaSAT`, `_encode`), and in `systems/magma_split.py` the functions `build`
(l. 97–147), `canonical_form` (l. 150–179), `admits` (l. 182–192), `solve_case` (l. 201–252) and `decide`.

**(a) Completeness of the case split (Lemma 8).**
* `cases(n)` (l. 55–59) lists the idempotent cases (λ, 1) with 1 ∈ λ and the non-idempotent cases (λ, ℓ) with
  ℓ ∈ set(λ) and ℓ ≥ 2. In total that is Σ_{k<n} p(k) cases. I counted the cases with my own partition
  generator: 45, 67, 97, 139, 195 and 272 for n = 8, …, 13, the same as the lab.
* `canonical_permutation` (l. 62–71) puts 0 in the first cycle, of length ℓ, as 0 → 1 → … → ℓ−1 → 0, and the
  remaining parts follow in the order of λ. In the idempotent case ℓ = 1 gives 0∗0 = 0; in the other case
  0∗0 = 1 ≠ 0. Both are correct.
* The relabelling argument of Lemma 8 is correct. If L′_{σa} = σ L_a σ⁻¹ and σ maps the cycles of L_a onto
  consecutive blocks, with the cycle orders respected, then L′₀ = π(λ, ℓ). The order of the other blocks does
  not matter.
* Fixed-point bounds (l. 114–120). Let k = λ.count(1) = fix(0). In the idempotent case the CNF has the unit
  clauses a∗a = a and "≥ k entries a∗b = b" for every a ≥ 1. In the other case every clause of the
  seqcounter at-least-k encoding gets the extra literal v[a,a,a].
  * The disjunction is exact. If v[a,a,a] holds, every clause is satisfied. If it does not, the remaining
    clauses are the cardinality encoding over fresh auxiliary variables, which is satisfiable iff the bound
    holds. The auxiliary variables are fresh for each a, because they come from the shared `IDPool`. I
    checked that no literal exceeds `pool.top` on 75 rebuilt CNFs.
  * The bounds are implied. In case 1, fix(a) is minimal among all elements. In case 2, fix(a) is minimal
    among the non-idempotent elements, and row 0 is fixed.
* The paper text of Lemma 8 (C05.md:150–181) matches the code.

**(b) Division clauses (l. 121–142).** The top clause, y∗a = x → T(x,y) = a, is implied by the law and the
injectivity of L_y. The descent then works as follows:
* Node A∗B with A a variable: the clause is "node = t ∧ A∗b = t → B = b". It is sound because rows are
  always Latin (Lemma 1, Lean `left_mul_bijective_of_law'`).
* Node A∗B with B a variable: the clause is "node = t ∧ a∗B = t → A = a". It is added only when `cols` holds,
  which means T = S∗y (Lemma 7′, Lean) or `part="quasigroup"`. The test in `columns_bijective` is T[1] == "y".
* The loop stops when both children are variables or both are compound.
* The w-variables in these clauses are the same variables as in the law encoding (`_encode` returns the
  existing block), so the clauses constrain the real subterm values.

I traced the descent for all 13 laws:
* 883 and 907 get only the top clause.
* 467, 501 and 704 descend through left factors.
* The six laws x = y∗(S∗y) descend three levels.
* 670 and 677 stop at (xy)y and (yx)y, unless `part="quasigroup"` is set.

Lemma 9 in the paper (C05.md:183–190) treats only 677 and 1313. The generalisation is stated in prose (C05.md:233
ff.). It is sound by the same argument; see §7 P8.

**(c) `part`.** Setting `part="quasigroup"` adds Latin columns and the column division clauses. Every clause is
implied for quasigroup models, so this part is sound for them. Setting `part="non-quasigroup"` adds `missing[b,c]
→ ¬v[a,b,c]` for all a, together with the clause ⋁ missing. With Latin rows, a magma fails to be a quasigroup
exactly when some column misses a value, so this part is complete for non-quasigroup models. The two parts
together cover the case. The assertion that rejects `non-quasigroup` for the laws x = y∗(S∗y) is correct.

**(d) `canonical_form` / `admits`.**
* `canonical_form` picks the first element with the fewest fixed points, among all elements when the model is
  idempotent and among the non-idempotent elements otherwise. It relabels so that row 0 equals
  `canonical_permutation(λ, ℓ)`; the other cycles are sorted by length in decreasing order, as in λ.
* `admits` builds the CNF of that case with `part=None`, so it covers every extra clause. It then solves with
  every v fixed to the relabelled table. The result is true iff the model satisfies the CNF of its case, which
  is what the docstring says.
* One minor point. The test `test_canonical_form_is_invariant_under_relabelling` (tests/test_magma_split.py:33–44)
  asserts that the case is invariant under relabelling. That is not true in general: tied minimisers can have
  different cycle types. The test passes only because the rows of linear models all have the same cycle type
  (§7 P10).

**Empirical test of the lab's encoding against every known model.**
* My encoder enumerated every labelled model of all 13 laws at orders 4, 5 and 7: 9,232 tables, which give 173
  distinct relabelled tables.
* I added 13 models of orders 8–9: my own models and the lab's control models.
* The lab's `admits` accepts all of them, with zero exclusions (`lab_admits.json`).
* At orders 2–4, and at order 5 for the Latin-square laws, my encoder's model sets are identical to brute force
  (§2).

**Results files.** I also checked the bookkeeping:
* For every pair in EXP-C05-09 and -10, the records are exactly the cases in the fixed order of `cases(n)`, a
  prefix of it when a model was found.
* 25 records from each of EXP-C05-09, -10 and -11, chosen at random, rebuild with the *current* `build` to the
  same SHA-256 and clause count. The `part` option added in `2f34d7a` leaves `part=None` CNFs unchanged.
* drat-trim prints `s VERIFIED` only after it derives the empty clause or the formula is trivially UNSAT.
  "s NOT VERIFIED", "s TIMEOUT" and "s DERIVATION" never match the test at l. 242.

**Verdict on task 1:** sound and complete as claimed. I found no off-by-one, no wrong variable and no clause that
excludes a legitimate model.

## 2. Independent re-decisions (task 2)

**My encoder** (`indep.py`), written from the paper text.
* Own parser and evaluator, with the laws typed in from the brief. The ETP numbers were checked against the
  downloaded ETP `equations.txt`.
* Every compound subterm gets exactly-one value variables per (x, y), defined in both directions; depth-1
  subterms use the table variables directly.
* No Lemma-9 clauses. Their effect follows by unit propagation from the reverse definition clauses and the
  Latin AMO clauses, but nothing depends on them.
* Latin rows, and Latin columns only for T = S∗y. Each is ALO plus pairwise AMO.
* Lemma 8 re-implemented with a different layout of row 0: the other cycles in *increasing* length, every cycle
  traversed *downwards*. My canonical relabelling picks the *last* minimiser.
* My own sequential counter for "≥ k fixed points", guarded by a∗a = a.
* Solver Glucose 4 (pysat `g4`), not CaDiCaL. For every UNSAT case the DRUP proof was checked by drat-trim; this
  is the same binary the lab uses (§8).

**Validation** (`test_indep.py`).
* At n = 2 and 3, the model sets of my plain encoder equal brute force over all n^(n²) tables.
* At n = 4 they equal brute force over all 331,776 Latin-row tables.
* At n = 5, for the six laws x = y∗(S∗y), they equal brute force over all 161,280 Latin squares.
* Every model of order 4 or 5 of every law is accepted by the CNF of its own case in my split.
* Every solution of every case CNF at n = 4 and 5 satisfies the law.
* The small spectra agree with CLM-C05-17 (for example 907: 3 yes, 4 and 5 no; 1286: none up to 5).

**Results.** Each run is one process. The time includes drat-trim; the lab's time is solve time only.

| pair | my verdict | cases run / total | DRUP proofs verified | my conflicts (total; hardest case) | my time (s) | lab verdict (source) | lab conflicts | lab solve s |
|---|---|---|---|---|---|---|---|---|
| 670/8 | no model | 45/45 | 45/45 | 19,427; 3,255 | 7.2 | no model (EXP-C05-09) | 44,610 | 5 |
| 907/8 | no model | 45/45 | 45/45 | 3,486; 557 | 13.3 | no model (EXP-C05-09) | 16,872 | 4 |
| 1286/8 | no model | 45/45 | 45/45 | 731; 229 | 7.8 | no model (EXP-C05-09) | 2,457 | 3 |
| 1076/9 | no model | 67/67 | 67/67 | 2,498; 1,549 | 11.9 | no model (EXP-C05-09) | 4,698 | 4 |
| 883/9 | no model | 67/67 | 67/67 | 192,295; 23,828 | 55.9 | no model (EXP-C05-09) | 448,150 | 47 |
| 1083/9 | **model** (my case 22) | 22/67 | 21/21 | 5,497; 3,720 | 6.2 | model (EXP-C05-09 control) | 261 | 0 |
| 1110/9 | **model** (my case 42) | 42/67 | 41/41 | 461; 182 | 10.1 | model (EXP-C05-09 control) | 9,637 | 6 |
| 1279/10 | no model | 97/97 | 97/97 | 31,617; 2,896 | 37.1 | no model (EXP-C05-09) | 24,942 | 10 |
| 1110/10 | no model | 97/97 | 97/97 | 40,205; 6,037 | 35.9 | no model (EXP-C05-09) | 43,371 | 13 |
| 1083/10 | no model | 97/97 | 97/97 | 388,887; 98,936 | 84.1 | no model (EXP-C05-09) | 382,031 | 47 |
| 1286/10 | no model | 97/97 | 97/97 | 37,829; 6,185 | 26.8 | no model (EXP-C05-09) | 78,728 | 15 |
| 1076/10 | no model | 97/97 | 97/97 | 21,742; 6,980 | 23.4 | no model (EXP-C05-09) | 31,226 | 12 |
| 467/10 | no model | 97/97 | 97/97 | 343,431; 43,622 | 50.1 | no model (EXP-C05-09) | 112,417 | 16 |
| 704/10 | no model | 97/97 | 97/97 | 135,037; 11,145 | 33.8 | no model (EXP-C05-09) | 180,566 | 21 |
| 907/10 | no model | 97/97 | 97/97 | 714,295; 67,095 | 137.9 | no model (EXP-C05-09) | 1,450,218 | 135 |
| 1076/11 | no model | 139/139 | 139/139 | 147,348; 47,719 | 66.5 | no model (EXP-C05-10, checkpoint) | 142,005 | 28 |
| 1313/11 | no model | 139/139 | 139/139 | 464,322; 58,436 | 124.3 | no model (EXP-C05-10, checkpoint) | 445,887 | 69 |
| 1279/12 | no model | 195/195 | 195/195 | 801,772; 25,419 | 194.7 | no model (EXP-C05-10, checkpoint) | 433,943 | 116 |
| 501/6, 501/7 | no model | 19/19, 30/30 | not logged | 479; 2,702 | 0.5 | no model (EXP-C05-12) | – | – |
| 501/8 | **model** (table in §9) | 35/45 | not logged | 11,004 | 0.8 | no stored table (§3.1) | – | – |

* Both models (1083/9 and 1110/9) were re-checked on the law with my own pure-Python evaluator.
* Every UNSAT answer in the table carries a Glucose DRUP proof that drat-trim verified, except 501/6 and 501/7,
  which I ran without proof logging.
* **CLM-C05-15 coverage.** 13 of the 15 pairs (all except 501/10 and 670/10) were decided independently, with
  the same answer and with proofs. 501/10 also follows from Theorem 14.
* **CLM-C05-16 coverage.** 3 of the 9 pairs were decided independently.

## 3. Evidence audit (task 3)

### 3.1 Every entry of the spectrum tables (`audit.py`, `audit.json`)

**Members.** For each member order (law, n) of CLM-C05-17 (n ≤ 10) and CLM-C05-16 (n ≤ 13), I looked for an
explicit table and re-checked each one on the law with my own evaluator. The sources were:
* the stored models of EXP-C05-12, -09, -10 and -08;
* the Lean certificates of EXP-C05-04;
* linear models x∗y = ax + by over my own GF(q), for q ≤ 16;
* products that I rebuilt: 883 = 2 × 5 and 2 × 4, and 1083 = 3 × 4.

My lists of linear orders for q ≤ 16 equal those of EXP-C05-07 for all 13 laws. Over GF(11) and GF(13) I find
exactly the 20 linear models of the six laws x = y∗(S∗y) that EXP-C05-10 lists. Every stored table satisfies its
law.

**Gaps.** Every gap order has a certified record:
* EXP-C05-12 for n ≤ 7;
* EXP-C05-08 for 677 and 1313 at 8 and 10;
* EXP-C05-09, targets and controls, for the other orders 8–10;
* EXP-C05-10 for 11–13.

Each EXP-C05-09/-10 verdict "no model (every case certified)" has the full set of records, all UNSAT and
VERIFIED. No member order carries a certificate of a gap, and no gap order has a model.

**One problem.** **501 at order 8** (CLM-C05-17) had no explicit table in any results file.
* EXP-C05-03 found a model but stores none. Its results have no tables, although CLM-C05-17's proof_check
  (record.yaml:296) and C05.md:267 cite EXP-C05-03 as a source.
* 501 has no linear model of order 8: EXP-C05-07 and my GF(8) both give none.
* No product works, because 501 has no model of order 2.
* The case split never ran 501/8.

The fact itself is true. My SAT search found a model, re-checked (§9). The Theorem 14 construction of
EXP-C05-15, which I rebuilt, gives another. EXP-C05-15 stores only booleans, but its tables are deterministic
code. Fix: cite EXP-C05-15 (or a Lean `decide` certificate of order 8) for 501/8, and drop EXP-C05-03 as a
source of tables.

Also, C05.md:267 lists sources only for the members at n = 8 and 9. 883 at 10 comes from the Lean certificate
`E883_order10` (EXP-C05-04) and from the product 2 × 5; please name it.

### 3.2 Counts quoted in the claims and the paper

All of the following match the JSON (my own sums):
* **EXP-C05-09:**
  * 1,532 cases run, 1,522 verified UNSAT, 128,449,196 proof lines, 0 UNKNOWN, 0 rejected.
  * Hardest case 1,651,622 conflicts (670/10).
  * Targets: 1,239 CNFs and 124.2 million lines.
  * Controls 13/13: 3 gaps, 10 members.
  * Every per-law entry of Theorem 11's table (cases per order, hardest conflicts) is correct.
* **EXP-C05-10:**
  * Targets: 1,797 cases, 206.26 million lines. With the controls: 1,823 cases run, 1,821 UNSAT.
  * Hardest case 812,068 conflicts (1110/13).
  * 21 of 21 known models admitted.
  * The model of the decision controls 1110/11 and 1279/11 lies in idempotent case (5, 5, 1). This is case
    *index* 12, 0-based; the log says "after 13 of 139 cases".
  * The model of 1083/12 lies in case index 189.
* **EXP-C05-11:**
  * 195 cases: 138 UNSAT, all verified, 10,513,763 lines; the maximum among the UNSAT cases is 196,580
    conflicts.
  * 57 UNKNOWN: 14 idempotent and 43 non-idempotent.
  * The 14 are *exactly* the idempotent cases with λ.count(1) = 1; there are p(11) − p(10) = 14 of them.
  * All 43 have ℓ ≥ 4 and at most 2 fixed points. 48 non-idempotent cases satisfy that condition, and the
    other 5 were refuted, so the condition is necessary, not a characterisation, which is how CLM-C05-20
    states it.
  * The probe log `g4/probe677_12.log` confirms that case (11, 1) was UNKNOWN at 3,000,002 conflicts.
* **EXP-C05-12:** 78 pairs, 50 gaps, 28 members, 0 disagreements. All 28 stored models re-checked by me.
* **EXP-C05-15:** 50 of 50 constructions, 39 sampled quasigroups (3 + 6 × 6), and the order-12 model
  (idempotent, not a quasigroup). The order-12 model equals the Lean table `E501_order12`.

### 3.3 EXP-C05-10 read 1,797 of its 1,823 results from checkpoints: judgement

**What I verified.**
* All 1,823 records in `results/EXP-C05-10.json` are identical, field by field, to the checkpoint files in
  `scratchpad/g4/e10_checkpoint/`, keyed by `{cnf_sha256}_4000000.json`.
* The 11 extra checkpoint files there are the dropped 1083/12 control (9 UNSAT) and 1313/14: case (13, 1) was
  UNKNOWN at 4,000,000 conflicts after 1,551 s, and case (12, 1, 1) was UNSAT. Both match the record's account.
* 27 checkpointed cases, two random and one of about 30k conflicts per target pair, were re-solved *from
  scratch* with the lab pipeline. Each had the same hash, the same status and the *same conflict count*, and
  drat-trim VERIFIED.
* 25 random E10 CNFs rebuild to the same hashes with today's code.
* Three of the nine pairs were re-decided independently (§2).

**Judgement.** The reuse is acceptable as evidence for a computer-assisted theorem at the lab's standard, for
four reasons:
* The checkpoint key is the SHA-256 of the exact CNF text, so a result can only be reused for the identical
  CNF.
* `solve_case` did not change in substance between the runs.
* The solver is deterministic, as the samples show.
* The reuse is disclosed in the record (record.yaml:54) and flagged per case in `timings`.

**It is not airtight.**
1. The checkpoints live in a scratch directory outside the repository. They are mutable and unhashed. For 1,797
   cases the "drat_trim: VERIFIED" flag is attested only by JSON files written by earlier processes, not by the
   recorded run.
2. The DRAT proofs were deleted (magma_split.py:239), so the verification cannot be repeated without
   re-solving.
3. The checkpoints carry no provenance: no git head, no pysat or CaDiCaL version, no SHA-256 of the drat-trim
   binary, no timestamps and no drat-trim output line. Neither does the results `env`: drat-trim lives at the
   unversioned scratch path of magma_split.py:37.
4. The proof of Theorem 12 (C05.md:313–318) and CLM-C05-16's proof_check (record.yaml:283) do not mention the
   reuse.

**What would make it airtight**, in decreasing order of value:
* **(i)** One clean, uninterrupted recorded run of EXP-C05-10 without `EXP_CHECKPOINT`. The recorded solve and
  check times sum to about 9,900 CPU-seconds, about 1 h on three workers. Alternatively, `lab verify EXP-C05-10`
  with checkpoints disabled.
* **(ii)** If checkpoints stay:
  * write provenance into each checkpoint (git head, solver and pysat versions, drat-trim SHA-256, start and
    end time, the final drat-trim line);
  * refuse a checkpoint whose provenance does not match;
  * copy the checkpoint directory (small JSON files) to `results/artifacts/EXP-C05-10/`, with a SHA-256
    manifest referenced from the results;
  * in the recorded run, re-solve a random sample from scratch and report the agreement, as I did here.
* **(iii)** Keep compressed DRAT or LRAT proofs of the hardest cases, so they can be re-checked by a checker
  independent of drat-trim, such as cake_lpr.
* **(iv)** Make `lab check` warn on any result with `from_checkpoint` records.

The same points (ii)–(iii) apply to EXP-C05-12. It stores no per-case records at all
(experiments/C05/E12_small_orders_certified.py:43–45 keep only the verdict, `cases_run`, the model and the
proof-line total), so its 50 certified gaps cannot be audited case by case (no CNF hashes). Fix: store the
records as EXP-C05-09 does.

## 4. Falsification attempt for CLM-C05-21 (task 4) — `falsify.py`, `falsify_A.json`, `falsify_B14.jsonl`

**Affine search.** I tried x∗y = a·x + b·y + c over Z_14, Z_18, Z_22 and Z_26, for all a, c and every unit b
(rows must be permutations), for each of the 12 laws: 0 models, in 10 s. For Z_6 × Z_3 I checked the Z_2
quotient (below): no candidate.

**The affine search is provably empty.** Let G be any group of order n = 2m with m odd. Its elements of odd order
form a normal subgroup N of index 2: the Sylow 2-subgroup is cyclic, so G has a normal 2-complement. An
endomorphism cannot raise the order of an element, so N is *fully invariant*. Hence every operation of the form
x∗y = f(x)·c·g(y), with f and g endomorphisms and c ∈ G, induces a magma structure on G/N ≅ Z_2. That covers
x∗y = a(x) + b(y) + c over any abelian group. A homomorphic image satisfies every identity of the model, so it
would be a model of order 2, and none of the 12 laws has one. So **no affine or group-endomorphism construction
of any order ≡ 2 (mod 4) can refute CLM-C05-21**. More generally, every model of order ≡ 2 (mod 4) has no
congruence of index 2. Direct products cannot help either: a product has order ≡ 2 (mod 4) only if a factor has.

**A non-affine search.** I wrote my own orbit encoder (`orbit_search`): the table is invariant under a prescribed
permutation σ, and the law is imposed only on orbit representatives. I calibrated it first: it finds the linear
models of 1110 and 1279 at order 11 at once with σ = (10-cycle) + 1 fixed point. I then searched at order 14 for
each of the 12 laws, with a budget of 200,000 conflicts and no proofs:
* **σ of type (13, 1):** UNSAT for all 12 laws. No model of order 14 has an automorphism with this cycle type.
* **σ = two 7-cycles:** UNSAT for 467, 704, 1076, 1110, 1279, 1286 and 1313; UNKNOWN for 501, 670, 677, 907
  and 1083. 501 is now settled by Theorem 14.

Result: **no counterexample**, and the conjecture stands. These are solver answers without certificates. Order 18
and above were not tried (§8).

## 5. Additional items

### 5.1 CLM-C05-22 / Theorem 14: the spectrum of 501 is {n ≡ 0, 1 mod 4} — UPHELD

**Necessity, step by step (C05.md:370–391).**
* L_y is onto (x = y∗(…)), hence a permutation, so L□_y = L_y² is even. Correct.
* **Step 1.** x = y□(x□y) = L□_y(R□_y(x)), so L□_y ∘ R□_y = id. L□_y is a permutation, so R□_y = (L□_y)⁻¹,
  which has the same sign. Correct.
* **Step 2.** Write z = x□y. Law 14 at (y, z) gives y = z□(y□z), and y□z = y□(x□y) = x, so z□x = y. Then:
  * Φ(x,y) = (y, x□y);
  * Φ² = (x□y, y□(x□y)) = (x□y, x);
  * Φ³ = (x, (x□y)□x) = (x, y).

  So Φ is a bijection (Φ⁻¹ = Φ²) with cycles of length 1 or 3, and sgn Φ = +1. Correct.
* **Step 3.** τ∘P(x,y) = τ(x□y, y) = (y, x□y) = Φ(x,y). P maps the block M × {y} to itself, acting as R□_y, so
  sgn P = ∏_y sgn R□_y = +1. Hence sgn τ = sgn Φ · sgn P = +1. τ has n fixed points and n(n−1)/2
  transpositions. So n(n−1)/2 is even, that is, n ≡ 0 or 1 (mod 4). The sign bookkeeping is right.
* The general identity (∏_y sgn L□_y = (−1)^{n(n−1)/2} in every finite semi-symmetric quasigroup) also follows.
  Every finite model of law 14 is automatically a quasigroup, by the same argument.

**Sufficiency (C05.md:392–408).**
* y□(x□y) = −y + x + y = x, and L□_x is an involution.
* A permutation is a square iff, for each even length, it has an even number of cycles of that length. For an
  involution: iff it has an even number of 2-cycles. Also (a c b d)² = (a b)(c d). The "conversely" sentence is
  right too: a root of an involution has only cycles of length 1, 2 and 4.
* The fixed points of L□_x form the solution set of 2y = −x, which is empty or a coset of A[2].
* For Z_n with n odd: one fixed point and (n−1)/2 2-cycles, an even number iff n ≡ 1 (mod 4).
* For Z_2 × Z_2 × Z_{n/4}: the number of fixed points f is 0 or |A[2]|, which is 4 or 8. Both n/2 and (n−f)/2 are
  even. The paper's "n − f ≡ 0 mod 8" is true (n = 4m with m odd gives 4(m−1); 8 | n gives n − 8), though only
  n − f ≡ 0 (mod 4) is needed.
* Then x∗(x∗y) = σ_x²(y) = x□y and y∗(y∗(x□y)) = y□(x□y) = x. Correct.

**The Lean proof** (`C05_Law501.lean`, added in `d22d2e7`). I compiled it myself: exit 0, standard axioms only.
I read it against the paper:
* `Law501` is exactly x = y(y(x(xy))).
* `boxRight` takes its inverse to be (y □ ·). It is a permutation by the identities alone, with no finiteness
  needed.
* `phi_eq` is Φ = τ ∘ `prodCongrLeft` R□. The convention (b, a) ↦ (e a b, a) gives P(x, y) = (x□y, y), as in the
  paper.
* `sign_prodComm` uses `sign_of_pow_two_eq_one` with the fixed points identified with the diagonal.
* `law501_card_mod_four` assumes only `[Fintype α] [DecidableEq α]`, so it covers every finite magma.

This mechanises the necessity completely. The paper's Theorem 14 does not yet mention the Lean proof (§7 P7).

**Computations (`law501.py`, `law501.json`, about 3 s).**
1. **My own rebuild of the construction.** I paired the 2-cycles in a different order and used the opposite
   4-cycle orientation. For all 50 orders n ≡ 0, 1 (mod 4) up to 100 the table satisfies law 501. As sanity
   checks:
   * Z_n with 4 | n fails: some row has an odd number of 2-cycles.
   * Z_2 × Z_{n/2} also works for n = 8, 16 and 24.
   * The construction is impossible for n = 3, 6, 7, 10, 11 and 14.
2. **Structure of the known models.** I took every model of 501 at hand: my SAT models of orders 8 and 9, the
   lab's orders 4, 5 and 9, the order-12 Lean table, and my constructions of orders 4–17. In each one:
   * □ is semi-symmetric;
   * every row of □ is even;
   * R□_y = (L□_y)⁻¹;
   * Φ³ = id.
3. **The sign identity** ∏_y sgn L□_y = (−1)^{n(n−1)/2}. No violations on:
   * **all** labelled semi-symmetric quasigroups of orders 2, 3, 4 and 5 (2, 3, 18 and 120 tables, enumerated
     by my SAT encoder and cross-checked by brute force at n = 2, 3);
   * 25 random ones of each order 6–12;
   * the Steiner quasigroups of STS(7), STS(9), STS(13) and STS(15);
   * −x−y over 24 abelian groups of order at most 16;
   * 24 linear ones a·x + b·y over GF(q), with b³ = −1 and a = −b².
4. **Order 6, 7 and 11.** My encoder decides 501 at 6 and 7 as gaps. At order 11 my orbit search finds no model
   with an automorphism of type (10, 1) or (11). Neither result can break the theorem, and none did.

**Remark (for the Historian; it does not affect the verdict).** The sign identity is the semi-symmetric case of a
general parity relation for Latin squares. For any Latin square of order n, let:
* π_r be the product of the signs of the rows (c ↦ L(r,c));
* π_c be the product of the signs of the columns (r ↦ L(r,c));
* π_s be the product of the signs of the symbol permutations (r ↦ c with L(r,c) = s).

Then π_r·π_c·π_s = (−1)^{n(n−1)/2}. **Proof**, the paper's argument with three maps instead of Φ:
* f₁(r,c) = (r, L(r,c)) has sign π_r;
* f₂(r,s) = (c, s) has sign π_s;
* f₃(c,s) = (r, c) is the swap τ composed with (c,s) ↦ (c,r), so it has sign (−1)^{n(n−1)/2}·π_c;
* f₃f₂f₁ = id, which gives the relation.

In a semi-symmetric quasigroup, y□z = x ⇔ x□y = z ⇔ z□x = y. So the column permutations are the inverses of the
rows, and the symbol permutations are the rows. Hence π_r = π_c = π_s, and π_r = (−1)^{n(n−1)/2}. I checked the
general relation on 330 random Latin squares of orders 2–12 with no violation. I believe it is in the
literature on even and odd Latin squares, but I did not verify any citation. Candidate places to look are
Derienko (1988) and J. Janssen, "On even and odd Latin squares" (JCTA 1995). This bears on the novelty of the
*lemma*, not of the spectrum theorem.

**E15 code review** (experiments/C05/E15_law501_spectrum.py).
* The construction (l. 71–83), the 4-cycle (a c b d) with (a c b d)² = (a b)(c d), and the sign function are
  correct.
* The order-12 model is cases(12)[0] = idempotent (11, 1), SAT, and it re-checks on the law.
* Two small inaccuracies:
  * Item (d) of the docstring (l. 14) says the results agree with EXP-C05-03, -06, -09 and -12. The code (l. 108)
    reads only -12 and -09.
  * "all 39 semi-symmetric quasigroups of orders 3–9 that a SAT search enumerated" (C05.md:411–412 and the
    record) is the first ≤ 6 labelled models per order, not an enumeration. My exhaustive check at n ≤ 5 can
    stand in.

### 5.2 CLM-C05-23 / Lemma 7″: 704 and 883 are quasigroup laws — UPHELD

* **883:** x = y((xy)(yy)). For fixed y, x is a function of x∗y, so R_y is injective, hence bijective.
* **704:** x = y(y((xx)y)). For fixed y, x is a function of (xx)∗y, and so of xx; hence squaring S is injective,
  so bijective. Then x is a function of R_y(S(x)), so R_y∘S is injective and R_y is injective, so bijective.

The Lean definitions match the ETP equations: `Law704` is ∀ x y, y∗(y∗((x∗x)∗y)) = x, and `Law883` is
∀ x y, y∗((x∗y)∗(y∗y)) = x. The proofs follow the argument:
* `hinj` comes from the two-line calc;
* the `rw [hab]` rewrites only the intended subterm `op a a`;
* `law704_right_bijective` takes square roots through `hsq` and then `rfl`.

The file compiles. Left translations are bijective by the general `left_mul_bijective_of_law'`. A side remark:
EXP-C05-09 ran 704 and 883 with Latin rows only, which is sound and merely weaker. Latin columns could now be
added.

### 5.3 CLM-C05-18 refuted by law 474 — refutation UPHELD

* Law 474 is x = y(x(y(xy))), of the form y∗T (ETP equation 474, checked against the list).
* The order-6 table of the record satisfies it under my own evaluator, and none of the 16 tables of order 2
  does.
* The Lean `E474_order6` has the same rows, and `E474_no_order2` quantifies over all 16 tables.

## 6. `lab check` and `pytest` (task 5)

* **`python -m pytest -q tests/`** in the repository: **29 passed** in 1.5 s.
* **`python -m lab check`** in the live tree at about 16:25 gave **1 error**: a duplicate key `change_reason` at
  record.yaml:262 in CLM-C05-14. It came from an edit in progress by another agent. Because of it the C05 record
  did not parse, which produced 23 follow-on warnings ("db claim CLM-C05-xx is not in any record"), plus
  "EXP-C05-13/14 never run with recording".
* On a clean `git archive` export of `8e01251`: **0 errors, 2 warnings** (EXP-C05-13 and -14 not yet recorded;
  they are running).
* Commit `23b6176` then fixed the duplicate key. **Final runs at 16:39 UTC on HEAD `23b6176`** (with other agents' uncommitted edits to C05.md, CONTINUATION.md, the textbook and a report in the tree): `lab check` **0 errors, 2 warnings** (EXP-C05-13 and -14 not yet recorded), and `pytest` **29 passed**.

## 7. Problems found, with locations and fixes

| # | Severity | Location | Problem | Fix |
|---|---|---|---|---|
| P1 | evidence (CLM-C05-17) | record.yaml:296; C05.md:267 | The member 501/8 has no stored table, and EXP-C05-03 (cited as a source of tables) stores none. | Cite EXP-C05-15's construction (n = 8 is one of its 50 orders), or store a table or a Lean `decide` certificate (mine is in §9). Drop EXP-C05-03 as a table source. |
| P2 | evidence | C05.md:265–269 | Theorem 11(b) gives no source for 883 at order 10. | Add "883 at 10: Lean certificate E883_order10 (EXP-C05-04), also the product 2 × 5". |
| P3 | provenance (CLM-C05-16) | C05.md:313–318; record.yaml:283 | The proof does not say that 1,797 of the 1,823 results were read from checkpoints of earlier runs. | Add one sentence, and the airtightness steps of §3.3. |
| P4 | provenance | systems/magma_split.py:206–212, 239, 37 | Checkpoints are trusted without provenance or integrity checks. Proofs are discarded. The drat-trim binary is unversioned. | §3.3 (i)–(iv). Record the drat-trim SHA-256 in `env`. |
| P5 | auditability | experiments/C05/E12_small_orders_certified.py:43–45 | No per-case records (CNF hashes, conflicts, drat verdicts) are stored. | Store `records` as EXP-C05-09 does. |
| P6 | wording / limitations | record.yaml:337 (CLM-C05-21) | "the quasigroup laws 1076, 1110, 1279, 1286, 1313 none of order 10 (order 14 undecided)" repeats the first clause. | Say instead that every order up to 13 of these laws is decided (CLM-C05-16), so 14 is their first open order ≡ 2 (mod 4). Add: "a counterexample has no congruence of index 2, so no affine or group-endomorphism construction (any group of order ≡ 2 mod 4) can give one (Skeptic batch 1.2 §4)". |
| P7 | wording (CLM-C05-22) | C05.md:365–415; record.yaml:344 | The paper does not cite the Lean necessity proof `law501_card_mod_four` (an uncommitted edit adding it was in the working tree at 16:39). "Z_n (n odd)" in the statement should be "Z_n (n ≡ 1 mod 4)". "all 39 … that a SAT search enumerated" is a sample, not an enumeration. E15's docstring (l. 14) cites experiments the code does not read. | Edit the wording. Optionally add the Latin-square parity remark of §5.1 with an attribution check by the Historian. |
| P8 | written proof | C05.md:183–190, 233–240 | Lemma 9 states the division clauses only for 677 and 1313. The generalised descent of magma_split.py (left factor: L_A injective; right factor: R_B injective, Lemma 7′) is described only in prose. | Add a two-line Lemma 9′ with the general clause "N = A∗B, N(x,y) = t, A∗b = t ⇒ B(x,y) = b (A a variable)", and its mirror image. |
| P9 | reproducibility | CLM-C05-20; results/EXP-C05-11.json | The 57 hard CNFs are identified by SHA-256 of `build`'s output, which depends on pysat's encoders. It is pinned (requirements-lock.txt: python-sat==1.9.dev16), but a future pysat would change every hash. | Archive the 57 CNFs (gzip) in results/artifacts/EXP-C05-11/, or note the pin in the claim. |
| P10 | test quality | tests/test_magma_split.py:33–44 | The test asserts that the case is invariant under relabelling, which is false in general (tied minimisers). It passes because linear models have rows of one cycle type. | Rename it, or test the real property: the relabelled model satisfies the CNF of its case, which `admits` already does. |
| P11 | paper precision | C05.md:321, 327 | "case 12 of 139" and "case 189 of 195" are 0-based indices. | Write "case index 12 (0-based; the 13th case)". |

None of these changes a mathematical conclusion.

## 8. What I could not check

* **Not re-decided independently:** 670/10 (EXP-C05-09: 21 million conflicts, 45 CPU-min) and six of the nine
  EXP-C05-10 pairs: 1076/12, 1110/12, 1286/12, 1313/12, 1110/13 and 1279/13. These rest on the lab's
  checkpointed CaDiCaL runs with drat-trim, which I sampled (§3.3) but did not redo.
* **Shared checker.** My proof checks use the same drat-trim binary as the lab
  (`scratchpad/drat/drat-trim`, md5 e36d4648…). The independence is in the encoding, the case layout and the
  solver, not in the checker. I ran no second proof checker.
* **No proofs logged** for 501/6 and 501/7, nor for the orbit searches of §4 (budgeted solver answers).
* **Not tried:** order 18 and above for the falsification search, and automorphism types other than the two I
  tried at order 14.
* **Not reviewed:** EXP-C05-13 and EXP-C05-14 (running, not run by me), the textbook chapters, the reports, and
  novelty or literature. For the Latin-square parity remark the Historian should look.
* **Lean.** I compiled `C05_QuasigroupLaws.lean` and `C05_Law501.lean`. The certificates in `C05_Magmas.lean`
  (E474, E501_order12) I compared by eye with the records but did not compile; the lab records them as
  checked in `proofs/lean_results.json`.

## 9. Files, the 501/8 table, final runs

**Scripts and outputs.** All are under
`/tmp/claude-0/-home-user-ai-lab/5e93bf16-791a-5608-a61f-d865140bf384/scratchpad/skeptic12/`. They are not
copied into the repository; copying them to `reviews/skeptic_checks/batch1.2/` would preserve them.
* `indep.py`: my encoder and case split. It imports nothing from the repository.
* `test_indep.py` → `test_indep_report.json`: brute-force validation.
* `run_decide.py` → `redecide.jsonl` and `redecide_batch*.log`: the re-decisions of §2, case by case.
* `audit.py` → `audit.json`: the evidence audit of §3.1.
* `rehash.py` → `rehash.json`: hash rebuilds (imports `systems.magma_split` on purpose).
* `resample_e10.py` and `resample_e10_hard.py` → `resample_e10*.json`: re-solved E10 cases (lab pipeline, no
  checkpoint).
* `lab_admits_test.py` → `lab_admits.json`: the lab's `admits` on all my models.
* `falsify.py` → `falsify_A.json` and `falsify_B14.jsonl`: §4.
* `law501.py` → `law501.json`: §5.1.
* `summarize.py`: the table of §2.

**A model of law 501 of order 8** (rows 0–7; Latin rows, not a quasigroup). Found by my case split in case 35 of
45 and re-checked with my evaluator:

```
1 0 3 2 5 4 7 6
7 6 5 4 2 3 0 1
7 6 5 4 1 0 3 2
7 6 5 4 0 1 2 3
6 3 0 5 2 7 4 1
7 6 0 1 3 2 4 5
7 0 5 2 3 4 1 6
1 7 3 5 2 4 0 6
```

**Final runs** (16:39 UTC, HEAD `23b6176`): `python -m lab check` 0 errors and 2 warnings (EXP-C05-13/14 not yet recorded); `python -m pytest -q tests/` 29 passed. My computations used about 25 CPU-minutes, one process at a time.
