# Closing an open problem, and what remains open {#ch-open-problems}

*Volume 10 — Open problems and future mathematical research. Research cycle C20.*

## Motivation

Chapter 5 classified 860 of the 868 one-rule systems $l \to r$ over $\{a, b\}$
with $|l| \le 3$, $|r| \le 5$. Eight rules — the images of
$aab \to ababa$ and $aab \to babaa$ under reversal and the exchange of
letters — resisted every certificate the laboratory tried: no loop, no
interpretation. The last research cycle of the batch went back to them.

## Two tools from earlier chapters

*Random descent.* The left side $aab$ has no border, so by Theorem 5.4 all
maximal derivations from a word have the same length; one terminating
strategy settles termination for all of them.

*Runs.* Writing $w = a^{x_0} b\, a^{x_1} b \cdots b\, a^{x_m}$, a redex is a
run $x_k \ge 2$ followed by a $b$. For $aab \to ababa$ a step turns
$(x_k, x_{k+1})$ into $(x_k - 1, 1, x_{k+1} + 1)$: one surplus $a$ moves one
$b$ to the right and a new run of length 1 appears behind it. For
$aab \to babaa$ a *pair* moves: $(x_k - 2, 1, x_{k+1} + 2)$.

## The results

**Theorem 21.1** *[PROVEN — written; termination REDISCOVERY (barren rules),
complexity POTENTIALLY NOVEL]*. $aab \to ababa$ terminates, and its
derivational complexity is exactly
$$D(n) = 2^{n-2} - 1 \qquad (n \ge 2),$$
attained by $a^{n-1} b$.

*Proof idea.* Always rewrite the rightmost redex. A surplus $a$ then travels
to the right — each step brings it one $b$ closer to the end — until it fills
an empty run or reaches the last run: a finite *journey*. Journeys never
create new surplus, so there are at most (number of $a$'s) $- 1$ of them.
Each step inserts one $b$, and a journey has at most as many steps as there
are $b$'s, so every journey at most doubles the number of $b$'s. For
$a^{n-1} b$ every journey has exactly that many steps:
$1 + 2 + \cdots + 2^{n-3}$. ∎

**Theorem 21.2** *[PROVEN — written; POTENTIALLY NOVEL]*. $aab \to babaa$
terminates. Every maximal derivation from $w$ has length
$$D(w) = \sum_{k=m-1}^{0} d_k \bigl(2^{\lfloor x_k/2 \rfloor} - 1\bigr),$$
where $d_k$ is the number of $b$'s to the right of run $k$ when its turn comes
(the original $m - k$ plus one for every step already made), and
$$D(n) = \max_{1 \le b \le n} b\,\bigl(2^{\lfloor (n-b)/2 \rfloor} - 1\bigr) = \Theta(2^{n/2}).$$

*Proof idea.* A pair of $a$'s, once released, always travels all the way to
the last run, so a run releases its pairs one after another, each journey
twice as long as the previous one. ∎

**Corollary 21.3** *[PROVEN]*. All 868 rules of the extended census are
classified: 480 terminate and 388 do not.

All three statements were checked on every word of length $\le 12$ for all
eight rules; the rightmost and leftmost strategies agree on every word, as
random descent predicts (EXP-C20-01).

*What the literature already knew.* Both rules are *right barren* in
McNaughton's sense, and barren one-rule systems are known to terminate
(McNaughton; Geser, ICASE Report 2002-33). So the termination half is a
rediscovery. Geser's report proves linear derivation lengths for its
non-barren rules; for barren rules, as these examples show, the lengths can
be exponential — and here they are known exactly.

## A literature question, settled by the Historian

Chapter 4 conjectured a divisibility criterion for when
$0^p 1^q \to 1^r 0^s$ does not terminate. Zantema and Geser published a
complete characterisation of these rules (tech. report 1994, journal 2000).
The Director's attempts to obtain the full text failed (HTTP 403, a bot
challenge, HTTP 500); the Historian then found the scanned report on an older
archive host. Their Theorem 1.1 is our conjecture, verbatim — now
Theorem 4.6. The 24 rules we had left open all terminate.

## The open problems of batch 1

Volume 10's catalogue (next chapter) lists every unproven claim of the
database. The most interesting ones, in the laboratory's judgement:

1. **Common borders** (Chapter 2): the class-count formula with two or more
   common borders — and, in the one-border case, the injectivity lemma that
   would finish the proof.
2. **Finite spectra** (Chapter 7): laws whose anchored models exist only for
   $N \in \{1, 2\}$ or $\{1, 3\}$ — checked to $N = 16$, unproved.
3. **The anchor instance of left-distributivity** (Chapter 19): does
   $x \star (y+1) = (x \star y) \star (x+1)$ single out the Laver tables
   for all $N$?
4. **Rows of mex operations** (Chapter 14): the structure beyond the
   Jacobsthal row.
5. **Octal games** (Chapter 5): the periodicity of 0.06 and Officers
   (famous and hard).
6. **Circle-product thresholds** (Chapter 9): the exact associativity
   thresholds, e.g. whether tribonacci is associative at shift 4 or 5 — the
   first version of the book got four of them wrong.
