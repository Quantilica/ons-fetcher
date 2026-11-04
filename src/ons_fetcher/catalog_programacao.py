"""Catálogo ONS do domínio ``programacao`` — Programação da Operação.

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "programacao"
NAME = "Programação da Operação"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="balanco_dessem_detalhe",
        ckan_slug="balanco_dessem_detalhe",
        group=GROUP,
        name="DESSEM - Balanço de Energia Detalhado",
        s3_dir="balanco_dessem_detalhe",
        prefix="BALANCO_DESSEM_DETALHE",
        granularity="daily",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Um arquivo por dia (centenas): exige planejador de diff.",
    ),
    OnsDataset(
        slug="balanco_dessem_geral",
        ckan_slug="balanco_dessem_geral",
        group=GROUP,
        name="DESSEM - Balanço de Energia Geral",
        s3_dir="balanco_dessem_geral",
        prefix="BALANCO_DESSEM_GERAL",
        granularity="daily",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Um arquivo por dia (centenas): exige planejador de diff.",
    ),
    OnsDataset(
        slug="descontinuado-dados-do-historico-de-despacho-de-energia-de-01-2021-a-09-2024",
        ckan_slug="descontinuado-dados-do-historico-de-despacho-de-energia-de-01-2021-a-09-2024",
        group=GROUP,
        name="Dados do Histórico de Despacho de Energia de Janeiro/2021 A Setembro/2024",
        s3_dir="hist_despacho_energia",
        prefix="info",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet"),
        note="Conjunto descontinuado pelo ONS (01/2021 a 09/2024).",
    ),
    OnsDataset(
        slug="oferta_respostademanda",
        ckan_slug="oferta_respostademanda",
        group=GROUP,
        name="Oferta - Resposta à Demanda",
        s3_dir="oferta_respostademanda",
        prefix="OFERTA_RESPOSTADEMANDA",
        granularity="annual",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="programacao_diaria",
        ckan_slug="programacao_diaria",
        group=GROUP,
        name="Dados dos Valores da Programação Diária",
        s3_dir="programacao_diaria",
        prefix="PROGRAMACAO_DIARIA",
        granularity="daily",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Um arquivo por dia (centenas): exige planejador de diff.",
    ),
    OnsDataset(
        slug="programacao_fluxo_controlado",
        ckan_slug="programacao_fluxo_controlado",
        group=GROUP,
        name="Dados dos Programados dos Elementos de Fluxo Controlado",
        s3_dir="programacao_fluxo_controlado",
        prefix="PROGRAMACAO_FLUXO_CONTROLADO",
        granularity="daily",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Um arquivo por dia (centenas): exige planejador de diff.",
    ),
    OnsDataset(
        slug="programacao_x_previsao",
        ckan_slug="programacao_x_previsao",
        group=GROUP,
        name="Dados dos Valores da Previsão Versus Programado - Eólicas e Solares",
        s3_dir="programacao_x_previsao",
        prefix="PROGRAMACAO_X_PREVISAO",
        granularity="daily",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Um arquivo por dia (centenas): exige planejador de diff.",
    ),
)

DATASETS: dict[str, OnsDataset] = {
    **r1_datasets(GROUP),
    **{d.slug: d for d in LISTED},
}
