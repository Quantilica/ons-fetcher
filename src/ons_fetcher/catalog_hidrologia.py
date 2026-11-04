"""Catálogo ONS do domínio ``hidrologia`` — Hidrologia, EAR e ENA.

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "hidrologia"
NAME = "Hidrologia, EAR e ENA"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="bacia_contorno",
        ckan_slug="bacia_contorno",
        group=GROUP,
        name="Contornos das Bacias Hidrográficas",
        s3_dir="bacia_contorno",
        prefix="Bacias_Hidrograficas_SIN",
        granularity="static",
        tier="listed",
        formats=("zip",),
        note="Shapefile em ZIP; sem Parquet.",
    ),
    OnsDataset(
        slug="dados_hidrologicos_ho",
        ckan_slug="dados_hidrologicos_ho",
        group=GROUP,
        name="Dados Hidráulicos por Reservatório – Base horária",
        s3_dir="dados_hidrologicos_ho",
        prefix="DADOS_HIDROLOGICOS_HO",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="deprec_fluv",
        ckan_slug="deprec_fluv",
        group=GROUP,
        name="Grandezas Fluviométricas Depreciadas",
        s3_dir="deprec_fluv",
        prefix="DEPREC_FLUVIOMETRICAS",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="deprec_hidro",
        ckan_slug="deprec_hidro",
        group=GROUP,
        name="Dados Hidrológicos Depreciados de Reservatórios",
        s3_dir="deprec_hidro",
        prefix="DEPREC_HIDROLOGICOSRES",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="grandezas_fluviometricas",
        ckan_slug="grandezas_fluviometricas",
        group=GROUP,
        name="Dados de Grandezas Fluviométricas",
        s3_dir="grandezas_fluviometricas_di",
        prefix="GRANDEZAS_FLUVIOMETRICAS",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="precipitacao-estacao",
        ckan_slug="precipitacao-estacao",
        group=GROUP,
        name="Precipitação Diária Observada",
        s3_dir="precipitacao_estacao_di",
        prefix="Precipitacao_Diaria_Observada",
        granularity="annual",
        tier="listed",
        formats=("csv",),
        note="",
    ),
    OnsDataset(
        slug="res_cotaareavolume",
        ckan_slug="res_cotaareavolume",
        group=GROUP,
        name="Reservatório - tabelas cota x area x volume",
        s3_dir="res_cotaareavolume",
        prefix="RES_COTAAREAVOLUME",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="res_volumeespera",
        ckan_slug="res_volumeespera",
        group=GROUP,
        name="Dados Hidrológicos - Volume de Espera Recomendado",
        s3_dir="res_volumeespera",
        prefix="RES_VOLUMEESPERA",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
)

DATASETS: dict[str, OnsDataset] = {
    **r1_datasets(GROUP),
    **{d.slug: d for d in LISTED},
}
