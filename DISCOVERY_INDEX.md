# Discovery Index

_Generated 2026-10-20T16:40:05Z by `python -m lab sync` from `db/claims/`. Do not edit by hand._

Every claim carries two independent labels: a **verification status** (PROVEN, COMPUTATIONALLY SUPPORTED, CONJECTURE, REFUTED, INCONCLUSIVE) and a **novelty status** (REDISCOVERY, POTENTIALLY NOVEL, NOT ASSESSED). A claim may therefore appear in more than one section below.

## Summary

| Verification status | Claims |
|---|---|
| PROVEN | 145 |
| COMPUTATIONALLY SUPPORTED | 37 |
| CONJECTURE | 5 |
| REFUTED | 50 |
| INCONCLUSIVE | 2 |

| Novelty status | Claims |
|---|---|
| REDISCOVERY | 115 |
| POTENTIALLY NOVEL | 53 |
| NOT ASSESSED | 71 |

## 1. Verified theorems (PROVEN)

| Claim | Title | Proof check | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-01 | Symbol counts are the complete invariant of the commutation congruence | Lean 4 + Mathlib (commEq_iff_count, projection_is_unary); s… | REDISCOVERY | EXP-C01-01 |
| CLM-C01-02 | One symbol, one relation a^m = a^(m+p) gives exactly m+p classes (index m, period p) | Lean 4 + Mathlib (gen_iff, exactly_m_add_p_classes); standa… | REDISCOVERY | EXP-C01-02 |
| CLM-C01-03 | Several one-symbol relations have index min m_i and period gcd(n_i - m_i) | written proof (proofs/paper/C01.md, Theorem 3), skeptic-rev… | REDISCOVERY | EXP-C01-02 |
| CLM-C01-04 | Multiplication emerges as composition of substitutions; with two symbols it is non-commut… | written proof (proofs/paper/C01.md, Theorem 4), skeptic-rev… | REDISCOVERY | EXP-C01-03 |
| CLM-C01-06 | Border-containment theorem for one length-preserving relation | written proof (proofs/paper/C01.md, Theorem 5), skeptic-rev… | REDISCOVERY | EXP-C01-04, EXP-C01-05, EXP-C01-07 |
| CLM-C01-07 | Common-border formula proved for 1632 specific relations by verified finite completions | computer-assisted (Python) - convergent completions (rules … | REDISCOVERY | EXP-C01-07 |
| CLM-C01-09 | Common-border formula when u and v share no border (c = 1) - consequence of published res… | derivation from published theorems (Gray-Steinberg 2026 Thm… | REDISCOVERY | EXP-C01-06, EXP-C01-07, EXP-C01-08 |
| CLM-C02-01 | Integer bases emerge as normal forms of the exchange rule b[k] -> [k+1] | written proof (proofs/paper/C02.md Theorem 2), skeptic-revi… | REDISCOVERY | EXP-C02-01 |
| CLM-C02-02 | Abelian property of carry rules (order of exchanges is irrelevant) | written proof (proofs/paper/C02.md Theorem 1), skeptic-revi… | REDISCOVERY | EXP-C02-01, EXP-C02-04 |
| CLM-C02-03 | Termination dichotomy for carry rules away from sum b = m | written proof (proofs/paper/C02.md Theorem 3), skeptic-revi… | REDISCOVERY | EXP-C02-03 |
| CLM-C02-04 | Carry rules with sum b = m never terminate from all unary starts (uniform glider) | two independent written proofs - proofs/paper/C02.md Theore… | POTENTIALLY NOVEL | EXP-C02-03 |
| CLM-C02-05 | Termination classification for all 189 small carry rules (computer-assisted) | computer-assisted (Python) - explicit periodic-glider or mo… | POTENTIALLY NOVEL | EXP-C02-03 |
| CLM-C02-07 | Uniqueness of representations when the reduced carry polynomial is primitive and irreduci… | Lean 4 + Mathlib for the polynomial core (digits_unique, ex… | REDISCOVERY | EXP-C02-05 |
| CLM-C02-08 | Exchange representations respect the radix order | written proof (proofs/paper/C02.md Theorem 6, gap closed by… | REDISCOVERY | EXP-C02-03 |
| CLM-C02-09 | The Fibonacci exchange system terminates at the Zeckendorf representation; shortest deriv… | written proof (proofs/paper/C02.md Theorem 8), skeptic-revi… | REDISCOVERY | EXP-C02-02, EXP-C02-06 |
| CLM-C02-10 | Longest Fibonacci exchange derivations (longest Zeckendorf games) for n <= 40 | computer-assisted exhaustive search of the full derivation … | REDISCOVERY | EXP-C02-02, EXP-C02-06 |
| CLM-C02-11 | Termination classification of carry rules: terminating from every unary start iff sum b <… | written proofs (proofs/paper/C02.md Theorem 3, skeptic-revi… | POTENTIALLY NOVEL | EXP-C02-03, EXP-C02-07 |
| CLM-C03-01 | A one-rule system that decreases the count of some letter terminates | Lean 4 + Mathlib (terminating_of_count_lt); standard axioms… | REDISCOVERY | EXP-C03-01 |
| CLM-C03-02 | Conserving rules terminate (s = p or r = q) | written proof (proofs/paper/C03.md Theorem 2, induction ove… | REDISCOVERY | EXP-C03-01 |
| CLM-C03-03 | Self-embedding derivations prove non-termination; the doubling region r >= 2q, s >= 2p al… | Lean 4 + Mathlib (not_terminating_of_loop, not_terminating_… | REDISCOVERY | EXP-C03-01, EXP-C03-02 |
| CLM-C03-04 | 011 -> 11100 is non-terminating although r < 2q | Lean 4 + Mathlib (not_terminating_0_11; each step checked b… | REDISCOVERY | EXP-C03-01 |
| CLM-C03-05 | Lifting lemma - loops transfer along letter morphisms (explains divisibility) | Lean 4 + Mathlib (step_map, loop_map); 147 + 225 lifted cer… | REDISCOVERY | EXP-C03-03, EXP-C03-04 |
| CLM-C03-06 | Classification of 601 of the 625 rules with p, q, r, s <= 5 (computer-assisted) | computer-assisted (Python) - theorems CLM-C03-01/02 for the… | REDISCOVERY | EXP-C03-01, EXP-C03-02, EXP-C03-03 |
| CLM-C03-10 | Divisibility characterization of termination for 0^p 1^q -> 1^r 0^s (H-C03-4) | published theorem - Zantema-Geser Theorem 1.1 (tech. report… | REDISCOVERY | EXP-C03-02, EXP-C03-03, EXP-C03-04 |
| CLM-C04-01 | Termination census of one-rule systems with |l|, |r| <= 3: non-terminating iff l is a fac… | computer-assisted (Python) - explicit termination certifica… | REDISCOVERY | EXP-C04-01 |
| CLM-C04-03 | The rules aab -> ababa and aab -> babaa (and their six symmetric images) terminate | written proof in cycle C20 (proofs/paper/C20.md Theorems 1-… | REDISCOVERY | EXP-C04-02, EXP-C20-01 |
| CLM-C04-04 | ab -> ba: every derivation has inv(w) steps, D(n) = floor(n^2/4), P-positions = even inve… | Lean 4 + Mathlib (inv_step, normal_iff_inv_zero, derivation… | REDISCOVERY | EXP-C04-03, EXP-C04-07 |
| CLM-C04-05 | One-rule systems with an unbordered left-hand side have random descent (Lean-verified) | Lean 4 + Mathlib (random_descent, unbordered_diamond, unbor… | REDISCOVERY | EXP-C04-05 |
| CLM-C04-06 | Every one-rule system has a constant-step potential; for terminating ones confluence is e… | written proof (proofs/paper/C04.md Theorem 2), skeptic-revi… | REDISCOVERY | EXP-C04-05, EXP-C04-06 |
| CLM-C04-08 | Rewriting games of random-descent rules are parity games (Grundy value = D(w) mod 2) | written proof (proofs/paper/C04.md Theorem 9, induction on … | REDISCOVERY | EXP-C04-07 |
| CLM-C04-09 | The rule aab -> ba has derivational complexity D(n) = n - 1 - min{k : 2^k + k >= n} (non-… | written proof (proofs/paper/C04.md Theorem 7), skeptic-revi… | POTENTIALLY NOVEL | EXP-C04-03, EXP-C04-04 |
| CLM-C04-10 | Identity: OEIS A247983 (truncation index of the series for log 2) equals D(n+2) for aab -… | written proof (proofs/paper/C04.md Theorem 8, Jensen's ineq… | POTENTIALLY NOVEL | EXP-C04-09, EXP-C04-10 |
| CLM-C04-13 | Rewriting games with lhs a^k are take-and-break games: aa -> b is Dawson's Kayles, aa -> … | written proof (proofs/paper/C04.md Theorem 10), skeptic-rev… | REDISCOVERY | EXP-C04-07, EXP-C04-08 |
| CLM-C04-15 | The rewriting game of aa -> b on a^n has Grundy values periodic with period 34 from n = 53 | computer-assisted - octal recursion to n = 3000 and the Guy… | REDISCOVERY | EXP-C04-08 |
| CLM-C05-04 | Law 167, x = (y*x)*(x*y): every finite model has order 0 or 1 mod 4 | Lean 4 + Mathlib (Infinity.C05.law167_card_mod_four; standa… | REDISCOVERY | EXP-C05-01 |
| CLM-C05-05 | Identities x = y*s(x, y) make every left translation of a finite model bijective | Lean 4 + Mathlib for the x = y*s(x,y) case (left_mul_biject… | REDISCOVERY | EXP-C05-03 |
| CLM-C05-07 | New spectrum memberships for open ETP laws: 677 has models of orders 5, 7, 9; 1286, 1313 … | Lean 4 kernel decide on explicit tables (E677_order5_law, E… | REDISCOVERY | EXP-C05-03, EXP-C05-04 |
| CLM-C05-08 | New spectrum gaps for open ETP laws (certified UNSAT): 501 has no models of orders 6, 7; … | computer-assisted - DRUP refutations from Glucose 4 verifie… | REDISCOVERY | EXP-C05-03, EXP-C05-06 |
| CLM-C05-10 | Linear models over finite fields: the orders q <= 128 at which the 15 open laws have a mo… | computer-assisted - exhaustive search over GF(q)^2 for ever… | REDISCOVERY | EXP-C05-07 |
| CLM-C05-11 | Law 677, x = y(x((yx)y)), has no model of order 8 (rediscovery; DRAT-certified) | computer-assisted - the CNFs of the case split of proofs/pa… | REDISCOVERY | EXP-C05-08 |
| CLM-C05-12 | Law 677 has no model of order 10 (DRAT-certified); its orders up to 10 are exactly 1, 5, … | computer-assisted - the CNFs of the case split of proofs/pa… | REDISCOVERY | EXP-C05-08 |
| CLM-C05-13 | Law 1313, x = y(((yx)x)y), has no model of order 8 or 10 (DRAT-certified); its orders up … | computer-assisted - the CNFs of the case split of proofs/pa… | POTENTIALLY NOVEL | EXP-C05-08 |
| CLM-C05-14 | Finite models of law 1313 are quasigroups (Lean) | Lean 4 (complete) - law1313_left_bijective, law1313_right_b… | NOT ASSESSED |  |
| CLM-C05-15 | Fifteen new certified spectrum gaps for open ETP laws x = y*T at orders 8-10 | computer-assisted - every case CNF of the case split of pro… | POTENTIALLY NOVEL | EXP-C05-09 |
| CLM-C05-16 | Nine new certified spectrum gaps at orders 11-13 for the quasigroup laws 1076, 1110, 1279… | computer-assisted - every case CNF of Lemma 8 (with Latin c… | POTENTIALLY NOVEL | EXP-C05-10, EXP-C05-07 |
| CLM-C05-17 | Complete spectra up to order 10 of the 13 open ETP laws of the form x = y*T | computer-assisted - every member has an explicit table re-c… | POTENTIALLY NOVEL | EXP-C05-12, EXP-C05-09, EXP-C05-08, EXP-C05-03, EXP-C05-07 |
| CLM-C05-19 | Finite models of any law x = y*(S*y) are quasigroups (Lean); this covers the ETP laws 107… | Lean 4 (complete) - right_mul_bijective_of_law and left_mul… | REDISCOVERY |  |
| CLM-C05-20 | Law 677 at order 12: a model exists iff one of 57 explicit case CNFs is satisfiable | computer-assisted - the other 138 of the 195 case CNFs of L… | POTENTIALLY NOVEL | EXP-C05-11 |
| CLM-C05-22 | The spectrum of ETP law 501, x = y(y(x(xy))), is exactly {n : n = 0, 1 (mod 4)} | Lean 4 for the necessity - law501_card_mod_four (proofs/lea… | POTENTIALLY NOVEL | EXP-C05-15, EXP-C05-09, EXP-C05-12, EXP-C05-06 |
| CLM-C05-23 | Finite models of the ETP laws 704 and 883 are quasigroups (Lean); for 704 squaring is a b… | Lean 4 (complete) - law883_right_bijective, law704_square_b… | REDISCOVERY |  |
| CLM-C06-01 | Left-distributivity with a successor anchor: the Laver tables (rediscovery) | published theorem (R. Laver 1992/1995; P. Dehornoy, Braids … | REDISCOVERY | EXP-C06-01, EXP-C06-02 |
| CLM-C06-02 | Anchored associativity forces x*y = x + y + 1, for every N | Lean 4 + Mathlib (anchored_assoc_unique; standard axioms on… | REDISCOVERY | EXP-C06-02 |
| CLM-C06-03 | Anchored right-distributivity forces x*y = x + 1, for every N | Lean 4 + Mathlib (anchored_rd_unique; standard axioms only)… | REDISCOVERY | EXP-C06-02 |
| CLM-C06-05 | Anchored right-permutable magmas are x*y = x + c(y); there are N^(N-1) of them | written proof (proofs/paper/C06.md Theorem 4), skeptic-revi… | REDISCOVERY | EXP-C06-02 |
| CLM-C06-06 | An 'odd' law: (xy)z = x((yz)z) has an anchored model exactly for odd N, and it is unique | Lean 4 + Mathlib (odd_law_even_impossible, odd_law_formula,… | POTENTIALLY NOVEL | EXP-C06-03, EXP-C06-04 |
| CLM-C06-07 | A 'golden' law: anchored models of (xy)z = x(y(zz)) correspond to roots of a^2 + a = 1 mo… | written proof (proofs/paper/C06.md Theorem 6), skeptic-revi… | POTENTIALLY NOVEL | EXP-C06-04 |
| CLM-C06-08 | Anchored left-permutable magmas are commutative monoids in disguise (counted by OEIS A058… | Lean 4 + Mathlib for the structural core (centralizer_eq, c… | REDISCOVERY | EXP-C06-02 |
| CLM-C06-12 | Anchored spectra are closed under coprime products | written proof (proofs/paper/C06.md Theorem 8), skeptic-revi… | REDISCOVERY | EXP-C06-03, EXP-C06-04 |
| CLM-C07-01 | The associative mex operations are 0, projections, min, +, XOR, nim-product and four rela… | written proof for the 11 canonical formulas (proofs/paper/C… | POTENTIALLY NOVEL | EXP-C07-01 |
| CLM-C07-03 | In a mex operation with both L and R options 0 is an identity; with neither, 0 is absorbi… | written proof (proofs/paper/C07.md Theorem 2, two-line indu… | NOT ASSESSED | EXP-C07-02 |
| CLM-C07-05 | The Jacobsthal row: row 2 of f(a,b) = mex{f(a',b) XOR f(a,b')} swaps the blocks [2^k - J_… | written proof (proofs/paper/C07.md Theorem 3, induction ove… | POTENTIALLY NOVEL | EXP-C07-03 |
| CLM-C08-01 | Every shifted Knuth product a o_t b = sum F(k+l+t) over Zeckendorf indices is associative… | Lean 4 + Mathlib (Infinity.C08.circ_assoc, circ_comm, key, … | REDISCOVERY | EXP-C08-01, EXP-C08-03, EXP-C08-05 |
| CLM-C09-01 | Knuth's circle semigroup embeds in Z[phi]; Fibonacci numbers are its units-images | written proof (proofs/paper/C09.md Theorem 1) relying on CL… | REDISCOVERY | EXP-C09-03 |
| CLM-C09-03 | Window obstruction: at least a proportion 1/phi^2 of all integers are circle-irreducible | written proof (proofs/paper/C09.md Theorem 3; Weyl equidist… | POTENTIALLY NOVEL | EXP-C09-04 |
| CLM-C09-06 | Factorisation lengths are bounded by the conjugate coordinate | written proof (proofs/paper/C09.md Theorem 4), skeptic-revi… | POTENTIALLY NOVEL | EXP-C09-04 |
| CLM-C09-07 | The norm N(n) = n*^2 + n n* - n^2 is multiplicative for the circle product | written proof (proofs/paper/C09.md Theorem 1 and the bound … | REDISCOVERY | EXP-C09-03 |
| CLM-C09-08 | Factorisation statistics of the circle semigroup up to 2e5 | computer-assisted enumeration (EXP-C09-01, EXP-C09-02). The… | POTENTIALLY NOVEL | EXP-C09-01, EXP-C09-02 |
| CLM-C10-01 | Average cost of counting in classical representations (b/(b-1), e-1, 1) | written proof (proofs/paper/C10.md Theorem 1); confirmed to… | REDISCOVERY | EXP-C10-01 |
| CLM-C10-02 | Zeckendorf counting: T_m = 2 G_m - ceil(m/2) - 2, average cost 2 | written proof (proofs/paper/C10.md Theorem 2); recurrence e… | REDISCOVERY | EXP-C10-02, EXP-C10-04 |
| CLM-C10-04 | Exchange systems fire 1/(m - sum b) times per increment on average | written proof (proofs/paper/C10.md Theorem 3) from the abel… | REDISCOVERY | EXP-C10-03 |
| CLM-C10-05 | Single-offset exchange rules cost exactly firings + 1 per increment (average 1 + 1/(m - q… | written proof (proofs/paper/C10.md Theorem 4), skeptic-revi… | REDISCOVERY | EXP-C10-03 |
| CLM-C10-07 | Skew binary counting has worst-case cost 2 and average 3/2 | Lean 4 (complete) - proofs/lean/Infinity/C10_SkewBinary.lea… | REDISCOVERY | EXP-C10-01 |
| CLM-C11-01 | Pattern-terminated codes T_p are complete prefix codes with counts x^k / (x^k + (1-2x) c_… | Prefix property and unique parsing machine-checked in Lean … | REDISCOVERY | EXP-C11-01, EXP-C11-02 |
| CLM-C11-02 | The all-ones terminator 1^k (and 0^k) uniquely maximises the growth rate among length-k p… | written proof (proofs/paper/C11.md Theorem 2, from D_(1^k) … | REDISCOVERY | EXP-C11-02 |
| CLM-C11-03 | Unbordered terminators: F_u = x/(1-x) F_(1^k), so codeword counts are partial sums of the… | written proof (proofs/paper/C11.md Theorem 3), skeptic-revi… | REDISCOVERY | EXP-C11-06, EXP-C11-02 |
| CLM-C11-04 | T_011 is never longer than the Fibonacci code for n >= 5 and one bit shorter on all but L… | written proof (proofs/paper/C11.md Corollary 4), skeptic-re… | REDISCOVERY | EXP-C11-06 |
| CLM-C11-07 | The average gain oscillates between (2-lambda)/(lambda-1)^2 and lambda(2-lambda)/(lambda-… | written proof (proofs/paper/C11.md Proposition 5), skeptic-… | POTENTIALLY NOVEL | EXP-C11-08, EXP-C11-07 |
| CLM-C11-09 | T_011 is never longer than Fraenkel-Klein's C3 except at n = 2, 4, 8; C3 is never longer … | written proof (proofs/paper/C11.md Corollary 6, from cum_01… | REDISCOVERY | EXP-C11-09 |
| CLM-C12-01 | Divisibility games: subtract a proper divisor = v2, subtract a divisor = v2 + 1, move to … | written proof (proofs/paper/C12.md Theorem 1), skeptic-revi… | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-02 | Coprimality games: index of the smallest prime factor; the non-coprime game has g(2k) = k… | written proof (proofs/paper/C12.md Theorem 2), skeptic-revi… | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-03 | P-positions of the deleting-divisors game (subtract d | n with 1 < d < n): 0, odd numbers… | Lean 4 + Mathlib: Infinity.C12.g03_pset and Infinity.C12.g0… | REDISCOVERY | EXP-C12-02, EXP-C12-04 |
| CLM-C12-04 | Grundy function of the deleting-divisors game: v2(n) except on odd parts <= 15 | Computer-assisted (proofs/paper/C12.md Theorem 8): exact co… | POTENTIALLY NOVEL | EXP-C12-06, EXP-C12-04, EXP-C12-01 |
| CLM-C12-05 | Bitwise and quotient games: popcount, floor(log2((n+1)/3)) + 1 and floor(log2 n) | written proof (proofs/paper/C12.md Theorem 4), skeptic-revi… | REDISCOVERY | EXP-C12-01, EXP-C12-02, EXP-C12-04 |
| CLM-C12-06 | Residue lemma; subtract-a-power-of-k has the Grundy function of the subtraction game {1, … | (a) machine-checked in Lean (Infinity.C12.residue_grundy, I… | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-07 | Splitting games in which every heap can be split have g(n) = [n even] | Lean 4 + Mathlib: Infinity.C12.split_parity (axioms propext… | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-08 | Subtract-a-square and subtract-a-triangular-number have infinite density-zero P-sets and … | written proof (proofs/paper/C12.md Theorem 7) from the Furs… | REDISCOVERY | EXP-C12-03, EXP-C12-01 |
| CLM-C13-01 | Affine anchored spectra are root sets of polynomial systems - divisor-closed, CRT-closed,… | Lean 4 (complete, except the standard fact quoted as an exa… | REDISCOVERY | EXP-C13-01 |
| CLM-C13-02 | Right-normed laws (xy)z = x V(y,z) have only translation models | Lean 4 + Mathlib (translation_form, right_normed_translatio… | POTENTIALLY NOVEL | EXP-C13-03 |
| CLM-C13-03 | The W-family: anchored models of (xy)z = x(y W(z)) are the affine tables with a*c_W(a) = 1 | Lean 4 + Mathlib for the model correspondence for every W (… | POTENTIALLY NOVEL | EXP-C13-03, EXP-C13-09 |
| CLM-C13-04 | Exact finite spectra {1,3} and {1,2} for x(yz) = ((zx)x)y and x(yz) = ((xy)z)x | Lean 4 + Mathlib for N | 3 resp. N | 2 and for the existenc… | POTENTIALLY NOVEL | EXP-C13-04 |
| CLM-C13-05 | The law x = x(x(xx)) has anchored models of every size except 2 | Lean 4 + Mathlib (cube_law_no_two, cubeOp_model with an exp… | NOT ASSESSED | EXP-C13-07, EXP-C13-09 |
| CLM-C13-06 | Offset congruence closure is a sound prover of finite anchored spectra; it settles 16 of … | written soundness proof (proofs/paper/C13.md Theorem 6); ap… | NOT ASSESSED | EXP-C13-08, EXP-C13-04 |
| CLM-C13-11 | Single laws whose affine spectra are classical arithmetic sets | affine systems computed mechanically (EXP-C13-01) and Theor… | POTENTIALLY NOVEL | EXP-C13-01, EXP-C13-09 |
| CLM-C14-01 | Associativity of a local graph product is a finite identity on relations, detected by P3 … | Lean 4 + Mathlib (rel_lprod, assoc_iso, assoc_iso_nonempty,… | NOT ASSESSED | EXP-C14-01, EXP-C14-06 |
| CLM-C14-02 | Exactly 20 of the 256 local graph products are associative, 10 commutative, 8 with unit K… | Lean 4 kernel computation (assoc_codes, comm_assoc_codes by… | REDISCOVERY | EXP-C14-01, EXP-C14-06 |
| CLM-C14-03 | For local graph products, associativity and commutativity up to isomorphism are no weaker… | computer-assisted - explicit witnesses for all 236 + 224 co… | NOT ASSESSED | EXP-C14-02, EXP-C14-06 |
| CLM-C14-04 | Exactly six local products are Kronecker products in disguise (multiplicative characters) | written case analysis (proofs/paper/C14.md Theorem 4); poly… | POTENTIALLY NOVEL | EXP-C14-03 |
| CLM-C14-05 | Additive characters: only the Cartesian product and its complement-dual; every non-trivia… | written proof (proofs/paper/C14.md Theorem 5); sympy over C… | POTENTIALLY NOVEL | EXP-C14-03 |
| CLM-C14-06 | The symmetric-difference product is the Kronecker product of Seidel matrices; it acts on … | written proof (proofs/paper/C14.md Theorem 6); entry-level … | REDISCOVERY | EXP-C14-03, EXP-C14-06 |
| CLM-C14-07 | Complete bipartite graphs multiply as (order, imbalance); K2 absorbs Seidel switching | written proof (proofs/paper/C14.md Theorem 7; (c) via twin … | REDISCOVERY | EXP-C14-05, EXP-C14-06 |
| CLM-C14-09 | The Cartesian and strong product monoids of all finite graphs are isomorphic graded monoi… | written proof (proofs/paper/C14.md Theorem 9) relying on th… | REDISCOVERY | EXP-C14-04 |
| CLM-C14-10 | Numbers of prime graphs (all graphs) for the unital associative products, orders <= 15 | computer-assisted exact census (all prime factorisations of… | POTENTIALLY NOVEL | EXP-C14-04 |
| CLM-C14-11 | The lexicographic product has non-unique factorisation already at order 10 (different mul… | by hand (both sides are two disjoint 4-cycles plus two isol… | REDISCOVERY | EXP-C14-04 |
| CLM-C15-01 | Light cones of semigroups - the popcount word, Pascal exponents, bounded streaming width | Lean 4 + Mathlib for the commutative formula (ca_comm_binom… | REDISCOVERY | EXP-C15-02, EXP-C15-03 |
| CLM-C15-02 | Affine magmas - binomial light cone and an O(L log L log t) fast-forward | written proof (proofs/paper/C15.md Theorem 2); implementati… | REDISCOVERY | EXP-C15-03 |
| CLM-C15-03 | Commutative semigroups - fast-forward by exponent arithmetic | written proof (proofs/paper/C15.md Theorem 3); implementati… | NOT ASSESSED | EXP-C15-03 |
| CLM-C15-04 | The fuse magma: linear streaming width, yet an O(L) fast-forward for every t | written proof (proofs/paper/C15.md Theorem 4); fast-forward… | POTENTIALLY NOVEL | EXP-C15-02, EXP-C15-03, EXP-C15-05 |
| CLM-C15-05 | Surjective iff permutive for magmas of order at most 3; false at order 4 | computer-assisted - exact pair-graph (Garden-of-Eden) decis… | REDISCOVERY | EXP-C15-01, EXP-C15-02, EXP-C15-05 |
| CLM-C15-06 | The two-element magma automata are the elementary rules 17m | written one-line proof (proofs/paper/C15.md Theorem 6) and … | REDISCOVERY | EXP-C15-01 |
| CLM-C16-01 | The Fibonacci pair map of a magma is a permutation iff every left translation is a biject… | Lean 4 + Mathlib (pairMap_injective_iff, pairMap_bijective_… | REDISCOVERY | EXP-C16-01 |
| CLM-C16-03 | Full-period magmas are de Bruijn cycles: there are (n!)^n / n^2 of them | written proof (proofs/paper/C16.md Theorem 2) using the van… | REDISCOVERY | EXP-C16-01 |
| CLM-C16-04 | A parity condition for full periods | written proof (proofs/paper/C16.md Theorem 3, factorisation… | NOT ASSESSED | EXP-C16-02 |
| CLM-C16-05 | Full-period quasigroups are cycles in which every pair occurs once at distance 1 and once… | written proof (proofs/paper/C16.md Theorem 4); the exhausti… | POTENTIALLY NOVEL | EXP-C16-02 |
| CLM-C16-07 | Full-period quasigroups: none of order 2, 3, 4; 3360 of order 5; examples of every order … | computer-assisted - exhaustive analysis of all Latin square… | POTENTIALLY NOVEL | EXP-C16-02 |
| CLM-C16-08 | Direct products of full-period magmas of coprime orders are full-period | written proof (proofs/paper/C16.md Theorem 6, Chinese remai… | NOT ASSESSED | EXP-C16-02 |
| CLM-C16-09 | No isotope of a group of even order has a full-period Fibonacci pair map | written proof (proofs/paper/C16.md Theorem 7, parity of the… | POTENTIALLY NOVEL | EXP-C16-02 |
| CLM-C16-11 | Fixed points of the pair map are idempotents | Lean 4 + Mathlib (pairMap_fixed_iff; standard axioms only) | NOT ASSESSED | EXP-C16-01 |
| CLM-C16-12 | Affine magmas: periods are orders of companion matrices; the anchored magma x + y + 1 is … | written proof (proofs/paper/C16.md Theorem 9, conjugation t… | REDISCOVERY | EXP-C16-03 |
| CLM-C16-14 | Fibonacci sequences of nimbers: maximal period pi(2^(2^k) - 1) | written proof (proofs/paper/C16.md Theorem 10, discrete log… | REDISCOVERY | EXP-C16-03 |
| CLM-C16-15 | Laver tables: every Fibonacci orbit ends in the fixed point or one of the N - 1 two-cycle… | written proof (proofs/paper/C16.md Theorem 11) from Laver's… | POTENTIALLY NOVEL | EXP-C16-03 |
| CLM-C16-18 | Maximal Fibonacci periods of small groups | computer-assisted - exhaustive functional-graph analysis of… | NOT ASSESSED | EXP-C16-03 |
| CLM-C17-01 | Light's test: generators suffice for associativity | written proof (proofs/paper/C17.md Theorem 1, four-line clo… | REDISCOVERY | EXP-C17-01 |
| CLM-C17-02 | Associativity of an anchored magma is decided by one O(n^2) identity | written proof (proofs/paper/C17.md Corollary 2) from C06 Th… | NOT ASSESSED | EXP-C17-01, EXP-C17-02 |
| CLM-C17-03 | The Rajagopalan-Schulman randomised associativity test is one-sided | one-sidedness proved (proofs/paper/C17.md Theorem 3, biline… | REDISCOVERY | EXP-C17-01 |
| CLM-C17-05 | The anchor instance of left-distributivity singles out the Laver tables (every N <= 4096) | computer-assisted - for every N, uniqueness and existence o… | REDISCOVERY | EXP-C17-03, EXP-C17-02 |
| CLM-C17-08 | For every N, the full anchor instance of left-distributivity has a model iff N is a power… | Lean 4 proof for every N with Laver's theorem as an explici… | REDISCOVERY | EXP-C17-03 |
| CLM-C18-01 | e-transformations are bijections of strings of fixed length | Lean 4 + Mathlib (eT_injective, eT_length; standard axioms … | REDISCOVERY | EXP-C18-01 |
| CLM-C18-02 | Differences propagate forward only; forward-only tail hashes fail the strict avalanche cr… | Lean 4 + Mathlib for the persistence of differences (eT_ne_… | NOT ASSESSED | EXP-C18-01, EXP-C18-02 |
| CLM-C18-03 | The tail-information bound: an e-transformation tail carries one byte of state | Lean 4 + Mathlib for the factorisation of the tail through … | NOT ASSESSED | EXP-C18-03, EXP-C18-05 |
| CLM-C18-04 | T-function quasigroups (affine mod 256, XOR, (x + 1) XOR y) cannot mix high input bits in… | written proof (proofs/paper/C18.md Theorem 4, induction alo… | REDISCOVERY | EXP-C18-01, EXP-C18-02 |
| CLM-C18-05 | GF(2)-affine quasigroups give GF(2)-affine hashes with key-independent differences | written proof (proofs/paper/C18.md Theorem 5); one distinct… | REDISCOVERY | EXP-C18-01, EXP-C18-02 |
| CLM-C18-06 | The anchored quasigroup x + c(y): additive differences persist, and the one-pass hash is … | written proof (proofs/paper/C18.md Theorem 6); 2000/2000 on… | NOT ASSESSED | EXP-C18-01, EXP-C18-02, EXP-C18-03 |
| CLM-C18-07 | The 8-pass cascade has a bijective 64-bit state update | written proof (proofs/paper/C18.md Theorem 7, triangular co… | NOT ASSESSED | EXP-C18-05 |
| CLM-C19-01 | Every Zeckendorf game has length B(n) - sum_{i>=2} (i-1) MC_i | written proof (proofs/paper/C19.md Theorem 1; potential Psi… | REDISCOVERY | EXP-C19-02 |
| CLM-C19-02 | The split phase of the longest game ends at the lazy Fibonacci representation | written proof (proofs/paper/C19.md Theorem 2 - abelian prop… | POTENTIALLY NOVEL | EXP-C19-02 |
| CLM-C19-03 | Closed form of the longest game on a Fibonacci number: L(F_k) = F_{k+2} - k - 2 - floor((… | written proof (proofs/paper/C19.md Theorem 4) from CLM-C19-… | POTENTIALLY NOVEL | EXP-C19-01, EXP-C19-03 |
| CLM-C19-04 | A short proof that only n = F_k - 1 can be played with split moves alone (Cusenza et al.,… | written proof (proofs/paper/C19.md Corollary 3, from CLM-C1… | REDISCOVERY | EXP-C19-01, EXP-C19-02 |
| CLM-C19-07 | Exact longest games for n <= 150 and independent confirmation of the split-first strategy | computer-assisted - exhaustive longest-path dynamic program… | REDISCOVERY | EXP-C19-01 |
| CLM-C19-08 | Every multiset of Fibonacci numbers with sum n is a reachable game position | written proof (proofs/paper/C19.md Proposition 6 - undoing … | NOT ASSESSED | EXP-C19-01 |
| CLM-C19-14 | Computing the longest game with O(log^2 n) moves instead of Theta(n) | written proof (proofs/paper/C19.md Theorem 7, from Theorems… | POTENTIALLY NOVEL | EXP-C19-05, EXP-C19-04 |
| CLM-C19-15 | The deficit of the longest Zeckendorf game is O(log^2 n) - D(n) <= 1 + (t+1)(t+6)/2, so L… | written proof with a Lean-checked arithmetic core - proofs/… | NOT ASSESSED | EXP-C19-05 |
| CLM-C20-01 | aab -> ababa terminates, with derivational complexity D(n) = 2^(n-2) - 1 | written proof (proofs/paper/C20.md Theorem 1 - run encoding… | REDISCOVERY | EXP-C20-01 |
| CLM-C20-02 | aab -> babaa terminates; exact per-word derivation length and D(n) = max_b b(2^floor((n-b… | written proof (proofs/paper/C20.md Theorem 2 - a pair of a'… | POTENTIALLY NOVEL | EXP-C20-01 |
| CLM-C20-03 | The C04 extended termination census is complete - 480 of the 868 rules with |l| <= 3, |r|… | computer-assisted certificates for 860 rules (EXP-C04-02, C… | NOT ASSESSED | EXP-C04-02, EXP-C20-01 |
| CLM-C20-04 | C03 Conjecture 4.6 coincides with the Zantema-Geser characterisation | Theorem statement read verbatim by the Historian from the s… | REDISCOVERY | EXP-C03-01 |

## 2. Unproven conjectures (CONJECTURE and COMPUTATIONALLY SUPPORTED)

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C04-16 | Open: are the rewriting games of aa -> ab (Officers), aaa -> b (0.007) and aaa -> ab (0.0… | CONJECTURE | REDISCOVERY | EXP-C04-08, EXP-C04-09 |
| CLM-C05-21 | H-C05-J': none of the 12 open ETP laws x = y*T without a model of order 2 has a model of … | CONJECTURE | NOT ASSESSED | EXP-C05-12, EXP-C05-09, EXP-C05-08, EXP-C05-10 |
| CLM-C09-05 | The density of circle irreducibles is exactly 1/phi^2 | CONJECTURE | POTENTIALLY NOVEL | EXP-C09-04, EXP-C09-01 |
| CLM-C12-13 | Subtract-a-Fibonacci-number has bounded Grundy values | CONJECTURE | NOT ASSESSED | EXP-C12-03, EXP-C12-01 |
| CLM-C15-18 | Bounded streaming width implies a fast-forward | CONJECTURE | NOT ASSESSED | EXP-C15-02, EXP-C15-03 |
| CLM-C01-08 | Common-border conjecture: one-relation class counts depend only on common borders | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-05, EXP-C01-06, EXP-C01-07 |
| CLM-C01-10 | Common-border formula with exactly one common border (derivation sketch from Gray-Steinbe… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-06, EXP-C01-07, EXP-C01-08 |
| CLM-C01-11 | Converse of border containment: u -> v (|u| = |v|) is confluent iff Borders(u) is contain… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C01-08 |
| CLM-C03-11 | Loop lengths in the base family grow like k^q | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C03-04 |
| CLM-C04-12 | Complexity classes and closed forms of the 162 terminating rules with |l|, |r| <= 3 | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C04-03 |
| CLM-C05-02 | Spectrum census of the 115 nontrivial two-variable identities t = x with 2-4 operations (… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C05-01, EXP-C05-02 |
| CLM-C06-10 | Laws with finite anchored spectra {1, 2} and {1, 3} | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C06-03, EXP-C06-04 |
| CLM-C06-11 | Mirror twins of the golden and odd laws | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C06-04 |
| CLM-C07-08 | Additive periodicity is the exception among mex operations | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C07-03 |
| CLM-C08-02 | Circle products over non-Pisot base sequences are never associative | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C08-02, EXP-C08-07 |
| CLM-C08-03 | Recurrences with non-increasing coefficients and canonical initial values give associativ… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C08-02, EXP-C08-03, EXP-C08-06, EXP-C08-07 |
| CLM-C08-04 | Non-monotone associative-shift sets require a negative conjugate root | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C08-07, EXP-C08-06, EXP-C08-04, EXP-C08-03 |
| CLM-C08-08 | Associativity thresholds after the targeted search - certified lower bounds, no failure u… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C08-07, EXP-C08-06 |
| CLM-C10-06 | Multi-offset exchange rules have rule-specific average counting costs | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C10-03 |
| CLM-C11-08 | Fixed pattern-terminated codes beat classical universal codes on heavy-tailed and wide-ra… | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C11-03, EXP-C11-04, EXP-C11-05, EXP-C11-09 |
| CLM-C12-12 | Subtract-a-prime has Grundy values at most 11 | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C12-03, EXP-C12-01 |
| CLM-C13-10 | Spectra of one-variable laws are finite or cofinite | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C13-07 |
| CLM-C13-12 | Non-affine models typically exist for all sizes beyond a small threshold; no Laver-like s… | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C13-02, EXP-C13-05, EXP-C13-06 |
| CLM-C14-12 | Code 141 (EA AE AA NN) has unique factorisation on connected graphs (equivalently, symmet… | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C14-04 |
| CLM-C14-13 | H-C14-4: two-graphs form a free commutative monoid under the symmetric-difference (Kronec… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C14-05 |
| CLM-C15-07 | Census of order-3 magma automata by streaming width | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C15-02 |
| CLM-C15-13 | Affine fast-forward by operator powers | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C15-03 |
| CLM-C15-14 | Commutative-semigroup fast-forward by exponent arithmetic | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C15-03 |
| CLM-C15-15 | Fuse fast-forward by burn times | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C15-03 |
| CLM-C15-16 | Cycle detection as a generic fast-forward | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C15-04 |
| CLM-C15-17 | Earlier structures of the lab as automata | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C15-05 |
| CLM-C16-10 | Full-period quasigroups exist for every order n >= 5 | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C16-02, EXP-C16-05 |
| CLM-C16-13 | For affine magmas the maximal period equals the order of the 3x3 affine matrix | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C16-03 |
| CLM-C16-16 | Fibonacci orbits in Laver tables reach the top element within 5 steps (n <= 10) | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C16-03 |
| CLM-C16-17 | Magma Fibonacci generators are not competitive pseudo-random generators | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C16-04 |
| CLM-C16-19 | Random sampling finds full-period quasigroups where exact search fails | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C16-05, EXP-C16-02 |
| CLM-C17-04 | Benchmark - generator and anchor tests versus the exhaustive check | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C17-01 |
| CLM-C18-08 | H-C18-1: QG-LS with 2 passes and a reverse pass has BLAKE2b-level avalanche | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C18-02 |
| CLM-C18-13 | Quasigroup hashes against non-cryptographic baselines - no significant improvement | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C18-02, EXP-C18-03, EXP-C18-04, EXP-C18-05 |
| CLM-C19-05 | A two-sequence recursion for the longest Zeckendorf game on every n | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C19-03, EXP-C19-04, EXP-C19-05 |
| CLM-C19-06 | The deficit of a two-summand number depends only on the lower level and the parity of the… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C19-03 |
| CLM-C19-09 | D(n) <= floor(j^2/4) for top level j, and L is strictly increasing | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C19-03 |

## 3. Potentially novel ideas

Novelty means only that no equivalent was found in the sources searched (recorded per claim in `novelty_basis`). It is never a confirmed priority claim.

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-08 | Common-border conjecture: one-relation class counts depend only on common borders | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-05, EXP-C01-06, EXP-C01-07 |
| CLM-C01-10 | Common-border formula with exactly one common border (derivation sketch from Gray-Steinbe… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-06, EXP-C01-07, EXP-C01-08 |
| CLM-C02-04 | Carry rules with sum b = m never terminate from all unary starts (uniform glider) | PROVEN | POTENTIALLY NOVEL | EXP-C02-03 |
| CLM-C02-05 | Termination classification for all 189 small carry rules (computer-assisted) | PROVEN | POTENTIALLY NOVEL | EXP-C02-03 |
| CLM-C02-11 | Termination classification of carry rules: terminating from every unary start iff sum b <… | PROVEN | POTENTIALLY NOVEL | EXP-C02-03, EXP-C02-07 |
| CLM-C04-09 | The rule aab -> ba has derivational complexity D(n) = n - 1 - min{k : 2^k + k >= n} (non-… | PROVEN | POTENTIALLY NOVEL | EXP-C04-03, EXP-C04-04 |
| CLM-C04-10 | Identity: OEIS A247983 (truncation index of the series for log 2) equals D(n+2) for aab -… | PROVEN | POTENTIALLY NOVEL | EXP-C04-09, EXP-C04-10 |
| CLM-C04-11 | H-C04-G (second part): every terminating rule has a rational complexity generating functi… | REFUTED | POTENTIALLY NOVEL | EXP-C04-03, EXP-C04-04 |
| CLM-C05-13 | Law 1313, x = y(((yx)x)y), has no model of order 8 or 10 (DRAT-certified); its orders up … | PROVEN | POTENTIALLY NOVEL | EXP-C05-08 |
| CLM-C05-15 | Fifteen new certified spectrum gaps for open ETP laws x = y*T at orders 8-10 | PROVEN | POTENTIALLY NOVEL | EXP-C05-09 |
| CLM-C05-16 | Nine new certified spectrum gaps at orders 11-13 for the quasigroup laws 1076, 1110, 1279… | PROVEN | POTENTIALLY NOVEL | EXP-C05-10, EXP-C05-07 |
| CLM-C05-17 | Complete spectra up to order 10 of the 13 open ETP laws of the form x = y*T | PROVEN | POTENTIALLY NOVEL | EXP-C05-12, EXP-C05-09, EXP-C05-08, EXP-C05-03, EXP-C05-07 |
| CLM-C05-20 | Law 677 at order 12: a model exists iff one of 57 explicit case CNFs is satisfiable | PROVEN | POTENTIALLY NOVEL | EXP-C05-11 |
| CLM-C05-22 | The spectrum of ETP law 501, x = y(y(x(xy))), is exactly {n : n = 0, 1 (mod 4)} | PROVEN | POTENTIALLY NOVEL | EXP-C05-15, EXP-C05-09, EXP-C05-12, EXP-C05-06 |
| CLM-C06-04 | H-C06-2: a restricted anchored spectrum is special to left-distributivity (refuted) | REFUTED | POTENTIALLY NOVEL | EXP-C06-03 |
| CLM-C06-06 | An 'odd' law: (xy)z = x((yz)z) has an anchored model exactly for odd N, and it is unique | PROVEN | POTENTIALLY NOVEL | EXP-C06-03, EXP-C06-04 |
| CLM-C06-07 | A 'golden' law: anchored models of (xy)z = x(y(zz)) correspond to roots of a^2 + a = 1 mo… | PROVEN | POTENTIALLY NOVEL | EXP-C06-04 |
| CLM-C06-09 | H-C06-3: anchored spectra are affine spectra (refuted) | REFUTED | POTENTIALLY NOVEL | EXP-C06-04 |
| CLM-C06-10 | Laws with finite anchored spectra {1, 2} and {1, 3} | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C06-03, EXP-C06-04 |
| CLM-C06-11 | Mirror twins of the golden and odd laws | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C06-04 |
| CLM-C07-01 | The associative mex operations are 0, projections, min, +, XOR, nim-product and four rela… | PROVEN | POTENTIALLY NOVEL | EXP-C07-01 |
| CLM-C07-05 | The Jacobsthal row: row 2 of f(a,b) = mex{f(a',b) XOR f(a,b')} swaps the blocks [2^k - J_… | PROVEN | POTENTIALLY NOVEL | EXP-C07-03 |
| CLM-C08-02 | Circle products over non-Pisot base sequences are never associative | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C08-02, EXP-C08-07 |
| CLM-C08-04 | Non-monotone associative-shift sets require a negative conjugate root | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C08-07, EXP-C08-06, EXP-C08-04, EXP-C08-03 |
| CLM-C09-03 | Window obstruction: at least a proportion 1/phi^2 of all integers are circle-irreducible | PROVEN | POTENTIALLY NOVEL | EXP-C09-04 |
| CLM-C09-04 | H-C09-1: circle irreducibles have density 0 like primes (refuted) | REFUTED | POTENTIALLY NOVEL | EXP-C09-01, EXP-C09-04 |
| CLM-C09-05 | The density of circle irreducibles is exactly 1/phi^2 | CONJECTURE | POTENTIALLY NOVEL | EXP-C09-04, EXP-C09-01 |
| CLM-C09-06 | Factorisation lengths are bounded by the conjugate coordinate | PROVEN | POTENTIALLY NOVEL | EXP-C09-04 |
| CLM-C09-08 | Factorisation statistics of the circle semigroup up to 2e5 | PROVEN | POTENTIALLY NOVEL | EXP-C09-01, EXP-C09-02 |
| CLM-C10-06 | Multi-offset exchange rules have rule-specific average counting costs | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C10-03 |
| CLM-C11-07 | The average gain oscillates between (2-lambda)/(lambda-1)^2 and lambda(2-lambda)/(lambda-… | PROVEN | POTENTIALLY NOVEL | EXP-C11-08, EXP-C11-07 |
| CLM-C12-04 | Grundy function of the deleting-divisors game: v2(n) except on odd parts <= 15 | PROVEN | POTENTIALLY NOVEL | EXP-C12-06, EXP-C12-04, EXP-C12-01 |
| CLM-C13-02 | Right-normed laws (xy)z = x V(y,z) have only translation models | PROVEN | POTENTIALLY NOVEL | EXP-C13-03 |
| CLM-C13-03 | The W-family: anchored models of (xy)z = x(y W(z)) are the affine tables with a*c_W(a) = 1 | PROVEN | POTENTIALLY NOVEL | EXP-C13-03, EXP-C13-09 |
| CLM-C13-04 | Exact finite spectra {1,3} and {1,2} for x(yz) = ((zx)x)y and x(yz) = ((xy)z)x | PROVEN | POTENTIALLY NOVEL | EXP-C13-04 |
| CLM-C13-11 | Single laws whose affine spectra are classical arithmetic sets | PROVEN | POTENTIALLY NOVEL | EXP-C13-01, EXP-C13-09 |
| CLM-C14-04 | Exactly six local products are Kronecker products in disguise (multiplicative characters) | PROVEN | POTENTIALLY NOVEL | EXP-C14-03 |
| CLM-C14-05 | Additive characters: only the Cartesian product and its complement-dual; every non-trivia… | PROVEN | POTENTIALLY NOVEL | EXP-C14-03 |
| CLM-C14-10 | Numbers of prime graphs (all graphs) for the unital associative products, orders <= 15 | PROVEN | POTENTIALLY NOVEL | EXP-C14-04 |
| CLM-C14-13 | H-C14-4: two-graphs form a free commutative monoid under the symmetric-difference (Kronec… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C14-05 |
| CLM-C15-04 | The fuse magma: linear streaming width, yet an O(L) fast-forward for every t | PROVEN | POTENTIALLY NOVEL | EXP-C15-02, EXP-C15-03, EXP-C15-05 |
| CLM-C15-07 | Census of order-3 magma automata by streaming width | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C15-02 |
| CLM-C15-15 | Fuse fast-forward by burn times | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C15-03 |
| CLM-C16-05 | Full-period quasigroups are cycles in which every pair occurs once at distance 1 and once… | PROVEN | POTENTIALLY NOVEL | EXP-C16-02 |
| CLM-C16-07 | Full-period quasigroups: none of order 2, 3, 4; 3360 of order 5; examples of every order … | PROVEN | POTENTIALLY NOVEL | EXP-C16-02 |
| CLM-C16-09 | No isotope of a group of even order has a full-period Fibonacci pair map | PROVEN | POTENTIALLY NOVEL | EXP-C16-02 |
| CLM-C16-15 | Laver tables: every Fibonacci orbit ends in the fixed point or one of the N - 1 two-cycle… | PROVEN | POTENTIALLY NOVEL | EXP-C16-03 |
| CLM-C19-02 | The split phase of the longest game ends at the lazy Fibonacci representation | PROVEN | POTENTIALLY NOVEL | EXP-C19-02 |
| CLM-C19-03 | Closed form of the longest game on a Fibonacci number: L(F_k) = F_{k+2} - k - 2 - floor((… | PROVEN | POTENTIALLY NOVEL | EXP-C19-01, EXP-C19-03 |
| CLM-C19-05 | A two-sequence recursion for the longest Zeckendorf game on every n | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C19-03, EXP-C19-04, EXP-C19-05 |
| CLM-C19-06 | The deficit of a two-summand number depends only on the lower level and the parity of the… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C19-03 |
| CLM-C19-14 | Computing the longest game with O(log^2 n) moves instead of Theta(n) | PROVEN | POTENTIALLY NOVEL | EXP-C19-05, EXP-C19-04 |
| CLM-C20-02 | aab -> babaa terminates; exact per-word derivation length and D(n) = max_b b(2^floor((n-b… | PROVEN | POTENTIALLY NOVEL | EXP-C20-01 |

## 4. Rediscovered existing mathematics

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-01 | Symbol counts are the complete invariant of the commutation congruence | PROVEN | REDISCOVERY | EXP-C01-01 |
| CLM-C01-02 | One symbol, one relation a^m = a^(m+p) gives exactly m+p classes (index m, period p) | PROVEN | REDISCOVERY | EXP-C01-02 |
| CLM-C01-03 | Several one-symbol relations have index min m_i and period gcd(n_i - m_i) | PROVEN | REDISCOVERY | EXP-C01-02 |
| CLM-C01-04 | Multiplication emerges as composition of substitutions; with two symbols it is non-commut… | PROVEN | REDISCOVERY | EXP-C01-03 |
| CLM-C01-05 | H-C01-4: a single rearranging relation generates counting equivalence on long words (refu… | REFUTED | REDISCOVERY | EXP-C01-04 |
| CLM-C01-06 | Border-containment theorem for one length-preserving relation | PROVEN | REDISCOVERY | EXP-C01-04, EXP-C01-05, EXP-C01-07 |
| CLM-C01-07 | Common-border formula proved for 1632 specific relations by verified finite completions | PROVEN | REDISCOVERY | EXP-C01-07 |
| CLM-C01-09 | Common-border formula when u and v share no border (c = 1) - consequence of published res… | PROVEN | REDISCOVERY | EXP-C01-06, EXP-C01-07, EXP-C01-08 |
| CLM-C01-11 | Converse of border containment: u -> v (|u| = |v|) is confluent iff Borders(u) is contain… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C01-08 |
| CLM-C02-01 | Integer bases emerge as normal forms of the exchange rule b[k] -> [k+1] | PROVEN | REDISCOVERY | EXP-C02-01 |
| CLM-C02-02 | Abelian property of carry rules (order of exchanges is irrelevant) | PROVEN | REDISCOVERY | EXP-C02-01, EXP-C02-04 |
| CLM-C02-03 | Termination dichotomy for carry rules away from sum b = m | PROVEN | REDISCOVERY | EXP-C02-03 |
| CLM-C02-06 | H-C02-4: every terminating carry rule gives unique stable representations (refuted) | REFUTED | REDISCOVERY | EXP-C02-04 |
| CLM-C02-07 | Uniqueness of representations when the reduced carry polynomial is primitive and irreduci… | PROVEN | REDISCOVERY | EXP-C02-05 |
| CLM-C02-08 | Exchange representations respect the radix order | PROVEN | REDISCOVERY | EXP-C02-03 |
| CLM-C02-09 | The Fibonacci exchange system terminates at the Zeckendorf representation; shortest deriv… | PROVEN | REDISCOVERY | EXP-C02-02, EXP-C02-06 |
| CLM-C02-10 | Longest Fibonacci exchange derivations (longest Zeckendorf games) for n <= 40 | PROVEN | REDISCOVERY | EXP-C02-02, EXP-C02-06 |
| CLM-C03-01 | A one-rule system that decreases the count of some letter terminates | PROVEN | REDISCOVERY | EXP-C03-01 |
| CLM-C03-02 | Conserving rules terminate (s = p or r = q) | PROVEN | REDISCOVERY | EXP-C03-01 |
| CLM-C03-03 | Self-embedding derivations prove non-termination; the doubling region r >= 2q, s >= 2p al… | PROVEN | REDISCOVERY | EXP-C03-01, EXP-C03-02 |
| CLM-C03-04 | 011 -> 11100 is non-terminating although r < 2q | PROVEN | REDISCOVERY | EXP-C03-01 |
| CLM-C03-05 | Lifting lemma - loops transfer along letter morphisms (explains divisibility) | PROVEN | REDISCOVERY | EXP-C03-03, EXP-C03-04 |
| CLM-C03-06 | Classification of 601 of the 625 rules with p, q, r, s <= 5 (computer-assisted) | PROVEN | REDISCOVERY | EXP-C03-01, EXP-C03-02, EXP-C03-03 |
| CLM-C03-07 | H-C03-1: terminates iff some letter count never grows (refuted) | REFUTED | REDISCOVERY | EXP-C03-01, EXP-C03-02 |
| CLM-C03-08 | H-C03-2: terminates iff r < 2q or s < 2p (refuted) | REFUTED | REDISCOVERY | EXP-C03-01, EXP-C03-02 |
| CLM-C03-09 | H-C03-3: non-terminating iff both counts grow and (r >= 2q or s >= 2p) (inconclusive, evi… | REFUTED | REDISCOVERY | EXP-C03-02, EXP-C03-03 |
| CLM-C03-10 | Divisibility characterization of termination for 0^p 1^q -> 1^r 0^s (H-C03-4) | PROVEN | REDISCOVERY | EXP-C03-02, EXP-C03-03, EXP-C03-04 |
| CLM-C03-11 | Loop lengths in the base family grow like k^q | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C03-04 |
| CLM-C04-01 | Termination census of one-rule systems with |l|, |r| <= 3: non-terminating iff l is a fac… | PROVEN | REDISCOVERY | EXP-C04-01 |
| CLM-C04-02 | H-C04-0: a rule with |l| <= 3 terminates iff l is not a factor of r (refuted) | REFUTED | REDISCOVERY | EXP-C04-02 |
| CLM-C04-03 | The rules aab -> ababa and aab -> babaa (and their six symmetric images) terminate | PROVEN | REDISCOVERY | EXP-C04-02, EXP-C20-01 |
| CLM-C04-04 | ab -> ba: every derivation has inv(w) steps, D(n) = floor(n^2/4), P-positions = even inve… | PROVEN | REDISCOVERY | EXP-C04-03, EXP-C04-07 |
| CLM-C04-05 | One-rule systems with an unbordered left-hand side have random descent (Lean-verified) | PROVEN | REDISCOVERY | EXP-C04-05 |
| CLM-C04-06 | Every one-rule system has a constant-step potential; for terminating ones confluence is e… | PROVEN | REDISCOVERY | EXP-C04-05, EXP-C04-06 |
| CLM-C04-07 | H-C04-1: random descent iff the left-hand side is unbordered (refuted) | REFUTED | REDISCOVERY | EXP-C04-05 |
| CLM-C04-08 | Rewriting games of random-descent rules are parity games (Grundy value = D(w) mod 2) | PROVEN | REDISCOVERY | EXP-C04-07 |
| CLM-C04-12 | Complexity classes and closed forms of the 162 terminating rules with |l|, |r| <= 3 | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C04-03 |
| CLM-C04-13 | Rewriting games with lhs a^k are take-and-break games: aa -> b is Dawson's Kayles, aa -> … | PROVEN | REDISCOVERY | EXP-C04-07, EXP-C04-08 |
| CLM-C04-14 | H-C04-6: Grundy values of rewriting games never exceed 3 (refuted) | REFUTED | REDISCOVERY | EXP-C04-08 |
| CLM-C04-15 | The rewriting game of aa -> b on a^n has Grundy values periodic with period 34 from n = 53 | PROVEN | REDISCOVERY | EXP-C04-08 |
| CLM-C04-16 | Open: are the rewriting games of aa -> ab (Officers), aaa -> b (0.007) and aaa -> ab (0.0… | CONJECTURE | REDISCOVERY | EXP-C04-08, EXP-C04-09 |
| CLM-C05-02 | Spectrum census of the 115 nontrivial two-variable identities t = x with 2-4 operations (… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C05-01, EXP-C05-02 |
| CLM-C05-04 | Law 167, x = (y*x)*(x*y): every finite model has order 0 or 1 mod 4 | PROVEN | REDISCOVERY | EXP-C05-01 |
| CLM-C05-05 | Identities x = y*s(x, y) make every left translation of a finite model bijective | PROVEN | REDISCOVERY | EXP-C05-03 |
| CLM-C05-07 | New spectrum memberships for open ETP laws: 677 has models of orders 5, 7, 9; 1286, 1313 … | PROVEN | REDISCOVERY | EXP-C05-03, EXP-C05-04 |
| CLM-C05-08 | New spectrum gaps for open ETP laws (certified UNSAT): 501 has no models of orders 6, 7; … | PROVEN | REDISCOVERY | EXP-C05-03, EXP-C05-06 |
| CLM-C05-10 | Linear models over finite fields: the orders q <= 128 at which the 15 open laws have a mo… | PROVEN | REDISCOVERY | EXP-C05-07 |
| CLM-C05-11 | Law 677, x = y(x((yx)y)), has no model of order 8 (rediscovery; DRAT-certified) | PROVEN | REDISCOVERY | EXP-C05-08 |
| CLM-C05-12 | Law 677 has no model of order 10 (DRAT-certified); its orders up to 10 are exactly 1, 5, … | PROVEN | REDISCOVERY | EXP-C05-08 |
| CLM-C05-19 | Finite models of any law x = y*(S*y) are quasigroups (Lean); this covers the ETP laws 107… | PROVEN | REDISCOVERY |  |
| CLM-C05-23 | Finite models of the ETP laws 704 and 883 are quasigroups (Lean); for 704 squaring is a b… | PROVEN | REDISCOVERY |  |
| CLM-C06-01 | Left-distributivity with a successor anchor: the Laver tables (rediscovery) | PROVEN | REDISCOVERY | EXP-C06-01, EXP-C06-02 |
| CLM-C06-02 | Anchored associativity forces x*y = x + y + 1, for every N | PROVEN | REDISCOVERY | EXP-C06-02 |
| CLM-C06-03 | Anchored right-distributivity forces x*y = x + 1, for every N | PROVEN | REDISCOVERY | EXP-C06-02 |
| CLM-C06-05 | Anchored right-permutable magmas are x*y = x + c(y); there are N^(N-1) of them | PROVEN | REDISCOVERY | EXP-C06-02 |
| CLM-C06-08 | Anchored left-permutable magmas are commutative monoids in disguise (counted by OEIS A058… | PROVEN | REDISCOVERY | EXP-C06-02 |
| CLM-C06-12 | Anchored spectra are closed under coprime products | PROVEN | REDISCOVERY | EXP-C06-03, EXP-C06-04 |
| CLM-C08-01 | Every shifted Knuth product a o_t b = sum F(k+l+t) over Zeckendorf indices is associative… | PROVEN | REDISCOVERY | EXP-C08-01, EXP-C08-03, EXP-C08-05 |
| CLM-C08-03 | Recurrences with non-increasing coefficients and canonical initial values give associativ… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C08-02, EXP-C08-03, EXP-C08-06, EXP-C08-07 |
| CLM-C08-05 | Measured associativity thresholds for 46 base sequences (refuted - five of the eight quot… | REFUTED | REDISCOVERY | EXP-C08-02, EXP-C08-03, EXP-C08-06, EXP-C08-07 |
| CLM-C08-06 | H-C08-1: Knuth's associative circle product is an isolated case (refuted) | REFUTED | REDISCOVERY | EXP-C08-01, EXP-C08-02 |
| CLM-C08-07 | Corrected associativity thresholds - certified lower bounds and searched ranges | REFUTED | REDISCOVERY | EXP-C08-06, EXP-C08-07 |
| CLM-C08-08 | Associativity thresholds after the targeted search - certified lower bounds, no failure u… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C08-07, EXP-C08-06 |
| CLM-C09-01 | Knuth's circle semigroup embeds in Z[phi]; Fibonacci numbers are its units-images | PROVEN | REDISCOVERY | EXP-C09-03 |
| CLM-C09-02 | H-C09-2: factorisation into circle irreducibles is unique (refuted) | REFUTED | REDISCOVERY | EXP-C09-02 |
| CLM-C09-07 | The norm N(n) = n*^2 + n n* - n^2 is multiplicative for the circle product | PROVEN | REDISCOVERY | EXP-C09-03 |
| CLM-C10-01 | Average cost of counting in classical representations (b/(b-1), e-1, 1) | PROVEN | REDISCOVERY | EXP-C10-01 |
| CLM-C10-02 | Zeckendorf counting: T_m = 2 G_m - ceil(m/2) - 2, average cost 2 | PROVEN | REDISCOVERY | EXP-C10-02, EXP-C10-04 |
| CLM-C10-03 | H-C10-0: Zeckendorf counting is cheaper than binary counting (refuted) | REFUTED | REDISCOVERY | EXP-C10-01, EXP-C10-02 |
| CLM-C10-04 | Exchange systems fire 1/(m - sum b) times per increment on average | PROVEN | REDISCOVERY | EXP-C10-03 |
| CLM-C10-05 | Single-offset exchange rules cost exactly firings + 1 per increment (average 1 + 1/(m - q… | PROVEN | REDISCOVERY | EXP-C10-03 |
| CLM-C10-07 | Skew binary counting has worst-case cost 2 and average 3/2 | PROVEN | REDISCOVERY | EXP-C10-01 |
| CLM-C11-01 | Pattern-terminated codes T_p are complete prefix codes with counts x^k / (x^k + (1-2x) c_… | PROVEN | REDISCOVERY | EXP-C11-01, EXP-C11-02 |
| CLM-C11-02 | The all-ones terminator 1^k (and 0^k) uniquely maximises the growth rate among length-k p… | PROVEN | REDISCOVERY | EXP-C11-02 |
| CLM-C11-03 | Unbordered terminators: F_u = x/(1-x) F_(1^k), so codeword counts are partial sums of the… | PROVEN | REDISCOVERY | EXP-C11-06, EXP-C11-02 |
| CLM-C11-04 | T_011 is never longer than the Fibonacci code for n >= 5 and one bit shorter on all but L… | PROVEN | REDISCOVERY | EXP-C11-06 |
| CLM-C11-09 | T_011 is never longer than Fraenkel-Klein's C3 except at n = 2, 4, 8; C3 is never longer … | PROVEN | REDISCOVERY | EXP-C11-09 |
| CLM-C12-01 | Divisibility games: subtract a proper divisor = v2, subtract a divisor = v2 + 1, move to … | PROVEN | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-02 | Coprimality games: index of the smallest prime factor; the non-coprime game has g(2k) = k… | PROVEN | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-03 | P-positions of the deleting-divisors game (subtract d | n with 1 < d < n): 0, odd numbers… | PROVEN | REDISCOVERY | EXP-C12-02, EXP-C12-04 |
| CLM-C12-05 | Bitwise and quotient games: popcount, floor(log2((n+1)/3)) + 1 and floor(log2 n) | PROVEN | REDISCOVERY | EXP-C12-01, EXP-C12-02, EXP-C12-04 |
| CLM-C12-06 | Residue lemma; subtract-a-power-of-k has the Grundy function of the subtraction game {1, … | PROVEN | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-07 | Splitting games in which every heap can be split have g(n) = [n even] | PROVEN | REDISCOVERY | EXP-C12-01, EXP-C12-02 |
| CLM-C12-08 | Subtract-a-square and subtract-a-triangular-number have infinite density-zero P-sets and … | PROVEN | REDISCOVERY | EXP-C12-03, EXP-C12-01 |
| CLM-C12-12 | Subtract-a-prime has Grundy values at most 11 | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C12-03, EXP-C12-01 |
| CLM-C13-01 | Affine anchored spectra are root sets of polynomial systems - divisor-closed, CRT-closed,… | PROVEN | REDISCOVERY | EXP-C13-01 |
| CLM-C14-02 | Exactly 20 of the 256 local graph products are associative, 10 commutative, 8 with unit K… | PROVEN | REDISCOVERY | EXP-C14-01, EXP-C14-06 |
| CLM-C14-06 | The symmetric-difference product is the Kronecker product of Seidel matrices; it acts on … | PROVEN | REDISCOVERY | EXP-C14-03, EXP-C14-06 |
| CLM-C14-07 | Complete bipartite graphs multiply as (order, imbalance); K2 absorbs Seidel switching | PROVEN | REDISCOVERY | EXP-C14-05, EXP-C14-06 |
| CLM-C14-09 | The Cartesian and strong product monoids of all finite graphs are isomorphic graded monoi… | PROVEN | REDISCOVERY | EXP-C14-04 |
| CLM-C14-11 | The lexicographic product has non-unique factorisation already at order 10 (different mul… | PROVEN | REDISCOVERY | EXP-C14-04 |
| CLM-C15-01 | Light cones of semigroups - the popcount word, Pascal exponents, bounded streaming width | PROVEN | REDISCOVERY | EXP-C15-02, EXP-C15-03 |
| CLM-C15-02 | Affine magmas - binomial light cone and an O(L log L log t) fast-forward | PROVEN | REDISCOVERY | EXP-C15-03 |
| CLM-C15-05 | Surjective iff permutive for magmas of order at most 3; false at order 4 | PROVEN | REDISCOVERY | EXP-C15-01, EXP-C15-02, EXP-C15-05 |
| CLM-C15-06 | The two-element magma automata are the elementary rules 17m | PROVEN | REDISCOVERY | EXP-C15-01 |
| CLM-C15-13 | Affine fast-forward by operator powers | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C15-03 |
| CLM-C15-16 | Cycle detection as a generic fast-forward | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C15-04 |
| CLM-C16-01 | The Fibonacci pair map of a magma is a permutation iff every left translation is a biject… | PROVEN | REDISCOVERY | EXP-C16-01 |
| CLM-C16-03 | Full-period magmas are de Bruijn cycles: there are (n!)^n / n^2 of them | PROVEN | REDISCOVERY | EXP-C16-01 |
| CLM-C16-12 | Affine magmas: periods are orders of companion matrices; the anchored magma x + y + 1 is … | PROVEN | REDISCOVERY | EXP-C16-03 |
| CLM-C16-14 | Fibonacci sequences of nimbers: maximal period pi(2^(2^k) - 1) | PROVEN | REDISCOVERY | EXP-C16-03 |
| CLM-C16-17 | Magma Fibonacci generators are not competitive pseudo-random generators | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C16-04 |
| CLM-C17-01 | Light's test: generators suffice for associativity | PROVEN | REDISCOVERY | EXP-C17-01 |
| CLM-C17-03 | The Rajagopalan-Schulman randomised associativity test is one-sided | PROVEN | REDISCOVERY | EXP-C17-01 |
| CLM-C17-04 | Benchmark - generator and anchor tests versus the exhaustive check | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C17-01 |
| CLM-C17-05 | The anchor instance of left-distributivity singles out the Laver tables (every N <= 4096) | PROVEN | REDISCOVERY | EXP-C17-03, EXP-C17-02 |
| CLM-C17-08 | For every N, the full anchor instance of left-distributivity has a model iff N is a power… | PROVEN | REDISCOVERY | EXP-C17-03 |
| CLM-C18-01 | e-transformations are bijections of strings of fixed length | PROVEN | REDISCOVERY | EXP-C18-01 |
| CLM-C18-04 | T-function quasigroups (affine mod 256, XOR, (x + 1) XOR y) cannot mix high input bits in… | PROVEN | REDISCOVERY | EXP-C18-01, EXP-C18-02 |
| CLM-C18-05 | GF(2)-affine quasigroups give GF(2)-affine hashes with key-independent differences | PROVEN | REDISCOVERY | EXP-C18-01, EXP-C18-02 |
| CLM-C19-01 | Every Zeckendorf game has length B(n) - sum_{i>=2} (i-1) MC_i | PROVEN | REDISCOVERY | EXP-C19-02 |
| CLM-C19-04 | A short proof that only n = F_k - 1 can be played with split moves alone (Cusenza et al.,… | PROVEN | REDISCOVERY | EXP-C19-01, EXP-C19-02 |
| CLM-C19-07 | Exact longest games for n <= 150 and independent confirmation of the split-first strategy | PROVEN | REDISCOVERY | EXP-C19-01 |
| CLM-C20-01 | aab -> ababa terminates, with derivational complexity D(n) = 2^(n-2) - 1 | PROVEN | REDISCOVERY | EXP-C20-01 |
| CLM-C20-04 | C03 Conjecture 4.6 coincides with the Zantema-Geser characterisation | PROVEN | REDISCOVERY | EXP-C03-01 |

## 5. Practical algorithmic results

| Claim | Title | Outcome | Verification | Evidence |
|---|---|---|---|---|
| CLM-C11-08 | Fixed pattern-terminated codes beat classical universal codes on heavy-tailed and wide-ra… | MIXED | COMPUTATIONALLY SUPPORTED | EXP-C11-03, EXP-C11-04, EXP-C11-05, EXP-C11-09 |
| CLM-C15-13 | Affine fast-forward by operator powers | IMPROVEMENT | COMPUTATIONALLY SUPPORTED | EXP-C15-03 |
| CLM-C15-14 | Commutative-semigroup fast-forward by exponent arithmetic | MIXED | COMPUTATIONALLY SUPPORTED | EXP-C15-03 |
| CLM-C15-15 | Fuse fast-forward by burn times | IMPROVEMENT | COMPUTATIONALLY SUPPORTED | EXP-C15-03 |
| CLM-C15-16 | Cycle detection as a generic fast-forward | MIXED | COMPUTATIONALLY SUPPORTED | EXP-C15-04 |
| CLM-C16-17 | Magma Fibonacci generators are not competitive pseudo-random generators | NO IMPROVEMENT | COMPUTATIONALLY SUPPORTED | EXP-C16-04 |
| CLM-C17-04 | Benchmark - generator and anchor tests versus the exhaustive check | MIXED | COMPUTATIONALLY SUPPORTED | EXP-C17-01 |
| CLM-C18-13 | Quasigroup hashes against non-cryptographic baselines - no significant improvement | NO IMPROVEMENT | COMPUTATIONALLY SUPPORTED | EXP-C18-02, EXP-C18-03, EXP-C18-04, EXP-C18-05 |
| CLM-C19-14 | Computing the longest game with O(log^2 n) moves instead of Theta(n) | IMPROVEMENT | PROVEN | EXP-C19-05, EXP-C19-04 |

## 6. Refuted hypotheses

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-05 | H-C01-4: a single rearranging relation generates counting equivalence on long words (refu… | REFUTED | REDISCOVERY | EXP-C01-04 |
| CLM-C02-06 | H-C02-4: every terminating carry rule gives unique stable representations (refuted) | REFUTED | REDISCOVERY | EXP-C02-04 |
| CLM-C03-07 | H-C03-1: terminates iff some letter count never grows (refuted) | REFUTED | REDISCOVERY | EXP-C03-01, EXP-C03-02 |
| CLM-C03-08 | H-C03-2: terminates iff r < 2q or s < 2p (refuted) | REFUTED | REDISCOVERY | EXP-C03-01, EXP-C03-02 |
| CLM-C03-09 | H-C03-3: non-terminating iff both counts grow and (r >= 2q or s >= 2p) (inconclusive, evi… | REFUTED | REDISCOVERY | EXP-C03-02, EXP-C03-03 |
| CLM-C04-02 | H-C04-0: a rule with |l| <= 3 terminates iff l is not a factor of r (refuted) | REFUTED | REDISCOVERY | EXP-C04-02 |
| CLM-C04-07 | H-C04-1: random descent iff the left-hand side is unbordered (refuted) | REFUTED | REDISCOVERY | EXP-C04-05 |
| CLM-C04-11 | H-C04-G (second part): every terminating rule has a rational complexity generating functi… | REFUTED | POTENTIALLY NOVEL | EXP-C04-03, EXP-C04-04 |
| CLM-C04-14 | H-C04-6: Grundy values of rewriting games never exceed 3 (refuted) | REFUTED | REDISCOVERY | EXP-C04-08 |
| CLM-C05-01 | H-C05-1: a single identity t = x cannot restrict the orders of its finite models (refuted) | REFUTED | NOT ASSESSED | EXP-C05-01 |
| CLM-C05-03 | H-C05-Q: nontrivial identities t = x force their finite models to be quasigroups (refuted) | REFUTED | NOT ASSESSED | EXP-C05-01, EXP-C05-02 |
| CLM-C05-06 | H-C05-A: full spectrum iff affine models over every Z_n (refuted) | REFUTED | NOT ASSESSED | EXP-C05-05, EXP-C05-01 |
| CLM-C05-09 | Laws 677 and 1313 have spectrum {1} together with all odd n >= 5 (refuted - both have mod… | REFUTED | NOT ASSESSED | EXP-C05-03, EXP-C05-02, EXP-C05-07 |
| CLM-C05-18 | H-C05-J: a law x = y*T without a model of order 2 has no model of any order n = 2 (mod 4)… | REFUTED | NOT ASSESSED | EXP-C05-01, EXP-C05-12, EXP-C05-09, EXP-C05-08 |
| CLM-C06-04 | H-C06-2: a restricted anchored spectrum is special to left-distributivity (refuted) | REFUTED | POTENTIALLY NOVEL | EXP-C06-03 |
| CLM-C06-09 | H-C06-3: anchored spectra are affine spectra (refuted) | REFUTED | POTENTIALLY NOVEL | EXP-C06-04 |
| CLM-C07-02 | H-C07-1: only nim-sum and nim-product are non-trivially associative (refuted) | REFUTED | NOT ASSESSED | EXP-C07-01 |
| CLM-C07-04 | H-C07-2: commutative mex operations are closed on the Fermat segments [0, 2^(2^m)) (refut… | REFUTED | NOT ASSESSED | EXP-C07-01 |
| CLM-C07-06 | H-C07-4: every row of every mex operation is eventually additively periodic (refuted) | REFUTED | NOT ASSESSED | EXP-C07-03 |
| CLM-C07-07 | H-C07-3: the diagonals of commutative mex operations are known sequences (refuted) | REFUTED | NOT ASSESSED | EXP-C07-02 |
| CLM-C08-05 | Measured associativity thresholds for 46 base sequences (refuted - five of the eight quot… | REFUTED | REDISCOVERY | EXP-C08-02, EXP-C08-03, EXP-C08-06, EXP-C08-07 |
| CLM-C08-06 | H-C08-1: Knuth's associative circle product is an isolated case (refuted) | REFUTED | REDISCOVERY | EXP-C08-01, EXP-C08-02 |
| CLM-C08-07 | Corrected associativity thresholds - certified lower bounds and searched ranges | REFUTED | REDISCOVERY | EXP-C08-06, EXP-C08-07 |
| CLM-C09-02 | H-C09-2: factorisation into circle irreducibles is unique (refuted) | REFUTED | REDISCOVERY | EXP-C09-02 |
| CLM-C09-04 | H-C09-1: circle irreducibles have density 0 like primes (refuted) | REFUTED | POTENTIALLY NOVEL | EXP-C09-01, EXP-C09-04 |
| CLM-C10-03 | H-C10-0: Zeckendorf counting is cheaper than binary counting (refuted) | REFUTED | REDISCOVERY | EXP-C10-01, EXP-C10-02 |
| CLM-C11-05 | H-C11-2: 1^k is the best length-k terminator beyond small n (refuted at practical sizes) | REFUTED | NOT ASSESSED | EXP-C11-02 |
| CLM-C11-06 | Average gain of an unbordered terminator over 1^k: log_lambda(1/(lambda-1)), then converg… | REFUTED | NOT ASSESSED | EXP-C11-06, EXP-C11-07 |
| CLM-C12-10 | H-C12-1: Grundy values of divisibility/coprimality games depend only on the prime signatu… | REFUTED | NOT ASSESSED | EXP-C12-05 |
| CLM-C12-11 | H-C12-2: sparse move sets keep a positive density of P-positions (refuted) | REFUTED | NOT ASSESSED | EXP-C12-03 |
| CLM-C13-07 | H-C13-1: every anchored spectrum is closed under divisors (refuted) | REFUTED | NOT ASSESSED | EXP-C13-05, EXP-C13-06, EXP-C13-07 |
| CLM-C13-08 | H-C13-2: laws with an infinite non-trivial affine spectrum are affinely rigid (refuted) | REFUTED | NOT ASSESSED | EXP-C13-02 |
| CLM-C13-09 | H-C13-5: a one-variable law has spectrum {1} or a cofinite spectrum (refuted) | REFUTED | NOT ASSESSED | EXP-C13-07 |
| CLM-C14-08 | H-C14-3: the six commutative unital associative products factor uniquely on connected (or… | REFUTED | NOT ASSESSED | EXP-C14-04, EXP-C14-06 |
| CLM-C15-08 | H-C15-1: streaming width is either bounded or geometric (refuted) | REFUTED | NOT ASSESSED | EXP-C15-02, EXP-C15-05 |
| CLM-C15-09 | H-C15-2: bounded width exactly for semigroups, affine magmas and bounded light cones (ref… | REFUTED | NOT ASSESSED | EXP-C15-02 |
| CLM-C15-10 | H-C15-4: an automaton can be fast-forwarded iff its light-cone complexity is bounded (ref… | REFUTED | NOT ASSESSED | EXP-C15-03, EXP-C15-05 |
| CLM-C15-11 | H-C15-5: cycle detection fast-forwards most automata, and long cycles mean geometric widt… | REFUTED | NOT ASSESSED | EXP-C15-04 |
| CLM-C15-12 | H-C15-6: every exact fast-forward beats simulation by more than 100x at L = 1024, t = 10^… | REFUTED | NOT ASSESSED | EXP-C15-03 |
| CLM-C16-02 | H-C16-1: maximal period at most n^2 - 1, attained only by quasigroups (refuted) | REFUTED | NOT ASSESSED | EXP-C16-01 |
| CLM-C16-06 | H-C16-5: no quasigroup has a full-period pair map (refuted) | REFUTED | NOT ASSESSED | EXP-C16-02 |
| CLM-C17-06 | H-C17-1: Light's test beats the exhaustive check by a factor >= n/10 on every family (ref… | REFUTED | NOT ASSESSED | EXP-C17-01 |
| CLM-C17-07 | H-C17-2: for anchored magmas the z = 0 instance of a law decides the law (refuted) | REFUTED | NOT ASSESSED | EXP-C17-02 |
| CLM-C18-10 | H-C18-3: the nimber-field quasigroup gives a hash competitive with FNV-1a (refuted) | REFUTED | NOT ASSESSED | EXP-C18-02, EXP-C18-03 |
| CLM-C18-11 | H-C18-8: the 8-pass cascade over LS, ISO and NIMINV passes every test (refuted) | REFUTED | NOT ASSESSED | EXP-C18-05 |
| CLM-C18-12 | H-C18-9: the cascade over x + c(y) still fails bit independence (refuted) | REFUTED | NOT ASSESSED | EXP-C18-05 |
| CLM-C19-10 | H-C19-1: the deficit is additive up to consecutive-pair corrections (refuted) | REFUTED | NOT ASSESSED | EXP-C19-03 |
| CLM-C19-11 | H-C19-2: the effect of the top summand depends only on the two highest levels (refuted) | REFUTED | NOT ASSESSED | EXP-C19-03 |
| CLM-C19-12 | H-C19-3: the deficit is additive over the runs of the lazy representation (refuted) | REFUTED | NOT ASSESSED | EXP-C19-03 |
| CLM-C19-13 | H-C19-4: the longest game is built by inserting one chip at a time (refuted) | REFUTED | NOT ASSESSED | EXP-C19-02 |

## 7. Inconclusive

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C12-09 | H-C12-0: every relational game is periodic, arithmetic-periodic or has a closed form (inc… | INCONCLUSIVE | NOT ASSESSED | EXP-C12-01, EXP-C12-02, EXP-C12-06, EXP-C12-03 |
| CLM-C18-09 | H-C18-2: structured quasigroups are worse mixers than a random Latin square (maximal aval… | INCONCLUSIVE | NOT ASSESSED | EXP-C18-02 |

