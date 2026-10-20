# Deciding laws of finite operations {#ch-law-testing}

*Volume 7 — Computational experiments and algorithms. Research cycle C17.*

## Motivation

Every model found by the laboratory's SAT searches had to be checked: is this
table really associative, left-distributive, …? The obvious check examines
all $n^3$ triples. This chapter measures how much the structure found in
earlier chapters can save, against honest baselines.

## Definitions

A finite magma is a table $T$ with $T[a, b] = a \star b$ on $n$ elements. The
cost of a test is its number of *probes* (table look-ups) — an exact,
machine-independent measure. Wall-clock times were also recorded, on a shared
machine, and are indicative only.

## Three tests

**Theorem 19.1** (Light's test) *[PROVEN — written; REDISCOVERY: Light,
Clifford–Preston]*. If $S$ generates the magma, then it is associative iff
$(x \star s) \star y = x \star (s \star y)$ for all $x, y$ and all $s \in S$.

*Proof idea.* The set of "good middles" $s$ is closed under $\star$: if $a$
and $b$ are good, four applications of the definition show that $a \star b$
is good. A submagma containing the generators is everything. ∎

**Corollary 19.2** *[PROVEN]*. For an anchored magma ($x \star 0 = x + 1$),
associativity holds iff $x \star (y + 1) = (x \star y) + 1$ for all $x, y$ —
a check of $2n^2$ probes. (Chapter 7: this identity alone forces
$x \star y = x + y + 1$.)

**Theorem 19.3** *[PROVEN (one-sidedness); detection bound cited —
REDISCOVERY: Rajagopalan–Schulman 2000]*. Comparing $(u \star v) \star w$ with
$u \star (v \star w)$ for random subsets $u, v, w$, computed in the magma
algebra over GF(2), never rejects an associative table and rejects a
non-associative one with probability at least $1/8$ per round, at $O(n^2)$
probes per round.

## The benchmark

Inputs: cyclic groups, anchored tables $x + y + 1$, left-zero bands
($x \star y = x$), random magmas, and single-entry corruptions of the first
two — the hardest case for sampling, since one wrong entry spoils only about
$4n$ of the $n^3$ triples.

| family ($n = 512$) | exhaustive / Light probes | exhaustive time | Light + generators | anchored test |
|---|---|---|---|---|
| cyclic group | 383 | 1.7 s | 6 ms | — |
| anchored $x + y + 1$ | 614 | 1.3 s | 4 ms | 3 ms |
| left-zero band | **1.7** | 1.4 s | 0.94 s | — |
| one corrupted entry | 0.15–1.1 | 0.16 s\* | 4–5 ms | 3 ms |
| random | $4 \cdot 10^{-6}$ (4 probes against $\approx 9 \cdot 10^5$) | 0.19 s\* | 4–5 ms | — |

\* Our vectorised implementation evaluates a whole slab of 64 rows; the probe
column counts a sequential check that stops at the first violating triple.

The first three rows are *certification*: the input is associative and every
exact test must do its full work. There Light's test wins by two to three
orders of magnitude whenever a small generating set exists. The last two rows
are *refutation*, and there the exhaustive check wins: a random magma fails at
the first triple it looks at. The first version of this table showed gains of
48–77 on these rows; the Skeptic traced them to an accounting error (the
exhaustive check was charged a whole slab as soon as the slab contained a
violation), and the numbers above are re-measured.

All exact tests and the randomised test (40 rounds) returned the correct
verdict on all 90 instances; random-triple sampling with $n^2/16$ samples
missed 27 of the 30 near-associative inputs.

*H-C17-1 [REFUTED].* "Light's test always wins by a factor of at least
$n/10$." Left-zero bands need every element as a generator, and the gain
collapses to 1.7×; on non-associative inputs there is no gain at all.

## The anchor instance of a law

For anchored magmas, the instance $z = 0$ of a three-variable law costs only
$O(n^2)$ probes to check. For associativity it decides the law
(Corollary 19.2). Does it always?

*H-C17-2 [REFUTED].* Among the 382 laws of Chapter 7, the anchor instance
decides the law for 339 (all anchored models with $N \le 5$) and is
insufficient for 43 — e.g. $x(yz) = y(y(xz))$ has 11 anchored models of its
instance at $N = 4$, two of which violate the law, and $x(yz) = x(zy)$ fails
already at $N = 3$. (The first version reported 333 / 18 and 31 undecided
laws; a classification bug, found by the Skeptic, had counted laws with a
violation at one size as undecided because the enumeration was capped at
another.)

**Observation 19.4** *[PROVEN — computer-assisted for $N \le 4096$, forcing
argument in Lean; REDISCOVERY]*. For
every $N \le 4096$, the single identity
$x \star (y + 1) = (x \star y) \star (x + 1)$ (for all $x, y$ modulo $N$) has an
anchored solution exactly when $N$ is a power of 2, and then it is the Laver
table. So left-distributivity of an anchored table is decided by an $O(N^2)$
check, at least for these sizes.

The first version checked only $N \le 10$, by SAT. The Skeptic then noticed
why the search space is so small: the instances with $y \le N - 2$ already
*force* the table. Row $N - 1$ must be the identity, and going down, every
entry $x \star (y+1) = v \star (x+1)$ with $v = x \star y > x$ refers to a row
that is already determined — this is Laver's recursion. So for every $N$ there
is at most one candidate, and the question is only whether it satisfies the
remaining wrap-around equations. Building the candidates for every
$N \le 4096$ (EXP-C17-03) shows they do exactly at the powers of 2. Lean
checks the forcing argument, the existence of the candidate and the reduction
to the wrap-around equations for every $N$ (`C17_ForcedTable.lean`).

The Historian's second audit found the general case in the literature.
Biane remarks, in the published version of his survey, that the full instance
fails when $N$ is not a power of 2 (a correction credited to A. Lewandowski),
and Aguilera and Iannella (2026) prove that the wrap-around equation at $x$
holds iff row $x$ ends in the top element; with Dehornoy's criterion — the
table is left-distributive iff every row ends in the top element — this
settles every $N$. The Historian also sketched a direct argument, and the
Skeptic completed it and checked it in Lean:

**Theorem 19.5** *[PROVEN — Lean, from Laver's theorem; REDISCOVERY: Biane,
Aguilera–Iannella]*. For every $N \ge 1$ the identity
$x \star (y + 1) = (x \star y) \star (x + 1)$, wrap-around included, has an
anchored solution iff $N$ is a power of 2.

*Proof idea.* Every row of the forced table is periodic, with period the first
column at which it reaches the top element, and the wrap-around equation holds
in row $x$ iff that period divides $N$. Write $N = 2^k r$ with $r \ge 3$ odd and
$s = N - 2^{k+1}$. Using only that the Laver table of order $2^{k+1}$ satisfies
the identity (Laver's theorem), the rows $s, \ldots, N - 2$ of the forced table
of order $N$ are shifted copies of rows of that Laver table, and row $s - 1$ is
$s, s + 1, \ldots$ with period $2^{k+1}$, which does not divide $N$. ∎ The Lean
file `C17_RowPeriod.lean` proves the equivalence for every $N$ with Laver's
theorem as its only hypothesis; the details are Theorem 5 of
`proofs/paper/C17.md`.

This experiment also corrected the laboratory's own citation of Laver's
theorem in Chapter 7: the classical recursion is imposed only for $q < N$;
with the wrap-around instance there are no solutions at all for most $N$.

## Comparison with existing mathematics

Light's test and the randomised test are classical; the anchored criteria
are small corollaries of Chapter 7. The benchmark is ours.

## Applications and limitations

Certifying a table found by a solver: compute a small generating set and run
Light's test — hundreds of times faster than the exhaustive check in our runs
at $n = 512$ — or, for anchored tables, a single identity. Limitations: Python
implementations on a shared machine; no comparison with optimised C code or
with model checkers.

## Open questions

1. *(Answered in version 1.1 by Theorem 19.5.)* What remains is to prove
   Laver's theorem itself in Lean, which would make Theorem 19.5
   unconditional.
2. Which other laws admit a Light-type reduction to generators?
