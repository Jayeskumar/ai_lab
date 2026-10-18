# Preface {.unnumbered}

This book is written by a research laboratory rather than by a single author.
The laboratory — a small team of cooperating AI research roles (an Inventor,
an Explorer, a Formal Verifier, a Skeptic, an Application Researcher, a
Historian and an Author) — set out to explore mathematical systems built from
deliberately minimal assumptions: distinguishable objects, equality, and
explicitly stated transformation rules. Numbers, positional notation,
multiplication and even "value" were not assumed; where they appear in these
pages, an earlier chapter shows how they *emerge*.

The book has one rule that overrides every other consideration:

> **Nothing is presented as established unless it has been proved, and
> nothing is presented as new unless we looked for it and failed to find it.**

Every theorem, conjecture and refuted hypothesis carries a label:

| Label | Meaning |
|---|---|
| **PROVEN** (Lean) | machine-checked in Lean 4 with Mathlib, standard axioms only |
| **PROVEN** (computer-assisted) | a finite certificate checked by a program; the trust base is stated |
| **PROVEN** (written) | a complete written proof, reviewed by the lab's independent Skeptic |
| **COMPUTATIONALLY SUPPORTED** | experiments support the claim; no proof |
| **CONJECTURE** | a precise claim awaiting proof |
| **REFUTED** | a counterexample is given — and kept, because failures teach |
| **REDISCOVERY** | the result is already in the literature (references given) |
| **POTENTIALLY NOVEL** | no equivalent found in the sources searched; *not* a priority claim |

Most of what the laboratory found is, honestly, rediscovery: the commutative
monoid of counts, chip-firing, rational base numeration, the Zeckendorf game,
Knuth's Fibonacci multiplication. We regard this as a success of the method —
independent rediscovery from minimal assumptions is evidence that the
structures are natural — and we document the literature carefully. Where
something appears to be new (for example, the "glider" of borderline exchange
rules, or the density of irreducibles for Knuth's circle product), we say
exactly how far our search went. We also report where a deeper, independent
audit found our "novelty" already in the literature: Chapter 2 tells how a
formula we first believed new turned out to follow, in most cases, from 2022
and 2026 papers on the homology of one-relator monoids.

Each chapter follows the same plan: motivation, definitions, examples,
results with proofs or proof attempts, the computational experiments behind
them (with experiment identifiers that can be re-run from the repository),
counterexamples, applications, comparison with existing mathematics,
limitations, and open questions.

*How to verify anything in this book.* Every experiment identifier
(EXP-C01-05, …) names a deterministic script in the repository; `python -m lab
run EXP-C01-05` re-runs it and checks the recorded result hash. Every claim
identifier (CLM-C08-01, …) has a record in `db/claims/` with its full status
history. Lean theorem names refer to `proofs/lean/Infinity/`.
