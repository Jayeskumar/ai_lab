# Historian and Novelty Review: cycles C03, C04, C06, C08, C09, C10

*Reviewer:* Historian and Novelty Analyst · *Date:* 2026-10-18 · *Scope:* the 60 claims
CLM-C03-01 … 11, CLM-C04-01 … 16, CLM-C06-01 … 12, CLM-C08-01 … 06, CLM-C09-01 … 08,
CLM-C10-01 … 07.

*Inputs read:* the claim records in `db/claims/`; `research/cycles/C03_*`, `C04_*`, `C06_*`,
`C08_*`, `C09_*`, `C10_*` (README.md, record.yaml); `proofs/paper/C03.md` … `C10.md`; textbook
chapters `04_termination`, `05_derivations`, `07_anchored`, `09_circle_products`,
`10_circle_primes`, `11_cost_of_counting`; for cross-checks `results/EXP-C03-02/03/04`,
`EXP-C08-02/04`; the Skeptic's review `reviews/skeptic_C03_C04_C06.md` and the C20 README (read
after the coordinator's update).

*Method:* web search (several phrasings per claim), full texts read for every source that decided
a label (listed in §8), OEIS through `lab.oeis` (new answers cached in `cache/oeis`), and
independent computations in `reviews/historian_checks/` (§9).

*Rules followed:* only this file and the scripts in `reviews/historian_checks/` were written
(plus the OEIS cache entries created by `lab.oeis`). No `lab sync/lean/book`. All computations ran
under `nice -n 10` (longest ≈ 70 s). **Disclosure:** early in the session I ran one read-only
`git log --oneline | head -5` before noticing the "no git" rule; it changed nothing.

**Labels** (as in `historian_C01_C02.md`):
- **REDISCOVERY:** the statement is in the cited literature, or follows from it by literally the
  same argument (said explicitly where so).
- **PARTIAL REDISCOVERY:** part of the claim is published, or the claim is a few-line corollary of a
  published result; the unpublished residue is named.
- **POTENTIALLY NOVEL:** nothing equivalent found in the sources searched. Never a priority claim.
- **NOT ASSESSED:** could not be evaluated.

Tags: **[LIT]** stated in a cited source (page/number given); **[DERIVED]** my own deduction from
cited results — short, unrefereed, for the Skeptic to check; **[COMPUTED]** my own computation (§9).

---

## 0. Executive summary

1. **The Zantema–Geser theorem has been obtained and C03's divisibility conjecture is literally it.**
   - Full text found: H. Zantema and A. Geser, *A complete characterization of termination of
     0^p 1^q → 1^r 0^s*, Utrecht tech. report UU-CS-1994-44 (scanned, 19 pp.),
     https://ics-archive.science.uu.nl/research/techreps/repo/CS-1994/1994-44.pdf
     (sha256 `588f84b6…f1a6`). The journal version's statement was read on its page-2 preview,
     https://page-one.springer.com/pdf/preview/10.1007/s002009900019 (AAECC 11 (2000) 1–25,
     https://doi.org/10.1007/s002009900019). Verbatim texts in §2.0.
   - The report's p. 2 lists the non-terminating cases as "2p ≤ s, 2q ≤ r, or p < s < 2p, q < r,
     q|r, or q < r < 2q, p < s, p|s": **exactly the cases (a), (b), (c) of CLM-C03-10 / Conjecture
     4.6.** [DERIVED] equivalence written out in §2.0, [COMPUTED] identical on all 40⁴ parameter
     quadruples ≤ 40.
   - Consequences: CLM-C03-10 is PROVEN by the literature (REDISCOVERY); the 24 rules "open here"
     all terminate; **CLM-C03-09 (H-C03-3) is refuted** by the published theorem
     (e.g. 0011 → 11100000 terminates; 8 counterexamples with parameters ≤ 5); the doubling loop of
     CLM-C03-03 is ZG Lemma 4.1 verbatim; loops for all divisible cases (which the lab had only for
     q ≤ 6) are ZG Lemma 4.3, whose proof uses the lab's lifting idea ("we may assume q = 1").
2. **C08: the measured associativity thresholds are partly wrong; the theory is largely published.**
   - A. Messaoudi, Math. Slovaca 50 (2000) 135–148 (read in full) already has the window
     criterion (∘ associative ⇔ the conjugate image set is stable under multiplication, Thm 3/Cor 1),
     s_m = 2 for Fibonacci, Pell-type thresholds (Thm 1, Cor 2–3, Thm 4–6), "s < d ⇒ not
     associative" (Prop 1) and associativity of tribonacci for large s.
   - **Tribonacci ∘₃ is not associative.** Arnoux's conjecture (∘₃ associative) was refuted by
     Ambrož–Frougny–Masáková–Pelantová (2003). [COMPUTED with the lab's own `systems/circle.py`]
     (10016 ∘₃ 10016) ∘₃ 1 = 3414681926 ≠ 3414681924 = 10016 ∘₃ (10016 ∘₃ 1). The lab's threshold "3"
     (CLM-C08-05, README, textbook) is wrong; the lab's random tests up to 10⁶ missed this failure.
   - [COMPUTED] Also wrong: G(k+1) = G(k) + G(k−2) "from s = 10" ((78 ∘ 248) ∘ 1 differs at s = 10),
     and two of the ten "non-monotone" sequences behind CLM-C08-04 ((4,3; 1,5) at s = 4 and
     (3,3; 1,2) at s = 7 are not associative).
   - [DERIVED] For canonical base sequences (Messaoudi's G/H classes) the associative shifts are
     always upward-closed, whatever the sign of the conjugate; CLM-C08-04 is substantive only for non-canonical initial
     values (all eight surviving examples are non-canonical).
3. **C04-06 (constant-step potential) is a rediscovery in substance:** M. Latteux and Y. Roos,
   RAIRO-ITA 48 (2014) 149–171, Lemma 3.7: in a length-preserving one-rule system all derivations
   between two words have the same length, proved with a scattered-subword invariant going back to
   Métivier (1985), Lemma 3.5. The "confluent ⇔ random descent" corollary is two lines.
4. **C04-03 (now settled in C20) — classification confirmed.** Both rules are right barren
   [COMPUTED]; McNaughton's theorem (non-overlapping + barren ⇒ terminating) applies; Geser's ICASE
   2002-33 Thm 3.2–3.3 is the accessible statement. They are also inside the class a^p b^q → t whose
   termination Kobayashi–Katsura–Shikishima-Tsuji (TCS 2001) characterise. **Side remark:** the
   ICASE report's introduction lists "terminating one-rule SRSs with one overlap pair have linear
   derivation lengths" as a contribution, but aab → ababa has one overlap pair (OVL(r,l) = {a},
   OVL(l,r) = {ab}) and exponential complexity 2^(n−2) − 1; the report proves linearity only in its
   non-barren case (p. 10), as C20 says.
5. **CLM-C04-10 answers an open OEIS question.** Kimberling asked in A083706 (2014) whether
   A247983(n+1) = A247983(n) iff n ∈ A083706. The lab's formula gives "yes" for n ≥ 1
   ([DERIVED], [COMPUTED]). POTENTIALLY NOVEL (small); worth an OEIS submission.
   CLM-C04-09 stays POTENTIALLY NOVEL with **low** confidence: Kobayashi et al. (TCS 262, 2001)
   announce "a complete analysis of the derivational complexity of a^p b^q → b^n a^m", a family
   containing aab → ba; I could not read that paper.
6. **C10 missed the central reference:** V. Berthé, C. Frougny, M. Rigo, J. Sakarovitch, *The carry
   propagation of the successor function*, Adv. Appl. Math. 120 (2020) 102062 (base p: p/(p−1);
   rational base, AFS normalisation: p/(p−q)). Their measure (length of the changed suffix) gives
   φ² ≈ 2.618 for Zeckendorf, the lab's Hamming measure gives 2 [COMPUTED]. CLM-C10-02's closed form
   is in OEIS A215005 (Kotesovec 2012) and is the potential-function identity Σ_{n<N} = 2N − s_Z(N).
7. **C06:** no literature on successor-anchored magmas was found beyond Laver tables; the odd and
   golden laws stay POTENTIALLY NOVEL (small). But CLM-C06-08 is a two-line consequence of
   "left-permutable + right identity ⇒ commutative monoid" (PARTIAL REDISCOVERY, downgrade), the
   unique model of CLM-C06-03 is the classical cyclic rack, and CLM-C06-12 is the anchored version
   of the product closure of variety spectra (Grätzer; Froemke–Quackenbush 1975).
8. **C09:** the window obstruction and density 1/φ² remain POTENTIALLY NOVEL (small). The product
   formula a ∘ b = ab + ab* + a*b is equivalent to Lunnon's formula in OEIS A101330 (2008).

## 1. Summary table

| Claim | Current label | Recommended | Conf. | Closest prior work |
|---|---|---|---|---|
| C03-01 | REDISCOVERY | REDISCOVERY | high | ZG 1994 Prop 3.1–3.2 |
| C03-02 | REDISCOVERY | REDISCOVERY | high | ZG 1994 Prop 3.1 (p ≥ s or q ≥ r simply terminating), Prop 3.3 |
| C03-03 | REDISCOVERY | REDISCOVERY (same two-step loop) | high | ZG 1994 Lemma 4.1 |
| C03-04 | REDISCOVERY | REDISCOVERY | high | ZG Thm 1.1, Lemma 4.3 |
| C03-05 | REDISCOVERY | REDISCOVERY | high | morphism closure (folklore); ZG Lemma 4.3 proof, §3.1 |
| C03-06 | REDISCOVERY | REDISCOVERY; **all 625 classified** (24 open ones terminate) | high | ZG Thm 1.1 |
| C03-07 (refuted) | NOT ASSESSED | REDISCOVERY | high | Geser 1993; ZG Thm 1.1 |
| C03-08 (refuted) | NOT ASSESSED | REDISCOVERY (40 counterexamples ≤ 5, not 35) | high | ZG Thm 1.1, Lemma 4.3 |
| C03-09 (inconclusive) | NOT ASSESSED | **REFUTED by ZG Thm 1.1**; REDISCOVERY | high | ZG Thm 1.1 (case 4) |
| C03-10 | REDISCOVERY (unverified) | **REDISCOVERY, verbatim; status PROVEN (literature)** | high | ZG 1994 Thm 1.1 and p. 2; AAECC 2000 Thm 1 |
| C03-11 | NOT ASSESSED | PARTIAL REDISCOVERY (fix author list) | medium | Geser, RTA 2002, Thm 1 (same closed form) |
| C04-01 | NOT ASSESSED | REDISCOVERY in substance | med-high | Kurth 1990 criteria A, D; McNaughton; ZG; GWW 2016 |
| C04-02 (refuted) | NOT ASSESSED | REDISCOVERY | high | ZG Lemma 4.1 (ab → bbaa); Kurth 1996 |
| C04-03 | NOT ASSESSED (now PROVEN in C20) | REDISCOVERY (termination) | high | McNaughton 1995/2001; Geser ICASE 2002-33 Thm 3.2–3.3; KKS 2001; Sénizergues 1996 |
| C04-04 | REDISCOVERY | REDISCOVERY (refs OK) | high | Bertrand 1994; RTA LooP #20; ZG Prop 3.3 |
| C04-05 | REDISCOVERY | REDISCOVERY (refs OK) | high | van Oostrom 2007 |
| C04-06 | NOT ASSESSED | **REDISCOVERY in substance** | med-high | Latteux–Roos 2014 Lemma 3.7; Métivier 1985 Lemma 3.5; Adinayev–Stein 2019 |
| C04-07 (refuted) | NOT ASSESSED | REDISCOVERY (one line from van Oostrom) | high | van Oostrom 2007 |
| C04-08 | REDISCOVERY | REDISCOVERY (folklore) | high | — |
| C04-09 | POTENTIALLY NOVEL | POTENTIALLY NOVEL | **low** | ZG Prop 3.2 (only O(n)); KKS 2001 (unread) |
| C04-10 | POTENTIALLY NOVEL | POTENTIALLY NOVEL (answers Kimberling's OEIS question; n ≥ 1) | medium | OEIS A247983, A083706 |
| C04-11 (refuted) | NOT ASSESSED | POTENTIALLY NOVEL (as C04-09) | low | as C04-09 |
| C04-12 | NOT ASSESSED | PARTIAL REDISCOVERY | medium | ZG 1994 §3; Bertrand 1994; KKS 2001 (unread) |
| C04-13 | REDISCOVERY | REDISCOVERY | high | Winning Ways; Guy–Smith 1956 |
| C04-14 (refuted) | NOT ASSESSED | REDISCOVERY | high | Dawson's Kayles values (A002187 shifted) |
| C04-15 | REDISCOVERY | REDISCOVERY (preperiod 53 exact) | high | Guy–Smith 1956 |
| C04-16 | REDISCOVERY | REDISCOVERY (open problems) | high | Grossman 2019; Flammenkamp table |
| C06-01 | REDISCOVERY | REDISCOVERY | high | Laver; Drápal; Dehornoy |
| C06-02 | REDISCOVERY | REDISCOVERY (folklore) | high | — |
| C06-03 | NOT ASSESSED | PARTIAL REDISCOVERY | medium | cyclic rack (Fenn–Rourke 1992; Lopes–Roseman Ex. 2.3) |
| C06-04 (refuted) | NOT ASSESSED | POTENTIALLY NOVEL (data) | low-med | — |
| C06-05 | NOT ASSESSED | PARTIAL REDISCOVERY (folklore-level) | medium | centraliser of an N-cycle; OEIS A000169 |
| C06-06 | POTENTIALLY NOVEL | POTENTIALLY NOVEL (small) | med-low | — |
| C06-07 | POTENTIALLY NOVEL | POTENTIALLY NOVEL (small) | med-low | A089270 (W. Lang's proof), A087781 |
| C06-08 | POTENTIALLY NOVEL | **PARTIAL REDISCOVERY** (downgrade) | medium | left-permutable + right identity lemma; Dudek–Gigoń 2013 (AG version); A058156 |
| C06-09 (refuted) | NOT ASSESSED | POTENTIALLY NOVEL (data) | low | — |
| C06-10 | NOT ASSESSED | POTENTIALLY NOVEL (conjecture) | low | — |
| C06-11 | NOT ASSESSED | POTENTIALLY NOVEL (data) | low | — |
| C06-12 | NOT ASSESSED | REDISCOVERY in substance | med-high | Grätzer; Froemke–Quackenbush 1975 |
| C08-01 | REDISCOVERY | REDISCOVERY (add Messaoudi 2000) | high | Knuth 1988; Arnoux 1989; Messaoudi 2000 Thm 6, Prop 1 |
| C08-02 | NOT ASSESSED | POTENTIALLY NOVEL (conjecture) | low | Messaoudi Cor 1 (tool); Frougny–Solomyak 1992 |
| C08-03 | REDISCOVERY | REDISCOVERY, **title overstated** | high | GPTW 1994 (non-increasing coefficients, canonical initial values) |
| C08-04 | POTENTIALLY NOVEL | POTENTIALLY NOVEL (low); **2 of 10 examples are artefacts** | low | Messaoudi 2000 Thm 2 [DERIVED monotonicity] |
| C08-05 | NOT ASSESSED | PARTIAL REDISCOVERY; **two thresholds wrong** | high (errors) | Messaoudi 2000/2002; AFMP 2003 |
| C08-06 (refuted) | NOT ASSESSED | REDISCOVERY | high | GPTW 1994; Messaoudi 2000 |
| C09-01 | REDISCOVERY | REDISCOVERY (+ Lunnon formula, A101330) | high | Arnoux 1989; A101330 |
| C09-02 (refuted) | NOT ASSESSED | REDISCOVERY (trivial from F_j ∘ F_k = F_{j+k}) | high | Knuth 1988 |
| C09-03 | POTENTIALLY NOVEL | POTENTIALLY NOVEL (small) | med-low | Arnoux 1989 (window) |
| C09-04 (refuted) | NOT ASSESSED | as C09-03 | med-low | — |
| C09-05 | NOT ASSESSED | POTENTIALLY NOVEL (conjecture) | low | — |
| C09-06 | NOT ASSESSED | POTENTIALLY NOVEL (minor corollary) | med-low | — |
| C09-07 | NOT ASSESSED | REDISCOVERY in substance | high | norm of ℚ(√5) + Arnoux embedding |
| C09-08 | NOT ASSESSED | POTENTIALLY NOVEL (data; not in OEIS) | medium | — |
| C10-01 | REDISCOVERY | REDISCOVERY (add BFRS 2020) | high | BFRS 2020; Cormen et al. ch. 17 |
| C10-02 | REDISCOVERY | REDISCOVERY in substance (state the measure) | high | OEIS A215005 (Kotesovec); potential method |
| C10-03 (refuted) | NOT ASSESSED | REDISCOVERY | high | as C10-02; BFRS (φ² with their measure) |
| C10-04 | NOT ASSESSED | REDISCOVERY in substance | med-high | token conservation; b-ary counter |
| C10-05 | NOT ASSESSED | PARTIAL REDISCOVERY | medium | BFRS Thm 3.23 (p/(p−q), AFS normalisation) |
| C10-06 | NOT ASSESSED | POTENTIALLY NOVEL (conjecture) | low | BFRS §5 (ergodic method) |
| C10-07 | REDISCOVERY | REDISCOVERY (refs OK) | high | Myers 1983; Okasaki 1995 |

---

## 2. Cycle C03

### 2.0 The Zantema–Geser theorem: verbatim statement and comparison (priority item)

**Sources (all accessible on 2026-10-18).**
- Tech. report: H. Zantema and A. Geser, UU-CS-1994-44, Utrecht University,
  https://ics-archive.science.uu.nl/research/techreps/repo/CS-1994/1994-44.pdf (HTTP 200,
  769,838 bytes, sha256 `588f84b68510ad9114736e9935d7c2f9b046e113c766c5e58e5a99f6fe51f1a6`;
  a scan, no text layer — read from rendered page images). The lab's failures were at
  `dspace.library.uu.nl` and `research-portal.uu.nl`; this older archive host works.
- RTA'95, LNCS 914, 41–55, https://doi.org/10.1007/3-540-59200-8_46; first two pages at
  https://page-one.springer.com/pdf/preview/10.1007/3-540-59200-8_46.
- AAECC 11 (2000) 1–25, https://doi.org/10.1007/s002009900019; first two pages at
  https://page-one.springer.com/pdf/preview/10.1007/s002009900019.

**Verbatim, tech report p. 1:**
> **Theorem 1.1** Let p, q, r, s denote positive integer numbers. Then the system
> 0^p 1^q → 1^r 0^s terminates if, and only if
> 1. p ≥ s, or
> 2. q ≥ r, or
> 3. p < s < 2p and q ∤ r, or
> 4. q < r < 2q and p ∤ s.

**Verbatim, tech report p. 2:** "Here x|y means that x is a divisor of y. We show that this class
contains 1. simply terminating systems (cases 1 and 2) of (a) linear (p > s or q > r),
(b) quadratic (p = s, q = r), and (c) exponential derivation lengths (p = s, q < r, or p < s, q = r),
2. **non-terminating systems (2p ≤ s, 2q ≤ r, or p < s < 2p, q < r, q|r, or q < r < 2q, p < s,
p|s)**, and 3. non-simply terminating systems (cases 3 and 4)."

**Verbatim, AAECC 2000 p. 2:**
> **Theorem 1 [36].** Let p, q, r, s denote positive integer numbers. Then the one-rule string
> rewriting system 0^p 1^q → 1^r 0^s terminates if, and only if,
> 1. p ≥ s or q ≥ r, or
> 2. p < s < 2p and q < r and q ∤ r or q < r < 2q and p < s and p ∤ s.
>
> Here x|y denotes that x is a divisor of y. In Case (1), termination can be proven by a division
> order [15], a fact that is also called simple termination [19]. In Case (2), self-embedding
> derivations exist and so termination is non-simple.

Caution: the PDF text layer of the 2000 preview renders "∤" as "|"; the rendered page shows ∤.
Only ∤ is consistent with the paper's motivating example 0011 → 111000 being terminating.

**Comparison with CLM-C03-10 / Conjecture 4.6 / textbook Conjecture 4.6. [DERIVED]**
- ZG's non-terminating set is p < s, q < r, (s ≥ 2p or q | r) and (r ≥ 2q or p | s).
- Split by the two "doubling" inequalities:
  - s ≥ 2p, r ≥ 2q: non-terminating — case (a);
  - s ≥ 2p, r < 2q: needs p | s — case (b) (q < r < 2q);
  - s < 2p, r ≥ 2q: needs q | r — case (c) (p < s < 2p);
  - s < 2p, r < 2q: needs q | r with q < r < 2q, impossible — terminating, as Conjecture 4.6 says.
- So Conjecture 4.6 **is** ZG Theorem 1.1. It even matches ZG's own three-case list on p. 2
  word for word.
- [COMPUTED] (`c03_zg_compare.py`) identical on all 1 ≤ p, q, r, s ≤ 40. All 596 decided statuses of
  EXP-C03-02 (plus the 5 mirror resolutions of EXP-C03-03) agree with ZG. The 24 rules left open
  are all terminating by ZG cases 3/4.

**What else is in the 1994 report [LIT].**
- Prop 3.1–3.2: p ≥ s or q ≥ r is simply terminating (rpo; or the interpretation [0](x) = (r+1)x,
  [1](x) = x + 1); linear derivations if p > s or q > r.
- Prop 3.3 and §3.1: quadratic for p = s, q = r ("0^p behave exactly like single characters";
  01 → 10 "is nothing but the well-known bubblesort").
- §3.2 and Prop 3.4–3.5: exponential cases; 01 → 110 has worst-case start 0^n 1 with 2^n − 1 steps.
- **Lemma 4.1:** the loop 0^p 1^{2q} → 1^r 0^s 1^q → 1^r 0^{s−p} 1^r 0^s ⊇ 0^p 1^{2q} for 2p ≤ s,
  2q ≤ r. This is the lab's CLM-C03-03 loop.
- **Lemma 4.3:** loops for p < s < 2p, q < r, q | r (and the mirror) for *all* parameters. The proof
  starts "we may assume … 1 = q", i.e. the lab's morphism-lifting reduction, then exhibits a loop
  from 0^{p²} 1².
- §§5–9: the termination proof of the hard case (dummy introduction/elimination).

### CLM-C03-01, -02, -03, -04, -05, -06: REDISCOVERY (high)
- **C03-01:** folklore; ZG Prop 3.1–3.2.
- **C03-02:** ZG Prop 3.1 (case 1 includes p = s, q = r); the lab's written proof (induction over
  zeros) is a different, valid proof (Skeptic A.1).
- **C03-03:** ZG Lemma 4.1 is the same two-step loop.
- **C03-04:** non-termination of 011 → 11100 is ZG Thm 1.1 (q < r < 2q, p = 1 | s); the explicit
  4-step loop is a certificate, not new mathematics.
- **C03-05:** closure of rewriting under morphisms is standard; ZG use exactly this reduction.
- **C03-06:** the 625-rule table is a special case of ZG Thm 1.1. **Correction:** the 24 "open"
  rules are terminating by a published theorem, so all 625 rules are classified.

### CLM-C03-07, -08, -09 (hypotheses). REDISCOVERY (high); **C03-09 must become REFUTED**
- H-C03-1 (C03-07) and H-C03-2 (C03-08) are refuted by ZG Thm 1.1 as recorded. For C03-08 the count
  is 40 counterexamples with parameters ≤ 5 (35 + the 5 mirror loops; Skeptic C5 agrees).
- **H-C03-3 (C03-09) is refuted by ZG Thm 1.1**: it predicts loops for 8 rules with parameters ≤ 5
  that ZG case 4 (or 3) declares terminating: (2,2,3,5) = 0011 → 11100000, (2,2,5,3), (2,3,4,5),
  (2,3,5,5), (2,4,5,5), (3,2,5,4), (3,2,5,5), (4,2,5,5) [COMPUTED]. As the Skeptic noted, this is
  the same footing on which H-C03-1 was refuted.

### CLM-C03-10: REDISCOVERY, verbatim (high). Recommended status: PROVEN (by literature)
- See §2.0. Update `novelty_basis` with the verbatim citation and URL, and relabel Conjecture 4.6 as
  "Theorem (Zantema–Geser 1995/2000)" in `textbook/src/04_termination.md`, `proofs/paper/C03.md`
  and the C03 README (Step 8, "Next directions" 1–3).

### CLM-C03-11: PARTIAL REDISCOVERY (medium); citation must be corrected
- [COMPUTED] All 25 stored loop lengths with r = q + 1 in EXP-C03-04 equal 1 + (k^q − 1)/(k − 1)
  exactly (`c03_loop_lengths.py`); the Skeptic found the same for 27 cases.
- [LIT] A. Geser, *Loops of superexponential lengths in one-rule string rewriting*, RTA 2002, LNCS
  2378, 267–280, https://doi.org/10.1007/3-540-45610-4_19, Theorem 1: for p ≥ 2q, q ≥ 1, r ≥ 2 the
  rule 10^p → 0^p 1^r 0^q "admits loops of length 1 + Σ_{i=0}^{ℓ−1} r^i where ℓ = ⌈p/q⌉ but no
  shorter loops". That is the same closed form, for a closely related but different family (after
  0↔1 the lab's rule is 10^q → 0^{q+1} 1^k; Geser's with q = 1 is 10^p → 0^p 1^r 0). The paper notes
  these rules loop by Sénizergues 1996 and Kobayashi et al.
- **New:** the lab's family, strategy and exact data. Whether its loops are the shortest is
  unproven.
- **Correction:** the paper is by A. Geser alone, not "Geser, Hofbauer, Waldmann".

---

## 3. Cycle C04

### CLM-C04-01: REDISCOVERY in substance (medium-high)
[COMPUTED] (`c04_census_criteria.py`) every one of the 196 rules is decided by a classical
criterion:
- 34 by a loop of length 1 (l a factor of r);
- the other 162 by at least one of:
  - |l| ≥ |r| (folklore);
  - Kurth's criterion A (a letter occurs more often in l than in r);
  - Kurth's criterion D (no overlap at one end);
  - McNaughton's barren criterion;
  - ZG Theorem 1.1.

These criteria are stated in A. Geser, J. Waldmann, M. Wenzel, *Symbolic enumeration of one-rule
string rewriting systems*, WST 2016, §4, and Geser, ICASE 2002-33, §3. W. Kurth (Dissertation, TU
Clausthal 1990) enumerated and treated all length-increasing one-rule systems with |r| ≤ 6.
The census itself was not found as a statement, but nothing in it needs a new idea.

### CLM-C04-02 (H-C04-0 refuted): REDISCOVERY (high)
- ab → bbaa is 01 → 1100, ZG's doubling region; the lab's loop is ZG Lemma 4.1.
- [COMPUTED] Of the 18 looping rules with l not a factor of r (|r| ≤ 5), 10 are in the ZG family
  and 4 more have loops of length 2 (`c04_short_loops.py`), the case analysed by W. Kurth,
  RAIRO ITA 30 (1996) 415–429, https://doi.org/10.1051/ita/1996300504151.

### CLM-C04-03: REDISCOVERY for termination (high) — confirms the C20 classification
- [LIT] A. Geser, ICASE Report 2002-33 (NASA/CR-2002-211923),
  https://ntrs.nasa.gov/api/citations/20020088729/downloads/20020088729.pdf (published as RTA 2003,
  LNCS 2706, 410–423, https://doi.org/10.1007/3-540-44881-0_29), §3:
  - Def. 3.1: with A = OVL(r,l) and B = OVL(l,r), l → r is *right barren* if l is not a factor of r
    and no l_β (l = l_β β) is a suffix of a concatenation r_{α1}⋯r_{αk} (r = r_α α).
  - Thm 3.2 (McNaughton): every non-overlapping left barren one-rule SRS terminates.
  - Thm 3.3 (Geser, habilitation, Tübingen 2002): every left barren one terminates; by reversal the
    same holds for right barren.
- [DERIVED, checked by `c04_census_criteria.py`]
  - aab → ababa: A = {a}, B = {ab}, l_β = a, r_α = abab. No (abab)^k ends in a, so it is right
    barren.
  - aab → babaa: A = {a, aa}, B = {b}, l_β = aa, r_α ∈ {baba, bab}. No concatenation ends in aa, so
    it is right barren.
  - aab is unbordered, so already McNaughton's Thm 3.2 (dual) applies to both.
- Further coverage:
  - Kobayashi, Katsura, Shikishima-Tsuji, TCS 262 (2001) 583–632,
    https://doi.org/10.1016/S0304-3975(00)00367-4, announce a complete termination characterisation
    of a^p b^q → t (t arbitrary), which contains both rules (paper not read).
  - Sénizergues (RTA 1996, LNCS 1103) proved decidability for l ∈ a*b*.
- C20's exact complexities are outside this audit. Note the ICASE wording issue in §0 item 4.

### CLM-C04-04, -05, -07, -08: REDISCOVERY (high)
- **C04-04** references are right:
  - A. Bertrand, *Sur une conjecture d'Yves Métivier*, TCS 123 (1994) 21–30,
    https://doi.org/10.1016/0304-3975(94)90066-3;
  - RTA LooP problem #20 (solved): bound n²/4, attained by ba → ab;
  - the quadratic behaviour of ab → ba is also ZG Prop 3.3.
- **C04-05:** V. van Oostrom, *Random descent*, RTA 2007, LNCS 4533, 314–328,
  https://doi.org/10.1007/978-3-540-73449-9_24. The unbordered case is the classical "no critical
  pairs ⇒ one-step diamond".
- **C04-07:** [DERIVED] the only critical peak of aa → a is aa ← aaa → aa, joinable in 0 = 0 steps,
  so van Oostrom's local criterion gives RD immediately.
- **C04-08:** elementary (every option lowers D by one).

### CLM-C04-06: REDISCOVERY in substance (medium-high)
- [LIT] M. Latteux and Y. Roos, *One-rule length-preserving rewrite systems and rational
  transductions*, RAIRO-ITA 48 (2014) 149–171, https://doi.org/10.1051/ita/2013044 (read).
  - **Lemma 3.7:** for u → v with |u| = |v|, u ≠ v: (1) w →⁺ w′ ⇒ Δ(w,w′) = Δ(u,v); (2) if w →ⁿ w′
    and w →ᵐ w′ then n = m.
  - Proof: for |z| ≤ Δ(u,v) the scattered-subword counts satisfy C(w′, z) − C(w, z) =
    n(C(v, z) − C(u, z)) (Property 3.5.3, "already Lemma 3.5 in" Y. Métivier, TCS 35 (1985) 71–87,
    https://doi.org/10.1016/0304-3975(85)90006-4).
  - A subword count with C(u,z) ≠ C(v,z), |z| = Δ(u,v), is therefore a constant-step potential, the
    same role as the lab's power sum Σ i^K. The two potentials are linear combinations of each other
    (Σ_{w_i = c} C(i, K) counts subwords of the form (K letters)·c).
- [LIT] A. Adinayev and I. Stein, arXiv:1910.02644, §1: "the reduction graph of a one-rule SRS is
  always a graded graph (… any two paths from x to y have the same length)".
- [DERIVED] "Terminating one-rule system: confluent ⇔ random descent" follows in two lines; not
  found verbatim.
- **New:** only the explicit power-sum form of the potential. The lab's earlier closest reference
  (Latteux–Roos, Inf. Comput. 2015) is the sequel of the paper that contains the result.

### CLM-C04-09 and -11: POTENTIALLY NOVEL, **low** confidence
- [LIT] ZG 1994 Prop 3.2 gives only D(n) = O(n) for 0²1 → 10 = aab → ba.
- KKS 2001 (above) state in their abstract that they "give a complete analysis of the derivational
  complexity for the system a^p b^q → b^n a^m"; aab → ba is a²b → ba. I could not obtain the paper
  (ScienceDirect blocks this environment; no preprint found).
- **Before any novelty claim, someone with library access must check whether KKS 2001 contains
  D(n) = n − 1 − κ(n) or only the growth class.**
- The non-rationality (C04-11) stands or falls with this.
- OEIS: D(n) is A247983 shifted (see C04-10); κ(n) is not in the OEIS.

### CLM-C04-10: POTENTIALLY NOVEL (medium) — answers a question in the OEIS
- [LIT] OEIS A247983 (Kimberling, 2014) has no formula; its comment and A083706's comment ask
  "Is A247983(n+1) = A247983(n) iff n is in A083706?" with A083706(k) = 2^{k+1} + k − 1.
- [DERIVED] From A(n) = n − J(n): A stalls exactly when n + 2 = 2^j + j, i.e.
  n = 2^j + j − 2 = A083706(j − 1). So the answer is **yes**, for n ≥ 1 (Skeptic C6: the identity
  fails at n = 0, outside the OEIS offset).
- [COMPUTED] (`c04_kimberling.py`) formula = OEIS data for n ≤ 68; stall set = A083706 below 5000.
- The tail bounds 2^{−k}/(k+2) ≤ t(k) < 2^{−k}/(k+1) are standard; the closed form was not found.
- Recommendation: submit the formula and the answer to Kimberling's question to the OEIS (human
  decision).

### CLM-C04-12: PARTIAL REDISCOVERY (medium)
- Known [LIT]:
  - the growth classes of the ZG-family members (ab → ba quadratic; ab → bba, ab → baa exponential
    with worst case 2^{n−1} − 1; aab → baa quadratic; aab → ba linear): ZG 1994 §3;
  - the n²/4 bound for length-preserving rules: Bertrand 1994.
- [DERIVED, sketch] ⌊n²/8⌋ for aab → baa follows from ZG's remark that for p = s the blocks 0^p act
  as letters (k pairs and n − 2k ones, max k(n − 2k)).
- Not found: ⌊n(n−1)/6⌋ for aab → aba (not a ZG-family rule); KKS 2001 may contain more (unread).
  The Skeptic re-verified all closed forms numerically.

### CLM-C04-13 to -16: REDISCOVERY (high)
- The octal codes are correct:
  - [COMPUTED] 0.4 equals Dawson's Kayles shifted by one;
  - DK satisfies G(n+34) = G(n) from n = 53 and fails at n = 52 (agrees with the Skeptic);
  - a¹⁴ has value 4 (the first 4 in A002187, shifted);
  - Guy and Smith, Proc. Cambridge Philos. Soc. 52 (1956) 514–526,
    https://doi.org/10.1017/S0305004100031509.
- **C04-16:**
  - J. P. Grossman, *Searching for periodicity in Officers*, Games of No Chance 5, MSRI Publ. 70
    (2019), https://library.slmath.org/books/Book70/files/1016.pdf: more than 140 trillion values,
    no period. This supports the lab's "1.4·10¹⁴".
  - A. Flammenkamp's table (https://wwwhomes.uni-bielefeld.de/achim/octal.html, updated
    2026-10-17): .06 to n = 2²⁷, .007 to 2³⁴, .6 to 2³⁹, no period known.
  - [COMPUTED] The 0.06 Grundy sequence is absent from the OEIS (offsets 0 and 1); .007 is A395248;
    .6 is A046695.

---

## 4. Cycle C06

General finding: no source treats "successor-anchored" magmas, i.e. a fixed element whose right
translation is the N-cycle, for any law other than left-distributivity. P. Biane, arXiv:1810.00548,
describes Laver tables as "left distributive, with one element acting by right multiplication as a
cyclic permutation". Searches for the specific laws found nothing (§8).

- **C06-01** REDISCOVERY (high). References fine; the Skeptic confirmed the corrected wording.
- **C06-02** REDISCOVERY (folklore; high). Trivial.
- **C06-03** PARTIAL REDISCOVERY (medium).
  - [LIT] The unique model x ⋆ y = x + 1 is the **cyclic rack** C_N, a standard example (R. Fenn and
    C. Rourke, J. Knot Theory Ramif. 1 (1992) 343–406, https://doi.org/10.1142/S0218216592000203;
    P. Lopes and D. Roseman, *On finite racks and quandles*, arXiv:math/0412487, Example 2.3:
    "C_n is the cyclic rack… i ∗ j := i + 1 mod n").
  - Uniqueness among anchored right-distributive magmas was not found stated; it is a two-line
    argument.
- **C06-05** PARTIAL REDISCOVERY (medium). A map commuting with x ↦ x + 1 is a translation, a
  one-line folklore fact. The count N^{N−1} is then immediate (A000169). No anchored statement was
  found.
- **C06-06 (odd law), C06-07 (golden law)** POTENTIALLY NOVEL, small (medium-low).
  - Searched: "(xy)z = x(y(zz))", "x((yz)z)" and variants; the Equational Theories Project scope
    (≤ 4 operations, so these 5-operation laws are outside it); affine/linear groupoid literature
    (e.g. Phillips–Vojtěchovský, J. Symb. Comput. 40 (2005), linear identities only).
  - The number theory is classical: A089270's comment that these are the moduli with
    x² ≡ x + 1 solvable has a proof by W. Lang (linked there); A087781 carries the multiplicative
    formula (2026).
  - The correspondence with an anchored magma law was not found.
- **C06-08** **PARTIAL REDISCOVERY** (downgrade; medium).
  - [DERIVED] With a · b := (a − 1) ⋆ b the anchor becomes a right identity: a · 0 = a, and
    left-permutability is preserved. Then:
    - x · y = x(y · 0) = y(x · 0) = y · x;
    - (xy)z = z(xy) = x(zy) = x(yz).
    So (ℤ/N, ·) is a commutative monoid with identity 0. That is the whole content of Theorem 7;
    the centraliser argument is not needed.
  - The same two-line lemma is standard for AG-groupoids ("an AG-groupoid with a right identity is a
    commutative monoid", e.g. W. A. Dudek and R. S. Gigoń, Semigroup Forum 87 (2013) 201–229,
    https://doi.org/10.1007/s00233-013-9465-z).
  - A058156 is by definition "labeled commutative monoids of order n with a fixed identity".
  - **New:** only the anchored packaging.
- **C06-04, -09, -10, -11** POTENTIALLY NOVEL as data or conjectures (low). The Skeptic extended
  C06-10 to N ≤ 16.
- **C06-12** REDISCOVERY in substance (medium-high).
  - [LIT] For any equational class the spectrum contains 1 and is closed under multiplication
    (direct products). This is "obvious" in J. Froemke and R. W. Quackenbush, Pacific J. Math. 58
    (1975) 381–386, https://msp.org/pjm/1975/58-2/p09.xhtml, who also recall Grätzer's theorem that
    every multiplicative monoid is a spectrum.
  - The anchored version needs coprimality (the successor on ℤ/N × ℤ/M is cyclic iff
    gcd(N, M) = 1). Same argument, minor new twist. Wording caveat: Skeptic C9.

---

## 5. Cycle C08

### Key sources [LIT]
- D. E. Knuth, *Fibonacci multiplication*, Appl. Math. Lett. 1 (1988) 57–60,
  https://doi.org/10.1016/0893-9659(88)90176-0.
- P. Arnoux, *Some remarks about Fibonacci multiplication*, Appl. Math. Lett. 2 (1989) 319–320,
  https://doi.org/10.1016/0893-9659(89)90078-5.
- P. J. Grabner, A. Pethő, R. F. Tichy, G. J. Woeginger (GPTW), *Associativity of recurrence
  multiplication*, Appl. Math. Lett. 7 (1994) 85–90, https://doi.org/10.1016/0893-9659(94)90017-5.
  - Not read; known through Messaoudi and the OEIS: recurrences with a₁ ≥ … ≥ a_d ≥ 1 and canonical
    initial values; ∃ s₀ such that ∘_s is associative for s > s₀; tribonacci for s > 9.
- **A. Messaoudi, *Généralisation de la multiplication de Fibonacci*, Math. Slovaca 50 (2000)
  135–148, http://dml.cz/dmlcz/136773 (read in full).**
  - Index dictionary [DERIVED]: for his G-class (G_s = 1, G_{s+1} = a₁ + 1) and for his H-class
    with a₁ = 1 (Fibonacci, tribonacci) his s is the lab's shift; for the U-class with U_s = k ≥ 2
    (e.g. Pell 1, 2, 5) the lab's shift is s − 1.
  - Prop 1: s < d ⇒ not associative.
  - Thm 2: ∘ associative ⇔ every digit convolution normalises without fractional digits.
  - Thm 3 / Cor 1: ∘ associative ⇔ the (closure of the) conjugate image set is stable under
    multiplication — **the lab's window mechanism**.
  - Thm 1 / Cor 2: U-class (G₁ = k) at lab shift 1 is associative iff p = 1, k ∈ {1, 2}.
  - Thm 4, Cor 3: U-class, p = 1, k ≥ 3: threshold at lab shift 2. Thm 5: negative p.
    Thm 6: G-class, p = 1 ⇒ s_m = 2.
  - Tribonacci: ∘₉ is associative (Thm 7, re-proving GPTW's s = 9 "d'une autre manière"); Arnoux
    conjectures ∘₃.
  - Tetranacci: associative for s ≥ 10 (Remark 2). He explicitly leaves s_m for p ≠ 1 open.
- A. Messaoudi, *Tribonacci multiplication*, Appl. Math. Lett. 15 (2002) 981–985,
  https://doi.org/10.1016/S0893-9659(02)00073-3 (not read). According to Ambrož–Masáková–Pelantová
  (2007, below) it improves the bound on fractional digits to L⊗ ≤ 6.
- **P. Ambrož, C. Frougny, Z. Masáková, E. Pelantová (AFMP), *Arithmetics on number systems with
  irrational bases*, Bull. Belg. Math. Soc. Simon Stevin 10 (2003) 641–659,
  https://doi.org/10.36045/bbms/1074791323 (read from the authors' PostScript,
  https://www.irif.fr/~cf/publications/belgian2.ps).**
  - Tribonacci: 4 ≤ L⊗ ≤ 5. Example (110100100101101)_β² = 110010001000100001001001011011.0011,
    "refut[ing] the conjecture of Arnoux that 3 is the maximal number of fractional digits".
  - L⊗ = max number of fractional digits of x·y over β-integers x, y. [DERIVED] By Messaoudi's
    Thm 2, ∘_s is associative iff β^s·x·y is a β-integer for all β-integers x, y, i.e. iff s ≥ L⊗.
    Arnoux's conjecture "∘₃ associative" is therefore the conjecture L⊗ = 3, which AFMP refuted.
  - See also Ambrož–Masáková–Pelantová, DMTCS 9(2) (2007) 73–88, https://doi.org/10.46298/dmtcs.394;
    L⊗ < ∞ for Pisot numbers: Guimond–Masáková–Pelantová, Acta Arith. 112 (2004) 23–40,
    https://doi.org/10.4064/aa112-1-2.

### CLM-C08-01: REDISCOVERY (high)
- t = 0: Knuth and Arnoux.
- All shifts s ≥ 2 for Fibonacci: Messaoudi 2000 (introduction: "dans le cas … Fibonacci,
  s_m = 2"; Thm 6 with k = 1).
- s = 0, 1 fail: Prop 1.
- The Lean proof is a verification asset.

### CLM-C08-02: POTENTIALLY NOVEL (conjecture; low)
- Not found. The natural attack is Messaoudi's Cor 1 (window stability).
- Related known fact: property (F) implies Pisot (C. Frougny and B. Solomyak, Ergodic Theory Dynam.
  Systems 12 (1992) 713–723).
- The lab's evidence (explicit failures for all tested shifts) is solid as data.

### CLM-C08-03: REDISCOVERY (high), but the title overstates the theorem
- GPTW cover non-increasing coefficients with canonical initial values, not all Pisot sequences.
- [DERIVED, hedged] Via Messaoudi Thm 2, eventual associativity for a canonical sequence means that
  products of β-integers have bounded fractional length (true for these β by
  Frougny–Solomyak/Guimond–Masáková–Pelantová). This is not automatic for every Pisot β or for
  non-canonical initial values.
- The lab's G(k+1) = G(k) + G(k−3) (no associative shift ≤ 20) may be a genuine exception.
- Suggested title: "Sequences with non-increasing coefficients and canonical initial values (GPTW)".

### CLM-C08-04: POTENTIALLY NOVEL (low), evidence needs repair
- [COMPUTED] (`c08_quadratic.py`, lab's own `systems/circle.py`) two of the ten "non-monotone"
  examples of EXP-C08-04 are false positives:
  - G(k+1) = 4G(k) + 3G(k−1), G = 1, 5, …: s = 4 is **not** associative,
    (50 ∘ 96) ∘ 1 = 986418448 ≠ 986418624;
  - G(k+1) = 3G(k) + 3G(k−1), G = 1, 2, …: s = 7 is **not** associative,
    (41 ∘ 280) ∘ 1 = 2459991795210 ≠ 2459991782925.
- [DERIVED] For canonical (Parry) sequences, appending a zero keeps a greedy word greedy. With
  Messaoudi's Thm 2 (stated for his G- and H-classes), associativity at s therefore implies it at
  s + 1, whatever the sign of β. Indeed (4,3; 1,5) is canonical, so its listed set {4} ∪ [6, 10]
  was impossible.
- The remaining 8 examples are all non-canonical (G₁ ∉ {p, p + 1}), with β < 0. For them no failure
  was found at the isolated shift for a, b < 300.
- So the conjecture is only meaningful for non-canonical initial values and should be restated so.

### CLM-C08-05: PARTIAL REDISCOVERY; **two listed thresholds are wrong** (high confidence in the errors)
| sequence | lab | literature / my check |
|---|---|---|
| Fibonacci 1,2 | 2 | 2 (Knuth; Messaoudi) |
| Pell 1,2,5 | 1 | 1 (Messaoudi Thm 1: U-class, p = 1, k = 2) |
| (2,2) 1,2 | 5 | open in Messaoudi (p ≠ 1); [COMPUTED] s = 4 fails, s = 5 no failure found |
| tribonacci 1,2,4 | 3 | **wrong**: s = 3 fails (AFMP 2003); [COMPUTED] (10016 ∘₃ 10016) ∘₃ 1 = 3414681926 ≠ 3414681924. Known bounds: s ≥ 9 (GPTW; Messaoudi 2000 Thm 7), s ≥ 6 (Messaoudi 2002), and [DERIVED] s ≥ 5 from AFMP's L⊗ ≤ 5 with Messaoudi's Thm 2. s = 4 holds iff L⊗ = 4, open in the sources read |
| 4-bonacci 1,2,4,8 | 7 | Messaoudi: s ≥ 10 proved; [COMPUTED] s = 6 fails, 7–10 no failure found |
| G(k+1) = G(k) + G(k−2) 1,2,3 | 10 | **wrong**: [COMPUTED] (78 ∘₁₀ 248) ∘₁₀ 1 = 31037057 ≠ 31037038; s = 11 no failure found |
| (3,3) 1,5 | 10 | [COMPUTED] s = 9 fails, 10–11 no failure found |

**Lesson:** random triples up to 10⁶ miss rare failures (the tribonacci failure needs a = 10016 with
a specific digit pattern and is missed by 3000 random pairs). Thresholds should be certified with
Messaoudi's criterion (fractional length of products of β-integers) or bounded from below by
explicit counterexamples, not by random testing.

### CLM-C08-06 (H-C08-1 refuted): REDISCOVERY (high)
GPTW 1994 and Messaoudi 2000 exhibit infinitely many associative circle products.

---

## 6. Cycle C09

- **C09-01** REDISCOVERY (high).
  - Arnoux 1989: embedding in ℤ[φ]; units ±φ^k are classical.
  - [LIT + DERIVED, COMPUTED] OEIS A101330 contains Lunnon's formula (2008)
    T(n,k) = 3nk − n⌊(k+1)/φ²⌋ − k⌊(n+1)/φ²⌋. Since ⌊(k+1)/φ²⌋ = k − k*, it equals the lab's
    a ∘ b = ab + ab* + a*b (`c09_lunnon.py`: equal for all n, k < 400).
- **C09-02** REDISCOVERY (trivial). 8 = F₆ = F₂ ∘ F₂ ∘ F₂ = F₃ ∘ F₃ follows from F_j ∘ F_k = F_{j+k},
  which is immediate from Knuth's definition.
- **C09-03, -04** POTENTIALLY NOVEL, small (medium-low).
  - The window (−ψ², −ψ) and its stability under multiplication are Arnoux's mechanism, as also
    used by Messaoudi.
  - The observation that products fall into the sub-window (ψ³, ψ²) of length 1/φ, so that a set of
    density 1/φ² can never be a product, was not found.
  - Searched: "Fibonacci multiplication" with irreducible/prime/factorisation; Porta–Stolarsky and
    Fraenkel–Porta–Stolarsky "arithmetical semigroups" (Progr. Math. 85 (1990) 255–264,
    https://doi.org/10.1007/978-1-4612-3464-7_16 — only the 2-page preview read; it embeds
    Beatty-defined associative operations into ℤ[φ] and should be read in full before publication);
    OEIS.
  - [COMPUTED] The reducibles are not in the OEIS. The irreducibles match A026273/A080746 only on a
    20-term window, consistent with the lab's own reading.
- **C09-05** POTENTIALLY NOVEL (conjecture; low).
- **C09-06** POTENTIALLY NOVEL (minor corollary of the embedding; medium-low).
- **C09-07** REDISCOVERY in substance (high): it is the multiplicativity of the field norm.
- **C09-08** POTENTIALLY NOVEL as data (medium).

---

## 7. Cycle C10

### Key source [LIT]
V. Berthé, C. Frougny, M. Rigo, J. Sakarovitch (BFRS), *The carry propagation of the successor
function*, Adv. Appl. Math. 120 (2020) 102062, https://doi.org/10.1016/j.aam.2020.102062
(arXiv:1907.01464, read).
- Def. 3.1: cp(N) = length of the suffix of rep(N) after the longest common prefix with rep(N+1)
  (e.g. cp_F(12) = 6 for 10101 → 100000).
- Formula (3), Cor. 3.16: CP = γ/(γ − 1), γ = growth rate of the language.
- Base p gives p/(p − 1). Thm 3.23: rational base p/q in the Akiyama–Frougny–Sakarovitch
  normalisation gives p/(p − q). §5: ergodic method for β-numeration.

### Assessments
- **C10-01** REDISCOVERY (high).
  - Base b: BFRS intro (both measures coincide); binary counter: Cormen et al., *Introduction to
    Algorithms*, ch. 17 (potential = number of 1s).
  - Factorial base e − 1, negabinary, balanced ternary and Gray code: the same frequency argument.
- **C10-02** REDISCOVERY in substance (high).
  - [LIT] T_m is OEIS A215005 (Ratushnyak 2012), *including* the closed form
    a(n) = 2F(n+2) − (2n + 9 − (−1)^n)/4 (Kotesovec), which equals 2G_m − ⌈m/2⌉ − 2.
  - [DERIVED] Each Zeckendorf successor adds exactly one digit 1 (x0(10)^k → x10^{2k} and
    x0(10)^k1 → x10^{2k+1}). Hence d(n, n+1) = 2 + s_Z(n) − s_Z(n+1) and
    Σ_{n<N} d(n, n+1) = 2N − s_Z(N): the binary-counter potential argument verbatim.
    [COMPUTED] for N < 3000.
  - **State the measure.** [COMPUTED] (`c10_measures.py`, N = 2·10⁵) mean Hamming cost 1.99998,
    mean BFRS carry propagation 2.61799 ≈ φ². Under the published standard measure Zeckendorf
    counting costs φ², more than binary (2).
- **C10-03** REDISCOVERY (high). H-C10-0 is false under both measures (2 = 2, resp. φ² > 2).
- **C10-04** REDISCOVERY in substance (medium-high): each firing destroys m − Σb tokens. The base-b
  case is the classical 1/(b − 1) carries per increment.
- **C10-05** PARTIAL REDISCOVERY (medium).
  - Integer base: classical.
  - Rational base in the AFS normalisation: BFRS Thm 3.23 gives p/(p − q), with the suffix measure,
    for adding 1 to N, i.e. q chips.
  - The lab's chip normalisation (one chip per increment), its value 1 + 1/(m − q), and the general
    offset g were not found.
- **C10-06** POTENTIALLY NOVEL (conjecture; low). Cite BFRS §5 as the established framework.
- **C10-07** REDISCOVERY (high): E. W. Myers, Inform. Process. Lett. 17 (1983) 241–248,
  https://doi.org/10.1016/0020-0190(83)90106-0; C. Okasaki, *Purely functional random-access lists*
  (FPCA 1995). The average 3/2 is elementary.

---

## 8. Searches performed (including negative results)

- **C03**
  - ZG theorem: Springer (paywall, but page-one previews work); UU DSpace and research portal (403,
    Cloudflare); **ics-archive.science.uu.nl (works)**; Zantema's TU/e pages (no PDFs); zbMATH
    (review withheld).
  - Geser 2002 (preview read); GWW 2016; Kfoury, arXiv:2608.19397 (survey; one-rule termination
    still open).
- **C04**
  - "one-rule" derivational complexity; aab → ba and 001 → 10 (no hits); KKS 2001 (Crossref,
    OpenAlex, ScienceDirect blocked; no preprint); Kobayashi's RIMS notes 1712-19 and 1809-26 (no
    one-rule details).
  - RTA LooP #20; Latteux–Roos 2014 (read), 2015 (abstract); Adinayev–Stein (read); Stein, RAIRO 49
    (2015) (a different notion of "graded").
  - Geser ICASE 2002-33 (read); McNaughton (via Geser); Kurth 1996; Hofbauer–Waldmann termination
    exercises (no aab → ba).
  - Octal games: Flammenkamp, Grossman. OEIS A247983, A083706, A247968, A002187, A046695, A395248;
    0.06 Grundy (no match, offsets 0/1); κ(n) (no match); text searches "octal game .06" (no entry).
- **C06**
  - "anchored/successor-anchored magma", "x*0 = x+1", Laver-table analogues of other identities,
    "(xy)z = x(y(zz))", "x((yz)z)" (all negative).
  - Cyclic/permutation racks (found); left-permutable + right identity (AG-groupoid literature
    found; no verbatim left-permutable statement); spectra of equational classes (found).
  - OEIS A058156, A089270, A087781, A098820, A000169.
- **C08**
  - GPTW (abstract-level only); Messaoudi 2000 (read), 2002 (metadata); AFMP 2003 (read);
    Ambrož–Masáková–Pelantová 2007 (read).
  - arXiv "Fibonacci multiplication" (no new hits); OEIS A101330, A101646, A101385.
  - Not found: non-Pisot non-associativity; sign-of-conjugate monotonicity.
- **C09**
  - "Fibonacci/Knuth multiplication" with primes, irreducibles, factorisation (negative);
    Porta–Stolarsky; Fraenkel–Porta–Stolarsky (preview only).
  - OEIS irreducibles, reducibles (no match), A026273/A026274.
- **C10**
  - BFRS 2020 (read), Barcucci–Pinzani–Poneti 2005 (via BFRS); A215005, A007895.
  - OEIS text searches "Zeckendorf increment", "Fibonacci counter", "bits change" (no relevant
    entry); the per-step cost sequence is not in the OEIS (it is 2 + A007895(n) − A007895(n+1)).

## 9. Independent computations (`reviews/historian_checks/`, all under `nice -n 10`)

1. `c03_zg_compare.py`:
   - H-C03-4 ≡ ZG Thm 1.1 on 40⁴ quadruples;
   - EXP-C03-02 statuses agree with ZG;
   - 24 unknowns all terminating; 5 mirror-resolved all non-terminating;
   - H-C03-2 has 40 disagreements, H-C03-3 has 8.
2. `c03_loop_lengths.py`: 25/25 stored base loops have length 1 + Σ_{i<q} k^i.
3. `c04_census_criteria.py`:
   - |r| ≤ 3: 196/196 decided by classical criteria;
   - |r| ≤ 5: 10 rules not covered by those criteria.
4. `c04_short_loops.py`: 4 of those 10 have loops of length 2.
5. `c04_kimberling.py`: formula = A247983 data (n ≤ 68); stalls = A083706 (< 5000).
6. `seqs.py`, `oeis_queries.py`:
   - OEIS look-ups;
   - Dawson's Kayles periodic from 53 (fails at 52); 0.4 = DK shifted;
   - Σ_{n<N} d_Z = 2N − s_Z(N) for N < 3000.
7. `c08_tribonacci.py`, `c08_tribonacci_afmp.py`:
   - AFMP's x ↔ a = 10016; x² has 4 fractional digits;
   - ∘₃ fails with c = 1, 2, 3; ∘₄, ∘₅ fine for this pair;
   - confirmed with the lab's `systems/circle.py`.
8. `c08_quadratic.py`, `c08_thresholds.py`: the counterexamples in §5.
9. `c09_lunnon.py`: lab formula ≡ Lunnon's A101330 formula (n, k < 400).
10. `c10_measures.py`: Hamming vs BFRS carry propagation for Zeckendorf (2 vs φ²).

## 10. Caveats

- Not read (paywalled or blocked): KKS 2001 (decisive for C04-09/11/12), GPTW 1994, Messaoudi 2002,
  Bertrand 1994, Métivier 1985, Fraenkel–Porta–Stolarsky 1990 beyond its first two pages,
  McNaughton's reports, Kurth's dissertation. Statements about them come from abstracts or from
  papers that cite them.
- The [DERIVED] items are mine and short; the Skeptic should check them:
  - §2.0 equivalence;
  - C04-07;
  - C04-10 → Kimberling;
  - C06-08 two-line lemma;
  - C08-04 monotonicity for canonical sequences, which relies on Messaoudi's Thm 2 holding for the
    sequence at hand; for (4,3; 1,5) the explicit counterexample makes it moot;
  - the C10-02 identity.
- "No failure found" in §5 is evidence, not proof. Only the stated counterexamples are certain
  (exact integer arithmetic, reproduced with the lab's own implementation).
- Absence from the sources searched is weak evidence of novelty. MathSciNet and zbMATH full text
  were unavailable.
