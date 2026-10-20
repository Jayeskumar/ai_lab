# Skeptic review — batch 1.1 (CLM-C17-08, EXP-C05-08, CLM-C05-10, CLM-C19-15, new Lean files)

Independent Skeptic, 2026-10-20. I did not produce any of the results under review. Everything below was
checked by me; where I could not check something I say so. My scripts and small outputs are in
`reviews/skeptic_checks/batch1.1/`. None of them imports `systems/`, `lab/` or the experiment builders, except
`c05_e08_dimacs_check.py`, which imports the EXP-C05-08 builder *on purpose* (to re-generate the certified CNFs
and compare their hashes). Until the container restart at 01:03 UTC all runs used `nice -n 15`, one process at a
time; afterwards, as the coordinator allowed, at most three detached processes at `nice -n 10`, each writing
its results case by case.

## Verdicts

| Claim | Verdict | Evidence | Recommended record change |
|---|---|---|---|
| CLM-C17-08 (full anchor instance of LD has a model iff N is a power of 2, every N) | **UPHELD** | The Historian's row-period argument (b) is correct and complete up to routine details, which I wrote out (§1.2) and machine-checked: `C17_RowPeriod.lean` proves, for every N ≥ 1, "a model of the full instance on Fin N exists ⇔ N is a power of 2" from one explicit hypothesis, Laver's theorem (a model exists on every Fin 2^j); standard axioms only, no sorry. Laver's theorem is used only at 2^(v₂(N)+1). Numerically: all lemmas hold for N ≤ 1000 (whole table) and the block lemmas for all non-powers of 2 up to 4096. The literature chain (a) is logically valid as quoted. | verification COMPUTATIONALLY SUPPORTED → PROVEN; proof: the written proof of §1.2 (to be copied to C17.md) plus the Lean file (move to `proofs/lean/Infinity/` and register); proof_check: "written proof (Skeptic, reviews/skeptic_batch1.1.md §1.2) and Lean (C17_RowPeriod.lean: the iff for every N ≥ 1), conditional on Laver's theorem (published: A_n is left-distributive), which is also the input of CLM-C17-05"; limitations: replace the present text (N ≤ 4096; unread book results; awaiting review) by "conditional on Laver's theorem, used only at 2^(v₂(N)+1), an explicit hypothesis in the Lean file"; title: drop "computational here for N <= 4096". |
| CLM-C17-05 (anchor instance forces one table; Laver tables; N ≤ 4096) | **UPHELD** | `C17_ForcedTable.lean` states uniqueness, existence and the reduction to the wrap-around equations faithfully (§4). The bounded statement is now a special case of CLM-C17-08. | limitations: replace "the exclusion of non-powers of 2 is computational here (N <= 4096)" by a pointer to CLM-C17-08 (proved for every N). |
| CLM-C05-11 (677 has no model of order 8) | **UPHELD** | Lemma 8 (case split) and Lemma 9 (division clauses) are correct, and so is the encoding of "a∗a = a or ≥ k fixed points"; code review found no error (§2.1–2.3). Independent decision with my own aux-free encoding and a *different* case split (SB-min, §2.4): all 45 cases UNSAT, all 45 DRAT proofs verified by drat-trim. | proof_check: add "independently re-decided and DRAT-certified with a different encoding and case split (reviews/skeptic_batch1.1.md §2.4)". |
| CLM-C05-12 (677 has no model of order 10; orders ≤ 10 exactly 1, 5, 7, 9) | **UPHELD** | Lab: 97/97 cases UNSAT, all DRAT-verified (results file checked, §2.5). Independent, my own encoding (§2.4): (a) Lemma 8's split with my own division clauses, 97/97 UNSAT, all 97 DRAT proofs verified by drat-trim; (b) my SB-min split with tie-break R1, 97/97 UNSAT, all 97 DRAT proofs verified as well. The 401 CNFs the lab certified are byte-for-byte those of the reviewed builder (hashes). Sizes 2, 3, 4, 6 (EXP-C05-06, certified) and 5, 7, 9 (Lean tables) re-decided by my encoding. | proof_check: add "independently re-decided with a different encoding (and a second case split), DRAT-certified (reviews/skeptic_batch1.1.md §2.4)". |
| CLM-C05-13 (1313 has no model of order 8 or 10; orders ≤ 10 exactly 1, 5, 7, 9) | **UPHELD WITH CORRECTIONS** | Independent: order 8 UNSAT even with no symmetry breaking at all (Latin square only, 39 s); orders 8 and 10 with my SB-min split, 45 + 97 cases UNSAT, all DRAT-verified. Correction: the statement cites EXP-C05-03 for the gaps 2, 3, 4, 6, which are solver results there; the certificates are EXP-C05-06. | statement/proof_check: cite EXP-C05-06 (DRUP-certified) for the orders 2, 3, 4, 6; add the independent re-decision. |
| CLM-C05-14 (finite models of 1313 are quasigroups; Lean) | **UPHELD** | `C05_Law1313.lean` states exactly the ETP laws 1313 and 677 and proves left/right bijectivity; no sorry/axiom (§4). The cited sentence on non-right-cancellative finite models of 677 is in the ETP blueprint (§13.1: a construction from fields of sizes 16 and 31, "this gives a finite 677 magma that is not right-cancellative"; read on the web page, construction not checked). My SAT searches find no non-right-cancellative model of order ≤ 10: every model of 677 of order ≤ 10 is a quasigroup (§2.6; solver results, not certified). | none (the citation is correct; one could add that such a model needs order ≥ 11). |
| CLM-C05-10 (linear models over GF(q), q ≤ 128) | **UPHELD WITH CORRECTIONS** | Theorem 6 is correct. My own GF(q) arithmetic with a *different* modulus (last instead of first irreducible) and two methods (coefficients; brute-force evaluation of the whole table for all q² pairs (a, b)) reproduces every order list and every solution count of EXP-C05-07 for all 15 laws and all 44 prime powers q ≤ 128; 0 conflicts with SAT gaps, certified gaps or notes. Correction: the paper and proof_check say "every solution is re-checked on its full table"; EXP-C05-07 re-checks only the first solution per (law, q). | proof_check / C05.md Theorem 6: "one model per (law, q) re-checked in EXP-C05-07; all solutions re-checked by full-table evaluation in the Skeptic's independent computation (reviews/skeptic_batch1.1.md §3.1)". |
| CLM-C19-15 (deficit D(n) ≤ 1 + (t+1)(t+6)/2, L(n) = φ²n − O(log² n)) | **UPHELD** | The written steps not in Lean are correct (§3.2): the split phase reaches lazy(n) after Ψ(lazy(n)) moves (Theorems 1–2, both PROVEN and previously reviewed), continuing arbitrarily gives L(n) ≥ Ψ(lazy(n)), Ψ(Zeckendorf(n)) = B(n) by definition. My exhaustive longest games for n ≤ 100 (equal to the lab's L_exact) satisfy L(n) ≥ Ψ(lazy(n)) and D(n) ≤ B(n) − Ψ(lazy(n)) ≤ bound; Theorem 2 checked over all split sequences for n ≤ 60; the arithmetic bound for all n ≤ 10^5. Lean core faithful (indexing checked). | none. |
| CLM-C19-14 (O(log² n)-move method; Lean part) | **UPHELD** | Only the Lean citation was in scope: `deficit_bound` is exactly the arithmetic of the move bound; nothing else is claimed to be formalised. | none. |
| CLM-C10-07 (skew binary counting; Lean) | **UPHELD** | `C10_SkewBinary.lean` states the claim faithfully (canonical form, cost = changed positions, average with explicit O(log N/N) constant); no trivialising definition found (§4). | none. |
| CLM-C13-01 (structure of affine spectra; Lean) | **UPHELD** | `C13_AffineStructure.lean` states (a)–(f) faithfully; the uncovered remarks (resultant in the ideal; construction of G′) are disclosed in the proof_check (§4). | none. |

Nothing was REFUTED and I found no GAP.

---

## 1. CLM-C17-08 — the full anchor instance has a model iff N is a power of 2

### 1.1 What the row-period argument uses

Convention (the lab's, 0-based): F_N is the table on {0, …, N−1} forced by x⋆0 = x+1 (mod N) and
x⋆(y+1) = (x⋆y)⋆(x+1) for y ≤ N−2 (unique and existing for every N: `C17_ForcedTable.lean`). By
`full_instance_iff` and `forced_unique`, the full instance has a model of order N iff F_N satisfies the
wrap-around equations x+1 = (x⋆(N−1))⋆(x+1).

The surveys' 1-based convention is p = x+1 with all values shifted by 1 (p⋆1 = p+1, p⋆(q⋆1) = (p⋆q)⋆(p⋆1)).
"p⋆N = N" is "x⋆(N−1) = N−1", "row p" is "row x = p−1", and the Historian's c* ∈ {1..2^k}, c* ≡ c (mod 2^k), is
(y mod 2^k) + 1 with y = c−1. I checked this translation line by line against the Historian's text; it is
correct (the shift s is the same in both conventions, so "rows s+1..N−1" (1-based) are rows s..N−2 (0-based) and
"row s" (1-based) is row s−1 (0-based)).

The argument uses exactly these facts:

* **Elementary facts about F_N** (all N, no left-distributivity): row N−1 is the identity; every entry of a
  row x ≤ N−2 is > x (both Lean, `row_last`, `row_gt`); and the row structure of Lemma A below, which the
  Historian's sketch takes for granted.
* **One fact about Laver tables, at one order:** for B = 2^(k+1), k = v₂(N), the forced table F_B satisfies
  the wrap-around equations. In 1-based terms: u⋆B = B for every u in A_(k+1), equivalently every row period
  of A_(k+1) is a power of 2 (the periodicity statement the Historian read in Dehornoy–Lebed, Thm 1.1(ii); I
  did not read that source), equivalently A_(k+1) satisfies the full instance — which follows from
  "A_(k+1) is left-distributive", the existence of the finite Laver tables (the large-cardinal results about
  the growth of the periods are not used). The lab already relies on this published theorem in CLM-C17-05.

### 1.2 The complete proof (0-based)

**Lemma A (row structure; any N).** Let x ≤ N−2.
(a) If x⋆y ≤ N−2 and y ≤ N−2, then x⋆(y+1) > x⋆y (because x⋆(y+1) = v⋆(x+1) with v = x⋆y ≤ N−2, and
entries of row v exceed v).
(b) If x⋆y₀ = N−1 with y₀ ≤ N−2, then x⋆(y₀+1) = (N−1)⋆(x+1) = x+1 = x⋆0, and, by induction on j using the
recursion on both sides, x⋆(y₀+1+j) = x⋆j whenever y₀+1+j ≤ N−1.
(c) Row x reaches N−1 at some column ≤ N−2−x (by (a) it increases by at least 1 per step from x⋆0 = x+1
while it stays below N−1). Let y₀ be the first such column and π(x) = y₀+1. By (b), x⋆y = x⋆(y mod π(x)) for
all y ≤ N−1; within the first period the values are strictly increasing, so N−1 occurs there only at y₀.
(d) Hence x⋆(N−1) = N−1 iff (N−1) mod π(x) = π(x)−1 iff π(x) | N.

**Lemma B (wrap-around).** For x ≤ N−2, x+1 = (x⋆(N−1))⋆(x+1) iff x⋆(N−1) = N−1. (If v = x⋆(N−1) = N−1, row
N−1 is the identity. If v ≤ N−2, then v > x, so v⋆(x+1) > v ≥ x+1.) For x = N−1 the equation always holds.
This is Aguilera–Iannella's Prop. 2.5 and the Historian's [DERIVED] remark; with Lemma A(d): the full
instance holds iff every period π(x), x ≤ N−2, divides N.

**Input (L).** For B = 2^(k+1), F_B satisfies the wrap-around equations (Laver). Then by Lemma B and A(d),
π_B(u) | B for every u ≤ B−2, and π_B(u) ≤ B−1−u < B, so π_B(u) is a power of 2 that is ≤ 2^k, i.e. π_B(u) | m
with m = 2^k. Consequently

 (P) u⋆_B y = u⋆_B (y mod m) for all u ≤ B−2 and y ≤ B−1.

**Theorem.** Let N = m·r with m = 2^k and r odd, r ≥ 3 (i.e. N not a power of 2), B = 2m, s = N−B = m(r−2).
So s ≥ m ≥ 1 and m | s. Then

(i) x⋆_N y = s + (x−s)⋆_B (y mod m) for s ≤ x ≤ N−2 and 0 ≤ y ≤ N−1;
(ii) (s−1)⋆_N y = s + (y mod B) for 0 ≤ y ≤ N−1;
(iii) the wrap-around equation fails at x = s−1 (1-based p = s).

*Proof of (i).* Descending induction on x from N−2 to s; for fixed x, ascending induction on y. Put u = x−s,
so 0 ≤ u ≤ B−2. For y = 0: x⋆0 = x+1 = s+(u+1) = s + u⋆_B 0. Step y → y+1 (y ≤ N−2): let c = y mod m and, by
the induction hypothesis on y, w = x⋆_N y = s + u′ with u′ = u⋆_B c ∈ [u+1, B−1].
* Right-hand side. Since c+1 ≤ m < B and (y+1) mod m ≡ c+1 (mod m), (P) and the recursion of F_B at column
  c ≤ B−2 give u⋆_B((y+1) mod m) = u⋆_B(c+1) = u′⋆_B(u+1).
* Left-hand side: x⋆_N(y+1) = w⋆_N(x+1).
  - *Top element*, u′ = B−1: then w = N−1, so w⋆_N(x+1) = x+1 (row N−1 of F_N is the identity), and
    u′⋆_B(u+1) = u+1 (row B−1 of F_B is the identity); both sides are s+u+1 = x+1.
  - u′ ≤ B−2: then w ∈ [x+1, N−2] is a row already treated (descending induction), so
    w⋆_N(x+1) = s + u′⋆_B((x+1) mod m). Since m | s, (x+1) mod m ≡ u+1 (mod m), and (P) (u+1 ≤ B−1) gives
    u′⋆_B((x+1) mod m) = u′⋆_B(u+1).

*Proof of (ii).* Induction on y: (s−1)⋆0 = s. Step: (s−1)⋆(y+1) = (s + (y mod B))⋆_N s. If y mod B = B−1 this
is (N−1)⋆s = s = s + ((y+1) mod B). Otherwise s + (y mod B) ∈ [s, N−2] and by (i) it equals
s + (y mod B)⋆_B(s mod m) = s + (y mod B)⋆_B 0 = s + (y mod B) + 1 = s + ((y+1) mod B).

*Proof of (iii).* N = B(r−1)/2 + m, so (N−1) mod B = m−1 and, by (ii), (s−1)⋆(N−1) = s+m−1 = N−m−1 ≤ N−2.
By Lemma B the wrap-around fails at x = s−1. (In the Historian's words: π(s−1) = B, which does not divide N.) ∎

**Corollary (CLM-C17-08).** For N ≥ 1 the full instance has a model iff N is a power of 2: for N = 2^n the
Laver table A_n is one (Laver), and it is the only one (uniqueness); otherwise every model would be F_N
(uniqueness), which fails at x = s−1.

### 1.3 Check of the Historian's sketch

* **Shifted-copy claim (i), induction.** Correct as sketched (descending on rows, ascending on columns). Its
  two ingredients are the ones the Historian names (periods of the rows of A_(k+1) divide 2^k; s ≡ 0 mod 2^k).
  *Base cases:* column 0 (1-based c = 1) is the anchor on both sides; the descending induction needs no
  separate base row, because the top row of the block, x = N−2, only ever meets the top element (its
  entries are all N−1), which is the next point.
  *Top element:* when an entry of the block equals N−1, the recursion continues with row N−1 of F_N, which is
  not a shifted copy of row B−1 of F_B; it works because both rows are identities and the column used,
  x+1 = s+(u+1), is consistent with the shift: N−1 ⋆ (x+1) = x+1 = s + ((B−1)⋆_B(u+1)). The sketch does not
  mention this case; it is the only place where care is needed, and it goes through.
  *Columns beyond B:* (i) is claimed for all columns c ≤ N; the right-hand side uses only columns ≤ 2^k of
  A_(k+1), which is legitimate because of (P).
* **"Period of row s does not divide N ⇒ wrap-around fails at p = s."** Correct, but it needs two steps that
  the sketch leaves implicit: Lemma A (in F_N, which is not left-distributive, a row is still periodic with a
  period equal to the first index of the top element, so p⋆N = N iff the period divides N) and Lemma B
  (p⋆N ≠ N ⇒ the wrap-around fails, the Historian's item-1 remark). With them the conclusion follows.
* **(ii)** is correct: in 1-based terms row s is s+1, …, N (period B = 2^(k+1)) and 2^(k+1) ∤ N since v₂(N) = k.

So (b) is a complete and correct proof once Lemma A is stated; no idea is missing and nothing needs repair.

### 1.4 Machine check and numerical checks

* **Lean** (`reviews/skeptic_checks/batch1.1/C17_RowPeriod.lean`, compiled with the project's Lean 4.35 /
  Mathlib, 0 errors, 0 warnings; `#print axioms`: `[propext, Classical.choice, Quot.sound]`; no sorry,
  admit, native_decide or axiom). Main theorems:
  * `wrap_fails` (ℕ-level (i)–(iii): for any f, g with the properties `Forced N f`, `Forced (2m) g` and (P),
    N ≡ m mod 2m and N > 2m, the wrap-around fails at s−1);
  * `Forced.mod_half` (derives (P) from the wrap-around of F_B: period divides B, is < B, hence divides m);
  * `only_powers_of_two` and
    `full_instance_iff_pow_two (laver : ∀ j, ∃ op : Fin (2^j) → Fin (2^j) → Fin (2^j), (∀ x, op x 0 = x + 1) ∧ ∀ x y, op x (y + 1) = op (op x y) (x + 1)) (N) [NeZero N] : (∃ op : Fin N → …, anchor ∧ full instance) ↔ ∃ j, N = 2 ^ j`
    — in exactly the formulation of `C17_ForcedTable.lean` (the five Fin lemmas of that file are copied so
    that the file only imports Mathlib). The only non-Lean input is the hypothesis `laver`, i.e. the
    existence of the Laver tables, which is true (Laver; the full instance at 2^j is also checked numerically
    for 2^j ≤ 4096 by EXP-C17-03 and for 2^j ≤ 1024 by me).
* **Numerics** (`c17_row_period.py`, my own forced-table code): Lemmas A, B and "full instance iff power of
  2" on the whole table for every N ≤ 1000 and N = 1024; (i), (ii), (iii) and (P) for all 4,083
  non-powers of 2 with 3 ≤ N ≤ 4096 (including 3·2^10, 7·2^9, 15·2^8, 4095); 0 failures; 60 s.
  (Independent of the Historian's `laver_top_block.py`, which tests the same claims to N ≤ 1024 in the
  1-based convention.)

### 1.5 The literature chain (a), at the level of logic

As quoted: Prop. 2.5 (for a < N: a⋆N = N iff the instance holds at (a, N)); Lemma X.1.7 (S_N is
left-distributive iff a⋆N = N for every a ≤ N); Prop. X.1.6 (no left-distributive operation with a⋆1 = a+1,
N⋆1 = 1 unless N is a power of 2). If S_N satisfies the full instance, then a⋆N = N for a < N (Prop. 2.5) and
N⋆N = N (row N is the identity), so S_N is left-distributive (X.1.7) and N is a power of 2 (X.1.6). The chain
is valid. Its weak point is that X.1.6 and X.1.7 were read only as cited; Prop. 2.5 is elementary (it is my
Lemma B). Since (b) is now complete and machine-checked modulo Laver's theorem, the record no longer needs
the unread book results.

### 1.6 Verdict

PROVEN is justified, on proof (b) as completed in §1.2 (Lean: `C17_RowPeriod.lean`), conditional only on
Laver's theorem that A_n is left-distributive — the same published input as CLM-C17-05 — used at the single
order 2^(v₂(N)+1). Novelty stays REDISCOVERY (Biane's footnote; Aguilera–Iannella).

---

## 2. EXP-C05-08 — laws 677 and 1313 at orders 8 and 10 (CLM-C05-11, -12, -13, -14)

### 2.1 Lemma 8: completeness of the case split, and the conditional cardinality encoding

Let M be a model of order n; all left translations are bijections (Lean `law677_left_bijective`,
`law1313_left_bijective`).

* *Case 1 (M idempotent).* Pick a with fix(a) minimal. Since a∗a = a, a is a fixed point of L_a, so λ (the
  cycle type of L_a) has a part 1 and a lies in a 1-cycle. A bijection σ sending the cycles of L_a onto the
  cycles of π(λ, 1) of the same lengths, respecting cyclic order, with σ(a) = 0, conjugates L_a to π(λ, 1).
  In the relabelled model M′ (M′ ≅ M, so the law, Latin rows, Latin columns for 1313 and the division
  clauses still hold) row 0 = π(λ, 1), every element is idempotent, and fix′(σb) = fix(b) ≥ fix(a) =
  λ.count(1) for every b. All constraints of CNF (idempotent, λ, 1) hold.
* *Case 2 (some b∗b ≠ b).* Pick a with a∗a ≠ a and fix(a) minimal among such elements. L_a(a) ≠ a, so the
  cycle of a has length ℓ ≥ 2 and ℓ is a part of λ. Relabel as above with σ(a) = 0 (the cycle of a goes onto
  (0 1 … ℓ−1), so 0∗0 = 1). Every non-idempotent element of M′ has ≥ λ.count(1) fixed points; idempotent
  ones are unconstrained. All constraints of CNF (non-idempotent, λ, ℓ) hold.

So every model lands in some case, and conversely every satisfying assignment of any case CNF is a model
(the CNFs only add constraints to the exact encoding of the law). Lemma 8 is complete. The case counts are
right: n = 8 has 15 partitions with a part 1 and 30 pairs (λ, ℓ ≥ 2); n = 10 has 30 and 67 (I recomputed
the lists; the results file contains exactly these cases, §2.5).

*Row 0 excluded from the bound loop:* correct — row 0 is π(λ, ℓ), which has exactly λ.count(1) fixed points,
so the bound holds for it automatically (and in case 2 row 0 is non-idempotent, 0∗0 = 1).

*"a∗a = a OR at least k fixed points".* If C(X, Y) is a CNF whose projection ∃Y C(X, Y) is the
at-least-k constraint and whose auxiliary variables Y occur nowhere else, then
{c ∨ l : c ∈ C} ≡ l ∨ C, and ∃Y (l ∨ C(X, Y)) ≡ l ∨ ∃Y C(X, Y) because l does not mention Y. So adding the
literal v[a,a,a] to every clause encodes exactly "a∗a = a or ≥ k fixed points" — *provided* each row's
encoding has fresh auxiliary variables. I checked pysat 1.9.dev16's `CardEnc.atleast(..., vpool=...)`: it
starts from `vpool.top` and afterwards sets `vpool.top = ret.nv`, so every call gets fresh variables and the
later `IDPool.id` calls (value variables of `_encode`) cannot collide with them. (The seqcounter at-least-k is
at-most-(n−k) of the negated literals, a standard encoding.) Semantic test (`c05_e08_dimacs_check.py`): I
relabelled every linear model of orders 5, 7 and 9 of both laws by Lemma 8, once for *each* admissible choice of
the element sent to 0, and gave the table as assumptions to the lab's CNF of its case: all 66 relabellings are
accepted. They fall into 7 different cases, 5 of them non-idempotent with an active conditional bound, e.g.
(non-idempotent, (6,1), 6) for 677 at 7 and (non-idempotent, (3,3,1), 3) for 1313 at 7, so the
"v[a,a,a] ∨ seqcounter" clauses and the division clauses do not exclude genuine models.

### 2.2 Lemma 9 (division clauses) and Lemma 7 / Lean (Latin columns for 1313 only)

Write the law as x = y∗T. *Generic:* y∗a = x and y∗T = x give T = a (L_y injective). *677:* T = x∗S,
S = (y∗x)∗y; y∗b = x gives T = x∗S = b, and x∗a = b gives S = a (L_x injective). *1313:* T = S∗y, S = (y∗x)∗x;
y∗b = x gives S∗y = b, and a∗y = b gives S = a (R_y injective). All three families are implied by the law
plus bijectivity, so they remove no model. Latin columns are used for 1313 only, where Lean proves them
(`law1313_right_bijective`: for w, the element z = (y∗(y∗w))∗(y∗w) satisfies z∗y = w by the law at
x = y∗w and injectivity of L_y). For 677 only rows are used. Sound.

### 2.3 Code review of `experiments/C05/E08_orders_8_10.py`

* `canonical_permutation(lam, ell)`: removes one part ℓ and writes the cycles [ℓ] + rest on consecutive
  labels; 0 is in the first cycle, of length ℓ. Correct.
* Bound loop over a = 1..n−1, unconditional in the idempotent case, with the literal v[a,a,a] added
  otherwise. Correct (§2.1).
* Term decomposition: `parse("y(x((yx)y))")[1]` = x((yx)y) = x∗S with S = `T[1]` = (yx)y;
  `parse("y(((yx)x)y)")[1]` = ((yx)x)y = S∗y with S = `T[0]` = (yx)x. Correct. `sat._encode(T, asg)` and
  `sat._encode(S, asg)` return the *existing* value variables of the law's encoding (same key: term string
  and values of its variables in order of first occurrence), and those value variables are exact (Lemma 0:
  forward clauses plus at-most-one force them to the true value), so the division clauses constrain the
  real values of T and S. The clause shapes match Lemma 9 exactly.
* DIMACS: header `p cnf top m`, every clause terminated by 0. I re-generated, with the experiment's own
  `build()`, all 401 UNSAT CNFs of the results file (n = 5, 6, 7, 8 and 10, both laws) and wrote them exactly
  as `solve_case` does: every sha256 equals the recorded `cnf_sha256` (401/401), the largest literal never
  exceeds the header's variable count, and no clause is empty or contains 0. So the certified CNFs are exactly
  the CNFs of the reviewed code.
* drat-trim parsing: `"s VERIFIED" in stdout`. "s NOT VERIFIED" does not contain that substring. I ran the
  binary on a correct proof (`s VERIFIED`, exit 0), a wrong one and an empty one (`s NOT VERIFIED`, exit 1).
  Its lines start with a carriage return, which a `grep '^s '` would miss but the substring test does not.
  Any other outcome (timeout, crash) is recorded as NOT VERIFIED, which is conservative.
* Verdict logic: "no model" only if *all* cases of the order are UNSAT *and* VERIFIED; any UNKNOWN makes the
  order UNDECIDED; a SAT answer counts only if the table satisfies the law. The proof is checked against the
  same clause list that was given to the solver. Correct and conservative.

### 2.4 Independent computation (my encoding; my split SB-min, and Lemma 8's split)

`c05_independent.py`, written from scratch. Encoding: exactly-one per cell (pairwise), Latin rows (Lean),
Latin columns for 1313 only (Lean), and the law **without auxiliary variables**: n⁵ clauses
¬(y∗x=c) ∨ ¬(c∗y=d) ∨ ¬(x∗d=e) ∨ (y∗e=x) for 677 and ¬(y∗x=c) ∨ ¬(c∗x=d) ∨ ¬(d∗y=e) ∨ (y∗e=x) for 1313 (in a
functional table the premise holds exactly for the true inner values, so these clauses are the law). No
division clauses unless stated.

My symmetry break **SB-min** (not Lemma 8): pick a with fix(a) minimal over *all* elements; relabel as in
§2.1 so that row 0 is a fixed permutation of cycle type λ with 0 in a cycle of length ℓ; then *every* row
has ≥ k = λ.count(1) fixed points. Cases: every partition λ and every distinct part ℓ of λ (45 for n = 8,
97 for n = 10). Completeness: the relabelling argument of §2.1 with the minimum over all elements
(σ(a) = 0, fix′(σb) = fix(b) ≥ fix(a) = k for every b). The at-least-k constraint is encoded without
auxiliary variables: every set of n−k+1 columns contains a b with a∗b = b (λ is written in decreasing order
below, as in the lab's files).

*Tie-break R1* (used for 677 at order 10): among the elements of minimal fix,
take a non-idempotent one if there is one. Then a case with ℓ = 1 arises only if every element of minimal
fix is idempotent, so in it every non-idempotent row has ≥ k+1 fixed points (clauses "a∗a = a or ≥ k+1 fixed
points", again aux-free). R1 only adds constraints to cases with ℓ = 1, so cases already refuted without it
stay refuted. *My division clauses* (optional, aux-free, same content as Lemma 9): y∗a = x ∧ y∗x = c ∧ c∗y = d
→ x∗d = a and y∗d = x ∧ x∗a = d ∧ y∗x = c → c∗y = a for 677; for 1313 the analogues with T = d∗y, d = c∗x and
right injectivity. *Lemma 8 in my encoding:* row 0 = my permutation of type λ, idempotency of all elements in
the idempotent cases, and "a∗a = a or ≥ k fixed points" written as the subset clauses plus the literal a∗a = a.
For cases with k ≤ 1 its non-idempotent CNFs coincide with my SB-min CNFs (a∗a = a already makes a a fixed
point of L_a), so the two splits differ in the cases with ℓ = 1 or k ≥ 2.
Solver: CaDiCaL 1.9.5 (pysat `cadical195`; the lab used 1.5.3); DRAT proofs from the same solver, checked by
the same drat-trim binary.
Validation of the encoding: every linear model over GF(5), GF(7), GF(9), GF(16) satisfies my plain CNF and,
after SB-min relabelling with *each* admissible choice of a, the CNF of its case (including ℓ ≥ 2 cases
such as ((3,3,1),3) for 1313 at 7, ((7),7) and ((6,1),6) for 677 at 7, ((3,3,3),3) for 1313 at 9); 200
random row-permutation tables of order 5 are accepted iff they satisfy the law. The same holds with my division
clauses switched on, and for my Lemma-8 CNFs with division clauses (66/66 relabellings of the linear models
of orders 5, 7, 9 accepted, 7 different cases).

| law | order | result | detail |
|---|---|---|---|
| 677 | 2, 3, 4, 6 | no model | SB-min: all cases UNSAT (2, 4, 7 and 19 cases) |
| 677 | 5, 7, 9 | model found | found by the search (cases ((2,2,1),1), ((6,1),1), ((8,1),1)), re-checked by evaluation |
| 677 | 8 | **no model** | 45/45 cases UNSAT, ≤ 37,746 conflicts each, all 45 DRAT proofs `s VERIFIED` (18 s in all) |
| 677 | 8 | (plain) | Latin rows + 0∗0 ∈ {0,1} only: not finished in 18 min (as EXP-C05-03 found) |
| 677 | 10 | **no model** | (a) Lemma 8's split in my encoding plus my division clauses: 97/97 UNSAT, all 97 DRAT proofs `s VERIFIED` (34.6 M proof lines; 807 s solving, 991 s checking; hardest case (non-idempotent, (7,3), 7), 972,836 conflicts). (b) SB-min with tie-break R1, with my division clauses in every case: 97/97 UNSAT, all 97 DRAT proofs `s VERIFIED` (40.8 M proof lines; 908 s solving, 1,069 s checking; hardest (7,3), ℓ = 7, 972,836 conflicts). Earlier solver-only runs of SB-min agree (72 cases within 300,000 conflicts with the plain encoding, 3 more unbounded with ≤ 2.16 M conflicts, the rest with division clauses and, for ℓ = 1, R1); plain SB-min without R1 and division clauses left ((3,3,3,1),1) open after 10 min |
| 1313 | 2, 3, 4, 6 | no model | SB-min: all cases UNSAT (2, 4, 7 and 19 cases) |
| 1313 | 5, 7, 9 | model found | cases ((2,2,1),1), ((3,3,1),1), ((3,3,3),3), re-checked |
| 1313 | 8 | **no model** | Latin square only, **no symmetry breaking at all**: UNSAT in 39 s (800,663 conflicts); SB-min: 45/45 UNSAT, all DRAT-verified |
| 1313 | 10 | **no model** | SB-min: 97/97 UNSAT (27 s; most cases by unit propagation), all 97 DRAT proofs `s VERIFIED`; Latin square without symmetry breaking: not finished in 10 min |

A by-product that explains the many one-conflict refutations of ℓ = 2 cases for 677 (in both splits): **no
model of 677 has an element a with b = a∗a ≠ a and a∗b = a.** Proof: the law at (x, y) = (a, a) gives
a∗(a∗(b∗a)) = a; L_a² is a bijection fixing a, so b∗a = a. At (x, y) = (b, a): y∗x = a∗b = a,
(y∗x)∗y = a∗a = b, so the law reads a∗(b∗b) = b = a∗a, hence b∗b = a = b∗a, contradicting injectivity of
L_b. So every case with ℓ = 2 is UNSAT for 677, for every n.

### 2.5 `results/EXP-C05-08.json` (finished 2026-10-19 23:52, 1,542 s)

Checked with `c05_e08_results_check.py`: for every (law, n) the recorded instances are exactly the Lemma 8
cases, each once (12, 19, 30, 45, 97 for n = 5, 6, 7, 8, 10); all 401 UNSAT instances have
`drat_trim = VERIFIED`; the 5 SAT tables satisfy the law (my evaluator), have row 0 = π(λ, ℓ), Latin rows
(and columns for 1313), and satisfy their case's idempotency / fixed-point constraints; 0 UNKNOWN, 0 rejected
proofs. Verdicts: for both laws a model at 5 and 7, none at 6, 8 and 10 (every case certified). Proof lines:
577,051 (677/8), 37,460,526 (677/10), 243,973 (1313/8), 2,221,539 (1313/10) — 40,503,089 for n = 8, 10, as
Theorem 10 says ("40.5 million"); the hardest case, 677/10, took 1,327,284 conflicts, 1313 at most 8,517 —
as stated.

### 2.6 Remarks on the new records

* CLM-C05-12 ("orders ≤ 10 exactly 1, 5, 7, 9" for 677) is supported: 2 is in the notes' list of laws
  without order-2 models and certified (EXP-C05-06), 3, 4, 6 certified (CLM-C05-08 / EXP-C05-06), 5, 7, 9 by
  Lean tables (CLM-C05-07), 8 and 10 here.
* CLM-C05-13 cites "the ETP notes and EXP-C05-03" for 1313 at 2, 3, 4, 6. EXP-C05-03 is solver-trusted; the
  DRUP certificates for (1313, n), n = 2, 3, 4, 6, are in EXP-C05-06 (all VERIFIED). Cite EXP-C05-06.
* CLM-C05-14, second sentence (non-right-cancellative finite models of 677 exist): the ETP blueprint page
  (https://teorth.github.io/equational_theories/blueprint/677-chapter.html, read 2026-10-20 through a web fetch)
  has it in §13.1 — an extension construction with a field M of size 16 and a field G of size 31, ending
  "Since ◇⁰ is not right-cancellative, this gives a finite 677 magma that is not right-cancellative." I did not
  check the construction. My own searches for a model of 677 with some column containing a repeated value
  are UNSAT at order 5 (1,532 conflicts) and order 7 (697,884 conflicts) with only Latin rows and 0∗0 ∈ {0, 1}
  (`c05_independent.py noncancel`), and at order 9 in all 67 cases of my SB-min split with R1 and my
  division clauses, which use only *left* injectivity (`c05_certify_runner.py sbmin-r1-noncancel`, 36 s,
  ≤ 40,424 conflicts per case; the same split at order 7 also gives 30/30 UNSAT; the plain order-9 search
  had not finished after 25 min). So every model of 677 of order ≤ 10 is a quasigroup, and a
  non-right-cancellative finite model, which exists by the blueprint, has order ≥ 11 (solver results, no
  proofs; a positive control — Latin rows plus the repeated-column clause, without the law — is SAT).
* Novelty: CLM-C05-11 as REDISCOVERY (Mace4, ETP paper §7.3.1) matches the task context. I did not re-check
  the ETP sources about order 10, so POTENTIALLY NOVEL for CLM-C05-12/13 rests on the Historian.

---

## 3. The two PROVEN claims without an independent review

### 3.1 CLM-C05-10 — linear models x∗y = ax + by over GF(q), q ≤ 128 (C05.md Theorem 6, EXP-C05-07)

*The argument.* By induction on terms, t(x, y) = α_t x + β_t y with α_x = 1, β_x = 0, α_y = 0, β_y = 1 and
α_(s∗u) = aα_s + bα_u, β_(s∗u) = aβ_s + bβ_u; since the identity must hold for (x, y) = (1, 0) and (0, 1), the
law x = t holds iff α_t(a, b) = 1 and β_t(a, b) = 0. A field isomorphism maps solutions to solutions, so the
set of q with a solution does not depend on the chosen modulus. Correct.

*Independent computation* (`c05_linear_gf.py`, own parser, own GF(p^k) arithmetic): modulus = the *last* monic
irreducible polynomial of degree k in lexicographic order (the lab uses the first), field property checked
(every non-zero element invertible); for every law, every prime power q ≤ 128 (44 values) and every
(a, b) ∈ GF(q)², the law was decided **twice**: by the coefficient method, and by evaluating the whole
q × q table ax + by on all q² pairs (x, y). Results (9.7 min):
* the two methods agree on every (law, q, a, b);
* the order lists agree with `results/EXP-C05-07.json` for all 15 laws, and so do the numbers of solutions
  (a, b) per (law, q);
* 677: 5, 7, 9, 11, 13, **16**, 19, 25, 31, 37, 41, 43, 49, 61, 67, 71, 73, 81, 97, 101, 103, 109, 121, 125;
  1313: 5, 7, 9, 13, **16**, 17, 19, 23, 25, 31, 37, 43, 47, 49, 53, 59, 67, 71, 73, 79, 81, 97, 101, 103, 107,
  109, 113, 125, 127 (8 solutions each at q = 16); absences, e.g. 677 at 8, 17, 23, 27, 29, 32, 64, 128 and
  1313 at 8, 11, 27, 29, 32, 64, 128, confirmed by both methods;
* 0 linear models at an order that EXP-C05-03 found UNSAT (n ≤ 10), that CLM-C05-08 certifies as a gap, or
  that the ETP notes exclude.
* the examples quoted in Theorem 6 hold: over GF(2)[t]/(t⁴+t+1), x∗y = (1+t³)x + t³y satisfies 677 and
  x∗y = t³x + (1+t³)y satisfies 1313 (full-table check; with the coefficients swapped, neither holds).

*Correction.* C05.md Theorem 6 says "Every solution is re-checked on its full q × q table" and the
proof_check says "every model found re-checked on its full table". In `E07_finite_field_models.py` only
`hits[0]`, the first solution per (law, q), is re-checked (`assert satisfies(T, law)`); the solution counts
come from the coefficient method alone. The claim is not affected (the coefficient method is exact, and my
full-table check covers every pair), but the wording should be corrected.

### 3.2 CLM-C19-15 — D(n) ≤ 1 + (t+1)(t+6)/2 and L(n) = φ²n − O(log² n) (C19.md Theorem 8)

*The written steps that are not in Lean.*
1. *The split phase reaches lazy(n) after Ψ(lazy(n)) moves.* Theorem 2 (CLM-C19-02, PROVEN, reviewed
   2026-10-18) says every maximal sequence of split moves (C1 and the S_i) from n·e₀ ends at lazy(n); Theorem 1
   (CLM-C19-01, PROVEN, Lean-checked move deltas) gives ΔΨ = +1 for C1, S2 and every S_i, and Ψ(n·e₀) = n·a₁ = 0
   (a₁ = F₃ − 3 = 0). So such a sequence has exactly Ψ(lazy(n)) moves. Correct. (Only *existence* of a split
   sequence from n·e₀ to lazy(n) is needed.)
2. *L(n) ≥ Ψ(lazy(n)).* Continue from lazy(n) with arbitrary legal moves; the game terminates (every move
   raises Ψ by ≥ 1 and Ψ is bounded on the finitely many positions of value n) at the unique terminal position
   (Zeckendorf). This is a game on n of length ≥ Ψ(lazy(n)). Correct; no optimality theorem is used.
3. *Ψ(Zeckendorf(n)) = B(n).* By definition: B(n) = Σ_i a_i δ_i with paper index i = level + 1, and
   Ψ(c) = Σ_k c_k a_(k+1). Correct.
4. Hence D(n) = B(n) − L(n) ≤ B(n) − Ψ(lazy(n)) = Σ_k a_(k+1)(z_k − ℓ_k), which is the left side of
   `deficit_bound` with z = Zeckendorf(n), ℓ = lazy(n), T ≥ both top levels (the truncated sums are then the
   full values, and both strings are 0/1 strings of value n). The Lean indexing is right: paper F_i =
   `fib (i+1)`, chip on level k worth `fib (k+2)`, a_(k+1) = F_(k+3) − k − 3 = `fib (k+4) − k − 3` (F₁ = 1,
   F₂ = 2, F₃ = 3 ✓; a₁ = 0, a₂ = 1, a₃ = 3 ✓), consistent with `Infinity.C19.a` in `C19_Zeckendorf.lean`.
5. *Asymptotics.* B(n) = Σ z_k(φ²F_(k+1) + ψ^(k+2) − k − 3) = φ²n + O(1) − O(j²) with j = O(log n) the
   Zeckendorf top level, and L(n) ≤ B(n) (Theorem 1); with D(n) = O(t²), t = O(log n) (a lazy string with top
   t has value ≥ F_(t+2) − 1), L(n) = φ²n − O(log² n). Correct.

*Numerical check* (`c19_checks.py`, written from scratch; 17 s):
* every move changes Ψ by the amounts of Theorem 1 (C1: +1, C_i: +i for i = 2..11, S_i: +1 for i = 2..9, as
  observed in 894 random games, three for each 2 ≤ n < 300), every random game ends at the Zeckendorf representation, and
  |G| = B(n) − Σ_(i≥2)(i−1)MC_i(G) holds in all of them;
* lazy(n), computed by brute force over all sets of levels, is unique for n < 400 and equals my fast
  construction;
* Theorem 2, exhaustively: for every n ≤ 60 *all* maximal split-only sequences from n·e₀ end at lazy(n) and
  have exactly Ψ(lazy(n)) moves;
* the longest game L(n) by exhaustive search over all positions for n ≤ 100 (1.68 million position
  evaluations): identical to the lab's `L_exact` (EXP-C19-01) for every n ≤ 100; for every n ≤ 100,
  L(n) ≥ Ψ(lazy(n)) and 0 ≤ D(n) ≤ B(n) − Ψ(lazy(n)) ≤ 1 + (t+1)(t+6)/2 (D(n) = B(n) − Ψ(lazy(n)) exactly at
  n = 1, 2, 4, 7, 12, 20, 33, 54, 88, the numbers F_k − 1, as Corollary 3 predicts; largest D = 20, largest
  B − Ψ(lazy) = 24);
* the arithmetic part B(n) − Ψ(lazy(n)) ≤ 1 + (t+1)(t+6)/2 for every n ≤ 100,000 (largest ratio 0.443; the
  lab reports 0.476 on a larger sample).

---

## 4. Fidelity of the new Lean files

All five files: the sha256 of the files on disk equals the one recorded in `proofs/lean_results.json`
(compiled 2026-10-19, exit 0, "nonstandard_axioms": []); `grep` finds no `sorry`, `admit`, `native_decide`,
`axiom`, `unsafe`, `implemented_by`, `opaque`, `@[extern]` or `set_option`; each main theorem is followed by
`#print axioms`. I recompiled all five files myself after the container restart (`lake env lean`, Lean
4.35.0): exit 0, no errors, no warnings; every `#print axioms` line reports `[propext, Classical.choice,
Quot.sound]` or `[propext, Quot.sound]` (C05_Law1313: 3 + 2 theorems with no axioms at all; C10: 19;
C13: 24; C17: 6; C19: 6 theorems listed).

**`C10_SkewBinary.lean` ↔ CLM-C10-07.** `Canon` = digits 0/1/2, the first non-zero digit ≤ 2 and all later
digits ≤ 1 — exactly "only the lowest non-zero digit may be 2"; `val` uses w_i = 2^(i+1) − 1; `changes`
counts differing positions of two lists of equal length; `canon_existsUnique` gives existence and uniqueness
(the paper only cites it), so `repK K n` *is* the canonical representation and the cost does not depend on how
`inc` is written. `increment_cost` is stated for arbitrary canonical l, m of equal length with
val m = val l + 1 (conclusion 1 + χ(l) ≤ 2); `average_cost` takes K = ⌊log₂(N+1)⌋, which satisfies N < w_K, so
every n ≤ N is representable, and bounds |cost/N − 3/2| by (⌊log₂(N+1)⌋+1)/(2N). Faithful; the "O(log N/N)" is
an explicit inequality. No vacuous hypothesis (equal-length canonical representations of n, n+1 exist for
every n + 1 < w_K).

**`C13_AffineStructure.lean` ↔ CLM-C13-01.** `coeffP`/`constP` are the paper's C_t[v], D_t for
x⋆y = x + a·y + 1 (C_(st) = C_s + a·C_t, D_(st) = D_s + a·D_t + 1); `sysLaw` is Sys(s = t); `affModels` is the
set of N ≥ 1 with an affine anchored model, and `affine_anchored` shows every anchored table αx+βy+γ is of
that form, so `affModels_eq` is (a)+(b). (c) `aff_of_dvd`, `aff_mul_of_coprime`, `mem_aff_iff_primePow`;
(d) `aff_structure_of_no_common_factor` — hypothesis "every common divisor in ℚ[X] has degree ≤ 0", which is
false for S = ∅ (vacuously every g, e.g. X, is a common divisor) and for S = {0}, so these fall correctly under (e)
(`aff_infinite`, `aff_empty`); (f) as disclosed (G and the cofactors are hypotheses). Polynomials are
evaluated in `ZMod N` with N ≥ 1 enforced in `Aff`. Faithful; the uncovered remarks are listed in the
proof_check.

**`C17_ForcedTable.lean` ↔ CLM-C17-05.** `anchor : ∀ x, op x 0 = x + 1` and
`step : ∀ x y, y.val + 1 < N → op x (y + 1) = op (op x y) (x + 1)` on `Fin N` with modular `+` are exactly
"x⋆0 = x+1 (mod N)" and the instances y ≤ N−2; `full_instance_iff` is the stated reduction; `forced_unique`
and `forced_exists` (built by the recursion `lav`, whose fallback value 0 is never reached by `lav_spec`) give
∃!. N = 1 is included (`NeZero N`). Faithful. (Not covered, as the file says: Laver's theorem; CLM-C17-08 now
has its own Lean file, §1.4.)

**`C19_DeficitBound.lean` ↔ CLM-C19-15 / CLM-C19-14.** Indexing checked in §3.2 (paper F_i = `fib (i+1)`;
not off by one). `deficit_bound` assumes only 0/1 strings z, ℓ with ℓ vanishing above t and equal truncated
values; the application (z = Zeckendorf(n), ℓ = lazy(n), T ≥ both top levels) satisfies all hypotheses, and
the left side is then exactly B(n) − Ψ(lazy(n)). The real-valued and the integer statements agree
(`deficit_bound_int`, exact quotient). As the file says, no game is formalised; the claims' proof_check texts
say the same ("Lean-checked arithmetic core"). Faithful.

**`C05_Law1313.lean` ↔ CLM-C05-14 (and Lemma 7).** `Law1313 op := ∀ x y, op y (op (op (op y x) x) y) = x` is
x = y∗(((y∗x)∗x)∗y) and `Law677 op := ∀ x y, op y (op x (op (op y x) y)) = x` is x = y∗(x∗((y∗x)∗y)), the laws
as given in the task and in `E03_frontier_push.LAWS` (I did not re-check the ETP numbering against the ETP list
itself). `[Finite α]` is the only assumption; bijectivity of left and right translations is proved, not
assumed. The "not right projection" lemmas need two distinct elements, as stated. Faithful.

---

## Files (`reviews/skeptic_checks/batch1.1/`)

| file | what |
|---|---|
| `C17_RowPeriod.lean` | Lean proof of CLM-C17-08 from Laver's theorem (§1.4); compile with `cd proofs/lean && lake env lean ../../reviews/skeptic_checks/batch1.1/C17_RowPeriod.lean` |
| `c17_row_period.py`, `c17_row_period.json` | numerical checks of Lemmas A, B and (i)–(iii) (§1.4) |
| `c05_independent.py` | my encoding and case splits for 677/1313 (modes: per-law SB-min run, `certify` (DRAT), `plain`, `cases`, `lemma8`, `noncancel`, `validate`, `validate_lemma8`) |
| `c05_certify_runner.py` | restartable runner (one JSON line per finished case): `lemma8-cert` (DRAT), `sbmin`, `sbmin-r1` |
| `c05_{677,1313}_n{2..10}_cadical195_0_end.json` | SB-min runs per law and order (n = 10 for 677: 300,000-conflict budget) |
| `c05_certify_677_n8.json`, `c05_certify_1313_n8.json`, `c05_certify_1313_n10.json` | SB-min with DRAT proofs: per-case status, CNF sha256, drat-trim line |
| `c05_lemma8_677_n10_div_0-96.json` | Lemma-8 split in my encoding, 677 at 10 (solver run) |
| `c05_cert_lemma8_677_n10_{even,odd}.jsonl` | the same 97 CNFs with DRAT proofs checked by drat-trim |
| `c05_cert_sbminr1_677_n10_{even,odd}.jsonl` | SB-min with R1 and division clauses, 677 at 10: 97 DRAT-certified cases |
| `c05_cases_*.json`, `c05_sbmin_677_n10_rest_lge2.jsonl`, `c05_sbmin_r1_677_n10_l1.jsonl` | the SB-min cases of 677 at 10 left open at 300,000 conflicts |
| `c05_plain_1313_n8_none.json`, `c05_noncancel_677_n*.json`, `c05_noncancel_split_677_n9_{even,odd}.jsonl`, `c05_validate_*.json` | runs without symmetry breaking, the searches for non-right-cancellative models of 677 (orders 5, 7; order 9 by the split), encoding validations |
| `c05_e08_results_check.py` / `.json` | check of `results/EXP-C05-08.json` (§2.5) |
| `c05_e08_dimacs_check.py`, `c05_e08_dimacs_check_5_6_7_8.json`, `c05_e08_dimacs_check_10.json` | re-generation of the lab's CNFs, hash comparison, DIMACS sanity, semantic acceptance test (§2.1, §2.3) |
| `c05_linear_gf.py` / `.json` | CLM-C05-10 recomputation (§3.1) |
| `c19_checks.py` / `.json` | C19 Theorems 1, 2, 8 checks (§3.2) |

The DRAT proofs and CNFs were written to the session scratchpad (not kept in the repository); the JSON files
record the CNF sha256 and the drat-trim status line of every certified case.

---

## Summary

* **CLM-C17-08: UPHELD; PROVEN is justified** on the Historian's row-period proof, which I completed (Lemma A on
  the row structure of the forced table, the top-element case of the induction) and machine-checked:
  `C17_RowPeriod.lean` proves "model of the full instance on Fin N ⇔ N is a power of 2" for every N ≥ 1 from
  Laver's theorem as an explicit hypothesis (used only at 2^(v₂(N)+1)). The literature chain is logically valid
  but no longer needed.
* **EXP-C05-08 / CLM-C05-11, -12, -13: UPHELD** (CLM-C05-13 with a citation correction). Lemma 8 is complete,
  Lemma 9 and Lemma 7 are sound, the conditional cardinality encoding is correct, the code implements the lemmas,
  the certified CNFs are exactly those of the reviewed builder, and my own encoding re-decides 677 and 1313 at
  orders 8 and 10 (and the controls) — at 8 and for 1313 at 10 with a different case split and DRAT proofs, for
  677 at 10 both with Lemma 8's split and with my own split (SB-min with tie-break R1), every case of both
  DRAT-certified.
* **CLM-C05-14: UPHELD**; its citation (non-right-cancellative finite models of 677) is in the ETP blueprint
  §13.1; by my (uncertified) searches there are none of order ≤ 10, so such a model has order ≥ 11.
* **CLM-C05-10: UPHELD WITH CORRECTIONS** — the computation is reproduced exactly; only the wording "every
  solution is re-checked on its full table" is wrong (EXP-C05-07 re-checks one per (law, q)).
* **CLM-C19-15: UPHELD** (the written steps are correct; exhaustive games for n ≤ 100 agree).
* **Lean files (CLM-C10-07, CLM-C13-01, CLM-C17-05, CLM-C19-14/-15, CLM-C05-14): faithful**; no sorry, admit,
  native_decide or axiom; recompiled.
* Nothing REFUTED, no GAP.
