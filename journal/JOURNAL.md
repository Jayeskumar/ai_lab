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


## C02

### [2026-10-18T08:20:07Z] Research Director — proof (`C02-14`)

Proved the critical-rule conjecture (CLM-C02-04) - the sweep window map is A x - phi(x) b with A having eigenvalues 1/mu for the roots of sum b_j mu^j = m; for gcd-1 support all non-unit eigenvalues lie inside the unit disk, so after O(log n) levels the window is a large multiple of T plus a bounded error and dominates T. Completes the termination classification of carry rules (CLM-C02-11).

*Evidence:* CLM-C02-04, CLM-C02-11, proofs/paper/C02.md

### [2026-10-18T08:20:07Z] Formal Verifier — result (`C02-15`)

EXP-C02-07 tested the sharper prediction (non-termination from EVERY large start) on 98 critical rules - no spectral exception and every start beyond <= 124 certified.

*Evidence:* EXP-C02-07


## C04

### [2026-10-18T08:20:07Z] Mathematical Inventor — hypothesis (`C04-01`)

Opened C04 with the question of how long derivations of a single rule can be, when their order is irrelevant, and which games rules define. Proposed the bold H-C04-0 after noticing that every non-terminating rule with |l|, |r| <= 3 contains l in r.

*Evidence:* EXP-C04-01, CLM-C04-01

### [2026-10-18T08:20:07Z] Formal Verifier — result (`C04-02`)

All 196 rules decided by checkable certificates; two length-increasing rules (aa -> aba, bb -> bab) needed a new certificate type - a factor whose occurrence count drops by exactly one in every context.

*Evidence:* EXP-C04-01

### [2026-10-18T08:20:07Z] Mathematical Skeptic — rejection (`C04-03`)

H-C04-0 refuted by the extended census - ab -> bbaa loops via aab -> abbaa -> bb.aab.aa although ab is not a factor of bbaa; 18 such rules with |r| <= 5.

*Evidence:* EXP-C04-02, CLM-C04-02

### [2026-10-18T08:20:07Z] Formal Verifier — result (`C04-04`)

Added linear interpretations with larger coefficients and LP-found integer factor weights (re-verified exactly); 860 of 868 rules decided. aab -> ababa and aab -> babaa (two symmetry classes) stay open.

*Evidence:* EXP-C04-02, CLM-C04-03

### [2026-10-18T08:20:07Z] Mathematical Explorer — surprise (`C04-05`)

The complexity of aab -> ba admitted no linear recurrence. Pattern guesses (zeros at k^2 + 3, or Fibonacci - 1) both predicted the next stall wrongly; deriving the binary-counter-with-sink model gave stalls at 2^k + k + 1, confirmed by simulation to n = 21.

*Evidence:* EXP-C04-03, EXP-C04-04, CLM-C04-09

### [2026-10-18T08:20:07Z] Historian and Novelty Analyst — surprise (`C04-06`)

The OEIS returned A247983 (least k such that the tail of sum 1/(h 2^h) for log 2 is below 2^-n) for our complexity sequence. Proved the identity A(n) = n - max{j : 2^j + j <= n+1} = D(n+2) with Jensen's inequality and checked it to n = 1500.

*Evidence:* EXP-C04-09, EXP-C04-10, CLM-C04-10

### [2026-10-18T08:20:07Z] Mathematical Inventor — hypothesis (`C04-07`)

Proposed the bold H-C04-1 - random descent iff unbordered left-hand side.

*Evidence:* CLM-C04-07

### [2026-10-18T08:20:07Z] Mathematical Skeptic — rejection (`C04-08`)

H-C04-1 refuted by aa -> a and 17 other bordered rules with random descent. The critical-peak criterion (H-C04-2) matched observed random descent in all 162 cases.

*Evidence:* EXP-C04-05, CLM-C04-07

### [2026-10-18T08:20:07Z] Mathematical Explorer — pattern (`C04-09`)

No terminating rule was confluent without random descent. Found the reason - every one-rule system has a potential changing by a fixed nonzero amount per step (length, or a power-sum moment of one letter's positions), so derivation lengths are fixed by their endpoints.

*Evidence:* EXP-C04-06, CLM-C04-06

### [2026-10-18T08:20:07Z] Formal Verifier — revision (`C04-10`)

Terminology corrected - the first random-descent test only compared minimal and maximal lengths (length uniformity). Random descent also requires a unique normal form; 126 length-preserving rules with |l| = 4, 5 are length-uniform but not confluent. E05/E06 were re-run with the correct definitions; conclusions for |l| <= 3 were unaffected.

*Evidence:* EXP-C04-05, EXP-C04-06

### [2026-10-18T08:20:07Z] Formal Verifier — proof (`C04-11`)

Lean 4 + Mathlib - random_descent (van Oostrom's local criterion), steps_length_unique, unbordered_diamond and unbordered_random_descent for arbitrary one-rule systems, length_changing_unique, and the ab -> ba theorems (inv_step, derivation_length_eq_inv, p_positions). 19 theorems, standard axioms only.

*Evidence:* proofs/lean/Infinity/C04_Derivations.lean, CLM-C04-05, CLM-C04-04

### [2026-10-18T08:20:07Z] Mathematical Explorer — result (`C04-12`)

Rewriting games - parity for every RD rule; for unary left sides the game is a sum of run games. aa -> b is Dawson's Kayles (period 34 from 53), aa -> ab is Officers, aaa -> b is Treblecross 0.007, aaa -> ab is 0.06.

*Evidence:* EXP-C04-07, EXP-C04-08, CLM-C04-13, CLM-C04-15

### [2026-10-18T08:20:07Z] Mathematical Skeptic — rejection (`C04-13`)

H-C04-6 (Grundy values <= 3, true on all words of length <= 10) refuted - a^14 has value 4 under aa -> b. Small-window evidence was misleading.

*Evidence:* EXP-C04-08, CLM-C04-14

### [2026-10-18T08:20:07Z] Historian and Novelty Analyst — novelty (`C04-14`)

Random descent and its local criterion are van Oostrom's (RTA 2007); n^2/4 for length-preserving one-rule systems is Metivier's conjecture proved by Bertrand (1994); octal games as pins in a row are classical; Officers, 0.007 and 0.06 have open periodicity. Potentially novel - the aab -> ba complexity formula and its identity with A247983; the 0.06 Grundy sequence is absent from the OEIS.

*Evidence:* CLM-C04-05, CLM-C04-09, CLM-C04-10, CLM-C04-16

### [2026-10-18T08:20:07Z] Formal Verifier — infrastructure (`C04-15`)

Lessons - a pkill pattern again matched the issuing shell (it contained the rerun command); kill and rerun must be separate commands. A quadratic big-integer loop in a closed-form check was bounded by an early break.

*Evidence:* EXP-C04-04


## C01

### [2026-10-18T08:39:48Z] Mathematical Skeptic — review (`C01-18`)

Independent review of C01 (reviews/skeptic_C01_C02.md) - no claim refuted; written proofs of CLM-C01-03/04/06 upheld; all 1632 completion certificates of CLM-C01-07 re-verified with separate code (incl. soundness and an exact Goulden-Jackson identity); the common-border conjecture survives 295,358 further relation orbits and 1,491 targeted relations with 1-4 common borders; the Historian's c = 1 deduction upheld step by step; the one-common-border deduction has a single gap (an injectivity lemma), numerically confirmed.

*Evidence:* CLM-C01-07, CLM-C01-08, CLM-C01-09, CLM-C01-10, reviews/skeptic_C01_C02.md

### [2026-10-18T08:39:48Z] Formal Verifier — decision (`C01-19`)

Integrated the review - CLM-C01-09 (no common border) upgraded to PROVEN as a corollary of Gray-Steinberg (proofs/paper/C01.md Theorem 8), which settles all 527 relations the completion method left open; EXP-C01-07 now stores every certificate and checks soundness directly (1632/1632 rules derivable from u = v); the Lean lemma label corrected (CLM-C01-06) and its coverage restated as list identities only.

*Evidence:* CLM-C01-09, EXP-C01-07, proofs/paper/C01.md, proofs/lean/Infinity/C01_Quantity.lean


## C02

### [2026-10-18T08:39:48Z] Mathematical Skeptic — review (`C02-16`)

Independent review of all C02 claims (reviews/skeptic_C01_C02.md) - nothing refuted; CLM-C02-07 restricted (converse false for 2[k] -> 4[k+1], existence false for 2[k] -> 3[k+1] when sum b > m); a gap in the radix-order proof (CLM-C02-08) closed; a second, Perron-Frobenius proof of the critical-rule theorem supplied (Appendix A) and simulated on 668,793 aperiodic critical rules.

*Evidence:* CLM-C02-07, CLM-C02-08, CLM-C02-04, CLM-C02-11, reviews/skeptic_C01_C02.md

### [2026-10-18T08:39:48Z] Formal Verifier — decision (`C02-17`)

Checked the Skeptic's Appendix A line by line (monotone minorant F(x) >= Ax - b, primitivity from cycle lengths with gcd 1, domination of T after N steps) - correct; added as Theorem 10 of proofs/paper/C02.md. Regenerated EXP-C02-03 with the committed script (rows identical, only the stale summary text changed; provenance issue C4 of the review).

*Evidence:* proofs/paper/C02.md, EXP-C02-03, CLM-C02-05


## C06

### [2026-10-18T08:45:16Z] Mathematical Inventor — hypothesis (`C06-01`)

Anchor a single invented operation to the successor (x*0 = x+1) and impose one composition law. H-C06-1 - left-distributivity then has exactly one model for N in {1, 2, 4, 8} (Laver tables). H-C06-2 (bold) - such restricted spectra are special to left-distributivity.

*Evidence:* EXP-C06-01, EXP-C06-02

### [2026-10-18T08:45:16Z] Mathematical Explorer — result (`C06-02`)

EXP-C06-02 confirmed H-C06-1 with an independent SAT encoding (LD only at 1, 2, 4, 8 for N <= 10) and produced exact model counts - one for associativity and right-distributivity at every N, N^(N-1) for right-permutability, 1, 2, 9, 94, 1486 for left-permutability.

*Evidence:* EXP-C06-02

### [2026-10-18T08:45:16Z] Formal Verifier — decision (`C06-03`)

Stopped the first EXP-C06-02 run after 27 minutes - it computed an unused isomorphism-class count with 8! permutations per table. Anchored structures have only the identity as anchored isomorphism, so tables are counted directly (53 s).

*Evidence:* EXP-C06-02

### [2026-10-18T08:45:16Z] Mathematical Skeptic — result (`C06-04`)

EXP-C06-03 refuted H-C06-2 - of 382 laws, 22 have restricted anchored spectra and only one is LD. Spectra {1,2}, {1,3}, {1,5}, odd numbers.

*Evidence:* EXP-C06-03, CLM-C06-04

### [2026-10-18T08:45:16Z] Formal Verifier — proof (`C06-05`)

Hand analysis of the restricted laws - substituting z = 0 in (xy)z = x((yz)z) gives x*(y+2) = x*y + 1, forcing odd N and x*y = x + 1 + y/2; in (xy)z = x(y(zz)) it gives x*(y*1) = x*y + 1, which forces x*y = x + 1 + kappa(y) and then kappa linear with a^2 + a = 1 - a golden-ratio spectrum. Both now proved (odd law also in Lean).

*Evidence:* CLM-C06-06, CLM-C06-07, proofs/paper/C06.md

### [2026-10-18T08:45:16Z] Mathematical Explorer — result (`C06-06`)

EXP-C06-04 tested the predictions - golden law model counts 1, 1, 2 at N = 1, 5, 11 and 0 otherwise for N <= 12, exactly the root counts; odd law one model at each odd N <= 11. The broader H-C06-3 (all spectra are affine spectra) is refuted by six laws with non-affine models.

*Evidence:* EXP-C06-04, CLM-C06-09

### [2026-10-18T08:45:16Z] Historian — novelty (`C06-07`)

OEIS - left-permutable counts 1, 2, 9, 94, 1486 match A058156 (commutative monoids with fixed identity), explained by Theorem 7 (centraliser argument); golden spectrum = A089270, golden counts = A087781. Literature - the LD case is Laver's theorem (Drapal's elementary proof; Dehornoy's book); no prior statement of the odd, golden or left-permutable correspondences found.

*Evidence:* CLM-C06-01, CLM-C06-07, CLM-C06-08

### [2026-10-18T08:45:16Z] Formal Verifier — proof (`C06-08`)

Lean file C06_Laver.lean extended - anchored_rd_unique, the odd law (no even sizes, unique formula, existence) and the left-permutable structure theorem (a pairwise commuting family that reaches every point from e exactly once is closed under composition and contains the identity); all with standard axioms only.

*Evidence:* proofs/lean/Infinity/C06_Laver.lean, CLM-C06-03, CLM-C06-06, CLM-C06-08

### [2026-10-18T08:46:39Z] Mathematical Inventor — result (`C06-09`)

Answered the cycle's own question 'can a spectrum be the primes?' - no, since direct products transported along the Chinese remainder isomorphism keep the anchor, every anchored spectrum is closed under coprime products (Theorem 8). Divisor-closure is observed in all examples but unproved.

*Evidence:* CLM-C06-12


## C11

### [2026-10-18T08:50:02Z] Mathematical Inventor — hypothesis (`C11-01`)

Read the Fibonacci code as "the words in which 11 occurs first at the end" and replaced 11 by any terminator p:
the family T_p, encoded enumeratively with a KMP automaton. Bold guess H-C11-2: the all-ones terminator 1^k is
the best length-k terminator beyond small n.

*Evidence:* CLM-C11-05, CLM-C11-01

### [2026-10-18T08:50:02Z] Formal Verifier — failure (`C11-02`)

The first EXP-C11-01 runs failed for test-design reasons, not code errors: growth-rate-1 patterns (10, 01) could
not reach 2^60 within the table (ValueError), a monotonicity check on an unsorted value list produced 70 false
problems, and Kraft partial sums at L <= 120 were only 0.865 for 00000 (expected waiting time 62). Fixed the
tests and kept the runs; a later fix of an inaccurate assumption string (61, not 62, pattern codes) reproduced
the result hash.

*Evidence:* EXP-C11-01

### [2026-10-18T08:50:02Z] Mathematical Explorer — proof (`C11-03`)

1^k and 0^k maximise the growth rate for all 2044 patterns of length 2..10; proved in general from
D_(1^k) - D_p = (1 - 2x)(c_(1^k) - c_p) <= 0 for x > 1/2.

*Evidence:* CLM-C11-02, EXP-C11-02

### [2026-10-18T08:50:02Z] Mathematical Skeptic — rejection (`C11-04`)

H-C11-2 rejected: maximal growth rate does not mean shortest codewords at practical sizes. At n = 1000 the
terminators 1000, 1001, 1010 beat 1111 by one bit, and for k = 6 rivals still win at n near 1.3e19.

*Evidence:* CLM-C11-05, EXP-C11-02

### [2026-10-18T08:50:02Z] Mathematical Explorer — surprise (`C11-05`)

Unbordered terminators have exactly the partial sums of the all-ones counts (x/(1-x) identity), so T_011 is one
bit shorter than the Fibonacci code on 1,999,568 of the first 2e6 integers and longer only at n = 1, 2, 4.

*Evidence:* CLM-C11-03, CLM-C11-04, EXP-C11-06

### [2026-10-18T08:50:02Z] Mathematical Explorer — failure (`C11-06`)

Two predictions of the average gain failed: log_lambda(1/(lambda-1)) (0.2875 predicted, 0.2282 measured for
k = 3), then convergence to (2-lambda)/(lambda-1)^2 (0.228, 0.310, 0.229 at 2^40, 2^80, 2^120).

*Evidence:* CLM-C11-06, EXP-C11-06, EXP-C11-07

### [2026-10-18T08:50:02Z] Formal Verifier — proof (`C11-07`)

Proved the oscillation (Proposition 5: liminf (2-lambda)/(lambda-1)^2, limsup lambda(2-lambda)/(lambda-1)),
confirmed to 6 digits for k = 2..6; Lean proofs of prefix-freeness and unique parsing of every T_p (no axioms).

*Evidence:* CLM-C11-07, CLM-C11-01, EXP-C11-08

### [2026-10-18T08:50:02Z] Application Researcher — result (`C11-08`)

Benchmarks with exact expectations: a fixed pattern code is the best fixed universal code on 5/12 synthetic
sources and on both posting lists; tuned Golomb wins every geometric source and tuned Golomb/Exp-Golomb every
uniform one; pattern codes are 4-10 times slower in CPython. A draft sentence claiming that pattern codes beat
tuned Golomb on every non-geometric source was false (uniform sources) and was corrected before recording.

*Evidence:* CLM-C11-08, EXP-C11-03, EXP-C11-04, EXP-C11-05

### [2026-10-18T08:50:02Z] Historian and Novelty Analyst — novelty (`C11-09`)

T_11 and T_(1^k) are the Fibonacci codes of Apostolico-Fraenkel (1987) and Fraenkel-Klein (1996); the generating
function and the correlation ordering are Guibas-Odlyzko (1981); counts are in the OEIS. Fraenkel-Klein's C3
(1996) is the closest prior art for T_011: it already improves C1 using the pattern 011, but is not prefix-free.
Corollaries 4 and 6 and Proposition 5 were not found: potentially novel, low confidence.

*Evidence:* CLM-C11-01, CLM-C11-02, CLM-C11-04, CLM-C11-07, CLM-C11-09

### [2026-10-18T08:50:02Z] Mathematical Skeptic — review (`C11-10`)

Demanded C3 as a baseline (EXP-C11-09). T_011 beats C3 except at n = 2, 4, 8, but those three values let C3 beat
T_011 on 7 light-tailed sources and data sets; with C3 included, the margin of pattern codes over the best
classical code shrinks from 0.58-3.06 to 0.34-3.06 bits per value. The improvement claim stays MIXED.

*Evidence:* CLM-C11-09, CLM-C11-08, EXP-C11-09

### [2026-10-18T08:50:02Z] Research Director — direction (`C11-11`)

Recommend T_0111 or T_101 for heavy-tailed integer streams of unknown scale, Golomb-Rice for geometric gaps and
gamma, Fibonacci or C3 for small values. Open: table-driven decoders, multi-pattern terminators, robustness.

*Evidence:* CLM-C11-08


## C12

### [2026-10-18T08:50:02Z] Mathematical Inventor — hypothesis (`C12-01`)

Bold guesses H-C12-1 (Grundy values of divisibility and coprimality games depend only on the prime signature) and H-C12-2 (sparse move sets keep a positive density of P-positions, as powers of k do).

*Evidence:* CLM-C12-10, CLM-C12-11

### [2026-10-18T08:50:02Z] Mathematical Explorer — experiment (`C12-02`)

Census of 19 relational one-heap games - 5 eventually periodic, 14 not within range; recognisable values v2, v2 + 1, Omega, smallest-prime index, popcount and logarithmic step functions.

*Evidence:* EXP-C12-01, CLM-C12-09

### [2026-10-18T08:50:02Z] Mathematical Skeptic — failure (`C12-03`)

The first census reported a period for subtract-a-Fibonacci with preperiod 99970 and constant tails for the logarithmic games - end-of-range artefacts. The detector now requires the periodic tail to cover half the range; the census was re-run and both runs are kept.

*Evidence:* EXP-C12-01

### [2026-10-18T08:50:02Z] Formal Verifier — proof (`C12-04`)

Lean - uniqueness of Grundy functions, the residue lemma (powers of 2 give n mod 3), the splitting parity theorem and the P-positions of G03, all with standard axioms and no sorry. Written proofs for the divisibility, coprimality, bitwise and quotient games.

*Evidence:* CLM-C12-01, CLM-C12-02, CLM-C12-03, CLM-C12-05, CLM-C12-06, CLM-C12-07

### [2026-10-18T08:50:02Z] Mathematical Explorer — result (`C12-05`)

Both bold hypotheses fail - n = 2 and 3 already separate a signature class in G01, and the P-density of subtract-a-square falls from 0.0538 to 0.0222; the Furstenberg-Sarkozy theorem shows it must tend to 0.

*Evidence:* EXP-C12-05, EXP-C12-03, CLM-C12-10, CLM-C12-11, CLM-C12-08

### [2026-10-18T08:50:02Z] Historian and Novelty Analyst — novelty (`C12-06`)

OEIS - only G03 matches nothing. The G10c hit (shifted window of A014586) is spurious; G19 is A099396 shifted by one; G06 is exactly A279119.

*Evidence:* EXP-C12-04

### [2026-10-18T08:50:02Z] Historian and Novelty Analyst — novelty (`C12-07`)

G03 is Codeforces 1537D "Deleting Divisors" (2021) - its P-positions are the official solution, so CLM-C12-03 is downgraded from potentially novel to rediscovery. Iannucci and Larsson (2021) already contain G02, G04, G05, G06 (values plus one) and G19 (Theorem 12, proof left to the reader).

*Evidence:* CLM-C12-03, CLM-C12-01, CLM-C12-02, CLM-C12-05

### [2026-10-18T08:50:02Z] Mathematical Explorer — surprise (`C12-08`)

The Grundy values of G03 equal v2(n) except on numbers with odd part at most 15 (96 exceptions up to 1e5) - forbidding "subtract 1" perturbs G01 only on a thin, explicitly describable set, with eventual shifts -2, +2, +1 and -1.

*Evidence:* EXP-C12-06, CLM-C12-04

### [2026-10-18T08:50:02Z] Formal Verifier — proof (`C12-09`)

Theorem 8 proved computer-assisted - exact base range n <= 1e5, written induction for odd parts >= 17, shift invariance plus a finite certificate for odd parts <= 15 (0 failures for a <= 100), 0 failures in 4000 random mex checks. Flagged for Skeptic review.

*Evidence:* CLM-C12-04, EXP-C12-06

### [2026-10-18T08:50:02Z] Mathematical Skeptic — decision (`C12-10`)

H-C12-0 is recorded as inconclusive, not refuted - its "closed form" clause is not falsifiable; only the periodic alternatives are excluded, by proof, for squares and triangular numbers.

*Evidence:* CLM-C12-09, CLM-C12-08

### [2026-10-18T08:50:02Z] Application Researcher — result (`C12-11`)

Theorem 8 solves sums of deleting-divisors heaps by XOR of closed-form values; beyond recreational and competitive-programming games no application was found, and no performance improvement is claimed.

*Evidence:* CLM-C12-04

### [2026-10-18T08:50:02Z] Historian and Novelty Analyst — novelty (`C12-12`)

The bound 11 for subtract-a-prime is documented in OEIS A014589 up to 1e9 (Huet 2022, Dobbelaere 2024), so CLM-C12-12 is a weak rediscovery; the Fibonacci bound (CLM-C12-13) was not found in the entries read.

*Evidence:* CLM-C12-12, CLM-C12-13


## C07

### [2026-10-18T09:13:45Z] Mathematical Inventor — hypothesis (`C07-01`)

Operations defined only by exclusion - f(a,b) is the least value not produced by earlier entries - form a 512-member family containing Conway's nim-sum and nim-product. H-C07-1 (bold) - these two are the only non-trivial associative members. H-C07-2 (bold) - commutative members are closed on the Fermat segments like the nimbers.

*Evidence:* EXP-C07-01

### [2026-10-18T09:13:45Z] Mathematical Explorer — result (`C07-02`)

EXP-C07-01 - 134 distinct operations, 11 associative - 0, projections, a[b>0], b[a>0], min, +, XOR, nim-product and zero-absorbing shifts of XOR and +. Ordinary addition and min arise from mex as well, refuting H-C07-1; H-C07-2 fails for 30 of 34 commutative operations.

*Evidence:* EXP-C07-01, CLM-C07-01, CLM-C07-02, CLM-C07-04

### [2026-10-18T09:13:45Z] Formal Verifier — decision (`C07-03`)

Found and fixed a bug before it affected any recorded result - in systems/mex.table the loop variable over D-masks shadowed the column count m of the new rectangular mode, truncating rows. EXP-C07-01/02 used the square mode (unaffected); the fix was regression-tested against the plain implementation.

*Evidence:* EXP-C07-03

### [2026-10-18T09:13:45Z] Mathematical Explorer — result (`C07-04`)

Row 2 of D[x^y] is not additively periodic - f(2,b) - b takes the values +-1, +-3, +-5, +-11, +-21, ..., the Jacobsthal numbers, in blocks of the same lengths. Verified for b < 2^15 with an independent algorithm (EXP-C07-03).

*Evidence:* EXP-C07-03

### [2026-10-18T09:13:45Z] Formal Verifier — proof (`C07-05`)

Proved the Jacobsthal row (Theorem 3) - since J_(k+1) + J_k = 2^k, the row swaps [2^k - J_k, 2^k) with [2^k, 2^k + J_k); each step of the induction reduces to a bit estimate (x XOR (x + c) > x for c > x; J_k < 2^(k-1) < J_(k+1)). The theorem refutes the bold additive-periodicity hypothesis H-C07-4 rigorously.

*Evidence:* CLM-C07-05, CLM-C07-06, proofs/paper/C07.md

### [2026-10-18T09:13:45Z] Historian — novelty (`C07-06`)

Nim-sum and nim-product are Conway's; + and min are rank functions of product posets (folklore in combinatorial game theory). No OEIS entry for the Jacobsthal row or for 88 further sequences of the census; no prior mex recursion of the D[x^y] form found.

*Evidence:* CLM-C07-01, CLM-C07-05, CLM-C07-07


## C14

### [2026-10-18T09:13:45Z] Mathematical Inventor — hypothesis (`C14-01`)

Opened C14 (System D): treat graphs as the quantities and the 256 local products as candidate multiplications. Bold hypotheses: H-C14-1 (isomorphism-level associativity is no weaker than strict), H-C14-3 (unique factorisation for all six commutative unital associative products on connected or co-connected graphs), H-C14-4 (two-graphs factor uniquely under xor).

*Evidence:* EXP-C14-01, EXP-C14-02

### [2026-10-18T09:13:45Z] Formal Verifier — proof (`C14-02`)

Reduced associativity to a 27-entry identity on relations and proved in Lean that P3 x P3 x P3 detects every failure (both directions, arbitrary vertex types); the count 20/10 then follows by kernel computation.

*Evidence:* CLM-C14-01, CLM-C14-02

### [2026-10-18T09:13:45Z] Historian and Novelty Analyst — novelty (`C14-03`)

The count of 20 associative products is Imrich-Izbicki (1975); Nowakowski-Rall (1996) report 10 depending on both factors, 8 of them commutative - our classification reproduces both numbers exactly.

*Evidence:* CLM-C14-02

### [2026-10-18T09:13:45Z] Mathematical Explorer — result (`C14-04`)

H-C14-1 survives: all 236 non-associative and 224 non-commutative products are already caught by factors with at most 3 vertices, and the degree sequences alone certify every witness.

*Evidence:* EXP-C14-02, CLM-C14-03

### [2026-10-18T09:13:45Z] Formal Verifier — surprise (`C14-05`)

Solving the character equations shows that the commutative associative products are exactly the products linearised by I, A and J: six multiplicative (Kronecker) and two additive (Kronecker sum). For the symmetric difference the character is S(G) + I - the symmetric difference is the Kronecker product of Seidel matrices and therefore acts on two-graphs.

*Evidence:* EXP-C14-03, CLM-C14-04, CLM-C14-05, CLM-C14-06

### [2026-10-18T09:13:45Z] Mathematical Skeptic — rejection (`C14-06`)

H-C14-3 refuted by the symmetric difference: K2 xor K2 xor K2 = K2 xor K_{1,3} (connected, order 8), and in all graphs C4 = K2 xor K2 = K2 xor 2K1. Cause: K2 absorbs Seidel switching, and C4 ~ K_{1,3}.

*Evidence:* EXP-C14-04, CLM-C14-08, CLM-C14-07

### [2026-10-18T09:13:45Z] Mathematical Explorer — pattern (`C14-07`)

Complete bipartite graphs under xor behave like split-complex numbers: K_{a,b} xor K_{c,d} = K_{ac+bd, ad+bc}, i.e. order and imbalance multiply - the order-15 collision 3K1 xor K_{2,3} = K_{1,2} xor K_{1,4} is (3,3)(5,1) = (3,1)(5,3).

*Evidence:* CLM-C14-07, EXP-C14-04

### [2026-10-18T09:13:45Z] Mathematical Explorer — surprise (`C14-08`)

On the level the product actually sees - two-graphs - every factorisation up to order 16 is unique, and on co-connected graphs (product 141 on connected graphs) none collide up to order 15. H-C14-4 survives as a conjecture.

*Evidence:* EXP-C14-05, CLM-C14-12, CLM-C14-13

### [2026-10-18T09:13:45Z] Historian and Novelty Analyst — novelty (`C14-09`)

The connected Cartesian prime counts are OEIS A129582 (Ji Li 2007) for every n <= 15, which also validates the census pipeline; the strong product gives identical counts because both monoids are polynomial semirings in their connected primes. No source found for the Seidel-Kronecker identity of the symmetric difference beyond the edgeless-factor special case.

*Evidence:* CLM-C14-09, CLM-C14-06

### [2026-10-18T09:13:45Z] Application Researcher — result (`C14-10`)

Spectra of products from factors via the characters: exact to 1.2e-14 and orders of magnitude faster than diagonalising the product (standard Kronecker gain). Squaring the 6-point regular two-graph gives 36 equiangular lines in R^18 - no improvement (36 lines exist already in R^15; 57 <= N(18) <= 59).

*Evidence:* EXP-C14-07

### [2026-10-18T09:13:45Z] Mathematical Skeptic — review (`C14-11`)

Independent re-implementation (no shared code) reproduced the classification, all 460 witnesses, the explicit xor isomorphisms, the bipartite formula, the Seidel identity in exact integers and K2-absorption; the census pipeline was validated against A129582 and A002854.

*Evidence:* EXP-C14-06


## C05

### [2026-10-18T09:23:59Z] Mathematical Inventor — hypothesis (`C05-01`)

Opened Branch B with the bold H-C05-1 - a single identity t = x cannot restrict the sizes of its finite models - and H-C05-Q (nontrivial identities force quasigroups).

*Evidence:* CLM-C05-01, CLM-C05-03

### [2026-10-18T09:23:59Z] Formal Verifier — infrastructure (`C05-02`)

Built systems/magma.py with an exact SAT encoding of identities (value variables per subterm and assignment); model counts agree with brute force on all magmas of orders 2 and 3 for four identities.

*Evidence:* systems/magma.py

### [2026-10-18T09:23:59Z] Mathematical Explorer — surprise (`C05-03`)

An exploratory scan showed 11 different spectrum patterns on n <= 6, including {1,3,4} (Mendelsohn-like), {1,3} (Steiner-like) and 'all but 2 and 6' (Euler's 36 officers pattern). H-C05-1 was clearly false.

*Evidence:* EXP-C05-01

### [2026-10-18T09:23:59Z] Historian and Novelty Analyst — novelty (`C05-04`)

Found that the Equational Theories Project already studied spectra of order <= 4 laws - the write-up 'Spectra of order-3 equations' (laws 66 Mendelsohn, 167 mod 4, 168 squares) and B. Le Floch's notes listing 48 laws with possibly non-full spectrum. The census became a rediscovery; the cycle pivoted to pushing the open cases.

*Evidence:* CLM-C05-02, CLM-C05-04

### [2026-10-18T09:23:59Z] Formal Verifier — proof (`C05-05`)

Lean-verified that every finite model of x = (yx)(xy) has order 0 or 1 mod 4 (pair map {a,b} -> {ab, ba} is a fixed-point-free involution on Sym2), plus certified models of orders 4 and 5.

*Evidence:* CLM-C05-04, proofs/lean/Infinity/C05_Magmas.lean

### [2026-10-18T09:23:59Z] Mathematical Skeptic — rejection (`C05-06`)

H-C05-Q rejected - the SAT model of law 167 of order 4 has a repeated entry in a row (Lean T4_not_latin); 18 census identities have non-quasigroup models of order <= 3.

*Evidence:* CLM-C05-03

### [2026-10-18T09:23:59Z] Mathematical Inventor — hypothesis (`C05-07`)

Proposed H-C05-A - full spectra are exactly explained by affine models over Z_n.

*Evidence:* CLM-C05-06

### [2026-10-18T09:23:59Z] Mathematical Skeptic — rejection (`C05-08`)

H-C05-A rejected - x = (yx)(x(yy)) is satisfied by NAND on two elements but by no affine operation over Z_2 (both facts Lean-certified); four identities in total.

*Evidence:* CLM-C05-06, EXP-C05-05

### [2026-10-18T09:23:59Z] Research Director — decision (`C05-09`)

Two long runs were stopped and rescoped under heavy shared CPU load (other cycles running in parallel): the census to n <= 6 (n = 7 UNSAT instances dominated) and the frontier push to n <= 10 with budget 1e6 (n = 11, 12 would likely have hit the timeout and lost all results, since the runner writes results only at the end). Lesson: long experiments should checkpoint partial results.

*Evidence:* EXP-C05-01, EXP-C05-03

### [2026-10-18T09:23:59Z] Formal Verifier — result (`C05-10`)

Frontier push agreed with every size stated in the ETP notes (0 disagreements) and settled new sizes - memberships 467 (9), 677 (5, 7, 9), 1286 (9), 1313 (9), 1516 (9), all Lean-certified; gaps 501 (6, 7), 677 (6), 883 (6), 1076 (8), 1083 (5, 6), all with drat-trim-verified DRUP proofs (48/48 refutations verified).

*Evidence:* CLM-C05-07, CLM-C05-08, EXP-C05-03, EXP-C05-04, EXP-C05-06

### [2026-10-18T09:23:59Z] Mathematical Skeptic — review (`C05-11`)

Caveats recorded - EXP-C05-02's 'identical model set' grouping compared non-canonical representatives (count not used); the field decided_beyond_notes over-counts because the notes' 'starting with' phrasing implicitly settles smaller sizes; most census non-memberships are solver-trusted; novelty of the frontier facts is relative to the notes and to a partially read ETP paper.

*Evidence:* EXP-C05-02, EXP-C05-03

### [2026-10-18T09:23:59Z] Mathematical Explorer — pattern (`C05-12`)

Laws 677 and 1313 share the spectrum fragment 1, 5, 7, 9 (not 2, 3, 4, 6) with idempotent quasigroup models; conjectured spectrum {1} plus odd n >= 5 (CLM-C05-09), pending orders 8 and 10.

*Evidence:* CLM-C05-09


## C17

### [2026-10-18T09:24:11Z] Application Researcher — hypothesis (`C17-01`)

Phase-5 cycle - can the lab's structural insights make law testing faster than the exhaustive n^3 check? Baselines: exhaustive check (vectorised), random triples; methods: Light's generator test, the anchored O(n^2) identity (from C06), the Rajagopalan-Schulman randomised test. Primary metric - exact table probes (the machine is shared); times secondary.

*Evidence:* EXP-C17-01

### [2026-10-18T09:24:11Z] Application Researcher — result (`C17-02`)

EXP-C17-01 - all exact tests correct; up to 614x fewer probes with Light's test, but only 1.7x on left-zero bands (H-C17-1 refuted); random-triple sampling misses 27 of 30 near-associative inputs, the randomised GF(2) test none.

*Evidence:* EXP-C17-01, CLM-C17-04, CLM-C17-06

### [2026-10-18T09:24:11Z] Mathematical Skeptic — result (`C17-03`)

EXP-C17-02 refuted the bold H-C17-2 (18 laws whose anchor instance admits non-models) and, as a by-product, showed that the cited form of Laver's theorem in the C06 record was imprecise - with the wrap-around instance there are no solutions for N = 3, 5, 6, 7, 9, 10. The C06 record was corrected.

*Evidence:* EXP-C17-02, CLM-C17-05, CLM-C17-07, CLM-C06-01


## C03

### [2026-10-18T16:49:32Z] Mathematical Skeptic — review (`C03-13`)

Independent review (reviews/skeptic_C03_C04_C06.md) - no claim refuted; 76 loops and 218 matrix certificates re-verified with independent code; H-C03-2 has 40 counterexamples with parameters <= 5 (not 35); the 24 open rules still have no loop; base-family loops extended to q = 7.

*Evidence:* CLM-C03-06, CLM-C03-08, CLM-C03-10, reviews/skeptic_C03_C04_C06.md

### [2026-10-18T16:49:32Z] Formal Verifier — correction (`C03-14`)

Correction of journal entry C03-11 - the larger matrix-interpretation tiers it mentions (upper-triangular d = 3 entries <= 5, d = 4 entries <= 2, full d = 3 entries <= 1) were searched outside the committed experiments and are not reproducible from the repository; only the tiers listed in the README are recorded evidence. The claim records do not rely on the unrecorded searches.

*Evidence:* reviews/skeptic_C03_C04_C06.md


## C04

### [2026-10-18T16:49:32Z] Mathematical Skeptic — review (`C04-16`)

Independent review - all C04 claims upheld; written proofs of CLM-C04-06/09/10/13 checked (CLM-C04-10 needs n >= 1, now stated); Lean p_positions covers the kernel property, the rest of CLM-C04-04 is written; no loop or matrix interpretation for the open rules.

*Evidence:* CLM-C04-04, CLM-C04-10, reviews/skeptic_C03_C04_C06.md

### [2026-10-18T16:49:32Z] Formal Verifier — decision (`C04-17`)

CLM-C04-03 (termination of aab -> ababa, aab -> babaa) upgraded to PROVEN by the proofs of cycle C20; the same theorems give exponential complexities 2^(n-2) - 1 and max_b b(2^floor((n-b)/2) - 1).

*Evidence:* CLM-C04-03, CLM-C20-01, CLM-C20-02


## C05

### [2026-10-18T16:49:32Z] Historian and Novelty Analyst — revision (`C05-13`)

Re-reading Le Floch's notes while writing the textbook chapter found statements missed in the first pass: the list of 31 laws without models of order 2 (incl. 501, 677, 1083, 1719), the list of 14 laws with order-2 but no order-3 models (incl. 883), and the Gaussian-integer models of law 467, which include order 9 = 3^2 + 0^2. CLM-C05-07 no longer counts 467 (order 9) as new, CLM-C05-08 separates new gaps from gaps stated in the notes, and the README frontier table was corrected (1719 has no new facts). Entry C05-10 overstated these points.

*Evidence:* CLM-C05-07, CLM-C05-08


## C06

### [2026-10-18T16:49:32Z] Mathematical Skeptic — review (`C06-10`)

Independent review - all C06 claims upheld; golden-law counts confirmed by complete enumeration for N <= 17 and N = 19; finite spectra (CLM-C06-10) survive to N = 16; mirror twins (CLM-C06-11) to N = 13; right-permutable count 7776 at N = 6; CLM-C06-12 reworded.

*Evidence:* CLM-C06-07, CLM-C06-10, CLM-C06-11, CLM-C06-12, reviews/skeptic_C03_C04_C06.md

### [2026-10-18T16:49:32Z] Formal Verifier — correction (`C06-11`)

EXP-C06-03 and EXP-C06-04 stored a wall-clock runtime inside the hashed results, so every re-run looked like a changed result; the audit-log entry 'reproduced: false' for EXP-C06-03 (skeptic re-run) reflects only that time stamp. The runtime now lives under 'timings' and both experiments were re-run.

*Evidence:* EXP-C06-03, EXP-C06-04


## C20

### [2026-10-18T16:49:32Z] Mathematical Inventor — hypothesis (`C20-01`)

Open problem from C04 - the 8 rules aab -> ababa, aab -> babaa (and images) were neither shown to loop nor certified terminating. Idea - aab is unbordered, so random descent reduces termination to ONE strategy; in the run encoding the rightmost strategy moves a single surplus a (resp. a pair) to the right until it is absorbed.

*Evidence:* CLM-C04-03

### [2026-10-18T16:49:32Z] Formal Verifier — proof (`C20-02`)

Proved termination of both rules (journeys are finite, the number of journeys is bounded) and the exact complexities - a journey at most doubles the number of b's, which gives 2^(n-2) - 1 for aab -> ababa and max_b b(2^floor((n-b)/2) - 1) for aab -> babaa, both attained.

*Evidence:* CLM-C20-01, CLM-C20-02, proofs/paper/C20.md

### [2026-10-18T16:49:32Z] Mathematical Explorer — result (`C20-03`)

EXP-C20-01 - no counterexample on all words of length <= 12 for all 8 rules; strategy independence holds exactly; both closed forms and the per-word formula match.

*Evidence:* EXP-C20-01

### [2026-10-18T16:49:32Z] Historian — novelty (`C20-04`)

Both rules are right barren (McNaughton; Geser, ICASE 2002-33, Thm 3.2-3.3), so their termination was already known in principle - recorded as a rediscovery; the exact complexities were not found. The Zantema-Geser characterisation for C03 could not be retrieved (403/500/Cloudflare) - C03 Conjecture 4.6 stays unverified against it.

*Evidence:* CLM-C20-01, CLM-C20-02, CLM-C20-04

