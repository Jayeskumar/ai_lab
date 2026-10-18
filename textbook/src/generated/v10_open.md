# Open problems {.unnumbered}

*Volume 10 — Open problems and future research. Generated from the claim database and the cycle records.*

## Unproven claims

Each of these is supported by the evidence cited in its record but has no proof. A proof or a counterexample would settle it.

* **CLM-C01-08** (computationally supported): For all words u != v of equal length k over a q-letter alphabet, the number of congruence classes of length-n words modulo u = v has generating function c(x) / (x\^k + (1 - q x) c(x)), where c(x) = 1 + sum over words b that are borders of both u and v of x\^(k - \|b\|). *Evidence:* EXP-C01-05, EXP-C01-06, EXP-C01-07.
* **CLM-C01-10** (computationally supported): If u != v of length k share exactly one common border z (neither border set containing the other), the class counts have generating function c/(x\^k + (1 - q x) c) with c = 1 + x\^(k - \|z\|). *Evidence:* EXP-C01-06, EXP-C01-07, EXP-C01-08.
* **CLM-C01-11** (computationally supported): For words u != v of equal length, the one-rule system {u -\> v} is confluent if and only if every border of u is a border of v. *Evidence:* EXP-C01-08.
* **CLM-C03-10** (computationally supported): 0\^p 1\^q -\> 1\^r 0\^s (p, q, r, s \>= 1) is non-terminating iff (a) r \>= 2q and s \>= 2p, or (b) s \>= 2p, q \< r \< 2q and p divides s, or (c) r \>= 2q, p \< s \< 2p and q divides r. Otherwise it terminates. *Evidence:* EXP-C03-02, EXP-C03-03, EXP-C03-04.
* **CLM-C03-11** (computationally supported): For 0 1\^q -\> 1\^(q+1) 0\^k the rightmost strategy from 0 1\^(q(q+1)) reaches a self-embedding after 16, 32, 64 steps (k = 2) and 260, 1556, 9332 steps (k = 6) for q = 4, 5, 6. *Evidence:* EXP-C03-04.
* **CLM-C04-12** (computationally supported): The 162 terminating rules (55 symmetry classes) have derivational complexity linear (144 rules, of which 4 are n - Theta(log n)), quadratic (14: floor(n\^2/4), floor(n(n-1)/6), floor(n\^2/8)) or exponential (4: 2\^(n-1) - 1); for 54 of the 55 classes D(n) = floor((a n\^2 + b n + c)/d) or 2\^(n-1) - 1 on all computed terms. *Evidence:* EXP-C04-03.
* **CLM-C04-16** (conjecture): The Grundy sequences of the rewriting games of aa -\> ab, aaa -\> b and aaa -\> ab on the words a\^n are ultimately periodic. *Evidence:* EXP-C04-08, EXP-C04-09.
* **CLM-C05-02** (computationally supported): Of the 115 identities t = x (x occurring in t, neither leftmost nor rightmost), 52 have models of every order 1..6, 2 have none of orders 2..6, and 61 have restricted spectra; the 63 non-full ones fall into 15 patterns on n = 1..8 listed in research/cycles/C05\_magma\_spectra/README.md (e.g. 10111011 for 16 identities including the Dupont law, 10110010 = Mendelsohn pattern for law 66 and three equivalents, 1010001? for law 907). *Evidence:* EXP-C05-01, EXP-C05-02.
* **CLM-C05-09** (conjecture): The finite models of x = y(x((yx)y)) (ETP 677) and of x = y(((yx)x)y) (ETP 1313) have exactly the orders 1 and the odd integers n \>= 5. *Evidence:* EXP-C05-03, EXP-C05-02.
* **CLM-C06-01** (computationally supported): An anchored left-distributive magma (x\*0 = x+1 mod N, x(yz) = (xy)(xz)) of size N exists exactly for N = 1, 2, 4, 8 among N \<= 10 and is then unique (the Laver table A\_n); Laver's recursion yields left-distributive tables exactly at the powers of 2 up to N = 64 (verified to N = 256 exhaustively). *Evidence:* EXP-C06-01, EXP-C06-02.
* **CLM-C06-10** (computationally supported): The seven laws x(yz) = ((zx)x)y, x(yz) = ((zx)y)x, x(yz) = ((zy)x)x, (xy)z = y((zx)y), (xy)z = y((zy)x), (xy)z = z((yx)z), (xy)z = z((yz)x) have anchored models exactly for N in {1, 3}; the ten laws x(yz) = y((yx)z), x(yz) = ((xx)y)z, x(yz) = ((xx)z)y, x(yz) = ((xy)x)z, x(yz) = ((xy)y)z, x(yz) = ((xy)z)x, x(yz) = ((xy)z)y, x(yz) = ((xz)x)y, x(yz) = ((xz)y)x, x(yz) = ((xz)y)y have anchored models exactly for N in {1, 2}. *Evidence:* EXP-C06-03, EXP-C06-04.
* **CLM-C06-11** (computationally supported): (xy)z = x(z(yy)) has the same anchored model counts as the golden law (xy)z = x(y(zz)), and (xy)z = x((zy)y) the same as the odd law (xy)z = x((yz)z), for N \<= 9; their affine spectra coincide for N \<= 40. *Evidence:* EXP-C06-04.
* **CLM-C07-08** (computationally supported): Among the 134 distinct mex operations, 22 have additively periodic rows a = 1..5 (period \<= 375 within b \< 1500), 40 have none, and the rest are mixed. *Evidence:* EXP-C07-03.
* **CLM-C08-02** (computationally supported): If the minimal linear recurrence of an increasing base sequence G (G\_0 = 1) has a characteristic root beta other than the dominant root with \|beta\| \>= 1, then the circle product o\_s is non-associative for every s \>= 0. *Evidence:* EXP-C08-02.
* **CLM-C08-03** (computationally supported): For base sequences satisfying the dominant-root conditions of Grabner-Petho-Tichy-Woeginger (1994), the circle product is associative once the shift parameter is large enough. *Evidence:* EXP-C08-02, EXP-C08-03.
* **CLM-C08-04** (computationally supported): For quadratic Pisot base sequences with real conjugate root beta \> 0, the set of shifts s for which o\_s is associative is upward-closed. Sets that are not upward-closed (e.g. {2} and s \>= 4 for G = 1,3,4,7,11,...) occur only when beta \< 0. *Evidence:* EXP-C08-04, EXP-C08-03.
* **CLM-C08-05** (computationally supported): Smallest shift s0 with o\_s associative for all tested s0 \<= s \<= max tested: Fibonacci 2, Pell (1,2,5) 1, G(k+1)=2G(k)+2G(k-1) (1,2) 5, tribonacci 3, 4-bonacci 7, G(k+1)=G(k)+G(k-2) 10, G(k+1)=3G(k)+3G(k-1) (1,5) 10; G(k+1)=G(k)+G(k-3) none up to 20 (full table in results/EXP-C08-02.json and EXP-C08-03.json). *Evidence:* EXP-C08-02, EXP-C08-03.
* **CLM-C09-05** (conjecture): Almost every n whose conjugate lies in the product zone is a circle product, so the circle irreducibles have natural density 1/phi\^2. *Evidence:* EXP-C09-04, EXP-C09-01.
* **CLM-C10-06** (computationally supported): For carry rules with two or more nonzero b\_j, the average digit-change cost per increment converges to a constant exceeding 1 + 1/(m - B) (measured excess: 0.500 for 3-\>(1,1), 0.333 for 4-\>(1,1), 0.643 for 3-\>(0,1,1), 0.714 for 3-\>(1,0,1), 0.831 for 4-\>(1,1,1)), equal to an expectation under the invariant measure of the digit process. *Evidence:* EXP-C10-03.
* **CLM-C10-07** (computationally supported): In canonical skew binary, every increment changes at most 2 digits and the average is 3/2 (n \< 1e6). *Evidence:* EXP-C10-01.
* **CLM-C11-08** (computationally supported): Among fixed (untuned) universal codes, a pattern-terminated code (T\_101, T\_0111 or T\_00111) has the smallest expected length on 5 of 12 synthetic sources (Zipf 1.1, geometric 0.001, uniform 2\^16, uniform 2\^32, log-uniform on \[1, 1e6\]) and on both posting-list data sets, beating the best classical universal code (Elias, Levenshtein, Fibonacci, Fraenkel-Klein C3, LEB128, fixed Exp-Golomb) by 0.34-3.06 bits per value; on Zipf 1.1, log-uniform and the bursty posting list it also beats Golomb and Exp-Golomb codes tuned to the source. It loses on light-tailed sources (Zipf \>= 1.5, geometric \>= 0.01, prime gaps) and to tuned Golomb/Exp-Golomb codes on geometric and uniform sources, and the reference implementation is 4-10 times slower than the Elias and Exp-Golomb codes. *Evidence:* EXP-C11-03, EXP-C11-04, EXP-C11-05, EXP-C11-09.
* **CLM-C12-12** (computationally supported): The Grundy values of the subtraction game whose move set is the set of primes satisfy g(n) \<= 11 for all n. *Evidence:* EXP-C12-03, EXP-C12-01.
* **CLM-C12-13** (conjecture): The Grundy values of the subtraction game with move set {1, 2, 3, 5, 8, ...} (Fibonacci numbers) are bounded; the observed maximum is 14 for n \<= 2e5. *Evidence:* EXP-C12-03, EXP-C12-01.
* **CLM-C14-12** (computationally supported): Every connected graph has exactly one factorisation into connected primes with respect to the product (g,h) \~ (g',h') iff (EA, AE, AA or NN); equivalently every graph with connected complement factors uniquely under the symmetric-difference product into primes with connected complement. *Evidence:* EXP-C14-04.
* **CLM-C14-13** (computationally supported): Every switching class of finite graphs has a unique factorisation into prime switching classes with respect to the product induced by the symmetric difference (equivalently, symmetric +-1 matrices with unit diagonal up to signed permutation similarity, under the Kronecker product). *Evidence:* EXP-C14-05.
* **CLM-C17-04** (computationally supported): On cyclic groups, anchored tables, random magmas and their one-entry corruptions (n = 32..512), Light's test with a greedy generating set uses 23-614 times fewer table probes than the exhaustive n\^3 check (generating-set cost included) and the anchored test 2n\^2 probes; on left-zero bands the gain is only 1.7x. The randomised test (40 rounds) made no error; random-triple sampling with n\^2/16 samples missed 27 of 30 near-associative inputs. *Evidence:* EXP-C17-01.
* **CLM-C17-05** (computationally supported): For 2 \<= N \<= 10, an anchored magma satisfies x\*(y+1) = (x\*y)\*(x+1) for all x, y mod N exactly when N is 2, 4 or 8 and the magma is the Laver table; so for these N, left-distributivity of an anchored table is decided by an O(N\^2) check. *Evidence:* EXP-C17-02.

## Directions proposed by the research cycles

**C01 — Quantity as the complete invariant of rewriting.**

* C01: prove the injectivity lemma that completes the one-common-border case (CLM-C01-10), then attack two or more common borders
* C01: full Lean formalisation of the border-containment theorem
* C01: Lean formalisation of the min/gcd theorem (Bezout over N)
* C01: common-border formula for pairs of relations?

**C02 — Exchange systems: positional numeration as normal forms.**

* C02: explicit bound n0 for critical rules; Lean formalisation of Theorem 10 (Perron-Frobenius argument)
* C02: longest Zeckendorf game - closed form or asymptotics
* C02: which carry rules have regular representation languages?

**C03 — Termination of one-rule string rewriting 0\^p 1\^q -\> 1\^r 0\^s.**

* C03: retrieve the Zantema-Geser theorem statement and compare with H-C03-4
* C03: implement RFC match-bounds to prove termination of the 24 open rules (start with 0011 -\> 111000 and 0011 -\> 11100000)
* C03: prove that every base rule 0 1\^q -\> 1\^r 0\^k (q \< r \< 2q, k \>= 2) loops from 0 1\^(q(q+1)); explain k\^q loop lengths
* C03: Lean formalisation of the conservation theorem (s = p)

**C04 — Derivation lengths, random descent and rewriting games.**

* C04: decide termination of aab -\> ababa and aab -\> babaa
* C04: games of aba -\> u and bab -\> u (alternating runs)
* C04: complexity census for \|l\| = 4 - new non-rational classes? cubic growth?
* C04: OEIS submissions (0.06 Grundy values; formula for A247983) - human decision

**C05 — Spectra of single-identity magma varieties.**

* C05: decide law 1286 at orders 8, 10 and law 677/1313 at 8, 10 with stronger symmetry breaking; certify
* C05: test the conjecture spec(677) = spec(1313) = {1} + odd n \>= 5
* C05: extend the census to order-5 laws and three-variable identities
* C05: Lean-formalise orbit-counting arguments for other laws with a finite-order pair map

**C06 — Successor-anchored magmas: spectra of composition laws.**

* C06: prove the finite spectra {1,2} and {1,3} (CLM-C06-10) by showing every anchored model of those laws is affine
* C06: which subsets of N arise as anchored spectra? They are closed under coprime products (CLM-C06-12), so never the primes; are they always closed under divisors? (bold)
* C06: larger terms - are there non-LD laws with power-of-two (Laver-like, non-affine) spectra?
* C06: Lean formalisation of the golden-law correspondence (Theorem 6)

**C07 — Arithmetic from the minimal excludant: a census of mex-defined operations.**

* C07: rows a \>= 3 of D\[x\^y\] - an exploratory look suggested row 3 is injective and rows 4-6 are not; is there a recursive block structure?
* C07: prove (or refute) that the 33 remaining specs equal their associative formulas for all a, b
* C07: submit the Jacobsthal row and selected census sequences to the OEIS (human decision)
* C07: which mex operations are automatic sequences (2-automatic tables)? A Walnut-style decision procedure would turn observations into proofs

**C08 — Circle multiplications on recurrence numeration systems.**

* C08: complete the Lean proof of the shifted Knuth theorem
* C08: prove non-Pisot never-associativity (CLM-C08-02)
* C08: compute greedy windows to prove the sign-of-beta conjecture (CLM-C08-04)
* C09: arithmetic of the circle semigroup - irreducibles and factorisation

**C09 — Arithmetic of Knuth's circle semigroup.**

* C09: prove the density-1/phi\^2 conjecture
* C09: characterise circle irreducibles via prime factorisation in Z\[phi\] plus a unit-window condition
* C09: arithmetic of other associative circle products (Pell, tribonacci)

**C10 — The cost of counting across representations.**

* C10: exact multi-offset counting constants via the invariant measure of the digit process

**C11 — Pattern-terminated universal integer codes.**

* C11: table-driven (byte-wise) decoders for T\_p and a fair speed comparison with optimised Elias and Fibonacci decoders
* C11: multi-pattern terminators (sets of delimiters, as in multi-delimiter codes) and the best set per source
* C11: synchronisation and robustness after bit errors for unbordered terminators (the classical selling point of Fibonacci codes)
* C11: exact oscillation constants for the average gain of T\_011 over C3 (as Proposition 5 does for 1\^k)

**C12 — Relational one-heap games.**

* C12: boundedness of the Grundy values of subtract-a-prime (11) and subtract-a-Fibonacci (14); convergence of the Fibonacci P-density (\<= 1/5)
* C12: forbidden-move perturbations - for which d0 does forbidding 'subtract d0' in G01 give finitely many exceptional odd parts as in Theorem 8?
* C12: prove g(m) \< m/4 for odd m in the non-coprime game G06 (max ratio 0.24985 up to 5000)
* C12: formalise Theorem 8 in Lean (finite certificate plus the shift-invariance lemma)

**C14 — Graphs as quantities: the 256 local graph products.**

* C14: prove or refute that two-graphs are a free commutative monoid under the symmetric-difference product (twin reducts; analogue of McKenzie's theorem for Kronecker products of +-1 matrices)
* C14: unique factorisation of product 141 on connected graphs (no collision to order 15)
* C14: classify the graphs G that absorb switching (G xor X = G xor X\^Z for all X); K\_{a,a} do
* C14: characters for directed graphs and for products of graphs with loops

**C17 — Deciding laws of finite magmas: generator, anchor and randomised tests against the exhaustive check.**

* C17: prove CLM-C17-05 for all N (anchored + wrap-around LD instance =\> Laver table, N a power of 2)
* C17: generator-based tests for other laws (left-distributivity, mediality) - which laws admit a Light-type reduction?
* C17: benchmark against optimised C implementations and against SAT-based model checkers

**C20 — Open problems revisited: the last one-rule systems of C04, and a literature check for C03.**

* C20: obtain the Zantema-Geser (2000) theorem and compare with C03 Conjecture 4.6 (human with library access)
* C20: derivational complexity of all terminating barren one-rule systems with \|l\| \<= 4 - is it always n - O(1), polynomial or 2\^Theta(n)?
* C20: formalise Theorems 1-2 of proofs/paper/C20.md in Lean (run encoding + journeys)
