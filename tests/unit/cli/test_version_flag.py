from __future__ import annotations

from importlib.metadata import version as dist_version

from cli_invocation_contract import CONTRACT_VERSION, DATA_VERSION
from typer.testing import CliRunner

from icon_templates_renderer.cli.main import app


def test_version_flag_reports_package_and_contract_version() -> None:
    result = CliRunner().invoke(app, ["--version"])

    assert result.exit_code == 0, result.output
    # The contract token is read from the package, never re-typed here, so a
    # contracts pin bump cannot leave this assertion silently stale.
    assert result.stdout.strip() == (
        f"{dist_version('icon-templates-renderer')} contract {CONTRACT_VERSION}"
    )


def test_pinned_contract_is_the_0_2_0_release() -> None:
    # The pin in pyproject.toml (`contracts` tag v0.2.0) is the only thing that
    # moves this; the explicit literals catch a silent rollback of the lock.
    assert CONTRACT_VERSION == "0.2.0"
    assert DATA_VERSION == 2
