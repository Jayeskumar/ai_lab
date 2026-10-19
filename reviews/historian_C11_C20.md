# Historian and Novelty Review: cycles C11–C20

*Reviewer:* Historian and Novelty Analyst. I am independent of the researchers who produced the claims.
*Date:* 2026-10-19.

*Scope:*
- the 26 claims of C11–C20 labelled POTENTIALLY NOVEL: CLM-C11-04, -07, -09; CLM-C12-04;
  CLM-C13-02, -03, -04, -11; CLM-C14-04, -05, -07, -10, -13; CLM-C15-04, -07, -15;
  CLM-C16-05, -07, -09, -15; CLM-C19-02, -03, -05, -06, -14; CLM-C20-02;
- the literature question on CLM-C17-05 (currently NOT ASSESSED).

*Inputs read:*
- the 27 records in `db/claims/` (statement, novelty_basis, limitations);
- Step 8 and the hypothesis tables of `research/cycles/C11`–`C17`, `C19`, `C20` README.md;
- `proofs/paper/C11.md`, `C13.md` (Thms 1–3), `C14.md` (Thms 4–11), `C15.md` (setting), `C16.md` (Thm 7),
  `C17.md`, `C19.md` (Thms 1–4), `C20.md`;
- the first 80 lines of `reviews/historian_C01_C02.md` and `reviews/historian_C03_C10.md`;
- the C06 README Step 8 and record, for the Laver citation.

The textbook chapters were only searched (grep) for the sources found below; I did not read them in full.

*Method:*
- About 50 web searches (WebSearch), 3–8 per claim and more for the integer codes, graph products, magma automata,
  quasigroup recurrences and Laver tables.
- arXiv API listings:
  - all 15 papers matching "Zeckendorf" AND "game", and the 40 most recent papers mentioning "Zeckendorf" (to 2026-10-07);
  - "Laver table(s)";
  - "quasigroup" + "de Bruijn";
  - "cellular automata" + magma/groupoid.
- Crossref, OpenAlex and Semantic Scholar for bibliographic data, and OEIS JSON queries.
- Full or partial reading of every source that decided a label. Each PDF was downloaded into its own new directory under
  the session scratchpad (`historian2/<name>/`), treated as untrusted data, and converted with `pdftotext`.
- Light checks (seconds each) in `reviews/historian_checks/C11_C20/`. Their purpose and results are listed in its `NOTES.md`.

*Rules followed:*
- Only this file and `reviews/historian_checks/C11_C20/` were written. No existing file was edited.
- No `lab` command and no git command (not even a read-only one) was run.

**Labels** (as in the earlier reports):
- **REDISCOVERY:** the statement is in the cited literature, or follows from it by literally the same argument.
- **PARTIAL REDISCOVERY** ("partly known"): part of the claim is published; the unpublished residue is named.
- **POTENTIALLY NOVEL:** nothing equivalent was found in the sources searched. This is never a priority claim.
  "(low confidence)" is added when a decisive source could not be read, or when the result is plausibly folklore.

**Tags:**
- **[LIT]:** stated in a cited source that I read.
- **[DERIVED]:** my own short deduction. Unrefereed; for the Skeptic to check.
- **[COMPUTED]:** my own check in `reviews/historian_checks/C11_C20/`.

### Sources read

Format: URL actually fetched, then what was read. "Full" means the whole text; otherwise the parts named.

**Integer codes (C11)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S1 | M. J. de C. Lima, V. C. da Rocha Jr., *Adaptive universal codes for integer representation*, J. Commun. Inf. Syst. (header prints "Vol. 1, No. 28, April 2013"), pp. 8–13 | https://jcis.sbrt.org.br/jcis/article/download/17/11/127 | full (§I–IV, Tables I–VII, references) |
| S2 | A. S. Fraenkel, S. T. Klein, *Robust universal complete codes for transmission and compression*, Discrete Appl. Math. 64 (1996) 31–55 (author preprint) | https://u.cs.biu.ac.il/~tomi/Postscripts/robust.pdf | §2.1, §3 (Thms 1–2), §4.1 (Props 1–2), Props 5–6, references |
| S3 | S. T. Klein, M. K. Ben-Nissan, *On the usefulness of Fibonacci compression codes*, Computer J. 53 (2010) | https://u.cs.biu.ac.il/~tomi/Postscripts/fib-rev.pdf | searched for Capocelli/Lakshmanan/pattern codes (none) |
| S4 | J. H. Thomas, *Variations on the Fibonacci universal code*, arXiv:cs/0701085 | https://arxiv.org/pdf/cs/0701085v2 | full (4 pp.; not relevant) |
| S5 | W. Yan, S.-J. Lin, Y. S. Han, *Generalized universal coding of integers*, arXiv:2204.07398 | https://arxiv.org/pdf/2204.07398 | introduction and references |
| S6 | Crossref record of R. M. Capocelli, *Comments and additions to "Robust transmission of unbounded strings using Fibonacci representations"*, IEEE Trans. Inf. Theory 35 (1989) 191–193, doi:10.1109/18.42193 | api.crossref.org | metadata only; **text not obtained** |

**Divisor game (C12)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S7 | J. Iannucci, U. Larsson, *Game values of arithmetic functions*, arXiv:2101.07608 | https://ar5iv.labs.arxiv.org/html/2101.07608 | list of all rulesets and theorems, as summarised by WebFetch (raw text not read) |
| S8 | U. Larsson, H. Manabe, *Additive subtraction games*, arXiv:2603.10414 | https://arxiv.org/abs/2603.10414 | abstract (not relevant) |

**Anchored magmas (C13)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S9 | Equational Theories Project contributors (Bolan, …, Tao, …), *The Equational Theories Project: advancing collaborative mathematical research at scale*, arXiv:2512.07087v2 | https://arxiv.org/pdf/2512.07087 | §9 "Spectrum of equational laws" |
| S10 | B. Le Floch, *Spectra of equational laws* (ETP notes, dated July 14, 2025) | https://leanprover.zulipchat.com/user_uploads/3121/jrBQt8qmSzvI3w359L3p-LVR/spectrum.pdf | §1–§2.1 |

**Graph products (C14)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S11 | A. Abiad, S. Butler, W. H. Haemers, *Graph switching, 2-ranks, and graphical Hadamard matrices*, arXiv:1801.01149 | https://arxiv.org/pdf/1801.01149 | §4–§5 |
| S12 | S. Oh, H. Yoo, T. Yun, *Rainbow graphs and switching classes*, SIAM J. Discrete Math. 27 (2013) 1106–1111 (doi:10.1137/110855089, Crossref), arXiv:1108.6143v3 | https://arxiv.org/pdf/1108.6143v3 | full |
| S13 | P. P. Mondal, M. R. Kannan, F. Atik, *When are standard graph products isomorphic?*, arXiv:2508.04137 | https://arxiv.org/abs/2508.04137 | abstract (not relevant) |

**Magma automata (C15)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S14 | C. Dürr, I. Rapaport, G. Theyssier, *Cellular automata and communication complexity*, Theoret. Comput. Sci. 322 (2004) 355–368 (doi:10.1016/j.tcs.2004.03.017, Crossref), arXiv:cs/0210008 | https://arxiv.org/pdf/cs/0210008 | full |
| S15 | P.-É. Meunier, *Unraveling simplicity in elementary cellular automata*, arXiv:1406.5306 | https://arxiv.org/abs/1406.5306 | abstract only |

**Fibonacci dynamics (C16)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S16 | P. Klimov, *Universal Fibonacci sequences and UFS-groupoids*, arXiv:2604.05754v2 (v1 7 Apr 2026, v2 6 May 2026) | https://arxiv.org/pdf/2604.05754v2 | introduction, statements of Ch. 4, Ch. 7 (open problems), references; searched for quasigroup/parity/isotope/Laver |
| S17 | Y. Tan, Y. Xu, *On the period factor of quasigroups*, CCIS 2013 (Atlantis Press) | https://www.atlantis-press.com/article/9908.pdf | full (4 pp.; a different object: e-transformations) |
| S18 | S. Li, *SB(3,n) has no Hamiltonian cycle when n is even: a sign-of-permutation proof…*, arXiv:2605.09489 | https://arxiv.org/abs/2605.09489 | abstract only |

**Zeckendorf game (C19)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S19 | A. Cusenza et al., *Bounds on Zeckendorf games*, arXiv:2009.09510 (Fib. Quart. 60, 2022) | https://arxiv.org/pdf/2009.09510 | §1 (Thms 1.2–1.4), §4, references |
| S20 | R. Li et al., *Deterministic Zeckendorf games*, arXiv:2006.16457 | https://arxiv.org/pdf/2006.16457 | §1 (results, conjectures) |
| S21 | J. Cheigh et al., *Towards the Gaussianity of random Zeckendorf games*, arXiv:2210.11038 | https://arxiv.org/pdf/2210.11038 | §1–§2 (open-problem sentence, Lemmas 2.2–2.3) |
| S22 | Z. X. Batterman et al., *The reversed Zeckendorf game*, arXiv:2309.12748; I. Bortnovskyi et al., *The ordered Zeckendorf game*, arXiv:2508.20222; C. Cashman et al., *Black hole Zeckendorf games*, arXiv:2409.10981 | https://export.arxiv.org/api/query?id_list=… ; https://arxiv.org/pdf/2309.12748 | abstracts; 2309.12748 searched for "lazy"/"longest" |
| S23 | arXiv listings `all:Zeckendorf AND all:game` and `all:Zeckendorf` (newest first; last entry 2026-10-07) | https://export.arxiv.org/api/query?search_query=… | titles and abstracts |
| S24 | C. Ahlbach, J. Usatine, C. Frougny, N. Pippenger, *Efficient algorithms for Zeckendorf arithmetic*, Fib. Quart. 51 (2013) | https://www.mathstat.dal.ca/FQ/Papers1/51-3/AhlbachUsatineFrougnyPippenger.pdf | searched (no lazy representations) |

**One-rule rewriting (C20)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S25 | Y. Kobayashi, *The derivational complexity of string-rewriting systems*, RIMS Kôkyûroku 1712 (2010) 140–147 | https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1712-19.pdf | searched (no one-rule details) |
| S26 | A. Kfoury, *String rewriting systems: brief introduction and sample of open problems*, arXiv:2608.19397v2 | https://arxiv.org/pdf/2608.19397 | §5.1 and references |

**Laver tables (C16-15, C17-05)**

| # | Source | URL read | Extent |
|---|---|---|---|
| S27 | P. Biane, *Laver tables and combinatorics*, arXiv:1810.00548v1 (2018) | https://arxiv.org/pdf/1810.00548 | §1–§3, references |
| S28 | P. Biane, *Laver tables and combinatorics*, Sém. Lothar. Combin. 80 (2019), Art. B80c (published version) | https://www.mat.univie.ac.at/~slc/wpapers/s80biane.pdf | §2.1–§2.2 with footnote 1 |
| S29 | P. Dehornoy, *Laver's results and low-dimensional topology* (= arXiv:1401.3302) | https://dehornoy.lmno.cnrs.fr/Surveys/Dij.pdf | §1 (Thm 1.1) |
| S30 | P. Dehornoy, *Some aspects of the SD-world*, arXiv:1711.09792v2 | https://arxiv.org/pdf/1711.09792v2 | Example 1.17 |
| S31 | P. Dehornoy, V. Lebed, *Two- and three-cocycles for Laver tables*, arXiv:1401.2335v2 | https://arxiv.org/pdf/1401.2335v2 | §1 (Thm 1.1, (1.3)–(1.5)) |
| S32 | J. P. Aguilera, M. Iannella, *Non-dyadic Laver algebras*, arXiv:2610.06106v1 (5 Oct 2026) | https://arxiv.org/pdf/2610.06106v1 | full |
| S33 | Wikipedia, *Laver table* | https://en.wikipedia.org/wiki/Laver_table | as quoted by WebFetch (defines only sizes 2ⁿ) |
| S34 | J. Van Name, *Generalizations of Laver tables*, arXiv:1812.02761; R. Qi, *Notes on Laver tables*, arXiv:2501.06733 | arXiv API | abstracts only |

**Other**

| # | Source | URL read | Extent |
|---|---|---|---|
| S35 | OEIS JSON search, queries listed in `historian_checks/C11_C20/NOTES.md` | https://oeis.org/search?q=…&fmt=json | 10 queries |

I also saw, in search snippets only and **not read** (so not used for any verdict):
- Wang (IEEE TIT 34, 1988), flag encoding;
- Yamamoto–Ochi (IEEE TIT 37, 1991);
- Froemke–Quackenbush (Pacific J. Math. 58, 1975);
- Goles–Little–Rapaport (ISAAC 2008);
- the Morisawa and Makino two-pile divisor games;
- Lajou's Cartesian factorisation of signed graphs;
- Couselo–González–Markov–Nechaev (Diskret. Mat. 10, 1998).

### Failed retrievals

| Host / URL | Result |
|---|---|
| jcis.sbrt.org.br/JCIS/article/download/17/11 | HTTP 503 (WebFetch). The alternative URL in S1 worked. |
| ieeexplore.ieee.org/document/42193 (Capocelli 1989) | WebFetch returned an empty page; curl got HTTP 418. |
| api.semanticscholar.org | HTTP 429 on the first query. Later queries returned metadata with the abstract elided by the publisher (Capocelli 1989, KKS 2001). |
| link.springer.com/article/10.1007/s00182-025-00948-0 (2-pile divisor Nim, Int. J. Game Theory) | HTTP 303 redirect to the idp.springer.com login. |
| doaj.org/article/c99e0187f83c4ca0aa369b354d650d23 (EPTCS 1.8) | HTTP 403. |
| www.sciencedirect.com/science/article/pii/S0304397500003674 (Kobayashi–Katsura–Shikishima-Tsuji, TCS 262, 2001) | HTTP 403 (WebFetch and curl). OpenAlex and Crossref have no abstract. |
| www.sciencedirect.com/…/0022404994001421/pdfft and pdf.sciencedirectassets.com (Drápal, JPAA 105, 1995) | HTTP 403. OpenAlex has no abstract. |
| dehornoy.lmno.cnrs.fr | First attempt: connection reset through the proxy (`ws_closed_mid_exchange`). The retry succeeded (S29). |
| link.springer.com/article/10.1186/1687-1847-2012-19 and /content/pdf/… (Han–Kim–Neggers, *Fibonacci sequences in groupoids*, 2012) | HTTP 303 to the login page; the PDF URL returned HTML. |
| export.arxiv.org over http | Redirect, 0 entries; https worked. |

---

## Bottom line

**Labels to change (4):**

1. **CLM-C17-05: NOT ASSESSED → REDISCOVERY (high).** The open part is published and proved for every N.
   - [LIT] Biane's published survey (S28, §2.1, footnote 1) restricts the generator instance to q < N. It adds: "In
     Dehornoy's book it is stated that (2.2) holds for all p, q however if N is not a power of 2 this is not true",
     crediting A. Lewandowski.
   - [LIT] Aguilera–Iannella (S32, Oct 2026) attribute to Biane the statement "S_N is a Laver table if and only if
     property (2) holds for b = N as well". Their Prop. 2.5 proves that the b = N instance holds at a iff a ⋆ N = N.
   - [LIT] They cite Dehornoy, *Braids and Self-Distributivity* (2000), Lemma X.1.7: S_N is left-distributive iff
     a ⋆ N = N for every a.
   - [LIT] They also cite Prop. X.1.6: no left-distributive table with a ⋆ 1 = a + 1 mod N exists unless N is a power of 2.
   - Together these give the lab's statement for every N, not only N ≤ 4096.
   - The verification can become PROVEN (by the literature) once the Skeptic has checked the chain in § "The CLM-C17-05 question".
2. **CLM-C14-07: POTENTIALLY NOVEL → PARTIAL REDISCOVERY (high for (b) and (c)).**
   - Oh–Yoo–Yun (S12, SIAM J. Discrete Math. 2013) study the 2n-vertex graph G̃. It is exactly K₂ ⊕ G.
   - They prove that G ↦ G̃ is well defined on switching classes and injective (Thm 1.1, Prop. 3.3). That is (b) for
     a = 1, and (c).
   - (b) for a ≥ 2 follows because K_{a,a} ≅ K₂ ⊕ aK₁ [DERIVED].
   - Only (a), the (order, imbalance) multiplicativity, remains, and it is elementary.
3. **CLM-C11-04: POTENTIALLY NOVEL → PARTIAL REDISCOVERY.**
   - T_011 is Capocelli's code C(3) (IEEE Trans. IT, 1989): all binary words in which 011 occurs only as a suffix
     (S1, §I and Table II). It is also a case of Lakshmanan's (1981) pattern codes L(π) (S2, §2.1 and §3).
   - Lima–da Rocha tabulate C(3) against the Fibonacci code (S1, Table I) at n = 2^t. C(3) is longer at n = 1, 2, 4,
     equal at 8, 16, 32, and one bit shorter at every tabulated n = 2^t with 6 ≤ t ≤ 26.
   - So the code and the phenomenon are known (high confidence). The exact statement of the claim was not found
     (medium confidence: Capocelli 1989 was not read).
4. **CLM-C11-09: POTENTIALLY NOVEL → PARTIAL REDISCOVERY (medium).**
   - Already known [LIT S2]: "C3 ≤ C1 for n > 1" (Fraenkel–Klein, proof of Prop. 6) and the count 2F_{r−2}
     (their Prop. 5).
   - Not found: the comparison of C3 with T_011 (= Capocelli's C(3)). Fraenkel–Klein do not cite Capocelli, and
     Lima–da Rocha do not include C3.

**Survive, but the novelty basis must be corrected:**
- **CLM-C11-07** (low): the two codes compared are Apostolico–Fraenkel's C^(k) and Lakshmanan/Capocelli pattern codes.
- **CLM-C15-04, -07, -15** (low): the measure is essentially the one-way communication complexity of the t-step rule
  (Dürr–Rapaport–Theyssier 2004, S14). That paper classifies the elementary CAs experimentally into
  bounded / linear / other. It proves linear complexity together with an explicit description of f^n for rule 132.
  Only the fuse instance and the order-3 census are new.
- **CLM-C13-02, -03, -11** (low): spectra of single laws via linear models over ℤ/n are an active topic in the
  unanchored setting (Equational Theories Project, S9–S10). Anchored spectra are not treated there.
- **CLM-C14-13** (conjecture; low): its K₂-cancellation is Oh–Yoo–Yun's theorem.
- **CLM-C20-02** (low): the most relevant paper could not be read. aab → babaa is a confluent one-rule system
  (aab is unbordered), and that is exactly the class whose "termination and derivational complexity"
  Kobayashi–Katsura–Shikishima-Tsuji treat (TCS 262, 2001).

**Survive with raised confidence:**
- **CLM-C16-05 and CLM-C16-07.** Klimov (S16, 2026) studies the same objects: finite "UFS-groupoids" with periodic
  universal Fibonacci sequence are exactly the lab's full-period tables (his Thm 4.2: de Bruijn B(n,2)).
  - He poses as open (Problems 7.3–7.5) whether any UFS-groupoid can be left-cancellative, a left quasigroup or a quasigroup.
  - CLM-C16-07 answers this in the positive for finite orders. [COMPUTED] The lab's order-5 cycle gives a Latin
    square whose pair map is a single 25-cycle.
  - The distance-2 characterisation (C16-05) is not in Klimov.
  - Recommend citing Klimov, and (a human decision) informing the author.

**Survive unchanged:**
- CLM-C12-04 (medium);
- CLM-C13-04 (medium; small);
- CLM-C14-04 and -05 (low; plausibly folklore);
- CLM-C14-10 (low; routine enumeration);
- CLM-C16-09 (low–medium);
- CLM-C16-15 (a two-line corollary of Laver's monotonicity, not worth a novelty claim);
- CLM-C19-02, -03 (medium), -05, -06 (conjectures), -14 (small).
  For the C19 claims, all arXiv Zeckendorf-game papers up to 2026-10-07 were checked; none treats L(F_k), lazy
  representations or a recursion for L(n).

---

## Verdicts

Relation means what the closest prior work does to the claim:
- *same*: it states the claim;
- *implies*: the claim follows from it;
- *partly*: part of the claim is in it;
- *method only*: the method is standard but this instance is not stated;
- *none found*: nothing related was found.

| Claim | Recommended novelty | Closest prior work | Relation | Confidence | Proposed novelty_basis (paste-ready) |
|---|---|---|---|---|---|
| CLM-C11-04 | **PARTIAL REDISCOVERY** | R. M. Capocelli, IEEE Trans. IT 35 (1989) 191–193 (code C(3) = words with 011 only as suffix), as described and tabulated in Lima–da Rocha 2013, https://jcis.sbrt.org.br/jcis/article/download/17/11/127 (§I, Tables I–II); Lakshmanan, IEEE Trans. IT 27 (1981) and Fraenkel–Klein 1996 §2.1/§3, https://u.cs.biu.ac.il/~tomi/Postscripts/robust.pdf | code: same; comparison: partly (numerical table) | high (code); medium (exact comparison; Capocelli 1989 unread) | "T_011 is Capocelli's code C(3) (all words in which 011 occurs only as a suffix; IEEE Trans. IT 35 (1989) 191–193, as attributed by Lima–da Rocha, JCIS 2013). T_p in general is the pattern code L(p): Lakshmanan, IEEE Trans. IT 27 (1981), in Fraenkel–Klein's version with p itself adjoined (DAM 64 (1996), §2.1 and §3); Berstel–Perrin call these semaphore codes. Lima–da Rocha (JCIS 2013, Table I) tabulate C(3) against the Fibonacci code at n = 2^t: longer at 1, 2, 4, equal at 8–32, one bit shorter for 2^6 ≤ n ≤ 2^26. The exact characterisation (one bit shorter except on the last L values of each level) was not found; Capocelli 1989 was not read." |
| CLM-C11-07 | POTENTIALLY NOVEL (low confidence) | same sources (S1 Table I compares AF(3) with C(4) at n = 2^t) | none found (objects known) | low | "Compares Apostolico–Fraenkel's code C^(k) (= T_{1^k}) with pattern codes such as Capocelli's C(k+1) (= T_{01^k}). Their lengths are tabulated (Lima–da Rocha 2013, Table I), but no analysis of the running average gain, its oscillation or the constants (2−λ)/(λ−1)², λ(2−λ)/(λ−1) was found. Capocelli 1989 and Lakshmanan 1981 were not read." |
| CLM-C11-09 | **PARTIAL REDISCOVERY** | Fraenkel–Klein 1996, Props 5–6 (S2) | partly | medium | "The count 2F_{r−2} and C3 ≤ C1 for n > 1 are Fraenkel–Klein (DAM 64 (1996), Prop. 5 and the proof of Prop. 6). The comparison of C3 with T_011 (= Capocelli's C(3), 1989), which is longer only at n = 2, 4, 8, was not found: Fraenkel–Klein do not cite Capocelli, and Lima–da Rocha (2013) do not treat C3." |
| CLM-C12-04 | POTENTIALLY NOVEL | Iannucci–Larsson, arXiv:2101.07608 (saliquot: subtract any divisor, SG = v₂ + 1), https://ar5iv.labs.arxiv.org/html/2101.07608; Codeforces 1537D (P-positions only) | none found | medium | "Not in Iannucci–Larsson (arXiv:2101.07608), whose divisor-subtraction game allows d = 1 and d = n; Codeforces 1537D and its solution give only the P-positions. OEIS has neither the Grundy sequence nor the P-position sequence (queried 2026-10-18 and again 2026-10-19). Web searches found no analysis of the Grundy values. Not a priority claim." |
| CLM-C13-02 | POTENTIALLY NOVEL (low confidence) | ETP, arXiv:2512.07087 §9, https://arxiv.org/abs/2512.07087; Le Floch's ETP notes (2025) | none found | low | "Anchored magmas impose Laver's initial condition x ⋆ 0 = x + 1 on arbitrary laws. Spectra of single magma laws are studied without anchor in the Equational Theories Project (arXiv:2512.07087 §9; B. Le Floch, 'Spectra of equational laws', 2025). No treatment of anchored models or of right-normed laws was found. Small lemma." |
| CLM-C13-03 | POTENTIALLY NOVEL (low confidence) | as above (linear models x ⋄ y = ax + by over ℤ/n) | method only | low | "Reducing laws to polynomial congruences through linear models is standard (Toyoda–Bruck; the ETP uses x ⋄ y = ax + by over ℤ/n, arXiv:2512.07087 §9). The anchored W-family theorem was not found: true spectrum = roots of a·c_W(a) − 1, and every gap-free c_W with constant term 1 occurs. The number theory of the resulting sets is classical." |
| CLM-C13-04 | POTENTIALLY NOVEL | none (the lab's own conjecture CLM-C06-10) | none found | medium | "Settles two cases of the lab's own conjecture CLM-C06-10; anchored spectra do not occur in the ETP material read (arXiv:2512.07087 §9; Le Floch 2025). Small." |
| CLM-C13-11 | POTENTIALLY NOVEL (low confidence) | Le Floch's notes §2.1 (e.g. law 546 has spectrum {k² + l²}), https://leanprover.zulipchat.com/user_uploads/3121/jrBQt8qmSzvI3w359L3p-LVR/spectrum.pdf | method only | low | "Classical arithmetic sets occur as (unanchored) spectra of single laws in the Equational Theories Project (e.g. law 546: sums of two squares; Le Floch's notes §2.1). Their realisation as affine anchored spectra was not found. The sets themselves are classical (OEIS entries quoted)." |
| CLM-C14-04 | POTENTIALLY NOVEL (low confidence) | individual identities classical; XOR case in Abiad–Butler–Haemers, https://arxiv.org/abs/1801.01149 §5 | partly | low | keep the present text, adding: "Searches on Boolean/NEPS products and Seidel spectra (2026-10-19) found no classification. Cvetković–Doob–Sachs, *Spectra of Graphs*, §2.5–2.6 not checked. Possibly folklore." |
| CLM-C14-05 | POTENTIALLY NOVEL (low confidence) | Cartesian Kronecker sum classical | partly | low | keep the present text (same addition as CLM-C14-04). |
| CLM-C14-07 | **PARTIAL REDISCOVERY** | S. Oh, H. Yoo, T. Yun, *Rainbow graphs and switching classes*, SIAM J. Discrete Math. 27 (2013) 1106–1111, https://arxiv.org/abs/1108.6143 (Thm 1.1, Prop. 3.3); see also Colbourn–Corneil, DAM 2 (1980) | same for (c) and (b) at a = 1; implies (b) | high | "(c) and (b) for a = 1 are Oh–Yoo–Yun (SIAM J. Discrete Math. 27 (2013), Thm 1.1 and Prop. 3.3). Their 2n-vertex graph G̃ is K₂ ⊕ G, and G̃ ≅ H̃ iff G and H are switching-equivalent; they note a similar map in Colbourn–Corneil 1980. (b) for a ≥ 2 follows since K_{a,a} ≅ K₂ ⊕ aK₁. Part (a), K_{a,b} ⊕ K_{c,d} = K_{ac+bd, ad+bc}, was not found (elementary)." |
| CLM-C14-10 | POTENTIALLY NOVEL (low confidence) | OEIS (no match, S35) | none found | low | keep: "OEIS searches (2026-10-18, repeated 2026-10-19) found none of the three sequences; derived sequences of a natural kind, novelty unconfirmed." |
| CLM-C14-13 | POTENTIALLY NOVEL (conjecture; low confidence) | Kronecker products of graphical Hadamard matrices (Abiad–Butler–Haemers §4–5); K₂-cancellation = Oh–Yoo–Yun 2013 | none found | low | "The product of two-graphs is the Kronecker product of the matrices S + I, as used for graphical Hadamard matrices (Abiad–Butler–Haemers, arXiv:1801.01149 §4–5). Cancellation by [K₂] is Oh–Yoo–Yun (SIAM J. Discrete Math. 2013). No unique-factorisation statement for two-graphs, or for ±1 matrices up to signed permutation similarity, was found. Lajou's unique factorisation of signed graphs concerns the Cartesian product." |
| CLM-C15-04 | POTENTIALLY NOVEL (low confidence) | Dürr–Rapaport–Theyssier, TCS 322 (2004) 355–368, https://arxiv.org/abs/cs/0210008 | method only | low | "Streaming width is essentially the one-way communication complexity of the t-step local rule used by Dürr–Rapaport–Theyssier (TCS 322 (2004); their d_n uses the central cut and the maximum over the two directions). They classify ECAs into bounded/linear/other and prove linear complexity with an explicit description of f^n for rule 132 (Lemma 10). So 'unbounded width yet easy prediction' is already exemplified there. The fuse magma and its burn-time fast-forward were not found." |
| CLM-C15-07 | POTENTIALLY NOVEL (low confidence) | as above (experimental classification of the 88 ECAs, n ≤ 12, Table 1) | method only | low | "A census in the style of Dürr–Rapaport–Theyssier's experimental classification of the 88 elementary CA (TCS 322 (2004), Table 1); the magma-automaton framework is Pedersen's (1992) and Moore's. No census of the 1734 order-3 magma automata by this measure was found." |
| CLM-C15-15 | POTENTIALLY NOVEL (low confidence) | as CLM-C15-04 | method only | low | "A benchmark of the fast-forward of CLM-C15-04; no mathematical novelty beyond it (see CLM-C15-04)." |
| CLM-C16-05 | POTENTIALLY NOVEL | P. Klimov, *Universal Fibonacci sequences and UFS-groupoids*, arXiv:2604.05754v2 (2026), https://arxiv.org/abs/2604.05754 | none found (same objects, criterion absent) | medium | "Full-period tables are Klimov's finite UFS-groupoids with periodic universal Fibonacci sequence (arXiv:2604.05754, Thm 4.2: their cycles are the de Bruijn sequences B(n,2)). Klimov characterises them through distance-1 pairs only and leaves open whether one can be a quasigroup (Problem 7.5). The distance-2 characterisation was not found. Tuscan-2 squares and recursive MDS codes are different objects. Small." |
| CLM-C16-07 | POTENTIALLY NOVEL | Klimov 2026, Problems 7.3–7.5 | none found (the question is posed as open) | medium | "Answers Problems 7.3–7.5 of P. Klimov (arXiv:2604.05754v2, 2026) positively, with finite examples. He asks whether a UFS-groupoid (finite or infinite) with more than one element can be left-cancellative, a left quasigroup or a quasigroup; the lab's order-5 cycle gives a Latin square whose pair map is one 25-cycle (Historian check). The counts 0, 0, 0, 3360 were not found. Small." |
| CLM-C16-09 | POTENTIALLY NOVEL (low confidence) | method: sign obstructions to single cycles (e.g. S. Li, arXiv:2605.09489, abstract); Klimov 2026 (no parity or isotopy results) | method only | low–medium | keep the present text and add: "Sign-of-permutation obstructions to single cycles of shift-register maps are standard (e.g. S. Li, arXiv:2605.09489, 2026). Klimov's study of UFS-groupoids (arXiv:2604.05754) contains no parity or isotopy result. The q-ary NFSR literature was not searched exhaustively for an even-alphabet obstruction." |
| CLM-C16-15 | POTENTIALLY NOVEL (low confidence; trivial corollary) | Laver's monotonicity: p ⋆ q > p for p < 2ⁿ and p ⋆ 2ⁿ = 2ⁿ (Dehornoy–Lebed, https://arxiv.org/abs/1401.2335, (1.3)–(1.4)) | implies (two lines) | medium (that it is unstated) | "No source on Fibonacci-type recurrences in Laver tables was found (Biane, SLC 80 (2019) B80c; Dehornoy's surveys; Klimov's UFS paper, arXiv:2604.05754, does not mention Laver tables). It is a two-line consequence of p ⋆ q > p (p < 2ⁿ) and p ⋆ 2ⁿ = 2ⁿ (Dehornoy–Lebed, arXiv:1401.2335, (1.3)–(1.4)). Not a substantive novelty." |
| CLM-C19-02 | POTENTIALLY NOVEL | Cusenza et al., https://arxiv.org/abs/2009.09510; Cheigh et al., https://arxiv.org/abs/2210.11038 (Type A moves, Lemma 2.2) | none found | medium | keep the present text, adding: "All arXiv Zeckendorf-game papers to 2026-10-07 checked (including the reversed, ordered and black-hole variants); none mentions lazy representations." |
| CLM-C19-03 | POTENTIALLY NOVEL | Cusenza et al. Thm 1.4 (equality only for F_k − 1); Cheigh et al. ("closed form for non-Fibonacci input open", Fibonacci case referred to Cusenza et al.) | none found | medium | keep the present text, adding: "Confirmed 2026-10-19: Cusenza et al. (arXiv:2009.09510) contain no formula for n = F_k; no later Zeckendorf-game paper treats it (arXiv to 2026-10-07); L(F_k) still not in the OEIS." |
| CLM-C19-05 | POTENTIALLY NOVEL (conjecture) | Cheigh et al. (stated as open) | none found | medium | keep the present text. |
| CLM-C19-06 | POTENTIALLY NOVEL (conjecture) | special case of CLM-C19-05 | none found | medium | keep the present text. |
| CLM-C19-14 | POTENTIALLY NOVEL | Cusenza et al. Thm 1.2 (move-by-move strategy) | none found | medium | keep the present text. |
| CLM-C20-02 | POTENTIALLY NOVEL (low confidence) | Kobayashi–Katsura–Shikishima-Tsuji, TCS 262 (2001) 583–632, doi:10.1016/S0304-3975(00)00367-4 (not read); Geser–Hofbauer–Waldmann, J. Symb. Comput. 38 (2004) (not read) | none found (decisive source unread) | low | "Termination is a rediscovery (right barren: McNaughton; Geser, ICASE 2002-33). The exact derivation length D(w) and D(n) were not found. The most relevant paper was not obtained: aab is unbordered, so aab → babaa is a confluent one-rule system, the class of Kobayashi–Katsura–Shikishima-Tsuji, 'Termination and derivational complexity of confluent one-rule string-rewriting systems', TCS 262 (2001) (ScienceDirect blocked). Geser–Hofbauer–Waldmann's derivational complexities of one-rule leftmost rewriting (JSC 38, 2004) are also unread. Small." |
| CLM-C17-05 | **REDISCOVERY** (from NOT ASSESSED) | P. Biane, Sém. Lothar. Combin. 80 (2019) B80c, §2.1 footnote 1, https://www.mat.univie.ac.at/~slc/wpapers/s80biane.pdf; Aguilera–Iannella, arXiv:2610.06106 Props 2.3–2.5, https://arxiv.org/abs/2610.06106; Dehornoy, *Braids and Self-Distributivity* (2000) Ch. X, Lemma 1.2, Prop. 1.6, Lemma 1.7 (as cited there) | same (Biane) and implies (Dehornoy + Aguilera–Iannella) | high | "Uniqueness for every N: Dehornoy, Braids and Self-Distributivity (2000), Lemma X.1.2; Biane, SLC 80 (2019) B80c §2.1. Non-existence of a model of the full instance for N not a power of 2: Biane's footnote 1 ('(2.2) for all p, q … if N is not a power of 2 this is not true', credited to A. Lewandowski); Aguilera–Iannella (arXiv:2610.06106) state it as Biane's observation. It follows from their Prop. 2.5 (the instance at (a, N) holds iff a ⋆ N = N) together with Dehornoy's Lemma X.1.7 (the table is left-distributive iff a ⋆ N = N for all a) and Prop. X.1.6. So the statement holds for every N." |

---

## The CLM-C17-05 question

Translation. The lab works 0-based: x ⋆ 0 = x + 1, x ⋆ (y + 1) = (x ⋆ y) ⋆ (x + 1). The surveys work 1-based with
p = x + 1: p ⋆ 1 = p + 1 mod N and p ⋆ (q ⋆ 1) = (p ⋆ q) ⋆ (p ⋆ 1). The lab's wrap-around instance y = N − 1 is the
surveys' instance q = N: p + 1 = (p ⋆ N) ⋆ (p + 1). Write S_N for the unique table defined by the recursion with
q < N (Aguilera–Iannella's notation).

**1. What the literature states, and in what form.**

- **Uniqueness for every N.** [LIT]
  - Biane (S28 §2.1) proves it by descending induction on p and ascending induction on q, with N ≥ p ⋆ q > p. This is
    the lab's argument.
  - Aguilera–Iannella (S32, eqs. (1)–(2)) state it with b < N and cite Dehornoy (2000), Lemma X.1.2.
  - The lab's written proof (C17 Observation 4) is a rediscovery of this.
- **Left-distributive iff N is a power of 2.**
  - [LIT] Biane §2.2: "the binary operation defined above is left distributive if and only if N = 2ⁿ". The proof is
    referred to Dehornoy's books and Drápal's survey.
  - [LIT] Dehornoy 2014 survey (S29), Thm 1.1(i), and Dehornoy 2018 (S30), Ex. 1.17.
  - [LIT] Aguilera–Iannella Prop. 2.3(ii), citing [Deh00, Prop. 1.6]: for N not a power of 2 there is no
    left-distributive algebra with a ⋆ 1 = a + 1, N ⋆ 1 = 1.
- **The last-column criterion.** [LIT] Aguilera–Iannella Prop. 2.4, citing [Deh00, Lemma 1.7]: "The algebra S_N is
  left distributive if and only if the equality a ⋆ N = N is true for every a ≤ N."
- **The wrap-around instance is exactly the last column.** [LIT] Aguilera–Iannella Prop. 2.5, proof read: for
  a < N, a ⋆ N = N iff (2) holds for a and b = N.
  - [DERIVED independently before I found S32] If a ⋆ N = v < N, then v > a and v ⋆ (a + 1) > v ≥ a + 1, so the
    instance fails.
  - [COMPUTED] No exception for N ≤ 128 (`laver_wraparound.py`).
- **The lab's statement itself.** [LIT]
  - Biane's footnote 1 (S28): "In Dehornoy's book [1] it is stated that (2.2) holds for all p, q however if N is not a
    power of 2 this is not true. I would like to thank Arkadiusz Lewandowski for pointing this out to me."
  - Aguilera–Iannella (S32, §2.2): "Another interesting observation, due to Biane [Bia21], is that the algebra S_N is a
    Laver table if and only if property (2) holds for b = N as well."

**2. A slip that may have misled the lab.** Several texts state the generator instance "for all p, q" and claim
existence and uniqueness for every N:
- Biane's arXiv v1 (S27 §2.1), which the lab cites in C06 (README Step 8 and the CLM-C06-01 basis);
- Dehornoy's 2014 survey (S29, Thm 1.1(i));
- Dehornoy's 2018 survey (S30, Ex. 1.17), which also omits the initial condition;
- by Biane's footnote, Dehornoy's 2000 book.

Read literally this is false already at N = 3. [COMPUTED] A brute force over all 3⁶ tables with the anchor finds
none satisfying (1.1) and (1.2) for all p, q; S_3 has rows (2,3,2), (3,3,3), (1,2,3) and 1 ⋆ 3 = 2 ≠ 3. The lab's
C17 correction of its own C06 paraphrase is the same correction Biane made in the published version.

**3. Does it imply the lab's open statement? Yes, for every N.**
- Let S_N satisfy the full instance.
- By Prop. 2.5, a ⋆ N = N for all a. (N ⋆ N = N because row N is the identity.)
- By Dehornoy's Lemma X.1.7, S_N is left-distributive.
- By Prop. X.1.6, N is a power of 2.
- Conversely, A_n is left-distributive, so it satisfies every instance (Dehornoy–Lebed S31, Thm 1.1(i) and (1.3)).

The LD theorem alone would not suffice, because the full instance is weaker than LD. The bridge is the
"last column / period" result: a ⋆ N = N, equivalently the period of every row divides N.

I read Lemma X.1.7 and Prop. X.1.6 only as stated and cited by Aguilera–Iannella, not in the book. A human expert
should confirm them there (Note 3).

**4. An independent argument through row periods.** [DERIVED; checked numerically] This uses only Laver's periodicity
theorem, which I read in S29 Thm 1.1(ii) and S31 Thm 1.1(ii). It essentially repeats the corner-embedding argument of
Aguilera–Iannella's Thm 4.2 and Lemma 4.6.

Setup: let N not be a power of 2, k = v₂(N), s = N − 2^{k+1} ≥ 1 (since N = 2^k m with m ≥ 3 odd).

- (i) Rows s + 1, …, N − 1 of S_N are shifted copies of rows 1, …, 2^{k+1} − 1 of the Laver table A_{k+1}:
  v ⋆_N c = s + ((v − s) ⋆_{k+1} c*), where c* ≡ c (mod 2^k).
  - Proof: descending induction on v and ascending induction on c.
  - It uses that the periods of these rows of A_{k+1} are powers of 2 below 2^{k+1}, hence divide 2^k, and that s ≡ 0 (mod 2^k).
- (ii) Hence row s of S_N is s + 1, s + 2, …, N, so its period is 2^{k+1}. This does not divide N, so s ⋆ N ≠ N and
  the wrap-around instance fails at p = s (0-based x = s − 1).
- [COMPUTED] `laver_top_block.py`: (i) and (ii) hold for all 1,013 non-powers of 2 with N ≤ 1024 and 15 further N up to
  4095, including N = 3·2^10 and 15·2^8.
- [COMPUTED] `laver_first_failing_row.py`: for N ≤ 300, row s is always the topmost failing row.

**5. Recommendations for the record (CLM-C17-05).**
- novelty → REDISCOVERY, with the basis in the table above.
- verification → PROVEN (by the literature), after the Skeptic has checked §3. The lab's computations to N = 4096
  agree.
- Note for the claim's corollary: by Lemma X.1.7, once the instances y ≤ N − 2 have forced S_N, left-distributivity
  of an anchored table is decided by its last column alone.
- Update the citations in C06 and C17: replace Biane's arXiv v1 by the published SLC version, and add
  Aguilera–Iannella 2026.

---

## Notes

1. **Check first: the integer-code sources (C11).**
   - Capocelli 1989 (IEEE Trans. IT 35:191–193, doi:10.1109/18.42193; IEEE Xplore blocked here).
   - Capocelli, *Flag encodings related to the Zeckendorf representation of integers*, in *Sequences: Combinatorics,
     Compression, Security and Transmission* (Springer 1990), 449–466. Cited in S1 and S5; not read.
   - Lakshmanan, IEEE Trans. IT 27 (1981) 659–662, which according to S2 gives recurrences for the codeword counts of
     every L(π) and characterises universality.
   - These probably contain the counts behind CLM-C11-03/04 for u = 01^k, and perhaps the comparison with
     Apostolico–Fraenkel. If Capocelli states the comparison, CLM-C11-04 becomes a full REDISCOVERY.
2. **CLM-C20-02:** Kobayashi–Katsura–Shikishima-Tsuji, TCS 262 (2001) (Elsevier open archive; blocked here). The
   earlier Historian report also could not read it. It is decisive for C20-02 and for CLM-C04-09/-12.
3. **CLM-C17-05:** Dehornoy, *Braids and Self-Distributivity* (2000), Ch. X, Lemma 1.2, Prop. 1.6, Lemma 1.7. Confirm
   the statements cited by Aguilera–Iannella, and see whether the book itself already proves "a ⋆ N = N ∀a ⇒ N = 2ⁿ".
   Drápal, *Persistence of cyclic left distributive algebras* (JPAA 105, 1995; blocked) is also likely relevant.
4. **Klimov 2026 (S16).**
   - The lab's C16 results (full-period quasigroups of orders 5–16, the distance-2 criterion, the even-order isotope
     obstruction) answer or extend his Problems 7.3–7.5.
   - His Thm 4.6 also counts all finite UFS-groupoids, (n!)ⁿ(1 + n²(n − 1))/n². Its periodic part is CLM-C16-03,
     already a rediscovery.
   - The lab and Klimov use the same recurrence up to transposing the table, which preserves the quasigroup property.
   - Whether to contact the author is a human decision.
5. **Graph products:** Cvetković–Doob–Sachs, *Spectra of Graphs* (1980), §2.5–2.6 (Boolean operations, NEPS), and
   Cvetković's 1975 paper in Publ. Inst. Math. (Beograd) should be checked for a classification like
   CLM-C14-04/05. My searches found none, but I could not read either.
6. **Records outside the 26 that the sources found here affect.**
   - CLM-C11-01 … 03 are already REDISCOVERY, but their bases omit:
     - Lakshmanan 1981;
     - Fraenkel–Klein 1996 §3: Thm 1, L(π) is complete for every π; Thm 2, for unbordered π the comma-free and
       prefix versions coincide;
     - Berstel–Perrin's semaphore codes.
   - Biane's published footnote and Aguilera–Iannella should be added to CLM-C06-01. That record is still
     COMPUTATIONALLY SUPPORTED, although its statement is the published theorem: Laver; Dehornoy 2000, Prop. X.1.6, as
     cited in S32.
   - The refutations of H-C15-1 and H-C15-4 (C15 README Step 1) are already exemplified in Dürr–Rapaport–Theyssier:
     linear-complexity ECAs with an explicit f^n (rules 132 and 23, S14 §6), and a 3-state CA of complexity Θ(n²)
     (S14 §7, Lemma 11).
7. **Attribution in the task text:** arXiv:1810.00548 is by Philippe Biane, not by Lebed. Lebed's Laver-table work in
   this area is Dehornoy–Lebed, arXiv:1401.2335 (S31), and Lebed's cohomology paper arXiv:1503.07030 (seen in a
   listing, not read).
8. **Bibliographic details to check before any record cites them.**
   - The JCIS header prints "Vol. 1, No. 28"; this is presumably Vol. 28, No. 1.
   - The Le Floch notes I read are dated July 14, 2025; the lab cites a July 10, 2025 version.
   - Every DOI and venue above comes from Crossref, except arXiv-only items.
