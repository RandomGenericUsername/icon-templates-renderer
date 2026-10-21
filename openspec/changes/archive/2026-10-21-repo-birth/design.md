# Design — repo birth

## Decisions

### D1. History comes from `git subtree split`, not a fresh root commit

The in-tree package has 13 commits, including the S0b hermetic-fixture commit, the S1/S2
sibling-pin commits and the invocation-contract `--version` commit. A fresh import would make the
extracted repo's first commit unrelated to the code's history and would lose those "why" records.
`git subtree split -P src/cli-tools/icon-templates-renderer` writes a branch whose tree is the
package directory and whose commits are the ones that touched it.

Evidence: `git -C /home/inumaki/Development/dotfiles-v3 rev-list --count
split/icon-templates-renderer` → `13`; the split tip is `47cab163`.
Verify: `git log --oneline | wc -l` in this repo → `13` before the scaffold commit.

Consequence: the split branch was pushed as `main` in one push, so `main` starts at the imported
tree, and the scaffold lands one merge later.

### D2. Harness files are copied, not re-authored

AD-12 requires the same `worktree-guard.sh` and the same `skills-lock.json` hashes as `mu`. The
copy set is exactly: `scripts/worktree-guard.sh`, `skills-lock.json`, `_bmad/`, `.agents/skills/`,
`.opencode/`, `tickets/_template/`, `tickets/_fixtures/`, `tickets/LIFECYCLE.md`.
`tickets/INDEX.md` is repo-specific (an empty ledger needs the counting rule, not `mu`'s 100+
rows), and `AGENTS.md` is retargeted but keeps the evidence rule verbatim.

Evidence: `diff` per path against `mu` is empty (ticket evidence table).
Verify: `diff -r /home/inumaki/Development/mu/_bmad _bmad && diff
/home/inumaki/Development/mu/skills-lock.json skills-lock.json`.

### D3. One branch exception, then the guard

The guard refuses to create a worktree from a dirty tree, and this repo has no `main` history to
branch from before the first scaffold commit. The scaffold commits are therefore made on `main` in
the fresh clone (the slice instruction), and every later item uses
`bash scripts/worktree-guard.sh create <id> <slug>`.

Evidence: `scripts/worktree-guard.sh` is copied and executable; the ticket records
`worktree: none` and the exception.
Verify: `bash scripts/worktree-guard.sh check-clean` → exit 0 on a clean tree.

### D4. The Makefile's `GATES` is the single gate list; CI is compared to it

The workflow has one job per gate so a failure names the gate, but a hand-maintained job list
drifts. `scripts/ci-gates-parity.py` parses `GATES` from the `Makefile` and the job keys from the
workflow and fails on any unmatched entry in either direction. CI-only jobs (`ci-gates-parity`,
`release`) are declared with a reason; a stale declaration fails.

Evidence: `make ci-gates-parity` → `PASS gates=[...] jobs=[...] exempt=[...]`.
Verify: `make ci-gates-parity`.

### D5. Hermetic means hermetic, not "green on this host"

AD-8 is already implemented in the imported tests (`tests/conftest.py` +
`tests/test_hermetic_canary.py`). The Makefile adds `hermetic`, which runs the suite with `HOME`
and all four `XDG_*` roots pointed at fresh temp dirs; the fixture does the `chdir`. `make gates`
includes it, so a host-dependent test cannot pass a release gate.

Evidence: the canary asserts `XDG_CONFIG_HOME` is under the pytest tmp root.
Verify: `make hermetic` → exit 0 with the same count as `make test`.

### D6. No container job, because `itr` has no container mode

The sibling `oci-runtime` workflow carries a container-engine skip report. `itr` renders SVGs in
process: there is no Dockerfile, no `install` verb and no `oci-runtime` dependency, so a container
job would either be an empty pass or invent a capability the package does not have. The workflow
keeps exactly the five gate jobs plus parity and release.

Evidence: `rg -n "oci_runtime|docker" src/icon_templates_renderer` → no hits;
`pyproject.toml` `dependencies` lists no `oci-runtime`.
Verify: `make ci-gates-parity` → the parsed job set is exactly `GATES` + the two declared jobs.

## Verification plan

| Decision | Command | Expected |
| --- | --- | --- |
| D1 | `git log --oneline \| wc -l` | `13` imported commits before the scaffold |
| D2 | `diff -r <mu-path> <path>` for each copied path | empty output, exit 0 |
| D3 | `bash scripts/worktree-guard.sh check-clean` | exit 0 |
| D4 | `make ci-gates-parity` | `PASS ...`, exit 0 |
| D5 | `make hermetic` | exit 0, same test count as `make test` |
| D6 | `make ci-gates-parity` | `jobs` has no container job |
| Packaging | `uv lock --check && uv build` | exit 0; `dist/icon_templates_renderer-0.1.0-{whl,tar.gz}` |
| Release | `git ls-remote --tags origin v0.1.0` | exactly one line (tag object) + peeled commit |
