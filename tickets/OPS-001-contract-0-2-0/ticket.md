---
id: OPS-001
title: "Re-pin cli-invocation-contract (contracts) v0.2.0 and release itr v0.2.0"
kind: ops-task
status: in-progress
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
