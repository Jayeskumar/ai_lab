# Catalogue of results {.unnumbered}

*Volume 6 — New conjectures and verified theorems. Generated from the claim database (`python -m lab catalogue`); every entry links to its record in `db/claims/`.*

Proof kinds: **Lean** — machine-checked; **computer-assisted** — a finite certificate checked by a program; **written** — a complete written proof in `proofs/paper/`. Novelty labels are those of the Historian's audit; *rediscovery* means the result is in the literature.

## C01 — Quantity as the complete invariant of rewriting

**Theorems.**

* **CLM-C01-01** (Lean), rediscovery: Symbol counts are the complete invariant of the commutation congruence.
* **CLM-C01-02** (Lean), rediscovery: One symbol, one relation a\^m = a\^(m+p) gives exactly m+p classes (index m, period p).
* **CLM-C01-03** (written), rediscovery: Several one-symbol relations have index min m\_i and period gcd(n\_i - m\_i).
* **CLM-C01-04** (written), rediscovery: Multiplication emerges as composition of substitutions; with two symbols it is non-commutative.
* **CLM-C01-06** (written), rediscovery: Border-containment theorem for one length-preserving relation.
* **CLM-C01-07** (computer-assisted), rediscovery: Common-border formula proved for 1632 specific relations by verified finite completions.

**Computationally supported.**

* **CLM-C01-08**, potentially novel: Common-border conjecture: one-relation class counts depend only on common borders.
* **CLM-C01-09**, rediscovery: Common-border formula when u and v share no border (c = 1) - consequence of published results.
* **CLM-C01-10**, potentially novel: Common-border formula with exactly one common border (derivation sketch from Gray-Steinberg 2022).
* **CLM-C01-11**, rediscovery: Converse of border containment: u -\> v (\|u\| = \|v\|) is confluent iff Borders(u) is contained in Borders(v).

## C02 — Exchange systems: positional numeration as normal forms

**Theorems.**

* **CLM-C02-01** (written), rediscovery: Integer bases emerge as normal forms of the exchange rule b\[k\] -\> \[k+1\].
* **CLM-C02-02** (written), rediscovery: Abelian property of carry rules (order of exchanges is irrelevant).
* **CLM-C02-03** (written), rediscovery: Termination dichotomy for carry rules away from sum b = m.
* **CLM-C02-04** (written), potentially novel: Carry rules with sum b = m never terminate from all unary starts (uniform glider).
* **CLM-C02-05** (computer-assisted), potentially novel: Termination classification for all 189 small carry rules (computer-assisted).
* **CLM-C02-07** (Lean), rediscovery: Uniqueness of representations when the reduced carry polynomial is primitive and irreducible.
* **CLM-C02-08** (written), rediscovery: Exchange representations respect the radix order.
* **CLM-C02-09** (written), rediscovery: The Fibonacci exchange system terminates at the Zeckendorf representation; shortest derivation n - z(n).
* **CLM-C02-10** (computer-assisted), rediscovery: Longest Fibonacci exchange derivations (longest Zeckendorf games) for n \<= 40.
* **CLM-C02-11** (written), potentially novel: Termination classification of carry rules: terminating from every unary start iff sum b \< m.

## C03 — Termination of one-rule string rewriting 0\^p 1\^q -\> 1\^r 0\^s

**Theorems.**

* **CLM-C03-01** (Lean), rediscovery: A one-rule system that decreases the count of some letter terminates.
* **CLM-C03-02** (written), rediscovery: Conserving rules terminate (s = p or r = q).
* **CLM-C03-03** (Lean), rediscovery: Self-embedding derivations prove non-termination; the doubling region r \>= 2q, s \>= 2p always loops.
* **CLM-C03-04** (Lean), rediscovery: 011 -\> 11100 is non-terminating although r \< 2q.
* **CLM-C03-05** (Lean), rediscovery: Lifting lemma - loops transfer along letter morphisms (explains divisibility).
* **CLM-C03-06** (computer-assisted), rediscovery: Classification of 601 of the 625 rules with p, q, r, s \<= 5 (computer-assisted).

**Computationally supported.**

* **CLM-C03-10**, rediscovery: Divisibility characterization of termination for 0\^p 1\^q -\> 1\^r 0\^s (H-C03-4).
* **CLM-C03-11**, not assessed: Loop lengths in the base family grow like k\^q.

## C04 — Derivation lengths, random descent and rewriting games

**Theorems.**

* **CLM-C04-01** (computer-assisted), not assessed: Termination census of one-rule systems with \|l\|, \|r\| \<= 3: non-terminating iff l is a factor of r.
* **CLM-C04-04** (Lean), rediscovery: ab -\> ba: every derivation has inv(w) steps, D(n) = floor(n\^2/4), P-positions = even inversion count.
* **CLM-C04-05** (Lean), rediscovery: One-rule systems with an unbordered left-hand side have random descent (Lean-verified).
* **CLM-C04-06** (written), not assessed: Every one-rule system has a constant-step potential; for terminating ones confluence is equivalent to random descent.
* **CLM-C04-08** (written), rediscovery: Rewriting games of random-descent rules are parity games (Grundy value = D(w) mod 2).
* **CLM-C04-09** (written), potentially novel: The rule aab -\> ba has derivational complexity D(n) = n - 1 - min{k : 2\^k + k \>= n} (non-rational).
* **CLM-C04-10** (written), potentially novel: Identity: OEIS A247983 (truncation index of the series for log 2) equals D(n+2) for aab -\> ba.
* **CLM-C04-13** (written), rediscovery: Rewriting games with lhs a\^k are take-and-break games: aa -\> b is Dawson's Kayles, aa -\> ab is Officers.
* **CLM-C04-15** (computer-assisted), rediscovery: The rewriting game of aa -\> b on a\^n has Grundy values periodic with period 34 from n = 53.

**Computationally supported.**

* **CLM-C04-03**, not assessed: The rules aab -\> ababa and aab -\> babaa (and their six symmetric images) terminate.
* **CLM-C04-12**, not assessed: Complexity classes and closed forms of the 162 terminating rules with \|l\|, \|r\| \<= 3.

**Conjectures.**

* **CLM-C04-16**, rediscovery: Open: are the rewriting games of aa -\> ab (Officers), aaa -\> b (0.007) and aaa -\> ab (0.06) ultimately periodic?.

## C08 — Circle multiplications on recurrence numeration systems

**Theorems.**

* **CLM-C08-01** (Lean), rediscovery: Every shifted Knuth product a o\_t b = sum F(k+l+t) over Zeckendorf indices is associative (t \>= 0).

**Computationally supported.**

* **CLM-C08-02**, not assessed: Circle products over non-Pisot base sequences are never associative.
* **CLM-C08-03**, rediscovery: Pisot base sequences give associative circle products for all sufficiently large shifts.
* **CLM-C08-04**, potentially novel: Non-monotone associative-shift sets require a negative conjugate root.
* **CLM-C08-05**, not assessed: Measured associativity thresholds for 45 base sequences.

## C09 — Arithmetic of Knuth's circle semigroup

**Theorems.**

* **CLM-C09-01** (written), rediscovery: Knuth's circle semigroup embeds in Z\[phi\]; Fibonacci numbers are its units-images.
* **CLM-C09-03** (written), potentially novel: Window obstruction: a fixed proportion 1/phi\^2 of all integers are circle-irreducible.
* **CLM-C09-06** (written), not assessed: Factorisation lengths are bounded by the conjugate coordinate.
* **CLM-C09-07** (written), not assessed: The norm N(n) = n\*\^2 + n n\* - n\^2 is multiplicative for the circle product.
* **CLM-C09-08** (computer-assisted), not assessed: Factorisation statistics of the circle semigroup up to 2e5.

**Conjectures.**

* **CLM-C09-05**, not assessed: The density of circle irreducibles is exactly 1/phi\^2.

## C10 — The cost of counting across representations

**Theorems.**

* **CLM-C10-01** (written), rediscovery: Average cost of counting in classical representations (b/(b-1), e-1, 1).
* **CLM-C10-02** (written), rediscovery: Zeckendorf counting: T\_m = 2 G\_m - ceil(m/2) - 2, average cost 2.
* **CLM-C10-04** (written), not assessed: Exchange systems fire 1/(m - sum b) times per increment on average.
* **CLM-C10-05** (written), not assessed: Single-offset exchange rules cost exactly firings + 1 per increment (average 1 + 1/(m - q)).

**Computationally supported.**

* **CLM-C10-06**, not assessed: Multi-offset exchange rules have rule-specific average counting costs.
* **CLM-C10-07**, rediscovery: Skew binary counting has worst-case cost 2 and average 3/2.
