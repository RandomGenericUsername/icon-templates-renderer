---
id: REQ-001
title: "Birth the icon-templates-renderer repo (mu-strict, itr) and cut v0.1.0"
kind: requirement
status: in-progress
lane: 3
links:
  openspec: repo-birth
  bmad: none
worktree: none
branch: none
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

- [ ] The repo exists, is **public**, and its `main` carries the imported subtree commits.
  Verify: `gh api repos/RandomGenericUsername/icon-templates-renderer --jq .private` → `false`;
  `git log --oneline | wc -l` → 13 imported commits before the scaffold.
- [ ] The harness is byte-identical to `mu` at every copied path.
  Verify: `diff -r` per path (see the evidence table) → empty, exit 0.
- [ ] `AGENTS.md` carries the evidence rule and this repo's charter; `CLAUDE.md` is a symlink.
  Verify: `rg -c "Evidence:|Verify:" AGENTS.md` → ≥ 2; `test -L CLAUDE.md` → exit 0.
- [ ] `tickets/INDEX.md` lists this ticket with the same status as the frontmatter, and the
  OpenSpec change validates strictly.
  Verify: `openspec validate --specs --strict` → exit 0; `openspec validate repo-birth --strict`
  → exit 0.
- [ ] A fresh clone passes `make sync && make gates && make build` and the suite count is 288.
  Verify: `uv sync --frozen && uv run pytest -q` → `288 passed`; `make gates` → exit 0;
  `ls dist/icon_templates_renderer-0.1.0-*` → wheel + sdist.
- [ ] `.github/workflows/gates.yml` exists and its job set equals `GATES` (plus declared CI-only
  jobs); the first run on `main` is green.
  Verify: `make ci-gates-parity` → `PASS ...`; `gh run list -R RandomGenericUsername/icon-templates-renderer
  --limit 1 --json status,conclusion` → `completed` / `success`.
- [ ] Annotated tag `v0.1.0` exists on the released commit, is anonymously fetchable, and its
  GitHub Release carries the wheel + sdist.
  Verify: `GIT_TERMINAL_PROMPT=0 git -c credential.helper= ls-remote
  https://github.com/RandomGenericUsername/icon-templates-renderer 'refs/tags/v0.1.0'` → exactly
  one line; `gh release view v0.1.0 --json assets --jq '.assets[].name'` → both artifacts.
- [ ] `git status --porcelain` is empty in both repos; `dotfiles-v3` `master` is at the same SHA
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

## Evidence (filled during the slice)

See `openspec/changes/repo-birth/tasks.md` for the task-level commands and results.
