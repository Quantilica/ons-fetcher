"""Typer plugin for quantilica-cli integration."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

import typer
from quantilica.cli.sdk import FetcherApp, make_resolve_groups
from quantilica.core.sync import FreshnessPolicy

from .catalog import GROUP_ALIASES, GROUPS, catalog_rows, list_datasets
from .storage import DataRepository

resolve_groups = make_resolve_groups(GROUPS, GROUP_ALIASES)


def path_builder(
    output_dir: Path, entry: dict[str, Any], last_modified: dt.date | None
) -> Path:
    """Build local storage path for a dataset entry."""
    return DataRepository(output_dir).path_for_entry(entry, last_modified=last_modified)


fetcher = FetcherApp(
    name="ons",
    help="Coletor e conversor Lake Hive de dados abertos do ONS",
    groups_dict=GROUPS,
    aliases_dict=GROUP_ALIASES,
    list_datasets=list_datasets,
    path_builder=path_builder,
    default_output=Path("/data/ons"),
    freshness_policy=FreshnessPolicy.HEAD_OR_MANIFEST,
)


def convert(
    input_dir: Path,
    lake_dir: Path,
    *,
    dataset: list[str] | None = None,
    force: bool = False,
) -> Any:
    """Converte arquivos brutos de ons para o lake Hive (Parquet)."""
    try:
        from ons_fetcher import lake
    except ImportError as exc:
        raise RuntimeError(
            "Conversão para o lake requer o extra 'analysis'. "
            "Instale com: quantilica install ons --extra analysis"
        ) from exc
    return lake.converter.convert(input_dir, lake_dir, datasets=dataset, force=force)


def catalogo(
    grupo: str | None = typer.Argument(None, help="Grupo, alias ou macro-alias"),
    tier: str | None = typer.Option(None, help="r1 (baixa hoje) ou listed"),
    as_json: bool = typer.Option(False, "--json", help="Saída em JSON"),
) -> None:
    """Mostra o catálogo completo de conjuntos (R1 e listados, sem rede)."""
    rows = catalog_rows(grupo, tier)
    if as_json:
        typer.echo(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    for row in rows:
        typer.echo(
            f"{row['group']:<12} {row['tier']:<6} {row['granularity']:<9} "
            f"{row['slug']}  ({row['s3_dir']})"
        )
    n_r1 = sum(1 for r in rows if r["tier"] == "r1")
    typer.echo(f"\n{len(rows)} conjunto(s): {n_r1} R1, {len(rows) - n_r1} listados.")


def discover_cmd(
    as_json: bool = typer.Option(False, "--json", help="Saída em JSON"),
    fail_on_change: bool = typer.Option(
        False, "--fail-on-change", help="Sai com código 1 se houver novidade"
    ),
) -> None:
    """Detecta conjuntos e períodos novos do ONS em relação ao catálogo."""
    from .discover import discover

    report = discover()
    if as_json:
        typer.echo(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        typer.echo(f"{report.known} conjunto(s) do catálogo encontrados no CKAN.")
        for pkg in report.new_packages:
            typer.echo(f"NOVO     {pkg['ckan_slug']} ({pkg['s3_dir']}): {pkg['title']}")
        for slug in report.removed_packages:
            typer.echo(f"REMOVIDO {slug}")
        for moved in report.moved_dirs:
            typer.echo(
                f"MOVIDO   {moved['ckan_slug']}: "
                f"{moved['catalogo']} -> {moved['atual']}"
            )
        for slug, periods in report.new_periods.items():
            typer.echo(
                f"PERÍODOS {slug}: {periods[0]} .. {periods[-1]} ({len(periods)})"
            )
        if not report.has_changes:
            typer.echo("Sem novidades em relação ao catálogo.")
    if fail_on_change and report.has_changes:
        raise typer.Exit(1)


fetcher.attach_command(catalogo, name="catalogo")
fetcher.attach_command(discover_cmd, name="discover")
fetcher.command_convert(convert)
fetcher.command_pipeline(convert)


app = fetcher.app
