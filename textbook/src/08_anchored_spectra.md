# Which sets of integers are spectra? {#ch-anchored-spectra}

*Volume 3 — Emergent mathematical structures. Research cycle C13.*

## Motivation

Chapter 7 anchored an invented operation to the successor, $x \star 0 = x + 1$
on $\mathbb{Z}/N$, and found that single laws cut out arithmetic sets of
sizes: the powers of two (Laver), the odd numbers, the moduli in which the
golden ratio exists. Every such *spectrum* is closed under products of coprime
sizes (Theorem 7.8). This chapter asks the converse question: **which sets of
integers are spectra?** Two answers emerge. Through the *affine* models a
single law can encode a remarkable range of classical number theory — squares,
cubes and cyclotomic conditions modulo $N$. But spectra in general are wilder
than the examples suggested: they need not even be closed under divisors.

## Definitions

An anchored table is *affine* if $x \star y = x + a y + 1$ for some
$a \in \mathbb{Z}/N$ (under the anchor these are the only tables of the form
$\alpha x + \beta y + \gamma$). Evaluating both sides of a law in the affine
table turns it into a finite set of polynomials in $\mathbb{Z}[a]$, its
*affine system*; the *affine spectrum* $\mathrm{Aff}(E)$ is the set of $N$ for
which the system has a common root modulo $N$. Always
$\mathrm{Aff}(E) \subseteq \mathrm{Spec}(E)$; a law is *affinely rigid* if
every anchored model is affine, so that the two coincide.

## Affine spectra are arithmetic

**Theorem 8.1** *[PROVEN — written]*. Affine spectra are closed under divisors
and under coprime products, so membership of $N$ depends only on the prime
powers dividing $N$. If the polynomials of the affine system have no common
factor over $\mathbb{Q}$, the affine spectrum is the set of divisors of a
single integer $L$; otherwise it is infinite (by Schur's theorem).

The laboratory computed the affine spectra of all 18,581 laws with at most
four leaves per side over $x, y, z$, and of all 75,625 laws over $x, y$ with
at most five leaves per side (EXP-C13-01). They fall into 27 and 125 distinct
spectra. Every finite one is a divisor set $\mathrm{Div}(L)$, with $L$
ranging over 80 values up to 328. The infinite ones read like a table of
contents of elementary number theory:

| affine condition | spectrum | OEIS | example law |
|---|---|---|---|
| $2a + 1 = 0$ | odd numbers | A005408 | $x = x((xx)x)$ |
| $3a + 1 = 0$ | $3 \nmid N$ | A001651 | $((xx)x)x = ((yy)y)y$ |
| $a^2 + 1 = 0$ | $-1$ is a square mod $N$ | A008784 | $x(xx) = y(xy)$ |
| $a^2 - 2a - 1 = 0$ | $2$ is a square mod $N$ | A057126 | $(xx)(xy) = (yy)(yx)$ |
| $a^2 + 2a - 2 = 0$ | $3$ is a square mod $N$ | A057125 | (5 leaves) |
| $a^2 + a + 1 = 0$ | $x^2 + xy + y^2$ represents $N$ primitively | A034017 | $x = x(x(xx))$ |
| $a^2 - a - 1 = 0$ | golden ratio exists mod $N$ | A089270 | $x(xy) = y(yx)$ |
| $2a^2 + 2a + 1 = 0$ | all prime factors $\equiv 1 \bmod 4$ | A004613 | (5 leaves) |
| $2a^2 - 1 = 0$ | all prime factors $\equiv \pm 1 \bmod 8$ | A058529 | (4 leaves) |
| $a^4 + 1 = 0$ | $-1$ is a fourth power mod $N$ | A192453 | (5 leaves) |
| $a^4 - a^2 + 1 = 0$ | all prime factors $\equiv 1 \bmod 12$ | A354467 | (5 leaves) |

Some cubic and quartic conditions — the plastic number ($a^3 - a - 1$), the
tribonacci and tetranacci polynomials, the fifth cyclotomic polynomial — give
sets that are **not in the OEIS** at all.

## …but most laws are not rigid

*H-C13-2 [REFUTED].* "Every law with an infinite, non-trivial affine spectrum is
affinely rigid." The laboratory blocked all affine tables and asked a SAT
solver for any other model (EXP-C13-02). Of 199 laws — the three shortest of
every class — **198 have non-affine models**, most of them at every size from
3 to 8. The shortest laws in each class are weak (for example $x = x(x(xx))$
only constrains each element's own diagonal), and weak laws have many models:
the affine spectrum of $x = x(x(xx))$ is the Eisenstein set A034017, but its
true spectrum turns out to be every $N$ except 2 (Theorem 8.6 below).

So affine spectra are lower bounds. To realise an arithmetic set as a *true*
spectrum, a law must be shown to be rigid, and the laboratory found a large
family where this can be proved.

**Theorem 8.2** *[PROVEN — Lean: `right_normed_translation`]*. For any term
$V(y, z)$, every anchored model of $(x \star y) \star z = x \star V(y, z)$ is
a *translation table* $x \star y = x + 1 + \kappa(y)$, with $\kappa$ a
permutation fixing 0.

*Proof idea.* Putting $z = 0$ gives $x \star \sigma(y) = (x \star y) + 1$ with
$\sigma(y) = V(y, 0)$. Iterating $\sigma$ from 0 therefore adds one each time,
so it visits every element exactly once, and $\kappa$ counts the steps. ∎

**Theorem 8.3** (the W-family) *[PROVEN — Lean: `w_family_models`,
`w_family_model_of_root`]*. For every term $W(z)$ in one variable, the
anchored models of
$$(x \star y) \star z = x \star (y \star W(z))$$
are exactly the affine tables with $a \cdot c_W(a) \equiv 1 \pmod N$, where
$c_W(a) = \sum_{\text{leaves}} a^{\text{(right depth)}}$. The polynomials
$c_W$ that occur are exactly the polynomials with non-negative integer
coefficients, constant term 1 and no gaps *[PROVEN — written]*.

For the right comb $W = z(z(\cdots z))$ with $n$ leaves the condition is that
the $n$-bonacci polynomial $t^n - t^{n-1} - \cdots - 1$ has a root modulo $N$:
the golden law of Chapter 7 is $n = 2$, and $n = 3$ gives a "tribonacci law"
whose spectrum $1, 2, 7, 11, 13, 14, 17, \ldots$ is not in the OEIS. For the
left comb with $k+1$ leaves the condition is $k a^2 + a - 1 \equiv 0$, of
discriminant $1 + 4k$. The theorem was tested before it was proved: for all
23 terms with at most five leaves and all $N \le 9$, the number of models
equals the number of roots (EXP-C13-03).

## Finite spectra, proved by machine

Chapter 7 conjectured that seventeen laws have spectrum exactly $\{1, 3\}$ or
$\{1, 2\}$ (CLM-C06-10). All seventeen agree with the conjecture for every
$N \le 12$ (EXP-C13-04).

**Theorem 8.4** *[PROVEN — Lean: `law13_size_dvd_three`,
`law12_size_dvd_two`]*. The laws $x(yz) = ((zx)x)y$ and $x(yz) = ((xy)z)x$ have
spectra exactly $\{1, 3\}$ and $\{1, 2\}$.

*Proof idea for the first.* With $x = 0$ the law says
$0 \star (y \star z) = (z + 2) \star y$, and with $y = 0$ as well,
$0 \star (0 \star z) = z + 3$. Together:
$w \star y = (w - 2) \star (y - 2) + 3$. Walking $N/2$ steps around an even
cycle gives $N/2 \equiv 0$, impossible; for odd $N$ the walk shows that the
table is affine with $a = 1/2$, and then the law forces $3 \equiv 0$. ∎

Such arguments have a common shape — instances of the law at small elements,
the anchor, and the fact that the table is a function — and they can be
automated.

**Theorem 8.5** *[PROVEN — written; computer-assisted applications]*. The
*offset closure* procedure of the laboratory, which records equalities of the
form "entry = element + integer" and merges them, is sound: whenever it
derives $N \mid g$, every anchored model has size dividing $g$.

Combined with the affine models, it proves the exact spectrum of **16 of the 17
laws** of the conjecture in milliseconds each (EXP-C13-08); the seventeenth,
$x(yz) = y((yx)z)$, is the one law with a non-affine model (at $N = 2$), and
it remains supported only up to $N = 12$.

## A bold hypothesis fails: spectra are not closed under divisors

Every spectrum seen in Chapter 7 was closed under divisors, and so are all
affine spectra (Theorem 8.1). *H-C13-1* conjectured that this always holds.

**Theorem 8.6** *[PROVEN — Lean: `cube_law_no_two`, `cubeOp_model`]*. The
one-variable law $x = x \star (x \star (x \star x))$ has anchored models of
every size except 2. In particular it has a model of size 4 but none of size 2.

*Proof.* At $N = 2$ the anchor forces $0 \star 0 = 1$, and neither choice of
$0 \star 1$ returns 0 after three steps. For $N \ge 3$ let
$0 \star 1 = 2$, $0 \star 2 = 0$ and $x \star x = x$ for $x \ne 0$. ∎

Divisor-closure fails often. Among all 253 one-variable laws with at most five
leaves per side, 24 violate it for $N \le 12$, with spectra missing exactly
$\{2\}$, $\{3\}$ or $\{2, 3\}$ (EXP-C13-07); the searches over two- and
three-variable laws find many more (EXP-C13-05, EXP-C13-06). The same survey
refutes a second guess, that one-variable laws have either only the trivial
model or models of all large sizes: $x = (xx)x$ has spectrum exactly
$\{1, 2\}$.

What *is* true is the weaker structure: spectra are closed under coprime
products (Theorem 7.8), and divisor-closed whenever the law is affinely rigid.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C13-01 | affine spectra of 94,206 laws | 27 + 125 spectra; finite ones are $\mathrm{Div}(L)$; classical sets |
| EXP-C13-02 | are infinite affine classes rigid? | 198 of 199 laws have non-affine models (H-C13-2 refuted) |
| EXP-C13-03 | the W-family | 23 terms, $N \le 9$: model counts = root counts |
| EXP-C13-04 | the 17 laws of CLM-C06-10 | spectra agree for $N \le 12$ |
| EXP-C13-05 | divisor-closure, 2-variable laws | see the cycle record |
| EXP-C13-06 | divisor-closure, 3-variable laws and pairs | see the cycle record |
| EXP-C13-07 | one-variable laws | 24 of 253 violate divisor-closure |
| EXP-C13-08 | offset-closure proofs | 16 of 17 conjectured spectra proved |

## Comparison with existing mathematics

The arithmetic sets of the atlas are classical: they are the sets of moduli
where a polynomial has a root, or equivalently (for quadratics) the numbers
primitively represented by a binary quadratic form, and their OEIS entries say
so. What we did not find in the literature is their appearance as spectra of
single magma laws with a successor anchor, nor the W-family theorem. The
reduction of identities to polynomial conditions on the coefficients of
affine (linear) models is the classical method of linear representations of
quasigroups and medial magmas; here the anchor removes all freedom except one
parameter. Laws whose finite models are counted or constrained by sizes are
studied in universal algebra as *spectra of varieties*; our anchored spectra
are a variant with a distinguished successor, and we make no claim about the
general spectrum problem.

## Applications and limitations

No application is claimed. The atlas covers laws with at most four leaves (three
variables) or five leaves (two variables); the rigidity and divisor-closure
searches cover sizes up to 8–12 only; the offset-closure prover is sound but
incomplete.

## Open questions

1. Prove the spectrum $\{1, 2\}$ of $x(yz) = y((yx)z)$, the last case of
   CLM-C06-10.
2. Which arithmetic sets are *true* spectra of rigid laws? Can "$-1$ is a
   square modulo $N$" be realised by a rigid law?
3. Is every spectrum of a one-variable law finite or cofinite?
4. Are there laws besides left-distributivity whose spectrum is infinite but
   of density zero and comes from non-affine models?
