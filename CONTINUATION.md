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

## 2. Check that the recorded state is reproducible

`python -m lab verify` re-runs every experiment and compares result hashes
with the last recorded run (timings are excluded from hashes). Any `CHANGED`
result must be investigated and recorded in the journal before continuing —
never silently overwritten. Experiments that query the OEIS read the cached
answers in `cache/oeis/` and need no network.

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
| reviews | `reviews/*.md` | Skeptic / Historian agents |

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
5. `python -m lab sync && python -m lab lean`, then commit and push.
6. Ask an *independent* Skeptic and Historian to review the new claims
   (see `reviews/` for the format) and fold their verdicts back in via
   `record.yaml` with `change_reason`.

Parallel workers must write only their own cycle's files and new modules in
`systems/`; only the coordinator runs `sync`, `lean` and git.

## 5. Next research priorities

The current list is in `checkpoints/state.json` (`next_priorities`) and in
the "Next directions" section of every cycle README; the batch report in
`reports/` ranks them.
