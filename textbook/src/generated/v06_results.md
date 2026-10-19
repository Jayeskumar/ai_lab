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
* **CLM-C01-09** (written), rediscovery: Common-border formula when u and v share no border (c = 1) - consequence of published results.

**Computationally supported.**

* **CLM-C01-08**, potentially novel: Common-border conjecture: one-relation class counts depend only on common borders.
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
* **CLM-C03-10** (written), rediscovery: Divisibility characterization of termination for 0\^p 1\^q -\> 1\^r 0\^s (H-C03-4).

**Computationally supported.**

* **CLM-C03-11**, rediscovery: Loop lengths in the base family grow like k\^q.

## C04 — Derivation lengths, random descent and rewriting games

**Theorems.**

* **CLM-C04-01** (computer-assisted), rediscovery: Termination census of one-rule systems with \|l\|, \|r\| \<= 3: non-terminating iff l is a factor of r.
* **CLM-C04-03** (written), rediscovery: The rules aab -\> ababa and aab -\> babaa (and their six symmetric images) terminate.
* **CLM-C04-04** (Lean), rediscovery: ab -\> ba: every derivation has inv(w) steps, D(n) = floor(n\^2/4), P-positions = even inversion count.
* **CLM-C04-05** (Lean), rediscovery: One-rule systems with an unbordered left-hand side have random descent (Lean-verified).
* **CLM-C04-06** (written), rediscovery: Every one-rule system has a constant-step potential; for terminating ones confluence is equivalent to random descent.
* **CLM-C04-08** (written), rediscovery: Rewriting games of random-descent rules are parity games (Grundy value = D(w) mod 2).
* **CLM-C04-09** (written), potentially novel: The rule aab -\> ba has derivational complexity D(n) = n - 1 - min{k : 2\^k + k \>= n} (non-rational).
* **CLM-C04-10** (written), potentially novel: Identity: OEIS A247983 (truncation index of the series for log 2) equals D(n+2) for aab -\> ba.
* **CLM-C04-13** (written), rediscovery: Rewriting games with lhs a\^k are take-and-break games: aa -\> b is Dawson's Kayles, aa -\> ab is Officers.
* **CLM-C04-15** (computer-assisted), rediscovery: The rewriting game of aa -\> b on a\^n has Grundy values periodic with period 34 from n = 53.

**Computationally supported.**

* **CLM-C04-12**, rediscovery: Complexity classes and closed forms of the 162 terminating rules with \|l\|, \|r\| \<= 3.

**Conjectures.**

* **CLM-C04-16**, rediscovery: Open: are the rewriting games of aa -\> ab (Officers), aaa -\> b (0.007) and aaa -\> ab (0.06) ultimately periodic?.

## C05 — Spectra of single-identity magma varieties

**Theorems.**

* **CLM-C05-04** (Lean), rediscovery: Law 167, x = (y\*x)\*(x\*y): every finite model has order 0 or 1 mod 4.
* **CLM-C05-05** (Lean), rediscovery: Identities x = y\*s(x, y) make every left translation of a finite model bijective.
* **CLM-C05-07** (Lean), potentially novel: New spectrum memberships for open ETP laws: 677 has models of orders 5, 7, 9; 1286, 1313 and 1516 have models of order 9.
* **CLM-C05-08** (computer-assisted), potentially novel: New spectrum gaps for open ETP laws (certified UNSAT): 501 has no models of orders 6, 7; 677 none of order 6; 883 none of 6; 1076 none of 8; 1083 none of 5, 6.
* **CLM-C05-10** (computer-assisted), not assessed: Linear models over finite fields: the orders q \<= 128 at which the 15 open laws have a model x\*y = ax + by over GF(q).

**Computationally supported.**

* **CLM-C05-02**, rediscovery: Spectrum census of the 115 nontrivial two-variable identities t = x with 2-4 operations (n \<= 6, restricted ones to n \<= 8).

## C06 — Successor-anchored magmas: spectra of composition laws

**Theorems.**

* **CLM-C06-02** (Lean), rediscovery: Anchored associativity forces x\*y = x + y + 1, for every N.
* **CLM-C06-03** (Lean), rediscovery: Anchored right-distributivity forces x\*y = x + 1, for every N.
* **CLM-C06-05** (written), rediscovery: Anchored right-permutable magmas are x\*y = x + c(y); there are N\^(N-1) of them.
* **CLM-C06-06** (Lean), potentially novel: An 'odd' law: (xy)z = x((yz)z) has an anchored model exactly for odd N, and it is unique.
* **CLM-C06-07** (written), potentially novel: A 'golden' law: anchored models of (xy)z = x(y(zz)) correspond to roots of a\^2 + a = 1 mod N.
* **CLM-C06-08** (Lean), rediscovery: Anchored left-permutable magmas are commutative monoids in disguise (counted by OEIS A058156).
* **CLM-C06-12** (written), rediscovery: Anchored spectra are closed under coprime products.

**Computationally supported.**

* **CLM-C06-01**, rediscovery: Left-distributivity with a successor anchor: the Laver tables (rediscovery).
* **CLM-C06-10**, potentially novel: Laws with finite anchored spectra {1, 2} and {1, 3}.
* **CLM-C06-11**, potentially novel: Mirror twins of the golden and odd laws.

## C07 — Arithmetic from the minimal excludant: a census of mex-defined operations

**Theorems.**

* **CLM-C07-01** (computer-assisted), potentially novel: The associative mex operations are 0, projections, min, +, XOR, nim-product and four relatives.
* **CLM-C07-03** (written), not assessed: In a mex operation with both L and R options 0 is an identity; with neither, 0 is absorbing.
* **CLM-C07-05** (written), potentially novel: The Jacobsthal row: row 2 of f(a,b) = mex{f(a',b) XOR f(a,b')} swaps the blocks \[2\^k - J\_k, 2\^k) and \[2\^k, 2\^k + J\_k).

**Computationally supported.**

* **CLM-C07-08**, not assessed: Additive periodicity is the exception among mex operations.

## C08 — Circle multiplications on recurrence numeration systems

**Theorems.**

* **CLM-C08-01** (Lean), rediscovery: Every shifted Knuth product a o\_t b = sum F(k+l+t) over Zeckendorf indices is associative (t \>= 0).

**Computationally supported.**

* **CLM-C08-02**, potentially novel: Circle products over non-Pisot base sequences are never associative.
* **CLM-C08-03**, rediscovery: Recurrences with non-increasing coefficients and canonical initial values give associative circle products for large shifts.
* **CLM-C08-04**, potentially novel: Non-monotone associative-shift sets require a negative conjugate root.
* **CLM-C08-08**, rediscovery: Associativity thresholds after the targeted search - certified lower bounds, no failure up to s = 16.

## C09 — Arithmetic of Knuth's circle semigroup

**Theorems.**

* **CLM-C09-01** (written), rediscovery: Knuth's circle semigroup embeds in Z\[phi\]; Fibonacci numbers are its units-images.
* **CLM-C09-03** (written), potentially novel: Window obstruction: at least a proportion 1/phi\^2 of all integers are circle-irreducible.
* **CLM-C09-06** (written), potentially novel: Factorisation lengths are bounded by the conjugate coordinate.
* **CLM-C09-07** (written), rediscovery: The norm N(n) = n\*\^2 + n n\* - n\^2 is multiplicative for the circle product.
* **CLM-C09-08** (computer-assisted), potentially novel: Factorisation statistics of the circle semigroup up to 2e5.

**Conjectures.**

* **CLM-C09-05**, potentially novel: The density of circle irreducibles is exactly 1/phi\^2.

## C10 — The cost of counting across representations

**Theorems.**

* **CLM-C10-01** (written), rediscovery: Average cost of counting in classical representations (b/(b-1), e-1, 1).
* **CLM-C10-02** (written), rediscovery: Zeckendorf counting: T\_m = 2 G\_m - ceil(m/2) - 2, average cost 2.
* **CLM-C10-04** (written), rediscovery: Exchange systems fire 1/(m - sum b) times per increment on average.
* **CLM-C10-05** (written), rediscovery: Single-offset exchange rules cost exactly firings + 1 per increment (average 1 + 1/(m - q)).
* **CLM-C10-07** (written), rediscovery: Skew binary counting has worst-case cost 2 and average 3/2.

**Computationally supported.**

* **CLM-C10-06**, potentially novel: Multi-offset exchange rules have rule-specific average counting costs.

## C11 — Pattern-terminated universal integer codes

**Theorems.**

* **CLM-C11-01** (written), rediscovery: Pattern-terminated codes T\_p are complete prefix codes with counts x\^k / (x\^k + (1-2x) c\_p(x)); T\_11 is the Fibonacci code.
* **CLM-C11-02** (written), rediscovery: The all-ones terminator 1\^k (and 0\^k) uniquely maximises the growth rate among length-k patterns.
* **CLM-C11-03** (written), rediscovery: Unbordered terminators: F\_u = x/(1-x) F\_(1\^k), so codeword counts are partial sums of the all-ones counts.
* **CLM-C11-04** (written), potentially novel: T\_011 is never longer than the Fibonacci code for n \>= 5 and one bit shorter on all but L values per level.
* **CLM-C11-07** (written), potentially novel: The average gain oscillates between (2-lambda)/(lambda-1)\^2 and lambda(2-lambda)/(lambda-1).
* **CLM-C11-09** (written), potentially novel: T\_011 is never longer than Fraenkel-Klein's C3 except at n = 2, 4, 8; C3 is never longer than C1 except at n = 1.

**Computationally supported.**

* **CLM-C11-08**, not assessed: Fixed pattern-terminated codes beat classical universal codes on heavy-tailed and wide-range sources (mixed result).

## C12 — Relational one-heap games

**Theorems.**

* **CLM-C12-01** (written), rediscovery: Divisibility games: subtract a proper divisor = v2, subtract a divisor = v2 + 1, move to a divisor = Omega.
* **CLM-C12-02** (written), rediscovery: Coprimality games: index of the smallest prime factor; the non-coprime game has g(2k) = k - 1.
* **CLM-C12-03** (Lean), rediscovery: P-positions of the deleting-divisors game (subtract d \| n with 1 \< d \< n): 0, odd numbers, 2\^(2j+1).
* **CLM-C12-04** (computer-assisted), potentially novel: Grundy function of the deleting-divisors game: v2(n) except on odd parts \<= 15.
* **CLM-C12-05** (written), rediscovery: Bitwise and quotient games: popcount, floor(log2((n+1)/3)) + 1 and floor(log2 n).
* **CLM-C12-06** (written), rediscovery: Residue lemma; subtract-a-power-of-k has the Grundy function of the subtraction game {1, k}.
* **CLM-C12-07** (Lean), rediscovery: Splitting games in which every heap can be split have g(n) = \[n even\].
* **CLM-C12-08** (written), rediscovery: Subtract-a-square and subtract-a-triangular-number have infinite density-zero P-sets and are not periodic.

**Computationally supported.**

* **CLM-C12-12**, rediscovery: Subtract-a-prime has Grundy values at most 11.

**Conjectures.**

* **CLM-C12-13**, not assessed: Subtract-a-Fibonacci-number has bounded Grundy values.

## C13 — Anchored spectra II: which sets of integers are spectra?

**Theorems.**

* **CLM-C13-01** (written), rediscovery: Affine anchored spectra are root sets of polynomial systems - divisor-closed, CRT-closed, finite ones are divisor sets.
* **CLM-C13-02** (Lean), potentially novel: Right-normed laws (xy)z = x V(y,z) have only translation models.
* **CLM-C13-03** (Lean), potentially novel: The W-family: anchored models of (xy)z = x(y W(z)) are the affine tables with a\*c\_W(a) = 1.
* **CLM-C13-04** (Lean), potentially novel: Exact finite spectra {1,3} and {1,2} for x(yz) = ((zx)x)y and x(yz) = ((xy)z)x.
* **CLM-C13-05** (Lean), not assessed: The law x = x(x(xx)) has anchored models of every size except 2.
* **CLM-C13-06** (computer-assisted), not assessed: Offset congruence closure is a sound prover of finite anchored spectra; it settles 16 of the 17 laws of CLM-C06-10.
* **CLM-C13-11** (written), potentially novel: Single laws whose affine spectra are classical arithmetic sets.

**Computationally supported.**

* **CLM-C13-10**, not assessed: Spectra of one-variable laws are finite or cofinite.
* **CLM-C13-12**, not assessed: Non-affine models typically exist for all sizes beyond a small threshold; no Laver-like sparse spectrum found.

## C14 — Graphs as quantities: the 256 local graph products

**Theorems.**

* **CLM-C14-01** (Lean), not assessed: Associativity of a local graph product is a finite identity on relations, detected by P3 x P3 x P3 (Lean).
* **CLM-C14-02** (Lean), rediscovery: Exactly 20 of the 256 local graph products are associative, 10 commutative, 8 with unit K1 (Lean decide).
* **CLM-C14-03** (computer-assisted), not assessed: For local graph products, associativity and commutativity up to isomorphism are no weaker than the strict notions.
* **CLM-C14-04** (written), potentially novel: Exactly six local products are Kronecker products in disguise (multiplicative characters).
* **CLM-C14-05** (written), potentially novel: Additive characters: only the Cartesian product and its complement-dual; every non-trivial commutative associative product has a character.
* **CLM-C14-06** (written), rediscovery: The symmetric-difference product is the Kronecker product of Seidel matrices; it acts on two-graphs.
* **CLM-C14-07** (written), potentially novel: Complete bipartite graphs multiply as (order, imbalance); K2 absorbs Seidel switching.
* **CLM-C14-09** (written), rediscovery: The Cartesian and strong product monoids of all finite graphs are isomorphic graded monoids; equal prime counts (A129582).
* **CLM-C14-10** (computer-assisted), potentially novel: Numbers of prime graphs (all graphs) for the unital associative products, orders \<= 15.
* **CLM-C14-11** (written), rediscovery: The lexicographic product has non-unique factorisation already at order 10 (different multisets of primes).

**Computationally supported.**

* **CLM-C14-12**, not assessed: Code 141 (EA AE AA NN) has unique factorisation on connected graphs (equivalently, symmetric difference on co-connected graphs).
* **CLM-C14-13**, potentially novel: H-C14-4: two-graphs form a free commutative monoid under the symmetric-difference (Kronecker) product.

## C15 — Magma cellular automata: light cones, streaming width and fast-forwarding

**Theorems.**

* **CLM-C15-01** (Lean), rediscovery: Light cones of semigroups - the popcount word, Pascal exponents, bounded streaming width.
* **CLM-C15-02** (written), rediscovery: Affine magmas - binomial light cone and an O(L log L log t) fast-forward.
* **CLM-C15-03** (written), not assessed: Commutative semigroups - fast-forward by exponent arithmetic.
* **CLM-C15-04** (written), potentially novel: The fuse magma: linear streaming width, yet an O(L) fast-forward for every t.
* **CLM-C15-05** (computer-assisted), rediscovery: Surjective iff permutive for magmas of order at most 3; false at order 4.
* **CLM-C15-06** (written), rediscovery: The two-element magma automata are the elementary rules 17m.

**Computationally supported.**

* **CLM-C15-07**, potentially novel: Census of order-3 magma automata by streaming width.
* **CLM-C15-13**, rediscovery: Affine fast-forward by operator powers.
* **CLM-C15-14**, not assessed: Commutative-semigroup fast-forward by exponent arithmetic.
* **CLM-C15-15**, potentially novel: Fuse fast-forward by burn times.
* **CLM-C15-16**, rediscovery: Cycle detection as a generic fast-forward.
* **CLM-C15-17**, not assessed: Earlier structures of the lab as automata.

**Conjectures.**

* **CLM-C15-18**, not assessed: Bounded streaming width implies a fast-forward.

## C16 — Fibonacci dynamics in invented finite algebras

**Theorems.**

* **CLM-C16-01** (Lean), rediscovery: The Fibonacci pair map of a magma is a permutation iff every left translation is a bijection.
* **CLM-C16-03** (written), rediscovery: Full-period magmas are de Bruijn cycles: there are (n!)\^n / n\^2 of them.
* **CLM-C16-04** (written), not assessed: A parity condition for full periods.
* **CLM-C16-05** (written), potentially novel: Full-period quasigroups are cycles in which every pair occurs once at distance 1 and once at distance 2.
* **CLM-C16-07** (computer-assisted), potentially novel: Full-period quasigroups: none of order 2, 3, 4; 3360 of order 5; examples of every order 6-16.
* **CLM-C16-08** (written), not assessed: Direct products of full-period magmas of coprime orders are full-period.
* **CLM-C16-09** (written), potentially novel: No isotope of a group of even order has a full-period Fibonacci pair map.
* **CLM-C16-11** (Lean), not assessed: Fixed points of the pair map are idempotents.
* **CLM-C16-12** (written), rediscovery: Affine magmas: periods are orders of companion matrices; the anchored magma x + y + 1 is the Fibonacci sequence mod N.
* **CLM-C16-14** (written), rediscovery: Fibonacci sequences of nimbers: maximal period pi(2\^(2\^k) - 1).
* **CLM-C16-15** (written), potentially novel: Laver tables: every Fibonacci orbit ends in the fixed point or one of the N - 1 two-cycles through the top element.
* **CLM-C16-18** (computer-assisted), not assessed: Maximal Fibonacci periods of small groups.

**Computationally supported.**

* **CLM-C16-10**, not assessed: Full-period quasigroups exist for every order n \>= 5.
* **CLM-C16-13**, not assessed: For affine magmas the maximal period equals the order of the 3x3 affine matrix.
* **CLM-C16-16**, not assessed: Fibonacci orbits in Laver tables reach the top element within 5 steps (n \<= 10).
* **CLM-C16-17**, rediscovery: Magma Fibonacci generators are not competitive pseudo-random generators.
* **CLM-C16-19**, not assessed: Random sampling finds full-period quasigroups where exact search fails.

## C17 — Deciding laws of finite magmas: generator, anchor and randomised tests against the exhaustive check

**Theorems.**

* **CLM-C17-01** (written), rediscovery: Light's test: generators suffice for associativity.
* **CLM-C17-02** (written), not assessed: Associativity of an anchored magma is decided by one O(n\^2) identity.
* **CLM-C17-03** (written), rediscovery: The Rajagopalan-Schulman randomised associativity test is one-sided.

**Computationally supported.**

* **CLM-C17-04**, rediscovery: Benchmark - generator and anchor tests versus the exhaustive check.
* **CLM-C17-05**, not assessed: The anchor instance of left-distributivity singles out the Laver tables (every N \<= 4096).

## C18 — Invented operations as mixing primitives: quasigroup string transformations versus standard hashes

**Theorems.**

* **CLM-C18-01** (Lean), rediscovery: e-transformations are bijections of strings of fixed length.
* **CLM-C18-02** (Lean), not assessed: Differences propagate forward only; forward-only tail hashes fail the strict avalanche criterion.
* **CLM-C18-03** (Lean), not assessed: The tail-information bound: an e-transformation tail carries one byte of state.
* **CLM-C18-04** (written), rediscovery: T-function quasigroups (affine mod 256, XOR, (x + 1) XOR y) cannot mix high input bits into low output bits.
* **CLM-C18-05** (written), rediscovery: GF(2)-affine quasigroups give GF(2)-affine hashes with key-independent differences.
* **CLM-C18-06** (written), not assessed: The anchored quasigroup x + c(y): additive differences persist, and the one-pass hash is anagram-blind.
* **CLM-C18-07** (written), not assessed: The 8-pass cascade has a bijective 64-bit state update.

**Computationally supported.**

* **CLM-C18-08**, not assessed: H-C18-1: QG-LS with 2 passes and a reverse pass has BLAKE2b-level avalanche.
* **CLM-C18-13**, not assessed: Quasigroup hashes against non-cryptographic baselines - no significant improvement.

## C19 — The longest Zeckendorf game

**Theorems.**

* **CLM-C19-01** (written), rediscovery: Every Zeckendorf game has length B(n) - sum\_{i\>=2} (i-1) MC\_i.
* **CLM-C19-02** (written), potentially novel: The split phase of the longest game ends at the lazy Fibonacci representation.
* **CLM-C19-03** (written), potentially novel: Closed form of the longest game on a Fibonacci number: L(F\_k) = F\_{k+2} - k - 2 - floor((k-1)\^2/4).
* **CLM-C19-04** (written), rediscovery: A short proof that only n = F\_k - 1 can be played with split moves alone (Cusenza et al., Thm 1.4).
* **CLM-C19-07** (computer-assisted), rediscovery: Exact longest games for n \<= 150 and independent confirmation of the split-first strategy.
* **CLM-C19-08** (written), not assessed: Every multiset of Fibonacci numbers with sum n is a reachable game position.
* **CLM-C19-14** (written), potentially novel: Computing the longest game with O(log\^2 n) moves instead of Theta(n).
* **CLM-C19-15** (written), not assessed: The deficit of the longest Zeckendorf game is O(log\^2 n) - D(n) \<= 1 + (t+1)(t+6)/2, so L(n) = phi\^2 n - O(log\^2 n).

**Computationally supported.**

* **CLM-C19-05**, potentially novel: A two-sequence recursion for the longest Zeckendorf game on every n.
* **CLM-C19-06**, potentially novel: The deficit of a two-summand number depends only on the lower level and the parity of the gap.
* **CLM-C19-09**, not assessed: D(n) \<= floor(j\^2/4) for top level j, and L is strictly increasing.

## C20 — Open problems revisited: the last one-rule systems of C04, and a literature check for C03

**Theorems.**

* **CLM-C20-01** (written), rediscovery: aab -\> ababa terminates, with derivational complexity D(n) = 2\^(n-2) - 1.
* **CLM-C20-02** (written), potentially novel: aab -\> babaa terminates; exact per-word derivation length and D(n) = max\_b b(2\^floor((n-b)/2) - 1).
* **CLM-C20-03** (computer-assisted), not assessed: The C04 extended termination census is complete - 480 of the 868 rules with \|l\| \<= 3, \|r\| \<= 5 terminate.
* **CLM-C20-04** (written), rediscovery: C03 Conjecture 4.6 coincides with the Zantema-Geser characterisation.
