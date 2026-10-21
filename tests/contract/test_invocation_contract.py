"""This repo's own side of the `itr` invocation contract (spine AD-4).

`cli_invocation_contract` owns the record (argv template, required env keys,
artifact shape). This module owns the proof that *this* checkout satisfies it: it
renders the record's argv/env from fixture values, runs the installed `itr`
console script for real with a scrubbed environment, and delegates the assertion
to ``assert_cli_writes_artifacts`` from the pinned conformance kit. Invocation
literals are never re-typed here (AGENTS.md §2) — the record is the source.

The fixture mirrors the provisioned shape: a mappings YAML with group `battery`,
a variant whose template is `status-bar/battery/battery-0/default/icon.svg`, a
palette `colors.yaml`, and a templates dir holding that SVG with the
`{{COLOR_FOREGROUND}}` placeholder. The mappings path is a regular file, so the
optional `{mappings_file}?` placeholder is present — the production branch of the
record (CONTRACT.md § `itr`).

Nothing here skips: a missing console script is a failure that names the fix, so
a green CI run cannot mean "the contract was never exercised".
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pytest
from cli_invocation_contract import get
from cli_invocation_contract.testkit import (
    assert_cli_writes_artifacts,
    assert_consumer_invocation,
)

CLI = "itr"

_MAPPINGS = (
    "battery:\n"
    "  color_mappings:\n"
    "    COLOR_FOREGROUND: foreground\n"
    "  variants:\n"
    "    - name: battery-0\n"
    "      template: status-bar/battery/battery-0/default/icon.svg\n"
    "      output: battery-0.svg\n"
)
_PALETTE = (
    "special:\n"
    '  background: "#1a1a2e"\n'
    '  foreground: "#e0e0e0"\n'
    '  cursor: "#e0e0e0"\n'
    "colors:\n"
    '  - "#1a1a2e"\n'
    '  - "#e94560"\n'
)
_TEMPLATE = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">\n'
    '  <path fill="{{COLOR_FOREGROUND}}" d="M0 0h24v24H0z"/>\n'
    "</svg>\n"
)

_PLACEHOLDER_RE = re.compile(r"^\{([a-z0-9_]+)\}(\?)?$")


def _render(token: str, values: Mapping[str, str]) -> str | None:
    """Render one record template token; `None` means an absent optional token."""
    match = _PLACEHOLDER_RE.match(token)
    if match is None:
        return token
    name, optional = match.groups()
    if name in values:
        value = values[name]
        if not value.strip():
            raise AssertionError(f"placeholder {name!r} resolved to an empty value")
        return value
    if optional:
        return None
    raise AssertionError(
        f"record placeholder {name!r} has no value; supplied one of {sorted(values)}"
    )


def _argv(record: Mapping[str, Any], values: Mapping[str, str]) -> list[str]:
    """The record's argv with its placeholders filled from `values`."""
    argv: list[str] = [_console_script(record["binary"]).as_posix()]
    for token in record["argv"]:
        rendered = _render(token, values)
        if rendered is not None:
            argv.append(rendered)
    return argv


def _env(record: Mapping[str, Any], values: Mapping[str, str]) -> dict[str, str]:
    """The record's injected env; a required key the record never injects fails loudly."""
    env: dict[str, str] = {}
    for key, template in record["env"]["injected"].items():
        rendered = _render(template, values)
        if rendered is None:
            raise AssertionError(f"record injects {key!r} as an absent optional")
        env[key] = rendered
    missing = sorted(set(record["env"]["required"]) - set(env))
    if missing:
        raise AssertionError(
            f"record requires {missing} but does not inject them; this test must supply "
            "those values before running the CLI"
        )
    return env


def _console_script(binary: str) -> Path:
    """Locate the console script of *this* interpreter's env first, then PATH."""
    candidates = (Path(sys.executable).with_name(binary), shutil.which(binary))
    for candidate in candidates:
        if candidate is not None and Path(candidate).is_file():
            return Path(candidate)
    pytest.fail(
        f"the `{binary}` console script is not next to {sys.executable} nor on PATH; "
        "run `make sync` first"
    )


def _scrubbed_env(
    root: Path, record: Mapping[str, Any], values: Mapping[str, str]
) -> dict[str, str]:
    """A minimal env: host HOME/XDG/ICON_RENDERER* cannot leak into the child."""
    for name in ("home", "config", "cache", "data", "state", "tmp"):
        (root / name).mkdir()
    return {
        "PATH": os.pathsep.join([str(Path(sys.executable).parent), "/usr/bin", "/bin"]),
        "HOME": str(root / "home"),
        "XDG_CONFIG_HOME": str(root / "config"),
        "XDG_CACHE_HOME": str(root / "cache"),
        "XDG_DATA_HOME": str(root / "data"),
        "XDG_STATE_HOME": str(root / "state"),
        "TMPDIR": str(root / "tmp"),
        "LANG": "C.UTF-8",
        "NO_COLOR": "1",
        "PYTHONNOUSERSITE": "1",
        **{key: str(value) for key, value in _env(record, values).items()},
    }


def _write_fixture(root: Path) -> tuple[Path, Path]:
    """Write the provisioned-shape fixture; return `(mappings_file, output_dir)`."""
    templates = root / "templates"
    template = templates / "status-bar" / "battery" / "battery-0" / "default" / "icon.svg"
    template.parent.mkdir(parents=True)
    template.write_text(_TEMPLATE, encoding="utf-8")

    (root / "colors.yaml").write_text(_PALETTE, encoding="utf-8")

    mappings = root / "icons.yaml"
    mappings.write_text(_MAPPINGS, encoding="utf-8")

    output_dir = root / "output"
    output_dir.mkdir()
    return mappings, output_dir


def test_itr_render_writes_the_contract_artifacts(tmp_path: Path) -> None:
    """The recorded invocation runs and writes the artifacts the record requires."""
    record = get(CLI)

    root = tmp_path / "contract"
    mappings, output_dir = _write_fixture(root)
    values = {
        "mappings_file": str(mappings),
        "output_dir": str(output_dir),
        "palette_colors_yaml": str(root / "colors.yaml"),
        "templates_dir": str(root / "templates"),
    }

    env = _scrubbed_env(root, record, values)
    argv = _argv(record, values)

    # The invocation this test runs is the one the record describes (argv template
    # walked, every required env key present, injected values non-empty).
    assert_consumer_invocation(record, CLI, argv, env)

    def run() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            argv,
            cwd=output_dir,
            env=env,
            capture_output=True,
            text=True,
            timeout=float(record["timeout"]),
            check=False,
        )

    artifacts = assert_cli_writes_artifacts(record, CLI, run, output_dir)

    assert artifacts, "the contract run exited 0 but matched no artifact"
    rendered = (output_dir / "battery-0.svg").read_text(encoding="utf-8")
    assert "{{COLOR_FOREGROUND}}" not in rendered, "artifact kept an unsubstituted placeholder"
    assert "#e0e0e0" in rendered, "artifact does not carry the palette foreground colour"
