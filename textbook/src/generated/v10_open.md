# Open problems {.unnumbered}

*Volume 10 — Open problems and future research. Generated from the claim database and the cycle records.*

## Unproven claims

Each of these is supported by the evidence cited in its record but has no proof. A proof or a counterexample would settle it.

* **CLM-C01-08** (computationally supported): For all words u != v of equal length k over a q-letter alphabet, the number of congruence classes of length-n words modulo u = v has generating function c(x) / (x\^k + (1 - q x) c(x)), where c(x) = 1 + sum over words b that are borders of both u and v of x\^(k - \|b\|). *Evidence:* EXP-C01-05, EXP-C01-06, EXP-C01-07.
* **CLM-C01-09** (computationally supported): If u != v have length k over a q-letter alphabet and no word is a border of both, the class counts of length-n words modulo u = v have generating function 1/(1 - q x + x\^k). *Evidence:* EXP-C01-06, EXP-C01-07, EXP-C01-08.
* **CLM-C01-10** (computationally supported): If u != v of length k share exactly one common border z (neither border set containing the other), the class counts have generating function c/(x\^k + (1 - q x) c) with c = 1 + x\^(k - \|z\|). *Evidence:* EXP-C01-06, EXP-C01-07, EXP-C01-08.
* **CLM-C01-11** (computationally supported): For words u != v of equal length, the one-rule system {u -\> v} is confluent if and only if every border of u is a border of v. *Evidence:* EXP-C01-08.
* **CLM-C03-10** (computationally supported): 0\^p 1\^q -\> 1\^r 0\^s (p, q, r, s \>= 1) is non-terminating iff (a) r \>= 2q and s \>= 2p, or (b) s \>= 2p, q \< r \< 2q and p divides s, or (c) r \>= 2q, p \< s \< 2p and q divides r. Otherwise it terminates. *Evidence:* EXP-C03-02, EXP-C03-03, EXP-C03-04.
* **CLM-C03-11** (computationally supported): For 0 1\^q -\> 1\^(q+1) 0\^k the rightmost strategy from 0 1\^(q(q+1)) reaches a self-embedding after 16, 32, 64 steps (k = 2) and 260, 1556, 9332 steps (k = 6) for q = 4, 5, 6. *Evidence:* EXP-C03-04.
* **CLM-C04-03** (computationally supported): The one-rule systems aab -\> ababa and aab -\> babaa over {a,b} (and their images under reversal and letter exchange) are terminating. *Evidence:* EXP-C04-02.
* **CLM-C04-12** (computationally supported): The 162 terminating rules (55 symmetry classes) have derivational complexity linear (144 rules, of which 4 are n - Theta(log n)), quadratic (14: floor(n\^2/4), floor(n(n-1)/6), floor(n\^2/8)) or exponential (4: 2\^(n-1) - 1); for 54 of the 55 classes D(n) = floor((a n\^2 + b n + c)/d) or 2\^(n-1) - 1 on all computed terms. *Evidence:* EXP-C04-03.
* **CLM-C04-16** (conjecture): The Grundy sequences of the rewriting games of aa -\> ab, aaa -\> b and aaa -\> ab on the words a\^n are ultimately periodic. *Evidence:* EXP-C04-08, EXP-C04-09.
* **CLM-C08-02** (computationally supported): If the minimal linear recurrence of an increasing base sequence G (G\_0 = 1) has a characteristic root beta other than the dominant root with \|beta\| \>= 1, then the circle product o\_s is non-associative for every s \>= 0. *Evidence:* EXP-C08-02.
* **CLM-C08-03** (computationally supported): For base sequences satisfying the dominant-root conditions of Grabner-Petho-Tichy-Woeginger (1994), the circle product is associative once the shift parameter is large enough. *Evidence:* EXP-C08-02, EXP-C08-03.
* **CLM-C08-04** (computationally supported): For quadratic Pisot base sequences with real conjugate root beta \> 0, the set of shifts s for which o\_s is associative is upward-closed. Sets that are not upward-closed (e.g. {2} and s \>= 4 for G = 1,3,4,7,11,...) occur only when beta \< 0. *Evidence:* EXP-C08-04, EXP-C08-03.
* **CLM-C08-05** (computationally supported): Smallest shift s0 with o\_s associative for all tested s0 \<= s \<= max tested: Fibonacci 2, Pell (1,2,5) 1, G(k+1)=2G(k)+2G(k-1) (1,2) 5, tribonacci 3, 4-bonacci 7, G(k+1)=G(k)+G(k-2) 10, G(k+1)=3G(k)+3G(k-1) (1,5) 10; G(k+1)=G(k)+G(k-3) none up to 20 (full table in results/EXP-C08-02.json and EXP-C08-03.json). *Evidence:* EXP-C08-02, EXP-C08-03.
* **CLM-C09-05** (conjecture): Almost every n whose conjugate lies in the product zone is a circle product, so the circle irreducibles have natural density 1/phi\^2. *Evidence:* EXP-C09-04, EXP-C09-01.
* **CLM-C10-06** (computationally supported): For carry rules with two or more nonzero b\_j, the average digit-change cost per increment converges to a constant exceeding 1 + 1/(m - B) (measured excess: 0.500 for 3-\>(1,1), 0.333 for 4-\>(1,1), 0.643 for 3-\>(0,1,1), 0.714 for 3-\>(1,0,1), 0.831 for 4-\>(1,1,1)), equal to an expectation under the invariant measure of the digit process. *Evidence:* EXP-C10-03.
* **CLM-C10-07** (computationally supported): In canonical skew binary, every increment changes at most 2 digits and the average is 3/2 (n \< 1e6). *Evidence:* EXP-C10-01.

## Directions proposed by the research cycles

**C01 — Quantity as the complete invariant of rewriting.**

* C01: prove the common-border conjecture (Hilbert series / Anick chains, or parametric completions)
* C01: full Lean formalisation of the border-containment theorem
* C01: Lean formalisation of the min/gcd theorem (Bezout over N)
* C01: common-border formula for pairs of relations?

**C02 — Exchange systems: positional numeration as normal forms.**

* C02: explicit bound n0 for critical rules; Lean formalisation of the spectral argument
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
