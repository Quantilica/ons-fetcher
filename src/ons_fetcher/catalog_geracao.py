"""Catálogo ONS do domínio ``geracao`` — Geração e Fator de Capacidade.

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "geracao"
NAME = "Geração e Fator de Capacidade"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="coff_eolica_usi_intrasemihora",
        ckan_slug="coff_eolica_usi_intrasemihora",
        group=GROUP,
        name="Dados de Restrição de Operação por Constrained-off de Usinas Eólicas Intra SemiHora",
        s3_dir="restricao_coff_eolica_intrasemihora",
        prefix="COFF_USI_EOLICAS_INTRASEMIHORA",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="coff_fotovoltaica_intrasemihora",
        ckan_slug="coff_fotovoltaica_intrasemihora",
        group=GROUP,
        name="Dados de Restrição de Operação por Constrained-off de Usinas Fotovoltaicas Intra SemiHora",
        s3_dir="restricao_coff_fotovoltaica_intrasemihora",
        prefix="COFF_USI_FOTOVOLTAICA_INTRASEMIHORA",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="disponibilidade_usina",
        ckan_slug="disponibilidade_usina",
        group=GROUP,
        name="Dados de Disponibilidade de Usinas",
        s3_dir="disponibilidade_usina_ho",
        prefix="DISPONIBILIDADE_USINA",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="energia-vertida-turbinavel",
        ckan_slug="energia-vertida-turbinavel",
        group=GROUP,
        name="Energia Vertida Turbinável",
        s3_dir="energia_vertida_turbinavel_ho",
        prefix="ENERGIA_VERTIDA_TURBINAVEL",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Granularidade mista: anual até 2023, mensal depois.",
    ),
    OnsDataset(
        slug="geracao-termica-despacho-2",
        ckan_slug="geracao-termica-despacho-2",
        group=GROUP,
        name="Geração Térmica por Motivo de Despacho",
        s3_dir="geracao_termica_despacho_2_ho",
        prefix="GERACAO_TERMICA_DESPACHO-2",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="Granularidade mista: anual até 2023, mensal depois.",
    ),
    OnsDataset(
        slug="geracao_itaipu",
        ckan_slug="geracao_itaipu",
        group=GROUP,
        name="Geração de Itaipu Binacional - Base horária",
        s3_dir="geracao_itaipu",
        prefix="GERACAO_ITAIPU",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="restricao_coff_eolica_detail",
        ckan_slug="restricao_coff_eolica_detail",
        group=GROUP,
        name="Dados de Restrição De Operação Por Constrained-off de Usinas Eólicas - Detalhamento Por Usinas",
        s3_dir="restricao_coff_eolica_detail_tm",
        prefix="RESTRICAO_COFF_EOLICA_DETAIL",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="restricao_coff_eolica_usi",
        ckan_slug="restricao_coff_eolica_usi",
        group=GROUP,
        name="Dados de Restrição de Operação por Constrained-off de Usinas Eólicas",
        s3_dir="restricao_coff_eolica_tm",
        prefix="RESTRICAO_COFF_EOLICA",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="restricao_coff_fotovoltaica",
        ckan_slug="restricao_coff_fotovoltaica",
        group=GROUP,
        name="Dados de Restrição de Operação por Constrained-off de Usinas Fotovoltaicas",
        s3_dir="restricao_coff_fotovoltaica_tm",
        prefix="RESTRICAO_COFF_FOTOVOLTAICA",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="restricao_coff_fotovoltaica_detail",
        ckan_slug="restricao_coff_fotovoltaica_detail",
        group=GROUP,
        name="Dados de Restrição De Operação Por Constrained-off de Usinas Fotovoltaicas - Detalhamento Por Usinas",
        s3_dir="restricao_coff_fotovoltaica_detail_tm",
        prefix="RESTRICAO_COFF_FOTOVOLTAICA_DETAIL",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="usi_servicoancilar_sandbox",
        ckan_slug="usi_servicoancilar_sandbox",
        group=GROUP,
        name="Usinas prestando serviço ancilar de reativo conforme PRIMEIRO SANDBOX",
        s3_dir="usi_servicoancilar_sandbox",
        prefix="USI_SERVICOANCILAR_SANDBOX",
        granularity="monthly",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
)

DATASETS: dict[str, OnsDataset] = {
    **r1_datasets(GROUP),
    **{d.slug: d for d in LISTED},
}
