# Arithmetic from the minimal excludant {#ch-mex}

*Volume 5 — Mathematical transformations and relationships. Research cycle C07.*

## Motivation

Most operations are defined by saying what their result *is*. Combinatorial
game theory suggests another way: define the result as the least value that is
*not* produced by a prescribed set of earlier results — the minimal excludant,
or mex. Conway built the nimbers this way:
$$a \oplus b = \operatorname{mex}\{a' \oplus b,\ a \oplus b' : a' < a,\ b' < b\},$$
$$a \otimes b = \operatorname{mex}\{(a' \otimes b) \oplus (a \otimes b') \oplus (a' \otimes b') : a' < a,\ b' < b\},$$
and obtained a field of characteristic 2 on the natural numbers. What else
does exclusion produce?

## Definitions

An operation of our family is given by a *spec*: which earlier entries are
"options" — $f(a', b)$ for $a' < a$ (L), $f(a, b')$ for $b' < b$ (R), and, for
$a' < a, b' < b$, XOR combinations of $x = f(a', b)$, $y = f(a, b')$,
$z = f(a', b')$ (D, any of the seven nonempty masks). Then
$f(a, b) = \operatorname{mex}$ of the option values. There are
$2 \cdot 2 \cdot 2^7 = 512$ specs; nim-sum is L + R and nim-product is
D[$x \oplus y \oplus z$].

## Which mex operations are associative?

*H-C07-1 [REFUTED].* "Apart from trivial ones, only Conway's two operations
are associative."

**Theorem 14.1** *[PROVEN — written and computer-assisted; the formulas are
classical]*. On $[0, 64)^2$ the 512 specs produce 134 different operations.
Exactly eleven are associative, and their canonical specs define, for all
$a, b$:

| spec | operation |
|---|---|
| (none) | $0$ |
| L, R | $a$, $b$ |
| D[$x$], D[$y$] | $a$ if $b > 0$ (else 0); $b$ if $a > 0$ (else 0) |
| D[$z$] | $\min(a, b)$ |
| L + R | $a \oplus b$ |
| D[$x \oplus y \oplus z$] | $a \otimes b$ |
| L + R + D[$z$] | $a + b$ |
| D[$x$] + D[$y$] | $((a-1) \oplus (b-1)) + 1$ on positives, 0 absorbing |
| D[$x$] + D[$y$] + D[$z$] | $a + b - 1$ on positives, 0 absorbing |

Every other spec is refuted by an explicit triple. So **ordinary addition is a
mex operation** — the least value not reachable by decreasing either argument
or both — and so is min.

*Proof idea.* For L + R + D[$z$] the options are $a' + b$, $a + b'$ and
$a' + b'$, which together cover exactly $0, \ldots, a + b - 1$. The other
formulas follow the same pattern or Conway's arguments. ∎

## Closure fails

*H-C07-2 [REFUTED].* "Commutative mex operations are closed on the segments
$[0, 2^{2^m})$, like the nimbers." Already for D[$x \oplus y$] we have
$f(2, 3) = 4$, and 30 of the 34 commutative operations fail.

**Theorem 14.2** *[PROVEN]*. If a spec contains both L and R, 0 is an
identity; if it contains neither, 0 is absorbing.

Beyond these facts, most commutative mex operations look chaotic: their values
grow roughly quadratically and 88 of their rows and diagonals are not in the
OEIS (EXP-C07-02).

## A Jacobsthal row

Wythoff's game, whose Grundy function is also a mex recursion, has *additively
periodic* rows: $G(a, b + p) = G(a, b) + p$ for large $b$. We guessed that
this was the rule (H-C07-4). The operation
$$f(a, b) = \operatorname{mex}\{f(a', b) \oplus f(a, b') : a' < a,\ b' < b\}$$
refutes it in an unexpectedly orderly way. Its first rows are $f(0, b) = 0$,
$f(1, b) = b$, and the second row begins
$$0,\ 2,\ 1,\ 4,\ 3,\ 8,\ 9,\ 10,\ 5,\ 6,\ 7,\ 16,\ 17,\ 18,\ 19,\ 20,\ 11,\ 12,\ \ldots$$

**Theorem 14.3** (the Jacobsthal row) *[PROVEN — written; POTENTIALLY NOVEL
(small)]*. Let $J_k = (2^k - (-1)^k)/3$ ($1, 1, 3, 5, 11, 21, 43, \ldots$).
For every $k \ge 1$ the second row exchanges the blocks
$$[\,2^k - J_k,\ 2^k\,) \quad\text{and}\quad [\,2^k,\ 2^k + J_k\,)$$
by translation: $f(2, b) = b + J_k$ on the first and $b - J_k$ on the second.
In particular the row is an involution, $|f(2, b) - b|$ is unbounded, and the
row is not additively periodic.

*Proof idea.* The row satisfies $g(b) = \min\{v : v \notin G,\ v \oplus b \notin G\}$
with $G$ the earlier values. Because $J_{k+1} + J_k = 2^k$, when the $k$-th
pair of blocks begins the used values are exactly $[0, 2^k - J_k)$. Inside the
pair, every smaller candidate is excluded because two numbers just below $2^k$
have a small XOR, while the claimed value survives because adding a number
$c > x$ to $x$ always creates a new top bit. ∎ An independent implementation
confirms the formula for all $b < 2^{15}$ (EXP-C07-03). Only 222 of 670 rows
tested are additively periodic.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C07-01 | census of 512 specs | 134 operations, 11 associative |
| EXP-C07-02 | structure of commutative ones | 0 identity/absorbing; 88 sequences not in OEIS |
| EXP-C07-03 | additive periodicity of rows | 222/670 rows; Jacobsthal row to $2^{15}$ |

## Comparison with existing mathematics

Nim-sum and nim-product are Conway's (*On Numbers and Games*, 1976);
$a + b$ and $\min(a, b)$ as mex values are the rank functions of product
orders, folklore in game theory. Additive periodicity is a theorem for
Wythoff's game (Dress, Flammenkamp and Pink, 1999). We found no prior
description of the Jacobsthal row or of the census.

## Applications and limitations

No application is claimed. The census uses tables up to $64 \times 64$ and
rows up to $b < 1500$; 33 specs are known to agree with associative formulas
only on that window.

## Open questions

1. Do rows $a \ge 3$ of the same operation have a recursive block structure?
2. Which mex tables are automatic sequences, so that statements about them
   could be decided mechanically?
3. Are the remaining 33 associative-looking specs associative for all
   arguments?
