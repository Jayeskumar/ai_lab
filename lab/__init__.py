"""Project Infinity research-laboratory infrastructure.

The lab is organised around five kinds of persistent records:

* experiments  -- executable scripts in ``experiments/`` (one per EXP id);
                  each run writes ``results/<EXP>.json`` and updates
                  ``db/experiments/<EXP>.json``.
* claims       -- precise mathematical statements in ``db/claims/<CLM>.json``
                  with a verification status and a novelty status.
* journal      -- append-only research journal ``journal/entries.jsonl``.
* proofs       -- Lean 4 files in ``proofs/lean`` (checked by ``lab lean``)
                  and written proofs in ``proofs/paper``.
* audit log    -- ``db/audit_log.jsonl``; every change to any record is
                  appended here and nothing is ever deleted.

Run ``python -m lab --help`` for the command-line interface.
"""

__version__ = "1.0.0"
