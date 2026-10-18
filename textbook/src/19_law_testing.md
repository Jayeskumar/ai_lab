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
| cyclic group | 383 | 1.4 s | 6 ms | — |
| anchored $x + y + 1$ | 614 | 1.7 s | 5 ms | 3 ms |
| left-zero band | **1.7** | 1.6 s | 1.2 s | — |
| one corrupted entry | 48–77 | 0.18 s | 5–7 ms | 3 ms |
| random | 74 | 0.20 s | 5 ms | — |

All exact tests and the randomised test (40 rounds) returned the correct
verdict on all 90 instances; random-triple sampling with $n^2/16$ samples
missed 27 of the 30 near-associative inputs.

*H-C17-1 [REFUTED].* "Light's test always wins by a factor of at least
$n/10$." Left-zero bands need every element as a generator, and the gain
collapses to 1.7×.

## The anchor instance of a law

For anchored magmas, the instance $z = 0$ of a three-variable law costs only
$O(n^2)$ probes to check. For associativity it decides the law
(Corollary 19.2). Does it always?

*H-C17-2 [REFUTED].* Among the 382 laws of Chapter 7, the anchor instance
decides the law for 333 (all anchored models with $N \le 5$), is insufficient
for 18 — e.g. $x(yz) = y(y(xz))$ has 11 anchored models of its instance at
$N = 4$, two of which violate the law — and could not be settled for 31.

**Observation 19.4** *[COMPUTATIONALLY SUPPORTED]*. For $2 \le N \le 10$,
the single identity $x \star (y + 1) = (x \star y) \star (x + 1)$ (for all
$x, y$ modulo $N$) has anchored solutions only for $N = 2, 4, 8$: the Laver
tables. So left-distributivity of an anchored table is decided by an
$O(N^2)$ check, at least for these sizes.

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

1. Prove Observation 19.4 for all $N$.
2. Which other laws admit a Light-type reduction to generators?
