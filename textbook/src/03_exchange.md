# Numeration from exchange {#ch-exchange}

*Volume 1 — Foundations. Research cycle C02.*

## Motivation

Chapter 2 showed that a multiset of tokens *is* a number. Positional notation
is usually introduced by fiat ("the digit in the second place is worth two").
Here we ask whether place value can be *discovered*: put tokens on levels
$0, 1, 2, \ldots$ and allow only local exchanges.

## Definitions

A *configuration* is a finitely supported vector $c = (c_0, c_1, \ldots)$ of
token counts. A **carry rule** $m[k] \to \sum_{j=1}^{J} b_j [k+j]$ removes $m$
tokens from a level holding at least $m$ and adds $b_j$ tokens $j$ levels
higher. A configuration is *stable* if every $c_k < m$. The *carry
polynomial* is $P(x) = \sum_j b_j x^j - m$ and the *emergent base* $r$ is its
unique positive root. Nothing about value is assumed — but solving
$m\,w_k = \sum_j b_j w_{k+j}$ for exchange-invariant weights forces
$w_k = r^k$: **value is the invariant of the exchange rule**,
$V(c) = \sum_k c_k r^k$.

## Examples

* $2[k] \to [k+1]$: from $n$ tokens at level 0 one obtains the binary digits
  of $n$. Base $b$ arises from $b[k] \to [k+1]$.
* $3[k] \to 2[k+1]$: base $3/2$ (the rational base of Akiyama, Frougny and
  Sakarovitch): $1, 2, 20, 21, 22, 210, \ldots$ (OEIS A024629).
* $3[k] \to [k+1] + [k+2]$: base $r = (\sqrt{13}-1)/2 \approx 1.3028$, digits
  $0..2$: $1, 2, 110, 111, 112, 220, 221, 222, 12100, \ldots$ (not in the OEIS).
* Fibonacci exchanges $[k]+[k+1] \to [k+2]$, $2[k] \to [k+1] + [k-2]$ (with
  boundary versions) produce Zeckendorf representations.

## Results

**Theorem 3.1** (abelian property) *[PROVEN — written; REDISCOVERY: chip-firing]*.
For a carry rule, firings at different levels commute. Hence from any
configuration either all maximal derivations are infinite, or all are finite,
end at the same stable configuration, have the same length, and fire every
level the same number of times.

**Theorem 3.2** (integer bases) *[PROVEN — written]*. Under $b[k] \to [k+1]$
every derivation from $n$ tokens ends at the base-$b$ expansion after exactly
$(n - s_b(n))/(b-1)$ exchanges ($s_b$ = digit sum).

**Theorem 3.3** (termination dichotomy) *[PROVEN — written; REDISCOVERY
(folklore)]*. If
$\sum b_j < m$, every derivation terminates. If $\sum b_j > m$, then $r < 1$
and no derivation from $n > (m-1)/(1-r)$ tokens terminates, because every
stable configuration has value at most $(m-1)/(1-r)$.

The borderline $\sum b_j = m$ is the interesting case: the rule
$2[k] \to [k+1] + [k+2]$ started from 6 tokens leaves a pattern $(2, 1)$ that
*glides* upward forever. In the upward sweep the "window" of the next $J$
levels evolves by a monotone map whose fixed point is the tail-sum vector
$T = (\sum_{j\ge 1} b_j, \sum_{j \ge 2} b_j, \ldots)$: every level fires
exactly once.

**Conjecture 3.4** *[COMPUTATIONALLY SUPPORTED; POTENTIALLY NOVEL — Propp
(2017) proposed this rule family but gave no results]*. Every carry rule with
$\sum b_j = m$ fails to terminate from some unary start. Verified for all 28
such rules with $m \le 4$, $J \le 3$, $b_j \le 3$; each produced exactly the
glider $T$ (or its sparse analogue). Together with Theorem 3.3 this gives a
complete termination classification of the 189 small rules
**[PROVEN — computer-assisted certificates]**.

**Theorem 3.5** (radix order) *[PROVEN — written; REDISCOVERY in substance:
Akiyama–Frougny–Sakarovitch 2008, Prop. 11]*. For terminating carry
rules, $n < n'$ implies that the representation of $n$ precedes that of $n'$
in radix order. (The highest level changed when one token is added cannot
have fired, so it only gained tokens.)

**Theorem 3.6** (uniqueness) *[PROVEN — Lean core: `digits_unique`;
REDISCOVERY in substance: Akiyama–Frougny–Sakarovitch 2008, Lemma 5]*.
Let $g$ be the gcd of the levels reachable in one exchange and $\tilde P$ the
carry polynomial in the variable $y = x^g$. If $\tilde P$ is primitive and
irreducible over $\mathbb{Q}$, distinct stable configurations on the reachable
levels have distinct values; in particular each integer has exactly one
representation. If $\tilde P$ is not primitive, uniqueness fails.

*Proof idea.* A difference $\Delta$ of two digit strings with equal value
vanishes at the root; an irreducible $\tilde P$ must then divide $\Delta$ over
$\mathbb{Q}$ (a Bézout identity evaluated at the root rules out coprimality),
hence over $\mathbb{Z}$ by Gauss's lemma; but a nonzero multiple of $\tilde P$
has a trailing coefficient divisible by $m$, while digit differences are
smaller than $m$. ∎

*A refuted hypothesis.* We first conjectured uniqueness for *every*
terminating rule. The rule $4[k] \to 2[k+1]$ (base 2 with digits $0..3$)
refutes it: "2" and "10" both have value 2. All failures among the 31
terminating small rules have a non-primitive reduced carry polynomial.

## The Fibonacci exchanges are the Zeckendorf game

**Theorem 3.7** *[PROVEN — written; REDISCOVERY]*. The Fibonacci exchanges
terminate from every configuration at the Zeckendorf representation of its
value, and the shortest derivation from $n$ tokens has $n - z(n)$ steps
($z(n)$ = number of Zeckendorf terms). Termination uses the potential
(token count, $\sum_k c_k g(k)$) with $g(0) = -\tfrac12$, $g(k) = k$; the
shortest derivation adds tokens one at a time, which needs only merges.

This system is exactly the *Zeckendorf game* of Baird-Smith, Epstein, Flint and
Miller (2018), who proved termination and the shortest game $n - Z(n)$, and
whose Figure 4 already lists the *longest* games for $n \le 49$ — identical to
our exhaustive values for $n \le 40$ ($0, 1, 2, 3, 5, 6, 8, 10, \ldots, 78$).
Cusenza et al. (2022) proved the greedy strategy optimal; a closed form is
known only for $n = F_k - 1$. The sequence is not yet in the OEIS.

## Limitations and open questions

1. Prove Conjecture 3.4 (a "spreading" lemma for the sweep).
2. Which carry rules give *regular* languages of representations?
3. A closed form for the longest Zeckendorf game.
