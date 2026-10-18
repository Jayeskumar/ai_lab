# When does rewriting stop? {#ch-termination}

*Volume 1 — Foundations. Research cycle C03.*

## Motivation

A transformation system is only a *computation* if it stops. For the simplest
non-trivial systems — a single rule moving a block of 0s past a block of 1s
while multiplying them,
$$0^p 1^q \to 1^r 0^s \qquad (p, q, r, s \ge 1),$$
we ask: from which rules does every sequence of transformations terminate?

## Easy cases

**Theorem 4.1** *[PROVEN — Lean: `terminating_of_count_lt`]*. If a rule
decreases the number of some letter ($s < p$ or $r < q$), it terminates.

**Theorem 4.2** *[PROVEN — written; swap case in Lean]*. Rules that conserve a
letter count ($s = p$ or $r = q$) terminate.

**Theorem 4.3** *[PROVEN — Lean: `not_terminating_of_loop`,
`not_terminating_double`]*. A derivation $u \to^+ x\,u\,y$ (a *loop*) proves
non-termination, and every rule in the *doubling region* $r \ge 2q$,
$s \ge 2p$ has a two-step loop.

## Two hypotheses that failed

*H-C03-1 [REFUTED]: "a rule terminates iff some letter count never grows."*
Zantema's problem $0011 \to 111000$ grows both counts and yet terminates —
a famous published result (Geser 1993), which our own search corroborates on
all 3747 words of length $\le 12$ containing $0011$, but which we did not
prove independently.

*H-C03-2 [REFUTED, Lean-checked]: "a rule terminates iff $r < 2q$ or
$s < 2p$."* The rule $011 \to 11100$ has $r = 3 < 4 = 2q$ yet loops:
$001111 \to^4 111\,001111\,00100$ (Lean: `not_terminating_0_11`). There are 35
counterexamples with parameters $\le 5$.

## Divisibility

The decisive surprise was a pair of almost identical rules:
$0011 \to 11100000$ ($s = 5$) appears to terminate, while
$0011 \to 111000000$ ($s = 6$) loops. The difference is whether the produced
block of zeros is a whole number of consumed blocks.

**Lemma 4.4** (lifting) *[PROVEN — Lean: `step_map`, `loop_map`]*. The
morphism $0 \mapsto 0^p$ carries every loop of $0\,1^q \to 1^r 0^k$ onto a loop
of $0^p 1^q \to 1^r 0^{kp}$.

One base loop thus certifies infinitely many rules. Together with exhaustive
search this classifies the family almost completely:

**Theorem 4.5** *[PROVEN — computer-assisted; REDISCOVERY]*. Of the 625 rules
with $p, q, r, s \le 5$, 525 terminate (Theorems 4.1–4.2) and 76 do not
(re-checked loop certificates); 24 remain open in our hands, all predicted to
terminate, including Zantema's problem.

**Conjecture 4.6** *[COMPUTATIONALLY SUPPORTED]*. $0^p1^q \to 1^r0^s$ is
non-terminating iff ($r \ge 2q$ and $s \ge 2p$), or ($s \ge 2p$, $q < r < 2q$
and $p \mid s$), or ($r \ge 2q$, $p < s < 2p$ and $q \mid r$). Zero
contradictions on 625 rules.

Loops can be long: the rule $0\,1^6 \to 1^7 0^6$ needs 9,332 steps and grows
a 56,035-letter word before its starting word reappears inside it.

## Comparison with existing mathematics

The family was completely characterised by Zantema and Geser (RTA 1995;
AAECC 2000); termination of one-rule systems with left side in $0^*1^*$ is
decidable. We could not retrieve their theorem statement from this
environment, so whether Conjecture 4.6 coincides with it is unverified — if it
differs, the published theorem wins. Hard terminating cases such as
Zantema's problem admit no simple matrix interpretations (none exist in the
tiers we searched) and need match-bounds or the Zantema–Geser method.

## Open questions

1. Compare Conjecture 4.6 with the Zantema–Geser characterisation.
2. Prove termination of the 24 open rules (RFC match-bounds).
3. Explain the $k^q$ growth of loop lengths in the base family.
