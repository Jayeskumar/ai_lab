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
  *Counterexample:* 011 -\> 11100 (r = 3 \< 4 = 2q) loops: 001111 -\>4 111 001111 00100 (Lean-verified, not\_terminating\_0\_11). 35 counterexamples with parameters \<= 5 (EXP-C03-02).
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
