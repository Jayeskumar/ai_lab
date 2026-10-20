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

*How the book is organised.* The ten volumes follow the plan with which the
laboratory started, adjusted to what the research actually produced. Volumes
1–5 and 7–8 contain the research chapters, one per research cycle: foundations
(quantity, exchange, termination, derivations), invented operations,
emergent structures, alternative representations of quantities,
transformations and relationships, computational experiments, and
applications. Volumes 6, 9 and 10 are *catalogues generated from the
laboratory's database*: every verified theorem and open conjecture, every
refuted hypothesis with its counterexample, and every open problem. They
cannot drift from the evidence, because they are rebuilt from it each time the
book is built. Volumes are unequal in size; no chapter was written to fill a
volume.

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

*Version 1.1.* After the first edition the laboratory ran a hardening sprint
instead of new research: an audit of the novelty labels of Chapters 12–21,
Lean proofs of four theorems that had only written proofs, a re-run of every
experiment, and a certified computation on two open spectrum questions of
Chapter 6. Every change this caused to a claim's status, label or statement is
listed, with its reason, in the generated *Corrections log* at the end of the
book.

*Version 1.2.* Asked to "find more", the laboratory then went back to one open
front, the spectra of the Equational Theories Project's open laws (Chapter 6):
every order up to 10 of the 13 laws $x = y \star T$ is now decided with a
certificate, 24 orders that no source we found states are shown to have no
model, and the open question of law 677 at order 12 is cut down to explicit
pieces. A conjecture drawn from the new data was refuted by the laboratory's own
census within a day; it is kept, with the refutation, in Chapter 6.
