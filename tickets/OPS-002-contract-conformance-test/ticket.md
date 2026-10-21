---
id: OPS-002
title: "Prove itr's own side of the CLI invocation contract in the test suite and CI"
kind: ops-task
status: done
lane: direct
links:
  openspec: none
  bmad: none
worktree: .worktrees/OPS-002/
branch: ticket/OPS-002-contract-conformance-test
---

# Prove itr's own side of the CLI invocation contract in the test suite and CI

> `ops-task` MAY be read as `chore` (Shortcut mapping); the file MUST still declare `kind: ops-task`.
> An `ops-task` SHALL NOT declare a `parent:`. Trivial ops tasks may skip OpenSpec/BMAD ceremony but never skip git discipline (main-clean check + worktree + ticket branch).

## Work

`cli-invocation-contract` v0.2.0 is pinned and `itr --version` reports it
(`tests/unit/cli/test_version_flag.py`), but this repo proves only the **version**, not the
**invocation**: nothing here runs the shipped conformance kit
(`cli_invocation_contract.testkit`) against the `itr` record. A record/CLI drift (argv shape,
required env key, artifact location) would go unnoticed on this side.

Add the CLI side of AD-4 conformance, using the kit as the single source of invocation literals
(AGENTS.md §2 "do not duplicate argv/env/artifact literals in tests"):

1. `tests/contract/test_invocation_contract.py`:
   - `record = cli_invocation_contract.get("itr")` (never a hand-copied record).
   - Hermetic fixture mirroring the provisioned shape: an icons mappings YAML with group
     `battery`, a variant whose `template` is
     `status-bar/battery/battery-0/default/icon.svg` and placeholder `{{COLOR_FOREGROUND}}`,
     a palette `colors.yaml`, and a templates dir containing that SVG.
   - Set the record's `env.required` keys to fixture paths (including
     `ICON_RENDERER__TEMPLATES__DIR`), with `HOME`/`XDG_*` pointing at temp dirs and no host
     `ICON_RENDERER__*` leak; `itr render <fixture mappings file>` is the production (file) branch
     of the optional placeholder.
   - Run the repo's own console script from the repo venv (absolute path, fails loudly when
     missing — no skip) and call `assert_cli_writes_artifacts(record, "itr", run, output_dir)`;
     also `assert_consumer_invocation(record, "itr", argv, env)` so the record's argv template and
     required env keys are checked, not assumed.
2. CI: run the contract suite as a named step in the existing `test` job (no new job, so
   `ci-gates-parity` is unchanged); `testpaths = ["tests"]` means it also runs under
   `make test`/`make hermetic`.

No production code change is expected. If the record and the CLI disagree, stop and report the
mismatch with evidence — that is the contract failing, not the test.

**No OpenSpec change** (recorded choice, `links.openspec: none`): test-only slice with no
capability behaviour change. The contract record is owned by `contracts` (spine AD-4); this repo
only asserts conformance to it.

**No version bump / tag** (recorded choice): no package or contract surface changes, so the
release ritual (AGENTS.md §6) does not apply; a tests-only change ships on `main`.

## Done-when

`uv run pytest tests/contract -q` (and `make test`, `make hermetic`) runs the new test in CI's
`test` job with exit 0, `make gates`, `make ci-gates-parity` and `uv build` are exit 0, and the
slice is merged to `main` with the ticket closed.

## Evidence

| Claim | Command | Observed |
| --- | --- | --- |
| main clean before work | `git status --porcelain` on `main` | empty; `main` = `origin/main` = `7fb51e9` |
| worktree + branch | `bash scripts/worktree-guard.sh create OPS-002 contract-conformance-test` | exit 0; `worktree=.worktrees/OPS-002/`, `branch=ticket/OPS-002-contract-conformance-test` |
| record read from the pinned kit | `uv run python -c "from cli_invocation_contract import CONTRACT_VERSION, DATA_VERSION, get; …"` | `0.2.0 2`; argv `['render', '{mappings_file}?']`; required `['ICON_RENDERER__OUTPUT__OUTPUT_DIR', 'ICON_RENDERER__COLOR_SCHEME__PATH', 'ICON_RENDERER__TEMPLATES__DIR']`; artifacts `suffix`/recursive/`.svg`/`min_count 1` |
| local contract run (CI-shaped env) | `GITHUB_ACTIONS=true FORCE_COLOR=1 COLUMNS=40 uv run pytest tests/contract -q` | exit 0; `1 passed in 0.74s` |
| assertions are live (negative proof) | mutated record: argv `render --not-a-real-flag {mappings_file}?` → `assert_cli_writes_artifacts` | `AssertionError: itr: invocation exited 2; a zero exit is required before artifacts count` |
| required-key drift fails loudly | mutated record: `env.required += ["ICON_RENDERER__NEW_KEY"]` → `_env` | `AssertionError: record requires ['ICON_RENDERER__NEW_KEY'] but does not inject them; this test must supply those values before running the CLI` |
| gates | `make gates` | exit 0; `290 passed` (test), `All checks passed!` (lint), `290 passed` (hermetic), `Resolved 26 packages` (lock-check), docs-check silent |
| workflow ↔ Makefile parity | `make ci-gates-parity` | exit 0; `PASS gates=['docs-check', 'hermetic', 'lint', 'lock-check', 'test'] jobs=['ci-gates-parity', 'docs-check', 'hermetic', 'lint', 'lock-check', 'release', 'test'] exempt=['ci-gates-parity', 'release']` |
| packaging | `uv build` | exit 0; `dist/icon_templates_renderer-0.2.0.tar.gz` + `dist/icon_templates_renderer-0.2.0-py3-none-any.whl` |
| CI on `3629441` (`main`) | `gh run view 39666028808 --json status,conclusion,jobs` | `completed` / `success`; `test`, `lint`, `hermetic`, `lock-check`, `docs-check`, `ci-gates-parity` all `success`; `release` skipped (tag-only) |
| the contract step really ran in CI | `gh run view 39666028808 --log \| grep -E "tests/contract\|passed"` | `Run uv run pytest tests/contract -q -rs` → `1 passed in 0.38s`; `Run make test` → `290 passed in 5.24s`; `hermetic` → `290 passed in 7.66s` |

## Deviations

1. **The ticket and `INDEX.md` landed on the ticket branch, not on `main` first** (unlike OPS-001):
   `scripts/worktree-guard.sh create` refuses a dirty tree, so the ticket was written inside the
   worktree and the planning commit (`fbaf7fb`) is part of the merged branch. `main` never held an
   uncommitted planning edit.
2. **The contract step is a named CI step *and* runs again inside `make test`/`make hermetic`**
   (`testpaths = ["tests"]`). The duplicate execution is deliberate: the named step attributes a
   contract drift directly, while `make test` keeps the local/CI gate sets identical.
3. **No version bump / tag.** Tests and CI only; no package, CLI or contract surface changed, so
   the release ritual (AGENTS.md §6) does not apply.

## Closeout

Closed 2026-10-21. Three commits on `main`: `fbaf7fb` (ticket + INDEX), `3629441`
(`tests/contract/test_invocation_contract.py` + the `test` job step) and `c29636a` (this
closeout). CI run `39666028808` on the code commit `3629441` is `success` and its contract step
reports `1 passed`. No OpenSpec change and no tag — see "No OpenSpec change" / "No version bump /
tag" above.
