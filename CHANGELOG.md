# Changelog

Notable changes to the `icon-templates-renderer` repo. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow the git tags
(`vMAJOR.MINOR.PATCH`, annotated, never moved).

## [Unreleased]

## [0.2.0] - 2026-10-21

Contract re-pin release. No render/list/validate/mapping/template behaviour changes.

### Changed

- `cli-invocation-contract` (`contracts`) re-pinned `v0.1.0` → `v0.2.0` (annotated tag object
  `442fb9abdc73fa109115ba804911a10af9f4cad1`, peeled commit
  `c6c3ab5d523d06210f8e87535c464d3190d005c0`): `CONTRACT_VERSION = "0.2.0"`, `DATA_VERSION = 2`.
  `uv.lock` records the peeled commit.
- The `clis.itr` invocation record now requires `ICON_RENDERER__TEMPLATES__DIR` and injects it
  from `{templates_dir}`. The **runtime** sets that variable; `itr` already reads it
  (`--template-dir` > `ICON_RENDERER__TEMPLATES__DIR` > `settings.toml` > discovery), so no CLI
  code changed.
- `itr --version` now prints `0.2.0 contract 0.2.0`; `tests/unit/cli/test_version_flag.py`
  compares against `CONTRACT_VERSION` (imported, never re-typed) and asserts the pinned contract
  is `0.2.0` / data shape `2`.
- `README.md` version, consumer-pin and sibling-pin references updated to `v0.2.0`.

## [0.1.0] - 2026-10-20

First release. The package content is the in-tree `src/cli-tools/icon-templates-renderer`
package (version `0.1.0` there) imported with `git subtree split`, history preserved; the
version continues at `0.1.0` (spine AD-9: versions never move backwards).

### Added

- Repo harness copied byte-for-byte from `mu`: `scripts/worktree-guard.sh`, `skills-lock.json`,
  `_bmad/`, `.agents/skills/`, `.opencode/`, `tickets/_template/`, `tickets/_fixtures/`,
  `tickets/LIFECYCLE.md`.
- `Makefile` fresh-clone verbs (`sync`, `test`, `test-all`, `lint`, `format`, `check`, `hermetic`,
  `lock-check`, `docs-check`, `gates`, `gates-ci`, `build`, `install`, `clean`,
  `ci-gates-parity`), `.github/workflows/gates.yml`, `scripts/ci-gates-parity.py`.
- MIT `LICENSE`, `README.md`, `AGENTS.md`, `CLAUDE.md` symlink, ticket `REQ-001-repo-birth`,
  the OpenSpec change `repo-birth`, and the imported capability specs `itr-architecture`,
  `itr-cli`, `itr-config-loading`.

### Changed

- `pyproject.toml`: release metadata (`readme`, `license`, `license-files`, classifiers),
  `hatchling>=1.27`, an sdist `only-include` list so the harness trees stay out of the artifact,
  explicit compatibility ranges for the three sibling dependencies, and a dev group carrying
  `pytest`, `pytest-cov` and `ruff`.
- Sibling dependencies are consumed as immutable git tags (spine AD-3): `cli-output` `v0.1.0`,
  `config-assembler-engine` `v0.1.0`, `cli-invocation-contract` (`contracts`) `v0.1.0`.
  `uv.lock` records the resolved commits.
- `make lint` covers `src/` and `tests/` (the imported in-tree Makefile scope).

### Notes

- `itr` remains pure Python: no container mode, no Dockerfile, no image-build verb, and no
  `oci-runtime` dependency (spine AD-7).
- Suite: 288 tests, green in the ambient and hermetic environments.
