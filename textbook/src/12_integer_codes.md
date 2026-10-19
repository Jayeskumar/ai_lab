# Codes from forbidden patterns {#ch-integer-codes}

*Volume 4 — Alternative representations of quantities. Research cycle C11.*

## Motivation

A *universal code* writes every positive integer as a self-delimiting bit
string, so that a stream of integers of unknown size can be decoded without
separators. The Fibonacci code writes the Zeckendorf digits of $n$ (weights
$1, 2, 3, 5, \ldots$, least significant first) and appends a 1; as Zeckendorf
digits never contain $11$, the codeword ends where $11$ first appears. The
code is defined by a *forbidden pattern*, and $11$ is one choice among many.
Replacing it by an arbitrary terminator $p$, we ask which terminator is best,
and whether any of the resulting codes is useful against honest baselines,
including an improved Fibonacci code from the literature and Golomb–Rice codes
tuned to the data. The counting is governed by the autocorrelation polynomial
of Chapter 2.

## Definitions

Let $p$ be a binary pattern of length $k$. The code $T_p$ has as codewords the
binary words in which $p$ occurs *for the first time at the very end*,
assigned to $n = 1, 2, 3, \ldots$ in order of length and then
lexicographically (enumerative coding with a Knuth–Morris–Pratt automaton):
$$T_{11} = \{11,\ 011,\ 0011,\ 1011,\ \ldots\}, \qquad
T_{011} = \{011,\ 0011,\ 1011,\ 00011,\ 01011,\ 10011,\ 11011,\ \ldots\}.$$
$f_p(L)$ is the number of codewords of length $L$,
$\mathrm{cum}_p(L) = \sum_{l \le L} f_p(l)$, and the codeword of $n$ has length
$L_p(n) = \min\{L : \mathrm{cum}_p(L) \ge n\}$. As in Chapter 2,
$c_p(x) = 1 + \sum_b x^{k - |b|}$, summed over the borders $b$ of $p$, is the
*autocorrelation polynomial*; $p$ is *unbordered* if $c_p = 1$. The *growth
rate* is $\lambda_p = 1/\rho_p$, with $\rho_p$ the smallest positive root of
$$D_p(x) = x^k + (1 - 2x)\,c_p(x),$$
and $L_p(n)/\log_2 n \to 1/\log_2 \lambda_p$. The *redundancy* of a code on a
source is its expected codeword length minus the entropy.

## The pattern-terminated family

**Theorem 12.1** *[PROVEN — Lean: `prefix_free`, `unique_parse_head`;
REDISCOVERY]*. For every pattern $p$ of length $k$:
(a) $T_p$ is a prefix code; (b) its Kraft sum $\sum_L f_p(L)\,2^{-L}$ equals 1;
(c) its counts have the generating function
$$F_p(x) = \sum_L f_p(L)\,x^L = \frac{x^k}{x^k + (1 - 2x)\,c_p(x)};$$
(d) $T_{11}$ has exactly the codewords of the Fibonacci code, and $T_{1^k}$
those of its order-$k$ generalisation.

*Proof idea.* (a) A codeword that is a proper prefix of another would put $p$
before the other's end (Lean also checks unique parsing). (b) The sum is the
probability that a random infinite bit sequence contains $p$. (c) If $A(x)$
counts the words avoiding $p$, appending a letter gives $1 + 2xA = A + F_p$,
and appending $p$ (whose first occurrence then ends after a period of $p$)
gives $x^k A = c_p F_p$. (d) A word whose first $11$ is at its end is a
Zeckendorf digit string followed by the extra 1. ∎ By (c), $T_p$ depends on
$p$ only through $k$ and $c_p$. The 61 implemented pattern codes passed round
trips, a prefix check and Kraft partial sums $\ge 0.999999999993$ (EXP-C11-01).

**Theorem 12.2** *[PROVEN — written; REDISCOVERY: Guibas–Odlyzko correlation
ordering]*. Among the binary patterns of length $k$, $1^k$ and $0^k$ have the
largest growth rate, and every other pattern has a strictly smaller one.

*Proof idea.* $D_p(1/2) = 2^{-k}$ for every $p$. Since $1^k$ has every period,
$c_{1^k}$ dominates $c_p$ coefficientwise, and for $x > 1/2$
$$D_{1^k}(x) - D_p(x) = (1 - 2x)\bigl(c_{1^k}(x) - c_p(x)\bigr) \le 0,$$
strictly unless $c_p = c_{1^k}$. So $D_{1^k}$ vanishes no later than $D_p$. ∎
All 2044 patterns of length 2 to 10 agree (EXP-C11-02); for example
$\lambda_{11} = 1.618$, $\lambda_{101} = 1.755$, $\lambda_{111} = 1.839$,
$\lambda_{0101} = 1.883$ and $\lambda_{1111} = 1.928$.

*The bold hypothesis fails.* H-C11-2 *[REFUTED]*: "hence $1^k$ is the best
length-$k$ terminator beyond small $n$." At $n = 1000$ the terminators $1000$,
$1001$, $1010$ give codewords one bit shorter than $1111$. Among the sampled
$n \ge 1000$ (all $n \le 2048$ and quarter-powers of 2 up to $2^{64}$), rivals
beat $1^k$ at 762, 972 and 1127 values for $k = 4, 5, 6$, the last as late as
$n \approx 1.3 \cdot 10^{19}$ (EXP-C11-02). Theorem 12.2 is about the limit; at
practical sizes the constants decide.

## Unbordered terminators

**Theorem 12.3** *[PROVEN — written; REDISCOVERY]*. If $u$ is unbordered and
$|u| = k + 1$, then
$$F_u(x) = \frac{x}{1 - x}\,F_{1^k}(x), \qquad\text{i.e.}\qquad
f_u(L) = \mathrm{cum}_{1^k}(L - 1).$$
Hence $\lambda_u = \lambda_{1^k}$ is the $k$-bonacci constant $\lambda$, and
$\mathrm{cum}_u(L)/\mathrm{cum}_{1^k}(L) \to 1/(\lambda - 1)$.

*Proof.* $c_{1^k} = (1 - x^k)/(1 - x)$ gives
$F_{1^k} = x^k(1 - x)/(1 - 2x + x^{k+1})$, and $c_u = 1$ gives
$F_u = x^{k+1}/(1 - 2x + x^{k+1})$. ∎ The identity holds exactly for every
unbordered pattern of length 3 to 9 up to length 200, and the count ratios at
length 300 are $1.618033989$, $1.191487884$, $1.078095078$ for $k = 2, 3, 4$
(EXP-C11-02, EXP-C11-06).

**Corollary 12.4** *[PROVEN — written; partly REDISCOVERY: $T_{011}$ is
Capocelli's code C(3)]*.
With $F_1 = F_2 = 1$, $\mathrm{cum}_{11}(L) = F_{L+1} - 1$ and
$\mathrm{cum}_{011}(L) = F_{L+2} - L - 1$. If the Fibonacci codeword of $n$ has
length $L + 1$, the $T_{011}$ codeword is one bit shorter when
$n \le F_{L+2} - L - 1$ and equally long for the last $L$ values of the level;
$T_{011}$ is longer than the Fibonacci code only for $n \in \{1, 2, 4\}$. The
same holds for every unbordered 3-letter terminator.

*Proof idea.* Theorem 12.3 with $k = 2$ gives $f_{011}(l) = F_l - 1$; compare
the cumulative counts level by level. ∎ For $n \le 2 \cdot 10^6$ the $T_{011}$
codeword is one bit shorter for 1,999,568 values, equally long for 429 and
longer for 3; block-wise checks up to $L = 90$ find no exception (EXP-C11-06).

*Two predictions of the average gain fail* *[REFUTED]*. For $k \ge 3$, $u$
wins only on part of each level. The guess that the average of
$L_{1^k}(n) - L_u(n)$ over $n \le N$ tends to $\log_\lambda(1/(\lambda - 1))$
predicts 0.2875 for $k = 3$; the average over $n \le 2^{40}$ is 0.2282
(EXP-C11-06). The corrected guess, convergence to
$(2 - \lambda)/(\lambda - 1)^2 = 0.228155$, fails too: the running average is
0.228181, 0.309709, 0.228548 at $N = 2^{40}, 2^{80}, 2^{120}$ (EXP-C11-07).

**Proposition 12.5** *[PROVEN — written; POTENTIALLY NOVEL (low
confidence)]*. Let $k \ge 2$, $\lambda$ the $k$-bonacci constant, $u$
unbordered of length $k + 1$ and
$G(N) = \frac{1}{N}\sum_{n \le N}\bigl(L_{1^k}(n) - L_u(n)\bigr)$. Then
$$\liminf_{N\to\infty} G(N) = \frac{2 - \lambda}{(\lambda - 1)^2}, \qquad
\limsup_{N\to\infty} G(N) = \frac{\lambda(2 - \lambda)}{\lambda - 1}.$$

*Proof idea.* Put $r = 1/(\lambda - 1)$. For $k \ge 3$, on the level of
$T_{1^k}$ with codeword length $L$, $T_u$ is one bit shorter exactly on the
first $\mathrm{cum}_u(L-1) - \mathrm{cum}_{1^k}(L-1) \approx
(r - 1)\,\mathrm{cum}_{1^k}(L-1)$ values and equally long on the rest; $G$
rises along this segment and falls after it, and geometric sums at the two
turning points give the constants. For $k = 2$ use Corollary 12.4. ∎
The pair (liminf, limsup) is $(1, 1)$, $(0.228155, 0.352201)$,
$(0.084194, 0.150533)$, $(0.036495, 0.069304)$, $(0.016970, 0.033108)$ for
$k = 2, \ldots, 6$; exact averages agree to six digits (EXP-C11-08).

## The improved Fibonacci code C3

Fraenkel and Klein (1996) improved C1 by a code C3: delete the final 1 of each
C1 codeword, take each length block twice and prefix the copies with $10$ and
$11$ ($101, 111, 1001, 1101, 10001, \ldots$). C3 is uniquely decipherable and
complete but *not* prefix-free: its decoder searches for $011$ and reads one
bit of the next codeword.

**Corollary 12.6** *[PROVEN — written; partly REDISCOVERY: Fraenkel–Klein]*.
C3 has $2F_{r-2}$ codewords of length $r \ge 3$, so
$\mathrm{cum}_{C3}(L) = 2F_L - 2$. C3 is never longer than C1 except at
$n = 1$, and $T_{011}$ is never longer than C3 except at $n \in \{2, 4, 8\}$;
$\mathrm{cum}_{011}/\mathrm{cum}_{C3} \to \varphi^2/2 \approx 1.309$ and
$\mathrm{cum}_{C3}/\mathrm{cum}_{C1} \to 2/\varphi \approx 1.236$. (The count
and the comparison with C1 are Fraenkel and Klein's; the comparison with
$T_{011}$ was not found in the sources we read.)

*Proof.* As $F_{L+2} - 2F_L = F_{L-1}$, $\mathrm{cum}_{011}(L) -
\mathrm{cum}_{C3}(L) = F_{L-1} - (L - 1)$, negative only for $L = 3, 4, 5$; and
$\mathrm{cum}_{C3}(L) - \mathrm{cum}_{C1}(L) = F_{L-2} - 1 \ge 0$ for $L \ge 3$. ∎
Our C3 (its first 12 codewords match the paper's list) confirms this for
$n \le 2 \cdot 10^6$ (EXP-C11-09). The average of $L_{C1} - L_{C3}$ over
$n \le 2^{40}, 2^{80}, 2^{120}$ is 0.462, 0.400, 0.481: C3 recovers less than
half of the bit that $T_{011}$ saves.

## Benchmarks

**Benchmark result 12.7** *[COMPUTATIONALLY SUPPORTED — algorithmic;
improvement MIXED; baselines: Elias $\gamma$, $\delta$, $\omega$, Levenshtein,
Fibonacci C1, Fraenkel–Klein C3, LEB128, Exp-Golomb(0, 2, 4), and Golomb–Rice
and Exp-Golomb codes tuned to each source]*. Among untuned codes, a pattern
code is best on 5 of 12 synthetic sources and on both posting lists, beating
the best classical code there by 0.34–3.06 bits per value; on Zipf 1.1,
log-uniform and the bursty posting list it also beats the tuned codes. It
loses on light-tailed sources and to tuned codes on geometric and uniform
sources, and is 4–10 times slower than the Elias and Exp-Golomb codes.

Expected lengths are exact, from the breakpoints of each length function (no
sampling); codes defined on $n \ge 0$ are applied to $n - 1$. Redundancy in
bits per value (EXP-C11-03; best entries bold):

| source | $H$ | best fixed classical | best pattern code | tuned Golomb | tuned Exp-Golomb |
|---|---|---|---|---|---|
| Zipf 1.1 | 10.90 | C3 0.60 | **$T_{101}$ 0.19** | 5.38 | 1.72 |
| Zipf 1.5 | 4.62 | **Fibonacci 0.10** | $T_{011}$ 0.52 | 6.07 | 0.25 |
| Zipf 2 | 2.36 | **$\gamma$ 0.08** | $T_{011}$ 1.38 | 2.00 | **0.08** |
| Zipf 3 | 0.98 | Levenshtein 0.39 | $T_{011}$ 2.23 | **0.39** | 0.44 |
| geometric 0.5 | 2.00 | Levenshtein 0.19 | $T_{011}$ 1.63 | **0.00** | 0.27 |
| geometric 0.1 | 4.69 | Exp-Golomb(2) 0.30 | $T_{011}$ 0.72 | **0.04** | 0.30 |
| geometric 0.01 | 8.08 | Exp-Golomb(4) 0.70 | $T_{011}$ 0.93 | **0.03** | 0.28 |
| geometric 0.001 | 11.41 | C3 2.51 | $T_{0111}$ 1.74 | **0.03** | 0.28 |
| uniform $2^8$ | 8 | Exp-Golomb(4) 1.75 | $T_{011}$ 1.93 | **0.50** | 1.00 |
| uniform $2^{16}$ | 16 | C3 5.71 | $T_{0111}$ 3.30 | **0.50** | 1.00 |
| uniform $2^{32}$ | 32 | LEB128 7.50 | $T_{00111}$ 4.44 | **0.50** | 1.00 |
| log-uniform $10^6$ | 13.41 | C3 1.36 | **$T_{0111}$ 0.40** | 3.93 | 2.00 |

Bits per value on data (EXP-C11-04; $H_0$ is the zeroth-order entropy; the
tuned codes are tuned on the same data, which favours them):

| data | $H_0$ | best fixed classical | best pattern code | tuned Golomb | tuned Exp-Golomb |
|---|---|---|---|---|---|
| prime gaps $\le 10^7$ | 4.17 | Exp-Golomb(4) 5.72 | $T_{011}$ 6.14 | **5.27** | 5.58 |
| prime gaps, halved | 4.17 | Exp-Golomb(2) 4.58 | $T_{011}$ 5.11 | **4.27** | 4.58 |
| posting list, geometric gaps | 11.36 | C3 13.93 | $T_{0111}$ 13.15 | **11.45** | 11.70 |
| bursty posting list | 10.71 | C3 11.82 | **$T_{101}$ 11.47** | 12.80 | 11.79 |

*Where pattern codes lose.* On light-tailed sources (Zipf $\ge 1.5$,
geometric $\ge 0.01$, prime gaps) $\gamma$, Levenshtein, Fibonacci or
Exp-Golomb are better; even C3 beats $T_{011}$ on Zipf $\ge 1.5$, geometric
0.5 and 0.1 and the prime gaps, where its shorter codewords for $n = 2, 4, 8$
carry much probability. Tuned codes are within 0.04 bits of the entropy on
geometric sources and within 0.5–1 bit on uniform ones; no universal code
comes close. *Speed:* in our string-based CPython implementations
(EXP-C11-05), pattern codes take about 3 µs per value, against 0.4–0.7 µs for
the Elias codes and 2.1 µs for the Fibonacci code (machine-dependent; no
optimised decoder was attempted).

## Comparison with existing mathematics

Most of the theory of $T_p$ is classical. The Fibonacci code and its order-$k$
generalisation are Apostolico and Fraenkel's and Fraenkel and Klein's. The
generating function of Theorem 12.1 comes from Guibas and Odlyzko's theory of
string overlaps, and Theorem 12.2 is in substance their comparison of patterns
through correlations; every count sequence we used is in the OEIS. The closest
prior art for $T_{011}$ is C3, which already improves C1 by decoding with
$011$ but gives up the prefix property. For prefix-synchronised (fixed-length)
codes, unbordered markers $1\cdots10$ are optimal at finite lengths (Gilbert;
Guibas and Odlyzko), the phenomenon of Theorem 12.3 in another setting; the
multi-delimiter codes of Anisimov and Zavadskyi are reported to beat Fibonacci
codes. The Historian's second audit found that $T_{011}$ itself is
Capocelli's code C(3) (IEEE Trans. Inform. Theory 35, 1989: the words in which
011 occurs only as a suffix), that the codes $T_p$ in general are Lakshmanan's
pattern codes (1981; Fraenkel and Klein 1996, §3), and that Lima and da Rocha
(2013) tabulate C(3) against the Fibonacci code, one bit shorter at the
tabulated $n = 2^t$. The exact comparisons of Corollaries 12.4 and 12.6 were
not found (Capocelli's paper could not be read), so both are recorded as
partial rediscoveries; our confidence in the novelty of Proposition 12.5 is
low, given the multi-delimiter codes and the generic nature of log-periodic
oscillations.

* P. Elias, "Universal codeword sets and representations of the integers",
  IEEE Trans. Inform. Theory 21 (1975) 194–203.
* A. Apostolico, A. S. Fraenkel, IEEE Trans. Inform. Theory 33 (1987) 238–245,
  <https://docs.lib.purdue.edu/cstech/464>.
* A. S. Fraenkel, S. T. Klein, Discrete Appl. Math. 64 (1996) 31–55 (codes C1,
  C2, C3), <https://u.cs.biu.ac.il/~tomi/Postscripts/robust.pdf>.
* L. J. Guibas, A. M. Odlyzko, J. Combin. Theory Ser. A 30 (1981) (string
  overlaps); SIAM J. Appl. Math. 35 (1978) 401–418 (prefix-synchronized
  codes). E. N. Gilbert, IRE Trans. Inform. Theory 6 (1960) 470–477.
* A. V. Anisimov, I. O. Zavadskyi, IEEE Trans. Inform. Theory 63 (2017)
  2885–2895, <https://arxiv.org/abs/1508.01360>.
* <https://en.wikipedia.org/wiki/Fibonacci_coding>; OEIS
  <https://oeis.org/A000071> ($T_{011}$), <https://oeis.org/A005314>
  ($T_{101}$), <https://oeis.org/A008937> ($T_{0111}$),
  <https://oeis.org/A059633> ($T_{1011}$), <https://oeis.org/A112575> ($T_{0101}$).

## Applications and limitations

$T_{011}$ is a drop-in prefix-free replacement for the Fibonacci code that
saves one bit on almost every integer (Corollary 12.4). For heavy-tailed
streams of unknown scale (gaps in posting lists with bursty terms, magnitudes
over many orders), a fixed pattern code such as $T_{0111}$ or $T_{101}$ is a
strong universal choice; for geometric gaps use Golomb–Rice, for values of
known range a tuned Golomb or Exp-Golomb code, for small values $\gamma$,
Fibonacci or C3. These are empirical findings on 12 synthetic sources and 4
data sets (two simulated), comparing memoryless codes with zeroth-order
entropy, with the tuned codes fitted to the evaluated data. No code is claimed
optimal, and the 4–10-fold speed penalty of our implementation is unresolved.

## Open questions

1. Can table-driven (byte-wise) decoders make pattern codes as fast as
   optimised Elias and Fibonacci decoders?
2. Which *sets* of terminators, as in multi-delimiter codes, suit a source?
3. How well do unbordered terminators resynchronise after bit errors?
4. What are the oscillation constants of the gain of $T_{011}$ over C3?
