# Changelog

Notable changes to the `icon-templates-renderer` repo. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow the git tags
(`vMAJOR.MINOR.PATCH`, annotated, never moved).

## [Unreleased]

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
