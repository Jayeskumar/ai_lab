# The longest Zeckendorf game {#ch-zeckendorf-game}

*Volume 5 — Mathematical transformations and relationships. Research cycle C19.*

## Motivation

In Chapter 3 the Fibonacci exchanges turned a heap of $n$ tokens into the
Zeckendorf representation of $n$, and every order of exchanges arrived there.
The *number* of exchanges, however, depends on the order. The shortest
derivation is easy: $n - Z(n)$ steps, $Z(n)$ the number of Zeckendorf terms.
The longest was left open in Chapter 3. As a two-player game this system is the
*Zeckendorf game* of Baird-Smith, Epstein, Flynt and Miller, and its longest
game has a literature of its own. This chapter reports what the laboratory
added to it: an exact identity for the length of every game, the shape of a
longest game, a closed form for Fibonacci inputs, and a conjectured recursion
for all inputs, a question that a 2025 paper calls open.

## Definitions

We write $F_1 = 1$, $F_2 = 2$, $F_{i+1} = F_i + F_{i-1}$. The game starts
with $n$ copies of $F_1$ and allows

* combines: $F_1 + F_1 \to F_2$ (C$_1$) and $F_{i-1} + F_i \to F_{i+1}$
  (C$_i$, $i \ge 2$);
* splits: $2F_2 \to F_1 + F_3$ (S$_2$) and $2F_i \to F_{i-2} + F_{i+1}$
  (S$_i$, $i \ge 3$).

Every game ends at the Zeckendorf representation $n = \sum \delta_i F_i$. Let
$L(n)$ be the length of a longest game, $MC_i$ the number of moves C$_i$ in a
game, and
$$B(n) = \sum_i \bigl(F_{i+2} - i - 2\bigr)\,\delta_i ,$$
the upper bound of Cusenza et al. (2022), who also proved that a longest game
is obtained by splitting whenever possible and otherwise combining the
smallest consecutive pair. The *deficit* is $D(n) = B(n) - L(n)$. The *lazy*
representation of $n$ writes $n$ as a sum of distinct $F_i$ with no two
consecutive indices missing below the largest one.

## What exhaustive search shows

**Theorem 16.1** *[PROVEN — computer-assisted; REDISCOVERY]*. For every
$n \le 150$ an exhaustive search over all positions, assuming no strategy,
gives $L(n) = 0, 0, 1, 2, 3, 5, 6, 8, 10, 11, 13, 15, 17, 20, \ldots$, and the
split-first strategy attains it. The bound $B(n)$ is attained exactly at
$n = 1, 2, 4, 7, 12, 20, 33, 54, 88, 143$, the numbers $F_k - 1$ (EXP-C19-01).

**Proposition 16.2** *[PROVEN]*. The positions reachable from $n$ copies of
$F_1$ are exactly the multisets of Fibonacci numbers with sum $n$. (Undo
combines until only copies of $F_1$ remain, then read the steps backwards.)
Their number is the number of partitions of $n$ into Fibonacci parts (OEIS
A003107), up to 910,775 positions for $n = 150$.

## Every game has the same "budget"

**Theorem 16.3** *[PROVEN — written; arithmetic core in Lean:
`length_identity`; REDISCOVERY (implicit in Cusenza et al.)]*. Every game $G$
on $n$ satisfies
$$|G| \;=\; B(n) \;-\; \sum_{i \ge 2} (i - 1)\, MC_i(G).$$

*Proof idea.* Give a token $F_i$ the weight $a_i = F_{i+2} - i - 2$. The total
weight starts at 0 (since $a_1 = 0$) and ends at $B(n)$, and each split or
C$_1$ raises it by exactly 1 while C$_i$ raises it by $i$; for instance a split
changes it by $a_{i-2} + a_{i+1} - 2a_i = 1$ by the Fibonacci recurrence. ∎

So a longest game is one that uses the fewest, and the lowest, consecutive
combines, and $D(n) = \min_G \sum (i-1) MC_i(G)$. The theorem was checked on
1500 random games as well as on the longest ones (EXP-C19-02).

## The shape of a longest game

The split-first game splits until no level holds two tokens, and only then
starts combining. Where does the first phase end?

**Theorem 16.4** (the lazy phase) *[PROVEN — written; POTENTIALLY NOVEL
(small)]*. Split moves, applied in any order until none is possible, always
take $n$ copies of $F_1$ to the **lazy** representation of $n$, after the same
number of moves.

*Proof idea.* Splits form an abelian chip-firing system, so the end point does
not depend on the order, and adding one token and re-stabilising is the same as
stabilising from scratch. Adding one $F_1$ to a lazy representation whose
lowest gap is at level $p$ creates a carry: the block $2, 1, 1, \ldots, 1$
below $p$ turns into the alternating block $\ldots, 1, 0, 1$ topped by a token
at level $p$, which is again lazy. ∎

**Corollary 16.5** *[PROVEN — a short new proof of Cusenza et al.'s Theorem
1.4]*. A game can be played with split moves alone iff $n = F_k - 1$: such a
game ends at the lazy representation, and the lazy and Zeckendorf
representations coincide exactly for alternating digit strings.

## Fibonacci inputs

For $n = F_k$ the lazy representation is the alternating string
$\ldots 1010$ with the two lowest tokens adjacent. The second phase is a
single carry running upwards: C$_2$, C$_4$, C$_6$, … (or C$_3$, C$_5$, …),
each combine landing next to the following token.

**Theorem 16.6** *[PROVEN — written, using the strategy theorem of Cusenza et
al.; weight sums in Lean; POTENTIALLY NOVEL]*.
$$L(F_k) \;=\; F_{k+2} - k - 2 - \left\lfloor \frac{(k-1)^2}{4} \right\rfloor :
\quad 0,\ 1,\ 2,\ 5,\ 10,\ 20,\ 37,\ 67,\ 117,\ 201,\ \ldots$$
The deficit $D(F_k)$ is the quarter-square $\lfloor (k-1)^2/4 \rfloor$, the
total weight $1 + 3 + 5 + \cdots$ or $2 + 4 + 6 + \cdots$ of the carry. ∎
Checked for every $k \le 34$ (EXP-C19-03). This sequence is not in the OEIS.

## Four failed guesses

Before the recursion below was found, four simpler descriptions of $D(n)$ were
proposed and refuted (EXP-C19-02, EXP-C19-03):

* *H-C19-1 [REFUTED]*: $D$ is a sum over Zeckendorf terms with corrections for
  consecutive pairs only. The two-term values are given exactly by such a rule
  (Conjecture 16.8), but already $n = 12 = F_5 + F_3 + F_1$ has $D = 0$
  where the rule predicts 1.
* *H-C19-2 [REFUTED]*: the effect of the largest term depends only on the two
  largest terms.
* *H-C19-3 [REFUTED]*: $D$ is additive over the runs of the lazy
  representation — the corresponding linear system is inconsistent already for
  $n < 160$ (rank 46 against 47).
* *H-C19-4 [REFUTED]*: a longest game on $n + 1$ is a longest game on $n$
  followed by the longest continuation after adding one token ($n = 3$ is a
  counterexample). Longest games avoid the Zeckendorf form until the very end.

## A recursion for all n

The failures pointed to carries that travel through alternating blocks.
The right bookkeeping turned out to be the *saving* that a smaller part $m$
grants to a top term $F_{j+1}$:
$$\rho = D(F_{j+1}) + D(m) - D(F_{j+1} + m).$$
Among 17,711 cases it depends only on $m$ and on the parity of $j$.

**Conjecture 16.7** *[COMPUTATIONALLY SUPPORTED; POTENTIALLY NOVEL]*. Let
$h(k) = \lfloor k^2/4 \rfloor$. For $p \in \{0, 1\}$ define $\rho_p(0) = 0$ and,
for $m = F_{i+1} + t$ with Zeckendorf top index $i + 1$,
$$\rho_p(m) = r_p(i) + [\,i \equiv p\,]\cdot \max\bigl(0,\ \rho_p(t) - h(i-2)\bigr),$$
with $r_p(0) = 1$, $r_p(i) = h(i) + 2$ if $i \equiv p \pmod 2$ ($i \ge 1$), and
$r_p(i) = h(i+1) + 1$ otherwise. Then
$$D(F_{j+1} + m) = h(j) + D(m) - \rho_{j \bmod 2}(m), \qquad L(n) = B(n) - D(n).$$

The recursion was read off all $n < 30000$. It was then tested on 6,272
numbers it had not seen, including every $n$ in $[30000, 36000)$ and random
$n$ up to $2 \cdot 10^7$, without a single mismatch (EXP-C19-04). It is not
proved.

**Conjecture 16.8** *[COMPUTATIONALLY SUPPORTED]* (two terms). For index
gaps $\ge 2$, $D(F_{j+1} + F_{i+1}) = h(j) + h(i) - R(j, i)$ with
$R(j, i) = \lfloor (i+1)^2/4 \rfloor + 1$ when $j - i$ is odd,
$\lfloor i^2/4 \rfloor + 2$ when $j - i$ is even ($i \ge 1$), and $R(j, 0) = 1$
(all 276 pairs with $j \le 24$).

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C19-01 | exact longest games | $n \le 150$; strategy optimal; equality iff $F_k - 1$ |
| EXP-C19-02 | identity; lazy phase; insertion | 0 violations; lazy for all $n < 5000$; H-C19-4 refuted |
| EXP-C19-03 | structure of $D$ | Fibonacci law to $k = 34$; three additive models refuted |
| EXP-C19-04 | recursion out of sample | 6,272 numbers, 0 mismatches |

## Comparison with existing mathematics

The game and its shortest length are due to Baird-Smith, Epstein, Flynt and
Miller (2020). Li et al. (2020) bounded the longest game by
$3n - 3Z(n) - IZ(n) + 1$. Cusenza et al. (*Fibonacci Quarterly* 60, 2022)
proved that the split-first strategy is longest, that $L(n) \le B(n)$, and that
equality holds iff $n = F_k - 1$. Cheigh et al. (2025) proved that every length
between the shortest and longest game occurs, and stated that a convenient
closed form for non-Fibonacci inputs is open. Theorem 16.3 is implicit in
Cusenza et al.'s argument, and Corollary 16.5 reproves their Theorem 1.4. We
found no earlier statement of the lazy phase, of the formula for $L(F_k)$, or
of a recursion for general $n$. The sequences $L(n)$ and $L(F_k)$ are not in
the OEIS.

## Applications and limitations

If Conjecture 16.7 holds, $L(n)$ can be computed with $O(\log^2 n)$ arithmetic
operations instead of playing $\approx 2.618\,n$ moves. At $n = 10^7$ the
recursion takes $9 \cdot 10^{-5}$ s against 8.3 s for playing the game. That
speed-up rests on an unproved recursion. All data beyond $n = 150$ rely on the
published optimality of the split-first strategy.

## Open questions

1. Prove Conjecture 16.7, for instance by following the carries of the second
   phase from the lazy representation.
2. Prove that $D(n) \le \lfloor j^2/4 \rfloor$, where $j$ is the level of the
   largest term, and that $L$ is strictly increasing (both hold for
   $n < 30000$).
3. Do the lazy phase and the Fibonacci-input formula extend to the generalised
   Zeckendorf games built on other linear recurrences?
