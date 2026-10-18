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
* **CLM-C03-09** (inconclusive). *Claimed:* The rule is non-terminating iff r \> q, s \> p and (r \>= 2q or s \>= 2p).

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

* **CLM-C08-06** (refuted). *Claimed:* Among digit-convolution products a o\_s b = sum d\_i d\_j G\_(i+j+s), only Fibonacci with s = 2 is associative.
  *Counterexample:* Fibonacci with s = 3 (t = 1) is associative by Theorem 1 (CLM-C08-01); geometric bases are associative for every s; many Pisot sequences are associative at larger shifts (EXP-C08-02).

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

## C14 — Graphs as quantities: the 256 local graph products

* **CLM-C14-08** (refuted). *Claimed:* Each of the six commutative associative local products with unit K1 (Cartesian, strong, symmetric difference, and their complement-duals 221, co-normal, 141) has unique prime factorisation on connected graphs, or, for the complement-duals, on co-connected graphs.
  *Counterexample:* Symmetric difference: K2 xor K2 xor K2 is isomorphic to K2 xor K\_{1,3}; K2 and K\_{1,3} are connected and prime, so this connected graph of order 8 has the two factorisations {K2,K2,K2} and {K2,K\_{1,3}} (proofs/paper/C14.md Theorem 8; explicit isomorphism in EXP-C14-06). In all graphs already C4 = K2 xor K2 = K2 xor 2K1. The other five products show no collision up to order 15 in the stated classes, consistent with Sabidussi-Vizing and Doerfler-Imrich/McKenzie.

## C17 — Deciding laws of finite magmas: generator, anchor and randomised tests against the exhaustive check

* **CLM-C17-06** (refuted). *Claimed:* Light's test with a greedy generating set uses at most a fraction 10/n of the exhaustive check's probes on every input family.
  *Counterexample:* Left-zero band x\*y = x (n generators needed): ratio 1.7 at n = 512; also one-entry corruptions of cyclic groups (ratio 47.9 \< 51.2 at n = 512, because the exhaustive check stops at the first violation).
* **CLM-C17-07** (refuted). *Claimed:* For every law of the C06 family, every anchored magma satisfying the instance z = 0 of the law satisfies the law (N \<= 5).
  *Counterexample:* 18 laws, e.g. x(yz) = y(y(xz)) (two violating models among 11 at N = 4), x(yz) = x((xy)z), (xy)z = (zy)x, (xy)z = (x(zz))y (EXP-C17-02). It does hold for associativity and (N \<= 10) for left-distributivity.

## C20 — Open problems revisited: the last one-rule systems of C04, and a literature check for C03

* **CLM-C20-04** (inconclusive). *Claimed:* The published complete characterisation of termination of 0\^p 1\^q -\> 1\^r 0\^s (H. Zantema, A. Geser, AAECC 11 (2000) 1-25; tech. report UU-CS-1994-44) could not be compared with the lab's Conjecture 4.6 (CLM-C03-\*), because the full text could not be retrieved from this environment.
  *Status:* Attempts on 2026-10-18 - Utrecht DSpace (HTTP 403 / Cloudflare challenge), its mirror (HTTP 500), the author's publication page (no link). A human with library access should compare the theorem with Conjecture 4.6; if they differ, the published theorem wins.
