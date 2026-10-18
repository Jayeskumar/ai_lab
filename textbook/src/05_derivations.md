# How long does rewriting take? {#ch-derivations}

*Volume 1 — Foundations: transformation systems. Research cycle C04.*

## Motivation

Chapter 4 asked whether a transformation system stops. Once it does, the
*length* of a derivation is itself a quantity produced by the system, without
any arithmetic having been put in. This chapter asks three questions about the
smallest systems — a single rule $l \to r$ over the letters $a, b$:

1. how long can derivations from words of length $n$ be?
2. when does the *order* in which rewrites are applied not matter?
3. what games does a rule define if two players take turns rewriting?

## Definitions

A step rewrites one occurrence: $x\,l\,y \to x\,r\,y$. A *normal form* contains
no occurrence of $l$. $D(w)$ is the maximal number of steps from $w$ to a
normal form, and the *derivational complexity* is
$D(n) = \max_{|w| = n} D(w)$. A rule has **random descent** (RD; van Oostrom)
if from every word all maximal derivations have the same length *and* end in
the same normal form. A *border* of $l$ is a nonempty proper prefix of $l$
that is also a suffix. In the *rewriting game* two players alternately make
one step; a player who cannot move loses (normal play), and positions get
Sprague–Grundy values.

## Which rules terminate?

**Theorem 5.1** *[PROVEN — computer-assisted]*. Of the 196 rules with
$1 \le |l| \le 3$, $0 \le |r| \le 3$, exactly the 34 in which $l$ is a factor
of $r$ are non-terminating. Each of the other 162 has a checked certificate:
length decrease (70 rules), lexicographic monotonicity of length-preserving
steps (70), a linear interpretation over $\mathbb{N}$ (20; e.g. $ab \to bba$
with $a \mapsto 3x$, $b \mapsto x + 1$), or a factor count that drops at every
step (2).

*The bold generalisation fails.* Hypothesis H-C04-0 — "a rule with
$|l| \le 3$ terminates iff $l$ is not a factor of $r$" — is **refuted** as soon
as $|r| = 4$ is allowed: $ab \to bbaa$ does not terminate although $ab$ does
not occur in $bbaa$:
$$aab \to a\,bbaa = abbaa \to bbaa\,baa = bb\cdot aab\cdot aa .$$
The extended census ($|r| \le 5$, 868 rules) has 18 such rules; two symmetry
classes ($aab \to ababa$, $aab \to babaa$) were left undecided here
(EXP-C04-02) and are settled — both terminate — in Chapter 21.

## One rule, one invariant

The following elementary fact organises the rest of the chapter.

**Theorem 5.2** (constant-step potential) *[PROVEN — written; consequences in
Lean: `steps_length_unique`, `length_changing_unique`]*. For every rule
$l \to r$ with $l \ne r$ there are $\Phi : \Sigma^* \to \mathbb{Z}$ and
$\delta \ne 0$ such that every step $u \to v$ satisfies
$\Phi(v) = \Phi(u) + \delta$. Consequently all derivations between two given
words have the same length, and a terminating one-rule system is confluent
if and only if it has random descent.

*Proof idea.* If $|l| \ne |r|$ take $\Phi(w) = |w|$. Otherwise pick a letter
$c$ whose position sets $P$ in $l$ and $Q$ in $r$ differ; the power sums
$\sum_{j \in P} j^m$ and $\sum_{j \in Q} j^m$ differ for some
$m < |l|$ (Vandermonde), and for the least such $K$ the potential
$\Phi(w) = \sum_{i : w_i = c} i^K$ changes by the same amount at every offset
by the binomial theorem. ∎ Checked on 470,927 steps of 5,365 rules
(EXP-C04-06), where $K \le 2$ always sufficed.

**Theorem 5.3** (local criterion) *[PROVEN — Lean: `random_descent`;
REDISCOVERY: van Oostrom 2007]*. If every local peak $b \leftarrow a \to c$
can be joined by two derivations of equal length, the system has random
descent (from any word that has a normal form).

**Theorem 5.4** *[PROVEN — Lean: `unbordered_diamond`,
`unbordered_random_descent`; REDISCOVERY]*. If $l$ is unbordered, two
different one-step reducts of a word have a common one-step reduct; hence
$l \to r$ has random descent. (Two overlapping occurrences of $l$ would
exhibit a border.)

*A refuted converse.* Hypothesis H-C04-1 claimed RD *iff* $l$ is unbordered.
The rule $aa \to a$ has a bordered left side but random descent: every step
shortens one run of $a$'s, so every derivation from $w$ has exactly
$\sum_{\text{runs}} (\text{length} - 1)$ steps and ends in the same word.
Eighteen bordered rules with $|l|, |r| \le 3$ have RD (EXP-C04-05).

## Derivational complexity

**Theorem 5.5** *[PROVEN — Lean: `inv_step`, `normal_iff_inv_zero`,
`derivation_length_eq_inv`, `p_positions`; REDISCOVERY]*. Under
$ab \to ba$ each step lowers the number of inversions by one; every complete
derivation from $w$ has exactly $\mathrm{inv}(w)$ steps, so
$D(n) = \lfloor n^2/4 \rfloor$; and in the rewriting game the losing
positions for the player to move are the words with an even number of
inversions.

This is the extremal case of Métivier's conjecture, proved by Bertrand
(1994): length-preserving one-rule systems never need more than $n^2/4$ steps.

**Theorem 5.6** *[PROVEN — written]*. For $ab \to bba$ and $ab \to baa$,
$D(n) = 2^{n-1} - 1$. (Scanning $w$ from the right, an $a$ that meets $B$
letters $b$ crosses them in $B$ steps and leaves $2B$ behind it.)

**Observation 5.7** *[COMPUTATIONALLY SUPPORTED]*. The 162 terminating rules
fall into 55 symmetry classes with complexity linear (144 rules), quadratic
(14: $\lfloor n^2/4 \rfloor$, $\lfloor n(n-1)/6 \rfloor$, $\lfloor n^2/8 \rfloor$)
or exponential (4: $2^{n-1} - 1$); 54 classes have a simple closed form on all
computed terms (EXP-C04-03).

One class does not: the rule $aab \to ba$ refutes the hypothesis (H-C04-G)
that every complexity sequence satisfies a linear recurrence.

**Theorem 5.8** *[PROVEN — written; POTENTIALLY NOVEL (small)]*. For
$aab \to ba$,
$$D(n) = n - 1 - \kappa(n), \qquad \kappa(n) = \min\{k \ge 0 : 2^k + k \ge n\},$$
so $D(n) = n - \log_2 n + O(1)$; $D$ stalls exactly at $n = 2^k + k + 1$
($4, 7, 12, 21, 38, \ldots$), and $\sum D(n) x^n$ is not a rational function.

*Proof idea.* Write $w = a^{x_0} b\, a^{x_1} b \cdots b\, a^{x_m}$. Rewriting
$aab$ moves two $a$'s before the $(k{+}1)$-th $b$ to one $a$ after it: this is
the exchange $2[k] \to [k+1]$ of Chapter 3 — a *binary counter* — with the
last level inert. The value $\sum_k x_k 2^k$ is invariant, each step removes
one token, and $aab$ is unbordered, so every derivation has the same length,
determined by the binary expansion of the value. Optimising over $w$ gives
$n - D(n) = \min_m (m + \lceil (n-m)/2^m \rceil) = 1 + \kappa(n)$. Since the
stall positions have unbounded gaps, no linear recurrence can produce them. ∎
(Checked for all words of length $\le 21$ and as an identity to $n = 20000$.)

The same numbers turned up somewhere unexpected. OEIS A247983 counts how many
terms of the series $\log 2 = \sum_{h \ge 1} 1/(h\,2^h)$ are needed for $n$
bits of accuracy; the entry gives no formula.

**Theorem 5.9** *[PROVEN — written, Skeptic-reviewed; POTENTIALLY NOVEL
(small)]*. For every $n \ge 1$, A247983$(n)$
$= n - \max\{j \ge 0 : 2^j + j \le n + 1\} = D(n+2)$ for $aab \to ba$.
(The Skeptic noted that the identity fails at $n = 0$, outside the OEIS
offset.)

*Proof idea.* The tail $\log 2 - \sum_{h \le k} 1/(h 2^h)$ lies between
$2^{-k}/(k+2)$ (Jensen) and $2^{-k}/(k+1)$, which pins down the first $k$
with tail below $2^{-n}$. ∎ (Checked with exact arithmetic for $n \le 1500$,
EXP-C04-10.) The coincidence has a simple reason: both quantities measure how
far the counter $2^k + k$ has advanced.

## Games from rewriting

**Theorem 5.10** *[PROVEN — written; REDISCOVERY]*. If a rule has random
descent, the Grundy value of its game at $w$ is $D(w) \bmod 2$: such games
are decided by parity alone.

**Theorem 5.11** *[PROVEN — written; REDISCOVERY: octal games as rows of
pins]*. For a terminating rule $a^k \to u$ the game on $w$ is the disjoint
sum of games on the maximal runs of $a$'s, and each run game is a
take-and-break game. In particular

| rule | game |
|---|---|
| $aa \to b$ | Dawson's Kayles (0.07) — period 34 from $n = 53$ |
| $aa \to ab$ | Officers (0.6) — periodicity **unknown** |
| $aaa \to b$ | Treblecross (0.007) — periodicity unknown |
| $aaa \to ab$ | 0.06 — no period $\le 300$ up to $n = 3000$ |
| $aaa \to aba$ | 0.4 — period 34 |

So the two-letter, one-rule system $aa \to ab$ already encodes a famous open
problem: whether the Grundy values of Officers are ultimately periodic (they
have been computed to beyond $10^{14}$ without a period appearing).

*A bold hypothesis refuted.* H-C04-6 guessed that Grundy values of these
games never exceed 3 (true on all words of length $\le 10$). The single word
$a^{14}$ under $aa \to b$ has Grundy value 4.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C04-01 | termination, $\lvert l\rvert,\lvert r\rvert \le 3$ | 162 terminating, 34 looping, 0 unknown |
| EXP-C04-02 | termination, $\lvert r\rvert \le 5$ | 472 / 388 / 8 undecided; $ab \to bbaa$ loops |
| EXP-C04-03 | complexity census | 144 linear, 14 quadratic, 4 exponential |
| EXP-C04-04 | $aab \to ba$ | formula confirmed to $n = 20000$ |
| EXP-C04-05 | random descent vs. borders | 84 unbordered all RD; 18 bordered RD |
| EXP-C04-06 | constant-step potential | 5,365 rules, 470,927 steps, 0 violations |
| EXP-C04-07 | game parity and run decomposition | 0 violations |
| EXP-C04-08 | octal games | agree with octal recursions to $n = 3000$ |
| EXP-C04-09 | OEIS | 0.06 Grundy values not in the OEIS |
| EXP-C04-10 | A247983 identity | 0 mismatches, $n \le 1500$ |

## Comparison with existing mathematics

Random descent and its local criterion are due to van Oostrom (RTA 2007) and
have been formalised in Isabelle; our Lean development is an independent
re-formalisation. Quadratic and exponential one-rule complexities are standard
examples (Kobayashi; Métivier's conjecture, settled by Bertrand). The octal
games are classical (Guy–Smith 1956; *Winning Ways*). A brief search found no
prior statement of Theorem 5.2 or of the analysis of $aab \to ba$; Theorem
5.2 is elementary enough to be folklore and is labelled accordingly in the
database ("not assessed").

## Applications and limitations

For one-rule systems the cost of normalisation is predictable without
simulation (Theorem 5.2): any one derivation tells the length of all of them.
Closed forms such as $\lfloor n^2/4 \rfloor$, $2^{n-1} - 1$ and
$n - \log_2 n + O(1)$ are exact worst-case costs of bubble-sort-like swaps,
doubling processes and binary-counter carries. These are observations; no
practical improvement over existing tools is claimed.

## Open questions

1. ~~Do $aab \to ababa$ and $aab \to babaa$ terminate?~~ Yes — see
   Chapter 21, which also gives their exact (exponential) complexities.
2. For $\lvert l\rvert = 4$, do complexities other than polynomial,
   exponential and $n - \Theta(\log n)$ appear?
3. Is the Grundy sequence of $aaa \to ab$ (octal game 0.06) ultimately
   periodic? (For $aa \to ab$ this is the open Officers problem.)
