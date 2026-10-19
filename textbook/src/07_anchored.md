# Anchored operations and arithmetic spectra {#ch-anchored}

*Volume 2 — Invented operations and their properties. Research cycle C06.*

## Motivation

An invented operation with no laws is just a table. A law such as
associativity cuts the tables down, and Chapter 6 asks which sizes admit
*any* model. Here we add one more ingredient, the simplest link between an
operation and counting: we *anchor* the operation to the successor,
$$x \star 0 = x + 1 \pmod N,$$
and ask, for a single composition law, for which sizes $N$ a model exists
and how many there are. The answers turn out to be pieces of arithmetic.

## Definitions

A *successor-anchored magma* of size $N$ is a binary operation $\star$ on
$\mathbb{Z}/N$ with $x \star 0 = x + 1$. The *spectrum* of a law is the set
of $N$ admitting an anchored model. An isomorphism of anchored structures must
fix 0 and commute with $x \mapsto x \star 0$, so it is the identity; we
therefore count tables. A table is *affine* if $x \star y = x + a y + 1$ for
some $a \in \mathbb{Z}/N$.

## The classical case: left-distributivity

For the left-distributive law $x \star (y \star z) = (x \star y) \star (x \star z)$
the anchor produces the famous **Laver tables**.

**Theorem 7.1** *[PROVEN — published theorem (Laver; Dehornoy, Prop. X.1.6);
REDISCOVERY]*. An anchored left-distributive magma of size $N$ exists iff $N$ is a
power of 2, and it is then unique.

Our evidence is independent of Laver's recursion: a complete SAT enumeration
finds exactly one model for $N = 1, 2, 4, 8$ and none for the other
$N \le 10$ (EXP-C06-02); Laver's recursion gives left-distributive tables
exactly at the powers of two up to 64 (EXP-C06-01). Lean checks the table
$A_3$ and the non-existence for $N = 3$. The general theorem is published
(Laver; elementary proof by Drápal; Dehornoy's book) and we do not re-prove it;
we read its statement in Biane's refereed survey (Sém. Lothar. Combin. 80,
2019, §2.2), whose published version restricts the recursion to $q < N$ — the
correction of the arXiv version that Chapter 19 rediscovers.

## When the anchor pins everything

**Theorem 7.2** *[PROVEN — Lean: `anchored_assoc_unique`]*. An anchored
associative operation is $x \star y = x + y + 1$, for every $N$.

**Theorem 7.3** *[PROVEN — Lean: `anchored_rd_unique`]*. An anchored
right-distributive operation, $(x \star y) \star z = (x \star z) \star (y \star z)$,
is $x \star y = x + 1$, for every $N$.

In both proofs, putting $z = 0$ moves the anchor *along* the law and pins the
whole table. Left-distributivity instead sends the anchor through *other
rows*, $p \star (q+1) = (p \star q) \star (p+1)$, and the consistency of that
recursion is a genuine arithmetic constraint on $N$.

## A bold hypothesis fails

*H-C06-2 [REFUTED].* "Restricted spectra are special to left-distributivity:
every other law gives either every $N$ or only $N = 1$."

We tested all 382 laws $x(yz) = t$ and $(xy)z = t$ whose right side has three
or four leaves using exactly $x, y, z$ (EXP-C06-03): 77 have models for every
$N \le 6$, 283 only for $N = 1$, and **22** have a restricted spectrum — only
one of them left-distributivity:

| spectrum (N ≤ 8) | number of laws | example |
|---|---|---|
| $\{1, 2\}$ | 10 | $x(yz) = ((xx)y)z$ |
| $\{1, 3\}$ | 7 | $x(yz) = ((zx)x)y$ |
| $\{1, 5\}$ | 2 | $(xy)z = x(y(zz))$ |
| odd $N$ | 2 | $(xy)z = x((yz)z)$ |
| powers of 2 | 1 | $x(yz) = (xy)(xz)$ |

## The odd law and the golden law

**Theorem 7.4** *[PROVEN — Lean: `odd_law_even_impossible`,
`odd_law_formula`, `odd_law_model`; POTENTIALLY NOVEL (small)]*. The law
$(x \star y) \star z = x \star ((y \star z) \star z)$ has an anchored model
iff $N$ is odd, and then exactly one: $x \star y = x + 1 + y/2$.

*Proof.* Put $z = 0$: $(x \star y) + 1 = x \star (y + 2)$. Going $N/2$ times
around an even cycle would give $x \star y = x \star y + N/2$; for odd $N$
every $y$ is $2k$ and $x \star y = x + 1 + k$. ∎

**Theorem 7.5** *[PROVEN — written, Skeptic-reviewed; Lean (Chapter 8):
`golden_law_models`; POTENTIALLY NOVEL (small)]*. The anchored
models of $(x \star y) \star z = x \star (y \star (z \star z))$ are exactly the
tables $x \star y = x + 1 + a y$ with
$$a^2 + a \equiv 1 \pmod N .$$
So the spectrum is the set of moduli in which the golden ratio exists:
$N = 5^e m$ with $e \le 1$ and every prime factor of $m$ congruent to
$\pm 1 \bmod 5$ — $1, 5, 11, 19, 29, 31, 41, 55, \ldots$ (OEIS A089270) — and
the number of models is the number of roots (OEIS A087781).

*Proof idea.* Putting $z = 0$ gives $x \star (y \star 1) = (x \star y) + 1$.
Iterating $\sigma(y) = y \star 1$ from 0 visits every element (the values
$0 \star \sigma^k(0) = 1 + k$ are distinct), so the table is
$x \star y = x + 1 + \kappa(y)$ for a bijection $\kappa$; the law then forces
$\kappa(y + c) = \kappa(y) + 1$ with $c$ a unit, so $\kappa$ is linear,
$\kappa(y) = a y$, and the law reduces to $a^2 + a = 1$. Quadratic reciprocity
and Hensel's lemma count the roots. ∎

The predictions were tested before they were proved: the SAT solver finds
exactly 1, 1 and **2** models at $N = 1, 5, 11$ and none at the other
$N \le 12$ (EXP-C06-04).

*A second hypothesis fails.* H-C06-3 guessed that *every* spectrum other than
Laver's is explained by affine tables. Six laws refute it — e.g.
$x(yz) = y(x(yz))$ has models for every $N$, none of them affine — but for 20
of the 22 restricted laws every model found ($N \le 9$) is affine.

## Two counting theorems

**Theorem 7.6** *[PROVEN — written]*. The anchored magmas satisfying
$(xy)z = (xz)y$ are exactly $x \star y = x + c(y)$ with $c(0) = 1$; there are
$N^{N-1}$ of them. (The law says that right translations commute; they all
commute with the successor, an $N$-cycle, whose centraliser consists of its
powers.)

**Theorem 7.7** *[PROVEN — Lean core: `centralizer_eq`, `comp_eq`, `id_eq`,
`leftPerm_assoc`, `leftPerm_comm`; REDISCOVERY in substance — a two-line
lemma on left-permutable groupoids with a right identity]*. Anchored
magmas satisfying $x(yz) = y(xz)$ correspond bijectively to commutative monoid
structures on $\mathbb{Z}/N$ with identity 0, via $a \cdot b = (a-1) \star b$.
Their numbers $1, 2, 9, 94, 1486, \ldots$ are OEIS A058156.

*Proof idea.* The maps $f_m = L_{m-1}$ commute and satisfy $f_m(0) = m$. Any
map $g$ commuting with all of them satisfies $g(m) = g(f_m(0)) = f_m(g(0)) =
f_{g(0)}(m)$: the family is its own centraliser. So it is closed under
composition and contains the identity — it is the regular representation of
a commutative monoid. ∎

The OEIS match came first; the explanation followed from asking *why* a
count of magmas should equal a count of monoids.

## Which sets can be spectra?

**Theorem 7.8** *[PROVEN — written]*. If a set of laws has anchored models of
coprime sizes $N$ and $M$, it has one of size $NM$.

*Proof.* Take the direct product of the two models and transport it to
$\mathbb{Z}/NM$ along the Chinese remainder isomorphism, which sends $x + 1$
to $(x + 1, x + 1)$ and therefore preserves the anchor. ∎

Every spectrum contains $N = 1$; Theorem 7.8 adds that a spectrum containing
two primes contains their product, so it can never be $\{1\}$ together with
an infinite set of primes.
Every spectrum we have seen is also closed under *divisors*; whether that is
always so is the first question of the next cycle.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C06-01 | Laver's recursion | LD exactly at powers of 2 (N ≤ 64); periods A098820 |
| EXP-C06-02 | model counts for 12 laws | LD: 1 at 1, 2, 4, 8; $N^{N-1}$; A058156 |
| EXP-C06-03 | spectra of 382 laws | 22 restricted; H-C06-2 refuted |
| EXP-C06-04 | affine models | golden and odd predictions exact; H-C06-3 refuted |

## Comparison with existing mathematics

Theorem 7.1 is Laver's; the number theory in Theorem 7.5 is classical and the
moduli are catalogued in the OEIS. Left-permutable groupoids are studied in
the literature on groupoid identities, and the centraliser argument is the
regular representation. We found no prior statement of the odd law, the
golden law or the left-permutable correspondence for anchored operations;
each is small.

## Applications and limitations

No application is claimed. The data cover laws with at most four leaves on
the right and sizes up to 8–12; spectra of larger laws are unexplored.

## Open questions

1. ~~Prove that the laws with spectra $\{1, 2\}$ and $\{1, 3\}$ have no other
   models.~~ Chapter 8 proves it for 16 of the 17 laws (two of them in Lean);
   only $x(yz) = y((yx)z)$ remains.
2. Which sets of integers are anchored spectra of a single law? They are
   closed under coprime products (Theorem 7.8); are they closed under divisors?
3. Are there laws other than left-distributivity with non-affine,
   Laver-like spectra?
