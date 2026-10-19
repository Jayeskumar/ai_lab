# Quasigroups as mixers: an honest negative {#ch-quasigroup-mixing}

*Volume 8 — Optimization and practical applications. Research cycle C18.*

## Motivation

The laboratory invented and studied many finite operations: Latin squares,
the nimber field of Chapter 14, the anchored structures of Chapter 7. A
*quasigroup* — an operation whose every row and column is a permutation — is
the natural candidate for a mixing primitive: Markovski, Gligoroski and
Bakeva's *e-transformation*
$$b_0 = l \star a_0, \qquad b_i = b_{i-1} \star a_i$$
turns a byte string into another one, and iterating it is the core of
published quasigroup hash designs. Can our operations serve as practical
(non-cryptographic) hash functions, measured honestly against standard
baselines? *Nothing in this chapter is a security evaluation.*

## Definitions

We use seven quasigroups of order 256: a random Latin square (built row by row
from random matchings), a random isotope of $\mathbb{Z}/256$, the nimber
inversion quasigroup $(x \oplus y)^{-1}$ (the nim-product itself is not a
quasigroup — its row 0 is zero), an affine operation $77x + 141y + 5$, XOR,
and the anchored quasigroups $x + c(y)$ and $(x + 1) \oplus y$ of Chapter 7.
A *tail hash* QG($T$, $p$, rev) applies $p$ e-transformations to
key ‖ length ‖ padding, optionally one more to the reversed string, and
outputs the last 8 bytes. Baselines: FNV-1a-64, MX64 (multiply-xorshift with
the splitmix64 finaliser), BLAKE2b-64 and CRC32.

## What can be proved in advance

**Theorem 20.1** *[PROVEN — Lean: `eT_injective`, `eT_length`;
REDISCOVERY: Markovski et al. 1999]*. Every e-transformation is a bijection of
strings of a given length; the *d-transformation* $a_i = b_{i-1} \backslash b_i$
inverts it.

**Theorem 20.2** *[PROVEN — Lean: `eT_ne_of_ne`]*. A difference at position
$i$ changes exactly the outputs at positions $\ge i$. So a tail hash without
a reverse pass cannot let a late input byte influence earlier tail bytes: its
maximal avalanche bias is $1/2$.

**Theorem 20.3** *[PROVEN — written; REDISCOVERY: Klimov–Shamir T-functions]*.
If the operation is a T-function — built from $+$, $\times$, $\oplus$ modulo
$2^8$, like the affine and the anchored $(x + 1) \oplus y$ quasigroups — then
no hash built from it can move information from high input bits to low output
bits.

**Theorem 20.4** *[PROVEN — written]*. For XOR the whole hash is affine over
GF(2): output differences do not depend on the key (as for CRC32). For the
anchored $x + c(y)$, differences between runs over the same inputs stay
constant, so its one-pass hash cannot see the order of the message bytes.

## The avalanche test: a misleading success

On 2000 random 16-byte keys, flipping each of the 128 input bits:

| hash | mean bias | max bias | bit independence (max corr.) |
|---|---|---|---|
| BLAKE2b-64 (reference) | 0.0089 | 0.045 | 0.11 |
| MX64 | 0.0090 | 0.045 | 0.11 |
| QG random Latin square, 2 passes + reverse | 0.0089 | 0.041 | 0.11 |
| QG nimber inversion, 2 passes + reverse | 0.0090 | 0.042 | 0.11 |
| QG $x + c(y)$, 2 passes + reverse | 0.0091 | 0.043 | **1.00** |
| QG random Latin square, forward only | 0.090 | **0.5** | 1.00 |
| FNV-1a-64 | 0.098 | **0.5** | 1.00 |
| QG affine / $(x+1) \oplus y$ | 0.39 / 0.34 | 0.5 | 1.00 |
| QG XOR, CRC32 | 0.5 | 0.5 | 1.00 |

The bold hypothesis H-C18-1 — a random Latin square with two passes and a
reverse pass reaches BLAKE2b's avalanche — **holds**. The anchored $x + c(y)$
has ideal per-bit flip rates but perfectly correlated bit changes, exactly as
Theorem 20.4 predicts.

## The distribution test: a collapse, and its theorem

On 65,536 decimal strings, near-duplicate keys and word-like strings, every
reverse-pass quasigroup hash failed badly: up to 2.7 times the expected
collisions in $2^{16}$ buckets and **32,624 identical 64-bit hash values**
among the near-duplicates. The nimber hash, conjectured to be competitive with
FNV-1a (H-C18-3), is **refuted** (chi-square $z = 1084$ on decimal strings).
The explanation is not a bug:

**Theorem 20.5** (tail-information bound) *[PROVEN — Lean core:
`eT_append`, `eT_tail_factors`]*. The last 8 outputs of an e-transformation
are a bijective function of **one state byte** and the last 7 inputs.
Consequently a reverse-pass tail hash gives at most 256 different values to all
keys sharing their first 7 bytes, and a $p$-pass forward hash at most $256^p$
to keys sharing their last 7 bytes.

*Proof idea.* $b_j$ is determined by $b_{j-1}$ and $a_j$, and conversely
$a_j = b_{j-1} \backslash b_j$; the rest of the message enters only through
$b_{n-8}$. ∎

The bound is attained exactly on data (256 values in every one of 100 test
families), and it predicts the observed number of collisions exactly:
$16 \times (2295 - 256) = 32{,}624$. A byte-level e-transformation is a
pipeline with an 8-bit state, however good its avalanche looks — which is why
published quasigroup hashes used enormous quasigroups.

## A repair that works — and does not pay

Theorem 20.5 suggests keeping a full 64-bit state: run eight e-transformations
in parallel and output the final state of each (a *cascade*). Its state update
is a bijection of the 8-byte state (**Theorem 20.6** *[PROVEN — written]*), so
the bound no longer applies.

| hash | max bias | BIC | flagged key sets | MB/s (indicative) |
|---|---|---|---|---|
| cascade, random Latin square | 0.048 | 0.11 | none | 13 |
| cascade, $\mathbb{Z}/256$ isotope | 0.046 | 0.11 | none | 10 |
| cascade, nimber inversion | **0.085** | 0.15 | one marginal | 10 |
| cascade, $x + c(y)$ | **0.116** | 0.18 | none | 9 |
| MX64 | 0.045 | 0.11 | none | 165 |
| BLAKE2b-64 | 0.045 | 0.11 | none | 41 |

The cascades over random-like quasigroups pass every test we ran. The bold
hypothesis that all three random-like cascades would pass (H-C18-8) is
**refuted** by the nimber cascade, whose structure ($x \star x = 0$,
commutativity) leaves a measurable bias.

**Result 20.7** *[COMPUTATIONALLY SUPPORTED — improvement: NO IMPROVEMENT]*.
No quasigroup construction improves significantly on the best baseline in any
measured dimension (some are numerically slightly better on a single
statistic, within noise): the good cascades only match MX64 and BLAKE2b in
quality and are several times slower in the same run. Throughput depends on
machine load — the tail-output variants reached 11–52 MB/s in one run and
20–98 MB/s in the Skeptic's re-run, against 640 and 428 MB/s for
numpy-vectorised FNV-1a and MX64 — but the ordering is stable. Against FNV-1a
alone the good cascades mix better, at a large speed cost. (FNV-1a's
$z = -9.8$ on sequential keys means *more* uniform than random; the first
version of this chapter read it as a defect.)

## Comparison with existing mathematics

The e-transformation and its bijectivity are Markovski, Gligoroski and
Bakeva's (1999); T-functions are Klimov and Shamir's (2002). Quasigroup
hashes submitted to the SHA-3 competition (Edon-R, NaSHA) used huge
quasigroups in wide-pipe designs and were nevertheless attacked. We found no
explicit statement of the byte-level tail-information bound, which is
elementary.

## Applications and limitations

The outcome is negative and is reported as such. Limitations: Python and
numpy implementations on a shared machine (timings indicative); a small subset
of standard hash tests; one random Latin square, not uniformly sampled;
16-byte keys for the avalanche test. None of this is a security evaluation.

## Open questions

1. Do cascades over larger quasigroups (order $2^{16}$), in optimised code,
   become competitive?
2. Which properties of a quasigroup (commutativity, relations such as
   $x \star x = 0$, its isotopy class) leave a bias in cascades?
3. How does the avalanche bias of a cascade over a random Latin square decay
   with its depth?
