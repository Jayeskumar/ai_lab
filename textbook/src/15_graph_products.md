# Multiplying graphs {#ch-graph-products}

*Volume 5 — Mathematical transformations and relationships. Research cycle C14.*

## Motivation

Volume 1 obtained numbers as what survives transformations of words. Here the
roles are reversed: the *objects* are relational structures — graphs — and we
ask which ways of combining two graphs into one deserve to be called a
multiplication. Only one kind of information is allowed: whether two vertices
are equal, adjacent or neither. If graphs are to behave like quantities, the
multiplication should be associative, perhaps commutative, have a unit, and
admit invariants that turn it into ordinary multiplication of numbers.

## Definitions

For vertices $x, y$ of a graph $G$ let $\mathrm{rel}_G(x,y)$ be $E$ (equal),
$A$ (adjacent) or $N$ (distinct and non-adjacent). A **local product** $G * H$
has vertex set $V(G) \times V(H)$; two distinct vertices $(g,h), (g',h')$ are
adjacent iff the pair $(\mathrm{rel}_G(g,g'), \mathrm{rel}_H(h,h'))$ lies in a
fixed set $S$ of *cells*. There are eight cells besides $(E, E)$, hence
$2^8 = 256$ local products. Familiar ones:

| product | cells $S$ |
|---|---|
| Cartesian $\square$ | $EA, AE$ |
| direct $\times$ | $AA$ |
| strong $\boxtimes$ | $EA, AE, AA$ |
| lexicographic $G[H]$ | $EA, AE, AA, AN$ |
| co-normal $\vee$ | $EA, AE, AA, AN, NA$ |
| symmetric difference $\oplus$ | $EA, AE, AN, NA$ |

The symmetric difference joins $(g,h)$ and $(g',h')$ when exactly one of
$g \sim g'$, $h \sim h'$ holds (Harary–Wilcox 1967). The *Seidel matrix* of $G$
is $S(G) = J - I - 2A(G)$; *switching* $G$ with respect to a vertex set $Z$
toggles all adjacencies between $Z$ and its complement, and the
switching classes are the *two-graphs*.

## Associativity is a finite fact

The relation of two vertices of $G * H$ is a function $\varphi_S$ of the
relations in the factors. Hence:

**Theorem 15.1** *[PROVEN — Lean: `assoc_iso`, `assoc_of_P3`]*. The canonical
map $((g,h),k) \mapsto (g,(h,k))$ is an isomorphism
$(G*H)*K \to G*(H*K)$ for all graphs iff
$\varphi_S(\varphi_S(r_1,r_2),r_3) = \varphi_S(r_1,\varphi_S(r_2,r_3))$ for all
relations $r_i$ — and already the path $P_3$ (taken three times) detects every
failure, because it contains pairs in all three relations.

**Theorem 15.2** *[PROVEN — Lean kernel computation; REDISCOVERY: Imrich–Izbicki
1975]*. Exactly 20 of the 256 local products are associative. Ten of them are
commutative: the empty and complete products, Cartesian, direct, strong,
co-normal, symmetric difference, and three "complement-duals"
$G *' H = \overline{\overline{G} * \overline{H}}$. Exactly eight have a unit
(necessarily $K_1$): Cartesian, strong, lexicographic and its mirror image,
co-normal, symmetric difference and two complement-duals.

Imrich and Izbicki proved the count of twenty in 1975; Nowakowski and Rall
(1996) noted that ten depend on both factors and eight of those are
commutative — exactly what our computation shows.

*A bold hypothesis that survived.* We expected that some product might be
associative only *up to isomorphism*, through a cleverer identification than
the canonical map. It is not so:

**Theorem 15.3** *[PROVEN — computer-assisted]*. A local product is associative
(commutative) up to isomorphism iff it is strictly associative (has a
symmetric cell set). For every one of the 236 non-associative and 224
non-commutative products, factors with at most three vertices give products
with different degree sequences (EXP-C14-02).

## Graphs become numbers: characters

For constants $c = (c_E, c_A, c_N)$ put
$M_c(G) = c_E I + c_A A + c_N (J - I - A)$.

**Theorem 15.4** *[PROVEN — written, sympy and Lean; POTENTIALLY NOVEL (small)]*.
$M_c(G * H) = M_c(G) \otimes M_c(H)$ for all graphs (with $c_A \ne c_N$) for
exactly six products:

| product | $M_c(G)$ |
|---|---|
| direct | $A$ |
| strong | $I + A$ |
| co-normal | $J - A$ |
| symmetric difference | $J - 2A = S(G) + I$ |
| two complement-duals | $J - I - A$, $\;I - S(G)$ |

**Theorem 15.5** *[PROVEN — written]*. $M_c(G*H) = M_c(G) \otimes I + I \otimes
M_c(H)$ holds exactly for the Cartesian product ($M = A$) and its
complement-dual. Consequently every commutative associative local product
except the empty and complete ones is "linear": a fixed combination of $I$,
$A$ and $J$ turns it into the Kronecker product or the Kronecker sum.

So each of these products carries a **spectral quantity**: the eigenvalues of
$M_c$ multiply (or add) under the product, and $\det M_c$, the traces of powers
of $M_c$, and the characteristic polynomial become homomorphisms into ordinary
arithmetic.

**Theorem 15.6** *[PROVEN — written; Lean (entry level): `xor_character`;
REDISCOVERY — Abiad, Butler and Haemers 2018]*. For all graphs,
$$S(G \oplus H) + I = \bigl(S(G) + I\bigr) \otimes \bigl(S(H) + I\bigr).$$
Hence the Seidel eigenvalues of $G \oplus H$ are $(\theta+1)(\eta+1) - 1$, and
$\oplus$ is compatible with switching: it is a multiplication of two-graphs.

The proof is one line — $(-1)^{a \oplus b} = (-1)^a (-1)^b$ — but it changes how
one should think about $\oplus$: it only half-sees graphs.

**Theorem 15.7** *[PROVEN — written; (b) is a REDISCOVERY: Oh, Yoo and Yun
2013]*. (a)
$K_{a,b} \oplus K_{c,d} \cong K_{ac+bd,\,ad+bc}$: on complete bipartite graphs
the order and the *imbalance* $|a - b|$ simply multiply, like the two
components of a split-complex number. (b) $K_2 \oplus X \cong K_2 \oplus Y$ iff
$X$ and $Y$ are switching-equivalent.

Part (b) is a theorem of Oh, Yoo and Yun (SIAM J. Discrete Math. 27, 2013),
whose *rainbow graph* of $G$ is $K_2 \oplus G$; only the multiplication rule (a)
was not found in the literature.

## A bold hypothesis that failed

For the Cartesian and strong products every connected graph factors uniquely
into prime graphs (Sabidussi–Vizing; Dörfler–Imrich, McKenzie). We conjectured
(H-C14-3) the same for all six commutative products with a unit, on connected
graphs.

*Refutation.* By Theorem 15.7(b), $K_2$ cannot tell a graph from its switched
versions. The 4-cycle $C_4 = K_2 \oplus K_2$ and the claw $K_{1,3}$ are
switching-equivalent, so
$$K_2 \oplus K_2 \oplus K_2 \;\cong\; K_2 \oplus K_{1,3},$$
two different factorisations of a connected graph on 8 vertices into connected
primes (Theorem 8 of the C14 proofs; an explicit isomorphism is in
EXP-C14-06). Among all graphs uniqueness fails already for
$C_4 = K_2 \oplus K_2 = K_2 \oplus 2K_1$, and Theorem 15.7(a) produces
collisions such as $3K_1 \oplus K_{2,3} \cong K_{1,2} \oplus K_{1,4}$
($(3,3)(5,1) = (3,1)(5,3)$ in (order, imbalance) coordinates).

The failure points to the right setting:

**Conjecture 15.8** *[COMPUTATIONALLY SUPPORTED; POTENTIALLY NOVEL]*. Two-graphs
form a free commutative monoid under $\oplus$: every switching class factors
uniquely into prime switching classes. (No collision among all factorisations
up to order 16; EXP-C14-05.)

**Conjecture 15.9** *[COMPUTATIONALLY SUPPORTED]*. The complement-dual of
$\oplus$ (cells $EA, AE, AA, NN$) has unique factorisation on connected graphs —
equivalently $\oplus$ on graphs with connected complement (no collision up to
order 15).

## Counting primes

**Theorem 15.10** *[PROVEN — written, from the published theorems;
REDISCOVERY]*. The Cartesian and the strong product make the set of all finite
graphs into isomorphic graded monoids: both are the multiplicative monoid of a
polynomial semiring $\mathbb{N}[X]$ in their connected primes, and the two
prime sets have the same size in every order. Our census reproduces the
connected Cartesian prime counts $1, 2, 5, 21, 110, 853, 11111, \ldots$
(OEIS A129582, Ji Li 2007) up to 15 vertices — for the strong product too.

Counting primes over *all* graphs gives sequences we did not find in the OEIS
(Theorem 10 of the C14 proofs):

| product | primes of order 2, 3, …, 9 |
|---|---|
| Cartesian, strong, co-normal | 2, 4, 8, 34, 148, 1044, 12326, 274658 |
| symmetric difference | 2, 4, 9, 34, 150, 1044, 12333, 274658 |
| lexicographic | 2, 4, 7, 34, 142, 1044, 12310, 274652 |

The lexicographic product loses uniqueness at order 10:
$2K_1[C_4 + K_1] \cong (2K_2 + K_1)[2K_1] \cong 2C_4 + 2K_1$ — in line with
Imrich's theorem that lexicographic factorisations are not unique although
the number of factors is.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C14-01 | which products are associative, commutative, unital? | 20 / 10 / 8; 0 disagreements with graph-level checks |
| EXP-C14-02 | is "up to isomorphism" weaker? | no: 460 witnesses with ≤ 3-vertex factors |
| EXP-C14-03 | which products have characters? | 6 multiplicative, 2 additive |
| EXP-C14-04 | factorisation census, orders ≤ 15 | $\oplus$ collides from order 4; A129582 reproduced |
| EXP-C14-05 | two-graphs under $\oplus$ | no collision up to order 16 |
| EXP-C14-06 | independent re-implementation | everything reproduced |
| EXP-C14-07 | spectra from factors vs. direct | error $\le 10^{-14}$, orders of magnitude faster |

## Comparison with existing mathematics

The twenty associative products (Imrich–Izbicki 1975), the unique
factorisation theorems for the Cartesian and strong products, the
non-uniqueness for the lexicographic product, the semiring view of
disconnected graphs and the prime counts A129582 are all in the literature,
and the chapter rediscovers them. So is Theorem 15.6: Abiad, Butler and
Haemers (arXiv:1801.01149, 2018, §5) define the same product and state that
its Seidel matrix is $(S_1 + I) \otimes (S_2 + I) - I$, using its
compatibility with switching. Our four literature searches missed the paper;
the Skeptic found it. We found no source for the classification of products
by characters (Theorems 15.4–15.5), for Theorem 15.7, or for the
factorisation behaviour of two-graphs; these are small results and could well
be known to specialists.

## Applications and limitations

* The spectrum of a large product follows from its factors: for
  $n = m = 40$ (1600 vertices) the factor route agreed with direct
  diagonalisation to $10^{-14}$ and was about three orders of magnitude faster
  (our first measurement, four to five orders, was inflated by competing BLAS
  threads on a loaded machine — a correction by the Skeptic) — the standard
  Kronecker gain, newly applicable to $\oplus$.
* Squaring the regular two-graph on 6 points with $\oplus$ gives 36
  equiangular lines in $\mathbb{R}^{18}$ at angle $\arccos(1/5)$ — no
  improvement, since 36 such lines already exist in $\mathbb{R}^{15}$.
* The factorisation censuses are exhaustive only up to 15 (graphs) and 16
  (two-graphs) vertices.

## Open questions

1. Are two-graphs a free commutative monoid under $\oplus$ (Conjecture 15.8)?
2. Does the complement-dual of $\oplus$ factor uniquely on connected graphs
   (Conjecture 15.9)?
3. Which graphs $G$ satisfy $G \oplus X \cong G \oplus X'$ for all switchings
   $X'$ of $X$? ($K_{a,a}$ do.)
4. Is there a character theory for directed graphs, or for graphs with loops,
   where the direct product acquires a unit?
