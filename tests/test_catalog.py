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


def _fake_keys(prefix_anual: str, prefix_mensal: str, anuais, mensais):
    nomes = [f"{prefix_anual}_{y}.{e}" for y in anuais for e in ("csv", "parquet")]
    nomes += [
        f"{prefix_mensal}_{y}_{m:02d}.{e}"
        for (y, m) in mensais
        for e in ("csv", "parquet")
    ]
    nomes.append("DicionarioDados_X.json")
    return [{"name": n, "size": 10} for n in nomes]


def test_granularidade_mista_cobre_as_duas_faixas(monkeypatch) -> None:
    """geracao-usina-2 e fator-capacidade-2: anual ate 2021 + mensal desde 2022."""
    from ons_fetcher import catalog

    mensais = [(2022, 1), (2022, 2), (2026, 11)]
    dados = {
        "geracao_usina_2_ho": _fake_keys(
            "GERACAO_USINA-2", "GERACAO_USINA-2", (2020, 2021), mensais
        ),
        "fator_capacidade_2_di": _fake_keys(
            "FATOR_CAPACIDADE", "FATOR_CAPACIDADE-2", (2009, 2021), mensais
        ),
    }
    monkeypatch.setattr(catalog, "_keys", lambda s3_dir: dados[s3_dir])
    catalog._GROUP_CACHE.clear()
    try:
        entries = catalog.list_datasets("geracao")
    finally:
        catalog._GROUP_CACHE.clear()
    por_id = {e["id"]: e for e in entries}

    for slug in ("geracao-usina-2", "fator-capacidade-2"):
        assert f"{slug}_2021" in por_id  # faixa anual
        assert f"{slug}_2022_01" in por_id  # faixa mensal
        assert f"{slug}_2026_11" in por_id
        assert por_id[f"{slug}_2021"]["month"] is None
        assert por_id[f"{slug}_2022_01"]["month"] == 1
    assert por_id["fator-capacidade-2_2009"]["url"].endswith(
        "/FATOR_CAPACIDADE_2009.parquet"
    )
    assert por_id["fator-capacidade-2_2022_02"]["url"].endswith(
        "/FATOR_CAPACIDADE-2_2022_02.parquet"
    )
    # ids unicos e um formato por periodo
    assert len(por_id) == len(entries)
