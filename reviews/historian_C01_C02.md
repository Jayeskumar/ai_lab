# Historian and Novelty Review: cycles C01 and C02

*Reviewer:* Historian and Novelty Analyst · *Date:* 2026-10-18 · *Scope:* every claim
CLM-C01-01 … CLM-C01-08 and CLM-C02-01 … CLM-C02-10.

*Inputs read:* `research/cycles/C01_quantity/{README.md,record.yaml}`,
`research/cycles/C02_exchange/{README.md,record.yaml}`, `proofs/paper/C01.md`,
`proofs/paper/C02.md`, and for cross-checks `results/EXP-C01-06.json`,
`results/EXP-C01-07.json`, `results/EXP-C02-02.json`.

*Method:*
- Web search.
- Full texts read for every source that decided a label (not only abstracts). These were
  Gray–Steinberg 2022 and 2026, the Nyberg-Brodda survey, Kudryavtseva 2010, Kurth 1987,
  Geser–Zantema 1999, Albenque–Nadeau 2009, Akiyama–Frougny–Sakarovitch 2008,
  Scheicher et al. 2014, Baird-Smith et al. 2018, Cusenza et al. 2020/22, Cheigh et al.,
  Borodin et al. and Propp 2017.
- All bibliographic data checked against Crossref or the source itself.
- OEIS searched through `lab.oeis`; the new responses are cached in `cache/oeis`.
- Independent computations were run in a scratch directory outside the repository
  (section 6).

Apart from those OEIS cache entries, this file is the only thing written to the repository.

**Labels used.**
- **REDISCOVERY:** the statement is in the literature (cited), or it is a special case or
  immediate generalisation proved by literally the same argument. Where only the latter
  holds, the text says so.
- **POTENTIALLY NOVEL:** nothing equivalent was found in the sources searched. This is never a
  priority claim.
- **NOT ASSESSED:** could not be evaluated.

Tags used in the text:
- **[LIT]:** stated in a cited source.
- **[DERIVED]:** our own deduction from cited results. Not peer-checked; the Skeptic should
  verify it.
- **[COMPUTED]:** our own computation (section 6).

---

## 0. Executive summary

1. **CLM-C01-08 (common-border conjecture) is far less open, and far less novel, than recorded.**
   - **Case c(x) = 1 (u and v share no border).** This is a corollary of published work.
     - [LIT] Gray and Steinberg (Forum Math. Sigma 2026, Thm 8.1): a one-relator monoid
       ⟨A | u = v⟩ with no non-empty word r such that u, v ∈ A\*r ∩ rA\* has Hochschild
       cohomological dimension ≤ 2.
     - [DERIVED] For |u| = |v| that hypothesis means exactly "no common border". Standard
       homological algebra then gives gl.dim K⟨A⟩/(u − v) ≤ 2, so u − v is strongly free
       (Anick 1982), so the growth series is 1/(1 − qx + x^k).
     - [LIT] When u and v begin (or end) with different letters, the formula is literally
       Corollary 3 of Albenque–Nadeau (2009), which they credit to Bronfman (2001), combined
       with Adjan's cancellativity theorem.
     - **[COMPUTED] All 527 relations that `EXP-C01-07` lists as open have c = 1.** So every
       relation the lab could not prove is settled by the literature.
   - **Border-containment case.** Rediscovery (CLM-C01-06, below).
   - **What remains genuinely unpublished:** relations with at least one common border where
     neither border set contains the other.
     - [COMPUTED] In the lab's test range this case has only **12 relations** (6 up to a↔b),
       each with exactly one common border.
     - The homological counterpart of the dichotomy "common border or not" is published:
       Gray–Steinberg (Selecta 2022), Thm B / Thm 3.3. There, cd ≤ 2 iff there is no common
       border, and cd = ∞ when there is exactly one.
     - [DERIVED] Two growth identities follow from the same paper (Thm 6.6, Props 8.3 and
       8.5). Together they imply the conjecture whenever u and v have exactly one common
       border, and they point to a proof of the general case by induction over compression.
     - [COMPUTED] The identities and the conjecture were checked numerically, including 6
       "hard" relations with two common borders at k = 8, 9. These lie outside the lab's test
       set, which contains none.
2. **CLM-C01-06 is a rediscovery.**
   - The confluence part is the length-preserving case of the one-rule confluence criterion:
     Kurth 1987, building on Book 1983 and Otto–Wrathall 1985; see also Wrathall 1992.
   - The counting part is Guibas–Odlyzko (1981).
   - The converse is also known: u→v is confluent **iff** Borders(u) ⊆ Borders(v)
     ([COMPUTED]: no counterexample among 152,928 ordered pairs).
3. **CLM-C02-10's table is published.**
   - [LIT] The longest Zeckendorf games for n ≤ 49 appear in Baird-Smith, Epstein, Flint and
     Miller (2018/2020), Figs 3–4. The lab's values for n ≤ 40 are identical.
   - [LIT] The greedy strategy that realises the longest game was proved optimal by Cusenza et
     al. (Fibonacci Quart. 2022). A closed form is known only for n = F_k − 1; the general
     case is stated as open (Cheigh et al.).
   - The sequence is still missing from the OEIS, so the lab could contribute it.
4. **CLM-C02-07 and CLM-C02-08 are rediscoveries in substance.** They transplant
   Akiyama–Frougny–Sakarovitch (2008) from the polynomial qX − p to Σ b_j y^j − m: Lemma 5
   (the Gauss-lemma and constant-term argument, word for word) and Prop. 11 (radix order).
   The general non-monic digit-system framework is Scheicher–Surer–Thuswaldner–van de
   Woestijne (2014).
5. **CLM-C02-03 is elementary folklore; CLM-C02-04 is the only C02 claim with no equivalent found.**
   - CLM-C02-03 rests on token-count and value monovariants; it is the half-line analogue of
     the Bond–Levine halting criterion.
   - CLM-C02-04 (the uniform glider when Σb = m) is POTENTIALLY NOVEL, with low–medium
     confidence. The rule family m → p(x) was proposed, with no results, by Propp (2017).

## 1. Summary table

| Claim | Current label | Recommended | Conf. | Closest prior work |
|---|---|---|---|---|
| C01-01 | REDISCOVERY | REDISCOVERY (refs OK) | high | Parikh 1966; Cartier–Foata 1969 |
| C01-02 | REDISCOVERY | REDISCOVERY (refs OK) | high | Howie 1995, monogenic semigroups |
| C01-03 | REDISCOVERY | REDISCOVERY (refs OK) | high | congruences on (ℕ,+), Howie 1995 |
| C01-04 | REDISCOVERY | REDISCOVERY (refs OK) | high | standard (End(ℕ) ≅ (ℕ,+,·); End(ℕ²) = 2×2 matrices over ℕ) |
| C01-05 (refuted) | NOT ASSESSED | REDISCOVERY (the negative answer is implied by known lower bounds) | high | Golod–Shafarevich/Anick bound H ≥ 1/(1−qx+x^k) (Anick 1982; Piontkovski 1999) |
| C01-06 | NOT ASSESSED | **REDISCOVERY** | high | Kurth 1987 (SLC B18m); Otto–Wrathall 1985; Wrathall 1992; Guibas–Odlyzko 1981 |
| C01-07 | NOT ASSESSED | **REDISCOVERY for 1620/1632 instances**; POTENTIALLY NOVEL for 12 | med-high | as C01-06 (833 instances); Gray–Steinberg 2026 Thm 8.1 and Albenque–Nadeau 2009 Cor. 3 (787 instances) |
| C01-08 | POTENTIALLY NOVEL | **POTENTIALLY NOVEL only for "common border, no containment"**; REDISCOVERY for c = 1 and for containment | medium | Gray–Steinberg 2022 (Thm B, §§6–9); Gray–Steinberg 2026 (Thm 8.1); Anick 1982; Albenque–Nadeau 2009 |
| C02-01 | REDISCOVERY | REDISCOVERY (add Legendre's formula) | high | carrying / chip-firing on a path; Legendre's formula |
| C02-02 | REDISCOVERY | REDISCOVERY (refs OK) | high | Björner–Lovász–Shor 1991; Dhar 1990; Bond–Levine 2016 |
| C02-03 | NOT ASSESSED | **REDISCOVERY (folklore)** | medium | Björner–Lovász 1992 (sink); Bond–Levine 2016 (halting criterion); Tanton's machines; AFS 2008 |
| C02-04 | NOT ASSESSED | **POTENTIALLY NOVEL** | low-med | Propp 2017 (family proposed, no results); Bond–Levine 2016 (critical case, finite networks only) |
| C02-05 | NOT ASSESSED | POTENTIALLY NOVEL (minor: only the 28 Σb = m certificates); rest REDISCOVERY | medium | as C02-03 and C02-04 |
| C02-06 (refuted) | NOT ASSESSED | REDISCOVERY | high | redundant digit sets (Avizienis 1961); AFS 2008 requires gcd(p,q) = 1 |
| C02-07 | NOT ASSESSED | **REDISCOVERY (in substance)** | high | AFS 2008 Lemma 5; Scheicher et al. 2014; Kovács–Pethő 1991 |
| C02-08 | NOT ASSESSED | **REDISCOVERY (in substance)** | medium | AFS 2008 Prop. 11 |
| C02-09 | REDISCOVERY | REDISCOVERY (refs OK) | high | Baird-Smith et al. 2018/2020; OEIS A219641 |
| C02-10 | REDISCOVERY | **REDISCOVERY (correct the basis: table published)** | high | Baird-Smith et al. Figs 3–4; Cusenza et al. 2022 Thm 1.2–1.4; Cheigh et al. 2025 |

---

## 2. Cycle C01: detailed assessments

### CLM-C01-01: symbol counts are the complete invariant of commutation. REDISCOVERY (high)

- **Known:** the free commutative monoid on Σ is ℕ^Σ (Parikh vectors), and partial commutation
  gives trace monoids. See Parikh, *On context-free languages*, J. ACM 13 (1966) 570–581,
  https://doi.org/10.1145/321356.321364, and Cartier–Foata, *Problèmes combinatoires de
  commutation et réarrangements*, LNM 85 (1969), https://doi.org/10.1007/BFb0079468.
- **New:** nothing. The Lean formalisation is a contribution to verification, not to
  mathematics.

### CLM-C01-02 and CLM-C01-03: one-symbol relations (index and period). REDISCOVERY (high)

- **Known:** these are the index and period of monogenic semigroups and monoids, and the
  description of finitely generated congruences on (ℕ,+): the generated congruence is the one
  with index min mᵢ and period gcd(nᵢ − mᵢ). See J. M. Howie, *Fundamentals of Semigroup
  Theory*, LMS Monographs 12, OUP 1995, https://academic.oup.com/book/53985.
- **New:** nothing.

### CLM-C01-04: multiplication as composition of substitutions. REDISCOVERY (high)

Textbook facts: End(ℕ,+) ≅ (ℕ,+,·), and End(ℕ²) is the monoid of 2×2 matrices over ℕ,
which is non-commutative. Nothing new.

### CLM-C01-05 (refuted H-C01-4). Recommended: REDISCOVERY (high)

- **Why the refutation is known:**
  - For one homogeneous relation of degree k on q letters, the Golod–Shafarevich/Anick lower
    bound gives H(x) ≥ |1/(1 − qx + x^k)|, coefficientwise. See D. J. Anick, *Non-commutative
    graded algebras and their Hilbert series*, J. Algebra 78 (1982) 120–140,
    https://doi.org/10.1016/0021-8693(82)90104-1, and the statement in D. Piontkovski,
    *Growth and relations in graded rings*, https://arxiv.org/abs/math/9903030.
  - For q = 2 and k ≥ 3 that bound grows exponentially, while Parikh classes number n + 1.
  - So no relation of length ≥ 3 can induce counting equivalence. The explicit counterexample
    (aab ↔ aba isolates baa) is immediate.
- **New:** nothing.

### CLM-C01-06: border-containment theorem. REDISCOVERY (high)

The theorem has three parts.
1. Borders(u) ⊆ Borders(v) implies {u→v} is convergent.
2. The classes correspond to u-avoiding words.
3. The generating function is c_u/(x^k + (1 − qx)c_u).

**Known [LIT].**
- **Confluence, part (1).** W. Kurth, *Some combinatorial properties of complete semi-Thue
  systems*, Séminaire Lotharingien de Combinatoire B18m (1987),
  https://www.mat.univie.ac.at/~slc/opapers/s18kurth.html.
  - Kurth's theorem: let u→v satisfy the chain condition, and write the self-overlaps
    (borders) of u as u₁…u_k, u₂…u_k, …. Then the system is confluent **iff** either
    (a) v has u₁…u_k, the longest border of u, as a self-overlap, or (b) v is a suffix of u of
    a special form.
  - For |u| = |v|, termination is automatic (the lab's lexicographic argument) and (b) is
    impossible.
  - Every border of u is the longest border z or a border of z. So (a) holds iff
    Borders(u) ⊆ Borders(v).
  - Kurth generalises Book (1983) and F. Otto and C. Wrathall, *A note on Thue systems with a
    single defining relation*, Math. Systems Theory 18 (1985) 135–143,
    https://doi.org/10.1007/BF01699465.
  - Related: C. Wrathall, *Confluence of one-rule Thue systems*, LNCS 572 (1992) 237–246,
    https://doi.org/10.1007/3-540-55124-7_11. As quoted by A. Geser and H. Zantema,
    *Non-looping string rewriting*, RAIRO ITA 33 (1999) 279–301,
    https://www.numdam.org/article/ITA_1999__33_3_279_0.pdf: a length-increasing one-rule
    system is confluent iff every self-overlap of l is a self-overlap of r. We could not read
    Wrathall's paper itself.
- **Part (2).** Standard for convergent systems; equivalently, {u − v} is a Gröbner basis of
  (u − v) in K⟨Σ⟩.
- **Part (3).** L. J. Guibas and A. M. Odlyzko, *String overlaps, pattern matching, and
  nontransitive games*, J. Combin. Theory A 30 (1981) 183–208,
  https://doi.org/10.1016/0097-3165(81)90005-4.

**Computed.** [COMPUTED] For every ordered pair u ≠ v with |u| = |v|, binary k ≤ 8 (86,868 pairs)
and ternary k ≤ 5 (66,060 pairs), confluence of u→v (all critical pairs joinable) coincides
with Borders(u) ⊆ Borders(v). There are 0 mismatches. This confirms the "iff".

**New:** the overlap lemma is now Lean-verified. That is a verification asset, not new
mathematics.

**Suggested wording:** "Special case (length-preserving) of the one-rule confluence criterion
of Kurth (1987) / Otto–Wrathall (1985) / Wrathall (1992), combined with Guibas–Odlyzko (1981).
The converse also holds."

### CLM-C01-07: 1632 computer-assisted cases. REDISCOVERY for 1620 instances; POTENTIALLY NOVEL for 12 (medium-high)

The 1632 relations split as follows ([COMPUTED] from `results/EXP-C01-07.json`).

**833 border-containment relations.** These are instances of CLM-C01-06 (Kurth and
Guibas–Odlyzko).

**799 "hard" relations proved by finite completion.**
- **787 have no common border (c = 1).** These are instances of the published c = 1 case
  (see CLM-C01-08 (A)).
- **12 have exactly one common border, with no containment.** These are instances of the
  genuinely unpublished case:
  - aaaaa↔ababa, aabaa↔ababa, aaaaaa↔abaaba, aaabaa↔abaaba, aabaaa↔abaaba and
    aabbaa↔abaaba,
  - plus their a↔b swaps.

The computer-assisted method itself (finite Knuth–Bendix completion, then the automaton of
normal forms, then a rational series) is standard. It is Ufnarovski's framework for algebras
with a regular set of normal words: V. A. Ufnarovskij, *Combinatorial and asymptotic methods in
algebra*, Encycl. Math. Sci. 57 (1995), https://doi.org/10.1007/978-3-662-06292-0_1.

### CLM-C01-08: common-border conjecture. Priority (a)

**Statement.** For u ≠ v ∈ Σ^k with q = |Σ|,

H(x) := Σ_n |Σ^n/∼| x^n = c(x) / (x^k + (1 − qx) c(x)),

where c(x) = 1 + Σ_{b common border} x^{k−|b|}.

Note that H is the growth series of the homogeneous monoid M = ⟨Σ | u = v⟩. It is also the
Hilbert series of K⟨Σ⟩/(u − v).

#### (A) Case c = 1 (no common border): a corollary of published results

**Literature.**
- [LIT] R. D. Gray and B. Steinberg, *Two-sided homological properties of special and
  one-relator monoids*, Forum of Mathematics, Sigma 14 (2026) e58,
  https://doi.org/10.1017/fms.2026.10209 (arXiv:2507.04819; theorem numbering as in arXiv v2).
  - Theorem 8.1: if M = ⟨A | u = v⟩, with u and v non-empty, has no non-empty r such that
    u, v ∈ A\*r ∩ rA\*, then M is bi-FP∞ and has Hochschild cohomological dimension ≤ 2.
  - Here the Hochschild cohomological dimension is the projective dimension of ℤM over
    ℤ[M × M^op].
  - The proof combines Kobayashi's strict-asphericity theorem with the two-sided Cayley
    complex. The Kobayashi papers are Y. Kobayashi, J. Pure Appl. Algebra 130 (1998)
    159–195, https://doi.org/10.1016/S0022-4049(97)00095-9 (Cor. 5.6), and J. Algebra 229
    (2000) 547–569, https://doi.org/10.1006/jabr.1999.8251.
- [DERIVED, standard] For |u| = |v| = k, u ≠ v, such an r would have |r| < k. So the
  hypothesis says exactly that u and v have no common border.
- [DERIVED, standard] Then:
  - Tensor a length-2 projective ℤ[M × M^op]-resolution of ℤM with a field K. All modules are
    ℤ-free, so it stays exact. Hence pd_{(KM)^e} KM ≤ 2.
  - Hence gl.dim KM ≤ 2: the Hochschild dimension bounds the global dimension.
  - KM = K⟨Σ⟩/(u − v) is connected graded with q generators of degree 1 and one minimal
    relation of degree k. So its minimal resolution of K is
    0 → KM(−k) → KM(−1)^q → KM → K → 0.
  - Therefore H(x)(1 − qx + x^k) = 1, which is the conjecture with c = 1.
  - Equivalently, u − v is strongly free in Anick's sense. For a free algebra, strongly free
    means gl.dim ≤ 2 (Anick 1982; see the statement in Piontkovski, arXiv:math/9903030).
- [LIT] Independent route for u₁ ≠ v₁ (different first letters), and for different last
  letters by reversing all words. M. Albenque and P. Nadeau, *Growth function for a class of
  monoids*, FPSAC 2009, DMTCS proc. AK, 25–38, https://dmtcs.episciences.org/2728.
  - Corollary 3, credited there to Bronfman 2001: if M is homogeneous, atomic and
    left-cancellative, and every set of atoms with a common right multiple has a right lcm,
    then G_M(t) = [Σ_J (−1)^{|J|} t^{|lcm J|}]^{−1}.
  - Left cancellativity is Adjan's theorem, when u and v begin with different letters.
  - The cliques are ∅, the singletons and {u₁, v₁}, whose lcm is [u]. [DERIVED: any
    derivation that changes the first letter must rewrite at position 0.]
  - So G = 1/(1 − qt + t^k). Known special cases include Kudryavtseva's n + 1 count (k = 2,
    q = 2; L. A. Kudryavtseva, Izv. Saratov Univ. 10(1) (2010) 14–18,
    https://doi.org/10.18500/1816-9791-2010-10-1-14-18) and positive dihedral Artin monoids,
    for example aba = bab, the positive braid monoid B₃⁺ (Albenque–Nadeau §3).
- [DERIVED, alternative] A degree-filtration argument on the contractible Cayley complex also
  works. Its ingredients are Kobayashi 1998 (strict asphericity), Gray–Steinberg 2022
  Lemma 6.4, and Adjan or Gray–Steinberg 2022 Lemma 7.1 for injectivity of the top-degree
  boundary. It gives the same identity.

**Consequences for the lab's data.** [COMPUTED]
- All 527 relations listed as "open, no finite completion" in `EXP-C01-07` have c = 1. 519
  of them have different first or different last letters, so the Albenque–Nadeau route
  applies. The remaining 8 (e.g. aabaab↔abaaab) need the Gray–Steinberg 2026 route.
- Of the lab's 1326 "hard" relations, 1314 have c = 1. The other 12 have exactly one common
  border. None has two.

#### (B) Containment case: REDISCOVERY (CLM-C01-06)

#### (C) Remaining case (common border, no containment): POTENTIALLY NOVEL (medium)

**What is published (homological counterpart) [LIT].** R. D. Gray and B. Steinberg, *A Lyndon's
identity theorem for one-relator monoids*, Selecta Math. 28 (2022) no. 3, art. 59,
https://doi.org/10.1007/s00029-022-00773-3 (arXiv:1910.09914).
- **Theorem B / Thm 3.3 (with |v| ≤ |u|).** Let z be the longest word that is a prefix and a
  suffix of both u and v.
  - For torsion-free M, cd ≤ 2 iff z = ε (or z = v).
  - In the non-subspecial case, compressibility by a unique word gives cd = ∞ (Prop. 9.5).
  - Otherwise compressibility gives cd ≥ 3.
  - For homogeneous relations: M is always torsion-free and non-subspecial; "compressible"
    means "has a common border"; "unique compressing word" means "exactly one common
    border".
  - So their dichotomy is exactly the lab's dichotomy c = 1 versus c ≠ 1, for the trivial
    module.
  - The conjectured series is consistent with it: 1/H = 1 − qx + x^k/c(x) has infinitely many
    terms when c ≠ 1.
- **Thm 6.6/6.7.** There is a contractible 2-complex K: the Cayley graph, with 2-cells attached
  at the vertices of M[z] and labelled u′, v′, where u = zu′ and v = zv′. Its exact sequence is
  0 → ℤM[z] → ℤM^{|A|} → ℤM → ℤ → 0.
- **Props 8.3, 8.5.** Let y be the shortest and z the longest common border, and write
  u = u″y, v = v″y. There is an exact sequence 0 → ℤM[z] → ℤM —·[y]→ ℤM[y] → 0, with kernel
  ℤM([u″] − [v″]) ≅ ℤM[z].
- **Compression.** Lallement 1974 (https://doi.org/10.1016/0021-8693(74)90146-X) and
  Adjan–Oganesyan (1978 and 1987; the Nyberg-Brodda survey §3 explains which paper contains
  which version). It is recast in Gray–Steinberg 2022 §4 (Props 4.11, 4.13, Cor. 4.15) and §8
  (Prop. 8.6).

**Two growth identities [DERIVED from the above; numerically confirmed].** Define

G_w(x) := Σ_{s ∈ M[w]} x^{|s|−|w|}, where M[w] is the left ideal M·[w].

- **(P)** H(x) = G_y(x) + x^{k−|y|} G_z(x). This is Props 8.3 and 8.5 read degree by degree;
  all maps involved are homogeneous.
- **(E)** H(x)(1 − qx) + x^k G_z(x) = 1. To derive it:
  - Filter the contractible complex K of Thm 6.6 by degree.
  - Each finite sub-level complex F_N is acyclic, provided the top-degree part of ∂₂ is
    injective.
  - That injectivity amounts to right multiplication by [u′₋] − [v′₋] being injective on
    ℤM[z], where w₋ means w without its last letter.
  - That in turn follows from the arguments in the proof of Prop. 8.5 (Lemma 4.10, Prop. 8.4,
    Lemma 7.1, Adjan).
  - So χ(F_N) = 1 for every N.
- **Consequence for exactly one common border (y = z).** By (P), G_z = H/(1 + x^{k−|z|}).
  Substituting into (E) gives H = c/(x^k + (1 − qx)c) with c = 1 + x^{k−|z|}. **This is the
  conjecture.** It covers all 12 such relations in the lab's range.
- **Several common borders.** Given (E), the conjecture is equivalent to G_z = H/c, and by (P)
  to G_y = (c − x^{k−|y|})·G_z. This is the analogous statement for the Adjan–Oganesyan
  compression N, a one-relator monoid over an infinite, weighted alphabet. It holds because
  M[y] is a free right N-set and ℤM[z] ≅ ℤM[y] ⊗_{ℤN} ℤN[z′] (Gray–Steinberg Props 4.13,
  8.6). This suggests an induction on the number of common borders. We have not carried it
  out.
- [COMPUTED] (E), (P) and the conjecture hold for:
  - one common border: ababa↔aabaa, aaba↔abaa, abaaba↔abbaba and aabaa↔abbaa (n ≤ 13), and
    the ternary abca↔acba (n ≤ 8);
  - two common borders (a, aa), hard: aaaaaaaa↔aabaabaa, aaaabaaa↔aabaabaa,
    aaabaaaa↔aabaabaa, aaaaaaaaa↔aabaaabaa, aaaaabaaa↔aabaaabaa and aaaabaaaa↔aabaaabaa
    (n ≤ 15);
  - c = 1 with the same first and last letter: the conjecture holds for aabaab↔abaaab,
    abbaab↔abbabb and babbba↔bbabba (n ≤ 16), and (E) also holds for aabaab↔abaaab
    (n ≤ 13).

**Searched without finding the growth formula.** The search covered Hilbert series of
one-relator binomial algebras; Anick (strongly free sets); Piontkovski (FPM 2001 coherence and
divisibility paper,
https://www.maths.tcd.ie/EMIS/journals/FPM/eng/k01/k012/k01211h.htm; math/9903030;
math/0502149); Iyudu–Shkarin and Cameron–Iyudu (JSC 2007); Ufnarovski; Golod–Shafarevich;
Cain–Maltcev and Cain–Gray–Malheiro (homogeneous monoids, Inf. Comput. 255 (2017),
https://doi.org/10.1016/j.ic.2017.05.003); Shneerson–Easdown (growth); the Nyberg-Brodda
survey (Semigroup Forum 103 (2021), https://doi.org/10.1007/s00233-021-10216-8, which only
notes that |u| = |v| makes the word problem trivial); Rigo, *Relations on words*
(Indag. Math. 28 (2017), https://doi.org/10.1016/j.indag.2016.11.018); and the OEIS (no
"one-relation monoid" entries).

**Recommendation.**
- Split CLM-C01-08:
  - (i) c = 1: REDISCOVERY, as a corollary of Gray–Steinberg 2026 Thm 8.1 + Anick 1982, and
    of Albenque–Nadeau 2009 Cor. 3 + Adjan for different first or last letters;
  - (ii) containment: REDISCOVERY (CLM-C01-06);
  - (iii) common border without containment: POTENTIALLY NOVEL.
- Rewrite the `novelty_basis` to cite Gray–Steinberg 2022 Thm B as the homological counterpart.
- Mark the 527 "open" relations as settled by literature, after the Skeptic checks the
  deduction in (A).
- Pursue a proof of (iii) via (E), (P) and compression rather than Anick chains.
- Extend the test set to hard relations with ≥ 2 common borders. These first occur at
  binary k = 8.

**Confidence.**
- Medium that the explicit formula in case (iii) is unpublished. No MathSciNet or zbMATH full
  text was available, and the Russian-language one-relation literature (Adjan school) was
  only searched indirectly.
- High that (A) and (B) are known in substance.

---

## 3. Cycle C02: detailed assessments

### CLM-C02-01: integer bases from b[k] → [k+1]. REDISCOVERY (high)

- **Known:** this is carrying, or chip-firing on a path.
- **Step count:** the number of firings is Σ_{i≥1}⌊n/bⁱ⌋ = (n − s_b(n))/(b − 1). That is
  Legendre's identity, https://en.wikipedia.org/wiki/Legendre%27s_formula. Suggested
  addition to `novelty_basis`.

### CLM-C02-02: abelian property. REDISCOVERY (high)

- **References are correct:**
  - A. Björner, L. Lovász and P. Shor, *Chip-firing games on graphs*, European J. Combin. 12
    (1991) 283–291, https://doi.org/10.1016/S0195-6698(13)80111-4;
  - D. Dhar, PRL 64 (1990) 1613, https://doi.org/10.1103/PhysRevLett.64.1613;
  - B. Bond and L. Levine, *Abelian networks I*, SIAM J. Discrete Math. 30 (2016) 856–874,
    https://doi.org/10.1137/15M1030984.

### CLM-C02-03: termination dichotomy away from Σb = m. REDISCOVERY, folklore (medium)

**Known.**
- **(a) Σb < m.** Each firing loses m − Σb tokens. This is chip-firing with a sink: model it
  as m − Σb edges to a sink, as in Borodin et al. below and A. Björner and L. Lovász,
  *Chip-firing games on directed graphs*, J. Algebraic Combin. 1 (1992) 305–328,
  https://doi.org/10.1023/A:1022467132614.
- **(b) Σb > m.** The value-conservation bound is elementary.
  - Tanton's Exploding Dots explicitly notes that the 1←1 and 2←1 machines "fire off to
    infinity", https://gdaymath.com/lessons/explodingdots/9-2-base-one-half/.
  - In general this is the infinite half-line analogue of the halting criterion of B. Bond and
    L. Levine, *Abelian networks II. Halting on all inputs*, Selecta Math. 22 (2016) 319–340,
    https://doi.org/10.1007/s00029-015-0192-z. A finite irreducible network halts on all
    inputs iff its production matrix has spectral radius < 1. This does not apply verbatim,
    because the half-line network is infinite and acyclic.
- **Context:** the condition m > Σb says that the constant coefficient of the carry
  polynomial exceeds the sum of the others. That is the weak form of the "representation of
  zero" property used for parallel addition by C. Frougny, E. Pelantová and M. Svobodová,
  TCS 412 (2011) 5714–5727, https://doi.org/10.1016/j.tcs.2011.06.028. Their strong form
  needs the dominant coefficient to exceed twice the sum of the others. This is context only.

**New:** nothing substantive. The general statement was not found verbatim; it is a two-line
consequence of standard monovariants.

### CLM-C02-04: uniform glider for Σb = m. POTENTIALLY NOVEL (low–medium)

**Closest prior work.**
- J. Propp, *How do you write one hundred in base 3/2?* (17 Sep 2017),
  https://mathenchant.wordpress.com/2017/09/17/how-do-you-write-one-hundred-in-base-32/.
  Endnote 3 proposes exactly the lab's family "m → p(x), p with non-negative coefficients",
  notes that the roots of p(x) = m matter, and hopes someone will study it. It gives no
  termination results.
- M. Borodin, H. Han, K. Ji, T. Khovanova et al., *Chip-firing and fractional bases*,
  Minnesota J. Undergrad. Math. 6 (2021),
  https://pubs.lib.umn.edu/index.php/mjum/article/download/4235/2906/19697. This studies
  two-directional a–b firing on ℤ, which always terminates.
- Bond–Levine 2016: in the critical case λ = 1, a finite network does not halt on all inputs.
- The trivial glider of the 1←1 machine (Tanton).

**New:** the statement that every Σb = m rule has a unary start reaching the uniform-firing
window T = (tail sums of b). The lab's Lemma 4 (T is a fixed point, and domination forces
infinite firing) is elementary. The spreading step is open, and we found no literature on it.

### CLM-C02-05: classification of 189 small rules (computer-assisted). POTENTIALLY NOVEL, minor (medium)

- The Σb < m rules (31) and Σb > m rules (130) follow from CLM-C02-03.
- Only the 28 certificates for Σb = m are new data. They are instances of CLM-C02-04.

### CLM-C02-06 (refuted H-C02-4). REDISCOVERY (high)

- Non-uniqueness with digits beyond the base (4[k] → 2[k+1] gives base 2 with digits 0..3)
  is the classical redundancy of number systems. See A. Avizienis, IRE Trans. Electron.
  Comput. EC-10 (1961) 389–400, https://doi.org/10.1109/TEC.1961.5219227.
- Akiyama–Frougny–Sakarovitch assume gcd(p, q) = 1 precisely to exclude it.

### CLM-C02-07: uniqueness when the reduced carry polynomial is primitive and irreducible. REDISCOVERY in substance (high)

**Known [LIT].** S. Akiyama, C. Frougny and J. Sakarovitch, *Powers of rationals modulo 1 and
rational base number systems*, Israel J. Math. 168 (2008) 53–91,
https://doi.org/10.1007/s11856-008-1056-4 (PDF: https://www.irif.fr/~cf/publications/IJM.pdf).
- Lemma 5 proves injectivity of evaluation by exactly the lab's argument: the difference
  polynomial vanishes at p/q; by Gauss's lemma it is divisible by qX − p; and the constant
  term has absolute value < p, giving a contradiction.
- Theorem 1 gives uniqueness of finite representations.

**General framework.** K. Scheicher, P. Surer, J. M. Thuswaldner and C. E. van de Woestijne,
*Digit systems over commutative rings*, Int. J. Number Theory 10 (2014) 1459–1483,
https://doi.org/10.1142/S1793042114500389 (arXiv:1004.3729).
- It allows non-monic P, with any system of residues modulo X as digits; {0..m−1} qualifies
  when P(0) = −m.
- The digit sequence of each element of ℤ[x]/(P) is unique.
- For primitive irreducible P, Gauss's lemma identifies equality in ℤ[x]/(P) with equality
  of values at the real root. [DERIVED, standard]
- The monic, canonical-number-system ancestor is Kovács and Pethő, Acta Sci. Math. (Szeged)
  55 (1991) 287–299, surveyed in A. Pethő and J. Thuswaldner, *Number systems over orders*,
  https://arxiv.org/abs/1708.04800.

**New:** the general family Σ b_j y^j − m was not found stated verbatim, but the proof is AFS
Lemma 5 word for word. The Lean formalisation (`digits_unique`) is a verification asset.

### CLM-C02-08: radix monotonicity. REDISCOVERY in substance (medium)

- **Known [LIT]:** AFS 2008 Prop. 11 (radix order agrees with numerical order on L_{p/q}),
  together with their "boosted Pascal machine" odometer (§3.2.3).
- **New:** only the general rule. That statement was not found verbatim, but the lab's
  three-line proof is the odometer argument.

**Note on the rational case (applies to the C02 README).** The lab's rule p→q is the
chip-firing "base p/q" of Propp, Tanton, OEIS A024629 (https://oeis.org/A024629) and Borodin
et al. AFS normalise differently: their expansion of N is the chip representation of qN. For
example, AFS give 3 ↦ 210 and A024629 gives 6 ↦ 210. So "AFS 2008 = A024629" holds up to this
rescaling.

### CLM-C02-09: Fibonacci exchanges = the Zeckendorf game. REDISCOVERY (high)

- **References are correct:** P. Baird-Smith, A. Epstein, K. Flint and S. J. Miller, *The
  Zeckendorf Game*, in Combinatorial and Additive Number Theory III, Springer PROMS 297
  (2020) 25–38, https://doi.org/10.1007/978-3-030-31106-3_3 (arXiv:1809.04881).
  - Theorem 1.2: termination, via the monovariant Σ√(index) of Lemma 2.1, which works from
    any configuration.
  - Theorem 1.3: the shortest game has n − Z(n) moves.
- **Rule match.** The lab's R1–R4 are exactly their moves, with level k corresponding to their
  F_{k+1}. The shortest-game sequence is OEIS A219641.

### CLM-C02-10: longest Fibonacci derivations, n ≤ 40. REDISCOVERY (high); correct the basis

**Known [LIT].**
- Baird-Smith et al. (above) list the longest game for n = 1..49 in Fig. 4 ("computer proven
  data", exhaustive Java search) and Fig. 3 (greedy algorithm).
  - Their values are 0,1,2,3,5,6,8,10,11,13,15,17,20,21,23,25,26,29,31,34,37,38,40,42,44,47,
    48,50,53,54,57,60,63,67,68,70,72,73,76,78,81,84,85,87,89,91,95,96,98.
  - The first 40 are identical to `max_len_seq` in `results/EXP-C02-02.json`.
- A. Cusenza, A. Dunkelberg, K. Huffman, D. Ke, M. McClatchey, S. J. Miller, C. Mizgerd,
  V. Tiwari, J. Ye and X. Zheng, *Bounds on Zeckendorf games*, Fibonacci Quart. 60 (2022)
  57–71, https://doi.org/10.1080/00150517.2022.12427498 (arXiv:2009.09510).
  - Thm 1.2: the longest game is realised by doing splits and combine-1 moves whenever
    possible, then combining from the smallest index. So the values are computable.
  - Thm 1.3/1.4: the bound Σ a_iδ_i with a_i = F_{i+2} − i − 2 is exact iff n = F_k − 1.
    Checked against the lab's values at n = 4, 7, 12, 20, 33: 3, 8, 17, 34, 63.
- J. Cheigh et al., *Towards the Gaussianity of random Zeckendorf games*, Springer PROMS (2025),
  https://doi.org/10.1007/978-3-031-65064-2_4 (arXiv:2210.11038). It states that a closed
  form for non-Fibonacci inputs remains open, and that all lengths between the shortest and
  longest game occur.

**Computed.** [COMPUTED] The Cusenza greedy algorithm reproduces all 40 lab values. Our own
exhaustive search reproduces n ≤ 30.

**New:** nothing. The sequence is not in the OEIS (the lab's cached query and ours, `"Zeckendorf
game"`, which returns only A219641, A007895, A003107 and the Reversed-Zeckendorf-game entries
A389617–9). Submitting it, citing Baird-Smith et al. and Cusenza et al., would be a
documentation contribution.

---

## 4. Check of references for claims already labelled REDISCOVERY (task c)

| Claim | Lab's reference | Verdict |
|---|---|---|
| C01-01 | Parikh 1966; Cartier–Foata 1969 | correct (DOIs above) |
| C01-02/03 | Howie 1995 (monogenic semigroups; congruences on ℕ) | correct |
| C01-04 | End(ℕ,+) ≅ (ℕ,+,·); End(ℕ²) = matrices | correct (textbook) |
| C02-01 | chip-firing on a path / carrying | correct; add Legendre's formula for the step count |
| C02-02 | Dhar 1990; Björner–Lovász–Shor 1991; Bond–Levine | correct |
| C02-09 | Baird-Smith et al. arXiv:1809.04881; A219641 | correct; published version Springer PROMS 297 (2020) |
| C02-10 | "studied by Cusenza et al.; not in OEIS; no closed form known to us" | **incomplete:** the table itself is in Baird-Smith et al. Figs 3–4; optimality of the greedy algorithm is Cusenza et al. Thm 1.2; closed form only for n = F_k − 1 |
| C02 README, rule p→q | AFS 2008; A024629 | correct up to the AFS normalisation (§3, CLM-C02-08) |
| C01 README, Kudryavtseva 2010 | n + 1 classes for a length-2 case | correct: L. A. Kudryavtseva, k = 2, q = 2 only (relations aa=ab, ab=ba, aa=bb) |

---

## 5. Searches performed (including negative results)

- **Web, priority (a).**
  - Searched: Hilbert series of one-relator (binomial) algebras; growth series of homogeneous
    one-relator monoids; Gray–Steinberg (found: decisive); Kobayashi; Piontkovski (FPM 2001,
    math/9903030, math/0502149: no binomial formula); Iyudu–Shkarin (nothing on one binomial
    relation); Anick strongly free sets; Dicks on one-relator algebras (1985 paper and 1988
    survey found only as titles, not read); Ufnarovski; Golod–Shafarevich; Cain–Maltcev and
    Cain–Gray–Malheiro (no growth results); Shneerson–Easdown (growth of inverse-semigroup
    quotients, not relevant); the Nyberg-Brodda survey; Rigo; Kudryavtseva; one-rule string
    rewriting confluence (Kurth, Wrathall, Otto–Wrathall, Diekert–Wrathall 1995, Geser–Zantema).
  - Found: Albenque–Nadeau and Artin-monoid growth (decisive for subcases).
  - No source states the common-border growth formula.
- **Web, priority (b).**
  - Found: AFS 2008 (decisive); Scheicher et al. 2014; CNS (Kovács–Pethő via Pethő–Thuswaldner);
    Propp 2017; Tanton's Exploding Dots; Borodin et al.; Bond–Levine II;
    Frougny–Pelantová–Svobodová; Baird-Smith et al.; Cusenza et al.; Li et al.
    (arXiv:2006.16457, upper bound 3n − 3Z(n) − IZ(n) + 1); Cheigh et al.
  - Not read in full: Frougny–Sakarovitch, *Number representation and finite automata*
    (CUP 2010, https://doi.org/10.1017/CBO9780511777653.003). Alternate/Cantor real bases
    (Charlier–Cisternino, Monatsh. Math. 195 (2021),
    https://doi.org/10.1007/s00605-021-01598-6) were checked for metadata only. They use a
    sequence of real bases rather than a single carry rule, and no overlap with the lab's
    claims was evident.
- **OEIS (via `lab.oeis`, cached).**
  - Text queries "one-relator monoid", "one-relation monoid", `monoid "one relation" growth`
    and "positive braid monoid": no hits.
  - "Artin monoid" growth: A054761 only.
  - "Zeckendorf game": A389617–9, A007895, A003107, A219641.
  - "longest Zeckendorf game": no hits.
  - "base 3/2" / "rational base": A024629, A081848, A244040, A246435, A383346, etc.

## 6. Independent computations (scratch, outside the repository)

1. **Confluence versus border containment** for length-preserving one-rule systems. All ordered
   pairs, binary k = 2..8 and ternary k = 2..5 (152,928 pairs): 0 mismatches.
2. **Classification of the lab's 1326 hard relations.** 1296 have c = 1 with different first
   or last letters, 18 have c = 1 with equal first and last letters, 12 have one common
   border, and 0 have ≥ 2. The 527 open relations all have c = 1 (519 + 8).
3. **Union-find class counts** compared with the conjectured series and identities (E), (P):
   - the relations listed in §2 (C), within the n-ranges stated there, all agree;
   - the first binary hard relations with two common borders occur at k = 8 (8 relations)
     and k = 9 (18 relations).
4. **Zeckendorf game.**
   - The Cusenza Thm 1.2 greedy algorithm equals the lab's sequence for n ≤ 40, and gives
     81, 84, 85, 87, 89, 91, 95, 96, 98 for n = 41..49, matching Baird-Smith et al. Fig. 4.
   - Exhaustive longest path equals the lab's sequence for n ≤ 30.
5. **Rational base normalisation:** AFS ⟨N⟩ equals the chip representation of qN (checked
   N = 3, 4).

## 7. Caveats

- MathSciNet/zbMATH full-text search was unavailable. Russian-language literature on
  one-relation semigroups (Adjan, Oganesyan, Shneerson) was reached only through surveys and
  citations.
- Wrathall (1992) and Dicks (1985) were not read directly. Wrathall's criterion is taken from
  Geser–Zantema (1999), and Kurth (1987) was read in full.
- The [DERIVED] deductions in §2 (A) and (C) are short. They are the reviewer's own and should
  be checked by the Skeptic before the record is changed. The deduction from Gray–Steinberg
  2026 Thm 8.1 relies only on standard homological algebra. The identities (E) and (P), and the
  one-common-border corollary, also rely on our reading of the proofs of Gray–Steinberg 2022
  Props 8.3–8.6.
- Absence from the sources searched is weak evidence of novelty.
