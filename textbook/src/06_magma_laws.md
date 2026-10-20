# Which sizes can a single law allow? Spectra of magma identities {#ch-magma-laws}

*Volume 2 — Invented operations and their properties. Research cycle C05.*

## Motivation

The barest invented operation is a *magma*: a set and a multiplication table,
with no laws at all. Impose a single equation, say $x = y(x(xy))$, and most
tables are cut away. This chapter asks the simplest question one can put to
such a law: for which sizes $n$ does *any* table satisfy it? There are no
numbers in the definition, yet the answers are pieces of arithmetic —
congruences modulo 3 and 4, single forbidden sizes, long gaps, as in triple
systems and Euler's 36 officers. We found these patterns before learning that
the Equational Theories Project (ETP) had studied such laws in 2024–25, so the
census is a rediscovery; we then pushed into the sizes its notes leave open.

## Definitions

A *magma* $(M, \ast)$ of *order* $n = |M|$ is given by its Cayley table; we
write $xy$ for $x \ast y$. A *law* is an identity $x = t$, where $t$ is a
term in the variables $x, y$; its *order* is the number of multiplications in
$t$. The *spectrum* of a law is the set of $n \ge 1$ for which some magma of
order $n$ satisfies it for all values of the variables. Numbers such as
"law 167" refer to the ETP's list of equations.

A law is *nontrivial* if $x$ occurs in $t$ but is neither its leftmost nor
its rightmost leaf. Otherwise only $n = 1$ works ($x$ absent: every element
equals $t(y)$), or a projection $ab = a$ or $ab = b$ is a model of every
order. A law and its *mirror* ($t$ read right to left) have the same
spectrum, via the opposite table $a \ast' b = b \ast a$. A *quasigroup* is a
magma whose table is a Latin square. An *affine* model over $\mathbb{Z}/n$ is a table
$xy = ax + by + c$. We write spectra on $n = 1, 2, \ldots$ as strings:
1 = a model exists, 0 = none, ? = undecided within the solver budget.

Model existence is decided by SAT: one variable per table entry and value,
plus one per subterm, assignment of $x, y$ and value. The encoding is exact
(`proofs/paper/C05.md`) and matches brute force on all magmas of orders 2, 3.

## The census

**Observation 6.1** *[COMPUTATIONALLY SUPPORTED; REDISCOVERY: Equational
Theories Project]*. There are 115 nontrivial laws $x = t(x, y)$ of order 2–4
(2, 15 and 98 of orders 2, 3 and 4). Of these, 52 have models of every order
$n \le 6$; 2 have none of any order $2 \le n \le 6$; and 61 have a restricted
spectrum. Mirror pairs always agree. Extended to $n \le 8$, the 63 non-full
laws fall into 15 patterns:

| pattern, $n = 1..8$ | laws | example (ETP number) | what is known |
|---|---|---|---|
| 10111011 | 16 | $x = y(x(xy))$ (63), $x = y((xx)y)$ (115) | 115: conjectured all $n \ne 2, 6$ |
| 10110010 | 4 | $x = y(x(yy))$ (66) | $n \equiv 0, 1 \pmod 3$, $n \ne 6$ (Mendelsohn) |
| 10011??1 | 1 | $x = (yx)(xy)$ (167) | $n \equiv 0, 1 \pmod 4$ (Theorem 6.2, which also settles the two ? as absent) |
| 11011011 | 8 | $x = y((xy)(yy))$ (883) | contains $n \equiv 1, 2 \pmod 3$ |
| 10001011 | 8 | $x = y(x(x(yy)))$ (467) | open |
| 1000101? | 4 | $x = y(x((yx)y))$ (677), $x = y(((yx)x)y)$ (1313) | open; up to 10 exactly the orders 1, 5, 7, 9 (Theorem 6.11), and 16 occurs (Theorem 6.10), so Conjecture 6.6 is refuted |
| 10001000 | 2 | $x = y((x(xy))y)$ (1076) | open |
| 1010001? | 2 | $x = y((yx)(xy))$ (907) | open; known sizes 1, 3, 7, 9, 13 |
| 10011001 | 2 | $x = y(y(x(xy)))$ (501) | open |
| 10011011 | 2 | $x = y((y(xx))y)$ (1110) | open |
| 100110?? | 2 | $x = y(x((xy)y))$ (670) | open |
| 10110011 | 2 | $x = y((x(yx))y)$ (1083) | open |
| 10101111 | 4 | $x = y(x(y(xy)))$ (474) | all $n \ne 2, 4$ |
| 10111111 | 4 | $x = (yx)((xy)y)$ (1685) | all $n \ne 2$ |
| 1000001? | 2 | $x = y(((xy)x)y)$ (1286) | open; smallest nontrivial model has order 7 |

The last column comes from the ETP sources under *Comparison*; our data
agree with every size stated there. The 16 Dupont-type laws have one model up
to isomorphism at each of $n = 3, 4, 5$, always a medial quasigroup; the
order-3 model of law 907 is the Steiner quasigroup; law 167 has 58 models of
order 4 up to isomorphism, not all quasigroups. The census's non-existence
answers are SAT results that we did not certify further.

## A law that counts modulo 4

**Theorem 6.2** *[PROVEN — Lean: `law167_card_mod_four`; REDISCOVERY:
Equational Theories Project]*. Every finite magma satisfying
$x = (yx)(xy)$ has order $n \equiv 0$ or $1 \pmod 4$.

*Proof.* Send an unordered pair $\{a, b\}$ to $F\{a, b\} = \{ab, ba\}$.
The law gives $(ab)(ba) = b$ and $(ba)(ab) = a$, so $F$ is an involution. If
$a \ne b$ then $ab \ne ba$, since otherwise $F(F\{a,b\})$ would be a single
element. So $F$ permutes the $\binom n2$ pairs of distinct elements. It fixes
none of them: $\{ab, ba\} = \{a, b\}$ forces $a = b$ through the law in both
possible cases. A fixed-point-free involution on a finite set has an even
number of points, so $4 \mid n(n-1)$. ∎

Lean follows this argument via Mathlib's `Sym2` and its fixed-point
congruence for maps of prime-power order, and checks models of orders 4, 5
(`T4_law167`, `T5_law167`) and the absence of order 2 (`no_law167_order2`).
The converse is the ETP write-up's construction: pair up the two-element
subsets as $\{a, b\}, \{c, d\}$ and set $ab = c$, $ba = d$, $cd = b$,
$dc = a$, $xx = x$. So the spectrum is exactly $\{n \equiv 0, 1 \pmod 4\}$.

## Pushing the open cases

**Theorem 6.3** *[PROVEN — Lean: `left_mul_bijective_of_law`; REDISCOVERY
(standard)]*. If a finite magma satisfies $x = y\,s(x, y)$ for some term
$s$, every left translation $a \mapsto ya$ is a bijection: each row of the
table is a permutation.

*Proof.* $y \cdot s(x, y) = x$ shows that $a \mapsto ya$ is onto, and an
onto map from a finite set to itself is one-to-one. ∎

Theorem 6.3, and fixing $0 \ast 0 \in \{0, 1\}$ (relabelling always allows
it), are *sound* extra constraints for the solver. With them we decided the
15 laws of unknown spectrum in the ETP notes for all $n \le 10$ but a few
UNKNOWN sizes, with no disagreement with any size stated in the notes. What
is new relative to the notes:

**Theorem 6.4** *[PROVEN — Lean `decide` certificates; POTENTIALLY NOVEL
relative to the ETP notes]*. Law 677, $x = y(x((yx)y))$, has models of
orders 5, 7 and 9. Laws 1286, $x = y(((xy)x)y)$; 1313, $x = y(((yx)x)y)$;
and 1516, $x = (yy)(x(xy))$, each have a model of order 9.

*Proof.* We give explicit Cayley tables found by SAT. Lean's kernel checks
each law on each table (`E677_order5_law`, `E677_order7_law`,
`E677_order9_law`, `E1286_order9_law`, `E1313_order9_law`,
`E1516_order9_law`). ∎

The same pipeline certified an order-9 model of law 467. That size is *not*
new: the notes construct models of 467 on $\mathbb{Z}[i]/(k + il)$ whenever
$k^2 + l^2$ is odd, and $9 = 3^2 + 0^2$. We first missed this and recorded
it as new; a second reading corrected it.

**Theorem 6.5** *[PROVEN — computer-assisted, drat-trim-verified; POTENTIALLY
NOVEL for $n \ge 5$]*. The following laws have no model of the given orders:
law 501, $x = y(y(x(xy)))$, orders 6 and 7; law 677, order 6;
law 883, $x = y((xy)(yy))$, order 6; law 1076, $x = y((x(xy))y)$, order 8;
law 1083, $x = y((x(yx))y)$, orders 5 and 6. The same holds for 501 at
order 3 and 677 at orders 3 and 4. These are new relative to the notes but
small enough that ETP searches probably settle them.

*Proof.* For each case Glucose 4 logs a DRUP refutation of the CNF formula,
and the independent checker drat-trim verifies it (all 48 frontier
refutations passed). What remains trusted is drat-trim, the CNF generator and
the soundness of the two extra constraints. ∎

**Conjecture 6.6** *[REFUTED — by the Skeptic's review; see Theorem 6.10]*.
"Laws 677 and 1313 both have spectrum $\{1\} \cup \{n \text{ odd} : n \ge 5\}$."

Both laws have models of orders 5, 7, 9 and none of orders 2, 3, 4, 6, all
certified except orders 5 and 7 of law 1313 (stated in the notes, found again
by SAT, tables re-checked). Orders 8 and 10 were undecided; the order-5 models
are idempotent quasigroups. The first version of this book stated the
conjecture on this evidence. It is false: both laws have models of order 16
(Theorem 6.10). The evidence was too thin — four odd sizes and four small
gaps say little about larger even sizes — and the search space had a blind
spot: the lab looked for affine models only over $\mathbb{Z}_n$, whose
additive group is cyclic, never over the fields $\mathrm{GF}(2^k)$.

## Three bold hypotheses fail

**Hypothesis 6.7 (H-C05-1)** *[REFUTED]*. "A single law $x = t$ has spectrum
$\{1\}$ or all of $\mathbb{N}$: one identity cannot restrict sizes." Law 167
is a counterexample (Theorem 6.2), and 61 of the 115 census laws are others.

**Hypothesis 6.8 (H-C05-Q)** *[REFUTED]*. "Every nontrivial law forces its
finite models to be quasigroups." Counterexample: this model of law 167, whose
row 1 repeats the value 2 (`T4_law167`, `T4_not_latin`):

| $\ast$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **0** | 0 | 3 | 1 | 0 |
| **1** | 0 | 2 | 2 | 2 |
| **2** | 2 | 0 | 1 | 3 |
| **3** | 1 | 3 | 1 | 3 |

Eighteen census laws already have non-quasigroup models of order at most 3.

**Hypothesis 6.9 (H-C05-A)** *[REFUTED]*. "A law has models of every order
$n \le 6$ iff it has an affine model over every $\mathbb{Z}/n$, $n \le 6$."
Counterexample: $x = (yx)(x(yy))$. It has models of every order up to 6, and
of order 2 it is satisfied by NAND, $xy = \lnot(x \land y)$:
$yy = \lnot y$, $x(yy) = \lnot x \lor y$, $yx = \lnot x \lor \lnot y$, so
$(yx)(x(yy)) = \lnot\big((\lnot x \lor \lnot y) \land (\lnot x \lor y)\big) = x$
(`nand2_law`). Yet no affine operation over $\mathbb{Z}/2$ satisfies it
(`no_affine_model_mod2`); for $n \le 6$ its affine models exist only at
$n = 1$ and $n = 5$. Three more laws (two mirror pairs in all) behave the same
way, and in 39 restricted laws some sizes of the spectrum have no affine model.

## After the review: linear models over finite fields

The Skeptic found the counterexample to Conjecture 6.6 by looking at linear
operations over a field with 16 elements. We then searched every prime power
$q \le 128$ systematically (EXP-C05-07). For $x \ast y = ax + by$ a term
$t(x, y)$ evaluates to $\alpha x + \beta y$, where $\alpha$ and $\beta$ are
polynomials in $a$ and $b$; the law $x = t$ holds exactly when $\alpha = 1$ and
$\beta = 0$ in $\mathrm{GF}(q)$.

**Theorem 6.10** *[PROVEN — computer-assisted, three tables Lean-checked;
NOT ASSESSED: linear models are a standard tool of the ETP]*. For the 15 open
laws of this chapter, the prime powers $q \le 128$ admitting a linear model
over $\mathrm{GF}(q)$ are those listed in EXP-C05-07. In particular:

* laws 677 and 1313 have models of order 16 — e.g. $x \ast y = (1 + t^3)x + t^3 y$
  for 677 and $x \ast y = t^3 x + (1 + t^3) y$ for 1313, in
  $\mathrm{GF}(16) = \mathrm{GF}(2)[t]/(t^4 + t + 1)$ (the Skeptic's
  examples); our search finds other pairs $(a, b)$ as well;
* laws 670, 1076 and 1286 also have models of order 16, and 1286 one of
  order 32;
* law 670 has a model of order 9, a size the SAT search had left UNKNOWN;
* no linear model exists at any order that the SAT search, the DRUP
  certificates or the ETP notes exclude (0 conflicts).

*Proof.* The search is exhaustive over $\mathrm{GF}(q)^2$, and
$\mathrm{GF}(q)$ is unique up to isomorphism, so "no linear model of order
$q$" does not depend on the representation. One model per law and order was
re-checked on its full table (the Skeptic's independent computation re-checked
all of them, with a different representation of the fields), and Lean's kernel
checks the tables `E677_order16_law`,
`E1313_order16_law` and `E670_order9_law`. ∎

Because direct products of models are models, the spectra of 677 and 1313
now contain every product of the orders 5, 7, 9, 16, … — including all
$16 \cdot m$ with $m$ in the spectrum. Which even orders below 16 occur was
left open; the next section settles 8 and 10.

## Orders 8 and 10 (version 1.1)

A direct SAT search with Latin rows and the symmetry break $0 \star 0 \in
\{0, 1\}$ (EXP-C05-03) could not decide the two laws at $n = 8$ and $10$. Two
observations make the search small enough to finish *and* to certify.

**Lemma 6.11a** *[PROVEN — Lean: `C05_Law1313.lean`]*. Every finite model of
law 1313 is a quasigroup. *Proof.* Rows are permutations because the law has
the form $x = y \star T$. Given $w$, put $x = y \star w$; the law gives
$y \star T = y \star w$ with $T = ((y \star x) \star x) \star y$, so $T = w$ and
the column of $y$ takes the value $w$. ∎ For 677 only the rows are known to be
permutations; finite models of 677 that are not right-cancellative exist (ETP
blueprint), so no column constraint may be used there.

*A case split guided by the hard cases.* Relabel so that some element is 0
and row 0 is a fixed permutation of a given cycle type. A first split on the
cycle type alone left 41 of the 97 order-10 cases of 677 undecided at 300,000
conflicts each — almost all of them cases where 0 is idempotent. So we split
first on idempotency: either every element is idempotent, or 0 can be chosen
non-idempotent; in both cases 0 is chosen with the fewest fixed points in its
row (among the non-idempotent elements in the second case), which gives every
competing row at least as many fixed points. Implied "division" clauses (if
$y \star a = x$ then the inner term $T$ equals $a$) shorten the search further.
The split is complete (Lemma 8 of `proofs/paper/C05.md`): 45 cases for $n = 8$
and 97 for $n = 10$.

**Theorem 6.11** *[PROVEN — computer-assisted; 677 at order 8: REDISCOVERY
(Mace4, ETP paper); the rest POTENTIALLY NOVEL]*. Neither law 677 nor law 1313
has a model of order 8 or 10. Consequently the orders $n \le 10$ of their
models are exactly 1, 5, 7 and 9, for both laws.

*Proof.* All 284 case CNFs are unsatisfiable (EXP-C05-08). Each refutation is a
DRAT proof from CaDiCaL that drat-trim verified — 40.5 million proof lines in
all, the hardest case of 677 needing 1.33 million conflicts. The same pipeline
finds models at orders 5 and 7 and none at 6, as the direct search did. ∎

Law 677 matters beyond this chapter: whether it implies $x = ((x \star x) \star
x) \star x$ (law 255) in finite magmas is the last implication between laws of
order at most 4 that the Equational Theories Project could not settle. A
finite counterexample would have to be a model of 677, so Theorem 6.11 rules
out orders 8 and 10 — a small, certified data point, nothing more.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C05-01 | spectra ($n \le 6$) of the 115 nontrivial laws | 52 full, 2 only $n = 1$, 61 restricted; 1 UNKNOWN (law 167 at $n = 6$, settled by Theorem 6.2) |
| EXP-C05-02 | the 63 non-full laws to $n \le 8$; models up to isomorphism for $n \le 5$ | 15 patterns; 52 of 63 have only quasigroup models ($n \le 5$) |
| EXP-C05-03 | the 15 open ETP laws, $n \le 10$ | 0 disagreements with the notes; Theorems 6.4–6.5 |
| EXP-C05-04 | Lean certificates for the models found | 9 of 9 tables checked by the kernel |
| EXP-C05-05 | affine models over $\mathbb{Z}/n$, $n \le 6$ | H-C05-A refuted by 4 laws |
| EXP-C05-06 | DRUP proofs for the gaps | 48 of 48 verified by drat-trim |
| EXP-C05-07 | linear models over $\mathrm{GF}(q)$, $q \le 128$ (after the review) | 0 conflicts; order 16 for laws 677 and 1313 (Theorem 6.10) |
| EXP-C05-08 | 677 and 1313 at orders 8 and 10: complete case split, DRAT proofs (version 1.1) | 284 of 284 case CNFs UNSAT, all proofs verified (Theorem 6.11) |

## Comparison with existing mathematics

*Classical spectra.* Steiner triple systems exist exactly for
$n \equiv 1, 3 \pmod 6$ (Kirkman, 1847). Mendelsohn triple systems exist for
$n \equiv 0, 1 \pmod 3$, $n \ne 6$ (N. S. Mendelsohn, 1971). Pairs of
orthogonal Latin squares exist for all $n \ne 2, 6$ (Bose, Shrikhande and
Parker, 1959–60; Euler's 36 officers). Spectra of quasigroup identities have
a long literature, for example Bennett and Mendelsohn on Stein quasigroups.

*The Equational Theories Project* (T. Tao et al.,
<https://teorth.github.io/equational_theories/>; paper arXiv:2512.07087,
<https://arxiv.org/abs/2512.07087>) settled the implications between the
4694 laws of order at most 4. Two notes on the project's Zulip treat spectra:

* "Spectra of order-3 equations"
  (<https://leanprover.zulipchat.com/user_uploads/3121/C8gCuSGHJXw9lUPe23ouRkVM/Order_3_spectra.pdf>)
  proves that law 66 has the Mendelsohn spectrum and law 167 the spectrum
  $\{0, 1 \bmod 4\}$. B. Le Floch's notes cite "Ben Gunby-Mann's notes" for
  law 167, which we take to be this write-up.
* B. Le Floch, "Spectra of equational laws" (July 10, 2025,
  <https://leanprover.zulipchat.com/user_uploads/3121/apvdoKH3jwd1mrnPxZcvlXL_/spectrum.pdf>)
  lists the 48 laws of order at most 4 that may have a non-full spectrum.
  Of these, 31 have no model of order 2 and 14 have one of order 2 but none of
  order 3. For many of them it gives only "unknown spectrum starting with …".

*Not new here:* Observation 6.1 as a whole; Theorem 6.2 (our addition is the
Lean proof); Theorem 6.3; the Mendelsohn spectrum of law 66; all gaps at
order 2 and law 883's gap at order 3, which the notes list; law 467 at
order 9. *New relative to the notes:* the memberships in Theorem 6.4 and the
gaps in Theorem 6.5, of which those at $n \ge 5$ are the plausible additions.
We retrieved the ETP paper only partly, and its model searches may already
contain these facts, so the novelty is relative to the sources we read. The
three refuted hypotheses were our own.

## Applications and limitations

The reusable output is a certification pipeline for finite algebra: a model
becomes a table checked by Lean's `decide`, a non-existence result a DRUP
proof checked by drat-trim, so neither direction rests on trusting the SAT
solver. Laws such as 66 or 907 also turn a solver into a generator of
triple-system-like designs, a well-known use of quasigroups; we ran no
comparison with dedicated design algorithms.

*Limitations.* Only two-variable laws $x = t$ of order at most 4 were
studied; the census stops at $n \le 6$ ($n \le 8$ and $10$ for subsets); solver
budgets left UNKNOWN entries. **Most non-existence results of the census are
trusted from the solver** — only the 48 frontier instances are independently
checked. An isomorphism-grouping step of EXP-C05-02 compared non-canonical
tables, so its count is not used.

## Open questions

1. Decide laws 677 and 1313 at orders 12 and 14 (8 and 10 are excluded by
   Theorem 6.11, 16 occurs), and law 1286 at orders 8 and 10, with the case
   split of Theorem 6.11.
2. Is the spectrum of law 115 all $n \ne 2, 6$, as the notes conjecture? Our
   data agree up to $n = 8$.
3. Direct products of models are models, so every spectrum is closed under
   multiplication. Which multiplicatively closed sets arise from a single law
   of small order?
4. Which laws admit a finite-order "pair map" like $F$ in Theorem 6.2, and
   which congruences do such maps force?
5. Extend the census to laws of order 5 and to three variables, where the
   central groupoid law (spectrum: the squares, by Knuth) already appears.
