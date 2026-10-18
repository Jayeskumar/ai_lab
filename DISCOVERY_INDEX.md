# Discovery Index

_Generated 2026-10-18T08:39:48Z by `python -m lab sync` from `db/claims/`. Do not edit by hand._

Every claim carries two independent labels: a **verification status** (PROVEN, COMPUTATIONALLY SUPPORTED, CONJECTURE, REFUTED, INCONCLUSIVE) and a **novelty status** (REDISCOVERY, POTENTIALLY NOVEL, NOT ASSESSED). A claim may therefore appear in more than one section below.

## Summary

| Verification status | Claims |
|---|---|
| PROVEN | 42 |
| COMPUTATIONALLY SUPPORTED | 13 |
| CONJECTURE | 2 |
| REFUTED | 12 |
| INCONCLUSIVE | 1 |

| Novelty status | Claims |
|---|---|
| REDISCOVERY | 36 |
| POTENTIALLY NOVEL | 9 |
| NOT ASSESSED | 25 |

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
| CLM-C04-01 | Termination census of one-rule systems with |l|, |r| <= 3: non-terminating iff l is a fac… | computer-assisted (Python) - explicit termination certifica… | NOT ASSESSED | EXP-C04-01 |
| CLM-C04-04 | ab -> ba: every derivation has inv(w) steps, D(n) = floor(n^2/4), P-positions = even inve… | Lean 4 + Mathlib (inv_step, normal_iff_inv_zero, derivation… | REDISCOVERY | EXP-C04-03, EXP-C04-07 |
| CLM-C04-05 | One-rule systems with an unbordered left-hand side have random descent (Lean-verified) | Lean 4 + Mathlib (random_descent, unbordered_diamond, unbor… | REDISCOVERY | EXP-C04-05 |
| CLM-C04-06 | Every one-rule system has a constant-step potential; for terminating ones confluence is e… | written proof (proofs/paper/C04.md Theorem 2); abstract con… | NOT ASSESSED | EXP-C04-05, EXP-C04-06 |
| CLM-C04-08 | Rewriting games of random-descent rules are parity games (Grundy value = D(w) mod 2) | written proof (proofs/paper/C04.md Theorem 9, induction on … | REDISCOVERY | EXP-C04-07 |
| CLM-C04-09 | The rule aab -> ba has derivational complexity D(n) = n - 1 - min{k : 2^k + k >= n} (non-… | written proof (proofs/paper/C04.md Theorem 7); per-word for… | POTENTIALLY NOVEL | EXP-C04-03, EXP-C04-04 |
| CLM-C04-10 | Identity: OEIS A247983 (truncation index of the series for log 2) equals D(n+2) for aab -… | written proof (proofs/paper/C04.md Theorem 8, Jensen's ineq… | POTENTIALLY NOVEL | EXP-C04-09, EXP-C04-10 |
| CLM-C04-13 | Rewriting games with lhs a^k are take-and-break games: aa -> b is Dawson's Kayles, aa -> … | written proof (proofs/paper/C04.md Theorem 10); word games … | REDISCOVERY | EXP-C04-07, EXP-C04-08 |
| CLM-C04-15 | The rewriting game of aa -> b on a^n has Grundy values periodic with period 34 from n = 53 | computer-assisted - octal recursion to n = 3000 and the Guy… | REDISCOVERY | EXP-C04-08 |
| CLM-C08-01 | Every shifted Knuth product a o_t b = sum F(k+l+t) over Zeckendorf indices is associative… | Lean 4 + Mathlib (Infinity.C08.circ_assoc, circ_comm, key, … | REDISCOVERY | EXP-C08-01, EXP-C08-03, EXP-C08-05 |
| CLM-C09-01 | Knuth's circle semigroup embeds in Z[phi]; Fibonacci numbers are its units-images | written proof (proofs/paper/C09.md Theorem 1) relying on CL… | REDISCOVERY | EXP-C09-03 |
| CLM-C09-03 | Window obstruction: a fixed proportion 1/phi^2 of all integers are circle-irreducible | written proof (proofs/paper/C09.md Theorem 3; Weyl equidist… | POTENTIALLY NOVEL | EXP-C09-04 |
| CLM-C09-06 | Factorisation lengths are bounded by the conjugate coordinate | written proof (proofs/paper/C09.md Theorem 4); 0 violations… | NOT ASSESSED | EXP-C09-04 |
| CLM-C09-07 | The norm N(n) = n*^2 + n n* - n^2 is multiplicative for the circle product | written proof (proofs/paper/C09.md Theorem 1); multiplicati… | NOT ASSESSED | EXP-C09-03 |
| CLM-C09-08 | Factorisation statistics of the circle semigroup up to 2e5 | computer-assisted exhaustive enumeration (EXP-C09-01, EXP-C… | NOT ASSESSED | EXP-C09-01, EXP-C09-02 |
| CLM-C10-01 | Average cost of counting in classical representations (b/(b-1), e-1, 1) | written proof (proofs/paper/C10.md Theorem 1); confirmed to… | REDISCOVERY | EXP-C10-01 |
| CLM-C10-02 | Zeckendorf counting: T_m = 2 G_m - ceil(m/2) - 2, average cost 2 | written proof (proofs/paper/C10.md Theorem 2); recurrence e… | REDISCOVERY | EXP-C10-02, EXP-C10-04 |
| CLM-C10-04 | Exchange systems fire 1/(m - sum b) times per increment on average | written proof (proofs/paper/C10.md Theorem 3) from the abel… | NOT ASSESSED | EXP-C10-03 |
| CLM-C10-05 | Single-offset exchange rules cost exactly firings + 1 per increment (average 1 + 1/(m - q… | written proof (proofs/paper/C10.md Theorem 4); deviation <=… | NOT ASSESSED | EXP-C10-03 |

## 2. Unproven conjectures (CONJECTURE and COMPUTATIONALLY SUPPORTED)

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C04-16 | Open: are the rewriting games of aa -> ab (Officers), aaa -> b (0.007) and aaa -> ab (0.0… | CONJECTURE | REDISCOVERY | EXP-C04-08, EXP-C04-09 |
| CLM-C09-05 | The density of circle irreducibles is exactly 1/phi^2 | CONJECTURE | NOT ASSESSED | EXP-C09-04, EXP-C09-01 |
| CLM-C01-08 | Common-border conjecture: one-relation class counts depend only on common borders | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-05, EXP-C01-06, EXP-C01-07 |
| CLM-C01-10 | Common-border formula with exactly one common border (derivation sketch from Gray-Steinbe… | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C01-06, EXP-C01-07, EXP-C01-08 |
| CLM-C01-11 | Converse of border containment: u -> v (|u| = |v|) is confluent iff Borders(u) is contain… | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C01-08 |
| CLM-C03-10 | Divisibility characterization of termination for 0^p 1^q -> 1^r 0^s (H-C03-4) | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C03-02, EXP-C03-03, EXP-C03-04 |
| CLM-C03-11 | Loop lengths in the base family grow like k^q | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C03-04 |
| CLM-C04-03 | The rules aab -> ababa and aab -> babaa (and their six symmetric images) terminate | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C04-02 |
| CLM-C04-12 | Complexity classes and closed forms of the 162 terminating rules with |l|, |r| <= 3 | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C04-03 |
| CLM-C08-02 | Circle products over non-Pisot base sequences are never associative | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C08-02 |
| CLM-C08-03 | Pisot base sequences give associative circle products for all sufficiently large shifts | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C08-02, EXP-C08-03 |
| CLM-C08-04 | Non-monotone associative-shift sets require a negative conjugate root | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C08-04, EXP-C08-03 |
| CLM-C08-05 | Measured associativity thresholds for 45 base sequences | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C08-02, EXP-C08-03 |
| CLM-C10-06 | Multi-offset exchange rules have rule-specific average counting costs | COMPUTATIONALLY SUPPORTED | NOT ASSESSED | EXP-C10-03 |
| CLM-C10-07 | Skew binary counting has worst-case cost 2 and average 3/2 | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C10-01 |

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
| CLM-C08-04 | Non-monotone associative-shift sets require a negative conjugate root | COMPUTATIONALLY SUPPORTED | POTENTIALLY NOVEL | EXP-C08-04, EXP-C08-03 |
| CLM-C09-03 | Window obstruction: a fixed proportion 1/phi^2 of all integers are circle-irreducible | PROVEN | POTENTIALLY NOVEL | EXP-C09-04 |

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
| CLM-C03-10 | Divisibility characterization of termination for 0^p 1^q -> 1^r 0^s (H-C03-4) | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C03-02, EXP-C03-03, EXP-C03-04 |
| CLM-C04-04 | ab -> ba: every derivation has inv(w) steps, D(n) = floor(n^2/4), P-positions = even inve… | PROVEN | REDISCOVERY | EXP-C04-03, EXP-C04-07 |
| CLM-C04-05 | One-rule systems with an unbordered left-hand side have random descent (Lean-verified) | PROVEN | REDISCOVERY | EXP-C04-05 |
| CLM-C04-08 | Rewriting games of random-descent rules are parity games (Grundy value = D(w) mod 2) | PROVEN | REDISCOVERY | EXP-C04-07 |
| CLM-C04-13 | Rewriting games with lhs a^k are take-and-break games: aa -> b is Dawson's Kayles, aa -> … | PROVEN | REDISCOVERY | EXP-C04-07, EXP-C04-08 |
| CLM-C04-15 | The rewriting game of aa -> b on a^n has Grundy values periodic with period 34 from n = 53 | PROVEN | REDISCOVERY | EXP-C04-08 |
| CLM-C04-16 | Open: are the rewriting games of aa -> ab (Officers), aaa -> b (0.007) and aaa -> ab (0.0… | CONJECTURE | REDISCOVERY | EXP-C04-08, EXP-C04-09 |
| CLM-C08-01 | Every shifted Knuth product a o_t b = sum F(k+l+t) over Zeckendorf indices is associative… | PROVEN | REDISCOVERY | EXP-C08-01, EXP-C08-03, EXP-C08-05 |
| CLM-C08-03 | Pisot base sequences give associative circle products for all sufficiently large shifts | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C08-02, EXP-C08-03 |
| CLM-C09-01 | Knuth's circle semigroup embeds in Z[phi]; Fibonacci numbers are its units-images | PROVEN | REDISCOVERY | EXP-C09-03 |
| CLM-C10-01 | Average cost of counting in classical representations (b/(b-1), e-1, 1) | PROVEN | REDISCOVERY | EXP-C10-01 |
| CLM-C10-02 | Zeckendorf counting: T_m = 2 G_m - ceil(m/2) - 2, average cost 2 | PROVEN | REDISCOVERY | EXP-C10-02, EXP-C10-04 |
| CLM-C10-07 | Skew binary counting has worst-case cost 2 and average 3/2 | COMPUTATIONALLY SUPPORTED | REDISCOVERY | EXP-C10-01 |

## 5. Practical algorithmic results

_None yet._

## 6. Refuted hypotheses

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C01-05 | H-C01-4: a single rearranging relation generates counting equivalence on long words (refu… | REFUTED | REDISCOVERY | EXP-C01-04 |
| CLM-C02-06 | H-C02-4: every terminating carry rule gives unique stable representations (refuted) | REFUTED | REDISCOVERY | EXP-C02-04 |
| CLM-C03-07 | H-C03-1: terminates iff some letter count never grows (refuted) | REFUTED | NOT ASSESSED | EXP-C03-01, EXP-C03-02 |
| CLM-C03-08 | H-C03-2: terminates iff r < 2q or s < 2p (refuted) | REFUTED | NOT ASSESSED | EXP-C03-01, EXP-C03-02 |
| CLM-C04-02 | H-C04-0: a rule with |l| <= 3 terminates iff l is not a factor of r (refuted) | REFUTED | NOT ASSESSED | EXP-C04-02 |
| CLM-C04-07 | H-C04-1: random descent iff the left-hand side is unbordered (refuted) | REFUTED | NOT ASSESSED | EXP-C04-05 |
| CLM-C04-11 | H-C04-G (second part): every terminating rule has a rational complexity generating functi… | REFUTED | NOT ASSESSED | EXP-C04-03, EXP-C04-04 |
| CLM-C04-14 | H-C04-6: Grundy values of rewriting games never exceed 3 (refuted) | REFUTED | NOT ASSESSED | EXP-C04-08 |
| CLM-C08-06 | H-C08-1: Knuth's associative circle product is an isolated case (refuted) | REFUTED | NOT ASSESSED | EXP-C08-01, EXP-C08-02 |
| CLM-C09-02 | H-C09-2: factorisation into circle irreducibles is unique (refuted) | REFUTED | NOT ASSESSED | EXP-C09-02 |
| CLM-C09-04 | H-C09-1: circle irreducibles have density 0 like primes (refuted) | REFUTED | NOT ASSESSED | EXP-C09-01, EXP-C09-04 |
| CLM-C10-03 | H-C10-0: Zeckendorf counting is cheaper than binary counting (refuted) | REFUTED | NOT ASSESSED | EXP-C10-01, EXP-C10-02 |

## 7. Inconclusive

| Claim | Title | Verification | Novelty | Evidence |
|---|---|---|---|---|
| CLM-C03-09 | H-C03-3: non-terminating iff both counts grow and (r >= 2q or s >= 2p) (inconclusive, evi… | INCONCLUSIVE | NOT ASSESSED | EXP-C03-02, EXP-C03-03 |

