# itr-architecture Specification

## Purpose
Defines the hexagonal architecture contracts for the icon-templates-renderer (ITR) tool: a real `ConfigResolverPort` backed by config-assembler, two discovery-only resolver ports, and `ResolvedRoots` replacing `PathOverrides` in the domain.

## Requirements

### Requirement: Real settings resolution via config-assembler
`ConfigResolverPort` SHALL be implemented by an `AssembledConfigResolver` that resolves `settings.toml` through five FILE strategies: `CliPathStrategy` (`--config`), `EnvPathStrategy` (`ICON_RENDERER_CONFIG_FILE_PATH`), `DirectoryTraversalStrategy` (`settings.toml`), `XdgStrategy` (`itr/settings.toml`) and the bundled `defaults/settings.toml`.

Source: `src/icon_templates_renderer/adapters/assembled_config_resolver.py`.

#### Scenario: bundled default settings
- **WHEN** no settings file is found via flag/env/traversal/XDG
- **THEN** the bundled `defaults/settings.toml` is used and `output_dir` resolves to `/tmp/icon-templates-renderer`

### Requirement: Override rules map CLI and env values onto settings
The resolver SHALL apply OverrideRules for `output.output_dir`, `output.verbosity`, `templates.dir` and `color_scheme.path` (each `{CLI, ENV}`), producing `AppSettings(output, templates, color_scheme)`.

Source: `src/icon_templates_renderer/adapters/assembled_config_resolver.py`.

#### Scenario: env overrides a settings field
- **WHEN** `ICON_RENDERER__TEMPLATES__DIR=/env/tpls` is set and `settings.toml` has a different `[templates] dir`
- **THEN** the assembled `templates.dir` is `/env/tpls`

### Requirement: TemplateDirResolver and ColorSchemeResolver ports
Two new `@runtime_checkable Protocol` ports SHALL provide discovery-only resolution returning `Path | None`: `TemplateDirResolverPort` (DirTraversal `templates` + Xdg `itr/templates`) and `ColorSchemeResolverPort` (traversal `colors.yaml` + Xdg `itr/colors.yaml`). They SHALL NOT consult env or CLI.

#### Scenario: every adapter satisfies its port
- **WHEN** `tests/unit/ports/test_contracts.py` runs
- **THEN** `isinstance`/signature/method-count assertions pass for both new adapters

#### Scenario: discovery returns None when nothing found
- **WHEN** no `templates/` dir and no XDG `itr/templates` exist
- **THEN** `TemplateDirResolverPort.resolve()` returns `None`

### Requirement: ResolvedRoots replaces PathOverrides
The domain SHALL carry a frozen `ResolvedRoots(template_root, color_scheme, output_root: Path | None)`, populated by the CLI orchestrator after settings + discovery. Requests SHALL carry `ResolvedRoots` (not `PathOverrides`). `PathResolutionService` SHALL be a pure joiner (`root / sub` then resolve; absolute passthrough); the 3-tier precedence SHALL live in the orchestrator, not the domain.

#### Scenario: render request carries resolved roots
- **WHEN** a render runs
- **THEN** `RenderRequest.roots` is a `ResolvedRoots` and the loader joins each group's relative dir under the corresponding root
