"""Tests for ons-fetcher catalog (sem rede)."""

from __future__ import annotations

import pytest

from ons_fetcher import catalog
from ons_fetcher.catalog import GROUP_ALIASES, GROUPS, list_datasets
from ons_fetcher.constants import R1_DATASETS_META


def _fake_keys(s3_dir: str) -> list[dict[str, object]]:
    meta = next(m for m in R1_DATASETS_META.values() if m["s3_dir"] == s3_dir)
    prefix = str(meta["prefix"])
    return [
        {
            "key": f"dataset/{s3_dir}/{prefix}_2024.parquet",
            "name": f"{prefix}_2024.parquet",
            "size": 10,
            "last_modified": "2025-01-01T00:00:00Z",
        },
        {
            "key": f"dataset/{s3_dir}/{prefix}_2024_01.parquet",
            "name": f"{prefix}_2024_01.parquet",
            "size": 11,
            "last_modified": "2025-02-01T00:00:00Z",
        },
        {
            "key": f"dataset/{s3_dir}/DicionarioDados_{prefix}.json",
            "name": f"DicionarioDados_{prefix}.json",
            "size": 5,
            "last_modified": "2025-02-01T00:00:00Z",
        },
    ]


@pytest.fixture(autouse=True)
def fake_s3(monkeypatch: pytest.MonkeyPatch) -> None:
    """Substitui a listagem do S3 e limpa os caches do catálogo."""
    monkeypatch.setattr(catalog, "_KEYS_CACHE", {})
    monkeypatch.setattr(catalog, "_GROUP_CACHE", {})
    monkeypatch.setattr(
        catalog.OnsClient, "list_dataset_keys", lambda self, s3_dir: _fake_keys(s3_dir)
    )


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
