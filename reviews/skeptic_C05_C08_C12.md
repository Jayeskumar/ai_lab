# Skeptic review of cycles C05, C08, C09, C10, C11 and C12

**Reviewer:** Mathematical Skeptic (independent of the researchers who produced the claims)
**Date:** 2026-10-18 · **Scope:** CLM-C05-01 … 09, CLM-C08-01 … 06, CLM-C09-01 … 08, CLM-C10-01 … 07,
CLM-C11-01 … 09, CLM-C12-01 … 13 (52 claims).

**Material read:**
- The six cycle READMEs and `record.yaml` files (C05 in full, the others for claims and journals); all 52 claim records in `db/claims/`.
- `proofs/paper/C05.md`, `C08.md`, `C09.md`, `C10.md`, `C11.md`, `C12.md`; `proofs/lean/Infinity/C05_Magmas.lean`, `C08_Knuth.lean`, `C11_Codes.lean`, `C12_Games.lean`.
- All experiment scripts of the six cycles (C05 E03/E06, C08 E01–E06, C09 E01–E04, C10 E03 and C12 E06 line by line); the stored `results/EXP-C05-*` … `EXP-C12-*`; `systems/magma.py`, `circle.py`, `circle_arith.py`, `counting_cost.py`, `codes.py`, `code_bench.py`, `relational_games.py`; `lab/runner.py`, `lab/oeis.py`.
- Textbook chapters `06_magma_laws.md`, `09_circle_products.md`, `10_circle_primes.md`, `11_cost_of_counting.md`, `12_integer_codes.md`, `13_relational_games.md`.
- The Historian's review `reviews/historian_C03_C10.md` (C08–C10 sections), read to avoid duplicating it and to cross-check it.
- External: the official ETP equation list (`data/equations.txt` of github.com/teorth/equational_theories), downloaded to the scratchpad to check every ETP number used in C05.

**Rules followed:**
- No existing file was edited. My code is in `reviews/skeptic_checks/C05_C08_C12/`, raw outputs in its `out/` subfolder.
  - None of my scripts imports `systems/` or `lab/`. Stored results are only read, for comparison.
  - pysat is used only as a SAT solver (Kissat 4.0.4 and CaDiCaL 1.9.5, not the lab's CaDiCaL 1.5.3 or Glucose 4), on my own CNF encoding. numpy is used for vectorised arithmetic.
  - Heavy enumerations are my own C programs (`c08_assoc.c`, `c08_pairs.c`, `c08_extreme.c`, `c09_circle.c`, `c12_g03.c`, `c12_sub.c`), in exact integer arithmetic (`__int128` with overflow detection where needed).
  - Every counterexample triple quoted below was re-verified by a separate plain-Python big-integer implementation (`c08_verify_triples.py`, `c08_verify_more.py`).
  - One Lean file of my own, `c05_order16.lean`, was compiled with `lake env lean` from `proofs/lean`. Nothing in `proofs/` was touched.
- Lab experiments re-run (allowed): EXP-C05-05, EXP-C08-03, EXP-C09-04, EXP-C10-02, EXP-C11-09, EXP-C12-06 (see (b) R).
  - This rewrote those `results/*.json` and appended runs to `db/experiments/*.json` and `db/audit_log.jsonl`.
  - The pre-run result files are kept in `out/lab_rerun_before/`.
- Not run: `lab sync`, `lab lean`, `lab book`, any git command. I committed nothing. EXP-C05-06 was not re-run (it needs a drat-trim binary and would overwrite its certificates).
- All jobs ran under `nice -n 10`, one heavy job of mine at a time, each under 15 minutes. The longest were 137 s (targeted C08 search over 627 sequences) and 107 s (circle semigroup to 10⁸). Another reviewer's jobs shared the machine.
- Every check reported below was actually run. Where I stopped a run, I say so.

## Bottom line

- **One claim is refuted outright: CLM-C05-09.**
  - The conjecture says laws 677, x = y(x((yx)y)), and 1313, x = y(((yx)x)y), have spectrum {1} ∪ {odd n ≥ 5}.
  - Both laws have models of the **even order 16**: affine operations x∗y = ax + by over GF(16), e.g. (a, b) = (1 + t³, t³) for 677 and (t³, 1 + t³) for 1313, with t⁴ = t + 1.
  - Checked by brute force over all (x, y) and by Lean's kernel (`decide`, axioms: propext only; Appendix B).
- **CLM-C08-05 is wrong as stated: 5 of its 8 thresholds are refuted by explicit, independently re-verified triples.**
  - tribonacci 3, 4-bonacci 7, G(k+1) = G(k) + G(k−2) 10, (3,3; 1,5) 10, (2,2; 1,2) 5.
  - Lower bounds from my targeted search: ≥ 4, ≥ 8, ≥ 11, **≥ 12**, **≥ 7**.
  - The last two contradict even the lab's corrected re-test EXP-C08-06, which reports "no failure" at (3,3; 1,5) s = 10 and (2,2; 1,2) s = 6.
  - The claim record and the C08 README were never updated after EXP-C08-06 and the Historian's audit. The textbook was.
- **CLM-C08-04's evidence is contaminated, but its statement survives.**
  - 31 of the 90 rows of EXP-C08-04 list shifts as "associative" that are certified non-associative. Eight of these rows have β > 0.
  - 4 of its 10 non-monotone examples are artefacts. The Historian found 2 of them; EXP-C08-06 still lists 2 others.
  - A much stronger targeted search (extreme-conjugate pairs) finds 0 non-monotone shift sets among 231 quadratic Pisot sequences with β > 0 (s ≤ 16). It finds 60 among 396 with β < 0, all with non-canonical initial values.
- **The potentially novel G03 theorem (CLM-C12-04) is correct.**
  - I checked the written inductive Steps 1–3 line by line (Appendix A.5); they are correct.
  - Exact Grundy values agree with the closed form for all n ≤ 10⁸ (lab: 10⁵).
  - The mex certificate holds for a ≤ 400, and the claimed shift invariance of the offset sets holds for 13 ≤ a ≤ 400.
- **All written proofs awaiting review are correct:** C09 Theorems 1, 3, 4 and C12 Theorem 8. Also correct: the other written proofs of C10, C11 and C12, and C08 Theorem 1, whose Lean file compiles.
  - Wording gaps: CLM-C09-07's bound |N(n)| < (√5/φ)n + 1 is not in the cited proof (a one-line proof is in A.2), and CLM-C09-03's title overstates.
- **C05 frontier facts re-derived independently.**
  - All 16 claimed non-memberships (gaps) are UNSAT under my own CNF and Kissat. The 13 with n ≤ 6 are UNSAT even without the extra Latin-row and symmetry-breaking constraints.
  - All 12 certified tables satisfy their laws. Every ETP number used (21 laws) matches the official ETP list.
- **Everything else I recomputed agrees with the records.** This covers the C05 census, C09 counts and the window obstruction to 10⁸, the C10 constants, the C11 counts, comparisons and benchmarks, and the C12 closed forms. Details in (b).
- **Other problems** (details in (c)):
  - P4: the "exhaustive" factorisation enumeration behind CLM-C09-08 was truncated at 64 factorisations per n (41 truncation hits).
  - P5: a floating-point boundary misclassification in EXP-C09-04 (n = 1).
  - P7: CLM-C10-05's evidence covered only offset-1 rules.
  - P9, P10: stale C08/C05 documents.

---

## (a) Verdicts

| Claim | Verdict | Details | Recommended status change |
|---|---|---|---|
| CLM-C05-01 (H-C05-1: spectrum {1} or all; refuted) | **UPHELD** | Lean re-run OK (`T4_law167`, `T5_law167`, `law167_card_mod_four`). My own evaluator confirms both tables. Brute force over all 16 + 19,683 tables finds no model of law 167 at orders 2, 3. | None. |
| CLM-C05-02 (census of 115 identities) | CENSUS_VERDICT | CENSUS_DETAILS | CENSUS_CHANGE |
| CLM-C05-03 (H-C05-Q refuted) | **UPHELD** | T4 row 1 = (0, 2, 2, 2) (Lean `T4_not_latin`, own check). By brute force over all magmas of order ≤ 3, exactly 18 of the 115 identities have a non-quasigroup model of order ≤ 3. | None. |
| CLM-C05-04 (law 167: n ≡ 0, 1 mod 4) | **UPHELD** | Lean re-run OK, standard axioms. `Law167 op := ∀ x y, op (op y x) (op x y) = x` is exactly x = (yx)(xy). The conclusion `card % 4 = 0 ∨ = 1` is the English. The parenthetical sufficiency (matching the 2-subsets in pairs {a,b} ↔ {c,d}; ab = c, ba = d, cd = b, dc = a; xx = x) was checked for every n ≡ 0, 1 (mod 4) up to 29, with 5 random matchings each. | None. |
| CLM-C05-05 (left translations bijective) | **UPHELD** | `left_mul_bijective_of_law` matches the x = y∗s(x, y) case. The written path version (Lemma 1) is correct (A.1). | None. |
| CLM-C05-06 (H-C05-A refuted) | **UPHELD** | NAND model re-checked. Affine models of (yx)(x(yy)) over ℤ_n exist exactly for n ∈ {1, 5} (n ≤ 6, brute force). Own recount: exactly 4 identities are full on 1..6 without affine models at every n ≤ 6, with affine spectra {1,5}, {1,2,5}, {1,2,5}, {1,5}. 39 restricted identities have spectrum members without affine model; no affine model lies outside the SAT spectrum. | None. |
| CLM-C05-07 (new memberships, POTENTIALLY NOVEL) | **UPHELD** | All 12 Lean tables of the file satisfy their laws under my own evaluator, and the Lean file re-compiles. The ETP numbers 467, 677, 1286, 1313, 1516 (and all other numbers used in C05) match the official ETP list. My own SAT encoding re-finds 677 at 5 and 7; I stopped the re-search at 677@9 because every membership is already Lean-certified. The novelty is explicitly relative to the notes read, which is fair. Note: 677 and 1313 also have models of order 16 (CLM-C05-09). | None (optionally add order 16 for 677 and 1313). |
| CLM-C05-08 (new gaps, POTENTIALLY NOVEL, computer-assisted) | **UPHELD** | Own CNF (no subterm sharing, exactly-one per node) + Kissat 4.0.4 with only the sound constraints: UNSAT for all 16 listed instances (501@2,3,6,7; 677@2,3,4,6; 883@3,6; 1076@8; 1083@2,5,6; 1719@2). The 13 with n ≤ 6 are also UNSAT under CaDiCaL 1.9.5 **without** the Latin-row and symmetry-breaking constraints, which removes Lemma 4 from the trust base for them. My encoder matches brute force on all 115 identities at n = 2, 3. My runs are solver-trusted; the DRUP certificates are the lab's. | None. |
| CLM-C05-09 (677 and 1313: spectrum {1} ∪ odd n ≥ 5) | **REFUTED** | Both laws have models of order 16: affine maps over GF(16), 8 pairs (a, b) per law. Brute force over all (x, y) and Lean's kernel (`decide`) confirm them; Appendix B. No affine model over GF(8), GF(4), ℤ₈, ℤ₁₀, ℤ₁₆, so orders 8 and 10 remain open. | CONJECTURE → **REFUTED**; record the counterexample. Spectra now contain 1, 5, 7, 9, 16 (and products such as 80). |
| CLM-C08-01 (all shifted Knuth products associative) | **UPHELD** | Lean re-run OK. `circ t a b` is exactly Σ_{k∈Z(a)} Σ_{l∈Z(b)} F(k+l+t) with Mathlib's Zeckendorf list. The written proof (window, integrality, injectivity) is correct (A.3). Own C checker, from the greedy definition in G-indexing: (2,4,4) at s = 0 and (1,4,4) at s = 1 are the lexicographically first failures. No failure at s = 2…24 on 416,000 triples each (cube [1,60]³ + 200,000 random up to 10⁹). | None. |
| CLM-C08-02 (non-Pisot ⇒ never associative) | **UPHELD WITH CAVEATS** | No counterexample with dominant root > 1. All 10 lab sequences and 6 new non-Pisot sequences fail at every s = 0…25 with explicit triples: Mersenne 2^(k+1) − 1, (3,−2; 1,4), (4,−3; 1,2), (1,4), (2,4), (1,6), (2,8), plus (x − 2)² with G_k = (k+1)2^k. Wording problem: G_k = k + 1 has minimal polynomial (x − 1)² and **is associative at every shift** (a ∘_s b = a + b + s − 1). EXP-C08-02's classifier would call it "non-Pisot". | Keep COMPUTATIONALLY SUPPORTED; require dominant root α > 1 (and say how repeated roots count). |
| CLM-C08-03 (Pisot ⇒ eventually associative; GPTW) | **UPHELD WITH CAVEATS** | A published theorem, cited. The supporting thresholds are partly wrong (CLM-C08-05), and the title is broader than GPTW, as the Historian notes. In my data G(k+1) = G(k) + G(k−3) fails at every s ≤ 24, consistent with it lying outside GPTW's hypotheses. | Restrict the title to GPTW's class. |
| CLM-C08-04 (β > 0 ⇒ upward-closed; non-monotone only for β < 0) | **UPHELD WITH CAVEATS** | Statement not refuted. Targeted search (s ≤ 16): 0 of 231 β > 0 sequences non-monotone; 60 of 396 β < 0 sequences non-monotone, none canonical. The evidence is contaminated: in EXP-C08-04, 31 of the 90 rows (8 with β > 0) list a shift as associative that has a certified failing triple (Appendix C.2). Of its 10 non-monotone rows, 4 are artefacts: (4,3;1,5), (3,3;1,2), (2,2;1,5), (3,2;1,6). The quoted example 1,3,4,7,11 ({2} ∪ s ≥ 4) survives. | Keep COMPUTATIONALLY SUPPORTED; restate for non-canonical initial values (as the Historian proposes); replace the evidence. |
| CLM-C08-05 (thresholds for 8 sequences) | **REFUTED (as stated)** | Certified failing triples, re-verified in Python (Appendix C.1): tribonacci at s = 3; 4-bonacci at 7; G(k+1) = G(k) + G(k−2) at 10; (3,3; 1,5) at **10 and 11**; (2,2; 1,2) at **5 and 6**. Only Fibonacci 2, Pell 1 and "G+G(k−3): none ≤ 20" survive; the last extends to s ≤ 24. | COMPUTATIONALLY SUPPORTED → **REFUTED** (or rewrite as lower bounds: ≥ 4, ≥ 8, ≥ 11, ≥ 12, ≥ 7 and cite the triples); correct the C08 README. |
| CLM-C08-06 (H-C08-1 refuted) | **UPHELD** | Fibonacci with s = 3 is associative by the Lean theorem. | None. |
| CLM-C09-01 (structure, embedding into ℤ[φ]) | **UPHELD** | Written proof correct (A.2). Exact checks for all n ≤ 10⁸ with products from the Zeckendorf definition, comparing conjugates with ψ-powers by integer sign tests: the window −ψ² < ν′(n) < −ψ holds for every n, and n* = ⌊(n+1)/φ⌋ for every n. | Mark "written proof, skeptic-reviewed". |
| CLM-C09-02 (unique factorisation refuted) | **UPHELD** | 8 = 1∘1∘1 = 2∘2 re-derived. Exact recount: FACT_FIRST. | None. |
| CLM-C09-03 (window obstruction, density 1/φ², POTENTIALLY NOVEL) | **UPHELD** | Written proof correct (A.2). Own exact computation to 10⁸: no reducible n outside the zone (ψ³, ψ²); forced-irreducible density 0.381966 at 10⁷ and 10⁸. Wording: the title "a fixed proportion 1/φ² of all integers are circle-irreducible" reads as "the irreducibles have density 1/φ²", which is Conjecture CLM-C09-05. The theorem gives density ≥ 1/φ². | Mark skeptic-reviewed; reword the title ("at least 1/φ²"). |
| CLM-C09-04 (density → 0 refuted) | **UPHELD** | Follows from CLM-C09-03. Irreducible density 0.5314 at 10⁷, 0.5247 at 10⁸. | None. |
| CLM-C09-05 (irreducible density exactly 1/φ², conjecture) | **UPHELD** (no counterexample) | The irreducible fraction inside the product zone is 0.2547 at 10⁶, 0.2418 at 10⁷, 0.2310 at 10⁸. This fits c·(log n)^(−0.33) well (successive log-log slopes −0.27, −0.33, −0.33, −0.34, −0.34), so it is consistent with decay to 0, but also with a positive limit. | Keep CONJECTURE; record the 10⁸ data. |
| CLM-C09-06 (length bound \|ν′(n)\| < \|ψ\|^r) | **UPHELD** | Proof correct (A.2). FACT_BOUND | Mark skeptic-reviewed. |
| CLM-C09-07 (norm multiplicative; bound; units) | **UPHELD WITH CAVEATS** | Multiplicativity and N = ±1 ⇔ Fibonacci are in Theorem 1's proof. The bound \|N(n)\| < (√5/φ)n + 1 is **not proved anywhere** in `C09.md`. It is true by one line (A.2). | Add the one-line proof. |
| CLM-C09-08 (factorisation statistics; PROVEN) | FACT_VERDICT | FACT_DETAILS | FACT_CHANGE |
| CLM-C10-01 (b/(b−1), 2, 3/2, e − 1, Gray 1) | **UPHELD** | Frequency proofs checked (negabinary and balanced ternary: digit k is determined by n mod b^(k+1) and changes on a cyclic block structure). Own averages over N = 10⁶ increments: 1.999993, 1.499993, 1.111111, 1.999997, 1.5, 1.718277, 1.0. The lab's figures are over 999,999 increments (P8, cosmetic). | None. |
| CLM-C10-02 (Zeckendorf T_m) | **UPHELD** | Brute force T_m for m ≤ 30 equals 2G_m − ⌈m/2⌉ − 2 and the recurrence. The potential identity d(n, n+1) = 2 + s(n) − s(n+1) (s = number of 1s) holds for all n < 10⁶, so Σ_{n<N} = 2N − s(N) exactly. That is sharper than the proof's O(log² N). | None. |
| CLM-C10-03 (H-C10-0 refuted) | **UPHELD** | Both averages tend to 2 (Hamming measure). | None. |
| CLM-C10-04 (firings 1/(m − B)) | **UPHELD** | Proof correct; token counting alone suffices (A.4). Own counter, 31 rules, N = 400,000: max deviation 3.4·10⁻⁴. The incremental counter equals full stabilisation at sampled n ≤ 3000. | Mark skeptic-reviewed. |
| CLM-C10-05 (single offset: cost = firings + 1) | **UPHELD** | Proof correct (A.4). Own check: for **all 18 single-offset rules**, including offsets g = 2, 3, **every** one of 400,000 increments costs exactly firings + 1. The lab's summary statistic covered only the 5 rules with g = 1 (P7). | Mark skeptic-reviewed; fix the evidence wording. |
| CLM-C10-06 (multi-offset excess; conjecture) | **UPHELD** (as a conjecture) | Own excesses at N = 4·10⁵: 0.4999, 0.3333, 0.6430, 0.7142, 0.8317 for the five quoted rules. All 13 multi-offset rules have positive excess, minimum 0.2960. | None. |
| CLM-C10-07 (skew binary: worst 2, average 3/2) | **UPHELD** | Own canonical increment: worst case 2, average 1.499996 at 10⁶. A proof is elementary: cost = 1 + [rep(n) contains a 2], and among 0 … 2^(k+1) − 2 exactly 2^k − 1 representations contain a 2. | Could be PROVEN. |
| CLM-C11-01 (T_p complete prefix code, GF, T_11 = C1) | **UPHELD** | Lean re-run OK (no axioms); `IsCodeword` matches the definition. GF = brute-force counts = automaton counts for all 126 patterns of length ≤ 6 and L ≤ 16. T_11's codeword set equals C1's up to length 18. Own enumerative encoder for 6 patterns gives codewords in T_p, prefix-free, ordered by (length, lex). Proof checked (A.6). | None. |
| CLM-C11-02 (1^k, 0^k uniquely maximal λ) | **UPHELD** | Proof correct (A.6); also the existence of ρ_p ∈ (1/2, 1]. Own root computation for all 2044 patterns of length 2–10: 0 violations. | None. |
| CLM-C11-03 (unbordered: x/(1−x) identity) | **UPHELD** | All 304 unbordered patterns of length 3–9: f_u(L) = cum_{1^k}(L − 1) exactly for L ≤ 80. | None. |
| CLM-C11-04 (T_011 vs C1, POTENTIALLY NOVEL) | **UPHELD** | Proof correct, including the L ≥ 4 condition F_{L+1} ≥ L + 1 (A.6). Own length functions (C1 from Zeckendorf directly) for n ≤ 2·10⁶ give −1: 3 (n = 1, 2, 4), 0: 429, +1: 1,999,568; the closed forms hold for L < 120. | None. |
| CLM-C11-05 (H-C11-2 refuted) | **UPHELD** | At n = 1000: L_1111 = 15, while 1000, 1001, 1010 (and 0111, 1110) give 14. Rivals beat 1^5 at n = 2^45 (01010, 10101) and 1^6 at 1.3·10¹⁹. | None. |
| CLM-C11-06 (two average-gain predictions refuted) | **UPHELD** | Exact G(2^40), G(2^80), G(2^120) for k = 3: 0.228181, 0.309709, 0.228548; the log-form prediction is 0.287511. | None. |
| CLM-C11-07 (liminf/limsup of the gain, POTENTIALLY NOVEL) | **UPHELD** | Proof checked (A.6). Exact averages at the turning points for L = 100, 200, 400 equal the two constants to 15 digits for k = 2…6. The structural inequalities b_{L−2} ≤ a_{L−1} < b_{L−1} ≤ a_L used by the proof hold for every L from 7, 9, 11, 13, 15 (k = 2…6) up to 420. | None. |
| CLM-C11-08 (benchmarks, mixed) | **UPHELD** | Own length functions reproduce the quoted redundancies to 4 decimals: Zipf 1.1, log-uniform, uniform 2³², geometric 0.001; e.g. T_101 0.1935 vs C3 0.6014 on Zipf 1.1, T_00111 4.4391 vs LEB128 7.4961 on uniform 2³². | None. |
| CLM-C11-09 (T_011 vs C3, C3 vs C1) | **UPHELD** | Proof correct. For n ≤ 2·10⁶: C3 longer than C1 only at n = 1, T_011 longer than C3 only at n = 2, 4, 8. Count inequalities fail only at L = 3, 4, 5 and L = 2 (L < 300). Ratios φ²/2 and 2/φ. I could not check that the C3 construction is Fraenkel–Klein's (paper not read); 101 being a prefix of the codeword 10101 confirms that it is not prefix-free. | None. |
| CLM-C12-01 (G01 = v₂, G02 = v₂ + 1, G04 = Ω) | **UPHELD** | Proofs checked. Own computation to n ≤ 3·10⁵: 0 mismatches. | None. |
| CLM-C12-02 (coprimality games) | **UPHELD** | Proofs checked (A.5). Own computation to 6000: G05 = prime index, G07 = G05, G06 even formula, odd bound and P-set; max g(m)/m over odd m = 0.24987. Also checked Iannucci–Larsson's SG = ⌊(n+1)/4⌋ for n ≡ 3 (mod 6), as SG = g + 1. | None. |
| CLM-C12-03 (G03 P-positions) | **UPHELD** | Lean re-run OK; `g03Opts` matches. Exact P-set for n ≤ 10⁸ (C): 0 mismatches. | None. |
| CLM-C12-04 (G03 Grundy function, POTENTIALLY NOVEL) | **UPHELD** | Steps 1–3 correct (A.5). Exact Grundy values for all n ≤ 10⁸: g = F everywhere. Records continue as 5·2^a up to a = 24; \|g − v₂\| ≤ 2 off odd powers of 2. Mex certificate for m ≤ 15, 6 ≤ a ≤ 400; offset sets identical for all a of each parity in 13 … 400. Step 2 checked exhaustively for odd parts 17 ≤ m ≤ 3001, a ≤ 60, and on 2,912 random large n (a ≤ 200). | Mark "written proof, skeptic-reviewed 2026-10-18"; PROVEN (computer-assisted) stands. |
| CLM-C12-05 (popcount, G19, G20) | **UPHELD** | Proofs checked. Own computation (G13 n < 2^14, G19 ≤ 6000, G20 ≤ 40,000): 0 mismatches. | None. |
| CLM-C12-06 (residue lemma, powers of k) | **UPHELD** | Lean re-run OK; the case analysis in (b) checked (A.5). Own computation k = 2…30, n ≤ 20,000: equals both {1, k} and the closed form. | None. |
| CLM-C12-07 (splitting parity) | **UPHELD** | Lean re-run OK (propext, Quot.sound). 60 random splitting relations (n ≤ 200), G16 and G17 (n ≤ 1500): parity. Grundy's game is not parity, as expected. | None. |
| CLM-C12-08 (squares/triangular: P-density 0) | **UPHELD** | Proof correct, given the cited theorems. Own P-densities and maxima at 2·10⁵ equal the lab's exactly (0.022170 / 95 and 0.011630 / 144). | None. |
| CLM-C12-09 (H-C12-0 inconclusive) | **UPHELD** (status correct) | Ill-posed hypothesis; nothing to check. | None. |
| CLM-C12-10 (signature hypothesis refuted) | **UPHELD** | All quoted pairs re-computed: G01 (1, 0), G02 (2, 1), G03 (1, 0), G05 (1, 2), G06 (2, 4). | None. |
| CLM-C12-11 (sparse sets keep positive P-density; refuted) | **UPHELD** | Densities re-computed. | None. |
| CLM-C12-12 (subtract-a-prime ≤ 11) | **UPHELD** | SUB_PRIME | None. |
| CLM-C12-13 (subtract-a-Fibonacci bounded) | **UPHELD** (no counterexample) | SUB_FIB | SUB_FIB_CHANGE |

---

## (b) Independent checks (commands and results)

Unless noted, commands run from `reviews/skeptic_checks/C05_C08_C12/` with `nice -n 10`; outputs are in `out/`.

**L. Lean.**
- `bash lean_check.sh` compiles C05_Magmas, C08_Knuth, C11_Codes and C12_Games with `lake env lean` (from `proofs/lean`). Exit 0 each, 5–10 s each (`out/lean_*.txt`).
- Axioms:
  - C05: propext only for the decided tables; propext, Classical.choice, Quot.sound otherwise.
  - C08: propext, Classical.choice, Quot.sound.
  - C11: none.
  - C12: ⊆ {propext, Classical.choice, Quot.sound}.
- `grep -nE "sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque"` finds no hits (`out/lean_grep.txt`).
- Statement match was checked for every theorem cited by a claim; see (a).
- `c05_order16.lean` (my own file): `M677_law`, `M1313_law` by `decide`, exit 0, axioms [propext] (`out/lean_c05_order16.txt`).

**C05** (`python3 c05_checks.py <part>`; own parser, enumerator, evaluator and CNF):

| part / script | what | result |
|---|---|---|
| `c05_selftest.py` | own encoder vs brute force, all 115 identities, n = 2, 3, all models enumerated | 0 mismatches |
| `c05_etp_numbers.py <equations.txt>` | the 21 ETP numbers used in C05 vs the official list (line k = equation k) | 21/21 match; 168 is x = (y◇x)◇(x◇z) |
| tables | the 12 Lean tables re-parsed from the .lean file and evaluated; law 167 and law 66 at n = 2, 3 by brute force; affine models of (yx)(x(yy)) | all satisfy; law 167: 0, 0 models; law 66: 0, 4; affine at n = 1, 5 only |
| brute3 | all magmas of order ≤ 3 for my own list of the 115 identities | the same 115 identities as EXP-C05-01; model counts n = 1..3 identical for all 115; 18 with non-quasigroup models |
| affine | affine models over ℤ_n, n ≤ 6 | 4 full-spectrum identities without affine models at all n ≤ 6; 39 restricted with non-affine members; 0 affine outside the spectrum |
| census | SAT spectra n ≤ 6 for all 115 (sound constraints only; 60 s per instance), n = 7, 8 for 2 identities per pattern | CENSUS_TABLE |
| frontier (`out/c05_frontier.log`, `out/c05_frontier_summary.json`) | the gaps of CLM-C05-08 with Kissat (sound constraints) and, for n ≤ 6, CaDiCaL without any extra constraint; memberships | 16/16 UNSAT; 13/13 UNSAT without extra constraints; 677 at 5, 7 SAT. I stopped the run during the re-search of 677@9 (memberships are Lean-certified) |
| `c05_law167_construction.py` | sufficiency construction for law 167 | valid for every n ≡ 0, 1 (mod 4), n ≤ 29 |
| `c05_gf16.py` | affine models of 677 and 1313 over GF(16), GF(8), GF(4), ℤ₈, ℤ₁₀, ℤ₁₆ | GF(16): 8 models per law (Appendix B); none elsewhere |
| conj09 | CONJ09_WHAT | CONJ09_RESULT |

**C08** (own C checkers; `c08_checks.py`, `c08_targeted.py` drive them):

| command | what | result |
|---|---|---|
| `python3 c08_checks.py knuth` | Fibonacci, s = 0…24, cube [1,60]³ + 200,000 random triples ≤ 10⁹ | s = 0: (2,4,4); s = 1: (1,4,4); s ≥ 2: 416,000 triples each, no failure (s = 24: 1452 overflow-skipped) |
| `python3 c08_checks.py thresholds` | 10 sequences, s = 0…24, random triples | random triples already refute 4-bonacci at s = 7, G+G(k−2) at s = 10, (3,3;1,5) at s = 10; they miss tribonacci s = 3 and (2,2;1,2) s = 5, 6 |
| `./c08_pairs …` | embedding criterion ν(a∘b) = x^s ν(a)ν(b) on pairs ≤ 300 + random pairs | also misses tribonacci s = 3 and (2,2;1,2) s = 5 (random sampling is weak) |
| `python3 c08_targeted.py thresholds` | extreme-conjugate candidates (n ≤ 4·10⁵, every non-dominant root), embedding test on all candidate pairs, certified by a triple | largest certified failing shift: Fibonacci 1, Pell 0, (2,2;1,2) **6**, tribonacci 3, 4-bonacci 7, G+G(k−2) 10, (3,3;1,5) **11**, G+G(k−3) ≥ 14 (every s ≤ 14 fails); 1,3,4,7,11: {0,1,3} fail, {2, 4…14} no failure; 1,4,5,9,14: {0,1,2,3,5} fail |
| `python3 c08_targeted.py quadratic` | 627 quadratic Pisot sequences (p ≤ 8, \|q\| ≤ 8, g1 = 2…12), s = 0…16 | β > 0: 0/231 non-monotone; β < 0: 60/396 non-monotone, 0 canonical |
| `python3 c08_compare_lab.py` | the above vs EXP-C08-04's 90 rows | 31 rows contain certified-failing "associative" shifts; 4 of the 10 non-monotone rows are artefacts |
| `python3 c08_checks.py posbeta / negbeta` | the same families with random triples | 0/231 and 67/396 non-monotone (weaker test; kept for comparison) |
| `python3 c08_checks.py nonpisot` | 10 lab + 6 new non-Pisot sequences, s = 0…25 | every shift fails for every one of them (the two remaining entries, (1,2,1) and (1,1,1,2), turned out to be Pisot and geometric — controls, both associative from some s) |
| `./c08_assoc 2 2 -1 1 2 …` | G_k = k + 1 | associative at every tested s (provable: a ∘_s b = a + b + s − 1) |
| `python3 c08_verify_triples.py`, `c08_verify_more.py` | plain-Python big-integer re-verification | every failing triple quoted in this review confirmed |

**C09** (`./c09_circle X`, products from the Zeckendorf definition; conjugates compared exactly with ψ-powers via integer sign tests):

| X | irreducible ≤ X | irr. density | forced density | irr. fraction in zone | violations (window / shadow formula / reducible outside zone) |
|---|---|---|---|---|---|
| 10⁶ | 539,392 | 0.539392 | 0.381967 | 0.254719 | 0 / 0 / 0 |
| 10⁷ | 5,314,330 | 0.531433 | 0.381966 | 0.241843 | 0 / 0 / 0 |
| 10⁸ | 52,473,122 | 0.524731 | 0.381966 | 0.230999 | 0 / 0 / 0 |

- 928,760,784 pairs a ≤ b with ab ≤ 10⁸ were evaluated; the bound a∘b ≥ ab follows from F_{k+l} ≥ F_k F_l, so no monotonicity was assumed.
- First irreducibles: 1, 2, 4, 6, 7, 9, 10, 12, 14, 15, … as recorded.
- `python3 c09_fact.py 200000` (exact factorisation sets, no truncation; exact length-set DP; exact length-bound test): FACT_TABLE

**C10** (`python3 c10_checks.py <part>`):
- classical (N = 10⁶): see (a). Digit functions are validated against their values for n < 2000.
- zeckendorf: T_m brute force for m ≤ 30 = closed form = recurrence; the potential identity holds for n < 10⁶.
- exchange (31 rules, N = 4·10⁵):
  - max firing deviation 3.4·10⁻⁴;
  - single-offset rules: 0 increments with cost ≠ firings + 1, max |average − (1 + 1/(m−q))| = 1.4·10⁻⁴;
  - multi-offset excesses: 0.4999 (3→1,1), 0.6430 (3→0,1,1), 0.7142 (3→1,0,1), 0.3333 (4→1,1), 0.4998 (4→1,2), 0.2960 (4→2,1), 0.3744, 0.6752, 0.4865, 0.4284, 0.6999, 0.8317 (4→1,1,1), 0.4752;
  - the excesses are stable between N/4, N/2 and N.

**C11** (`python3 c11_checks.py <part>`): theory, codes, compare, oscillation, bench. All results are in (a); outputs in `out/c11_*.json`.

**C12:**
- `./c12_g03 100000000` (16.7 s): g = F for all n ≤ 10⁸. P-set = {0, odd, 2^(2j+1)}. Positions with g ≠ v₂ by odd part (1, 3, …, 15): 26, 24, 23, 21, 21, 21, 19, 20; none with odd part ≥ 17. Max \|g − v₂\| off odd powers of 2: 2 (first at 16).
- `python3 c12_checks.py step3`: mex equation for F at 2^a m, m ≤ 15 odd, 6 ≤ a ≤ 400: 0 failures. Offset sets {v − a : v ≥ a − 4}, presence of 0, and completeness of 1 … a − 5: identical for all a of each parity, 13 ≤ a ≤ 400.
- `python3 c12_checks.py step2`: exhaustive 17 ≤ m ≤ 3001, 1 ≤ a ≤ 60, and 2,912 random m with known factorisation, a ≤ 200: 0 failures.
- `python3 c12_checks.py divisor | coprime | misc | split`: 0 mismatches (ranges in (a)).
- `./c12_sub {squares,triangular,fibonacci,primes} N`: P-densities and maxima at 1.25·10⁴ … 2·10⁵ identical to EXP-C12-03; SUB_EXT

**R. Reproducibility.**
- `python3 repro_check.py`: the code sha256 stored in all 35 result files of the six cycles equals the current script (`out/repro_sha.json`).
- Lab re-runs (`python -m lab run <id>` from the repository root; `out/lab_reruns.log`):

| experiment | stored sha256 = current script | outcome |
|---|---|---|
LAB_RERUNS

---

## (c) Bugs and problems in code, records and documents

P1–P3 change mathematical conclusions. The others do not.

- **P1 (refuted conjecture, CLM-C05-09).**
  - Laws 677 and 1313 have models of order 16 (Appendix B). They are affine maps over GF(16), so they are not in reach of the ℤ_n affine search of EXP-C05-05 or of SAT at n ≤ 10.
  - Wherever the conjecture is repeated, it needs updating: the claim record, `textbook/src/06_magma_laws.md` (Conjecture 6.6, census table row "1000101?", open question 1), the C05 README (Next directions 2) and `record.yaml` (journal C05-12, next_directions).
- **P2 (wrong thresholds; stale records, CLM-C08-05).**
  - The claim still reads "(2,2;1,2) 5, tribonacci 3, 4-bonacci 7, G(k+1)=G(k)+G(k−2) 10, (3,3;1,5) 10" (history: created only). The C08 README (EXP-C08-03 row, "Thresholds: …") says the same.
  - All five values are refuted by explicit triples (Appendix C.1).
  - The lab's own correction EXP-C08-06 (17:04) and the corrected textbook chapter fixed tribonacci, 4-bonacci and G+G(k−2), but not the claim or the README.
  - EXP-C08-06 itself still reports "no failure found" at (2,2;1,2) s = 6 and (3,3;1,5) s = 10, 11. All three fail: (314965 ∘₆ 314965) ∘₆ 1 ≠ 314965 ∘₆ (314965 ∘₆ 1), and (173938 ∘ 173938) ∘ 1 ≠ 173938 ∘ (173938 ∘ 1) at s = 10 and at s = 11.
  - Root cause: random triples or pairs up to 10⁶ (and pairs below 300) rarely hit the extreme-conjugate inputs that break associativity. Choosing a, b with extreme conjugates finds them immediately (`c08_extreme.c`).
  - Every remaining "no failure found" threshold is computational support only (Fibonacci excepted).
- **P3 (contaminated evidence, CLM-C08-04).**
  - EXP-C08-04's test (cube [1,12]³ + 800 random triples ≤ 10⁵) is far too weak. 31 of its 90 rows list certified-failing shifts as associative, among them 8 rows with β > 0: (4,−2) with G₁ = 2, 3, 6 and (5,−3) with G₁ = 2…6 (Appendix C.2).
  - 4 of its 10 non-monotone rows are artefacts: (4,3;1,5) and (3,3;1,2) (found by the Historian), and (2,2;1,5) at s = 6 and (3,2;1,6) at s = 4 (new; EXP-C08-06 still lists them as non-monotone).
  - Consequently the chapter's "10 non-monotone sequences … two of the original ten examples were artefacts" (`09_circle_products.md`, Conjecture 9.2) should read: 8 on 0…10, 4 artefacts.
  - The conjecture itself survives the stronger search.
- **P4 (overstated certification, CLM-C09-08 / EXP-C09-02).** FACT_PROBLEM
- **P5 (floating-point boundary, EXP-C09-04).**
  - The script tests ψ³ < nψ + n* < ψ² in floating point. For n = 1 the value is exactly ψ² (a boundary point), but it rounds to 0.3819660112501051 < 0.3819660112501052, so n = 1 is counted inside the open zone.
  - n = 1 is irreducible, so no theorem is affected. The reported "irreducible fraction inside the zone" (0.315534 at 10³) and "forced density" (0.382 at 10³, 0.381966 at 10⁶) are off by that one count. Exact values: 0.314425 and 0.383 at 10³, 0.381967 at 10⁶.
  - The script's safety argument names this very boundary case.
- **P6 (missing proof, CLM-C09-07).** The record cites Theorem 1 of `C09.md` as the proof, but the bound \|N(n)\| < (√5/φ)n + 1 is not proved there. A one-line proof is in A.2.
- **P7 (evidence wording, CLM-C10-05).**
  - EXP-C10-03 computes `J1_prediction` and `max_J1_change_deviation` only for rules with len(b) = 1.
  - The claim's "deviation ≤ 2.7e-4 for all single-offset rules" therefore covers 5 of the 18 single-offset rules. The other 13 (offset 2, 3) match too, but that was not what was summarised.
  - My check covers all 18, increment by increment.
- **P8 (cosmetic, EXP-C10-01).** "n < 10⁶" averages are over the 999,999 increments n → n+1, n ≤ 999,998: binary 1,999,986/999,999 = 1.999988. That is why the worst decimal cost is 6, not 7.
- **P9 (C08 README/claims vs textbook).** The textbook (`09_circle_products.md`) carries the 2026-10-18 correction; `research/cycles/C08_circle_products/README.md` and CLM-C08-05 do not (see P2).
- **P10 (wording, CLM-C08-02).**
  - The intended statement needs a dominant root α > 1 and a rule for repeated roots.
  - G_k = k + 1 has minimal polynomial (x − 1)², and a ∘_s b = a + b + s − 1 is associative for all s. EXP-C08-02's classifier (`other root moduli ≥ 1 − 1e-9` ⇒ "non-Pisot") would label this sequence non-Pisot.
- **P11 (title, CLM-C09-03).** "A fixed proportion 1/φ² of all integers are circle-irreducible" suggests the irreducibles have density 1/φ²; that is Conjecture CLM-C09-05. The theorem gives "at least 1/φ²" (observed 0.5247 at 10⁸).
- **P12 (minor, C05 textbook census table).** Row "10011??1" for law 167 keeps "?" at n = 6, 7 although Theorem 6.2 decides both (absent). The README table has the same "?".

Audited and found correct:
- `MagmaSAT` (indirectly: my independent encoder reproduces every census and frontier status I recomputed).
- EXP-C05-03's `latin_rows` is applied exactly to the laws x = y∗(…), where it is sound.
- `BaseSequence.greedy` / `circle` (indirectly: identical failures and passes on all common test points).
- `circle_arith.shadow` (exact `isqrt` floor identity).
- `PatternCode` ranking.
- `FraenkelKleinC3.length`.
- The G03 certificate functions of EXP-C12-06.
- `grundy_subtraction`'s bitset method (P-densities identical to mine).

Faults in my own harness, fixed before the reported runs:
- My first C08 checker refused large inputs for slowly growing sequences (table too short), so all random triples for G_k = k + 1 were skipped. Only its cube result is used, and that case is settled by the one-line proof.
- `c11_checks.py bench` first crashed on a too-short Fibonacci table; fixed and re-run.
- `c10_checks.py exchange` first used a fixed 80-level array, too short for 4 → (0,0,3); replaced by 400 levels before the run.
- My attempt to stop the frontier run with `pgrep -f … | kill` also matched my own issuing shell. That command aborted after stopping the intended Python process; the frontier log was complete up to 677@7 and was converted to `out/c05_frontier_summary.json`. No other process was touched.
- The first version of `c05_order16.lean` lacked `import Mathlib.Tactic` (the `![…]` notation failed); fixed and re-compiled.

---

## Appendix A — checks of the written proofs

**A.1 C05 (Lemmas 0, 1, 4; Theorem 2; Remark 5).**
- Lemma 0: forward linking clauses force the true value of each subterm; at-most-one makes it the only one. Correct.
- Lemma 1: along the path to the unique occurrence of x, T₁∘…∘T_k = id for fixed values of the other variables. So T_k is injective and T₁ surjective, hence both are bijections, and by induction on the shorter composition every T_i is. Correct.
- Lemma 4:
  - (a) is Lemma 1.
  - (b): relabelling by the transposition (1 a) fixes 0 and maps the value a at (0,0) to 1. Identities and "rows are permutations" are isomorphism-invariant, so (a) and (b) are jointly sound. Correct.
- Theorem 2: the Lean proof is the fixed-point-free involution on Sym2 minus the diagonal. Sufficiency checked numerically (see (a)).
- Remark 5: re-computed mod 3. With x∗y = (1+i)x + iy on ℤ[i]/(3): y∗y = (1+2i)y; x∗(y∗y) = (1+i)(x+y); x∗(x∗(y∗y)) = 2i x + (i−1)y; y∗(…) = −2x = x. Correct.

**A.2 C09 (Theorems 1, 3, 4; the bound of CLM-C09-07).**
- Theorem 1:
  - Expanding (aφ + a*)(bφ + b*) with φ² = φ + 1 gives a∘b = ab + ab* + a*b and (a∘b)* = ab + a*b*.
  - ν(n) ≥ φ² > 1, and a unit φ^k = F_kφ + F_{k−1} forces n = F_k, k ≥ 2.
  - N is the field norm.
  - −ψ² < nψ + n* < −ψ is n* ∈ ((n+1)/φ − 1, (n+1)/φ).
  - "No identity": a∘b ≥ 1∘b > b. Correct.
- Theorem 3:
  - For u, v ∈ (−ψ², −ψ), uv ∈ (ψ³, ψ²): infimum (−ψ²)(−ψ) = ψ³, supremum (−ψ)² = ψ².
  - ν′(n) = 1/φ − f(n), and the zone has length ψ² − ψ³ = 1/φ.
  - Weyl applies to (n+1)/φ. Correct.
- Theorem 4: \|ν′(a_i)\| < max(ψ², −ψ) = \|ψ\| and ν′(n) ≠ 0. Correct.
- CLM-C09-07 bound (missing in the paper):
  - ν(n) = nφ + n* < nφ + (n+1)/φ = n√5 + 1/φ, and \|ν′(n)\| < 1/φ.
  - Hence \|N(n)\| < (√5/φ)n + 1/φ² < (√5/φ)n + 1.

**A.3 C08 Theorem 1.**
- Step (3) holds for every finite K ⊂ [2, ∞), not only Zeckendorf sets: the even part is < Σ_{j≥1} φ^{−2j} = 1/φ, and the odd part is < ψ².
- Steps (5)–(9) checked.
- The Lean variant (\|E′\| < −ψ, hence \|Q − P*\| < ψ² + (−ψ) = 1) is also valid. Correct.

**A.4 C10 Theorems 1–4.**
- Theorem 1: in negabinary and balanced ternary, digit k depends only on n mod b^(k+1). The digit-k-specific residues form one cyclic interval of length b^k per digit value, so digit k changes with frequency b^(−k).
- Theorem 2: block decomposition; induction on the closed form with ⌈(m+1)/2⌉ = ⌈(m−1)/2⌉ + 1.
- Theorem 3:
  - #firings = (n − s(n))/(m − B) by token counting, whatever the firing order.
  - s(n) = O(log n) because the value Σ c_k r^k = n is conserved, where r > 1 solves Σ b_j r^j = m (it exists since B < m).
  - The abelian property is needed only to identify the stable configuration with rep(n).
- Theorem 4:
  - Each level receives from one level only (single offset). A receiving level goes from ≤ m − 1 to ≤ 2m − 2, so it fires at most once.
  - Fired levels change by 1 − m or q − m ≠ 0, and the last receiver changes by q or 1. Correct.

**A.5 C12 Theorems 1, 2, 4, 5 and 8.**
- Theorems 1, 2, 4, 5(b) re-derived step by step:
  - Theorem 2(b): an odd option of 2k is ≤ 2k − q ≤ 2k − 3, so its value is ≤ k − 2.
  - Theorem 4(b): the options of n are exactly the residues r < n/2.
  - Theorem 5(b): the four residue cases.
- **Theorem 8 (CLM-C12-04).**
  - Step 1: the zero set of F equals the Lean P-set. Correct.
  - Step 2 (m ≥ 17):
    - (i) n − 2^j has odd part 2^(a−j)m − 1 ≥ 33; n − m is odd.
    - (ii), i < a: the odd cofactor 2^(a−i)m − e ≥ m ≥ 17 (also for i = 0, where the option is odd).
    - (ii), i = a: e is a proper divisor of the odd m, so e ≤ m/3 and 2e < m, i.e. n < 2x. Hence x > 5·10⁴ and the exponent b = a + k ≥ 12 ≥ 6.
    - e \| m′ because the odd e divides 2^k m′.
    - Stable values equal to a: only (m′, k) = (1, 1) (then m = 3) or (3, 2) (then m ∈ {13, 15}). Correct.
  - Step 3 (m ≤ 15, a ≥ 13):
    - Options with t ≥ 5 give exactly {1, …, a − 5}, plus 0 iff m > 1.
    - Options with t ≤ 4 have exponent a − t ≥ 9, and options with i = a have exponent ≥ 14, so all their values are stable values a + const (or 0 / b − 1 for odd part 1).
    - The offsets depend only on (m, a mod 2), so the mex is 0 or a + δ(m, a mod 2). Checking one exponent per parity suffices.
    - Correct. My computation confirms both the mex equation and the invariance of the offset sets on 13 ≤ a ≤ 400.

**A.6 C11 Theorems 1–3, Corollaries 4, 6, Proposition 5.**
- Theorem 1(c): 1 + 2xA = A + F and x^k A = c_p F.
  - Conversely, a codeword followed by the last j letters of p (j a period) is wp with w avoiding p.
- Theorem 2: D_p > 0 on (0, 1/2], and D_p(1) = 1 − c_p(1) ≤ 0, so ρ_p ∈ (1/2, 1] exists.
  - The numerator x^k does not vanish there, so Pringsheim gives the radius.
  - The comparison argument is correct.
- Theorem 3: the algebra re-done; 1 − 2x + x^(k+1) = (1 − x)(1 − x − … − x^k).
- Corollary 4: the condition F_{L+1} ≥ L + 1 holds for L ≥ 4, and n ≤ 4 is checked directly.
- Proposition 5:
  - 1 < r = 1/(λ − 1) ≤ λ.
  - The level structure (verified numerically, see (a)) gives the maxima at N = cum_U(L−1) and the minima at N = cum_O(L).
  - The geometric sums give (r − 1)/(λ − 1) and (r − 1)λ.
- Corollary 6: F_{L+2} − 2F_L = F_{L−1}. Correct.

## Appendix B — order-16 models of laws 677 and 1313 (refutes CLM-C05-09)

- **Law 677.** For an affine operation x∗y = ax + by over a commutative ring, x = y(x((yx)y)) expands to (ab + ab³)x + (a + a²b² + b³)y = x. So the law holds iff ab(1 + b²) = 1 and a + a²b² + b³ = 0.
- **Law 1313.** x = y(((yx)x)y) gives (a²b² + ab²)x + (a + a³b + b²)y. So it holds iff ab²(a + 1) = 1 and a + a³b + b² = 0.
- **Idempotent case in characteristic 2** (b = 1 + a):
  - Law 677 reduces to b⁴ + b³ + b² + b + 1 = 0, after which ab(1 + b²) = b(1 + b)³ = b + b² + b³ + b⁴ = 1 holds automatically.
  - Law 1313 reduces to the same equation for a.
  - So a primitive 5th root of unity is needed. GF(16) has one: t³, with t⁴ = t + 1.
- **The models.** In GF(16) = GF(2)[t]/(t⁴ + t + 1), elements as 4-bit masks (bit i ↔ tⁱ):
  - 677: x∗y = (1 + t³)x + t³y, i.e. (a, b) = (9, 8).
  - 1313: x∗y = t³x + (1 + t³)y, i.e. (a, b) = (8, 9).
  - In fact `c05_gf16.py` finds 8 pairs (a, b) for each law over GF(16), checked by brute force over all 256 (x, y). It finds none over GF(8), GF(4), ℤ₈, ℤ₁₀ or ℤ₁₆.
  - The tables are in `out/c05_gf16.json`.
  - LEAN_B
- **Consequences.** 16 lies in both spectra, so neither spectrum is {1} ∪ {odd n ≥ 5}. Spectra are closed under products, so 80 = 5·16 and 112 = 7·16 are in too.
- **Further members.** Over odd characteristic, the idempotent affine models of 677 exist iff GF(q) contains a primitive 10th root of unity, i.e. 10 \| q − 1. Examples: q = 11, 31, 41, 61, 71, 81. These are odd orders, consistent with the old conjecture.
- **Still open.** Orders 8 and 10.

## Appendix C — C08 thresholds and false "associative" entries

**C.1 Thresholds of CLM-C08-05.**
- My columns come from the targeted extreme-conjugate search (`c08_targeted.py thresholds`) and the random-triple search.
- Every triple below was re-verified with plain Python big integers.

| sequence | CLM-C08-05 | EXP-C08-06 (largest failure / next) | my largest certified failure | certifying triple(s) (a, b, c) | my first shift with no failure found |
|---|---|---|---|---|---|
| Fibonacci 1,2 | 2 | 1 / 2 | 1 | (1,4,4) at s = 1 | 2 (and every s ≤ 24) |
| Pell 1,2 | 1 | 0 / 1 | 0 | (275806, 275806, 2) at s = 0 | 1 |
| (2,2) 1,2 | **5** | 5 / 6 | **6** | (314965, 314965, 1) at s = 6; (29957, 280628, 1) at s = 5 | 7 |
| tribonacci 1,2,4 | **3** | 3 / 4 | 3 | (387502, 390638, 1); AFMP's (10016, 10016, 1) | 4 |
| 4-bonacci 1,2,4,8 | **7** | 7 / 8 | 7 | (348872, 348872, 1); (384723, 160586, 707599) | 8 |
| G(k+1)=G(k)+G(k−2) 1,2,3 | **10** | 10 / 11 | 10 | (164049, 164049, 1); (194040, 37982, 925743) | 11 |
| (3,3) 1,5 | **10** | 9 / 10 | **11** | (173938, 173938, 1) at s = 10 and s = 11; (84247, 985522, 148455) at s = 10 | 12 |
| G(k+1)=G(k)+G(k−3) 1,2,3,4 | none ≤ 20 | — | every s ≤ 24 fails | (1, 6, 6) | none ≤ 24 |
| 1,3,4,7,11 (CLM-C08-04 example) | {2} ∪ [4, …) | same | fails at 0, 1, 3 | (1,2,6) at s = 3 | 2 and 4…24 |
| 1,4,5,9,14 | {4} ∪ [6, …) | same | fails at 0–3, 5 | (1,8,8) at s = 5 | 4 and 6…14 |

**C.2 Rows of EXP-C08-04 with certified-failing "associative" shifts.**
- Format: p, q; G₁ → failing shifts (`out/c08_compare_lab.json`).
- β > 0: (4,−2; 2) → 3; (4,−2; 3) → 3; (4,−2; 6) → 4; (5,−3; 2) → 5; (5,−3; 3) → 7; (5,−3; 4) → 6; (5,−3; 5) → 7; (5,−3; 6) → 7.
- β < 0:
  - (2,2): G₁ = 2 → 4,5,6; G₁ = 4 → 6,7; G₁ = 5 → 6; G₁ = 6 → 9.
  - (3,2): G₁ = 2 → 3; G₁ = 5 → 5; G₁ = 6 → 4.
  - (3,3): G₁ = 2 → 7,9,10; G₁ = 3 → 9,10; G₁ = 4 → 8,9,10; G₁ = 5 → 10; G₁ = 6 → 10.
  - (4,2): G₁ = 2 → 2; G₁ = 4 → 2; G₁ = 5 → 2,3.
  - (4,3): G₁ = 2 → 5,6; G₁ = 3 → 5; G₁ = 4 → 5; G₁ = 5 → 4; G₁ = 6 → 6,7.
  - (5,3): G₁ = 3 → 4; G₁ = 5 → 4,5; G₁ = 6 → 5.
- Total: 31 of 90 rows. Note that the first group consists of β > 0 rows; with corrected sets they remain upward-closed.
