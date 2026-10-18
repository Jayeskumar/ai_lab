# Magma automata and fast-forwarding {#ch-magma-automata}

*Volume 7 — Computational experiments and algorithms. Research cycle C15.*

## Motivation

A binary operation can be read as a law of motion. Put symbols in a row and
let every cell look at its right neighbour:
$$c'_i = c_i * c_{i+1}.$$
Every magma of the earlier chapters — the invented operations of Volume 2, the
Laver tables, the nimbers — becomes a one-dimensional cellular automaton. Two
questions follow. How *complicated* is the state after $t$ steps as a function of
the initial row? And can it be computed without simulating all $t$ steps
("fast-forwarding")?

## Definitions

Cell $i$ at time $t$ is $F_t(c_i, \ldots, c_{i+t})$, where $F_0(x_0) = x_0$ and
$$F_t(x_0, \ldots, x_t) = F_{t-1}(x_0, \ldots, x_{t-1}) * F_{t-1}(x_1, \ldots, x_t).$$
A cell $x_k$ is *essential* if $F_t$ depends on it. To measure complexity we
read the arguments of $F_t$ from left to right and count how many different
residual functions of the unread arguments can occur after a prefix of fixed
length; the maximum over prefix lengths is the *forward width* (the width of the
reduced ordered decision diagram). Reading from the right gives the backward
width, and the smaller of the two is the **streaming width** $\lambda(t)$ — the
memory a one-pass reader needs, up to a logarithm. The automaton is *permutive*
if all rows or all columns of the table are permutations, *surjective* if every
bi-infinite row has a preimage.

## Two letters: the elementary rules

**Theorem 17.1** *[PROVEN; REDISCOVERY]*. The 16 automata of two-element magmas
are exactly the elementary cellular automata that ignore the left neighbour —
the Wolfram rules $0, 17, 34, \ldots, 255$. All have streaming width at most 3;
XOR (rule 102) depends on $2^{\mathrm{popcount}(t)}$ cells (Gould's sequence).

## Structure makes the light cone simple

**Theorem 17.2** *[PROVEN — Lean: `ca_comm_binomial`; REDISCOVERY]*. If $*$ is
associative, $F_t(x_0, \ldots, x_t) = \prod_{j < 2^t} x_{s(j)}$ with $s(j)$ the
number of ones in the binary expansion of $j$. If it is also commutative,
$$F_t(x_0, \ldots, x_t) = \prod_{k=0}^{t} x_k^{\binom{t}{k}},$$
Pascal's triangle in the exponents, and the streaming width is at most $|S|$.

**Theorem 17.3** *[PROVEN — written; REDISCOVERY: linear cellular automata]*.
For an affine operation $x * y = \varphi(x) + \psi(y) + c$ on an abelian group
($\varphi, \psi$ commuting endomorphisms),
$F_t = \sum_k \binom{t}{k}\varphi^{t-k}\psi^k(x_k) + \text{const}$, the streaming
width is at most $|A|$, and a cyclic row at time $t$ is
$P^t r + \text{const}$ with $P = \varphi + \psi S$ ($S$ the shift), computable with
$O(\log t)$ polynomial multiplications modulo $S^L - 1$.

For commutative semigroups the exponents $\binom{t}{k}$ can be grouped by residue
mod $L$ and reduced with the index and period of each element, which gives a
second exact fast-forward (Theorem 3 of `proofs/paper/C15.md`).

## Surjectivity

**Theorem 17.4** *[PROVEN — computer-assisted; REDISCOVERY: Kari, Salo and
Törmä]*. For magmas of order at most 3 the automaton is surjective if and only
if it is permutive; there are $1, 6, 420$ surjective tables of orders $1, 2, 3$,
namely $2(n!)^n$ minus the number of Latin squares. For order 4 the rectangular
band $(b, c) * (b', c') = (b, c')$ is surjective — even reversible, an identity
on one coordinate and a shift on the other — without being permutive.

The order-3 statement is the prime-alphabet case of a 2013 theorem; our
exhaustive pair-graph computation is an independent confirmation, and the
order-4 band shows why the hypothesis "prime" cannot simply be dropped.

## A census of order 3

There are 19683 tables of order 3, 1734 up to isomorphism and mirror image.

**Observation 17.5** *[COMPUTATIONALLY SUPPORTED, $t \le 9$]*. The streaming
width is bounded for 808 classes, grows linearly for 104, roughly geometrically
for 300 (up to $\lambda(9) = 649$) and irregularly for 522. All 18 semigroup
and all 8 affine classes are bounded; 43 classes are surjective (exactly the
permutive ones), 7 are reversible, 34 are nilpotent.

*Two bold hypotheses fail.* H-C15-1 predicted that widths are either bounded or
geometric. H-C15-2 predicted that bounded width means "semigroup, affine, or a
light cone of at most two cells". In fact 685 bounded-width classes have none of
these structures — for example the reversible automaton with table
$[[0,0,2],[2,2,0],[1,1,1]]$, whose light cone uses every cell but whose width
stays 3 — and linear growth exists, as the next result proves.

## The burning fuse

Let 0 mean *burnt*, 1 *burning* and 2 *intact*, with
$0 * y = 0$; $1 * y = 1$ if $y = 2$, else $0$; $2 * y = 2$ if $y \neq 0$, and
$2 * 0 = 1$. An intact cell starts burning when its right neighbour has burnt,
and burns out one step later.

**Theorem 17.6** *[PROVEN — written; POTENTIALLY NOVEL (small)]*. Let $\tau_i$ be
the time at which cell $i$ burns out. Then $\tau_i = \tau_{i+1} + 2$ for an intact
cell, $\tau_i = 0$ for a burnt one, and $\tau_i \in \{1, \tau_{i+1}\}$ for a
burning one, according as its right neighbour is not or is intact. Consequently

1. the row at any time $t$ can be computed in $O(L)$ operations, whatever $t$;
2. the streaming width grows linearly: with $m = \lfloor t/2 \rfloor$,
   $$\left\lfloor \tfrac{m+1}{2} \right\rfloor \le \lambda(t) \le 3t + 3,$$
   and in fact $\lambda(t) = t + 2$ for all $t \le 12$.

*Proof idea.* A run of intact cells burns from the right, two steps per cell, so
the light cone has to compare $t$ with twice the length of a run — a counter,
which no bounded memory can hold. The prefixes
$2\,(12)^b\,2^{m-1-2b}$ and suffixes $2^j 0 2^{\ldots}$ produce output 2 exactly
when $j \ge b + 1$ (for even $t$), so they generate pairwise distinct residuals. ∎

The fuse refutes the "dichotomy" H-C15-1, and it also refutes H-C15-4 — the
brief's hypothesis that an automaton can be fast-forwarded exactly when its
light-cone complexity is bounded: its width is unbounded, yet the future is
computable in $O(L)$. The reverse direction is open (Conjecture CLM-C15-18).

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C15-01 | order 2 | rules $17m$; widths $\le 3$ |
| EXP-C15-02 | order-3 census | 808 / 104 / 300 / 522 width classes; surjective = permutive |
| EXP-C15-03 | exact fast-forwards | 99/99 agree with simulation |
| EXP-C15-04 | cycle detection | 1590 of 1734 rows ($L = 32$) repeat within 5000 steps |
| EXP-C15-05 | case studies | fuse $\lambda(t) = t + 2$ to $t = 12$; Laver tables; order-4 band |

## Benchmark

Direct numpy simulation is the baseline; rows of length $L = 1024$; times are
indicative (shared machine).

| method | $t = 10^2$ | $t = 10^3$ | $t = 10^4$ | $t = 10^5$ | $t = 10^9$ |
|---|---|---|---|---|---|
| affine (5 magmas) | ×3–4 | ×22–29 | ×138–215 | ×1800–2500 | 1.5–3 ms |
| fuse burn times | ×2.5 | ×27 | ×239 | ×4000 | 0.6 ms |
| commutative semigroups (3) | ×1–3 | ×0.9–2.1 | ×6–9 | ×62–100 | 21–42 ms |
| cycle detection | exact whenever the row repeats; 1590/1734 classes within 5000 steps at $L = 32$; fails for the affine quasigroups mod 3 | | | | |

*A third hypothesis fails.* H-C15-6 predicted more than ×100 for every exact
method at $t = 10^5$ and losses for small $t$. The commutative-semigroup method
stays below ×100 — its final product costs $O(L^2)$ and it is even slower than
simulation near $t = 10^3$ — while the affine and fuse methods never lose. And
H-C15-5 ("long cycles only for geometric width") fails because the affine
quasigroups mod 3 have bounded width but long cycles.

## Comparison with existing mathematics

Automata defined by a binary operation were studied algebraically by Pedersen
(1992) and by Moore with Drisko and with Pnin (1995–1997), who showed that rules
given by nilpotent or solvable groups can be predicted in logarithmic parallel
time. Linear automata and their fast-forward go back to Martin, Odlyzko and
Wolfram (1984); the surjectivity theorem for prime alphabets is due to Kari, Salo
and Törmä (2013), building on Hedlund (1969). We found no prior use of the
streaming width of $t$-step rules, no census of order-3 magma automata and no
analysis of the fuse rule.

## Applications and limitations

Exact fast-forwarding gives the state of affine and fuse automata after $10^9$
steps in milliseconds. The census judges growth on $t \le 9$ only, and the
"geometric" label is empirical; timings come from a loaded shared machine.

## Open questions

1. What do the 685 bounded-width automata without known structure have in common?
2. Does bounded streaming width always allow a fast-forward polynomial in $L$ and
   $\log t$?
3. Is the width of the most complex order-3 automaton truly exponential?
4. How large are the light cones of Laver tables in general?
