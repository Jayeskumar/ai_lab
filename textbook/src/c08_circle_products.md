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
| Pisot (other roots $|\beta| < 1$) | 31 | all $s$ beyond a threshold (most cases) |
| non-Pisot (some $|\beta| \ge 1$) | 10 | **none** ($s \le 8$) |

Thresholds grow as $|\beta| \to 1$: Pell ($|\beta| = 0.41$) from $s = 1$,
Fibonacci (0.62) from 2, tribonacci (0.74) from 3, 4-bonacci from 7,
$G_{k+1} = G_k + G_{k-2}$ (0.83) from 10; $G_{k+1} = G_k + G_{k-3}$
($|\beta| \approx 0.94$) not yet at $s = 20$.

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

For $G = 1, 3, 4, 7, 11, \ldots$ (a Lucas-type sequence) the product is
associative for $s = 2$, *not* for $s = 3$, and again for all $s \ge 4$ —
confirmed on inputs up to $10^6$. Our explanation: $\beta^s$ alternates in
sign when $\beta < 0$, and the window is asymmetric about 0 (for Fibonacci
$(-0.382, 0.618)$), so an odd shift can push a product's conjugate out.

**Conjecture 9.2** *[COMPUTATIONALLY SUPPORTED; POTENTIALLY NOVEL]*. For
quadratic Pisot sequences with positive conjugate root the associative shifts
form an upward-closed set; non-monotone sets occur only for negative
conjugates. *Evidence:* 30/30 positive-$\beta$ sequences upward-closed; all
10 non-monotone cases among 60 negative-$\beta$ sequences (EXP-C08-04).

**Conjecture 9.3** *[COMPUTATIONALLY SUPPORTED]*. For non-Pisot sequences the
circle product is non-associative at every shift.

## Comparison with existing mathematics

Knuth (1988) proved associativity for Fibonacci; Arnoux (1989) found the
$\mathbb{Z}[\varphi]$ embedding; Grabner, Pethő, Tichy and Woeginger (1994)
proved associativity for dominant-root recurrences once a parameter is large
enough — our Pisot observations are a **rediscovery** of their theorem; a
Math. Slovaca paper (2000) treats length-2 recurrences and Tribonacci. We did
not find the non-Pisot statement or the sign phenomenon in our (limited)
search.

## Open questions

1. Prove Conjectures 9.2 and 9.3 by computing the greedy windows (Rauzy-type
   fractals for higher degree).
2. Determine the exact threshold $s_0(G)$ from the geometry of the window.
