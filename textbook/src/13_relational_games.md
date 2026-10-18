# Games defined by relations {#ch-relational-games}

*Volume 5 — Mathematical transformations and relationships. Research cycle C12.*

## Motivation

System D asks for structures in which only *relations* matter. In a one-heap
game a move from $n$ goes to a smaller position, and who wins is decided by the
move relation alone. In Chapter 5 games came from rewriting rules; here the
move relation is an arithmetic relation — *divides*, *is coprime to*, *is a
submask of*, *differs by a square* — and we ask which relations produce
structured values. Nineteen games were solved exactly and compared.

## Definitions

The *Sprague–Grundy value* of a position is
$$g(n) = \operatorname{mex}\{\, g(m) : m \text{ an option of } n \,\},$$
where $\operatorname{mex} A$ is the least natural number not in $A$. Options are
smaller, so $g$ is unique (Lean: `IsGrundy.unique`), and $n$ is a *P-position*
(the player to move loses) iff $g(n) = 0$ (Lean: `IsGrundy.zero_pset`). In a
*splitting game* a heap $n$ is replaced by two nonempty heaps $a + b = n$ with
option value $g(a) \oplus g(b)$ (XOR). By the Sprague–Grundy theorem a sum of
games has the XOR of the values, so a formula for $g$ solves all sums of heaps.

$v_2(n)$ is the exponent of 2 in $n$, $\Omega(n)$ the number of prime factors
with multiplicity, $\operatorname{popcount}(n)$ the number of 1-bits, and $m$
in $n = 2^a m$ ($m$ odd) the *odd part*. A sequence is *eventually
(arithmetic-)periodic* if $g(n + p) = g(n)$ (resp. $g(n) + s$, $s \ne 0$) for
all large $n$.

| game | move from $n$ | relation |
|---|---|---|
| G01, G02 | $n \to n - d$, $d \mid n$, $d < n$ (G02: also $d = n$) | divisibility |
| G03 | $n \to n - d$, $d \mid n$, $1 < d < n$ ("deleting divisors") | divisibility |
| G04 | $n \to d$, $d \mid n$, $d < n$ | divisibility |
| G05, G06 | $n \to m$, $1 \le m < n$, $\gcd(m, n) = 1$ (G06: $> 1$) | coprimality |
| G08–G12 | $n \to n - s$, $s$ a square, Fibonacci number, power of 2, 3 or 4, prime, triangular number | additive sets |
| G13 | $n \to$ a proper binary submask of $n$ | bitwise |
| G16–G18 | split $n = a + b$ with $\gcd(a, b) = 1$, $a \mid b$, or $a \ne b$ (Grundy's game) | splitting |
| G19, G20 | $n \to n \bmod k$ ($1 \le k < n$), $n \to \lfloor n/k \rfloor$ ($2 \le k \le n$) | Euclidean division |

## Arithmetic relations give arithmetic values

**Theorem 13.1** (CLM-C12-01) *[PROVEN — written; REDISCOVERY]*. G01 has
$g(n) = v_2(n)$, G02 has $g(n) = v_2(n) + 1$ (for $n \ge 1$), and G04 has
$g(n) = \Omega(n)$.

*Proof idea.* In G01 let $k = v_2(n)$. The options $n - 2^j$ ($j < k$) have
valuation $j$ and realise every smaller value. No option has valuation $k$: if
$v_2(d) < k$ then $v_2(n - d) = v_2(d)$, and if $v_2(d) = k$ then
$n - d = 2^k(a - b)$ with $a, b$ odd, so the valuation exceeds $k$. G02 adds
the option 0, which shifts every value by one; for G04 a chain of divisors
realises $0, \ldots, \Omega(n) - 1$. ∎

**Theorem 13.2** (CLM-C12-02) *[PROVEN — written; REDISCOVERY]*. In G05,
$g(1) = 0$ and $g(n) = j$ when the smallest prime factor of $n$ is the $j$-th
prime; "subtract $k$ coprime to $n$" is the same game, since
$\gcd(n - m, n) = \gcd(m, n)$. In G06, $g(2k) = k - 1$, $g(m) \le (m - 1)/2$
for odd $m$, and the P-positions $n \ge 1$ are exactly 1 and the primes.

*Proof idea.* In G05 the primes below the smallest prime factor $p_j$ of $n$
are options with values $1, \ldots, j - 1$, and 1 has value 0; an option of value
$j$ would be divisible by $p_j$. In G06 a simultaneous induction proves the even
formula and the odd bound: every odd option of $2k$ shares an odd prime $q$ with
$2k$, so it is at most $2k - 3$ and its value is at most $k - 2$. ∎ We know no
closed form for the odd values of G06; we observed $g(m)/m < 0.24985$ for odd
$m \le 5000$.

**Theorem 13.3** (CLM-C12-05) *[PROVEN — written; REDISCOVERY]*. G13 has
$g(n) = \operatorname{popcount}(n)$; G19 has
$g(n) = \lfloor \log_2((n + 1)/3) \rfloor + 1$ for $n \ge 2$; G20 has
$g(n) = \lfloor \log_2 n \rfloor$ for $n \ge 1$.

*Proof idea.* Proper submasks realise every smaller popcount. The remainders
$n \bmod k$ are exactly the $r$ with $0 \le r < n/2$, so
$g(n) = \operatorname{mex} g([0, \lceil n/2 \rceil))$ and the value $v$ first
appears at $3 \cdot 2^{v-1} - 1$. In G20 the quotients $\lfloor n/2^j \rfloor$
realise every smaller value and every option is at most $n/2$. ∎

## Periodic games and rigid splitting

**Theorem 13.4** (CLM-C12-06) *[PROVEN — Lean: `residue_grundy`,
`power_of_two_grundy`; general $k$ written; REDISCOVERY]*. (a) If no move is
divisible by $q$ and $1, \ldots, q - 1$ are moves, the subtraction game has
$g(n) = n \bmod q$; in particular subtract-a-power-of-2 has $g(n) = n \bmod 3$.
(b) For every $k \ge 2$, subtract-a-power-of-$k$ has the Grundy function of the
finite game $\{1, k\}$: $n \bmod 2$ for odd $k$, and for even $k$ the pattern
$0, 1, 0, 1, \ldots, 1, 2$ of period $k + 1$.

*Proof idea.* $k^i \equiv (-1)^i \pmod{k+1}$, so every move changes the residue
modulo $k + 1$ by $\pm 1$, exactly as the moves 1 and $k$ do; the mex equations
are then checked residue by residue. ∎

**Theorem 13.5** (CLM-C12-07) *[PROVEN — Lean: `split_parity`;
REDISCOVERY]*. In every splitting game in which each heap $n \ge 2$ has at
least one allowed split, $g(n) = 1$ for even $n$ and $g(n) = 0$ for odd $n$:
every play lasts exactly $n - 1$ moves.

So the coprime and dividing splits (G16, G17) are pure parity games; Grundy's
game (G18) escapes only because a heap of size 2 cannot be split.

## Deleting divisors

**Theorem 13.6** (CLM-C12-03) *[PROVEN — Lean: `g03_pset`,
`g03_P_positions`; REDISCOVERY: Codeforces 1537D]*. The P-positions of G03 are
exactly 0, the odd numbers, and the powers $2^{2j+1}$.

*Proof idea.* From odd $n$ every option $n - d$ is even and divisible by the odd
$d \ge 3$, hence neither odd nor a power of 2. An even $n$ with odd part
$m > 1$ moves to the odd number $n - m$. The only power of 2 among the options
of $2^a$ is $2^{a-1}$, so the powers of 2 alternate. ∎

The P-positions do not solve *sums* of heaps; the whole Grundy function does.

**Theorem 13.7** (CLM-C12-04) *[PROVEN — written + computer-assisted; Skeptic
review pending; POTENTIALLY NOVEL]*. Let $n = 2^a m$ with $m$ odd. Then
$g(n) = 0$ for odd $n$, and for $a \ge 1$:

| odd part $m$ | $g(2^a m)$ |
|---|---|
| $m \ge 17$ | $a$ |
| $1$ | $0$ for odd $a$; $a - 1$ for even $a$, except $g(16) = 2$ |
| $3$ | $2, 3, 4, 3, 6$ for $a = 1, \ldots, 5$; $a - 2$ for $a \ge 6$ |
| $5$ | $1, 3, 4, 3, 6$ for $a = 1, \ldots, 5$; $a + 2$ for $a \ge 6$ |
| $7, 9, 11, 15$ | $a$ for $a \le 2$; $a + 1$ for $a \ge 3$ |
| $13$ | $a$ for $a \le 3$; $a + 1$ for $a \ge 4$ |

Consequently $\lvert g(n) - v_2(n) \rvert \le 2$ unless $n$ is an odd power of
2, and the record values occur at $n = 5 \cdot 2^a$ for $a \ge 6$.

*Proof idea.* Call $F$ the tabulated function; we show $g = F$ by strong
induction. Up to $10^5$ the two agree by exact computation. Odd $n$ have value
0 because the zero set of $F$ is the P-set of Theorem 13.6. For odd part
$m \ge 17$ the options $n - 2^j$ realise $0, \ldots, a - 1$; an option with
$v_2 < a$ again has odd part $\ge 17$, and an option $2^a(m - e)$ can only take
the value $a$ when $m \in \{3, 13, 15\}$. For odd part $m \le 15$ (so $a \ge 13$
beyond $10^5$) every option value has the form $a + \delta$ with offsets that
depend only on $m$ and the parity of $a$, so the mex equation needs to be
checked for one exponent of each parity; the certificate checks all $m \le 15$
and $13 \le a \le 100$. ∎ (EXP-C12-06; the written inductive steps have not yet
been reviewed by the Skeptic.)

Compare G01, the same game with the move "subtract 1" allowed, where
$g = v_2$ exactly. Forbidding one move perturbs the Grundy function only on the
odd powers of 2 and on numbers whose odd part is at most 15; up to $10^5$ there
are 96 such exceptions.

## Sparse move sets

**Theorem 13.8** (CLM-C12-08) *[PROVEN — written, from the Furstenberg–Sárközy
theorem; REDISCOVERY]*. For subtract-a-square and subtract-a-triangular-number
the P-positions form an infinite set of natural density 0. Hence neither Grundy
sequence is eventually periodic or eventually arithmetic-periodic.

*Proof idea.* Two P-positions never differ by a move. So the P-set of
subtract-a-square has no two elements differing by a square and has density 0
(Furstenberg 1977, Sárközy 1978); triangular numbers contain the values
$m(2m + 1)$ of a polynomial vanishing at 0, and the polynomial version (Kamae
and Mendès France 1978) applies. A finite P-set would force a tail of
$\mathbb{N}$ into finitely many translates of the move set, which has density 0.
An infinite eventually periodic zero set has positive density, and an
arithmetic-periodic sequence has only finitely many zeros. ∎

The data agree: from $N = 1.25 \cdot 10^4$ to $2 \cdot 10^5$ the P-density falls
$0.0538 \to 0.0222$ (squares) and $0.0344 \to 0.0116$ (triangular), while the
maxima grow $36 \to 95$ and $50 \to 144$. Primes and Fibonacci numbers differ.

**Conjecture 13.9** (CLM-C12-12) *[COMPUTATIONALLY SUPPORTED; REDISCOVERY:
OEIS A014589]*. Subtract-a-prime satisfies $g(n) \le 11$ for all $n$. (Our
check reaches $2 \cdot 10^5$; the OEIS entry records the bound up to $10^9$.)

**Conjecture 13.10** (CLM-C12-13) *[CONJECTURE]*. Subtract-a-Fibonacci-number
has bounded Grundy values (maximum 14 for $n \le 2 \cdot 10^5$; weak support,
since it rose from 13 to 14 between $2.5 \cdot 10^4$ and $5 \cdot 10^4$).

## Hypotheses that failed

*H-C12-1 [REFUTED]* (CLM-C12-10). "In each of the games G01–G06, $g(n)$
depends only on the prime signature of $n$." Already $n = 2$ and $n = 3$
refute it in G01 ($g = 1$ and $0$). The first counterexamples elsewhere are
$(2, 3)$ in G02, $(4, 9)$ in G03, $(2, 3)$ in G05 and $(6, 10)$ in G06 (values
2 and 4). Only G04 depends on the signature alone, as $g = \Omega$ predicts.

*H-C12-2 [REFUTED]* (CLM-C12-11). "Subtraction games whose move sets are the
squares, the triangular numbers, the Fibonacci numbers or the primes keep a
positive density of P-positions." Squares and triangular numbers have density
0 (Theorem 13.8). For Fibonacci numbers (0.180) and primes (0.155) the question
remains open.

*H-C12-0 [INCONCLUSIVE]* (CLM-C12-09). "Every game is eventually periodic,
eventually arithmetic-periodic, or has a closed form in a number-theoretic
function." Thirteen of the 19 games conform. Subtract-a-square and
subtract-a-triangular-number are provably not (arithmetic-)periodic, but "has no
closed form" is not a theorem, so the hypothesis cannot be refuted as stated.

## Experiments

| Experiment | Question | Result |
|---|---|---|
| EXP-C12-01 | census of 19 games | 5 eventually periodic, 0 arithmetic-periodic, 14 neither within range; the detector was fixed after spurious end-of-range periods and both runs are kept |
| EXP-C12-02 | closed forms | 0 mismatches ($n \le 10^5$, $5000$ or $2 \cdot 10^4$; powers of $k$ for $k = 2..20$; 40 random splitting rules) |
| EXP-C12-03 | sparse move sets, $n \le 2 \cdot 10^5$ | P-density: squares $0.0538 \to 0.0222$, triangular $0.0344 \to 0.0116$, Fibonacci $0.169 \to 0.180$, primes $0.135 \to 0.155$ |
| EXP-C12-04 | OEIS | 18 of 19 Grundy sequences catalogued (the G10c hit is spurious); G03 matches nothing |
| EXP-C12-05 | prime signatures | H-C12-1 fails in 5 of 6 games |
| EXP-C12-06 | Grundy function of G03 | Theorem 13.7 exact on $[0, 10^5]$; 96 exceptions to $v_2$, all with odd part $\le 15$; certificate and 4000 random checks: 0 failures |

## Comparison with existing mathematics

Sprague–Grundy theory and the classical subtraction, take-and-break and
Grundy's games are treated in Berlekamp, Conway and Guy's *Winning Ways*.
Iannucci and Larsson, "Game values of arithmetic functions"
(arXiv:2101.07608, 2021), contain G04 (Theorem 1), G02 (Theorem 2), G05
(Theorem 5), the values of G06 shifted by one (Theorem 6), and G19 (Theorem 12,
whose proof is left to the reader there; ours supplies it). The win/loss
version of G01 is the "Divisor Game" puzzle (LeetCode 1025). The P-positions of
G03 are the official solution of Codeforces problem 1537D "Deleting Divisors"
(Round #726, June 2021); first believed new (no OEIS match), they were
relabelled as a rediscovery when the Historian found the problem. For
subtract-a-square, the P-set is a maximal
square-difference-free set, of density zero by Furstenberg–Sárközy (Wikipedia,
"Square-difference-free set"; Eppstein, FUN 2018). The OEIS entries A014586,
A019509, A014588 and A014589 catalogue the sparse games, A002188 Grundy's game,
and A279119 is exactly G06.

Theorem 13.7 is the exception: its sequence is not in the OEIS, the game is not
among Iannucci and Larsson's, Codeforces 1537D settles only win and loss, and
web searches found no analysis of its values. Potentially novel — not a
priority claim.

## Applications and limitations

A closed form replaces the dynamic programme over all smaller positions by a
direct evaluation and, through XOR, solves sums of games: "Deleting Divisors"
on several heaps is solved by Theorem 13.7 but not by Theorem 13.6. Beyond
recreational and competitive-programming games we found no application; no
benchmark was run and no performance improvement is claimed.

Limitations: the census covers $n \le 10^5$, $5000$ or $2 \cdot 10^4$ depending
on the game; Theorem 13.8 rests on cited theorems not re-proved here; the
written inductive steps of Theorem 13.7 await the Skeptic's review.

## Open questions

1. Are the Grundy values of subtract-a-prime (11) and subtract-a-Fibonacci
   (14) bounded? Does the Fibonacci P-density converge? (It is at most $1/5$
   by Pond and Howells, 1965.)
2. For which $d_0$ does forbidding the move "subtract $d_0$" in G01 perturb
   $v_2$ on only finitely many odd parts, as in Theorem 13.7?
3. Prove $g(m) < m/4$ for odd $m$ in the non-coprime game G06.
4. Formalise Theorem 13.7 in Lean (the certificate is finite).
5. Is Grundy's game (G18) eventually periodic? (A well-known open problem.)
