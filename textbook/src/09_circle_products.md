# Multiplying digit positions {#ch-circle}

*Volume 4 — Alternative representations of quantities. Research cycle C08.*

## Motivation

In base 10, multiplying $10^i$ by $10^j$ gives $10^{i+j}$: digit positions add.
What happens if we *define* a multiplication by adding digit positions in a
numeration system where that is not automatically consistent? Let $G$ be an
increasing base sequence ($G_0 = 1$), let $n = \sum_i d_i(n) G_i$ be the
greedy expansion, and set
$$a \circ_s b = \sum_{i,j} d_i(a)\, d_j(b)\, G_{i+j+s}.$$
For Fibonacci weights $G = 1, 2, 3, 5, 8, \ldots$ and $s = 2$ this is Knuth's
*circle multiplication* (1988), famous for being associative for no visible
reason. Our implementation reproduces its OEIS table A101330 (EXP-C08-05).

## The associativity atlas

We tested 46 base sequences × shifts $s = 0..5$ exhaustively on $[1,22]^3$,
then every candidate on random triples up to $10^6$ (EXP-C08-01..03). The
pattern is governed by the roots of the sequence's *minimal* recurrence:

| class of $G$ | sequences | associative shifts |
|---|---|---|
| geometric ($G_k = b^k$) | 5 | all $s$ |
| Pisot (other roots $|\beta| < 1$) | 31 | all $s$ beyond a threshold (most cases; see the correction below) |
| non-Pisot (some $|\beta| \ge 1$) | 10 | **none** ($s \le 8$) |

Thresholds grow as $|\beta| \to 1$: Pell ($|\beta| = 0.41$) from $s = 1$,
Fibonacci (0.62) from 2, tribonacci (0.74) not before 4, 4-bonacci not
before 8, $G_{k+1} = G_k + G_{k-2}$ (0.83) not before 11;
$G_{k+1} = G_k + G_{k-3}$ ($|\beta| \approx 0.94$) not yet at $s = 20$.

> **Correction (2026-10-18).** The first version of this chapter gave the
> thresholds 3 (tribonacci), 7 (4-bonacci), 10 ($G_k + G_{k-2}$) and 5
> ($G_{k+1} = 2G_k + 2G_{k-1}$). All four are wrong. The laboratory's
> Historian found the tribonacci counterexample in the literature —
> $(10016 \circ_3 10016) \circ_3 1 = 3414681926 \ne 3414681924 =
> 10016 \circ_3 (10016 \circ_3 1)$, the example by which Ambrož, Frougny,
> Masáková and Pelantová (2003) refuted a conjecture of Arnoux — and one more
> by computation. A certificate-producing re-test (EXP-C08-06) found the
> other two. The original tests sampled random triples up to $10^6$, and
> such sampling misses rare failures. Every failure quoted above is now
> certified by an explicit triple; every "from $s$" is a search result,
> proved only where the literature proves it (Fibonacci: Lean; Pell:
> Messaoudi 2000; tribonacci $s \ge 6$ and 4-bonacci $s \ge 10$: Messaoudi).

## Why: a twisted embedding into an algebraic number field

**Theorem 9.1** *[PROVEN — Lean: `circ_assoc`, `circ_comm`, `key`, `window`;
REDISCOVERY (Knuth, Arnoux)]*. For every $t \ge 0$ the shifted Knuth product
$a \circ_t b = \sum_{k \in Z(a),\, l \in Z(b)} F_{k+l+t}$ (Zeckendorf indices
$\ge 2$) is associative and commutative. For the two smaller shifts the
product is not associative.

*Proof.* Put $E(n) = \sum_{k \in Z(n)} \varphi^k$ and
$E'(n) = \sum_{k\in Z(n)} \psi^k$ ($\psi = -1/\varphi$). Since
$\varphi^k = F_k\varphi + F_{k-1}$, $E(n) = n\varphi + n^*$ and
$E'(n) = n\psi + n^*$ for an integer $n^*$. The conjugates of Zeckendorf sums
lie in a window of length 1: $|E'(n)| < -\psi$ (the Lean proof) or, sharper,
$-\psi^2 < E'(n) < -\psi$. For a product, $\varphi^t E(a)E(b) = P\varphi + Q$
and $\psi^t E'(a)E'(b) = P\psi + Q$ with $P = a\circ_t b$; the second number
has absolute value $< \psi^2$, so $|Q - P^*| < \psi^2 - \psi = 1$, forcing
$Q = P^*$. Hence $E(a \circ_t b) = \varphi^t E(a)E(b)$ — the product becomes
multiplication in $\mathbb{Z}[\varphi]$ twisted by $\varphi^t$ — and
associativity follows because $n$ is recovered from $(E(n), E'(n))$. ∎

The same picture explains the atlas. The conjugate coordinates of a product
are multiplied by $\beta^s$; if $|\beta| < 1$ large shifts push them into the
window of greedy expansions, if $|\beta| \ge 1$ nothing can.

## A surprise: non-monotone thresholds

For $G = 1, 3, 4, 7, 11, \ldots$ (a Lucas-type sequence) no failure is found
for $s = 2$, $s = 3$ fails (certified), and no failure is found again for
$s \ge 4$ — even under the stronger search of EXP-C08-06. Our explanation: $\beta^s$ alternates in
sign when $\beta < 0$, and the window is asymmetric about 0 (for Fibonacci
$(-0.382, 0.618)$), so an odd shift can push a product's conjugate out.

**Conjecture 9.2** *[COMPUTATIONALLY SUPPORTED; POTENTIALLY NOVEL (low)]*.
For quadratic Pisot sequences with positive conjugate root the associative
shifts form an upward-closed set; non-monotone sets occur only for negative
conjugates — and, as the Historian pointed out, only for *non-canonical*
initial values: for canonical sequences Messaoudi's criterion implies
upward-closure whatever the sign of $\beta$. *Evidence (after the certified
re-test, EXP-C08-06):* 0 of 30 positive-$\beta$ sequences non-monotone; 10
non-monotone sequences, all non-canonical with $\beta < 0$. Two of the
original ten examples were artefacts of random testing.

**Conjecture 9.3** *[COMPUTATIONALLY SUPPORTED]*. For non-Pisot sequences the
circle product is non-associative at every shift.

## Comparison with existing mathematics

Knuth (1988) proved associativity for Fibonacci; Arnoux (1989) found the
$\mathbb{Z}[\varphi]$ embedding; Grabner, Pethő, Tichy and Woeginger (1994)
proved eventual associativity for recurrences with non-increasing
coefficients and canonical initial values — our Pisot observations are a
**rediscovery** of their theorem in that range (the first version of this
chapter overstated it as "all Pisot sequences"). A. Messaoudi (Math. Slovaca
2000) characterises associativity by the stability of the conjugate window —
exactly our mechanism — and proves the Fibonacci case for all $s \ge 2$;
Ambrož, Frougny, Masáková and Pelantová (2003) bound the fractional digits of
products of tribonacci integers. We did not find the non-Pisot statement or
the sign phenomenon.

## Open questions

1. Prove Conjectures 9.2 and 9.3 by computing the greedy windows (Rauzy-type
   fractals for higher degree).
2. Determine the exact threshold $s_0(G)$ from the geometry of the window.
