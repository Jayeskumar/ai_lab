# The cost of counting {#ch-counting-cost}

*Volume 4 — Alternative representations. Research cycle C10.*

## Motivation

The successor $n \mapsto n+1$ is the most basic operation on quantities. Its
*cost* in a representation — the number of digit positions that change — is
a natural measure of how well the representation suits counting, and it
matters in practice (counters in data structures and hardware).

*Which measure.* Throughout this chapter the cost is the Hamming distance
between the representations of $n$ and $n+1$. Berthé, Frougny, Rigo and
Sakarovitch (Adv. Appl. Math., 2020) study the related *carry propagation*
measure systematically; under theirs the Zeckendorf value is $\varphi^2$, not
the 2 we obtain below. The two measures agree for ordinary bases.

## Classical constants

**Theorem 11.1** *[PROVEN — written; REDISCOVERY]*. The average cost per
increment is $b/(b-1)$ in base $b$ (2 in binary, $10/9$ in decimal), the same
in negabinary and balanced ternary, $e - 1 \approx 1.71828$ in the factorial
base, and exactly 1 for the Gray code. *(Digit $k$ changes with frequency
$b^{-k}$, respectively $1/k!$.)*

Measured over $n < 10^6$ (EXP-C10-01): binary 1.999988, factorial 1.7182767,
Gray 1.0, skew binary 1.4999955 with worst case 2.

## Zeckendorf counts like binary

The Inventor guessed that the sparse Zeckendorf system (no two adjacent ones)
would be cheaper to count in than binary. It is not.

**Theorem 11.2** *[PROVEN — written; REDISCOVERY in substance: OEIS A215005]*.
Let $T_m$ be the total cost of counting
from 0 to $G_m - 1$ in the Zeckendorf system ($G = 1, 2, 3, 5, \ldots$). Then
$$T_{m+1} = T_m + T_{m-1} + \lceil m/2\rceil + 1,\qquad
  T_m = 2G_m - \lceil m/2\rceil - 2,$$
so the average cost tends to exactly 2, the same as binary.

*Proof idea.* The numbers below $G_{m+1}$ split into $[0, G_m)$ and a block of
$G_{m-1}$ numbers beginning "10"; the step from $G_m - 1 = 1010\cdots$ to
$G_m = 10\cdots0$ costs $\lceil m/2 \rceil + 1$. ∎

The sequence $T_m$ is OEIS A215005; the per-increment cost sequence is not
catalogued.

## Exchange systems

For the exchange numerations of Chapter 3 two clean laws hold.

**Theorem 11.3** *[PROVEN — written]*. A terminating carry rule
$m[k] \to \sum b_j[k+j]$ fires on average $1/(m - \sum b_j)$ times per
increment (the abelian property makes one-at-a-time counting fire exactly as
often as stabilising $n$ tokens at once).

**Theorem 11.4** *[PROVEN — written]*. If only one $b_g = q$ is nonzero, every
increment changes exactly (firings $+ 1$) digits, so the average cost is
$1 + 1/(m - q)$: 2 for base $3/2$, $3/2$ for base 3.

With two or more nonzero $b_j$ a level can receive several tokens in one
increment, and the cost carries a rule-specific excess — 0.500 for
$3[k] \to [k+1] + [k+2]$, 0.333 for $4[k] \to [k+1] + [k+2]$, 0.831 for
$4[k] \to [k+1]+[k+2]+[k+3]$ (EXP-C10-03). *Conjecture:* these are expectations
under the invariant measure of the digit process; we have no formula.

## Application note

As counters, none of the invented exchange representations beats the
classical choices: Gray code (cost 1 at every step) or skew binary (average
1.5, worst case 2, used in purely functional random-access lists). We record
this as a negative result.
