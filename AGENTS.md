# AGENTS.md — icon-templates-renderer operating contract

Canonical agent instructions for this repo. Claude (`CLAUDE.md` symlinks here), OpenCode, and all
BMAD/OpenSpec skills must follow this.

## 1. Evidence rule (hard requirement)

No suggestion "in the air". Every technical claim, recommendation, or design decision must carry testable evidence — at least one of:

- **Doc evidence:** file path + line range, or commit SHA, or URL + quoted section.
- **Prototype evidence:** a script/command in-repo that runs and prints the validating output. State the exact command and observed result.
- **Test evidence:** `command run → result` (exit code + key output). Failing-as-expected counts if it validates the claim.

Format: any non-trivial claim gets an `Evidence:` line and a `Verify:` line (how to reproduce in one command). If evidence doesn't exist yet, say `Evidence: MISSING — run <X> to produce it` and do not present the claim as fact.

## 2. Charter — `itr`, the SVG icon template renderer

- This repo owns one package: `icon-templates-renderer` (import package
  `icon_templates_renderer`, console script `itr`). It renders SVG icon templates from a color
  scheme and an icons YAML, and validates/edits the icon config surfaces.
- Public surface: the console script `itr` with `render`, `list`, `validate`, `mapping
  {show,set,set-default,register}` and `template {analyze,scan,set-placeholder}`; the Python
  entry point is `icon_templates_renderer.cli.main:app`.
  Evidence: `pyproject.toml` `[project.scripts]`; `src/icon_templates_renderer/cli/main.py`;
  `src/icon_templates_renderer/cli/mapping.py`; `src/icon_templates_renderer/cli/template.py`.
- **Pure Python rendering. No container mode and no build verb.** The package must not depend on
  `oci-runtime` and must not invoke another CLI. Dependencies are `typer`, `pydantic`, `pyyaml`,
  `ruamel.yaml`, `rich`, plus the pinned sibling packages `cli-output`,
  `config-assembler-engine` and `cli-invocation-contract`.
  Evidence: `pyproject.toml` `dependencies`; `rg -n "oci_runtime|subprocess" src/`.
- `cli-output` is presentation only; this repo does not own the runtime↔CLI invocation contract
  (it lives in the `contracts` repo as `cli-invocation-contract`, spine AD-4). The contract's
  conformance kit (`cli_invocation_contract.testkit`) is the source of invocation assertions; do
  not duplicate argv/env/artifact literals in tests.
- Siblings are consumed as immutable git tags, never a path and never `editable = true`
  (spine AD-3). The three git sources are declared in `[tool.uv.sources]` and locked in
  `uv.lock`.
- Settings discovery order is CLI flag → `ICON_RENDERER__…` env → `settings.toml` field →
  discovery (templates / color scheme) or bundled default (output dir) → error, recorded in
  `openspec/specs/itr-config-loading/spec.md`.

## 3. How we work here

- Read files, run commands (`rg`, `git log`, `uv`, `pytest`, `openspec validate`), paste results.
  Prefer executed output over recalled text.
- When findings contradict an earlier claim, state the discrepancy and trust the evidence.
- Keep changes small, verifiable, committable. A suite that is green only on the author's host is
  not green: tests are hermetic (empty `HOME` / `XDG_*`, foreign cwd), enforced by
  `tests/conftest.py` plus the canary in `tests/test_hermetic_canary.py`.
  Verify: `make hermetic` → exit 0.
- Do not add a container mode, Dockerfile, `oci-runtime` dependency or image-build verb to this
  repo. `itr` is pure Python by charter (spine AD-7).

## 4. OpenSpec + BMAD routing (via tickets)

- All work starts as a ticket in `tickets/` (`_template/`, vocab + rollup in `INDEX.md`, flow in
  `LIFECYCLE.md`). Triage with `/triage` (lanes in `tickets/_fixtures/router-lanes.md`).
- Broad scope (package charter, public API evolution, dependency policy) → BMAD. Installed
  skills are exactly the seven in `skills-lock.json`: `bmad`, `bmad-architecture`, `bmad-build`,
  `bmad-product-brief`, `bmad-spec`, `bmod-core-tools`, `bmod-method` — say so when a step needs a
  missing skill instead of improvising.
- Bounded slices (one proposal + spec + design + tasks) → OpenSpec
  (`/opsx-propose`, `/opsx-apply`, `/opsx-archive`). Artifact rules in
  `openspec/config.yaml` restate this evidence rule per artifact.
- Never work on main: `scripts/worktree-guard.sh create <id> <slug>` scaffolds
  `ticket/<id>-<slug>` + `.worktrees/<id>/`, and aborts when the tree is dirty. Record
  worktree/branch in the ticket.

## 5. Planning vs implementation

- Planning edits (tickets, `openspec/` changes, docs) and implementation changes (code, packaging,
  harness) land in **separate commits**.
- Never mix planning edits with implementation in one commit or one turn.

## 6. Release ritual

- Green gates on the ticket branch → version bumped in `pyproject.toml` + `CHANGELOG.md` →
  annotated tag `vMAJOR.MINOR.PATCH` → CI builds sdist + wheel and attaches them to the GitHub
  Release → consumer pin bump in its own commit.
- A published tag is never moved or deleted; a fix is a new tag. PyPI is not a channel.
- The first tag is `v0.1.0`, continuing the imported package's in-tree `0.1.0` version (spine
  AD-9: version continuity; versions never move backwards).
  Evidence: `CHANGELOG.md` `0.1.0`; `git tag -l`.

## 7. Gates

- `make gates` = `test lint hermetic lock-check docs-check`; `make build` produces the sdist and
  wheel. CI (`.github/workflows/gates.yml`) runs one job per gate target plus `ci-gates-parity`,
  which compares the workflow's job set against `GATES` in the `Makefile`.
  Verify: `make gates && make build` → exit 0; `make ci-gates-parity` → exit 0.
