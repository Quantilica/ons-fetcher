"""Catálogo ONS do domínio ``intercambio`` — Intercâmbio e Balanço de Energia.

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "intercambio"
NAME = "Intercâmbio e Balanço de Energia"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="geracao-exportacao-internacional",
        ckan_slug="geracao-exportacao-internacional",
        group=GROUP,
        name="Geração Comercial Para Exportação Internacional",
        s3_dir="geracao_exportacao_internacional_ho",
        prefix="GERACAO_EXPORTACAO_INTERNACIONAL",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="importacaoenergia-comercial-2",
        ckan_slug="importacaoenergia-comercial-2",
        group=GROUP,
        name="Importação de Energia na Modalidade Comercial por Bloco",
        s3_dir="importacaoenergia-comercial-2-ho",
        prefix="IMPORTACAOENERGIA_COMERCIAL-2",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="intercambio_modalidade",
        ckan_slug="intercambio_modalidade",
        group=GROUP,
        name="Dados de Intercâmbio de Energia por Modalidade",
        s3_dir="intercambio_modalidade_ho",
        prefix="INTERCAMBIO_ENERGIA_MODALIDADE",
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
