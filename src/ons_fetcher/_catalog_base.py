"""Shared types and helper constructors for ons-fetcher catalogs."""

from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass
from typing import Any, Literal

from .constants import R1_CKAN_SLUGS, R1_DATASETS_META

Tier = Literal["r1", "listed"]


@dataclass(frozen=True)
class DatasetEntry:
    """Represents a single dataset entry to be downloaded."""

    id: str
    base_id: str
    name: str
    url: str
    ext: str
    group: str
    source: str = "ons"
    year: int | None = None
    quarter: int | None = None
    month: int | None = None
    slug: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert entry to dict."""
        return asdict(self)


@dataclass(frozen=True)
class GroupInfo:
    """Represents a logical group of dataset entries."""

    name: str
    entries: list[DatasetEntry]

    def to_dict(self) -> dict[str, Any]:
        """Convert group to dict."""
        return {
            "name": self.name,
            "entries": [e.to_dict() for e in self.entries],
        }


def static_dataset(
    group: str,
    *,
    id: str,
    name: str,
    url: str,
    ext: str = "csv",
) -> DatasetEntry:
    """Construct a static (single-file) dataset entry."""
    return DatasetEntry(
        id=id,
        base_id=id,
        name=name,
        url=url,
        ext=ext,
        group=group,
    )


def annual_datasets(
    group: str,
    *,
    base_id: str,
    name_template: str,
    url_template: str,
    start_year: int,
    end_year: int | None = None,
    ext: str = "parquet",
) -> list[DatasetEntry]:
    """Construct annual dataset entries."""
    end = end_year or dt.date.today().year
    return [
        DatasetEntry(
            id=f"{base_id}_{y}",
            base_id=base_id,
            name=name_template.format(year=y),
            url=url_template.format(year=y),
            ext=ext,
            group=group,
            year=y,
        )
        for y in range(start_year, end + 1)
    ]


def monthly_datasets(
    group: str,
    *,
    base_id: str,
    name_template: str,
    url_template: str,
    start_year: int,
    end_year: int | None = None,
    ext: str = "parquet",
) -> list[DatasetEntry]:
    """Construct monthly dataset entries."""
    end = end_year or dt.date.today().year
    entries: list[DatasetEntry] = []
    for y in range(start_year, end + 1):
        for m in range(1, 13):
            entries.append(
                DatasetEntry(
                    id=f"{base_id}_{y}_{m:02d}",
                    base_id=base_id,
                    name=name_template.format(year=y, month=m),
                    url=url_template.format(year=y, month=f"{m:02d}"),
                    ext=ext,
                    group=group,
                    year=y,
                    month=m,
                )
            )
    return entries


@dataclass(frozen=True)
class OnsDataset:
    """Descritor estático de um conjunto do CKAN do ONS.

    Attributes:
        slug: Id estável do conjunto no catálogo (``base_id`` das entradas).
        ckan_slug: Nome do pacote no CKAN do ONS.
        group: Grupo (domínio) canônico.
        name: Título do conjunto.
        s3_dir: Diretório do bucket S3 (nunca deduzido do slug).
        prefix: Prefixo dos nomes dos arquivos (vazio se não há arquivo).
        granularity: ``annual``, ``monthly``, ``daily``, ``static`` ou ``external``.
        tier: ``r1`` (baixa hoje) ou ``listed`` (listado; download em release futura).
        formats: Formatos de dados publicados no bucket.
        note: Observação sobre o motivo de não baixar ou particularidades.
    """

    slug: str
    ckan_slug: str
    group: str
    name: str
    s3_dir: str
    prefix: str
    granularity: str
    tier: Tier
    formats: tuple[str, ...] = ()
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Converte o descritor em dict."""
        return asdict(self)


def r1_datasets(group: str) -> dict[str, OnsDataset]:
    """Constrói os descritores R1 de um grupo a partir de ``R1_DATASETS_META``."""
    return {
        slug: OnsDataset(
            slug=slug,
            ckan_slug=R1_CKAN_SLUGS.get(slug, slug),
            group=group,
            name=str(meta["name"]),
            s3_dir=str(meta["s3_dir"]),
            prefix=str(meta["prefix"]),
            granularity=str(meta["granularity"]),
            tier="r1",
            formats=("parquet", "csv", "xlsx"),
        )
        for slug, meta in R1_DATASETS_META.items()
        if meta["group"] == group
    }
