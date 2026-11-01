"""Dataset catalog for ons-fetcher."""

from __future__ import annotations

import datetime as dt
from typing import Any

from ._catalog_base import (
    DatasetEntry,
    GroupInfo,
    annual_datasets,
    monthly_datasets,
    static_dataset,
)
from .constants import R1_DATASETS_META, S3_BASE_URL

__all__ = [
    "DatasetEntry",
    "GroupInfo",
    "GROUPS",
    "GROUP_ALIASES",
    "list_datasets",
]


def _build_entries_for_dataset(slug: str, meta: dict[str, Any]) -> list[DatasetEntry]:
    """Build dataset entries based on metadata descriptor."""
    group = meta["group"]
    s3_dir = meta["s3_dir"]
    prefix = meta["prefix"]
    name = meta["name"]
    granularity = meta["granularity"]
    current_year = dt.date.today().year

    if granularity == "annual":
        start_year = meta.get("start_year") or 2000
        url_tmpl = f"{S3_BASE_URL}/{s3_dir}/{prefix}_{{year}}.parquet"
        name_tmpl = f"{name} ({{year}})"
        return annual_datasets(
            group=group,
            base_id=slug,
            name_template=name_tmpl,
            url_template=url_tmpl,
            start_year=start_year,
            end_year=current_year,
            ext="parquet",
        )
    elif granularity == "monthly":
        start_year = meta.get("start_year") or 2020
        url_tmpl = f"{S3_BASE_URL}/{s3_dir}/{prefix}_{{year}}_{{month}}.parquet"
        name_tmpl = f"{name} ({{year}}-{{month}})"
        return monthly_datasets(
            group=group,
            base_id=slug,
            name_template=name_tmpl,
            url_template=url_tmpl,
            start_year=start_year,
            end_year=current_year,
            ext="parquet",
        )
    elif granularity == "static":
        url = f"{S3_BASE_URL}/{s3_dir}/{prefix}.parquet"
        return [
            static_dataset(
                group=group,
                id=slug,
                name=name,
                url=url,
                ext="parquet",
            )
        ]
    return []


def _build_all_groups() -> dict[str, GroupInfo]:
    """Assemble all dataset groups."""
    group_names: dict[str, str] = {
        "carga": "Carga e Demanda do SIN",
        "hidrologia": "Hidrologia, EAR e ENA",
        "geracao": "Geração e Fator de Capacidade",
        "precos": "Preços e Custo Marginal de Operação (CMO)",
        "intercambio": "Intercâmbio e Balanço de Energia",
        "cadastros": "Cadastros de Usinas e Reservatórios",
        "programacao": "Programação da Operação (R2)",
        "indicadores": "Indicadores de Desempenho e Qualidade (R2)",
    }

    group_entries: dict[str, list[DatasetEntry]] = {k: [] for k in group_names}

    for slug, meta in R1_DATASETS_META.items():
        entries = _build_entries_for_dataset(slug, meta)
        grp = meta["group"]
        if grp in group_entries:
            group_entries[grp].extend(entries)

    return {
        grp: GroupInfo(name=group_names[grp], entries=entries)
        for grp, entries in group_entries.items()
    }


_GROUPS_MAP = _build_all_groups()

GROUPS: dict[str, dict[str, Any]] = {
    grp: info.to_dict() for grp, info in _GROUPS_MAP.items()
}

GROUP_ALIASES: dict[str, str] = {
    "padrao": "carga",
    "sin": "carga",
    "hidro": "hidrologia",
    "ear": "hidrologia",
    "ena": "hidrologia",
    "cmo": "precos",
    "preco": "precos",
    "usinas": "geracao",
    "troca": "intercambio",
    "cadastro": "cadastros",
}


def list_datasets(group: str | None = None) -> list[dict[str, Any]]:
    """List datasets for a group or all groups."""
    if group is None:
        entries: list[dict[str, Any]] = []
        for g_data in GROUPS.values():
            entries.extend(g_data["entries"])
        return entries

    canon = GROUP_ALIASES.get(group, group)
    if canon not in GROUPS:
        raise ValueError(f"Grupo desconhecido: {group!r}")
    return list(GROUPS[canon]["entries"])
