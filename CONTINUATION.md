# Research continuation instructions

How to resume Project Infinity in a fresh environment without losing completed
work. Everything needed is in this repository; nothing lives only in a
running process.

## 1. Restore the environment

```bash
pip install -r requirements-lock.txt        # pinned versions used for all recorded runs
curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none
export PATH="$HOME/.elan/bin:$PATH"
cd proofs/lean && lake exe cache get && cd ../..   # Mathlib v4.35.0 oleans (~5 GB)
python -m pytest -q tests/                  # infrastructure tests
python -m lab status                        # should match checkpoints/state.json
python -m lab lean                          # re-check every Lean file
```

PDF export needs a Chromium binary (`CHROMIUM=/path/to/chrome python -m lab book`).

Only EXP-C05-06 and EXP-C05-08 to -13 need an external proof checker, drat-trim (see
`research/cycles/C05_magma_spectra/README.md`, "Reproducibility"):

```bash
mkdir -p ~/tools/drat && cd ~/tools/drat
curl -sSfL https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c -o drat-trim.c
gcc -O2 -o drat-trim drat-trim.c && export DRAT_TRIM="$HOME/tools/drat/drat-trim"
```

Without it these experiments record "checker unavailable" and certify nothing.
The batch 1.2 experiments EXP-C05-09 to -13 take from minutes to hours each; run
them detached with a checkpoint directory (`EXP_CHECKPOINT=/some/dir python -m lab
run EXP-C05-10`) so that an interrupted run resumes case by case — checkpoints
are keyed by the SHA-256 of the case CNF and the conflict budget.

## 2. Check that the recorded state is reproducible

`python -m lab check` (about a second) validates everything that does not need
a re-run: every `record.yaml` parses with duplicate keys rejected, claim ids
and journal keys are unique, every reference resolves (evidence, related ids,
proof files and their `#anchor`, Lean files), the database agrees with the
records, every result file's stored hash matches its content and the last
recorded run, no result was produced by an older version of its script, and
no wall-clock field sits inside the hashed results. Run it after every
`sync` and before every commit; it must report 0 errors.

`python -m lab verify` re-runs every experiment and compares result hashes
with the last recorded run (timings are excluded from hashes; add `--dry` to
compare without recording the runs, and `--cycle Cnn` to restrict it). The
whole batch takes several hours on one core — EXP-C05-03 alone needed 47
minutes on the shared container — so verify cycle by cycle. Any `CHANGED`
result must be investigated and recorded in the journal before continuing —
never silently overwritten. Experiments that query the OEIS read the cached
answers in `cache/oeis/` and need no network. `verify` skips experiments that
were never recorded (run them with `python -m lab run` first). The batch 1.1
audit (`reports/REPRODUCIBILITY_batch1.1.md`) re-ran every experiment.

## 3. Where the state lives

| State | File(s) | Writer |
|---|---|---|
| checkpoint summary | `checkpoints/state.json` | `python -m lab sync` |
| claims (verification + novelty + history) | `db/claims/*.json` | `sync` from `research/cycles/*/record.yaml` |
| experiments (meta + runs) | `db/experiments/*.json` | `python -m lab run` and `sync` |
| audit log (every change, append-only) | `db/audit_log.jsonl` | `lab.db` |
| journal (append-only) | `journal/entries.jsonl` → `journal/JOURNAL.md` | `sync`, `python -m lab journal` |
| raw results | `results/*.json`, `results/artifacts/` | runner |
| Lean status | `proofs/lean_results.json` | `python -m lab lean` |
| reviews | `reviews/*.md`, their check code in `reviews/skeptic_checks/`, `reviews/historian_checks/` | Skeptic / Historian agents |
| catalogue volumes (Vol. 6, 9, 10 lists) and the corrections-log appendix | `textbook/src/generated/*.md` | `python -m lab catalogue` (also run by `book`) |
| batch statistics and report tables | `reports/batch_statistics.json`, `reports/REPORT_DATA.md` | `python -m lab report` |
| textbook build | `textbook/build/` (HTML, PDF) | `python -m lab book [--no-pdf]` |

Never edit `db/` or `journal/` by hand. To change a claim (e.g. after a
review), edit the cycle's `record.yaml`, add `change_reason: ...` to the
claim, and run `python -m lab sync`; the old value stays in the claim's
history and in the audit log.

## 4. Adding a research cycle

1. Create `experiments/Cnn/` (with `__init__.py`) and scripts `Emm_slug.py`
   defining a literal `META` dict (`id: EXP-Cnn-mm`, cycle, title, agent,
   question, hypothesis, assumptions, methodology, falsification, seed) and a
   deterministic `run()` returning a dict with a `summary` list (timings only
   under `timings`).
2. Run with `python -m lab run --cycle Cnn`.
3. Proofs: `proofs/paper/Cnn.md`; Lean in `proofs/lean/Infinity/Cnn_Name.lean`
   ending with `#print axioms` lines.
4. Write `research/cycles/Cnn_slug/README.md` (ten steps) and `record.yaml`
   (claims with type/title/statement/verification/novelty/evidence; PROVEN
   needs `proof` and `proof_check`; REFUTED needs `counterexample`).
   The report classifies a PROVEN claim by the start of its `proof_check`:
   `Lean 4 (complete) - ...` for a proof that is entirely machine-checked,
   `computer-assisted - ...` for a finite certificate, `written proof ...`
   (mention any Lean-checked part), `published theorem ...` for a statement
   read in the literature. A partial rediscovery is recorded as REDISCOVERY
   with a novelty basis starting `Partial - ` that names the unpublished part.
5. `python -m lab sync && python -m lab lean`, then commit and push.
6. Ask an *independent* Skeptic and Historian to review the new claims
   (see `reviews/` for the format) and fold their verdicts back in via
   `record.yaml` with `change_reason`.

Parallel workers must write only their own cycle's files and new modules in
`systems/`; only the coordinator runs `sync`, `lean` and git. `sync` checks
every claim of a record before importing it and skips a cycle whose record is
not yet valid (e.g. a PROVEN claim without `proof`), with a warning — so a
worker's unfinished record never aborts the coordinator's sync.

To add a chapter to the textbook, write `textbook/src/NN_slug.md` (a first
heading with an `{#ch-...}` anchor, then the chapter structure of
`textbook/src/01_method.md`) and list it in `textbook/BOOK.yaml`; chapter
numbers are hard-coded in the theorem labels ("Theorem 16.3"), so check them
after reordering.

## 5. Next research priorities

The current list is in `checkpoints/state.json` (`next_priorities`) and in
the "Next directions" section of every cycle README; the batch report
(`reports/RESEARCH_REPORT_batch1.md`, section 10) ranks them, and the
textbook's Volume 10 lists every open claim.

## 6. Review status (batch 1 and the batch 1.1 sprint)

Every cycle had an independent Skeptic review and (for C01–C10 and selected
later claims) a Historian novelty audit; the review files in `reviews/` list
the claims they covered and the verdicts. A claim whose `proof_check` still
says "awaiting independent skeptic review" has not been re-checked by
someone other than its author — treat such a written proof as provisional
and review it first. `grep -l "awaiting independent" db/claims/*.json`
lists them. Batch 1.1 added the Historian audit of C11–C20
(`reviews/historian_C11_C20.md`) and a Skeptic review of the sprint's own
results (`reviews/skeptic_batch1.1.md`); the sprint plan and its outcome are
in `reports/PM_PLAN_batch1.1.md`.

## 7. Lessons from batch 1, 1.1 and 1.2 (operational)

* **Test a general pattern on all the data at hand before writing it down.**
  Batch 1.2 stated "a law x = y*T without a model of order 2 has none of order
  2 mod 4" from twelve laws; the lab's own census (EXP-C05-01) refuted it the
  same day with law 474 (CLM-C05-18). Query the census first.
* **Controls can be direct.** When a decision control would take a day (the
  known model sits in a late case), check instead that each known model,
  relabelled into its case, satisfies that case's CNF
  (`systems.magma_split.admits`): this tests exactly the encoding that could
  wrongly exclude models.
* **`python -m lab run --dry` runs the experiment** (it only skips recording);
  use `python -m lab check` to validate without running.
* **Split a hard search by a structural dichotomy before adding brute force.**
  The 57 hard cases of law 677 at order 12 all fall within seconds once the
  table is required to be a Latin square (EXP-C05-13); what is left is the
  non-quasigroup half.

* **Check the literature before a heavy computation.** The ETP paper already
  reports that Mace4 exhausts size 8 for law 677; reading it first turned a
  planned "new result" into a certified rediscovery and redirected the CPU
  time to order 10.
* **Let the hard cases shape the symmetry breaking.** For 677 at order 10 the
  first case split left 41 of 97 cases undecided, almost all with the chosen
  element idempotent; splitting on idempotency (Lemma 8 of
  `proofs/paper/C05.md`) and adding implied division clauses made them easy.
* **Run multi-hour jobs detached and with progress output.** Background jobs of
  the agent harness are stopped after at most two hours; start long runs with
  `setsid nohup <script> &`, print one progress line per unit of work to
  stderr (never into the results), and restart a stopped audit from the
  cycle where it stopped (`python -m lab verify <ids> --dry`).
* **Tooling bugs hide in idempotent-looking code.** `sync` re-appended the same
  journal revision of two entries on every run (16 copies each) because it
  compared the record with the original entry instead of its latest revision;
  `lab check` and a regression test now catch this.

* **Random testing is not a proof — and it missed real counterexamples.**
  The first circle-product thresholds (C08) were found by random triples and
  four of them were wrong; certificates (an explicit failing triple, or an
  algebraic embedding) replaced them in EXP-C08-06. Prefer exhaustive search
  over a stated range, or a certificate, to sampling.
* **Keep wall-clock data out of result hashes.** Put every timing under the
  summary's `timings` key; a timing anywhere else makes `verify` report
  CHANGED on every re-run (EXP-C06-03/-04 and EXP-C16-01 had this bug).
* **Check heavy experiments before running them.** One unused 8!-permutation
  canonicalisation made EXP-C06-02 run for 27 minutes instead of 53 s. Run
  long jobs under `nice`, record their runtime, and checkpoint (commit) before
  and after.
* **Sessions can stop at any time** (rate limits, container restarts). Commit
  and push after every completed cycle and before launching long agents; an
  interrupted agent can be resumed from its transcript, but processes it had
  started are gone.
* **The literature is not always reachable.** Record every failed retrieval
  (HTTP status, host) in the novelty basis; a later attempt from another host
  can succeed, as it did for Zantema–Geser 1994.
* **Independent review pays.** The Skeptics found false statements at
  boundary cases (n = 0, N = 1), mislabelled cross-references, results that
  were weaker than proved and stronger than proved, and an imprecisely quoted
  theorem (the Laver-table recursion, CLM-C06-01); the Historian downgraded
  many "potentially novel" findings to rediscoveries. Never skip the review
  step.
