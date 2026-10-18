# Primes of an invented multiplication {#ch-circle-primes}

*Volume 4 — Alternative representations. Research cycle C09.*

## Motivation

Chapter 9 produced a new associative, commutative operation on the positive
integers. Every such operation has an arithmetic: which numbers are
*irreducible* (not $a \circ b$), how many are there, and is factorisation
unique?

## Exact formulas

From the embedding $\nu(n) = n\varphi + n^*$ with $n^* = \lfloor (n+1)/\varphi \rfloor$:
$$a \circ b = ab + a b^* + a^* b,\qquad (a\circ b)^* = ab + a^* b^*,$$
validated against the digit definition on 89,401 pairs.

## Structure

**Theorem 10.1** *[PROVEN — written, resting on Theorem 9.1]*.
$(\mathbb{N}_{\ge 1}, \circ)$ is commutative and cancellative, has no identity,
and embeds into the multiplicative monoid of $\mathbb{Z}[\varphi]$. The
Fibonacci numbers are exactly the elements mapped to units
($\nu(F_k) = \varphi^k$), and $F_j \circ F_k = F_{j+k}$. The norm
$N(n) = n^{*2} + n n^* - n^2$ is multiplicative.

**Refuted hypothesis.** Factorisation into irreducibles is *not* unique:
$8 = 1 \circ 1 \circ 1 = 2 \circ 2$ (EXP-C09-02). The reason is pretty: 1 and
2 are $F_2$ and $F_3$, so factorisations of $F_k$ are factorisations of $k$ in
the numerical semigroup $\langle 2, 3\rangle$.

## Circle primes are common

We conjectured (H-C09-1) that circle irreducibles thin out like primes. The
data (EXP-C09-01) disagree: up to $10^6$ more than half of all integers are
irreducible (density 0.600, 0.577, 0.562, 0.549, 0.539 at $10^2..10^6$). A
proof explains why.

**Theorem 10.2** (window obstruction) *[PROVEN — written; POTENTIALLY NOVEL]*.
If $n = a\circ b$ then the conjugate $\nu'(n) = \nu'(a)\nu'(b)$ lies in
$(\psi^3, \psi^2)$, i.e. the fractional part of $(n+1)/\varphi$ lies in
$(0.2360\ldots, 0.8541\ldots)$, an interval of length $1/\varphi$. Hence every
$n$ outside it is irreducible, and by Weyl equidistribution these $n$ have
density exactly $1/\varphi^2 \approx 0.381966$.

Numerically: not a single reducible number up to $10^6$ lies outside the zone,
and the forced-irreducible density at $10^6$ is 0.381966 (EXP-C09-04).

**Theorem 10.3** *[PROVEN — written]*. Every factorisation of $n$ into $r$
irreducibles satisfies $|\nu'(n)| < |\psi|^r$; factorisation lengths are
bounded.

**Conjecture 10.4** *[CONJECTURE]*. The circle irreducibles have density
exactly $1/\varphi^2$: almost every $n$ in the product zone is reducible. The
irreducible fraction inside the zone falls slowly — 0.316, 0.291, 0.270,
0.255 at $10^3..10^6$.

## A lesson in reading the OEIS

The list of irreducibles matched OEIS A026273 for 24 terms. Reading the
entry term by term showed the sequences diverge at 40 ($= 4 \circ 4$): for
$n < 40$ every product has the form $1 \circ b$, a Beatty-like set related to
the Wythoff sequences, which explains the coincidence. The irreducibles of
Knuth's product appear not to be catalogued.

## Open questions

1. Prove Conjecture 10.4.
2. Describe the irreducibles through prime factorisation in $\mathbb{Z}[\varphi]$
   plus a unit-window condition.
3. The same questions for other associative circle products.
