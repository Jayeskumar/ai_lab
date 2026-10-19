# Cycle C14 — Graphs as quantities: the 256 local graph products

**Branch:** D (relationships instead of magnitude) · **Status:** complete
**Experiments:** EXP-C14-01 … EXP-C14-07 · **Claims:** CLM-C14-01 … CLM-C14-13
**Proofs:** `proofs/lean/Infinity/C14_GraphProducts.lean` (8 results, standard axioms only),
`proofs/paper/C14.md` (Theorems 1–11) · **Module:** `systems/graph_products.py`

## Step 1 — Hypotheses

Question: *if graphs are the "numbers", which ways of multiplying them behave like
multiplication, and what plays the role of factorisation, units and invariants?*
A local product decides adjacency in V(G)×V(H) from the pair of relations
(equal / adjacent / non-adjacent) in the factors: 2⁸ = 256 products.

| ID | Hypothesis | Proposer | Outcome |
|---|---|---|---|
| H-C14-R | Strict associativity reduces to a finite identity on the 27 relation triples (26 non-trivial), and P₃³ detects every failure. | Formal Verifier | **proved** (Lean, both directions) |
| H-C14-2 | Exactly 20 products are associative, 10 commutative (Historian's recollection of Imrich–Izbicki 1975). | Historian | **confirmed** (Lean `decide`); rediscovery |
| H-C14-1 | *(bold)* Associativity/commutativity *up to isomorphism* is no weaker than the strict notions. | Inventor | **proved** (computer-assisted: 236 + 224 witnesses with ≤ 3-vertex factors, certified by degree sequences) |
| H-C14-5 | Exactly six products are linearised by a Kronecker "character" M(G∗H) = M(G)⊗M(H). | Formal Verifier | **proved** (hand case analysis + sympy + Lean at {−1,0,1}) |
| H-C14-6 | *(bold)* Every commutative associative product except empty/complete has a (multiplicative or additive) character. | Inventor | **proved** |
| H-C14-3 | *(bold)* The six commutative unital associative products have unique prime factorisation on connected graphs (co-connected for the complement-duals). | Inventor | **refuted** by the symmetric difference: K₂⊕K₂⊕K₂ ≅ K₂⊕K_{1,3} (order 8) |
| H-C14-7 | Cartesian-prime and strong-prime connected graphs are equinumerous in every order. | Explorer | **proved** (from published UPF theorems); A129582 reproduced to n = 15 |
| H-C14-4 | *(bold)* Two-graphs (switching classes) factor uniquely under the symmetric difference. | Inventor | **no counterexample to order 16** (conjecture) |
| H-C14-8 | K₂⊕X ≅ K₂⊕Y iff X, Y are switching-equivalent. | Explorer | **proved** |

## Step 2 — Definitions

rel_G(x, y) ∈ {E, A, N}; a product is a set S of cells (r, s) ≠ (E, E);
φ_S(r, s) is the relation in the product; characters M_c(G) = c_E I + c_A A +
c_N (J − I − A); Seidel matrix S(G) = J − I − 2A; switching, two-graphs,
twins and reducts: `proofs/paper/C14.md`. Codes: bit i ↔ cell i in the order
EA, EN, AE, AA, AN, NE, NA, NN (Cartesian 5, direct 8, strong 13,
lexicographic 29, symmetric difference 85, co-normal 93).

## Step 3 — Falsification design

* Classification: relation-level verdicts compared with brute-force graph
  computations (P₃³ and random triples) and with an independent
  implementation (Skeptic).
* H-C14-1: a non-strict product for which no small witness exists would refute it.
* H-C14-3/4: exhaustive factorisation censuses — every prime factorisation of
  every order ≤ 15 (graphs) and ≤ 16 (two-graphs); a single collision refutes.
* Validation of the censuses against independent published data: A129582
  (Cartesian primes, Ji Li 2007) and A002854 (two-graphs).

## Steps 4–5 — Implementation and execution

| Experiment | Outcome |
|---|---|
| EXP-C14-01 | 20 associative products (10 commutative; 32 symmetric products overall); two-sided unit K₁ for exactly 8 (Cartesian, strong, lexicographic and its transpose, symmetric difference, co-normal, 141, 221); associative and distributive over disjoint union on both sides: 0, 1, 4, Cartesian, direct, strong; 76 orbits under ⟨transpose, complement-conjugation⟩, associative ones forming 8 orbits; 0 disagreements between relation-level and graph-level checks |
| EXP-C14-02 | every one of the 236 non-associative products has a witness (G∗H)∗K ≇ G∗(H∗K) with factors of ≤ 3 vertices (product orders 2: 144, 4: 84, 8: 8), every one of the 224 non-commutative products a witness G∗H ≇ H∗G; all certified by edge count/degree sequence |
| EXP-C14-03 | multiplicative characters: direct (0,1,0), strong (1,1,0), symmetric difference (1,−1,1), co-normal (1,0,1), 127 (0,0,1), 141 (1,1,−1); additive: Cartesian (0,t,0), 221 (0,0,t); sympy over ℂ = hand analysis; 0 numerical failures; Seidel spectrum of XOR products multiplicative on 30/30 random pairs |
| EXP-C14-04 | factorisation census, all graphs, orders ≤ 15: Cartesian, strong, co-normal, 221 — no collision; lexicographic (and transpose) — collisions at orders 10, 14 (multisets) — e.g. 2K₁∘(C₄+K₁) ≅ (2K₂+K₁)∘2K₁; symmetric difference and 141 — collisions at every even order ≥ 4 and at 15; connected: XOR collisions at 8, 10, 12, 14 (2, 6, 15, 53 classes); connected Cartesian/strong primes 1, 2, 5, 21, 110, 853, 11111, … = A129582 to n = 15; prime counts (all graphs) for every product; the 63-vertex Cartesian/strong counterexample verified |
| EXP-C14-05 | switching classes n ≤ 8 reproduce A002854 (1,1,2,3,7,16,54,243); no non-unique factorisation of two-graphs under ⊕ up to order 16 (246 composite classes at order 16, each with one factorisation); prime two-graphs 1, 2, 2, 7, 14, 54, 240, 2035, 33113, …; K₂-cancellation 0 violations in 12,713 pairs |
| EXP-C14-06 | Skeptic re-implementation (no shared code): 20/10 recounted, all 460 witnesses re-certified, K₂⊕K₂⊕K₂ ≅ K₂⊕K_{1,3} by explicit permutation, K_{a,b}⊕K_{c,d} = K_{ac+bd,ad+bc} edge by edge (a,b,c,d ≤ 4), Seidel identity exact in integers, K₂-absorption 200/200 |
| EXP-C14-07 | spectra of products from the factors vs direct diagonalisation (`numpy.linalg.eigvalsh`): max relative error 1.2e−14 over 16 cases; at nm = 1600 the factor route took ≈ 0.2–0.4 ms against 14–19 s for the baseline on the (heavily loaded, shared) machine — the baseline was inflated by BLAS thread oversubscription; the Skeptic measured 0.22–0.38 s for the same `eigvalsh` on an unloaded run, so the typical gain is about 3 orders of magnitude, not 4–5 |

## Step 6 — Analysis

* **Associativity is a finite fact.** Because adjacency in a product depends
  only on relations, associativity of a product of *all* graphs is a 27-entry
  identity, and the 3-vertex path already sees every failure. Twenty products
  pass, exactly as Imrich and Izbicki found in 1975. Up to isomorphism nothing
  more is gained: every failure is visible in the degree sequences of products
  of graphs with at most three vertices.
* **Linear characters explain the commutative ones.** Ten associative products
  are commutative; two are trivial (empty, complete), two are *additive*
  (Cartesian, A ↦ A ⊗ I + I ⊗ A, and its complement-dual) and six are
  *multiplicative*: one fixed linear combination of I, A and J − I − A turns
  the product into the Kronecker product. For the symmetric difference that
  combination is S(G) + I (Seidel matrix plus identity).
* **Graphs become quantities through characters**: the spectrum of M_c(G) is a
  multiplicative (resp. additive) invariant; complete bipartite graphs under ⊕
  are exactly the "split-complex" quantities (order, imbalance) with
  componentwise multiplication.
* **Unique factorisation is the exception for ⊕.** Since S(G ⊕ H) + I is a
  Kronecker product, ⊕ only sees switching classes in the presence of K₂, so
  switching-equivalent factors collide (C₄ = K₂⊕K₂ = K₂⊕2K₁;
  K₂⊕K₂⊕K₂ ≅ K₂⊕K_{1,3}). The bold hypothesis H-C14-3 fails for ⊕ — but on
  the level the product actually sees, the two-graphs, no collision occurs up
  to order 16, and for graphs with connected complement no collision occurs up
  to order 15.
* **Cartesian and strong are the same monoid in disguise** (graded isomorphism
  via the polynomial semirings ℕ[connected primes]); their prime counts agree
  in every order, and the census reproduces Ji Li's A129582 to n = 15.

## Step 7 — Proofs and counterexamples

Lean (`C14_GraphProducts.lean`, standard axioms): `rel_lprod`, `assoc_iso`,
`assoc_iso_nonempty`, `assoc_of_P3` (Theorem 1, both directions),
`assoc_codes`, `comm_assoc_codes` (Theorem 2 by kernel computation),
`character_codes` (Theorem 4 at {−1,0,1}), `xor_character` (Theorem 6, entry
level). Written: Theorems 1–11 in `proofs/paper/C14.md`. Counterexamples:
K₂⊕K₂⊕K₂ ≅ K₂⊕K_{1,3} and C₄ = K₂⊕K₂ = K₂⊕2K₁ (H-C14-3);
3K₁⊕K_{2,3} ≅ K_{1,2}⊕K_{1,4} (order 15); 2K₁∘(C₄+K₁) ≅ (2K₂+K₁)∘2K₁
(lexicographic).

## Step 8 — Comparison with existing mathematics (Historian)

* **Associative products.** W. Imrich, H. Izbicki, *Associative products of
  graphs*, Monatsh. Math. 80 (1975) 277–281, doi:10.1007/BF01472575
  (https://pure.unileoben.ac.at/en/publications/associative-products-of-graphs/):
  exactly twenty products of this type are associative. R. J. Nowakowski,
  D. F. Rall, *Associative graph products and their independence, domination
  and coloring numbers*, Discuss. Math. Graph Theory 16 (1996) 53–79,
  doi:10.7151/dmgt.1023 (https://www.dmgt.uz.zgora.pl/publish/article.php?doi=1023):
  ten depend on both factors, eight of these commutative. Our Theorem 2 agrees
  exactly. **REDISCOVERY.** We did not obtain the full text of either paper;
  whether they treat isomorphism-level associativity (Theorem 3) is unknown.
* **Boolean products.** The symmetric difference, conjunction (direct) and
  disjunction (co-normal) products appear in F. Harary, G. W. Wilcox, *Boolean
  operations on graphs*, Math. Scand. 20 (1967) 41–51
  (https://www.mscand.dk/article/view/10817).
* **Unique factorisation.** Cartesian: Sabidussi (1960), Vizing (1963); strong:
  Dörfler–Imrich (1970), McKenzie (1971); lexicographic factorisations are not
  unique, but the number of prime factors is (Imrich; see the survey remarks in
  arXiv:2407.02615, https://arxiv.org/abs/2407.02615). Disconnected graphs and
  the semiring view: Hammack–Imrich–Klavžar, *Handbook of Product Graphs*
  (2nd ed., CRC 2011); S. Klavžar et al., *Cancellation properties of products
  of graphs* (https://users.fmf.uni-lj.si/klavzar/preprints/CC.pdf), which
  notes that the strong product has the same cancellation theory as the
  Cartesian product. Theorem 9 is a reformulation of this (REDISCOVERY in
  substance). The connected prime counts are OEIS A129582 (Ji Li, *Prime graphs
  and exponential composition of species*, J. Combin. Theory A 115 (2008)
  1374–1401, arXiv:0705.0038). **REDISCOVERY.**
* **Seidel matrices.** Two-graphs and switching: van Lint–Seidel (1966),
  Seidel; background https://en.wikipedia.org/wiki/Two-graph and
  https://www.win.tue.nl/~aeb/graphs/twographs.html. A paper on Seidel
  equienergetic graphs uses the special case S(D_m(G)) + I = J_m ⊗ (S(G) + I)
  (one factor edgeless), seen through a secondary summary
  (https://www.themoonlight.io/review/some-new-results-on-seidel-equienergetic-graphs).
  Four targeted searches ("symmetric difference" + Seidel spectrum; Kronecker
  product of Seidel matrices / two-graphs; tensor product two-graphs) found no
  statement of the general identity S(G⊕H) + I = (S(G)+I)⊗(S(H)+I), of the
  switching compatibility of ⊕, of Theorem 7 or of the character
  classification. **Correction (Skeptic review, 2026-10-18):** the identity and
  the switching compatibility are in A. Abiad, S. Butler, W. H. Haemers,
  arXiv:1801.01149 (2018), §5 — CLM-C14-06 is a **REDISCOVERY**. Theorem 7 and
  the character classification remain **POTENTIALLY NOVEL (small; plausibly
  folklore).**
* **OEIS.** Prime counts with respect to each product over *all* graphs, and
  the prime two-graph counts: no match (searched 2026-10-18; cached).

## Step 9 — Applications

* *Spectra of large products from small factors* (EXP-C14-07): for ⊕, ⊠, ∨ and
  □ the spectrum of the relevant matrix of an nm-vertex product follows from
  the factors' spectra — exact to 1.2e−14 (relative) and orders of magnitude
  faster than diagonalising the product (baseline: `numpy.linalg.eigvalsh` on
  the product). This is the
  standard Kronecker eigenvalue trick; the only new ingredient is that it
  applies to the symmetric difference through Seidel matrices.
* *Constructions of two-graphs / equiangular lines*: the XOR product multiplies
  Seidel spectra (shifted by 1). One natural case, worked out from Theorem 6:
  the regular two-graph on 6 points has Seidel eigenvalues ±√5 (3 each), so its
  XOR square has Seidel eigenvalues 5 ± 2√5 (9 each) and −5 (18), i.e. 36
  equiangular lines in ℝ¹⁸ at angle arccos(1/5). This is no improvement: 36
  lines already exist in ℝ¹⁵, and 57 ≤ N(18) ≤ 59 (table in arXiv:2603.02469,
  https://arxiv.org/abs/2603.02469). **Honest negative.**
* No practical claim beyond these is made.

## Step 10 — Documentation

`record.yaml` (claims, journal). Textbook: Chapter 15
(`textbook/src/15_graph_products.md`, Volume 5).

## Next directions

1. Prove (or refute beyond order 16) that two-graphs are a free commutative
   monoid under ⊕ — e.g. via twin reducts and an analogue of McKenzie's
   theorem for Kronecker products of ±1 matrices.
2. Decide whether the product 141 has unique factorisation on connected graphs
   (equivalently ⊕ on co-connected graphs); no collision to order 15.
3. Characterise all pairs X ≁ Y with G ⊕ X ≅ G ⊕ Y (which G absorb switching?
   K_{a,a} does; 3K₁ and K_{1,2} only in combination).
4. Extend the character analysis to directed graphs and to products with
   loops (the direct product's unit is a looped vertex).
