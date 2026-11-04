"""Catálogo completo do ONS: grupos, tiers, aliases e retrocompatibilidade."""

from __future__ import annotations

import pytest

from ons_fetcher.catalog import (
    CATALOG,
    GROUP_ALIASES,
    GROUPS,
    MACRO_ALIASES,
    catalog_rows,
    expand_group,
    list_datasets,
)
from ons_fetcher.catalog_snapshot import EXCLUDED, SNAPSHOT
from ons_fetcher.constants import R1_DATASETS_META


def test_catalogo_cobre_os_88_pacotes_do_ckan() -> None:
    """87 catalogados + 1 excluído (link externo) = 88 pacotes do snapshot."""
    assert len(CATALOG) == 87
    assert len(EXCLUDED) == 1
    assert len(SNAPSHOT) == 88
    assert {d.ckan_slug for d in CATALOG.values()} | set(EXCLUDED) == set(SNAPSHOT)


def test_todos_os_grupos_tem_conjuntos_catalogados() -> None:
    """Nenhum dos 8 grupos fica vazio no catálogo (programação e indicadores incl.)."""
    assert len(GROUPS) == 8
    for group in GROUPS:
        assert catalog_rows(group), group
    assert len(catalog_rows("programacao")) == 7
    assert len(catalog_rows("indicadores")) == 23


def test_tiers_r1_e_listados() -> None:
    """R1 são os 23 de R1_DATASETS_META; o resto fica listado."""
    r1 = {r["slug"] for r in catalog_rows(tier="r1")}
    assert r1 == set(R1_DATASETS_META)
    assert len(catalog_rows(tier="listed")) == len(CATALOG) - len(R1_DATASETS_META)


def test_ids_r1_retrocompativeis() -> None:
    """list_datasets continua devolvendo só R1, com os ids históricos."""
    ids = {e["id"] for e in list_datasets()}
    assert "carga-energia_2024" in ids
    assert "fator-capacidade-2_2024_01" in ids
    assert all(e["base_id"] in R1_DATASETS_META for e in list_datasets())
    # grupos só com conjuntos listados não baixam nada (R2)
    assert list_datasets("programacao") == []
    assert list_datasets("indicadores") == []


def test_macro_aliases_expandem_para_grupos_canonicos() -> None:
    """Macro-aliases e aliases simples resolvem para grupos existentes."""
    for alias, targets in GROUP_ALIASES.items():
        assert targets
        assert set(expand_group(alias)) <= set(GROUPS)
    assert expand_group("programacao-da-operacao") == ["programacao", "precos"]
    assert set(MACRO_ALIASES) <= set(GROUP_ALIASES)
    assert expand_group("hidro") == ["hidrologia"]
    with pytest.raises(ValueError, match="Grupo desconhecido"):
        expand_group("xyz")


def test_s3_dir_vem_do_catalogo_nao_do_slug() -> None:
    """Diretório S3 diferente do slug CKAN é preservado (ex.: carga_energia_di)."""
    assert CATALOG["carga-energia"].s3_dir == "carga_energia_di"
    assert CATALOG["balanco_dessem_geral"].granularity == "daily"
    assert CATALOG["carga-energia-verificada"].granularity == "external"
