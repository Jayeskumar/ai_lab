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


## C15

### [2026-10-18T16:55:13Z] Mathematical Inventor — hypothesis (`C15-01`)

A binary operation is also a cellular automaton - c'_i = c_i * c_{i+1}. Measure how hard its t-step map is by the streaming width (ordered-BDD width) of F_t. Bold guesses - H-C15-1, widths are bounded or geometric; H-C15-2, bounded width exactly for semigroups, affine magmas and bounded light cones; H-C15-4, fast-forwardable iff bounded width.

*Evidence:* EXP-C15-02

### [2026-10-18T16:55:13Z] Mathematical Explorer — result (`C15-02`)

Order 2 calibrates - the 16 automata are the elementary rules 17m and all have width <= 3. Order 3 (1734 classes) - bounded 808, linear 104, geometric 300, irregular 522 on t <= 9; surjective exactly when permutive (43 classes); 7 reversible automata.

*Evidence:* EXP-C15-01, EXP-C15-02

### [2026-10-18T16:55:13Z] Formal Verifier — proof (`C15-03`)

The simplest linear-width magma is a burning fuse - 0 burnt, 1 burning, 2 intact. Burn times satisfy tau_i = tau_(i+1) + 2 along runs of 2s, so F_t compares t with a counter - width between ~t/4 and 3t + 3 (proved), t + 2 computed. The same burn times give an O(L) fast-forward, refuting both the width dichotomy and 'fast-forwardable iff bounded width'.

*Evidence:* CLM-C15-04, CLM-C15-08, CLM-C15-10, proofs/paper/C15.md

### [2026-10-18T16:55:13Z] Mathematical Skeptic — result (`C15-04`)

Bounded width is far more common than structure - 685 bounded-width classes are neither semigroups, affine magmas nor bounded light cones (e.g. a reversible automaton with a full light cone), so H-C15-2 is refuted. Bounded width also does not mean short cycles - the affine quasigroups mod 3 have long ones.

*Evidence:* CLM-C15-09, CLM-C15-11

### [2026-10-18T16:55:13Z] Application Researcher — result (`C15-05`)

Fast-forwards against direct simulation - affine operator powers and fuse burn times are exact and up to ~2500x / ~4000x faster at t = 10^5 (L = 1024); exponent arithmetic for commutative semigroups wins only for t >> L and loses near t = 10^3; cycle detection is generic but fails exactly where cycles are long. Timings indicative (shared machine).

*Evidence:* EXP-C15-03, EXP-C15-04, CLM-C15-13, CLM-C15-14, CLM-C15-15, CLM-C15-16

### [2026-10-18T16:55:13Z] Historian — novelty (`C15-06`)

The magma-automaton framework is Pedersen's (Complex Systems 1992) and Moore's (Moore-Drisko 1995/96, Moore-Pnin 1997); linear CA theory is Martin-Odlyzko-Wolfram (1984); surjective two-neighbour automata over prime alphabets are permutive (Kari-Salo-Torma 2013), which our exhaustive order-3 check confirms independently. No prior notion of streaming width or analysis of the fuse rule was found.

*Evidence:* CLM-C15-01, CLM-C15-02, CLM-C15-05, CLM-C15-07

### [2026-10-18T16:55:13Z] Formal Verifier — proof (`C15-07`)

Lean file C15_MagmaCA.lean - ca_comm_binomial (Pascal exponents in commutative monoids) and ca_step_shift (local maps compose like the global map), standard axioms only.

*Evidence:* proofs/lean/Infinity/C15_MagmaCA.lean, CLM-C15-01


## C18

### [2026-10-18T16:55:13Z] Application Researcher — hypothesis (`C18-01`)

Phase-5 cycle - can invented operations (Latin squares, the nimber field of C07, the anchored quasigroups of C06) serve as non-cryptographic hash mixers? Baselines FNV-1a-64, MX64, BLAKE2b-64, CRC32. Bold hypotheses - H-C18-1 (random Latin square, 2 passes + reverse, BLAKE2b-level avalanche), H-C18-2 (structured quasigroups worse), H-C18-3 (the nimber hash competitive with FNV-1a). Explicitly not a security evaluation.

*Evidence:* EXP-C18-02, EXP-C18-03

### [2026-10-18T16:55:13Z] Formal Verifier — proof (`C18-02`)

Before measuring - proved bijectivity of e-transformations (Lean), forward-only propagation of differences (Lean) and its consequence for forward-only tail hashes, the T-function obstruction (affine mod 256, XOR, (x + 1) XOR y) and the GF(2)-affinity of XOR hashes; EXP-C18-01 confirmed every prediction on random inputs.

*Evidence:* EXP-C18-01, CLM-C18-01, CLM-C18-02, CLM-C18-04, CLM-C18-05

### [2026-10-18T16:55:13Z] Mathematical Explorer — result (`C18-03`)

EXP-C18-02 - the random-Latin-square, group-isotope and nimber-inversion hashes with a reverse pass reach BLAKE2b's avalanche noise floor (H-C18-1 holds), FNV-1a does not (max bias 0.5); x + c(y) has ideal flip rates but bit independence 1.0.

*Evidence:* EXP-C18-02, CLM-C18-08, CLM-C18-06

### [2026-10-18T16:55:13Z] Mathematical Skeptic — result (`C18-04`)

EXP-C18-03 overturned the picture - every reverse-pass variant, including those with perfect avalanche, collides massively on structured keys (32,624 full collisions on near-duplicates). Diagnosed as a theorem rather than a bug - the 8-byte tail of an e-transformation is a function of one state byte and 7 input bytes, so with a reverse pass all keys sharing a 7-byte prefix get at most 256 hash values; the observed collision count is exactly the lower bound 16 x (2295 - 256).

*Evidence:* EXP-C18-03, CLM-C18-03, CLM-C18-10

### [2026-10-18T16:55:13Z] Application Researcher — decision (`C18-05`)

Redesign guided by the theorem - output the final state of 8 parallel passes (a bijectively updated 64-bit state) instead of the tail of one string. EXP-C18-05 - the bound holds exactly on data; QC-LS and QC-ISO pass every quality test; QC-NIMINV keeps a small real bias and QC-ARP improves but does not reach the noise floor (H-C18-8, H-C18-9 refuted).

*Evidence:* EXP-C18-05, CLM-C18-07, CLM-C18-11, CLM-C18-12

### [2026-10-18T16:55:13Z] Application Researcher — result (`C18-06`)

No improvement over the baselines - the good cascades only match MX64 and BLAKE2b in quality and are several times slower; MX64 dominates on every measured axis. Recorded as NO IMPROVEMENT (CLM-C18-13).

*Evidence:* EXP-C18-04, EXP-C18-05, CLM-C18-13

### [2026-10-18T16:55:13Z] Historian — novelty (`C18-07`)

e/d bijectivity is Markovski-Gligoroski-Bakeva (1999); the T-function obstruction is Klimov-Shamir's T-function closure; quasigroup hash designs in the SHA-3 competition (Edon-R, NaSHA) used huge quasigroups in wide-pipe constructions and were attacked (Khovratovich-Nikolic-Weinmann; Ji-Xu-Guan, ePrint 2008/519). No explicit statement of the byte-level tail-information bound was found.

*Evidence:* CLM-C18-01, CLM-C18-03, CLM-C18-04

### [2026-10-18T16:55:13Z] Formal Verifier — decision (`C18-08`)

Housekeeping - the first EXP-C18-03 run failed (synthetic words passed as str instead of bytes) and was fixed; a container restart interrupted the cycle after EXP-C18-01, and EXP-C18-02..05 were run afterwards from the committed scripts; the corrected near-duplicate count in the EXP-C18-03 META (65,280) reproduced the result hash.

*Evidence:* EXP-C18-03


## C03

### [2026-10-18T17:10:10Z] Historian — novelty (`C03-15`)

Found the Zantema-Geser technical report (UU-CS-1994-44) on an older archive host after the usual hosts failed; its Theorem 1.1 is the lab's Conjecture 4.6 verbatim. CLM-C03-10 becomes PROVEN (by literature), H-C03-3 (CLM-C03-09) is refuted by the theorem, and the 24 rules left open all terminate.

*Evidence:* CLM-C03-09, CLM-C03-10, reviews/historian_C03_C10.md


## C04

### [2026-10-18T17:10:10Z] Historian — novelty (`C04-18`)

Audit - most of C04 is classical (Kurth, McNaughton, Zantema-Geser, van Oostrom, Latteux-Roos); the aab -> ba complexity stays potentially novel (low confidence) and the A247983 identity answers a question left open by Kimberling in the OEIS.

*Evidence:* CLM-C04-06, CLM-C04-09, CLM-C04-10, reviews/historian_C03_C10.md


## C06

### [2026-10-18T17:10:10Z] Historian — novelty (`C06-12`)

Audit - CLM-C06-08 (left-permutable <-> commutative monoids) downgraded to a rediscovery in substance (a two-line lemma); the odd and golden laws remain potentially novel (small); spectra closed under products is classical for varieties.

*Evidence:* CLM-C06-08, CLM-C06-06, CLM-C06-07, CLM-C06-12, reviews/historian_C03_C10.md


## C08

### [2026-10-18T17:10:10Z] Historian — contradiction (`C08-09`)

The tribonacci circle product is NOT associative at shift 3 - (10016 o 10016) o 1 = 3414681926 != 3414681924 = 10016 o (10016 o 1), the example by which Ambroz-Frougny-Masakova-Pelantova (2003) refuted Arnoux's conjecture; G(k+1) = G(k) + G(k-2) also fails at s = 10. The lab's random tests up to 10^6 missed both.

*Evidence:* CLM-C08-05, reviews/historian_C03_C10.md

### [2026-10-18T17:10:10Z] Mathematical Skeptic — result (`C08-10`)

EXP-C08-06 re-tested every threshold and the 90 quadratic rows with an exact embedding filter and explicit certificates - four of eight listed thresholds were too small (tribonacci, 4-bonacci, (2,2;1,2), G(k)+G(k-2)); 6 quadratic rows had listed shifts that are certified failures; Conjecture 9.2 survives (no positive-beta row is non-monotone; all 10 non-monotone rows have non-canonical initial values). CLM-C08-05 marked REFUTED, corrected values in CLM-C08-07.

*Evidence:* EXP-C08-06, CLM-C08-04, CLM-C08-05, CLM-C08-07

### [2026-10-18T17:10:10Z] Formal Verifier — revision (`C08-11`)

Lesson recorded for all cycles - random sampling of triples is not a reliable associativity test when failures are rare; use certificate-producing searches (exact embeddings, structured candidates, literature examples) and state 'no failure found' as support only.

*Evidence:* EXP-C08-06


## C09

### [2026-10-18T17:10:10Z] Historian — novelty (`C09-08`)

Audit - the product formula is Lunnon's formula in OEIS A101330 and the norm statement follows from Q(sqrt 5); the window-obstruction density 1/phi^2 and its corollaries remain potentially novel.

*Evidence:* CLM-C09-01, CLM-C09-03, CLM-C09-07, reviews/historian_C03_C10.md


## C10

### [2026-10-18T17:10:10Z] Historian — novelty (`C10-07`)

Audit - missed source: Berthe-Frougny-Rigo-Sakarovitch (Adv. Appl. Math. 2020) on the cost of the successor; under their carry-propagation measure Zeckendorf costs phi^2, under the lab's Hamming measure 2. Claims now state the measure; T_m is OEIS A215005.

*Evidence:* CLM-C10-01, CLM-C10-02, CLM-C10-05, reviews/historian_C03_C10.md


## C13

### [2026-10-18T17:12:39Z] Mathematical Inventor — hypothesis (`C13-01`)

Continue C06 - which sets of integers are anchored spectra? Bold hypotheses - H-C13-1 every spectrum is divisor-closed (all C06 examples are); H-C13-2 laws with infinite non-trivial affine spectra are affinely rigid; H-C13-5 one-variable laws have spectrum {1} or cofinite.

*Evidence:* CLM-C13-07, CLM-C13-08, CLM-C13-09

### [2026-10-18T17:12:39Z] Mathematical Explorer — result (`C13-02`)

EXP-C13-01 - 94,206 laws, 152 distinct affine spectra; every finite one is Div(L); the infinite ones are classical sets (-1, 2, 3 squares; x^2+x+1; golden; cyclotomic conditions), and ~30 cubic/quartic sets are absent from the OEIS.

*Evidence:* EXP-C13-01, CLM-C13-01, CLM-C13-11

### [2026-10-18T17:12:39Z] Mathematical Skeptic — result (`C13-03`)

EXP-C13-02 refuted H-C13-2 - 198 of 199 laws have non-affine models. In the same data x = x(x(xx)) has models at N = 4 but none at N = 2 - H-C13-1 refuted as well; a hand proof and a Lean proof (cube_law_no_two, cubeOp_model) followed.

*Evidence:* EXP-C13-02, CLM-C13-05, CLM-C13-07, CLM-C13-08

### [2026-10-18T17:12:39Z] Formal Verifier — proof (`C13-04`)

Generalised C06's golden-law argument - substituting z = 0 in (xy)z = x V(y,z) gives x*sigma(y) = x*y + 1, which forces a translation table; for V = y W(z) the shift equation forces linearity, giving the W-family theorem. Formalised in Lean for every one-variable term W (inductive type T1), together with C06 Theorem 6 (golden law), which C06 had left as a Lean target.

*Evidence:* CLM-C13-02, CLM-C13-03, proofs/lean/Infinity/C13_Spectra.lean

### [2026-10-18T17:12:39Z] Formal Verifier — proof (`C13-05`)

Two laws of CLM-C06-10 proved in Lean (spectra exactly {1,3} and {1,2}). The hand proofs share a pattern - law instances at small elements, the anchor, functionality of the table - which was automated as offset congruence closure (sound, incomplete); it settles 16 of the 17 laws and 6,912 laws of the 3-variable family, with 0 contradictions in 1,245 SAT checks.

*Evidence:* CLM-C13-04, CLM-C13-06, EXP-C13-08

### [2026-10-18T17:12:39Z] Mathematical Skeptic — result (`C13-06`)

Divisor-closure fails often - 24/253 one-variable laws, 81/300 two-variable laws, 29/150 three-variable laws and 17/80 pairs. H-C13-5 also fails - x = (xx)x has spectrum {1, 2}. Two first runs were stopped for exceeding the time budget (hard UNSAT instances near the conflict limit) and replaced by smaller, documented ones.

*Evidence:* EXP-C13-05, EXP-C13-06, EXP-C13-07, CLM-C13-09

### [2026-10-18T17:12:39Z] Historian — novelty (`C13-07`)

The arithmetic sets are classical (OEIS entries read; quadratic ones are represented-by-a-form sets; roots of the tribonacci polynomial mod p studied by Klaska-Skula and Moree-Noubissie). Spectra of varieties (sets of sizes of finite algebras) are studied in universal algebra (Taylor 1980, 'Maltsev conditions and spectra'; Kearnes); there spectra are closed under all products, whereas anchored spectra are only closed under coprime products. No source realising these sets by single anchored magma laws was found.

*Evidence:* CLM-C13-03, CLM-C13-11

### [2026-10-18T17:12:39Z] Application Researcher — result (`C13-08`)

No application found. The offset closure is a reusable tool for bounding the sizes of finite models of identities with a successor-type constant; it was not benchmarked against general finite-model provers (Mace4, Paradox), so no improvement is claimed.

*Evidence:* CLM-C13-06


## C16

### [2026-10-18T17:12:39Z] Mathematical Inventor — hypothesis (`C16-01`)

In any finite magma the pair (x_{k-1}, x_k) determines x_{k+1} = x_k * x_{k-1}, so every magma carries a Fibonacci dynamics on n^2 states. H-C16-1 (bold) - as for Pisano periods the maximum is at most n^2 - 1 and is reached only by quasigroups. H-C16-4 (bold) - for Laver tables the maximal period is a power of 2.

*Evidence:* EXP-C16-01, EXP-C16-03

### [2026-10-18T17:12:39Z] Mathematical Explorer — result (`C16-02`)

EXP-C16-01 - the maximum is n^2 for n = 2, 3, 4 (x*y = 1 - y has period 4), refuting H-C16-1; the full-period tables number 1, 24, 20736, which identified them as de Bruijn cycles ((n!)^n / n^2). Since every function M x M -> M is a feedback, magma pair maps are exactly order-2 feedback shift registers - much of the general theory is classical.

*Evidence:* EXP-C16-01, CLM-C16-02, CLM-C16-03

### [2026-10-18T17:12:39Z] Mathematical Inventor — hypothesis (`C16-03`)

No full-period table of order <= 4 is a quasigroup, and the quasigroup maximum is n^2 - 1. H-C16-5 (bold) - this holds for all n.

*Evidence:* EXP-C16-01

### [2026-10-18T17:12:39Z] Mathematical Skeptic — result (`C16-04`)

H-C16-5 refuted - exactly 3360 full-period quasigroups of order 5 (two independent methods agree), and examples of every order 6-16. Lexicographic DFS and a SAT encoding fail from n = 9 on within their budgets (EXP-C16-05); seeded random sampling of Latin squares finds examples at rates near 1/n^2.

*Evidence:* EXP-C16-02, EXP-C16-05, CLM-C16-06, CLM-C16-07

### [2026-10-18T17:12:39Z] Formal Verifier — proof (`C16-05`)

A parity obstruction - the pair map factors as a swap of coordinates after fibrewise left translations, so a full period forces prod_b sgn(L_b) = (-1)^((n-1)(n+2)/2). For isotopes of groups of even order this product is always (-1)^(n/2) (Burnside's normal 2-complement), the wrong sign; this explains why sampled isotopes of Z_n were full-period for every odd n and never for even n.

*Evidence:* CLM-C16-04, CLM-C16-09, proofs/paper/C16.md

### [2026-10-18T17:12:39Z] Formal Verifier — proof (`C16-06`)

Laver tables - by Laver's monotonicity x*y > x below the top element, Fibonacci sequences climb to the top and then alternate; the pair map has exactly one fixed point and N - 1 two-cycles. Affine magmas reduce to companion matrices; the anchored associative magma of C06 is the Fibonacci sequence mod N in disguise; nim-multiplication gives Pisano periods of 2^(2^k) - 1.

*Evidence:* CLM-C16-12, CLM-C16-14, CLM-C16-15

### [2026-10-18T17:12:39Z] Application Researcher — result (`C16-07`)

EXP-C16-04 - no magma generator is a usable PRNG compared with PCG64; the maximal period available to any order-2 recurrence on bytes is 65536, and affine generators mod 2^32 have lowest-bit period 3.

*Evidence:* EXP-C16-04, CLM-C16-17

### [2026-10-18T17:12:39Z] Historian — novelty (`C16-08`)

Classical - nonsingular feedback registers (Golomb), de Bruijn counts (van Aardenne-Ehrenfest--de Bruijn), periods of linear recurrences mod N (Ward, Wall), Fibonacci lengths of groups (Knox; Campbell et al.). Not found - the characterisation of full-period quasigroups as distance-1/2 de Bruijn cycles, the counts 0, 0, 0, 3360, the even-order group-isotope obstruction, and Fibonacci dynamics in Laver tables.

*Evidence:* CLM-C16-05, CLM-C16-07, CLM-C16-09, CLM-C16-15


## C13

### [2026-10-18T17:27:51Z] Mathematical Skeptic — review (`C13-09`)

EXP-C13-09 cross-checked the main results by independent code paths - explicit cube-law models for N = 3..60, the W-family theorem on all 42 six-leaf terms (N <= 6), and six atlas identifications against their direct arithmetic definitions up to N = 1000; no discrepancy. Remaining weak points - Theorem 1, Theorem 3 (iv) and Theorem 6 are written proofs not yet reviewed by an independent Skeptic; CLM-C13-11 rests on mechanical affine systems.

*Evidence:* EXP-C13-09, CLM-C13-03, CLM-C13-05, CLM-C13-11


## C19

### [2026-10-18T17:45:11Z] Historian — novelty (`C19-01`)

Literature read before experimenting - Baird-Smith et al. (shortest game n - Z(n), arXiv:1809.04881), Li et al. (deterministic games, bound 3n - 3Z(n) - IZ(n) + 1, arXiv:2006.16457), Cusenza et al. (split-first strategy is longest, bound B(n), equality iff n = F_k - 1; Fib. Quart. 60 (2022), arXiv:2009.09510), Cheigh et al. (every length between shortest and longest occurs; closed form for non-Fibonacci inputs open; CANT VI 2025). The cycle's target became the open closed form.

*Evidence:* CLM-C19-05

### [2026-10-18T17:45:11Z] Mathematical Explorer — result (`C19-02`)

Exact search for all n <= 150 (EXP-C19-01) confirms the published strategy and the equality cases independently; the reachable positions are all Fibonacci partitions of n.

*Evidence:* EXP-C19-01, CLM-C19-07, CLM-C19-08

### [2026-10-18T17:45:11Z] Formal Verifier — proof (`C19-03`)

A potential with weights a_i = F_{i+2} - i - 2 changes by 1 for every split or combine-1 and by i for the combine C_i, giving |G| = B(n) - sum (i-1) MC_i for every game; the longest game minimises a weighted count of combines (Lean-verified arithmetic core).

*Evidence:* CLM-C19-01

### [2026-10-18T17:45:11Z] Mathematical Inventor — hypothesis (`C19-04`)

Bold guesses for the deficit D(n) - additivity with consecutive-pair corrections (H-C19-1), dependence on the two top levels (H-C19-2), additivity over lazy runs (H-C19-3), chip-by-chip insertion (H-C19-4). All four were refuted; each failure pointed to longer-range carries.

*Evidence:* CLM-C19-10, CLM-C19-11, CLM-C19-12, CLM-C19-13

### [2026-10-18T17:45:11Z] Mathematical Explorer — result (`C19-05`)

The greedy game splits until every level holds at most one chip and only then combines; the intermediate configuration is the lazy Fibonacci representation (proved, Theorem 2). For a Fibonacci input the combines form a single upward cascade C_j, C_{j-2}, ..., giving D = floor(j^2/4) (proved, Theorem 4).

*Evidence:* CLM-C19-02, CLM-C19-03

### [2026-10-18T17:45:11Z] Mathematical Explorer — result (`C19-06`)

The saving rho = D(F_j) + D(m) - D(F_j + m) depends only on m and the parity of j (no exception among 17,711 cases), and rho itself is constant on Zeckendorf blocks of the wrong parity and shifted-clipped on the others - an exact recursion for D, inferred from n < 30000.

*Evidence:* CLM-C19-05, CLM-C19-06

### [2026-10-18T17:45:11Z] Mathematical Skeptic — result (`C19-07`)

Out-of-sample test of the recursion on 6,272 n not used to infer it (up to 2*10^7) - 0 mismatches. A first run of EXP-C19-04 crashed at its last step because the Fibonacci table ended near 5*10^19 (n = 10^30 requested); the table was extended to 200 terms and the experiment re-run. A first version of EXP-C19-02 was stopped because it was too slow (quadratic simulation up to n = 20000) and was rescaled.

*Evidence:* EXP-C19-04, EXP-C19-02


## C05

### [2026-10-18T18:17:35Z] Mathematical Skeptic — rejection (`C05-14`)

Independent review (reviews/skeptic_C05_C08_C12.md) - CLM-C05-09 refuted by linear models of order 16 over GF(16) for both laws (Lean-checked); all other C05 claims upheld (own CNF encodings with CaDiCaL and Kissat reproduce the census and all 15 claimed gaps).

*Evidence:* CLM-C05-09, reviews/skeptic_C05_C08_C12.md

### [2026-10-18T18:17:35Z] Mathematical Explorer — result (`C05-15`)

EXP-C05-07 - systematic search for linear models over GF(q), q <= 128. 0 conflicts with SAT, DRUP gaps or notes; even orders for 14 of 15 laws; 670 at n = 9 settled (new relative to the notes). Lesson - the Z_n affine search of EXP-C05-05 was blind to non-cyclic additive groups.

*Evidence:* EXP-C05-07, CLM-C05-10


## C08

### [2026-10-18T18:17:35Z] Mathematical Skeptic — rejection (`C08-12`)

Independent review (reviews/skeptic_C05_C08_C12.md) - five of the eight thresholds of CLM-C08-05 fail with explicit triples, and the lab's own corrected values (EXP-C08-06, CLM-C08-07) are still too low for (2,2;1,2) and (3,3;1,5). Root cause - random or small inputs rarely hit the extreme-conjugate inputs that break associativity. CLM-C08-02 needs a dominant root > 1 (G_k = k + 1 is associative at every shift); the evidence of CLM-C08-04 is contaminated, its statement survives a stronger search.

*Evidence:* CLM-C08-02, CLM-C08-04, CLM-C08-05, CLM-C08-07, reviews/skeptic_C05_C08_C12.md

### [2026-10-18T18:17:35Z] Mathematical Explorer — result (`C08-13`)

EXP-C08-07 - a targeted search (extreme conjugates, a window occupancy grid, known pairs as seeds, minimal recurrences) reproduces every certified failure of the review with the lab's own code; thresholds now (2,2;1,2) >= 7, (3,3;1,5) >= 12, tribonacci >= 4, 4-bonacci >= 8, G+G(k-2) >= 11 (CLM-C08-08); 8 non-monotone quadratic rows, all beta < 0 and non-canonical. Lesson for the lab - for rare failures, search where the theory says failures live.

*Evidence:* EXP-C08-07, CLM-C08-08, CLM-C08-04


## C20

### [2026-10-18T18:17:35Z] Historian — novelty (`C20-05`)

Revision of C20-04 - the scanned Zantema-Geser report UU-CS-1994-44 was found on ics-archive.science.uu.nl; its Theorem 1.1 is C03 Conjecture 4.6 verbatim (equivalence by case analysis, checked on all parameters <= 40). CLM-C20-04 and CLM-C03-10 are PROVEN (published proof) and REDISCOVERY.

*Evidence:* CLM-C20-04, CLM-C03-10, reviews/historian_C03_C10.md

### [2026-10-19T14:24:53Z] Mathematical Skeptic — review (`C20-06`)

Independent review (reviews/skeptic_C07_C17_C20.md) - Theorems 1-2 and Corollary 3 upheld (exhaustive derivation graphs n <= 10 / 15, strategies to length 18 / 21); the Zantema-Geser statement re-read on the scan and the equivalence confirmed on all parameters <= 50. Correction to C20-05 - the conjecture is equivalent to Theorem 1.1, not verbatim (one characterises termination, the other non-termination). Warning - the introduction of Geser's ICASE report claims linear lengths for all one-overlap-pair rules, which aab -> ababa contradicts; only the body's restricted statement is correct.

*Evidence:* CLM-C20-01, CLM-C20-02, CLM-C20-04, reviews/skeptic_C07_C17_C20.md


## C07

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C07-07`)

Independent review (reviews/skeptic_C07_C17_C20.md) - all claims upheld; the three written proofs are correct. Strengthening - the 33 further specs define the same 11 operations (absorption argument, now in proofs/paper/C07.md), so exactly 44 specs are associative; (J2) holds for k >= 2 (index slip); the Jacobsthal row checked from the definition for all b < 2^18.

*Evidence:* CLM-C07-01, CLM-C07-05, reviews/skeptic_C07_C17_C20.md


## C09

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C09-09`)

Independent review (reviews/skeptic_C05_C08_C12.md) - all claims upheld, written proofs correct, data extended to 1e8. Fixes - the bound |N(n)| < (sqrt5/phi) n + 1 had no proof (added); the title of CLM-C09-03 said 'a proportion 1/phi^2 are irreducible' (now 'at least'); EXP-C09-02 truncated factorisation sets at 64 (now exact, same numbers); EXP-C09-04 used floating point at the boundary n = 1 (now exact).

*Evidence:* CLM-C09-03, CLM-C09-07, CLM-C09-08, reviews/skeptic_C05_C08_C12.md


## C10

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C10-08`)

Independent review (reviews/skeptic_C05_C08_C12.md) - all claims upheld; the evidence summary of CLM-C10-05 covered only offset-1 rules (the Skeptic checked all 18); CLM-C10-07 (skew binary) now PROVEN by an elementary argument sketched by the Skeptic.

*Evidence:* CLM-C10-05, CLM-C10-07, reviews/skeptic_C05_C08_C12.md


## C11

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C11-12`)

Independent review (reviews/skeptic_C05_C08_C12.md) - all nine claims upheld, every written proof checked; benchmarks reproduced to 4 decimals with independent length functions.

*Evidence:* reviews/skeptic_C05_C08_C12.md


## C12

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C12-13`)

Independent review (reviews/skeptic_C05_C08_C12.md) - all 13 claims upheld; the potentially novel Grundy theorem CLM-C12-04 checked step by step and computed to 1e8. CLM-C12-13 (subtract-a-Fibonacci bounded) has weaker support than recorded - new record values 15 at n = 206,025 and 16 at n = 63,331,966.

*Evidence:* CLM-C12-04, CLM-C12-13, reviews/skeptic_C05_C08_C12.md


## C14

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C14-12`)

Independent review (reviews/skeptic_C14_C15_C16_C18.md) - no claim refuted; every census number reproduced with independent code. CLM-C14-06 is a rediscovery - Abiad, Butler and Haemers (arXiv:1801.01149, 2018, Section 5) define the product and give its Seidel matrix; the lab's searches missed it. CLM-C14-13 survives a much larger search (53,703 multisets, product order <= 64). The '4-5 orders of magnitude' spectra speedup was inflated by BLAS thread oversubscription (about 3 orders).

*Evidence:* CLM-C14-06, CLM-C14-13, reviews/skeptic_C14_C15_C16_C18.md


## C15

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C15-08`)

Independent review (reviews/skeptic_C14_C15_C16_C18.md) - no claim refuted; written proofs correct. Corrections - 'affine and fuse fast-forwards never lose' was false (they lose for t below about 20-70 with a fair timing protocol), recorded speedups are single-run orders of magnitude (fuse x4000 became x1363 on re-run), the width bound holds for commutative semigroups only (S3 grows to 1296 by t = 6).

*Evidence:* CLM-C15-12, CLM-C15-13, CLM-C15-15, reviews/skeptic_C14_C15_C16_C18.md


## C16

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C16-09`)

Independent review (reviews/skeptic_C14_C15_C16_C18.md) - all 19 claims upheld; written proofs correct. Evidence extended - full-period quasigroups for every n <= 26, CLM-C16-13 exhaustive for all affine magmas with N <= 60, Laver transients 5 up to n = 13. EXP-C16-01 hashed a wall-clock value (fixed; it now reproduces).

*Evidence:* CLM-C16-10, CLM-C16-13, EXP-C16-01, reviews/skeptic_C14_C15_C16_C18.md


## C17

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C17-04`)

Independent review (reviews/skeptic_C07_C17_C20.md) - the theorems are correct, but two code problems changed stated numbers - the exhaustive check was charged a whole 64-row slab on non-associative inputs (the gains of CLM-C17-04 hold for certification only), and a classification bug in EXP-C17-02 gave 18 insufficient / 31 undecided laws instead of 43 / 0. Both fixed and re-run; the Skeptic's uniqueness argument for the anchored LD instance added, and EXP-C17-03 extends CLM-C17-05 to every N <= 4096.

*Evidence:* CLM-C17-04, CLM-C17-05, CLM-C17-07, reviews/skeptic_C07_C17_C20.md


## C18

### [2026-10-19T14:25:22Z] Mathematical Skeptic — review (`C18-09`)

Independent review (reviews/skeptic_C14_C15_C16_C18.md) - no claim refuted; the negative result is robust. Wording fixed - FNV-1a's z = -9.8 means more uniform than random (not a defect), 'no improvement in any dimension' became 'no significant improvement', H-C18-2 restricted to the reverse-pass construction tested, the C18-11 refutation rests on the avalanche bias, throughput figures are load-dependent ranges.

*Evidence:* CLM-C18-09, CLM-C18-10, CLM-C18-13, reviews/skeptic_C14_C15_C16_C18.md


## C13

### [2026-10-19T14:44:17Z] Mathematical Skeptic — review (`C13-10`)

Independent review (reviews/skeptic_C13_C19.md) - no claim refuted; the written proofs of Theorems 1, 3 (iv) and 6 are correct and the closure code implements Theorem 6 (an independent closure proves the same 16 laws). Corrections - EXP-C13-02 selected 52 laws from finite classes (re-run - 146 of 147 infinite-class laws non-rigid); CLM-C13-11 cited a part of Theorem 1 that did not exist (part (f) added); Lean coverage of C13-02/04 stated more broadly than it is.

*Evidence:* CLM-C13-01, CLM-C13-06, CLM-C13-08, CLM-C13-11, EXP-C13-02, reviews/skeptic_C13_C19.md


## C19

### [2026-10-19T14:44:17Z] Mathematical Skeptic — review (`C19-08`)

Independent review (reviews/skeptic_C13_C19.md) - no claim refuted; the written proofs of Theorems 2 and 4 are correct and complete, and Cusenza et al.'s Thm 1.2 says exactly what Theorem 4 uses (read in the arXiv and published versions). Corrections - Theorem 1 is stated in Cusenza et al. as eq. (3.16), not just implicit; Theorems 1-2 already give a provably correct O(log^2 n)-move method and an unconditional bound D(n) = O(log^2 n) (now Theorems 7-8); the textbook's statement of the recursion lacked its range condition; the carry cascade of entry C19-05 is played bottom-up (C_2, C_4, ... or C_3, C_5, ...), not top-down.

*Evidence:* CLM-C19-01, CLM-C19-14, CLM-C19-15, reviews/skeptic_C13_C19.md

### [2026-10-19T14:44:17Z] Mathematical Explorer — result (`C19-09`)

EXP-C19-05 - the lazy-representation method agrees with full simulation for every n < 20,000; the conjectured recursion agrees with this provably correct method on 103,799 n up to 10^15, so the recursion is now tested against a proof-backed reference rather than against the Theta(n) simulation.

*Evidence:* EXP-C19-05, CLM-C19-05, CLM-C19-14


## C20

### [2026-10-19T22:30:20Z] Research Director — infrastructure (`manual-2026-10-19T22:30:20Z`)

Batch 1.1 (G6): 'lab sync' compared each record's journal entry with the original entry, kind included. The records of C03 and C06 had changed the kind of entries C03-14 and C06-11 from 'correction' (not a known kind) to 'revision', so every sync appended an identical revision of both entries (16 copies each, text unchanged). The 32 copies were removed from journal/entries.jsonl (they remain in the git history), 'correction' is now a known journal kind and the two records use it again, sync now compares agent, text and references with the latest version of an entry, and the new 'python -m lab check' rejects a revision that repeats the version before it. The batch-1 report's journal count (255) included the 32 copies.

*Evidence:* lab/records.py, lab/check.py


## C06

### [2026-10-19T23:04:05Z] Historian — novelty (`C06-13`)

Historian audit 2026-10-19 (reviews/historian_C11_C20.md, note 6) - CLM-C06-01 states a published theorem (Laver; Dehornoy 2000, Prop. X.1.6, statement read in Biane's refereed survey SLC 80 (2019) and in Aguilera-Iannella 2026), so it is now PROVEN (literature) instead of COMPUTATIONALLY SUPPORTED. The C06 citation of Biane's arXiv v1, whose section 2.1 states the recursion for all q, is replaced by the published version, which corrects it.

*Evidence:* CLM-C06-01, reviews/historian_C11_C20.md


## C10

### [2026-10-19T23:04:05Z] Formal Verifier — proof (`C10-09`)

Batch 1.1 - Theorem 6 (skew binary counting: worst case 2, average 3/2 + O(log N / N)) is now proved in Lean (proofs/lean/Infinity/C10_SkewBinary.lean, standard axioms), with the explicit bound |average - 3/2| <= (floor(log2(N+1)) + 1)/(2N) and a proof of the uniqueness of canonical skew-binary representations, which the paper had cited.

*Evidence:* CLM-C10-07, proofs/lean/NOTES_batch1.1.md


## C11

### [2026-10-19T23:04:05Z] Historian — novelty (`C11-13`)

Historian audit 2026-10-19 (reviews/historian_C11_C20.md) - T_011 is Capocelli's code C(3) (IEEE Trans. IT 35, 1989), tabulated against the Fibonacci code by Lima-da Rocha (JCIS 2013), and the pattern codes T_p are Lakshmanan's (1981); CLM-C11-04 and CLM-C11-09 become partial rediscoveries (REDISCOVERY with a 'Partial' basis), CLM-C11-07 keeps POTENTIALLY NOVEL with low confidence. Capocelli 1989 and Lakshmanan 1981 could not be read and may settle the residue.

*Evidence:* CLM-C11-04, CLM-C11-07, CLM-C11-09, reviews/historian_C11_C20.md


## C13

### [2026-10-19T23:04:05Z] Formal Verifier — proof (`C13-11`)

Batch 1.1 - Theorem 1 (structure of affine spectra) is now proved in Lean (proofs/lean/Infinity/C13_AffineStructure.lean): parts (a)-(f), the infinite case by Gauss's lemma instead of Schur's theorem; only the example that resultants lie in the ideal is not formalised. Historian audit 2026-10-19: CLM-C13-02, -03, -11 keep POTENTIALLY NOVEL with low confidence (single-law spectra are an ETP topic, without the anchor).

*Evidence:* CLM-C13-01, CLM-C13-02, CLM-C13-03, CLM-C13-11, reviews/historian_C11_C20.md


## C14

### [2026-10-19T23:04:05Z] Historian — novelty (`C14-13`)

Historian audit 2026-10-19 (reviews/historian_C11_C20.md) - Oh, Yoo and Yun (SIAM J. Discrete Math. 27, 2013) prove that G -> K_2 (+) G is well defined and injective on switching classes, which is CLM-C14-07 (c) and (b); only the elementary part (a) is not in the literature found. CLM-C14-07 becomes a partial rediscovery; the K_2-cancellation step of the conjecture CLM-C14-13 is their theorem.

*Evidence:* CLM-C14-07, CLM-C14-13, reviews/historian_C11_C20.md


## C15

### [2026-10-19T23:04:05Z] Historian — novelty (`C15-09`)

Historian audit 2026-10-19 (reviews/historian_C11_C20.md) - streaming width is essentially the one-way communication complexity of the t-step rule of Durr, Rapaport and Theyssier (TCS 322, 2004), who classify the elementary CA into bounded / linear / other and give explicit linear-complexity rules (132, 23) and a 3-state Theta(n^2) CA, so the refutations of H-C15-1 and H-C15-4 were already exemplified there. Only the fuse magma and the order-3 census are new; CLM-C15-04, -07, -15 keep POTENTIALLY NOVEL with low confidence.

*Evidence:* CLM-C15-04, CLM-C15-07, CLM-C15-15, reviews/historian_C11_C20.md


## C16

### [2026-10-19T23:04:05Z] Historian — novelty (`C16-10`)

Historian audit 2026-10-19 (reviews/historian_C11_C20.md) - P. Klimov (arXiv:2604.05754, 2026) studies the same objects (UFS-groupoids) and poses as open (Problems 7.3-7.5) whether one can be left-cancellative, a left quasigroup or a quasigroup; CLM-C16-07 answers this positively with finite examples (the Historian re-checked the order-5 example). CLM-C16-05 and -07 keep POTENTIALLY NOVEL with more confidence; CLM-C16-15 is a two-line corollary, not a substantive novelty.

*Evidence:* CLM-C16-05, CLM-C16-07, CLM-C16-15, reviews/historian_C11_C20.md


## C17

### [2026-10-19T23:04:05Z] Historian — novelty (`C17-05`)

Historian audit 2026-10-19 (reviews/historian_C11_C20.md) - the anchor-instance question of CLM-C17-05 is answered in the literature for every N: uniqueness is Dehornoy's Lemma X.1.2 (also Biane, SLC 80 (2019) section 2.1), and the full instance fails for every N that is not a power of 2 (Biane's footnote 1; Aguilera-Iannella, arXiv:2610.06106, Prop. 2.5 with Dehornoy's Lemma X.1.7 and Prop. X.1.6). Several surveys, including Biane's arXiv v1 cited in C06, state the recursion for all q, which is false already at N = 3; the lab's C17 correction of its own C06 paraphrase is the correction Biane made in the published version. With the new Lean file C17_ForcedTable.lean (uniqueness, existence, reduction to the wrap-around equations for every N), CLM-C17-05 becomes PROVEN (computer-assisted, N <= 4096) and REDISCOVERY; the all-N statement is recorded as CLM-C17-08 (REDISCOVERY, COMPUTATIONALLY SUPPORTED until an independent proof check).

*Evidence:* CLM-C17-05, CLM-C17-08, reviews/historian_C11_C20.md


## C19

### [2026-10-19T23:04:05Z] Formal Verifier — proof (`C19-10`)

Batch 1.1 - the arithmetic core of Theorems 7-8 (the weight identity and the bound 1 + (t+1)(t+6)/2 for any two 0/1 strings of equal value) is proved in Lean (proofs/lean/Infinity/C19_DeficitBound.lean); the game-theoretic steps remain a written proof. Historian audit 2026-10-19: all arXiv Zeckendorf-game papers to 2026-10-07 checked; the C19 labels stand.

*Evidence:* CLM-C19-14, CLM-C19-15, reviews/historian_C11_C20.md


## C05

### [2026-10-19T23:54:21Z] Formal Verifier — result (`C05-16`)

Batch 1.1 (G4) - EXP-C05-08 decides the two open orders of laws 677 and 1313 left by EXP-C05-03: neither law has a model of order 8 or 10. A complete case split (Lemma 8: idempotent or not, cycle type of one row) gives 45 and 97 CNFs per law; all 284 are UNSAT and every DRAT proof was verified by drat-trim. So both laws have exactly the orders 1, 5, 7, 9 up to 10, and 16 is the only even order known for either. 677 at order 8 was already known (Mace4, ETP paper section 7.3.1); 677 at 10 and 1313 at 8 and 10 were not found in the sources read. Law 677 is the premise of the ETP's last open finite implication (677 => 255).

*Evidence:* EXP-C05-08, CLM-C05-11, CLM-C05-12, CLM-C05-13

### [2026-10-20T02:03:31Z] Mathematical Skeptic — review (`C05-17`)

Skeptic review of batch 1.1 (reviews/skeptic_batch1.1.md) - Lemmas 7-9 and the encoding of EXP-C05-08 are correct and the code matches them; all 401 CNFs rebuilt with matching hashes; laws 677 and 1313 re-decided at orders 8 and 10 with an encoding written from scratch and a different case split, every case UNSAT with DRAT proofs verified by drat-trim (677 at order 10 twice). CLM-C05-11, -12, -14 upheld; CLM-C05-13 upheld with a citation correction (EXP-C05-06 certifies the gaps 2, 3, 4, 6); CLM-C05-10 upheld with a correction (EXP-C05-07 re-checks one model per (law, q); the Skeptic's computation re-checks all and reproduces every order list). Every model of 677 of order <= 10 is a quasigroup (SAT, uncertified).

*Evidence:* CLM-C05-10, CLM-C05-11, CLM-C05-12, CLM-C05-13, CLM-C05-14, reviews/skeptic_batch1.1.md


## C17

### [2026-10-20T02:03:31Z] Mathematical Skeptic — review (`C17-06`)

Skeptic review of batch 1.1 (reviews/skeptic_batch1.1.md) - the Historian's row-period argument for CLM-C17-08 is correct once the row structure of the forced table (rows are periodic, with period the first index of the top element) and the top-element case of the induction are written out; the Skeptic did so and machine-checked the whole argument: C17_RowPeriod.lean proves, for every N, that the full anchor instance has a model iff N is a power of 2, from Laver's theorem taken as an explicit hypothesis (used only at order 2^(v2(N)+1)). CLM-C17-08 becomes PROVEN; the literature chain through Dehornoy's book is no longer needed. CLM-C17-05 upheld.

*Evidence:* CLM-C17-08, CLM-C17-05, reviews/skeptic_batch1.1.md


## C19

### [2026-10-20T02:03:31Z] Mathematical Skeptic — review (`C19-11`)

Skeptic review of batch 1.1 (reviews/skeptic_batch1.1.md, section 3.2) - the written steps of Theorem 8 (CLM-C19-15) that are not in Lean are correct; exhaustive longest games for n <= 100 agree with the lab's values and satisfy the bound; the Lean core and the Lean part of CLM-C19-14 are faithful.

*Evidence:* CLM-C19-15, CLM-C19-14, reviews/skeptic_batch1.1.md


## C05

### [2026-10-20T14:17:53Z] Historian — novelty (`C05-18`)

Historian spectrum audit 2026-10-20 (reviews/historian_spectra_2026.md) - nothing newer than B. Le Floch's July 14, 2025 notes states the spectra of the 15 laws, except for 677, which the ETP Zulip topic 'FINITE: 677 -> 255' and the eq677 model database treat in depth: 677 has no models of orders 2, 3, 4, 6 (Tencer, Dec 7, 2024), 8 (Brox, Dec 7, 2024) or 10 (Brox, Jan 12, 2025, 39 h of Mace4), models of 5, 7, 9, 11, 13, 16, 19, ..., and orders 12 and 14 are open in every source. So CLM-C05-12 is a rediscovery (with the first checkable certificate), CLM-C05-07, -08, -10 are partial rediscoveries, and none of the target pairs of EXP-C05-09 and EXP-C05-10, nor 1313 at 8 and 10, is decided by any source.

*Evidence:* CLM-C05-07, CLM-C05-08, CLM-C05-10, CLM-C05-12, CLM-C05-13, reviews/historian_spectra_2026.md

### [2026-10-20T15:39:55Z] Formal Verifier — result (`C05-19`)

Batch 1.2 (find more) - the case split of EXP-C05-08, generalised to every law x = y*T (systems/magma_split.py, Lean: right_mul_bijective_of_law for the laws x = y*(S*y)), decides all 15 orders n <= 10 that EXP-C05-03 had left UNKNOWN: none has a model (EXP-C05-09; 1,522 drat-trim-verified proofs; 13 of 13 controls agree). With EXP-C05-12, which certifies every order n <= 7 again, the spectra up to 10 of all 13 laws are complete and rest on the lab's own certificates (CLM-C05-17). Pattern recorded as a conjecture: none of these laws without a model of order 2 has one of order 6 or 10 (CLM-C05-18).

*Evidence:* EXP-C05-09, EXP-C05-12, CLM-C05-15, CLM-C05-17, CLM-C05-18, CLM-C05-19

### [2026-10-20T15:39:55Z] Formal Verifier — result (`C05-20`)

Batch 1.2 - law 677 at order 12 (open in every source). The cheap pass of EXP-C05-11 refutes 138 of the 195 case CNFs with verified proofs; the 57 that remain are structured: in the idempotent case exactly the 14 cases whose row 0 has a single fixed point, in the other case only cycles of 0 of length >= 4 with at most 2 fixed points (CLM-C05-20). This is a reduction and a hand-off; the order stays open.

*Evidence:* EXP-C05-11, CLM-C05-20

