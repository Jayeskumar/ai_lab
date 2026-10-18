# Research Journal

_Rendered from the append-only log `journal/entries.jsonl`. Entries are never edited or removed; corrections appear as later `revision` entries._


## C01

### [2026-10-18T06:44:01Z] Research Director — decision (`C01-01`)

Opened Branch A with the question "can quantity be derived from transformations alone?" Chose the swap system and one-symbol relations as minimal test beds; meta-level use of ordinary mathematics declared explicitly in SYSTEMS.md section 0.

*Evidence:* research/systems/SYSTEMS.md

### [2026-10-18T06:44:01Z] Mathematical Inventor — hypothesis (`C01-02`)

Proposed H-C01-1 (counting is the complete invariant of commutation), H-C01-2/3 (one-symbol relations give threshold-plus-cycle structures) and the emergence of multiplication as composition.

*Evidence:* EXP-C01-01, EXP-C01-02, EXP-C01-03

### [2026-10-18T06:44:01Z] Mathematical Explorer — result (`C01-03`)

EXP-C01-01..03 confirmed all three on exhaustive finite slices (25 slices; 6159 relation sets with two independent algorithms; all semiring laws on a^0..a^12). Two-symbol substitutions do not commute in 154/200 random pairs.

*Evidence:* EXP-C01-01, EXP-C01-02, EXP-C01-03

### [2026-10-18T06:44:01Z] Mathematical Inventor — hypothesis (`C01-04`)

Proposed the deliberately bold H-C01-4 - any single rearranging relation eventually generates counting equivalence.

*Evidence:* CLM-C01-05

### [2026-10-18T06:44:01Z] Mathematical Skeptic — rejection (`C01-05`)

H-C01-4 rejected. EXP-C01-04 found counterexamples for all 33 relations of length 3 and 4; the simplest is aab <-> aba, under which baa is isolated.

*Evidence:* EXP-C01-04, CLM-C01-05

### [2026-10-18T06:44:01Z] Mathematical Explorer — surprise (`C01-06`)

The class counts in EXP-C01-04 were not random - every length-3 relation gave 2,4,7,12,20,33,... = F(n+3)-1 and 25 of the 27 length-4 relations gave tribonacci partial sums, while aaba<->abaa (and its complement) gave 97 instead of 96 at n = 7.

*Evidence:* EXP-C01-04

### [2026-10-18T06:44:01Z] Mathematical Explorer — hypothesis (`C01-07`)

Explanation proposed (H-C01-5) - if u is unbordered, u -> v has no critical pairs and terminates by lexicographic monotonicity, so classes are u-avoiding words (Guibas-Odlyzko count 1/(1-qx+x^k)). The exceptional pair has both sides bordered.

*Evidence:* EXP-C01-05

### [2026-10-18T06:44:01Z] Formal Verifier — result (`C01-08`)

EXP-C01-05 tested H-C01-5 on 1037 relations (binary k<=5, ternary k<=3) - 0 failures among 756 with an unbordered side; 81 both-bordered relations deviate.

*Evidence:* EXP-C01-05

### [2026-10-18T06:44:01Z] Mathematical Explorer — pattern (`C01-09`)

All 81 deviations share a common border between u and v, and their counts match avoidance of a word whose borders are exactly the common borders. Formulated H-C01-7 (common-border conjecture).

*Evidence:* EXP-C01-05, CLM-C01-08

### [2026-10-18T06:44:01Z] Formal Verifier — proof (`C01-10`)

Proved the border-containment theorem (Borders(u) in Borders(v) implies {u -> v} convergent) - the overlap along a common border joins in one step on each side. The one-step joinability identity is checked in Lean (common_border_joinable).

*Evidence:* CLM-C01-06, proofs/lean/Infinity/C01_Quantity.lean

### [2026-10-18T06:44:01Z] Formal Verifier — result (`C01-11`)

EXP-C01-06 confirmed H-C01-7 on 2159 relations including 1326 hard ones. EXP-C01-07 turned 1632 of them into proofs for all n (finite completion re-verified independently, rational generating function, recurrence-order bound). 527 hard relations have infinite completions, e.g. aba <-> bab completes to b a^j b a -> a b a a b^(j-1).

*Evidence:* EXP-C01-06, EXP-C01-07, CLM-C01-07

### [2026-10-18T06:44:01Z] Formal Verifier — proof (`C01-12`)

Lean 4 + Mathlib proofs compiled with standard axioms only - commEq_iff_count, projection_is_unary, gen_iff, exactly_m_add_p_classes, common_border_joinable.

*Evidence:* proofs/lean/Infinity/C01_Quantity.lean

### [2026-10-18T06:44:01Z] Historian and Novelty Analyst — novelty (`C01-13`)

Theorems 1-4 are textbook rediscoveries (Parikh vectors, monogenic semigroups, endomorphisms of N). Theorem 5 is very likely folklore (Newman + critical pairs + Guibas-Odlyzko). Two quick searches found no general common-border formula; CLM-C01-08 marked POTENTIALLY NOVEL pending a deeper audit.

*Evidence:* CLM-C01-06, CLM-C01-08

### [2026-10-18T06:44:01Z] Mathematical Skeptic — review (`C01-14`)

Caution recorded - the computer-assisted proofs (CLM-C01-07) trust the Python implementation; the guard is an independent convergence re-check plus brute-force agreement for n <= 8. Written proofs of CLM-C01-03/04/06 still need an independent review.

*Evidence:* CLM-C01-07


## C02

### [2026-10-18T07:22:46Z] Mathematical Inventor — hypothesis (`C02-01`)

Proposed exchange systems - tokens on levels with local exchange rules - as a route from System A to positional numeration without assuming place value. H-C02-0 (binary carrying) and H-C02-F (Fibonacci exchanges).

*Evidence:* EXP-C02-01, EXP-C02-02

### [2026-10-18T07:22:46Z] Mathematical Explorer — result (`C02-02`)

Both confirmed on exhaustive derivation graphs. The Fibonacci system is not abelian - derivation lengths range from n - z(n) to roughly twice that.

*Evidence:* EXP-C02-01, EXP-C02-02

### [2026-10-18T07:22:46Z] Mathematical Explorer — surprise (`C02-03`)

The rule 2[k] -> [k+1]+[k+2] (sum b = m) does not terminate from 6 tokens - a pattern (2,1) glides upward forever. Initially mistaken for a bug.

*Evidence:* EXP-C02-03

### [2026-10-18T07:22:46Z] Formal Verifier — infrastructure (`C02-04`)

First survey run flagged 74 'violations' of H-C02-1 because only periodic gliders counted as certificates. Added the monotone-pumping certificate (a later window dominating an earlier one with an entry >= m); all 158 non-terminating rules are now certified.

*Evidence:* EXP-C02-03

### [2026-10-18T07:22:46Z] Mathematical Explorer — pattern (`C02-05`)

For every sum-b-equals-m rule the glider is exactly the tail-sum window T = (sum_{j>=i} b_j), i.e. every level fires exactly once - the uniform-firing steady state.

*Evidence:* EXP-C02-03, CLM-C02-04

### [2026-10-18T07:22:46Z] Mathematical Inventor — hypothesis (`C02-06`)

Proposed H-C02-4 - every terminating rule represents each integer uniquely.

*Evidence:* CLM-C02-06

### [2026-10-18T07:22:46Z] Mathematical Skeptic — rejection (`C02-07`)

H-C02-4 refuted by 4[k] -> 2[k+1] (base 2 with digits 0..3) and three relatives. All failures have a non-primitive reduced carry polynomial or ask for uniqueness off the reachable lattice. Proposed H-C02-4'.

*Evidence:* EXP-C02-04, CLM-C02-06

### [2026-10-18T07:22:46Z] Formal Verifier — proof (`C02-08`)

Proved and Lean-verified the uniqueness core (digits_unique) - Bezout over Q at the common root, Gauss's lemma, and a trailing-coefficient bound. EXP-C02-05 confirms H-C02-4' with 0 violations.

*Evidence:* CLM-C02-07, EXP-C02-05, proofs/lean/Infinity/C02_Exchange.lean

### [2026-10-18T07:22:46Z] Formal Verifier — infrastructure (`C02-09`)

Lesson - a first implementation of EXP-C02-04 called sympy inside a 200k-iteration loop and timed out; replaced by exact integer matrices (x^k mod the minimal polynomial, scaled by a common denominator). Also, a pkill pattern matched its own shell; use patterns that cannot match the issuing command line.

*Evidence:* EXP-C02-04

### [2026-10-18T07:22:46Z] Historian and Novelty Analyst — novelty (`C02-10`)

The Fibonacci exchange system is the Zeckendorf game (Baird-Smith, Epstein, Flint, Miller 2018); our shortest-derivation theorem is theirs and A219641. Rule p -> q is the rational base system of Akiyama-Frougny-Sakarovitch (A024629). The OEIS hit A089881 (twin primes) for representation lengths is a coincidence on a shifted window - matches must be read, not just counted.

*Evidence:* EXP-C02-06, CLM-C02-09

### [2026-10-18T07:22:46Z] Mathematical Skeptic — review (`C02-11`)

Open caution - the uniqueness theorem's novelty is doubtful (canonical number system literature); keep NOT ASSESSED until the Historian audit. The B = m conjecture still lacks the spreading lemma.

*Evidence:* CLM-C02-07, CLM-C02-04


## C01

### [2026-10-18T08:13:57Z] Historian and Novelty Analyst — novelty (`C01-15`)

Independent novelty audit (reviews/historian_C01_C02.md) - CLM-C01-06 is the length-preserving case of Kurth's 1987 one-rule confluence criterion (an iff); the no-common-border case of the common-border formula follows from Gray-Steinberg 2026 Thm 8.1 plus Anick; all 527 relations we could not prove are in that case. Only 'common border without containment' remains unpublished, and identities derived from Gray-Steinberg 2022 settle the one-common-border case modulo a check.

*Evidence:* CLM-C01-06, CLM-C01-08, CLM-C01-09, CLM-C01-10

### [2026-10-18T08:13:57Z] Research Director — revision (`C01-16`)

Novelty labels revised - CLM-C01-05/06/07 to REDISCOVERY; CLM-C01-08 narrowed to the common-border-without-containment case and split into CLM-C01-09 (c = 1, rediscovery), CLM-C01-10 (one common border, potentially novel) and CLM-C01-11 (converse, Kurth). The Historian's deductions were sent to the independent Skeptic for checking; statuses stay COMPUTATIONALLY SUPPORTED until then.

*Evidence:* CLM-C01-08, CLM-C01-09, CLM-C01-10, CLM-C01-11

### [2026-10-18T08:13:57Z] Mathematical Skeptic — review (`C01-17`)

The audit's computations were run outside the repository; EXP-C01-08 reproduces them inside the lab (0 mismatches for the confluence criterion; 527/527 open relations with c = 1; 12 one-common-border relations; k = 8 two-common-border relations agree up to n = 13).

*Evidence:* EXP-C01-08


## C02

### [2026-10-18T08:13:57Z] Historian and Novelty Analyst — novelty (`C02-12`)

Independent audit (reviews/historian_C01_C02.md) - uniqueness (CLM-C02-07) and radix order (CLM-C02-08) are Akiyama-Frougny-Sakarovitch 2008 Lemma 5 and Prop. 11 transplanted; the termination dichotomy is folklore; our longest-Zeckendorf-game table is already in Baird-Smith et al. Fig. 4. Only the sum-b = m glider (CLM-C02-04, with the 28 certificates of CLM-C02-05) has no known equivalent; Propp (2017) proposed the rule family without results.

*Evidence:* CLM-C02-03, CLM-C02-04, CLM-C02-07, CLM-C02-08, CLM-C02-10

### [2026-10-18T08:13:57Z] Research Director — revision (`C02-13`)

Labels revised per the audit; README note added that AFS normalise rational-base expansions differently (their expansion of N is our chip representation of qN, e.g. AFS 3 -> 210, A024629 6 -> 210).

*Evidence:* CLM-C02-07, CLM-C02-08


## C03

### [2026-10-18T08:13:57Z] Historian and Novelty Analyst — novelty (`C03-01`)

Located the reference result (Zantema-Geser, complete characterization of termination of 0^p 1^q -> 1^r 0^s, RTA 1995 / AAECC 2000) but could not retrieve its statement - Springer, zbMATH (license-blocked text) and the Utrecht repository all refused access. Recorded verifiable facts instead - decidability for l in 0*1* (Geser-Waldmann-Wenzel WST 2016) and termination of Zantema's problem 0011 -> 111000 (Geser 1993).

*Evidence:* CLM-C03-10

### [2026-10-18T08:13:57Z] Research Director — hypothesis (`C03-02`)

Proposed H-C03-2 (terminates iff r < 2q or s < 2p), reasoning that produced blocks shorter than two consumed blocks cannot sustain growth; the Inventor's naive H-C03-1 (letter counts) was recorded alongside.

*Evidence:* CLM-C03-07, CLM-C03-08

### [2026-10-18T08:13:57Z] Mathematical Explorer — surprise (`C03-03`)

Hand analysis found that 01 -> 1100 loops (011 ->+ 11 011 00), contradicting the Inventor's belief that rules with p = 1 always terminate. The first machine run then found 011 -> 11100 looping from 001111 in four steps - H-C03-2 is false.

*Evidence:* EXP-C03-01, CLM-C03-04

### [2026-10-18T08:13:57Z] Mathematical Skeptic — rejection (`C03-04`)

H-C03-2 rejected - 12 counterexamples with parameters <= 4 and 35 with parameters <= 5; the simplest (011 -> 11100) is now Lean-verified.

*Evidence:* EXP-C03-01, EXP-C03-02, CLM-C03-08

### [2026-10-18T08:13:57Z] Mathematical Explorer — hypothesis (`C03-05`)

All 28 first-survey loops lie in the region (r >= 2q or s >= 2p) with both counts growing; proposed H-C03-3.

*Evidence:* EXP-C03-01, CLM-C03-09

### [2026-10-18T08:13:57Z] Formal Verifier — infrastructure (`C03-06`)

Breadth-first forward closures (<= 40-90 letters) missed loops for 0 111 -> 1111 000; a deterministic rightmost-redex strategy from 0^2 1^9 found one after 14 steps (53 letters). Added the strategy finder; long loops need depth, not breadth.

*Evidence:* EXP-C03-02

### [2026-10-18T08:13:57Z] Mathematical Explorer — surprise (`C03-07`)

For p = 2 every s = 4 rule loops while every s = 5 rule stays unknown; exhaustive reachable sets confirm - 0011 -> 111 0^4 and 111 0^6 explode, 111 0^5 and 111 0^7 terminate from every tested start. H-C03-3 predicts the opposite for s = 5.

*Evidence:* EXP-C03-02, EXP-C03-03, CLM-C03-09

### [2026-10-18T08:13:57Z] Mathematical Inventor — pattern (`C03-08`)

The lifting lemma explains the even/odd pattern - the morphism 0 -> 0^p maps loops of 0 1^q -> 1^r 0^k onto loops of 0^p 1^q -> 1^r 0^(kp). Proposed H-C03-4 (divisibility characterization).

*Evidence:* CLM-C03-05, CLM-C03-10

### [2026-10-18T08:13:57Z] Mathematical Skeptic — contradiction (`C03-09`)

EXP-C03-03 first reported a non-finite word (001001001111 under 0011 -> 11100000) contradicting H-C03-4. Investigation showed a false alarm - the evidence routine capped words at 96 letters, but the reachable set is finite (232 words, longest 104). The cap is now a parameter; the corrected run supports H-C03-4 with 0 contradictions.

*Evidence:* EXP-C03-03

### [2026-10-18T08:13:57Z] Formal Verifier — result (`C03-10`)

All 75 base rules 0 1^q -> 1^r 0^k (q <= 6) loop; the last gap (q = 5, r = 6, k = 6) needed 1556 steps and 9367 letters. Loop lengths grow roughly like k^q.

*Evidence:* EXP-C03-04, CLM-C03-11

### [2026-10-18T08:13:57Z] Formal Verifier — failure (`C03-11`)

No matrix interpretation (d = 2 entries <= 4; upper-triangular d = 3 entries <= 5, d = 4 entries <= 2; full d = 3 entries <= 1) proves termination of any both-growing rule, including Zantema's problem and 0011 -> 11100000. Termination of the 24 open rules remains unproven here.

*Evidence:* EXP-C03-02, CLM-C03-10

### [2026-10-18T08:13:57Z] Formal Verifier — proof (`C03-12`)

Lean file C03_Termination.lean compiles with standard axioms only - counting termination, inversion termination for the swap rule, loops imply non-termination, lifting lemma, the doubling-region loop and the explicit loop of 011 -> 11100.

*Evidence:* proofs/lean/Infinity/C03_Termination.lean


## C08

### [2026-10-18T08:13:57Z] Mathematical Inventor — hypothesis (`C08-01`)

Proposed digit-position convolution ("circle") products on greedy numeration systems as an invented operation; devil's-advocate hypothesis H-C08-1 that Knuth's associative case is isolated.

*Evidence:* EXP-C08-01

### [2026-10-18T08:13:57Z] Mathematical Explorer — surprise (`C08-02`)

First run already shows associativity for Fibonacci at s = 3, 4, 5 and for many other sequences at larger shifts, with failure rates that do not depend smoothly on s.

*Evidence:* EXP-C08-01, CLM-C08-06

### [2026-10-18T08:13:57Z] Mathematical Explorer — pattern (`C08-03`)

Every persistent failure belongs to a sequence whose minimal recurrence has a second root on or outside the unit circle (e.g. roots 2 and -1). Degenerate initial conditions (powers of 2 from x^2 - x - 2) remove the bad root and restore associativity.

*Evidence:* EXP-C08-02, CLM-C08-02

### [2026-10-18T08:13:57Z] Mathematical Skeptic — review (`C08-04`)

Small-cube associativity is weak evidence; re-tested every candidate on random triples up to 1e6 and Knuth's product up to 1e9. The non-monotone shift sets survive.

*Evidence:* EXP-C08-03

### [2026-10-18T08:13:57Z] Mathematical Explorer — hypothesis (`C08-05`)

Proposed H-C08-4 - the sign of beta^s flips the product's conjugate and the greedy window is asymmetric, so non-monotonicity should need beta < 0. Confirmed on 90 quadratic Pisot sequences (30/30 positive-beta sets upward-closed).

*Evidence:* EXP-C08-04, CLM-C08-04

### [2026-10-18T08:13:57Z] Formal Verifier — proof (`C08-06`)

Wrote a complete proof that all shifted Knuth products (s >= 2) are associative using the explicit window (-psi^2, -psi) of conjugates of Zeckendorf sums; launched a Lean formalisation.

*Evidence:* CLM-C08-01, proofs/paper/C08.md

### [2026-10-18T08:13:57Z] Historian and Novelty Analyst — novelty (`C08-07`)

Eventual associativity for dominant-root recurrences is the theorem of Grabner, Petho, Tichy and Woeginger (1994); Knuth (1988) and Arnoux (1989) for Fibonacci. Our implementation reproduces OEIS A101330. Non-Pisot never-associativity and the sign-of-beta mechanism were not found in a first search.

*Evidence:* EXP-C08-05, CLM-C08-03, CLM-C08-04

### [2026-10-18T08:13:57Z] Formal Verifier — proof (`C08-08`)

Lean 4 + Mathlib formalisation of Theorem 1 completed by a dedicated Formal Verifier worker (proofs/lean/Infinity/C08_Knuth.lean, 256 lines) - circ_assoc and circ_comm for every shift t, via the twisted homomorphism E(circ t a b) = phi^t E(a) E(b) and a symmetric conjugate window |sum psi^k| < -psi. Standard axioms only. Knuth's theorem and its shifted versions are now machine-checked.

*Evidence:* CLM-C08-01, proofs/lean/Infinity/C08_Knuth.lean


## C09

### [2026-10-18T08:13:57Z] Research Director — decision (`C09-01`)

Cross-branch cycle - the associative operation found in C08 is studied as a new arithmetic. Fast exact formula a o b = ab + ab* + a*b derived from the Z[phi] embedding and validated against the digit definition on 89,401 pairs.

*Evidence:* EXP-C09-01

### [2026-10-18T08:13:57Z] Mathematical Inventor — hypothesis (`C09-02`)

Proposed H-C09-1 (circle primes thin out like primes) and the bold H-C09-2 (unique factorisation, since Z[phi] is a UFD).

*Evidence:* CLM-C09-04, CLM-C09-02

### [2026-10-18T08:13:57Z] Mathematical Skeptic — rejection (`C09-03`)

H-C09-2 fails at n = 8 = 1o1o1 = 2o2. The Fibonacci numbers are images of units, F_j o F_k = F_(j+k), so their factorisations are those of the numerical semigroup <2,3>.

*Evidence:* EXP-C09-02, CLM-C09-02

### [2026-10-18T08:13:57Z] Historian and Novelty Analyst — novelty (`C09-04`)

The OEIS returned a shifted-window match (A026273) for the irreducibles; checked term by term - it agrees for 24 terms and diverges at 40 = 4o4. Explained by the Beatty structure of 1 o b; recorded as a coincidence, not a rediscovery.

*Evidence:* EXP-C09-01

### [2026-10-18T08:13:57Z] Formal Verifier — proof (`C09-05`)

Proved the window obstruction - products have conjugate in (psi^3, psi^2), a sub-window of length 1/phi - so 1/phi^2 of all integers are forced irreducible (refuting H-C09-1), and the length bound |nu'(n)| < |psi|^r. EXP-C09-04 found no counterexample up to 1e6 and density 0.381966.

*Evidence:* CLM-C09-03, CLM-C09-06, EXP-C09-04

### [2026-10-18T08:13:57Z] Mathematical Skeptic — review (`C09-06`)

Integrity fix - EXP-C09-04 META originally claimed an exact-arithmetic re-check that was not implemented. Replaced by the actual justification (only n = 1, 2 hit the zone boundaries exactly; otherwise badly-approximable margins >= 0.4/n). Results hash unchanged.

*Evidence:* EXP-C09-04

### [2026-10-18T08:13:57Z] Mathematical Explorer — direction (`C09-07`)

Conjecture 5 - the irreducible density is exactly 1/phi^2; supported only by a slowly decreasing trend inside the product zone.

*Evidence:* CLM-C09-05


## C10

### [2026-10-18T08:13:57Z] Mathematical Inventor — hypothesis (`C10-01`)

Bold guess H-C10-0 - the sparse Zeckendorf system should count more cheaply than binary.

*Evidence:* CLM-C10-03

### [2026-10-18T08:13:57Z] Mathematical Explorer — surprise (`C10-02`)

Zeckendorf averages 1.999992 per increment - indistinguishable from binary. Derived the block recurrence T_(m+1) = T_m + T_(m-1) + ceil(m/2) + 1 and the closed form 2G_m - ceil(m/2) - 2; H-C10-0 refuted.

*Evidence:* EXP-C10-01, EXP-C10-02, CLM-C10-02

### [2026-10-18T08:13:57Z] Formal Verifier — proof (`C10-03`)

Proved that exchange systems fire 1/(m - B) times per increment (abelian property + token count) and that single-offset rules cost exactly firings + 1 (each level fires at most once per increment).

*Evidence:* CLM-C10-04, CLM-C10-05

### [2026-10-18T08:13:57Z] Mathematical Explorer — pattern (`C10-04`)

Multi-offset rules break firings + 1 - a level can receive several tokens per increment; excess costs between 0.30 and 0.83 recorded, some near simple fractions (1/2, 1/3, 5/7?) but no formula found.

*Evidence:* EXP-C10-03, CLM-C10-06

### [2026-10-18T08:13:57Z] Application Researcher — result (`C10-05`)

Negative result - no invented exchange representation beats Gray code (cost 1) or skew binary (worst case 2) as a counter; recorded honestly.

*Evidence:* EXP-C10-01, EXP-C10-03

### [2026-10-18T08:13:57Z] Historian and Novelty Analyst — novelty (`C10-06`)

Zeckendorf block totals are OEIS A215005; classical constants are folklore; skew binary is Myers/Okasaki.

*Evidence:* EXP-C10-04

