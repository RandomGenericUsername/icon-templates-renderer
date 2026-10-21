# repo-birth

## Why

`icon-templates-renderer` is the first CLI extracted from `dotfiles-v3` in the CLI/split programme
(spine `SLICES.md` § S4). The package already exists and is green in-tree, but a repository is not
a valid extraction target until it is mu-strict from its first commit (spine **AD-12**: "harness
later" is exactly the failure the guide names).

Evidence: the package is pure Python and green in-tree — `src/cli-tools/icon-templates-renderer`
has a `pyproject.toml` with `oci-runtime` absent, no Dockerfile and 32 `test_*.py` modules.
Verify: `git -C /home/inumaki/Development/dotfiles-v3 ls-tree -r --name-only master --
src/cli-tools/icon-templates-renderer | grep -c '^tests/.*test_.*\.py$'` → `32`;
`git -C /home/inumaki/Development/dotfiles-v3 grep -n "oci_runtime" master --
src/cli-tools/icon-templates-renderer` → no hits.

Evidence: the split must preserve history with `git subtree split`, not a fresh-root import
(spine OPEN-8, `SLICES.md` § Slice template step 2).
Verify: `git -C /home/inumaki/Development/dotfiles-v3 subtree split -P
src/cli-tools/icon-templates-renderer -b split/icon-templates-renderer` → exit 0, branch tip
`47cab163`, 13 commits.

Evidence: the harness must be copied from `mu`, not re-authored (AD-12).
Verify: `diff -r /home/inumaki/Development/mu/_bmad _bmad` → empty; same for
`scripts/worktree-guard.sh`, `skills-lock.json`, `.agents/skills`, `.opencode`, `tickets/_template`,
`tickets/_fixtures`, `tickets/LIFECYCLE.md`.

## What Changes

- Create the public repo `RandomGenericUsername/icon-templates-renderer`, default branch `main`,
  from the `git subtree split` result of `src/cli-tools/icon-templates-renderer` (13 commits
  preserved).
- Install the mu-strict harness **byte-for-byte**: `scripts/worktree-guard.sh`, `skills-lock.json`,
  `_bmad/`, `.agents/skills/`, `.opencode/`, `tickets/_template/`, `tickets/_fixtures/`,
  `tickets/LIFECYCLE.md`.
- Add the repo contract: `AGENTS.md` (evidence rule verbatim, charter = pure-Python `itr`, ticket
  routing, never work on main, planning vs implementation, release ritual), `CLAUDE.md` →
  `AGENTS.md`.
- Add the work ledger: `tickets/INDEX.md` (counting rule header), `tickets/REQ-001-repo-birth/`.
- Add the OpenSpec root: `openspec/config.yaml` (evidence rules, repo context),
  `openspec/specs/{itr-architecture,itr-cli,itr-config-loading}/` (the imported capability specs)
  and this change.
- Add a fresh-clone Makefile (`sync`, `test`, `test-all`, `lint`, `format`, `check`, `hermetic`,
  `lock-check`, `docs-check`, `gates`, `gates-ci`, `build`, `install`, `clean`,
  `ci-gates-parity`), `.github/workflows/gates.yml` (one job per gate + `ci-gates-parity` + tag
  release), `scripts/ci-gates-parity.py`, MIT `LICENSE`, `README.md`, `CHANGELOG.md`,
  `.gitignore`.
- Keep packaging honest: the three sibling dependencies stay git-tag sources with compatibility
  ranges and a current committed `uv.lock`; `uv build` produces `icon_templates_renderer-0.1.0`
  sdist + wheel.

## Capabilities

- **New Capabilities:** `repo-harness` — the repo contract, ticket ledger, OpenSpec root, gate set
  and release ritual that make this repo a valid extraction target.

- **Modified Capabilities:** none. `itr-architecture`, `itr-cli` and `itr-config-loading` are
  imported as the existing behaviour; no render/list/validate/mapping/template behaviour changes.

## Non-goals (out of scope)

- **Not** rewiring `dotfiles-v3`: no consumer pin change, no deletion of
  `src/cli-tools/icon-templates-renderer`, no lock regeneration, no `deploy-coverage` change there.
  Those are the remaining S4 steps and a different repo/commit set.
- **Not** changing package behaviour: no new verb, flag, adapter or dependency.
- **Not** adding a container mode, Dockerfile, image-build verb or `oci-runtime` dependency —
  `itr` is pure Python by charter (spine AD-7).
- **Not** publishing to PyPI (spine AD-9): the release channel is a git tag plus GitHub Release
  artifacts.

## Impact

- New: `AGENTS.md`, `CLAUDE.md` (symlink), `Makefile`, `LICENSE`, `CHANGELOG.md`, `.gitignore`,
  `.github/workflows/gates.yml`, `scripts/ci-gates-parity.py`, `openspec/`, `tickets/`, and the
  copied harness trees.
- Modified: `pyproject.toml` (release metadata, sdist `only-include`, dependency ranges, dev
  group).
- Unchanged: `src/icon_templates_renderer/`, `tests/`, and every file in `dotfiles-v3`.
