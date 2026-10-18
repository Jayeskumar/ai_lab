# Fibonacci dynamics in invented algebras {#ch-magma-dynamics}

*Volume 7 — Computational experiments and algorithms. Research cycle C16.*

## Motivation

The Fibonacci numbers need two things: a pair of starting values and a rule
that turns the last two values into the next one. Any invented operation
provides such a rule:
$$x_{k+1} = x_k \star x_{k-1}.$$
Modulo $m$ with ordinary addition this gives the Pisano periods. What happens
in a finite magma with no laws at all — and what do the laws studied earlier in
this book (anchoring, left-distributivity, the odd and golden laws, nim
arithmetic) do to these sequences?

## Definitions

On a magma $M$ with $n$ elements the state is the pair $(x_{k-1}, x_k)$ and the
*pair map* is
$$P(a, b) = (b,\ b \star a)$$
on the $n^2$ states. Periods are the cycle lengths of $P$; a table is
*full-period* if $P$ is a single cycle through all $n^2$ pairs. Write
$L_b(a) = b \star a$ for the left translations. Every function
$f : M \times M \to M$ is the rule of exactly one magma, so the pair maps of
$n$-element magmas are exactly the *feedback shift registers of order 2* over
an $n$-letter alphabet — a translation that turned several of our findings into
rediscoveries.

## How long can a magma's Fibonacci sequence cycle?

**Theorem 18.1** *[PROVEN — Lean: `pairMap_injective_iff`,
`pairMap_bijective_iff`; REDISCOVERY: Golomb's nonsingularity criterion]*. $P$
is a permutation iff every left translation $L_b$ is a bijection; exactly
$(n!)^n$ tables have this property. The mirror recurrence
$x_{k+1} = x_{k-1} \star x_k$ is the forward recurrence of the opposite magma.

*A bold hypothesis fails.* For Fibonacci numbers modulo $m$ the pair $(0, 0)$
is fixed, so the period is at most $m^2 - 1$. H-C16-1 guessed the same bound for
every magma, attained only by quasigroups. Already for $n = 2$ the table
$x \star y = 1 - y$ produces $0, 0, 1, 1, 0, 0, 1, 1, \ldots$ — period 4.

**Theorem 18.2** *[PROVEN — written; REDISCOVERY: van Aardenne-Ehrenfest and de
Bruijn, 1951]*. A table is full-period iff the symbols along its cycle form a de
Bruijn cycle of order 2 (every ordered pair once as consecutive symbols), and
this correspondence is a bijection. Hence there are exactly
$$\frac{(n!)^n}{n^2}$$
full-period tables of order $n$ — $1, 24, 20736$ for $n = 2, 3, 4$, as the
exhaustive census confirms — and the maximal period is $n^2$ for every $n$.

**Theorem 18.3** (parity) *[PROVEN — written]*. If every $L_b$ is a bijection,
$\operatorname{sgn} P = (-1)^{n(n-1)/2} \prod_b \operatorname{sgn} L_b$, because
$P$ is a coordinate swap after fibrewise left translations. A full period
therefore requires
$$\prod_b \operatorname{sgn} L_b = (-1)^{(n-1)(n+2)/2}.$$

## Quasigroups

None of the 24 full-period tables of order 3, nor any of the 20736 of order 4,
is a quasigroup, and the largest quasigroup period was $n^2 - 1$ for
$n = 2, 3, 4$.

*H-C16-5 [REFUTED].* "No quasigroup is full-period."

**Theorem 18.4** *[PROVEN — written; POTENTIALLY NOVEL]*. A full-period table
is a quasigroup iff every ordered pair also occurs exactly once at *distance 2*
$(x_i, x_{i+2})$ along its cycle. Equivalently, the windows
$(x_{i-1}, x_i, x_{i+1})$ run once through the $n^2$ triples $(a, b, b \star a)$
of the Latin square: the cycle is a universal cycle of the quasigroup.

**Theorem 18.5** *[PROVEN — computer-assisted; POTENTIALLY NOVEL]*.

| order $n$ | 2 | 3 | 4 | 5 | 6 … 16 |
|---|---|---|---|---|---|
| full-period quasigroups | 0 | 0 | 0 | 3360 (28 classes) | examples verified |

The counts for $n \le 5$ come from all $2 + 12 + 576 + 161280$ Latin squares and,
independently, from a depth-first enumeration of cycles with distinct pairs at
distances 1 and 2. An example of order 5 is the cycle
$$0,0,1,0,2,2,0,3,3,1,2,1,4,0,4,4,2,3,2,4,1,1,3,4,3.$$

**Theorem 18.6** *[PROVEN — written]*. The direct product of full-period
quasigroups of coprime orders is full-period (cycles of coprime lengths combine
into one), giving orders such as $30, 35, 40, 42, 45, 56, 63, 72$.

Random sampling revealed a striking pattern: isotopes of the cyclic group
$\mathbb{Z}_n$ were full-period for every odd $n$ from 5 to 15 and *never* for
even $n$. The parity condition explains it.

**Theorem 18.7** *[PROVEN — written; POTENTIALLY NOVEL]*. No isotope
$\gamma(\alpha(x)\beta(y))$ of a group of even order $n = 2m$ is full-period:
its rows have sign product $(-1)^m$, while Theorem 18.3 demands $(-1)^{m+1}$.

*Proof idea.* The sign product equals that of the left regular representation,
$\prod_g \operatorname{sgn}\lambda_g = (-1)^{\#\{g\,:\,n/o(g)\ \text{odd}\}}$, and by
Burnside's normal 2-complement theorem exactly $m$ elements (or none, with $m$
even) have $n/o(g)$ odd. ∎

**Conjecture 18.8** *[COMPUTATIONALLY SUPPORTED]*. Full-period quasigroups
exist for every $n \ge 5$. Random Latin squares are full-period with
probability close to $1/n^2$, as if the pair map were a random permutation of
the forced parity. Exhaustive search and a SAT encoding, by contrast, stall at
$n = 9$.

## Laws shape the dynamics

**Theorem 18.9** *[PROVEN — Lean: `pairMap_fixed_iff`]*. The fixed points of $P$
are the pairs $(a, a)$ with $a \star a = a$; an idempotent magma has period at
most $n^2 - n$, and no idempotent quasigroup is full-period.

**Theorem 18.10** (affine magmas) *[PROVEN — written, Lean for the anchored
case; REDISCOVERY: periods of linear recurrences]*. For $x \star y = \alpha x +
\beta y + \gamma$ on $\mathbb{Z}/N$ with a fixed point, the maximal period is the
order of the companion matrix $\begin{pmatrix} 0 & 1 \\ \beta & \alpha
\end{pmatrix}$. So the anchored associative magma $x + y + 1$ of Chapter 7 is
the Fibonacci sequence in disguise ($y_k = x_k + 1$), with maximal period the
Pisano period $\pi(N)$. The odd law's $x + 1 + y/2$ and the golden law's
$x + 1 + a y$ have the orders of $\begin{pmatrix} 0 & 1 \\ 1/2 & 1
\end{pmatrix}$ and $\begin{pmatrix} 0 & 1 \\ a & 1 \end{pmatrix}$. Their period
sequences, $6, 24, 48, 18, 5, \ldots$ and $4, 120, 342, \ldots$, are not in the
OEIS. For general affine magmas, the maximal period matched the order of the
$3 \times 3$ affine matrix in 300 of 300 random cases (a conjecture).

**Theorem 18.11** *[PROVEN — written; REDISCOVERY]*. In the nimber fields
$[0, 2^{2^k})$ of Chapter 14, nim-multiplication gives maximal period
$\pi(2^{2^k} - 1)$: 40 on $[0, 16)$ and 360 on $[0, 256)$. (Logarithms turn the
recurrence into Fibonacci numbers modulo $2^{2^k} - 1$.)

**Theorem 18.12** (Laver tables) *[PROVEN — written, using Laver's
monotonicity; POTENTIALLY NOVEL (small)]*. For $n \ge 1$ the pair map of the
Laver table $A_n$ has exactly one fixed point and $2^n - 1$ two-cycles, all
through the top element. Every Fibonacci sequence climbs strictly
($x \star y > x$ below the top) until it reaches the top, then alternates.

So the bold guess that Laver periods are powers of 2 was true, for the dullest
possible reason. Observed but unexplained: the climb never takes more than five
steps ($n \le 10$).

For small groups the maximal periods are S3: 8, D4: 6, Q8: 6, A4: 16, S4: 18;
the dihedral value agrees with Knox's period 6 for generating pairs.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C16-01 | all magmas, orders 2–4 | max period $n^2$; de Bruijn counts; no full-period quasigroup |
| EXP-C16-02 | quasigroups | 0, 0, 0, 3360; examples to 16; parity obstruction confirmed |
| EXP-C16-03 | structured families | Laver: period ≤ 2; affine = matrix orders; nimbers 40, 360 |
| EXP-C16-04 | PRNG test | no improvement over PCG64 |
| EXP-C16-05 | search methods | sampling beats DFS and SAT from $n = 9$ |

| generator (2^20 outputs) | result |
|---|---|
| PCG64 (baseline) | passes every test |
| LCG $1664525x + 1013904223$ (baseline) | lowest bit of period 2; low byte too regular |
| anchored Fibonacci $x + y + 1$ on $\mathbb{Z}/2^{32}$ | low byte non-uniform; lowest bit of period 3 |
| affine $x + \beta y + 1$ on $\mathbb{Z}/2^{32}$ | low byte non-uniform; lowest bit of period 3 |
| de Bruijn byte magma (period 65536) | too regular in every frequency test |

## Comparison with existing mathematics

Feedback shift registers (Golomb, 1967), de Bruijn counts (van
Aardenne-Ehrenfest and de Bruijn, 1951), periods of linear recurrences (Ward,
1933; Wall, 1960) and Fibonacci lengths of groups (Knox, 1992; Campbell and
coauthors) cover the general theory. Tuscan squares (Etzion, Golomb and Taylor,
1989) impose similar distance-2 conditions on arrays rather than single cycles.
We found no description of full-period quasigroups, their counts, the
even-order isotope obstruction, or Fibonacci sequences in Laver tables.

## Applications and limitations

The test against standard generators was negative: order-2 recurrences on $n$
symbols cannot have period longer than $n^2$, and affine versions modulo
$2^{32}$ inherit the known low-bit weaknesses of lagged Fibonacci generators.
The test battery is a sanity check, not TestU01. The existence of full-period
quasigroups beyond order 16 is unproved.

## Open questions

1. Do full-period quasigroups exist for every $n \ge 5$? A construction for even
   $n$ must avoid isotopes of groups (Theorem 18.7).
2. How many are there of order 6, and is the count close to $L(6)/36$?
3. Why do Fibonacci sequences in Laver tables reach the top within five steps?
