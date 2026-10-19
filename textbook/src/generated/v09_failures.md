# Failed theories and counterexamples {.unnumbered}

*Volume 9 — Failed theories and mathematical counterexamples. Generated from the claim database.*

Every bold hypothesis the laboratory proposed and refuted is kept here with the counterexample that refuted it. Failures are part of the record: several of them (the Fibonacci pattern of Chapter 2, the non-rational complexity of Chapter 5, the odd and golden spectra of Chapter 7) led directly to the positive results of the book.

## C01 — Quantity as the complete invariant of rewriting

* **CLM-C01-05** (refuted). *Claimed:* For every relation u \<-\> v over {a,b} with u != v and equal symbol counts, the generated congruence coincides with counting (Parikh) equivalence on all words of length \>= \|u\|.
  *Counterexample:* u = aab, v = aba: the word baa is fixed by every rewrite, so its class {baa} is smaller than its counting class {aab, aba, baa}. All 33 relations of length 3-4 fail (EXP-C01-04).

## C02 — Exchange systems: positional numeration as normal forms

* **CLM-C02-06** (refuted). *Claimed:* For every carry rule with sum b \< m, each integer has exactly one stable configuration of that value.
  *Counterexample:* 4\[k\] -\> 2\[k+1\] (base 2 with digits 0..3): the stable configurations '2' and '10' both have value 2. Also 4\[k\] -\> \[k+2\] on all levels, 4\[k\] -\> 2\[k+2\], 4\[k\] -\> 2\[k+3\] (EXP-C02-04).

## C03 — Termination of one-rule string rewriting 0\^p 1\^q -\> 1\^r 0\^s

* **CLM-C03-07** (refuted). *Claimed:* The rule 0\^p 1\^q -\> 1\^r 0\^s terminates iff s \<= p or r \<= q.
  *Counterexample:* 0011 -\> 111000 (both counts grow) is terminating - a published theorem (A. Geser, 'A Solution to Zantema's Problem', Passau MIP-9314, 1993; Zantema-Geser 2000; automated RFC match-bound proofs). Our own evidence agrees (all 3747 words of length \<= 12 containing 0011 have finite derivation trees) but we have no independent proof; the refutation rests on the cited proof.
* **CLM-C03-08** (refuted). *Claimed:* The rule 0\^p 1\^q -\> 1\^r 0\^s terminates iff r \< 2q or s \< 2p.
  *Counterexample:* 011 -\> 11100 (r = 3 \< 4 = 2q) loops: 001111 -\>4 111 001111 00100 (Lean-verified, not\_terminating\_0\_11). 40 counterexamples with parameters \<= 5 (35 loops of EXP-C03-02 plus the 5 mirror loops of EXP-C03-03; count corrected after the skeptic review).
* **CLM-C03-09** (refuted). *Claimed:* The rule is non-terminating iff r \> q, s \> p and (r \>= 2q or s \>= 2p).
  *Counterexample:* 0011 -\> 11100000 (p = q = 2, r = 3, s = 5): H-C03-3 predicts non-termination (r \> q, s \> p, s \>= 2p), but the rule terminates by Zantema-Geser Theorem 1.1, case 4 (q \< r \< 2q and p does not divide s). The refutation rests on the published proof.

## C04 — Derivation lengths, random descent and rewriting games

* **CLM-C04-02** (refuted). *Claimed:* A one-rule system l -\> r with \|l\| \<= 3 is non-terminating iff l is a factor of r.
  *Counterexample:* ab -\> bbaa is non-terminating although ab is not a factor of bbaa: aab -\> abbaa -\> bbaabaa = bb.aab.aa. In total 18 such rules with \|r\| \<= 5 (EXP-C04-02).
* **CLM-C04-07** (refuted). *Claimed:* A terminating one-rule system has random descent iff its left-hand side is unbordered.
  *Counterexample:* aa -\> a has the bordered left-hand side aa but random descent (every derivation from w has sum over a-runs of (length - 1) steps and ends in the same word); 18 bordered rules with \|l\|, \|r\| \<= 3 have random descent (EXP-C04-05). The 'if' direction is CLM-C04-05.
* **CLM-C04-11** (refuted). *Claimed:* For every terminating one-rule system over {a,b} with \|l\|, \|r\| \<= 3, the derivational complexity D(n) satisfies a linear recurrence.
  *Counterexample:* aab -\> ba (and its 3 symmetric images): D(n) = n - 1 - kappa(n) is not given by any linear recurrence (CLM-C04-09).
* **CLM-C04-14** (refuted). *Claimed:* Every rewriting game of a terminating one-rule system with \|l\|, \|r\| \<= 3 has Sprague-Grundy values \<= 3.
  *Counterexample:* aa -\> b: the word a\^14 has Grundy value 4 (computed from its own derivation graph); Dawson's Kayles reaches 9, Officers 91 for n \<= 3000 (EXP-C04-08).

## C05 — Spectra of single-identity magma varieties

* **CLM-C05-01** (refuted). *Claimed:* Every identity t = x has spectrum {1} or the set of all positive integers.
  *Counterexample:* ETP law 167, x = (y\*x)\*(x\*y): Lean-certified models of orders 4 and 5 (T4\_law167, T5\_law167) and no model of order 2, 3, 6 or 7 (law167\_card\_mod\_four: every finite model has order 0 or 1 mod 4). The census EXP-C05-01 finds 61 of 115 nontrivial two-variable identities with spectra on n \<= 6 that are neither {1} nor everything.
* **CLM-C05-03** (refuted). *Claimed:* If x occurs in t but is neither its leftmost nor its rightmost leaf, every finite model of t = x is a quasigroup.
  *Counterexample:* The 4-element model T4 of law 167, x = (y\*x)\*(x\*y), has row 1 = (0, 2, 2, 2) (Lean: T4\_law167, T4\_not\_latin). In the census, 18 of the 115 identities already have non-quasigroup models of order \<= 3.
* **CLM-C05-06** (refuted). *Claimed:* A nontrivial identity t = x has models of all orders 1..6 iff it has an affine model x\*y = a x + b y + c over Z\_n for every n \<= 6.
  *Counterexample:* x = (y\*x)\*(x\*(y\*y)) has models of every order 1..6 (EXP-C05-01); of order 2 it is satisfied by NAND (Lean: nand2\_law), yet no affine operation over Z\_2 satisfies it (Lean: no\_affine\_model\_mod2); its affine models exist only for n in {1, 5}. Three further identities behave alike (EXP-C05-05).
* **CLM-C05-09** (refuted). *Claimed:* The finite models of x = y(x((yx)y)) (ETP 677) and of x = y(((yx)x)y) (ETP 1313) have exactly the orders 1 and the odd integers n \>= 5.
  *Counterexample:* Linear models of order 16 (found by the Skeptic, reviews/skeptic\_C05\_C08\_C12.md, Appendix B) - over GF(16) = GF(2)\[t\]/(t\^4 + t + 1), x\*y = (1 + t\^3)x + t\^3 y satisfies law 677 and x\*y = t\^3 x + (1 + t\^3)y satisfies law 1313 (each has 8 such pairs (a, b)). Re-found by EXP-C05-07 and Lean-certified (E677\_order16\_law, E1313\_order16\_law, kernel decide on the 16 x 16 tables).

## C06 — Successor-anchored magmas: spectra of composition laws

* **CLM-C06-04** (refuted). *Claimed:* Among the laws x(yz) = t and (xy)z = t with t a term of 3-4 leaves over exactly {x, y, z}, every law other than left-distributivity has anchored spectrum {1} or {1, ..., 6}.
  *Counterexample:* 21 other laws have restricted spectra (EXP-C06-03): (xy)z = x((yz)z) - odd N; (xy)z = x(y(zz)) - N = 1, 5 (and 11, 19, ... by Theorem 6 of proofs/paper/C06.md); x(yz) = ((zx)x)y - N = 1, 3; x(yz) = ((xx)y)z - N = 1, 2.
* **CLM-C06-09** (refuted). *Claimed:* For every law of EXP-C06-03 other than left-distributivity, the anchored spectrum for N \<= 6 equals the set of N for which some affine table x\*y = x + a\*y + 1 satisfies the law.
  *Counterexample:* x(yz) = y(x(yz)), x(yz) = y(x(xz)), x(yz) = y(y(xz)) and x(yz) = (yx)(yz) have anchored models for every N \<= 6 but no affine model for N \> 1; x(yz) = y((yx)z) has a non-affine model at N = 2 (EXP-C06-04).

## C07 — Arithmetic from the minimal excludant: a census of mex-defined operations

* **CLM-C07-02** (refuted). *Claimed:* Apart from trivial operations (0, projections), the only associative mex operations of the family are Conway's nim-sum and nim-product.
  *Counterexample:* L+R+D\[z\] gives ordinary addition a + b and D\[z\] gives min(a, b) (Theorem 1); also the zero-absorbing shifts of XOR and +.
* **CLM-C07-04** (refuted). *Claimed:* Every commutative mex operation of the family is closed on \[0, 2), \[0, 4) and \[0, 16), like the nimbers.
  *Counterexample:* D\[x\^y\]: f(2,3) = 4, so \[0,4) is not closed; 30 of the 34 commutative operations fail (EXP-C07-01).
* **CLM-C07-06** (refuted). *Claimed:* For every operation of the family and every a, the row b -\> f(a,b) satisfies f(a, b + p) = f(a, b) + s for all large b, for some p \>= 1 and s, as for Wythoff's game.
  *Counterexample:* Row 2 of D\[x\^y\] (Theorem 3): \|f(2,b) - b\| = J\_k on the k-th block pair, which rules out every (p, s). Numerically only 222 of 670 rows (a = 1..5, b \< 1500) have a period \<= 375.
* **CLM-C07-07** (refuted). *Claimed:* For every commutative mex operation of the family, 0 is absorbing or an identity, and the diagonal f(n,n) is a sequence in the OEIS.
  *Counterexample:* The first part holds (Theorem 2); the second fails - e.g. the diagonal 0, 2, 1, 5, 7, 4, 3, 16, 13, 10, 15, 6, ... of L+R+D\[x\^y\^z\] and 0, 1, 3, 6, 8, 11, 10, 19, ... of D\[z\]+D\[x\^y\^z\] have no OEIS match (88 unmatched sequences, EXP-C07-02, OEIS state of 2026-10-18).

## C08 — Circle multiplications on recurrence numeration systems

* **CLM-C08-05** (refuted). *Claimed:* Smallest shift s0 with o\_s associative for all tested s0 \<= s \<= max tested: Fibonacci 2, Pell (1,2,5) 1, G(k+1)=2G(k)+2G(k-1) (1,2) 5, tribonacci 3, 4-bonacci 7, G(k+1)=G(k)+G(k-2) 10, G(k+1)=3G(k)+3G(k-1) (1,5) 10; G(k+1)=G(k)+G(k-3) none up to 20 (full table in results/EXP-C08-02.json and EXP-C08-03.json).
  *Counterexample:* Certified violations (EXP-C08-06) - tribonacci s = 3: (10016 o 10016) o 1 = 3414681926 != 3414681924 = 10016 o (10016 o 1) (the example of Ambroz-Frougny-Masakova-Pelantova 2003); 4-bonacci s = 7: triple (623729, 581581, 1); G(k+1) = 2G(k) + 2G(k-1) (1,2) s = 5: triple (29957, 280628, 1); G(k+1) = G(k) + G(k-2) s = 10: triple (78, 248, 1) (found by the Historian). The random tests behind the measurement (triples up to 10\^6) missed these rare failures. The Skeptic's review adds G(k+1) = 3G(k) + 3G(k-1) (1,5) at s = 10: (173938 o 173938) o 1 != 173938 o (173938 o 1) - the fifth wrong value. Thresholds after the targeted search in CLM-C08-08.
* **CLM-C08-06** (refuted). *Claimed:* Among digit-convolution products a o\_s b = sum d\_i d\_j G\_(i+j+s), only Fibonacci with s = 2 is associative.
  *Counterexample:* Fibonacci with s = 3 (t = 1) is associative by Theorem 1 (CLM-C08-01); geometric bases are associative for every s; many Pisot sequences are associative at larger shifts (EXP-C08-02).
* **CLM-C08-07** (refuted). *Claimed:* For the circle product o\_s: Fibonacci (1,2) fails for s \<= 1 and is associative for s \>= 2 (Lean, CLM-C08-01); Pell (1,2,5) fails at s = 0, no failure found for 1 \<= s \<= 5 (associative for s \>= 1 by Messaoudi 2000); G(k+1) = 2G(k) + 2G(k-1) (1,2) fails for s \<= 5, no failure found for 6 \<= s \<= 8; tribonacci (1,2,4) fails for s \<= 3, no failure found for 4 \<= s \<= 9; 4-bonacci (1,2,4,8) fails for s \<= 7, no failure found for 8 \<= s \<= 10; G(k+1) = G(k) + G(k-2) (1,2,3) fails for s \<= 10, no failure found for s = 11, 12; G(k+1) = 3G(k) + 3G(k-1) (1,5) fails for s \<= 9, no failure found for 10 \<= s \<= 12. Every failure is certified by an explicit triple; every "no failure" is computational support only.
  *Counterexample:* Two of its 'no failure found' ranges were wrong (Skeptic review 2026-10-18, reviews/skeptic\_C05\_C08\_C12.md, P2) - G(k+1) = 2G(k) + 2G(k-1) (1,2) fails at s = 6: (314965 o 314965) o 1 != 314965 o (314965 o 1); G(k+1) = 3G(k) + 3G(k-1) (1,5) fails at s = 10 and s = 11: (173938 o 173938) o 1 != 173938 o (173938 o 1). Both re-verified with the lab's code and re-found by EXP-C08-07 (e.g. (5653, 42197, 1) at s = 6; (3192, 173938, 1) at s = 10; (12100, 12100, 1) at s = 11). The certified lower bounds of this claim stand; the thresholds it implied for these two sequences do not. Superseded by CLM-C08-08.

## C09 — Arithmetic of Knuth's circle semigroup

* **CLM-C09-02** (refuted). *Claimed:* Every n \>= 1 has a unique multiset of circle-irreducible factors.
  *Counterexample:* 8 = 1 o 1 o 1 = 2 o 2 with 1, 2 irreducible (every product is \>= 3); the factorisations even differ in length.
* **CLM-C09-04** (refuted). *Claimed:* The proportion of circle-irreducible numbers up to x tends to 0 as x tends to infinity.
  *Counterexample:* By CLM-C09-03 the irreducibles contain a set of natural density 1/phi\^2 = 0.3819...; observed density is 0.539 at 1e6.

## C10 — The cost of counting across representations

* **CLM-C10-03** (refuted). *Claimed:* The average number of digit changes per increment in the Zeckendorf system is smaller than in binary.
  *Counterexample:* Both averages tend to exactly 2 (Theorem 2 and the binary case of Theorem 1); at n \< 1e6 the Zeckendorf average is 1.999992 vs binary 1.999988.

## C11 — Pattern-terminated universal integer codes

* **CLM-C11-05** (refuted). *Claimed:* For every k, the all-ones terminator 1\^k gives the shortest codeword among all length-k terminators for every n beyond a small threshold.
  *Counterexample:* k = 4, n = 1000: terminators 1000, 1001 and 1010 give codewords 1 bit shorter than 1111. Rivals beat 1\^k at 762, 972 and 1127 sampled n \>= 1000 (all n \<= 2048 and quarter-powers of 2 up to 2\^64) for k = 4, 5, 6, up to n = 311743, 2\^45 and about 1.3e19 respectively (EXP-C11-02). By Theorem 2 (CLM-C11-02), 1\^k does win eventually.
* **CLM-C11-06** (refuted). *Claimed:* (a) The average over n \<= N of L\_(1\^k)(n) - L\_u(n), u unbordered of length k + 1, tends to log\_lambda(1/(lambda - 1)). (b) Corrected version: this average converges to (2 - lambda)/(lambda - 1)\^2.
  *Counterexample:* k = 3 (111 vs 0111): the average over n \<= 2\^40 is 0.2282 against the prediction 0.2875 of (a) (EXP-C11-06); the running average is 0.228181, 0.309709 and 0.228548 at N = 2\^40, 2\^80 and 2\^120, so it does not converge (EXP-C11-07). Both statements hold only for k = 2 (value 1).

## C12 — Relational one-heap games

* **CLM-C12-09** (inconclusive). *Claimed:* Every game of the catalogue is eventually periodic, eventually arithmetic-periodic, or has a Grundy function given by a closed form in a number-theoretic function.
  *Status:* The "closed form" clause is not precisely defined, so the hypothesis cannot be refuted as stated; recorded as inconclusive rather than refuted.
* **CLM-C12-10** (refuted). *Claimed:* For each of the games G01-G06, g(n) depends only on the prime signature (sorted exponent vector) of n.
  *Counterexample:* G01: n = 2 and n = 3 have signature (1) but g = 1 and 0. Further first counterexamples: G02 (2, 3: g = 2, 1), G03 (4, 9: 1, 0), G05 (2, 3: 1, 2), G06 (6, 10: 2, 4). Only G04 (g = Omega) depends on the signature alone.
* **CLM-C12-11** (refuted). *Claimed:* Subtraction games whose move sets are the squares, the triangular numbers, the Fibonacci numbers or the primes have P-positions of positive natural density.
  *Counterexample:* Squares and triangular numbers: the P-set has density 0 (CLM-C12-08); measured P-density 0.0538 -\> 0.0222 and 0.0344 -\> 0.0116 as N grows from 1.25e4 to 2e5. For Fibonacci numbers (0.180) and primes (0.155) the question remains open.

## C13 — Anchored spectra II: which sets of integers are spectra?

* **CLM-C13-07** (refuted). *Claimed:* If a set of laws has an anchored model of size N, it has one of every size d dividing N.
  *Counterexample:* x = x(x(xx)) has models of every size except 2 (CLM-C13-05, Lean). Violations are common - 24 of 253 one-variable laws (N \<= 12), 81 of 300 random 2-variable laws (N \<= 9), 29 of 150 random 3-variable laws and 17 of 80 random pairs of laws (N \<= 8); e.g. ((xy)x)y = (y(xx))x has models at N = 6 and 8 but none at N = 2, 3, 4, 5.
* **CLM-C13-08** (refuted). *Claimed:* For every law with at most 4 leaves per side (3 variables) or 5 leaves per side (2 variables) whose affine spectrum is infinite and not all N, every anchored model is affine.
  *Counterexample:* 146 of the 147 laws tested from infinite non-trivial affine classes have non-affine models (EXP-C13-02, corrected run), all at every N = 6, 7, 8; e.g. x = x(x(xx)) (affine spectrum A034017, non-affine models for N = 3..8) and (xx)x = (yy)y (non-affine models for N = 2..8). (The first run also tested 52 laws from finite classes Div(L), L \>= 61, through a faulty filter - they are all non-rigid too.)
* **CLM-C13-09** (refuted). *Claimed:* Every law t1(x) = t2(x) in one variable has anchored spectrum {1} or contains all sufficiently large N.
  *Counterexample:* x = (xx)x has spectrum exactly {1, 2}: at x = 0 the anchor gives 0 = 2, and x\*y = x + 1 is a model of size 2; likewise x = ((xx)x)x has spectrum {1, 3} and x = (((xx)x)x)x has {1, 2, 4} (proofs/paper/C13.md, remark after Theorem 5).

## C14 — Graphs as quantities: the 256 local graph products

* **CLM-C14-08** (refuted). *Claimed:* Each of the six commutative associative local products with unit K1 (Cartesian, strong, symmetric difference, and their complement-duals 221, co-normal, 141) has unique prime factorisation on connected graphs, or, for the complement-duals, on co-connected graphs.
  *Counterexample:* Symmetric difference: K2 xor K2 xor K2 is isomorphic to K2 xor K\_{1,3}; K2 and K\_{1,3} are connected and prime, so this connected graph of order 8 has the two factorisations {K2,K2,K2} and {K2,K\_{1,3}} (proofs/paper/C14.md Theorem 8; explicit isomorphism in EXP-C14-06). In all graphs already C4 = K2 xor K2 = K2 xor 2K1. The other five products show no collision up to order 15 in the stated classes, consistent with Sabidussi-Vizing and Doerfler-Imrich/McKenzie.

## C15 — Magma cellular automata: light cones, streaming width and fast-forwarding

* **CLM-C15-08** (refuted). *Claimed:* For every magma automaton of order \<= 3 the streaming width lambda(t) is either bounded or grows geometrically; there is no intermediate growth.
  *Counterexample:* The fuse magma \[\[0,0,0\],\[0,0,1\],\[1,2,2\]\] has floor((floor(t/2)+1)/2) \<= lambda(t) \<= 3t + 3 (Theorem 4; lambda(t) = t + 2 for t \<= 12); 104 order-3 classes show linear growth on t \<= 9 (EXP-C15-02).
* **CLM-C15-09** (refuted). *Claimed:* An order-3 magma automaton has bounded streaming width iff the magma is a semigroup, is affine over Z\_3, or its light cone depends on at most two cells.
  *Counterexample:* The 'if' direction holds for all 18 semigroup and 8 affine classes, but 685 bounded-width classes lie outside the three classes, e.g. the reversible automaton \[\[0,0,2\],\[2,2,0\],\[1,1,1\]\] whose light cone uses all t + 1 cells and whose width stays 3 (EXP-C15-02).
* **CLM-C15-10** (refuted). *Claimed:* A magma automaton admits a fast-forward (rows at time t computable in time polynomial in L and log t) if and only if its streaming width is bounded.
  *Counterexample:* The fuse magma has unbounded (linear) streaming width but its row at any time t is computable in O(L) operations (Theorem 4). The converse direction is open (CLM-C15-18).
* **CLM-C15-11** (refuted). *Claimed:* For at least half of the order-3 classes a random cyclic row of length 32 repeats within 5000 steps, and only classes with geometric streaming width have rows that do not.
  *Counterexample:* The first part holds (1590/1734 classes at L = 32), the second fails - the bounded-width affine quasigroups x + y, 2x + y, 2x + 2y, 2x + 2y + 1 (mod 3, up to relabelling) do not repeat within 5000 steps at L = 32 and 64 (EXP-C15-04). The cap matters (Skeptic) - at L = 32 they do repeat, with periods 6,560 or 19,680 (still long, so the refutation stands); at L = 64 none repeats within 200,000 steps.
* **CLM-C15-12** (refuted). *Claimed:* Each of the affine, commutative-semigroup and fuse fast-forwards is exact, beats direct numpy simulation by more than 100x at L = 1024, t = 10\^5, and loses for t below a few hundred steps.
  *Counterexample:* Exactness holds (99/99), but the commutative-semigroup method reaches only x62 (mult mod 3) and x77 (min) at L = 1024, t = 10\^5 (the Skeptic's re-run - 79-97x). The clause 'loses for small t' is partly true - timed with the same protocol on both sides, the affine method loses for t below about 20 and the fuse method below about 20-70 (Skeptic review, Appendix C). The first version said the affine and fuse methods never lose; EXP-C15-03 had timed the fast method as the best of 3 runs and the simulation as a single run.

## C16 — Fibonacci dynamics in invented finite algebras

* **CLM-C16-02** (refuted). *Claimed:* As for Pisano periods (where (0, 0) is fixed), the maximal period of the pair map on an n-element magma is at most n\^2 - 1, and the maximum is attained only by quasigroups.
  *Counterexample:* x\*y = 1 - y on {0,1} has the single cycle (0,0) -\> (0,1) -\> (1,1) -\> (1,0) of length 4 = n\^2 and is not a quasigroup; every n has full-period tables (Theorem 2); for n \<= 4 none of them is a quasigroup (EXP-C16-01).
* **CLM-C16-06** (refuted). *Claimed:* For every n, no quasigroup of order n has a full-period pair map; the maximal period of a quasigroup of order n is n\^2 - 1.
  *Counterexample:* True for n = 2, 3, 4, false for n = 5 - exactly 3360 of the 161280 Latin squares of order 5 are full-period (e.g. the cycle 0,0,1,0,2,2,0,3,3,1,2,1,4,0,4,4,2,3,2,4,1,1,3,4,3); examples exist for every order 6-16 (EXP-C16-02).

## C17 — Deciding laws of finite magmas: generator, anchor and randomised tests against the exhaustive check

* **CLM-C17-06** (refuted). *Claimed:* Light's test with a greedy generating set uses at most a fraction 10/n of the exhaustive check's probes on every input family.
  *Counterexample:* Left-zero band x\*y = x (associative; n generators needed) - exhaustive/Light probe ratio 1.71 at n = 512 (EXP-C17-01). The first version also cited one-entry corruptions of cyclic groups (ratio 47.9 at n = 512); that number was an artefact of the probe accounting (Skeptic review, P1). With correct accounting an early-exit exhaustive check is about as cheap as Light's test on corruptions and far cheaper on random magmas, so the hypothesis fails on non-associative inputs as well.
* **CLM-C17-07** (refuted). *Claimed:* For every law of the C06 family, every anchored magma satisfying the instance z = 0 of the law satisfies the law (N \<= 5).
  *Counterexample:* 43 of the 382 laws (first violating anchored model at N = 3 for 33 laws, at N = 4 for 10), e.g. x(yz) = x(zy) (54 violating models among 82 at N = 3), x(yz) = y(y(xz)) (two violating models among 11 at N = 4), x(yz) = x((xy)z), (xy)z = (zy)x, (xy)z = (x(zz))y (EXP-C17-02). For the other 339 laws the instance decides the law for N \<= 5, among them associativity, and (N \<= 10) left-distributivity. The first version reported 18 insufficient and 31 undecided laws because of a classification bug - a law whose enumeration was capped at one N was counted as undecided even when a violation had been found at another N; the Skeptic's independent census gives the same 339 / 43 / 0 as the corrected experiment.

## C18 — Invented operations as mixing primitives: quasigroup string transformations versus standard hashes

* **CLM-C18-09** (inconclusive). *Claimed:* Every structured quasigroup tested (affine, XOR, x + c(y), (x + 1) XOR y) gives a larger maximal avalanche bias than the random Latin square, in the reverse-pass (p2+rev) construction. (As first worded - 'in the same construction' - the hypothesis is false for the forward-only construction, where the random Latin square and x + c(y) both have bias exactly 1/2 by CLM-C18-02; the experiment compared every structured variant with QG-LS p2+rev.)
  *Status:* Proved (bias 1/2) for the T-function and GF(2)-affine quasigroups (CLM-C18-04, CLM-C18-05). For x + c(y) with a reverse pass the difference (0.043 versus 0.041) is within sampling noise; its defect shows in bit independence instead (CLM-C18-06), which the hypothesis did not measure.
* **CLM-C18-10** (refuted). *Claimed:* QG-NIMINV p2+rev (x\*y = (x XOR y)\^-1 in the nimber field of order 256) has avalanche at least as good as FNV-1a-64, \|chi-square z\| \<= 3 and a bucket-collision ratio within 2% on all four key sets.
  *Counterexample:* Avalanche is better than FNV-1a's (max bias 0.0415 vs 0.5), but on the decimal strings 0..65535 the 1024-bucket z-score is 1084 and the bucket-collision ratio 2.62, and near-duplicate keys give 32,624 full 64-bit collisions - the tail-information bound (CLM-C18-03). (FNV-1a itself has z = -9.8 there - more uniform than random, bucket-collision ratio 0.995 - and 0 full collisions; the first wording wrongly attributed \|z\| \<= 3 on all four key sets to FNV-1a.)
* **CLM-C18-11** (refuted). *Claimed:* The cascades QC-LS, QC-ISO and QC-NIMINV (depth 8, 8 zero bytes of finalisation) have avalanche within 0.01 of BLAKE2b-64, \|z\| \<= 3, collision ratios within 2% and no full collisions on all four key sets.
  *Counterexample:* QC-NIMINV d8 - maximal avalanche bias 0.0845 against 0.045 for BLAKE2b (about 7 standard deviations of a cell; the Skeptic's replication with new keys - 0.0735, against a null maximum of 0.048; worst cell key byte 15, bit 0 -\> top bit of s1). QC-LS d8 and QC-ISO d8 pass every test (EXP-C18-05). (A z = -3.21 on synthetic words was also cited at first; it is 1 of 48 z-scores and in the benign direction - more uniform than random - so the refutation rests on the avalanche bias alone.)
* **CLM-C18-12** (refuted). *Claimed:* The cascade QC-ARP d8 has a maximal bit-independence correlation of at least 0.5.
  *Counterexample:* QC-ARP d8 has maximal correlation 0.176 (noise level about 0.11) - the cascade removes the perfect correlation of QG-ARP p2+rev, although 5 avalanche cells still exceed bias 0.1 (EXP-C18-05).

## C19 — The longest Zeckendorf game

* **CLM-C19-10** (refuted). *Claimed:* D(n) = sum\_t floor(j\_t\^2/4) - sum\_t R(j\_t, j\_{t+1}) over consecutive Zeckendorf levels j\_1 \> j\_2 \> ... of n.
  *Counterexample:* n = 12 = F\_5 + F\_3 + F\_1 (levels 4, 2, 0): D(12) = 0 but the model gives 1; 23,680 of the n \< 30000 violate it (EXP-C19-03).
* **CLM-C19-11** (refuted). *Claimed:* D(n) - D(n - F\_top) is a function of the two highest Zeckendorf levels of n.
  *Counterexample:* Levels (4, 2) occur with D(n) - D(n - F\_5) in {0, 1} (n = 12 and n = 11); 87 such ambiguous pairs below 30000 (EXP-C19-03). The dependence is through the parity chain of lower levels, captured by rho in CLM-C19-05.
* **CLM-C19-12** (refuted). *Claimed:* There is a function phi(start, length) with D(n) = sum of phi over the maximal runs of ones of the lazy representation of n.
  *Counterexample:* For n \< 160 the linear system D(n) = sum phi(run) has coefficient rank 46 and augmented rank 47 (exact rational elimination), so it has no solution (EXP-C19-03).
* **CLM-C19-13** (refuted). *Claimed:* L(n + 1) = L(n) + lambda(n), where lambda(n) is the longest game from the Zeckendorf representation of n plus one extra F\_1.
  *Counterexample:* n = 3: L(4) = 3, L(3) = 2, lambda(3) = 0 (Zeckendorf(3) + F\_1 is already Zeckendorf); fails for 288 of the first 300 n (EXP-C19-02). Longest games avoid early normalisation, so they do not pass through Zeckendorf(n).
