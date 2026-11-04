"""Catálogo ONS do domínio ``cadastros`` — Cadastros de Usinas e Reservatórios.

Gerado a partir do ``package_search`` do CKAN do ONS (2026-11-03). Os conjuntos R1
(``tier="r1"``) vêm de :data:`R1_DATASETS_META` e baixam hoje; os demais ficam
listados (``tier="listed"``), com download previsto para releases futuras.
"""

from __future__ import annotations

from ._catalog_base import OnsDataset, r1_datasets

GROUP = "cadastros"
NAME = "Cadastros de Usinas e Reservatórios"

LISTED: tuple[OnsDataset, ...] = (
    OnsDataset(
        slug="capacidade-transformacao",
        ckan_slug="capacidade-transformacao",
        group=GROUP,
        name="Capacidade de Transformação da Rede Básica",
        s3_dir="capacidade-transformacao",
        prefix="CAPACIDADE_TRANSFORMACAO",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="equipamento-controle-reativo",
        ckan_slug="equipamento-controle-reativo",
        group=GROUP,
        name="Equipamentos de Controle de Reativos",
        s3_dir="equipamento_controle_reativo",
        prefix="EQP_CONTROLE_REATIVO",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="linha-transmissao",
        ckan_slug="linha-transmissao",
        group=GROUP,
        name="Linhas de Transmissão da Rede de Operação",
        s3_dir="linha_transmissao",
        prefix="LINHA_TRANSMISSAO",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="modalidade-usina",
        ckan_slug="modalidade-usina",
        group=GROUP,
        name="Modalidade de Operação de Usinas",
        s3_dir="modalidade_usina",
        prefix="MODALIDADE_USINA",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="subestacao",
        ckan_slug="subestacao",
        group=GROUP,
        name="Subestação da Rede de Operação",
        s3_dir="subestacao",
        prefix="SUBESTACAO",
        granularity="static",
        tier="listed",
        formats=("csv", "parquet", "xlsx"),
        note="",
    ),
    OnsDataset(
        slug="usina_pqu",
        ckan_slug="usina_pqu",
        group=GROUP,
        name="Dados do Relacionamento Entre Grupos de Pequenas Usinas e Usinas",
        s3_dir="usina_pqu",
        prefix="RELACIONAMENTO_USINA_PEQUENAUSINA",
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
