"""Catálogo ONS do domínio ``precos`` — Preços e Custo Marginal de Operação (CMO).

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "precos"
NAME = "Preços e Custo Marginal de Operação (CMO)"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="ofertapreco-importacao",
        ckan_slug="ofertapreco-importacao",
        group=GROUP,
        name="Ofertas de Preço para Importação",
        s3_dir="ofertapreco-importacao-se",
        prefix="OFERTA_PRECO_IMPORTACAO",
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
