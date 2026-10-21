---
id: OPS-001
title: "Re-pin cli-invocation-contract (contracts) v0.2.0 and release itr v0.2.0"
kind: ops-task
status: done
lane: direct
links:
  openspec: none
  bmad: none
worktree: .worktrees/OPS-001/
branch: ticket/OPS-001-contract-0-2-0-v0-2-0
---

# Re-pin cli-invocation-contract (contracts) v0.2.0 and release itr v0.2.0

> `ops-task` MAY be read as `chore` (Shortcut mapping); the file MUST still declare `kind: ops-task`.
> An `ops-task` SHALL NOT declare a `parent:`. Trivial ops tasks may skip OpenSpec/BMAD ceremony but never skip git discipline (main-clean check + worktree + ticket branch).

## Work

The `contracts` repo cut `v0.2.0` (annotated tag object
`442fb9abdc73fa109115ba804911a10af9f4cad1`, peeled commit
`c6c3ab5d523d06210f8e87535c464d3190d005c0`): `CONTRACT_VERSION = "0.2.0"`,
`DATA_VERSION = 2`, and the `clis.itr` invocation record now lists
`ICON_RENDERER__TEMPLATES__DIR` in `env.required` and injects it from `{templates_dir}`.

This repo consumes that record but does not set it — the **runtime** (`dotfiles-v3`) injects
`ICON_RENDERER__TEMPLATES__DIR`; `itr` already reads that env key
(`src/icon_templates_renderer/cli/_helpers.py`), so no CLI code or behaviour changes here.

Work:

1. `pyproject.toml`: `[tool.uv.sources] cli-invocation-contract` tag `v0.1.0` → `v0.2.0`;
   package `version` `0.1.0` → `0.2.0`; dependency floor `cli-invocation-contract>=0.2.0`.
2. `uv lock`, proving `uv.lock` records peeled commit `c6c3ab5d…`.
3. `tests/unit/cli/test_version_flag.py`: assert `f"{dist_version} contract {CONTRACT_VERSION}"`
   (no duplicated contract literal) plus an explicit `CONTRACT_VERSION == "0.2.0"` assertion.
4. `README.md` version/pin references, `CHANGELOG.md` `0.2.0` entry.
5. `make gates` exit 0, `uv build`, commit, ff-merge `main`, push, annotated tag `v0.2.0`,
   GitHub Release with wheel + sdist built from the tag.

**No OpenSpec change** (recorded choice, `links.openspec: none`): this is a dependency pin bump
plus a release version bump. No capability requirement changes — the contract record is owned by
`contracts` (spine AD-4), the env key is set by the runtime, and `itr`'s own surfaces (`itr-cli`,
`itr-config-loading`, `itr-architecture`, `repo-harness`) are untouched.

## Done-when

`uv.lock` pins `cli-invocation-contract` at `c6c3ab5d…`, `make gates` is exit 0, `v0.2.0` is an
annotated tag on `main` whose GitHub Release carries the wheel + sdist, and an isolated tag
install prints `0.2.0 contract 0.2.0`.

## Evidence

| Claim | Command | Observed |
| --- | --- | --- |
| main clean before work | `git status --porcelain` on `main` | empty; `main` = `origin/main` = `2543c00` |
| worktree + branch | `bash scripts/worktree-guard.sh create OPS-001 contract-0-2-0-v0-2-0` | exit 0; `worktree=.worktrees/OPS-001/`, `branch=ticket/OPS-001-contract-0-2-0-v0-2-0` |
| contracts v0.2.0 objects | `GIT_TERMINAL_PROMPT=0 git -c credential.helper= ls-remote https://github.com/RandomGenericUsername/contracts 'refs/tags/v0.2.0*'` | `442fb9ab… refs/tags/v0.2.0`; `c6c3ab5d… refs/tags/v0.2.0^{}` |
| contract contents | `rg -n "CONTRACT_VERSION|DATA_VERSION"` in a `v0.2.0` checkout | `CONTRACT_VERSION = "0.2.0"`, `DATA_VERSION = 2`; `invocation-contract.json` lists `ICON_RENDERER__TEMPLATES__DIR` in `required` + `injected` |
| lock records the peeled commit | `uv lock`; `rg -n -A3 'name = "cli-invocation-contract"' uv.lock` | `Updated cli-invocation-contract v0.1.0 (48cf3cfe) -> v0.2.0 (c6c3ab5d)`; lock line `source = { git = "…/contracts?tag=v0.2.0#c6c3ab5d523d06210f8e87535c464d3190d005c0" }` |
| version test | `uv run pytest -q tests/unit/cli/test_version_flag.py` | `2 passed` |
| gates | `make gates` | exit 0; `289 passed` (test), `All checks passed!` (lint), `289 passed` (hermetic), lock current, docs-check exit 0 |
| workflow ↔ Makefile parity | `make ci-gates-parity` | exit 0; `PASS gates=['docs-check','hermetic','lint','lock-check','test'] jobs=[…] exempt=['ci-gates-parity','release']` |
| packaging | `uv build` | exit 0; `icon_templates_renderer-0.2.0-py3-none-any.whl` (48961 B) + `icon_templates_renderer-0.2.0.tar.gz` (124827 B) |
| annotated tag | `git cat-file -t v0.2.0`; `git rev-parse v0.2.0`; `git rev-parse 'v0.2.0^{commit}'` | `tag`; `04929197fcf99e1007deba0ca28728867565ddea`; `c23216d845fecbdecebda95104e3e040b6cdc56b` |
| anonymous fetch | `GIT_TERMINAL_PROMPT=0 git -c credential.helper= ls-remote https://github.com/RandomGenericUsername/icon-templates-renderer 'refs/tags/v0.2.0'` | exactly one line: `0492919… refs/tags/v0.2.0` |
| tag install | `UV_TOOL_DIR=… UV_TOOL_BIN_DIR=… uv tool install --force git+https://github.com/RandomGenericUsername/icon-templates-renderer@v0.2.0` → `itr --version` | exit 0; `0.2.0 contract 0.2.0` |
| CI on `main` (`c23216d`) | `gh run list …` / `gh run view 39655745761` | `completed`/`success` |
| CI on tag `v0.2.0` (`c23216d`) | `gh run view 39655754679 --json jobs` | `completed`/`success`; all six gates + `release` `success` |
| release assets | `gh release view v0.2.0 --json assets` | `isDraft:false`; `icon_templates_renderer-0.2.0-py3-none-any.whl` (48961 B) + `icon_templates_renderer-0.2.0.tar.gz` (124827 B) |

## Deviations

1. **`LIFECYCLE.md` names the guard flag with a leading double dash.** `bash scripts/worktree-guard.sh
   --check-clean` exits 2 with the script's usage line; the implemented spelling is
   `bash scripts/worktree-guard.sh check-clean` (exit 0). The `create` path runs the same
   `check_clean` internally, so the gate's intent held; the doc spelling is a harness defect, not
   fixed here (byte-pinned `mu` copy).
2. **`README.md`/`CHANGELOG.md` ship in the release commit** rather than a separate planning
   commit: the release ritual (AGENTS.md §6) requires the version bump and its changelog entry
   together, and the README's `--version`/pin examples would otherwise be stale. The ticket and
   `INDEX.md` are the separate planning commit (`0f60b53`).
3. **`dotfiles-v3` was not re-pinned** (it still addresses `itr` at `tag: v0.1.0`); that consumer
   bump is its own commit in that repo, per the repo boundary in AGENTS.md §6.

## Closeout

Closed 2026-10-21. Two commits on `main`: `0f60b53` (ticket + INDEX) and `c23216d`
(pin/version/lock/test/docs); annotated tag `v0.2.0` points at `c23216d`. No OpenSpec change was
opened — see "No OpenSpec change" above.
