---
id: OPS-002
title: "Prove itr's own side of the CLI invocation contract in the test suite and CI"
kind: ops-task
status: in-progress
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

Evidence is recorded in the closeout commit once the gates and CI runs exist.

## Deviations

To be recorded in the closeout commit (`MISSING` if none).
