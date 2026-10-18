# Skeptic review of cycles C14, C15, C16 and C18

**Reviewer:** Mathematical Skeptic (independent of the researchers who produced the claims)
**Date:** 2026-10-18 · **Scope:** CLM-C14-01 … 13, CLM-C15-01 … 18, CLM-C16-01 … 19, CLM-C18-01 … 13 (63 claims).

**Material read:**
- The four cycle READMEs and `record.yaml` files (claims, experiment analyses, journals); all 63 claim records in `db/claims/`.
- `proofs/paper/C14.md`, `C15.md`, `C16.md`, `C18.md`; the Lean files `C14_GraphProducts.lean`, `C15_MagmaCA.lean`, `C16_Dynamics.lean`, `C18_Quasigroups.lean`.
- All scripts in `experiments/C14`, `C15`, `C16`, `C18`; `systems/graph_products.py`, `magma_ca.py`, `magma_dynamics.py`, `quasigroup_hash.py`; the relevant parts of `lab/runner.py`.
- All `results/EXP-C14-*`, `C15-*`, `C16-*`, `C18-*` files; their run histories in `db/experiments/`.
- Textbook chapters 15, 17, 18, 20 (searched for strong statements, key passages read).
- Literature for one novelty point: A. Abiad, S. Butler, W. H. Haemers, *Graph switching, 2-ranks, and graphical Hadamard matrices*, [arXiv:1801.01149](https://arxiv.org/abs/1801.01149) (read: §§4–5). Found through a web search on Kronecker products of graphical Hadamard matrices, which also returned [Goethals–Seidel 1970](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8ECA2731AAE39670EFFCA9B3B3DBF75C/S0008414X00047271a.pdf/strongly-regular-graphs-derived-from-combinatorial-designs.pdf) (not read).

**Rules followed:**
- No existing file was edited by hand. My code is in `reviews/skeptic_checks/C14_C18/`, raw outputs in its `out/` subfolder.
- My scripts do not import `systems/` or `lab/`, with three disclosed exceptions:
  - `c15_crossover.py` times the lab's own fast-forward functions, because the claim being checked is about them.
  - `audit_nim.py` imports `systems/quasigroup_hash.py` only to compare its nim table with mine.
  - Some scripts *read* stored lab results or data to compare or to reuse inputs: EXP-C14-04 counts; the OEIS cache values of A000088, A001349, A129582 and A002854; the class order of EXP-C15-02 (asserted equal to my own order); the stored C16 certificates.
- Libraries used: numpy, scipy (bipartite matching only), sympy (equation solving only), hashlib (BLAKE2b). All graph isomorphism, canonical forms, switching tests, automata, pair maps, Latin squares, hashes and the nim table are my own code (C or Python).
- Lab experiments re-run (allowed): EXP-C14-01, EXP-C15-03, EXP-C15-05, EXP-C16-01, EXP-C16-02, EXP-C18-04, EXP-C18-05.
  - This rewrote those seven `results/*.json` files and appended runs to `db/experiments/*.json` and `db/audit_log.jsonl`.
  - The pre-run result files are kept in `out/lab_rerun_before/`.
  - The audit log now holds a `reproduced: false` entry for EXP-C16-01. It is a false alarm caused by bug P1.
- Not run: `lab sync`, `lab lean`, `lab book`, any git command.
- Every computation ran under `nice -n 10`, one heavy job at a time. The longest was 81 s (the exhaustive affine check). Every check below was actually run.

## Bottom line

- **No claim is refuted. No code bug invalidates a mathematical conclusion.** Every number I recomputed with my own code agrees with the records.
  - This includes the complete factorisation census of EXP-C14-04: all 8 products, all and connected graphs, orders ≤ 15, with identical class, factorisation and prime counts.
  - It also includes the 1734-class automaton census (identical λ sequences per class) and the 3360 full-period quasigroups of order 5.
- **All written proofs awaiting review are correct** (step checks in Appendix A):
  - CLM-C15-01, -02, -03, -04;
  - CLM-C16-03, -04, -05, -08, -09, -12, -14, -15;
  - the written parts of CLM-C14-04 … -09 and CLM-C18-01 … -07.

  CLM-C15-04's upper bound needs one extra sentence (A.2).
- **Lean:** all four files compile (exit 0) with only propext / Classical.choice / Quot.sound, and contain no `sorry`, `admit` or `native_decide`. Coverage is stated honestly in every `proof_check`.
- **Novelty:** CLM-C14-06 is not novel. Abiad–Butler–Haemers (2018, §5) define exactly this graph product and state that its Seidel matrix is (S₁+I)⊗(S₂+I) − I. They also use its compatibility with Seidel switching. **Recommend REDISCOVERY.**
- **Conjectures survive much larger searches:**
  - CLM-C14-13: 0 collisions among all 53,703 multisets of prime two-graphs with ≤ 8 vertices and product order ≤ 64 (lab: 350 multisets, order ≤ 16).
  - CLM-C16-13: holds for every one of the 1,997,716 affine magmas with β a unit, 2 ≤ N ≤ 60 (lab: 300 random cases).
  - CLM-C16-10: new examples for every order 17–26.
  - CLM-C16-16: the transient is still 5 for n ≤ 13.
  - CLM-C15-04: λ(t) = t + 2 holds to t = 14.
- **Main problems** (details in (c)):
  - P1: EXP-C16-01 stores a wall-clock `seconds` value inside the hashed results, so every re-run reports CHANGED. Confirmed.
  - P2: the C15 README's "Semigroups (width ≤ |S|) … as proved" is false beyond the commutative case. For S₃, λ(t) = 6, 6, 6, 36, 72, 216, 1296 for t = 0…6.
  - P3: "the affine and fuse fast-forwards never lose" is false. Under an equal timing protocol they lose for t below roughly 20–70.
  - P4: the benchmark protocol is asymmetric (best of 3 against 1 run), and the recorded speedups and MB/s figures do not reproduce to the precision stated. The fuse "≈ 4000×" was 1363× on re-run.
  - P5: the "4–5 orders of magnitude" for spectra comes from BLAS thread oversubscription; the gap is about 3 orders otherwise.
  - P6: novelty of CLM-C14-06 (above).
  - P7, P8: in C18, "like FNV-1a, |z| ≤ 3" is false, and FNV-1a's negative z is misread as a defect. H-C18-2 is worded more broadly than it was tested.

---

## (a) Verdicts

| Claim | Verdict | Details | Recommended status change |
|---|---|---|---|
| CLM-C14-01 (associativity ⇔ 27-triple identity ⇔ P₃³) | **UPHELD** | Lean re-run OK; `rel_lprod`, `assoc_iso` and `assoc_of_P3` state (3⇒1) and (2⇒3) for arbitrary vertex types. The commutative half is written only, as recorded. Own check: the relation-level verdict equals the P₃³ graph-level verdict for all 256 codes, and 60 random triples never break an associative code. | None. |
| CLM-C14-02 (20 associative, 10 commutative, 8 unital) | **UPHELD** | Own recount: exactly the 20 listed codes; 32 symmetric codes; 10 commutative and associative. Unit K₁ was tested by isomorphism on all graphs ≤ 4 vertices: exactly the 8 listed. 76 orbits; the 20 associative codes form exactly the 8 listed orbits. 10 of them depend on both factors, 8 of those commutative (the Nowakowski–Rall numbers). | None. |
| CLM-C14-03 (up-to-isomorphism no weaker) | **UPHELD** | Own minimal-witness search: minimal product orders {2: 144, 4: 84, 8: 8}, every minimal witness certified by degree sequence. All 224 non-commutative codes have degree-certified witnesses of order 2 (192 codes) or 4 (32). | None. |
| CLM-C14-04 (six multiplicative characters) | **UPHELD** | Case analysis checked (A.1). Independent derivation: equations taken from the full 9×9 matrix identity on P₃×P₃, not from the cell analysis, and solved by sympy over ℂ. Result: exactly codes 8, 13, 85, 93, 127, 141, each with the stated unique c. The identity holds numerically on 40 random pairs per character. Lean covers only values in {−1,0,1}, as stated. | None (see the novelty note under C14-06). |
| CLM-C14-05 (additive characters) | **UPHELD** | Proof checked. Own sympy: exactly Cartesian (0,t,0) and 221 (0,0,t). Empty and complete are the only commutative associative codes without a character, and no code has both kinds. | None. |
| CLM-C14-06 (XOR = Kronecker product of S+I) | **UPHELD WITH CAVEATS** (novelty) | The mathematics is correct: the identity is exact in integers on 624 pairs, and switching compatibility follows. But Abiad–Butler–Haemers, arXiv:1801.01149 §5, define this product and state that "the Seidel matrix of G₁ ⊗ G₂ equals (S₁+I)⊗(S₂+I) − I". Their F₂ formula A₁⊗J + J⊗A₂ shows it is the XOR product; their verbal definition has the adjacency rule inverted. Their proof of Thm 5.1 uses compatibility with Seidel switching. | Novelty POTENTIALLY NOVEL → **REDISCOVERY** (cite arXiv:1801.01149 §5). |
| CLM-C14-07 (bipartite rule; K₂ absorbs switching) | **UPHELD** | Proof checked (A.1). (a) All 1225 cases a,b,c,d ≤ 5 give complete bipartite graphs with the predicted parts. (b) The explicit map Π of the proof is an isomorphism in 300 random cases. (c) For all graphs ≤ 6 vertices, the invariants of K₂⊕X are constant on switching classes and separate the 1+1+2+3+7+16 classes. | None. |
| CLM-C14-08 (H-C14-3 refuted) | **UPHELD** | Own: K₂⊕K₂⊕K₂ and K₂⊕K₁,₃ are both K₄,₄, and K₁,₃ is prime. The own census reproduces the connected XOR collisions at orders 8/10/12/14 (2/6/15/53 classes). | None. |
| CLM-C14-09 (□ and ⊠ monoids isomorphic) | **UPHELD** | Proof correct given the cited UPF theorems (A.1). Own census: equal prime counts for □, ⊠, ∨ and 221 for n ≤ 15; connected □- and ⊠-primes equal A129582 for n = 2…15. | None. |
| CLM-C14-10 (prime counts) | **UPHELD** | The own census (own graph generation and own exact isomorphism) reproduces every composite-class count and every prime count for n = 2…15, for all 8 products. Totals come from cached A000088. | None. |
| CLM-C14-11 (lexicographic collision at order 10) | **UPHELD** | Both isomorphisms found by my own search. The lexicographic census has no multiset collision at orders 4, 6, 8, 9; there are 2 at order 10 and 6 at order 14. | None. |
| CLM-C14-12 (141 UF on connected graphs) | **UPHELD** (conjecture) | Own census: no collision for 141 on connected graphs at any order ≤ 15. | Keep COMPUTATIONALLY SUPPORTED. |
| CLM-C14-13 (two-graphs free under ⊕) | **UPHELD** (conjecture survives a much larger search) | Own switching classes for n ≤ 8 equal A002854; primes are 1, 2, 2, 7, 14, 54, 240; no collision to order 16 (350 multisets). Extension: every multiset of prime classes with ≤ 8 vertices and product order ≤ 64 (53,703 multisets) was screened by exact integer power sums tr((S+I)^k). This gave 2,205 cospectral groups (largest 6 members); all 3,012 pairs were decided by exact switching-equivalence tests, with 0 collisions. Caveats: (i) the lab's evidence to order 16 was thin, since most composites contain [K₂] and are covered by the proved cancellation (C14-07c); (ii) the product itself is implicit in Abiad–Butler–Haemers. | Keep COMPUTATIONALLY SUPPORTED; record the extension. |
| CLM-C15-01 (semigroup light cones) | **UPHELD** | Proof checked (A.2). Lean `ca_comm_binomial` plus the adjoined-identity remark is valid. Popcount word checked in S₃ on 300 random cases; every order-3 semigroup has λ ≤ 3. The claim limits the width bound to commutative semigroups, correctly, but the README extends it to all semigroups (P2). | Mark skeptic-reviewed; fix README. |
| CLM-C15-02 (affine fast-forward) | **UPHELD** | Proof checked. My own exact (FFT-free) operator-power implementation equals direct simulation in 252 cases (6 affine magmas incl. ℤ₇, t ≤ 1000). | Mark skeptic-reviewed. |
| CLM-C15-03 (exponent arithmetic) | **UPHELD** | Proof checked; t ≥ 2L+ι+1 is more than sufficient (t ≥ max(L+1, ι) suffices). My own version with exact binomials equals simulation for all 63 commutative semigroup tables of order 3 (756 cases). | Mark skeptic-reviewed. |
| CLM-C15-04 (fuse magma) | **UPHELD** | Proof checked (A.2), including the lower-bound threshold b+1+(t−2m). The upper bound needs one sentence (A.2). Burn-time formula against simulation: 870,969 exhaustive (row, t) cases (cyclic L ≤ 9, t ≤ 3L+3) plus random rows, 0 mismatches. λ(t) = t+2 for t = 1…14 (lab: to 12). | Mark skeptic-reviewed; optionally record t ≤ 14. |
| CLM-C15-05 (surjective ⇔ permutive, order ≤ 3) | **UPHELD** | Own pair-graph test: 420 surjective tables, exactly the 420 permutive ones; all 16 of order 2; the order-4 band is surjective and injective but not permutive. Cross-check with bijectivity of cyclic maps for L ≤ 8: no conflict. | None. |
| CLM-C15-06 (rules 17m) | **UPHELD** | Own: rules 0, 17, …, 255; surjective rules 51, 85, 102, 153, 170, 204. | None. |
| CLM-C15-07 (order-3 census) | **UPHELD** | Own census: 808 / 104 / 300 / 522, max λ(9) = 649, 43 surjective, 7 injective, 34 nilpotent. The λ sequence of every class equals the lab's. The classes are heuristic on t ≤ 9, as the record says. | None. |
| CLM-C15-08 (H-C15-1 refuted) | **UPHELD** | Fuse: proof plus λ(t) = t+2 to t = 14. | None. |
| CLM-C15-09 (H-C15-2 refuted) | **UPHELD** | 685 bounded classes outside the three classes confirmed. The reversible table has λ ≡ 3 with all t+1 cells essential. Scope note: order 3 only (S₃ shows semigroups can have growing width). | None. |
| CLM-C15-10 (H-C15-4 refuted) | **UPHELD** | Fuse: unbounded width yet an O(L) fast-forward. | None. |
| CLM-C15-11 (H-C15-5 refuted in part) | **UPHELD** | Reproduced exactly with the same seeds (1590/1734 at L = 32). The refutation rests on the 5000-step cap: at L = 32 the affine quasigroups do repeat, after 6,560–19,681 steps (x+y: μ = 1, λ = 6,560; 2x+2y+1: μ = 1, λ = 19,680). At L = 64 none repeats within 200,000 steps. | None (wording note P15). |
| CLM-C15-12 (H-C15-6 refuted) | **UPHELD WITH CAVEATS** | Valid through the ">100×" clause: commutative-semigroup speedups at L = 1024, t = 10⁵ were 62–100× (lab) and 79–97× (my re-run). The second reason given, that affine and fuse "never lose", is false for small t (P3, Appendix C), so the hypothesis' "loses for small t" part partly holds. | Reword the counterexample text. |
| CLM-C15-13 (affine fast-forward speedups) | **UPHELD WITH CAVEATS** | Exactness confirmed (own formula; lab re-run reproduces 99/99). The ranges come from one run with an asymmetric protocol. Re-run: 202–314× at t = 10⁴ and 1459–2262× at 10⁵ (recorded 138–215× and 1800–2500×); t = 10⁹ took 0.8–4.9 ms. It loses for t ≲ 20. | Give orders of magnitude, note the small-t loss. |
| CLM-C15-14 (exponent-arithmetic speedups) | **UPHELD WITH CAVEATS** | Same protocol caveat. Re-run: 79–97× at 10⁵, 0.9–1.0× at 10³. MIXED is right. | None beyond P4. |
| CLM-C15-15 (fuse fast-forward speedups) | **UPHELD WITH CAVEATS** | Exact (my own burn-time code). The "about 4000× at t = 10⁵" was 1,363× on re-run. Because the O(L) method is a Python loop, it loses to simulation for t ≲ 20–70. | Restate as about 10³×, with a small-t crossover. |
| CLM-C15-16 (cycle detection) | **UPHELD** | Reproduced exactly: 1590 at L = 32, medians 5 and 2. Non-repeating classes: 128 geometric, 12 other, 4 bounded (the affine quasigroups). | None. |
| CLM-C15-17 (earlier structures as automata) | **UPHELD** | Own Laver tables (LD checked): ≤ 3 and ≤ 4 essential cells; streaming (forward) widths 4 and 8, while the backward widths are 5 and 13–14. GF(4) and XOR on [0,4) have width 4; the anchored models are permutive. | Say "streaming width". |
| CLM-C15-18 (bounded width ⇒ fast-forward) | **UPHELD** (status) | Open conjecture; nothing found against it. | None. |
| CLM-C16-01 (pair map bijective ⇔ rows bijective) | **UPHELD** | Lean re-run OK. Own counts 4, 216, 331,776. | None. |
| CLM-C16-02 (H-C16-1 refuted) | **UPHELD** | x⋆y = 1−y is a single 4-cycle. No full-period table of order 2–4 is a quasigroup; the quasigroup maxima are 3, 8, 15. | None. |
| CLM-C16-03 (de Bruijn bijection, (n!)ⁿ/n²) | **UPHELD** | Proof checked (A.3). Own exhaustive counts: 1, 24, 20,736. | Mark skeptic-reviewed. |
| CLM-C16-04 (parity condition) | **UPHELD** | Proof checked. The parity holds for every full-period table of orders 3, 4, 5 and every certificate of order 6–26 (own). | Mark skeptic-reviewed. |
| CLM-C16-05 (distance-2 characterisation) | **UPHELD** | Proof checked. | Mark skeptic-reviewed. |
| CLM-C16-06 (H-C16-5 refuted) | **UPHELD** | Own: 3360 of 161,280; the quoted cycle is a full-period quasigroup. | None. |
| CLM-C16-07 (0, 0, 0, 3360; orders 6–16; products) | **UPHELD** | Own Latin-square enumeration: 0, 0, 0, 3360; 28 isomorphism classes, all of size 120 (trivial automorphism groups). All 11 stored certificates and the 8 coprime products re-verified. | None. |
| CLM-C16-08 (coprime products) | **UPHELD** | The CRT proof is correct. All 8 products are full-period; a 6×6 control is not (max cycle 36). | Mark skeptic-reviewed. |
| CLM-C16-09 (even-order isotope obstruction) | **UPHELD** | Proof checked, including the Burnside step (A.3). Own check over 36 groups of even order 2–30 (incl. Q₁₆, Dic₃, Dic₅, A₄, S₄, ℤ₂×A₄, D₁₅): ∏ sgn λ_g = (−1)^m exactly; every sampled isotope has (−1)^m, and none is full-period. The lab never tested the n = 5 case of the parenthetical, but it is true: 480 of the 3360 are isotopes of ℤ₅ (own isotopy test). | Mark skeptic-reviewed. |
| CLM-C16-10 (existence for all n ≥ 5) | **UPHELD** (conjecture survives) | My own sampler found verified examples for every n = 17…26, and full-period ℤₙ-isotopes for odd n ≤ 21. "Rates close to 1/n²" is loose: the exact rate at n = 5 is 0.52/n², and the lab's samples pool to 139 hits against 181 expected (P10). | Keep COMPUTATIONALLY SUPPORTED; extend the range. |
| CLM-C16-11 (fixed points) | **UPHELD** | Lean re-run OK. | None. |
| CLM-C16-12 (affine with fixed point: companion order) | **UPHELD** | Proof checked. Own exhaustive check of all 1,575,671 affine magmas with β a unit and a fixed point, 2 ≤ N ≤ 60: the maximal period equals ord([[0,1],[β,α]]) in every case. | Mark skeptic-reviewed. |
| CLM-C16-13 (max period = order of 3×3 matrix) | **UPHELD** (conjecture; much stronger evidence) | Own exhaustive check of all 1,997,716 affine magmas with β a unit, 2 ≤ N ≤ 60: the maximal cycle length equals the lcm of all cycle lengths in every case, and that lcm equals the directly computed matrix order for N ≤ 24. Partial proof idea: if γ is a unit, e₃ is a cyclic vector (det[e₃, Âe₃, Â²e₃] = −γ²). | Keep COMPUTATIONALLY SUPPORTED; record "exhaustive for N ≤ 60". |
| CLM-C16-14 (nimbers) | **UPHELD** | Own nim table from Conway's mex definition. Maximal periods 8, 40, 360 = π(3), π(15), π(255); pairs containing 0 reach (0,0) within 2 steps. | Mark skeptic-reviewed. |
| CLM-C16-15 (Laver: fixed point + 2-cycles) | **UPHELD** | Proof checked. Own Laver tables for n ≤ 13: one fixed point and N−1 two-cycles, and every orbit reaches the top element. | Mark skeptic-reviewed. |
| CLM-C16-16 (Laver transients 5) | **UPHELD** | Maximal transient 1, 3, 3, then 5 for every n = 4…13 (lab: n ≤ 10). | Optionally extend to n = 13. |
| CLM-C16-17 (PRNG: no improvement) | **UPHELD** | Own: lowest-bit period 3; low-byte χ² = 3.2·10⁵ (df 255). A sanity battery only. "Too regular" is automatic for the de Bruijn generator, because exactly 16 full periods are tested. | None. |
| CLM-C16-18 (small groups) | **UPHELD** | Own: S₃ 8, D₄ 6, Q₈ 6, A₄ 16, S₄ 18, with exactly the stated period sets. | None. |
| CLM-C16-19 (sampling beats DFS/SAT) | **UPHELD** (budget-specific observation) | Not re-run. Consistent with my sampler, which needed ≤ 1,416 samples for every n ≤ 26. | None. |
| CLM-C18-01 (e-transformations are bijections) | **UPHELD** | Lean OK (injectivity; finiteness step written). Own d∘e round trip for forward plus reversed passes: 0 failures on 3000 strings × 6 quasigroups. | None. |
| CLM-C18-02 (forward-only propagation; bias ½) | **UPHELD** | Lean `eT_ne_of_ne`. Own: QG-LS p1 and QG-ARP p1 have maximal bias 0.5 with exactly 1,344 deterministic cells, which is 64·(1+…+6), the number Theorem 2 predicts for 16-byte keys. | None. |
| CLM-C18-03 (tail-information bound) | **UPHELD** | Proof and Lean factorisation checked. My own LS, ISO, NIMINV and ARP with my own leaders give exactly 256 values in every 4096-key family (80 families); forward 1-pass also 256. Near-duplicates: 32,624–32,626 full collisions for every reverse-pass variant. The forward 1-pass count is exactly 36,720 = 16·(2550 − 255): there b₉ can never equal the base key's value, so the bound is 255. This explains QG-LS p1 and QG-ARP p1. | None. |
| CLM-C18-04 (T-function obstruction) | **UPHELD** | Proof checked. Own check: 0 violations for AFF p2+rev (all 128 input bits, 2000 keys). | None. |
| CLM-C18-05 (GF(2)-affine) | **UPHELD** | Own: XOR p2+rev gives one input difference ↦ one output difference over 2000 keys. | None. |
| CLM-C18-06 (x + c(y)) | **UPHELD** | Own: 2000/2000 hashes unchanged under anagrams; all 8 output bytes shift by a common additive constant for 100 % of keys; BIC 1.0. | None. |
| CLM-C18-07 (cascade bijective state) | **UPHELD** | The triangular argument is correct. Own cascades: 0 full collisions on near-duplicates. | None. |
| CLM-C18-08 (H-C18-1) | **UPHELD WITH CAVEATS** | Own (new keys, own LS): 0.0089/0.045, against 0.0089/0.045 for BLAKE2b. The test has low power: in 12 BLAKE2b replicates the maximal bias ranged 0.039–0.048, so "within 0.01" spans the whole null range. | None (limitation already recorded). |
| CLM-C18-09 (H-C18-2, INCONCLUSIVE) | **UPHELD WITH CAVEATS** (wording) | As worded ("in the same construction"), the hypothesis is false for the forward-only construction: ARP p1 and LS p1 both have bias exactly ½ by the C18-02 corollary. The experiment compared every structured variant with QG-LS p2+rev instead. For reverse-pass constructions INCONCLUSIVE is right (ARP 0.043 vs LS 0.041; own 0.0415 vs 0.045). | Restrict the statement to reverse-pass constructions (P8). |
| CLM-C18-10 (H-C18-3 refuted) | **UPHELD** | z = 1083.75 and ratio 2.623 are in the data. But the clause "like FNV-1a, \|z\| ≤ 3 … on all four key sets" is false about FNV-1a, which has z = −9.8 (sequential) and −7.1 (near-duplicates); own FNV-1a: −9.77 (P7). | Fix the wording. |
| CLM-C18-11 (H-C18-8 refuted) | **UPHELD** | Own replication (new keys, own leaders): QC-NIMINV maximal bias 0.0735, far above the null maximum 0.048. The worst cell is key byte 15, bit 0 → top bit of s₁. QC-LS and QC-ISO stay at the noise floor. The z = −3.21 part is weak: it is 1 of 48 z-scores, and negative means more uniform than random. | Base the refutation on the avalanche bias. |
| CLM-C18-12 (H-C18-9 refuted) | **UPHELD** | Own: QC-ARP BIC 0.18, maximal bias 0.106 with 4 cells above 0.1. The null BIC maximum is 0.100–0.116. | None. |
| CLM-C18-13 (NO IMPROVEMENT) | **UPHELD WITH CAVEATS** | The negative result is robust, but three statements need care (P7, P9). (i) "No improvement in any measured dimension" and "MX64 dominates on every axis": raw numbers favour some quasigroups within noise (QG-LS p2+rev 0.041 against 0.0445/0.045); say "no significant improvement". (ii) "Better distribution on sequential keys (FNV-1a z = −9.8)" misreads super-uniformity: FNV-1a's bucket-collision ratio there is 0.995. (iii) The MB/s figures are load-dependent: on re-run QG variants ran at 20–98 and cascades at 19–21 MB/s, against the recorded 11–52 and 10–13; BLAKE2b and CRC32 pay one Python call per key. | Reword (i)–(ii); call the MB/s figures indicative ranges. |

---

## (b) Independent checks (commands and results)

All commands run from `reviews/skeptic_checks/C14_C18/` with `nice -n 10`; outputs in `out/`.

**L. Lean** (`cd proofs/lean && PATH=$HOME/.elan/bin:$PATH lake env lean Infinity/<f>.lean`; `out/lean_*.txt`):

| file | exit | time | `#print axioms` |
|---|---|---|---|
| C14_GraphProducts | 0 | 29 s | 8 results (7 theorems, 1 def), each [propext, Classical.choice, Quot.sound] |
| C15_MagmaCA | 0 | 3 s | `ca_step_shift`: none; `ca_comm_binomial`: the three standard axioms |
| C16_Dynamics | 0 | 4 s | 6 theorems, subsets of the three |
| C18_Quasigroups | 0 | 4 s | 5 theorems, subsets of the three |

- `grep -nE "sorry|admit|native_decide|axiom|unsafe|implemented_by|extern|opaque"`: the only hits are the English word "admit" in two C14 doc comments.
- Coverage notes:
  - C14: Lean has the associativity half of Thm 1; the characters only for values in {−1,0,1}; `xor_character` only at entry level.
  - C15: only the commutative binomial formula.
  - C16: lemma-level results; the counts and consequences are written.
  - C18: injectivity only; bijectivity on Qⁿ follows by a written finiteness step.

**C14** (`python3 c14_checks.py <part>`, `c14_census.py`, `c14_twographs.py`):

| check | result |
|---|---|
| `classify` | 20 associative codes (exact list) = P₃³ graph level for all 256; 60 random triples; 32 symmetric; unit K₁ (isomorphism, all graphs ≤ 4 vertices) exactly for 5, 13, 29, 77, 85, 93, 141, 221; 76 orbits, associative orbits exactly as listed; 10 depending on both factors (8 commutative) |
| `witness` | minimal associativity witnesses {2: 144, 4: 84, 8: 8}, all degree-certified; commutativity witnesses 224/224 ({2: 192, 4: 32}), all degree-certified |
| `characters` | sympy over ℂ on the full P₃×P₃ identity: multiplicative codes [8, 13, 85, 93, 127, 141] with c = (0,1,0), (1,1,0), (1,−1,1), (1,0,1), (0,0,1), (1,1,−1); additive [5, 221]; numeric failures 0; without character: 0, 255 |
| `seidel` | Seidel identity exact on 624 pairs; bipartite rule 1225/1225; explicit Π 300/300; Thm 7(c) for all graphs ≤ 6 vertices, 0 violations; K₂³ ≅ K₂⊕K₁,₃ = K₄,₄; 3K₁⊕K₂,₃ = K₁,₂⊕K₁,₄ = K₆,₉ |
| `c14_census.py` (37 s) | own graphs 1, 2, 4, 11, 34, 156, 1044 (exact canonical forms); all 8 products, all and connected graphs, orders 4–15. Composite classes, factorisation counts, multiset collisions and prime counts n = 2…15 identical to EXP-C14-04. Connected □/⊠ primes = A129582 for n = 2…15 |
| `c14_twographs.py 64` (38 s) | switching classes n ≤ 8: 1, 1, 2, 3, 7, 16, 54, 243 (= A002854); primes 1, 2, 2, 7, 14, 54, 240. 53,703 multisets with order ≤ 64; cospectral groups only at orders 16, 24, …, 64 (2,205 groups, largest 6); 3,012 exact tests; **0 collisions** |
| `sanity_switching.py` | the exact switching test returns True on 60/60 equivalent pairs (random graphs to 64 vertices and two-graph products) and False on 30/30 perturbed pairs |
| `misc_checks.py` | the CLM-C14-11 isomorphisms; the 63-vertex □/⊠ collision |
| `c14_spectra_timing.py` | factor route against `eigvalsh` at nm = 1600: 54,082× under thread contention (eigvalsh 9.9 s), 1,230× with default threads otherwise, 2,046× single-threaded (P5) |

**C15** (`python3 c15_checks.py <part>`, `c15_crossover.py`):

| part | result |
|---|---|
| `fuse 14` | λ(t) = 3, 3, 4, …, 16 for t = 0…14 (forward = backward); both bounds hold; burn-time formula vs simulation 0/870,969 mismatches (plus random rows); lower-bound family distinct for t ≤ 12 |
| `census3` (22 s) | 1734 classes (19,683 tables); 808/104/300/522; max λ(9) = 649; 43 surjective (420 tables) = 420 permutive; 7 injective; 34 nilpotent; 18 semigroups, all λ ≤ 3; reversible table λ ≡ 3 with 1, 2, …, 10 essential cells; per-class λ identical to the lab's; periodic cross-check: 0 conflicts |
| `cycledet` (same seeds) | L = 16: 1693; L = 32: 1590 (median μ 5, λ 2; non-repeating 128 geometric, 12 other, 4 bounded); L = 64: 1561. Affine quasigroups: (μ, λ) = (1, 6560), (0, 6560), (1, 6560), (1, 19680) at L = 32; none within 200,000 at L = 64 |
| `semigroups` | popcount word 0/300 mismatches (S₃); S₃ widths (forward = backward) 6, 6, 6, 36, 72, 216, 1296 for t = 0…6; ℤ₆ constant 6 |
| `fastforward` | Theorem 2 (own exact powers) 0 mismatches; Theorem 3, 63 commutative semigroup tables, 756 cases, 0 mismatches |
| `misc` | rules 17m; surjective {51, 85, 102, 153, 170, 204}; XOR essential = 2^popcount(t) (t < 15); Laver A₂/A₃ (LD) essential ≤ 3 / ≤ 4, widths 4 / 8 forward; band surjective, injective, not permutive; anchored models permutive |
| `c15_crossover.py` | the lab's fast-forwards against direct simulation, both median of 7 (Appendix C): they lose for small t |

**C16** (`python3 c16_checks.py <part>`, `c16_existence.py`, C programs `c16_affine_laver.c` and `nim_mex.c`):

| part | result |
|---|---|
| `small` | n = 2, 3 all tables, n = 4 all 331,776 row-permutation tables: full-period 1, 24, 20,736; 0 quasigroups; quasigroup maxima 3, 8, 15; parity 0 violations |
| `latin` (24 s) | own Latin squares 2, 12, 576, 161,280; full-period 0, 0, 0, **3360**; 28 classes, all of size 120, automorphism groups trivial; parity 0 violations; 480 are isotopes of ℤ₅ (all isotopes of ℤ₅: 17,280, as (5!)³/100 predicts) |
| `certs` | 11 stored certificates (6–16): Latin, a single n²-cycle, parity OK; the "isotope of ℤₙ" ones are group isotopes; 8 products full-period; 6×6 control not |
| `isotopes` | 36 groups of even order 2–30: ∏ sgn λ_g = (−1)^m; isotopes (300 each for n ≤ 16, 60 above) always (−1)^m, 0 full-period. ℤₙ isotopes for n = 7, 9, …, 21: 47, 30, 26, 19, 15, 7, 19, 4 full-period out of 3000 |
| `c16_existence.py` | full-period quasigroups for every n = 17…26 (10–1,416 samples each), all verified |
| `groups`, `nimbers` | S₃ 8, D₄ 6, Q₈ 6, A₄ 16, S₄ 18 (period sets as stated); nimbers q = 4, 16, 256: 8, 40, 360 = Pisano |
| `./c16_affine_laver affine 60` (81 s) | 1,997,716 magmas (2 ≤ N ≤ 60): max cycle = lcm in all cases; lcm = 3×3 order (N ≤ 24); with a fixed point, max = companion order in all 1,575,671 cases. The only mismatches are N = 1 artefacts of my order routine (`out/c16_affine_N12_details.txt`) |
| `./c16_affine_laver laver 13` | n ≤ 13: 1 fixed point, N−1 two-cycles, every orbit reaches the top element; transients 1, 3, 3, 5, …, 5 |

**C18** (`python3 c18_checks.py <part>`, `c18_de.py`, `audit_nim.py`):

| part | result |
|---|---|
| `structure` | own nim field (mex) checks; T-function 0 violations; XOR 1 output difference; ARP anagram-blind 2000/2000; common additive shift 100 % |
| `tailbound` | reverse-pass p2: exactly 256 per family (4 quasigroups × 20 families); forward p1: 256; forward p2: 3,947–3,988 of 4096. Near-duplicate full collisions: reverse-pass 32,624–32,626, forward p1 36,720, forward p2 678–747, cascades 0 |
| `avalanche` (seed 424242) | mean/max bias, BIC: QG-LS p2+rev 0.0089/0.045, 0.109; QG-NIMINV p2+rev 0.009/0.0395; QC-LS 0.0088/0.042; QC-ISO 0.0089/0.0455; **QC-NIMINV 0.0091/0.0735**, 0.16; **QC-ARP 0.011/0.1055**, 0.18; MX64 0.009/0.044; BLAKE2b 0.0089/0.045; FNV-1a 0.098/0.5 |
| `noise` | 12 BLAKE2b replicates: maximal bias 0.039–0.048 (mean 0.044), BIC maximum 0.100–0.116 |
| `distribution` | FNV-1a on decimal keys: z = −9.77 (mask), −7.99 (mod 1021), bucket-collision ratio 0.995; MX64 −0.50 / 0.57 / 1.004 |
| `c18_de.py`, `audit_nim.py` | d∘e = id on 18,000 strings; the lab's nim table equals my mex table, and its NIMINV quasigroup equals mine |

**R. Lab re-runs** (`python -m lab run <id>` from the repository root; `out/lab_reruns.log`; comparison in `timing_compare.py` → `out/timing_compare.json`):

| experiment | stored code sha256 = current script? | outcome |
|---|---|---|
| EXP-C14-01 | yes | reproduced previous hash |
| EXP-C15-03 | yes | reproduced; speedups differ (Appendix D) |
| EXP-C15-05 | yes | reproduced |
| EXP-C16-01 | yes | **RESULT HASH CHANGED**: the only differing key is `census/4/seconds` (3.26 → 2.66) (P1) |
| EXP-C16-02 | yes | reproduced |
| EXP-C18-04 | yes | reproduced; MB/s differ up to 2.5× |
| EXP-C18-05 | yes | reproduced; MB/s about 2–3× higher |

All 22 result files of the four cycles carry a code sha256 equal to the current script (`code_hashes.py`). Only EXP-C16-01 has wall-clock keys outside `timings`.

---

## (c) Bugs and problems in code, records and documents

None of these changes a mathematical conclusion.

- **P1 (reproducibility bug, EXP-C16-01).**
  - `experiments/C16/E01_small_magmas.py` line 72 stores `"seconds": round(time.perf_counter() - t0, 2)` inside `census/<n>`, which is hashed.
  - My re-run changed only `census/4/seconds` and was reported as RESULT HASH CHANGED, so `lab verify` will flag it every time.
  - Fix: move the value under `timings`.
- **P2 (overstatement, C15 README Step 6).**
  - "Semigroups (width ≤ \|S\|) and affine magmas (width ≤ \|A\|) are bounded, as proved" holds only for *commutative* semigroups (Theorem 1(c), and the claim says so).
  - For the group S₃, λ(t) = 6, 6, 6, 36, 72, 216, 1296 (t = 0…6).
  - The textbook's Theorem 17.2 is correctly restricted. The README and the H-C15-2 discussion should say "commutative" or "order 3".
- **P3 (false statement: "affine and fuse never lose").**
  - Appears in the C15 README Step 1 table ("affine/fuse never lose"), textbook ch. 17 ("while the affine and fuse methods never lose"), and the CLM-C15-12 counterexample text.
  - With the same protocol on both sides, both methods lose for small t: below t ≈ 20 (affine) and t ≈ 20–70 (fuse); Appendix C.
  - Hence H-C15-6's "loses for small t" clause is partly true. The refutation still stands on the ">100×" clause.
- **P4 (benchmark protocol and precision, EXP-C15-03).**
  - The fast-forward is timed as the best of 3, direct simulation as 1 run.
  - Recorded ranges are single-run figures on a loaded machine and do not reproduce to the stated precision: fuse ×4021 → ×1363 at L = 1024, t = 10⁵; affine at 10⁴: 138–214 → 202–314.
  - Ratios between methods measured in the same run are more stable; claims should give orders of magnitude.
- **P5 ("4–5 orders of magnitude", C14 README Step 9 and textbook ch. 15).**
  - The EXP-C14-07 baseline (14–19 s for a 1600×1600 `eigvalsh`) reflects OpenBLAS thread oversubscription: I measured 9.9 s once under contention, then 0.22 s (default threads) and 0.38 s (1 thread).
  - The typical gap is about 3 orders. The README's explanation that the 4–5 orders "reflect" the complexity gap is not right.
- **P6 (novelty, CLM-C14-06; affects the "not found" statements under CLM-C14-04/13).**
  - Abiad, Butler and Haemers, arXiv:1801.01149 (2018), §5 "A graph product and its 2-rank behaviour", define this product (their F₂ formula A₁⊗J + J⊗A₂ is the XOR product) and state its Seidel matrix as (S₁+I)⊗(S₂+I) − I. They also use its compatibility with Seidel switching.
  - That Kronecker products of graphical (symmetric, constant-diagonal) Hadamard matrices are again graphical Hadamard matrices is classical. Their §4 states it alongside the "well known" Hadamard case: "It is well known that if H₁ and H₂ are Hadamard matrices, then so is the Kronecker product H₁ ⊗ H₂. Moreover, … if H₁ and H₂ are graphical, then so is H₁ ⊗ H₂".
  - The lab's four searches missed this.
- **P7 (C18 interpretation).**
  - CLM-C18-10's "like FNV-1a, \|z\| ≤ 3 on all four key sets" is false about FNV-1a.
  - CLM-C18-13 and textbook Result 20.7 read FNV-1a's z = −9.8 as worse distribution, although it means *more* uniform than random (bucket-collision ratio 0.995); a two-sided \|z\| > 3 flag is not a hash-table defect.
  - "No improvement in any measured dimension" and the journal's "MX64 dominates on every measured axis" should be "no significant improvement": several quasigroup hashes have numerically smaller maximal bias or BIC than both baselines, within noise.
  - CLM-C18-11's z = −3.21 is 1 of 48 z-scores and in the benign direction.
- **P8 (CLM-C18-09 wording).**
  - The hypothesis says "in the same construction", but EXP-C18-02 compares every structured variant with QG-LS p2+rev.
  - In the forward-only construction, ARP p1 and LS p1 tie at exactly ½. As written, the hypothesis is therefore refuted, not inconclusive.
- **P9 (C18 throughput noise).**
  - EXP-C18-04 is internally inconsistent in one run: QG-LS p1+rev/8 at 57 MB/s exceeds QG-LS p1/8 at 22 MB/s although it does strictly more work.
  - Timings at L = 8 (2–7 ms) are dominated by noise. "11–52 MB/s" became 20–98 MB/s on my re-run; the cascades went from 10–13 to 19–21.
  - The ordering against FNV-1a and MX64 is stable: in both runs and both key lengths, the fastest quasigroup variant is still ≥ 4× slower than MX64 and ≥ 5× slower than FNV-1a; the reverse-pass variants are ≥ 7× slower than MX64.
- **P10 (CLM-C16-10 and textbook Conj. 18.8).**
  - "Rates close to 1/n²": the exact n = 5 rate is 0.52/n²; at n = 6 the sampled rate is 0.50/n²; pooled over 6–16 the lab has 139 hits against 181 expected.
  - The rate is the right order, not close.
- **P11 (evidence gap, CLM-C16-09).**
  - The "n = 5, …, 15" parenthetical was sampled only for n = 7–15; EXP-C16-02 never tests isotopy at n = 5.
  - It is true: 480 of the 3360 full-period quasigroups are isotopes of ℤ₅.
- **P12 (thin evidence, CLM-C14-13).** Up to order 16, almost all composite two-graphs are [K₂]⊕X, whose distinctness is the proved cancellation (C14-07c). My order-64 extension is substantially stronger.
- **P13 (EXP-C14-02).** `n_non_associative: 236` and `n_non_commutative: 224` are hard-coded, not computed. They are correct.
- **P14 (minor wording, C14).**
  - The README says "26 relation triples"; the claim says 27 (E,E,E is trivial).
  - Journal C14-05 says the commutative associative products are "exactly" those with a character; empty and complete have none.
- **P15 (CLM-C15-11).** "Do not repeat within 5000 steps" depends on the cap: at L = 32 the four affine quasigroups have periods 6,560 or 19,680, just above it.
- **P16 (CLM-C15-17).** "Widths 4 and 8" are the streaming (forward) widths; the backward widths are 5 and 13–14.
- **P17 (CLM-C16-17).** The de Bruijn generator's "too regular" verdict is automatic: 2²⁰ outputs are exactly 16 full periods.

Audited and found correct:
- `graph_products.product`/`phi`/`assoc_defects`; `IsoRegistry`, which is exact.
- `SwitchingRegistry.equivalent`: the descendant criterion is exact. Its bucketing by Seidel spectra rounded to 6 decimals is a theoretical miss risk, but my exact census agrees.
- `magma_ca.light_cones`, `obdd_widths`, the pair-graph surjectivity and injectivity tests.
- `fuse_burn_times` and `fuse_fast_forward`; `affine_fast_forward` (the FFT is exact for the sizes used); `commutative_semigroup_fast_forward`.
- `magma_dynamics._uc_dfs`, including its wrap-around conditions; `batch_analyze`.
- `quasigroup_hash.nim_mul`, which equals the mex definition; the `avalanche`, `chi2_z` and `collisions` formulas.

Faults in my own harness, fixed before the reported runs:
- My first Laver-table construction did not set the top row to the identity and produced non-LD tables (in `c15_checks.py` and `c16_affine_laver.c`). My left-distributivity check caught it.
- The first two-graph screen keyed on float spectra; it was replaced by exact integer power sums.
- My matrix-order routines give 2 instead of 1 at N = 1. These are the only mismatches in the affine run and were excluded.
- An output-printing bug and a `time | cut` pipeline hid two outputs; I re-ran those parts.

---

## Appendix A: checks of the written proofs

**A.1 C14.**
- *Thm 1:* (2⇒3) is valid because φ_S(x, y) = E only for x = y = E, so both sides of (3) lie in {A, N} except at (E,E,E).
- *Thm 4:*
  - Disjoint, all-nonzero blocks on P₃×P₃ give c_E² = c_E and c_r c_s ∈ {c_A, c_N}.
  - Case c_E = 0 yields S = {AA} or all cells but NN. Case c_E = 1 forces EA, AE ∈ S and EN, NE ∉ S.
  - I solved all eight (y², yz, z²) patterns: (y,y,z) gives co-normal, (y,z,y) gives 141, (y,z,z) gives strong, (z,y,z) gives XOR, and the other four force y = z.
  - c_A ≠ c_N makes M_c injective, so associativity and commutativity follow.
- *Thm 5:* the additive identity forces c_E = 0, c_s on (E,s) and 0 on E-free cells, which gives Cartesian or 221. For empty and complete the cells EA and EN have equal status, which forces c_A = c_N. **Correct.**
- *Thm 6:* the identity holds entrywise as (−1)^{a⊕b} = (−1)^a(−1)^b. Switching acts as D(S+I)D, and D_Z⊗D_W is diagonal ±1. **Correct.**
- *Thm 7:*
  - (a) S+I = wwᵀ.
  - (b) I re-derived that entry (Π(g,x), Π(g′,y)) of the first product equals w_g w_{g′} d_x d_y m_{xy}, the corresponding entry of the second.
  - (c) The twin relation (rows equal up to sign) is switching invariant. Each class can be switched so that rows inside a class are equal, which gives the blow-up of a twin-free reduct. J₂⊗M doubles the multiplicities, and halving is injective. **Correct.**
- *Thm 8:* each case follows from (order, imbalance) multiplicativity. Note that K₂⊕K₂⊕K₂ = K₂⊕K₁,₃ = K₄,₄ directly.
- *Thm 9:* connected graphs closed under □ and ⊠, distributivity and UPF give ℕ[X]. The Dirichlet-series identity forces p_n = q_n, and complementation is an isomorphism ⊠→∨ and □→221. **Correct**, given the cited UPF theorems.

**A.2 C15.**
- *Thm 1:* (a) is a correct induction (j = 2^{t−1}+j′ ↦ x_{1+s(j′)}); (b) regroups by C(t,k). (c) The residual after a prefix is y ↦ p·∏ y_j^{C(t,j)}, which gives ≤ \|S\| residuals; this needs commutativity, see P2.
- *Thm 2:* the Pascal step needs φψ = ψφ; the constant term satisfies g_{t+1} = (φ+ψ)g_t + c; and P𝟙 = (φ+ψ)𝟙.
- *Thm 3:* N_j ≥ C(t, j or L) ≥ t ≥ ι. The bound needs only t ≥ max(L+1, ι).
- *Thm 4:*
  - (a) I re-derived all four burn-time cases, including the case x_i = 1, x_{i+1} = 2: c_i(t) = 1 iff t ≤ τ_{i+2}+1, so τ_i = τ_{i+1}.
  - Lower bound: τ₁ = 2j + 2(m−1−b), and F_t = 2 iff j ≥ b + 1 + (t−2m). The threshold is ≤ t−m for every admissible b, so it separates both the prefixes and the suffixes.
  - Upper bound: the statement "τ_k computed inside the suffix, ∞ if no seed" needs one justification. F_t does not depend on cells beyond t, so evaluate with the all-2 continuation; then a seedless suffix really has τ = ∞. With that, a level has ≤ 1 + (t+1) + t = 2t + 2 ≤ 3t + 3 residuals (x_k = 0 forces τ_k = 0; x_k = 1 gives τ_k ∈ {1,…,t, >t}; x_k = 2 gives τ_k ∈ {2,…,t, >t}). **Correct.**

**A.3 C16.**
- *Thm 1:* correct.
- *Thm 2:* the bijection with de Bruijn cycles up to rotation is correct; B(k,2) = (k!)^k/k².
- *Thm 3:* P = S∘R with sgn R = ∏ sgn L_b and sgn S = (−1)^{n(n−1)/2}; and n²−1−n(n−1)/2 = (n−1)(n+2)/2.
- *Thm 4:* the column a ↦ (·)⋆a is injective iff the n distance-2 pairs starting at a are distinct.
- *Thm 6:* CRT on cycle lengths n₁², n₂².
- *Thm 7:*
  - L_b = γλ_{α(b)}β, so ∏ sgn L_b = ∏ sgn λ_g for even n, and sgn λ_g = (−1)^{n/o(g)}.
  - Cyclic Sylow 2-subgroup: Burnside gives a normal 2-complement N, and 2^k \| o(g) ⇔ g maps to a generator of G/N ≅ C_{2^k} (the 2-part of o(g) equals o(gN)). That is φ(2^k)\|N\| = m elements.
  - Non-cyclic Sylow 2-subgroup: no element has 2^k \| o(g), and 4 \| n, so m is even.
  - Needed: (−1)^{(2m−1)(m+1)} = (−1)^{m+1}. **Correct.**
- *Thm 9:* conjugation by (x*, x*); e₂ and Ce₂ form a basis (det −1); C^k e₂ = e₂ implies C^k = I. **Correct.**
- *Thm 10:* any finite field works the same way through discrete logarithms.
- *Thm 11:* (N−1)⋆y = y, x⋆(N−1) = N−1 and x⋆y > x below N−1 force a strict climb. **Correct.**

**A.4 C18.**
- *Thm 2:* left cancellation at i, then right cancellation afterwards.
- *Thm 3:* the induction over passes using (i) with k = 7 is right. For (iii), the first 7 entries of each forward pass depend only on the first 7 inputs.
- *Thm 4:* congruence mod 2^r propagates through T-functions; reversal permutes positions only.
- *Thm 5:* compositions of affine maps are affine.
- *Thm 6:* the additive difference stays constant; one pass gives prefix sums.
- *Thm 7:* the update is a triangular composition of bijections.

All **correct**. Theorem 3's bound uses only the e-transformation structure, not the quasigroup property.

## Appendix B: streaming width of S₃ (P2)

| t | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| S₃: forward = backward width | 6 | 6 | 6 | 36 | 72 | 216 | 1296 |
| ℤ₆ (commutative) | 6 | 6 | 6 | 6 | 6 | 6 | 6 |

Reason at t = 3, level 2: the residual (y₂,y₃) ↦ a y₂ b y₂ y₂ y₃ determines (a, b) because Z(S₃) = 1. That gives 36 distinct residuals.

## Appendix C: small-t crossover of the lab's fast-forwards (median of 7 on both sides; speedup = direct / fast-forward)

| L | method | t = 1 | 5 | 10 | 20 | 50 | 100 |
|---|---|---|---|---|---|---|---|
| 256 | affine | 0.21 | 0.39 | 0.70 | 1.18 | 2.38 | 3.96 |
| 256 | fuse | 0.06 | 0.27 | 0.54 | 1.10 | 2.49 | 4.97 |
| 1024 | affine | 0.19 | 0.54 | 0.62 | 0.92 | 2.40 | 4.07 |
| 1024 | fuse | 0.02 | 0.14 | 0.22 | 0.51 | 1.17 | 2.44 |
| 4096 | affine | 0.11 | 0.25 | 0.43 | 0.85 | 1.56 | 2.78 |
| 4096 | fuse | 0.02 | 0.07 | 0.11 | 0.26 | 0.70 | 1.32 |

## Appendix D: timing reproducibility (stored run → my re-run, same scripts)

| quantity | recorded | re-run |
|---|---|---|
| affine, L = 1024, t = 10⁴ / 10⁵ | ×138–214 / ×1793–2462 | ×202–314 / ×1459–2262 |
| fuse, L = 1024, t = 10⁵ | ×4021 | ×1363 |
| commutative semigroups, L = 1024, t = 10⁵ | ×62–100 | ×79–97 |
| QG tail hashes, 64-byte keys (MB/s, EXP-C18-04) | 11–52 | 20–98 |
| cascades / BLAKE2b / MX64 (MB/s, EXP-C18-05) | 9.5–13 / 41 / 165 | 19–21 / 81 / 514 |

The direction of every comparison is stable. The magnitudes are not.
