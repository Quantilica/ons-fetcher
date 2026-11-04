"""Catálogo ONS do domínio ``carga`` — Carga e Demanda do SIN.

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "carga"
NAME = "Carga e Demanda do SIN"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="carga-energia-programada",
        ckan_slug="carga-energia-programada",
        group=GROUP,
        name="Carga de Energia Programada",
        s3_dir="carga_programada_tm",
        prefix="",
        granularity="external",
        tier="listed",
        formats=(),
        note="Sem arquivo no bucket: apenas API Swagger do ONS.",
    ),
    OnsDataset(
        slug="carga-energia-verificada",
        ckan_slug="carga-energia-verificada",
        group=GROUP,
        name="Carga de Energia Verificada",
        s3_dir="carga_verificada_tm",
        prefix="",
        granularity="external",
        tier="listed",
        formats=(),
        note="Sem arquivo no bucket: apenas API Swagger do ONS.",
    ),
    OnsDataset(
        slug="cargaglobal-roraima",
        ckan_slug="cargaglobal-roraima",
        group=GROUP,
        name="Carga global de Roraima",
        s3_dir="cargaglobal_roraima",
        prefix="CargaGlobalRoraima",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="demanda_maxima_di",
        ckan_slug="demanda_maxima_di",
        group=GROUP,
        name="Demanda Máxima Diária por Subsistema",
        s3_dir="demanda_maxima_di",
        prefix="DEMANDA_MAXIMA_DI",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="interrupcao_carga",
        ckan_slug="interrupcao_carga",
        group=GROUP,
        name="Interrupção de Carga",
        s3_dir="interrupcao_carga",
        prefix="INTERRUPCAO_CARGA",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
)

DATASETS: dict[str, OnsDataset] = {
    **r1_datasets(GROUP),
    **{d.slug: d for d in LISTED},
}
