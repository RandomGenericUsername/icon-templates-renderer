# icon-templates-renderer (`itr`)

SVG icon template renderer for the dotfiles CLI toolchain: reads an icons YAML plus a color
scheme, substitutes color placeholders in SVG templates, and writes the rendered icons. It also
lists, validates and edits the icon/mapping config surfaces.

The package is **pure Python** — no Docker, no container mode, no image-build verb, and no
`oci-runtime` dependency.

## Public surface

```console
itr render ICONS_YAML [--icon NAME] [--unsafe] [--template-dir DIR] \
                       [--color-scheme FILE] [--output-dir DIR] [--config FILE]
itr list ICONS_YAML [--icon NAME] [--config FILE]
itr validate ICONS_YAML [--icon NAME] [--config FILE]
itr mapping show|set|set-default|register ...
itr template analyze|scan|set-placeholder ...
itr --version
```

- `--version` prints `<package version> contract <contracts version>`, e.g.
  `0.2.0 contract 0.2.0`. The contract token comes from `cli_invocation_contract.CONTRACT_VERSION`,
  not from `cli-output`.
- Global flags: `--output-format {plain,rich,json}`, `-v/-vv/-vvv`, `-q`.
- Exit codes: `0` success, `1` a domain/config error with the message on stderr.

## Settings and path resolution

For each of `templates_dir`, `color_scheme` and `output_dir` the effective root is resolved with
this precedence (highest first):

1. CLI flag (`--template-dir`, `--color-scheme`, `--output-dir`)
2. env `ICON_RENDERER__<SECTION>__<KEY>` (e.g. `ICON_RENDERER__TEMPLATES__DIR`)
3. `settings.toml` field
4. discovery: `templates/` up to 3 levels / `colors.yaml` up to 3 levels; bundled default for
   `output_dir` (`/tmp/icon-templates-renderer`)
5. error naming the missing root and the levers that set it

`settings.toml` is found by `--config`, then `ICON_RENDERER_CONFIG_FILE_PATH`, then `./settings.toml`
up to 2 levels, then `$XDG_CONFIG_HOME/itr/settings.toml`, then the packaged defaults.

## Install

From a checkout (development):

```bash
make sync          # uv sync --frozen
make gates         # test + lint + hermetic + lock-check + docs-check
make build         # sdist + wheel in dist/
```

As a consumer, pin an immutable tag — never a path and never a branch:

```toml
# pyproject.toml
dependencies = ["icon-templates-renderer>=0.2.0"]

[tool.uv.sources]
icon-templates-renderer = { git = "https://github.com/RandomGenericUsername/icon-templates-renderer", tag = "v0.2.0" }
```

```bash
uv tool install "git+https://github.com/RandomGenericUsername/icon-templates-renderer@v0.2.0"
itr --version    # 0.2.0 contract 0.2.0
```

A published tag is never moved or deleted; a fix ships as a new tag.

## What `dotfiles-v3` pins

`dotfiles-v3` addresses this repo as `{name: itr, repo: <this repo>, tag: v0.1.0}` in
`provisioning/cli-tools.yaml`; the `cli_tools` role shallow-clones that tag and installs the tool
from the checkout. Provisioning owns the pin, clone and install invocation; it never edits this
repo (spine AD-10).

## Sibling pins

This repo consumes three sibling repos by immutable tag (spine AD-3):

| Distribution | Tag | Source |
| --- | --- | --- |
| `cli-output` | `v0.1.0` | `https://github.com/RandomGenericUsername/cli-output` |
| `config-assembler-engine` | `v0.1.0` | `https://github.com/RandomGenericUsername/config-assembler-engine` |
| `cli-invocation-contract` | `v0.2.0` | `https://github.com/RandomGenericUsername/contracts` |

## Release

Version in `pyproject.toml` + `CHANGELOG.md` entry → annotated tag `vX.Y.Z` → GitHub Actions
builds the sdist and wheel and attaches them to the GitHub Release. PyPI is not used.

## Repo harness

- `AGENTS.md` (with `CLAUDE.md` symlinked to it) is the operating contract: evidence rule,
  worktree discipline, planning-vs-implementation commits.
- `tickets/` is the work ledger (`INDEX.md`, `LIFECYCLE.md`, `_template/`).
- `openspec/` holds the specs and the change log (`config.yaml`, `specs/`, `changes/`).
- `scripts/worktree-guard.sh create <id> <slug>` makes `.worktrees/<id>/` on
  `ticket/<id>-<slug>`; never work on `main`.
- `.agents/skills/` + `skills-lock.json` and `_bmad/` are hash-pinned copies of the `mu` harness.

## License

MIT — see `LICENSE`.
