---
id: REQ-001
title: "Birth the icon-templates-renderer repo (mu-strict, itr) and cut v0.1.0"
kind: requirement
status: done
lane: 3
links:
  openspec: repo-birth
  bmad: none
worktree: .worktrees/REQ-001/
branch: ticket/REQ-001-closeout
---

# Birth the icon-templates-renderer repo (mu-strict, itr) and cut v0.1.0

## Requirement

Slice **S4a** of the CLI-repos split SHALL create
`RandomGenericUsername/icon-templates-renderer` as a public repo whose root is the imported
`src/cli-tools/icon-templates-renderer` package, preserve that package's history with
`git subtree split`, install the `mu` harness byte-for-byte, and cut the repo's first tag
(`v0.1.0`) only after the gates, packaging and CI exist.

The package remains **pure-Python rendering**: this slice changes no render/list/validate/mapping/
template behaviour, adds no dependency outside the three already-pinned siblings, and adds no
container mode, Dockerfile, image-build verb or `oci-runtime` dependency (spine AD-7). `dotfiles-v3`
is not modified — the consumer rewire and the in-tree deletion are the remaining S4 steps in that
repo.

## Acceptance

- [x] The repo exists, is **public**, and its `main` carries the imported subtree commits.
  Verify: `gh api repos/RandomGenericUsername/icon-templates-renderer --jq .private` → `false`;
  `git log --oneline | wc -l` → 13 imported commits before the scaffold.
- [x] The harness is byte-identical to `mu` at every copied path.
  Verify: `diff -r` per path (see the evidence table) → empty, exit 0.
- [x] `AGENTS.md` carries the evidence rule and this repo's charter; `CLAUDE.md` is a symlink.
  Verify: `rg -c "Evidence:|Verify:" AGENTS.md` → ≥ 2; `test -L CLAUDE.md` → exit 0.
- [x] `tickets/INDEX.md` lists this ticket with the same status as the frontmatter, and the
  OpenSpec change validates strictly.
  Verify: `openspec validate --specs --strict` → exit 0; `openspec validate repo-birth --strict`
  → exit 0 **before** the change is archived (after `openspec archive repo-birth` on 2026-10-21
  the name resolves only as `openspec/changes/archive/2026-10-21-repo-birth`, so the reproducible
  check is `openspec validate --specs --strict` → `4 passed`).
- [x] A fresh clone passes `make sync && make gates && make build` and the suite count is 288.
  Verify: `uv sync --frozen && uv run pytest -q` → `288 passed`; `make gates` → exit 0;
  `ls dist/icon_templates_renderer-0.1.0-*` → wheel + sdist.
- [x] `.github/workflows/gates.yml` exists and its job set equals `GATES` (plus declared CI-only
  jobs); the first run on `main` is green.
  Verify: `make ci-gates-parity` → `PASS ...`; `gh run list -R RandomGenericUsername/icon-templates-renderer
  --limit 1 --json status,conclusion` → `completed` / `success`.
- [x] Annotated tag `v0.1.0` exists on the released commit, is anonymously fetchable, and its
  GitHub Release carries the wheel + sdist.
  Verify: `GIT_TERMINAL_PROMPT=0 git -c credential.helper= ls-remote
  https://github.com/RandomGenericUsername/icon-templates-renderer 'refs/tags/v0.1.0'` → exactly
  one line; `gh release view v0.1.0 --json assets --jq '.assets[].name'` → both artifacts.
- [x] `git status --porcelain` is empty in both repos; `dotfiles-v3` `master` is at the same SHA
  as before the slice.
  Verify: `git status --porcelain` → empty; `git -C /home/inumaki/Development/dotfiles-v3 rev-parse
  master` → `c4056631eac63aec15c450851312b77624b8bfed`.

## Out of scope

- Rewiring `dotfiles-v3` (`provisioning/cli-tools.yaml`, `roles/cli_tools`, `roles/verify`,
  `deploy-coverage`) to the `{name, repo, tag}` pin and deleting
  `src/cli-tools/icon-templates-renderer` — those are the remaining S4 steps in that repo.
- Any package behaviour change, dependency change, or invocation-contract content.
- A container mode / Dockerfile / image build (spine AD-7: `itr` has none).
- PyPI publication; the channel is the git tag plus GitHub Release artifacts.

## Evidence

| Claim | Command | Observed |
| --- | --- | --- |
| repo is public | `gh api repos/RandomGenericUsername/icon-templates-renderer --jq .private` | `false` |
| history preserved | `git rev-list --count split/icon-templates-renderer` (dotfiles) | `13`; split tip `47cab163a0dd9e8e2cb6235d1ab25e57e59f91b8` |
| harness byte-identical | `diff -r mu/<path> <path>` for `_bmad`, `.agents/skills`, `.opencode`, `scripts/worktree-guard.sh`, `skills-lock.json`, `tickets/_template`, `tickets/_fixtures`, `tickets/LIFECYCLE.md` | `IDENTICAL` × 8, exit 0 |
| evidence rule present | `rg -c "Evidence:\|Verify:" AGENTS.md`; `test -L CLAUDE.md` | `6`; exit 0 |
| specs/change valid | `openspec validate --specs --strict`; `openspec validate repo-birth --strict` | 3 passed; `Change 'repo-birth' is valid` |
| suite | `uv run pytest -q` | `288 passed` |
| gates | `make gates` | exit 0; `288 passed` (test and hermetic), `All checks passed!`, lock current |
| packaging | `uv build` | exit 0; `icon_templates_renderer-0.1.0-py3-none-any.whl` + `.tar.gz` |
| fresh clone | clone → `make sync && make gates && make build` | all exit 0; `288 passed` ×2; both artifacts in `dist/` |
| CI parity | `make ci-gates-parity` | `PASS gates=[...] jobs=[...] exempt=[...]` |
| first CI run (main `92895a0`) | `gh run view 39530859918 --json jobs` | test/hermetic/docs-check/lock-check/ci-gates-parity/lint `success`; `release` skipped |
| tag CI run (`v0.1.0`) | `gh run view 39531008690 --json jobs` | all six gates + `release` `success` |
| annotated tag | `git cat-file -t v0.1.0`; `git rev-parse v0.1.0`; `git rev-parse 'v0.1.0^{commit}'` | `tag`; `09271f64375ccfb2eeb36dc3c6b81a4b55b2bdd6`; `92895a068b7117832d0cbf2a5bfb158ca3fda68c` |
| anonymous fetch | `GIT_TERMINAL_PROMPT=0 git -c credential.helper= ls-remote https://github.com/RandomGenericUsername/icon-templates-renderer 'refs/tags/v0.1.0'` | exactly one line (`09271f6…`); peeled line `92895a0… refs/tags/v0.1.0^{}` |
| release artifacts | `gh release view v0.1.0 --json assets --jq '.assets[].name'` | wheel + sdist |
| tag install | `UV_TOOL_DIR=… UV_TOOL_BIN_DIR=… uv tool install --force git+…@v0.1.0` → `itr --version` | `0.1.0 contract 0.1.0` |
| dotfiles untouched | `git -C /home/inumaki/Development/dotfiles-v3 rev-parse master`; `git status --porcelain` | `c4056631eac63aec15c450851312b77624b8bfed`; empty |

## Deviations from the slice text

1. **Template-integration tests now read a vendored fixture tree.** Two tests
   (`TestRoundTripRealTemplates`, `TestScanIntegration`) resolved
   `dotfiles/assets/icon-templates` by walking up to a `dotfiles/` sibling, which cannot exist in a
   standalone checkout. They now read `tests/fixtures/icon-templates/` (117 tracked SVGs copied as
   test input, never as the asset's source of truth). `_worktree_root()` was replaced by
   `_templates_root()`.
2. **Two formatting fixes to keep the in-tree lint scope (`src` + `tests`) green**: ruff import
   order in `src/icon_templates_renderer/cli/mapping.py` (auto-fix) and one over-long call in
   `tests/unit/adapters/test_ruamel_mapping_writer.py` (wrapped). No behaviour change; the suite
   stayed at 288 passed.
3. **Strict OpenSpec validation** required splitting the imported `itr-architecture` requirement
   "Real settings resolution via config-assembler" (over 500 characters) into two requirements and
   adding the missing source citation. Behaviour text is unchanged.
4. **No testkit migration was needed.** The imported tests carry no local argv/env/artifact
   literals to replace (only `tests/unit/cli/test_version_flag.py` imports
   `CONTRACT_VERSION`). Evidence: `rg -n "testkit" src tests` → no hits.
5. **`requires-python = ">=3.14"` and `ruff target-version = "py314"` are kept** from the in-tree
   package (host interpreter 3.14.7). The spine's stack table says ">=3.12 unchanged in all six",
   which was already stale for this package; changing it is out of scope for a birth slice.

## Closeout

Closed 2026-10-20. Two commits on `main` in the fresh clone (birth-worktree exception, as in the
sibling births): `dacbd72` planning (ticket + OpenSpec) and `92895a0` implementation (harness,
gates, packaging), then this closeout commit. Tag `v0.1.0` points at `92895a0`. Every later item
uses `bash scripts/worktree-guard.sh create <id> <slug>`.

The remaining S4 steps live in `dotfiles-v3`: the `{name, repo, tag}` manifest entry, role/verify
mirrors, `deploy-coverage` shape assertions, and the in-tree deletion.

### Re-verified and archived 2026-10-21

Re-ran the whole gate set before ticking anything, in the guard-created worktree
`.worktrees/REQ-001/` on `ticket/REQ-001-closeout`, then archived the OpenSpec change so the
ticket's last open link closes.

| Claim | Command | Observed |
| --- | --- | --- |
| tree clean before work | `git status --porcelain` on `main` | empty; `main` = `d28de8c` = `origin/main` |
| repo public, default `main` | `gh api repos/RandomGenericUsername/icon-templates-renderer --jq '{private,default_branch}'` | `{"default_branch":"main","private":false}` |
| gate set green | `make gates` | exit 0; `288 passed` (test), `All checks passed!` (lint), `288 passed` (hermetic), lock current, docs-check ok |
| workflow ↔ Makefile parity | `make ci-gates-parity` | exit 0; `PASS gates=['docs-check','hermetic','lint','lock-check','test'] jobs=[...] exempt=['ci-gates-parity','release']` |
| packaging | `uv build` | exit 0; `icon_templates_renderer-0.1.0-py3-none-any.whl` + `icon_templates_renderer-0.1.0.tar.gz` |
| tag install from the public URL | `UV_TOOL_DIR=… UV_TOOL_BIN_DIR=… uv tool install --force git+https://github.com/RandomGenericUsername/icon-templates-renderer@v0.1.0` → `itr --version` | exit 0; `0.1.0 contract 0.1.0` |
| release carries both artifacts | `gh release view v0.1.0 --json assets` | `draft:false`; `icon_templates_renderer-0.1.0-py3-none-any.whl` (48954 B) + `icon_templates_renderer-0.1.0.tar.gz` (124251 B) — no upload needed |
| recent CI runs green | `gh run list -R … --limit 3 --json status,conclusion` | `d28de8c`/`92895a0` (main) and `92895a0` (`v0.1.0`) all `completed`/`success` |
| change valid before archive | `openspec validate repo-birth --strict` | `Change 'repo-birth' is valid` |
| change archived | `openspec archive repo-birth -y` | `Change 'repo-birth' archived as '2026-10-21-repo-birth'`; specs `+4` → `repo-harness` created |
| specs valid after archive | `openspec validate --specs --strict` | `4 passed, 0 failed` (after writing the `repo-harness` Purpose the archive leaves as `TBD`) |
| no active changes left | `openspec list --json` | `{"changes":[]}` |
