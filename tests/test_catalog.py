"""Tests for ons-fetcher catalog (sem rede)."""

from __future__ import annotations

import pytest

from ons_fetcher.catalog import GROUP_ALIASES, GROUPS, list_datasets


def test_granularidade_anual_e_mensal() -> None:
    """Anual casa <prefix>_<ano>; mensal casa <prefix>_<ano>_<mes>."""
    anual = list_datasets("carga")
    ids = {e["id"] for e in anual}
    assert "carga-energia_2024" in ids

    geracao = list_datasets("geracao")
    mensal = [e for e in geracao if e["id"] == "fator-capacidade-2_2024_01"]
    assert mensal
    assert mensal[0]["url"].endswith("_2024_01.parquet")
    assert mensal[0]["month"] == 1


def test_estatico_ignora_dicionario() -> None:
    """Cadastros usam o objeto de dados, nunca o dicionário."""
    cadastros = list_datasets("cadastros")
    assert cadastros
    for entry in cadastros:
        assert "Dicionario" not in entry["url"]
        assert entry["url"].startswith("https://ons-aws-prod-opendata")


def test_list_datasets_por_grupo_e_alias() -> None:
    """Grupos e aliases válidos respondem; inválido levanta ValueError."""
    for group in GROUPS:
        assert isinstance(list_datasets(group), list)
    for alias in GROUP_ALIASES:
        assert isinstance(list_datasets(alias), list)
    with pytest.raises(ValueError, match="Grupo desconhecido"):
        list_datasets("grupo_inexistente_xyz")
