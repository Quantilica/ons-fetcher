"""Tests for ons-fetcher Typer plugin."""

from typer.testing import CliRunner

from ons_fetcher.plugin import app


def test_cli_list() -> None:
    """Test quantilica ons list."""
    runner = CliRunner()
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "carga" in result.output
    assert "carga-energia" in result.output


def test_cli_convert_help() -> None:
    """Test quantilica ons convert --help."""
    runner = CliRunner()
    result = runner.invoke(app, ["convert", "--help"])
    assert result.exit_code == 0
    assert "--lake" in result.output
