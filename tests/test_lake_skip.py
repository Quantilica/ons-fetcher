"""O build do lake pula, sem ler o bruto, o que já está em dia."""

from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

import ons_fetcher.lake as lake_mod
from ons_fetcher.lake import converter


def _bruto(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    (raw / "carga").mkdir(parents=True)
    df = pl.DataFrame(
        {
            "DAT_REFERENCIA": ["2024-01-01"],
            "NOM_SUBSISTEMA": ["SUDESTE"],
            "VAL_CARGAENERGIA": [50000.5],
        }
    )
    df.write_parquet(raw / "carga" / "carga-energia_2024@20261101.parquet")
    df.write_parquet(raw / "carga" / "carga-energia_2025@20261101.parquet")
    (raw / "cad").mkdir()
    (raw / "cad" / "intercambio-nacional_2000.csv").write_text(
        "din_instante;nom_subsistema\n2000-01-01;SUL\n", encoding="utf-8"
    )
    return raw


@pytest.fixture
def leituras(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Registra toda leitura do bruto (Parquet e CSV)."""
    vistas: list[str] = []

    def espia(nome: str, original):  # noqa: ANN001, ANN202
        def _f(*args, **kwargs):  # noqa: ANN002, ANN003
            vistas.append(nome)
            return original(*args, **kwargs)

        return _f

    monkeypatch.setattr(pl, "read_parquet", espia("parquet", pl.read_parquet))
    monkeypatch.setattr(pl, "read_csv", espia("csv", pl.read_csv))
    monkeypatch.setattr(lake_mod, "_ler_csv", espia("ler_csv", lake_mod._ler_csv))
    return vistas


@pytest.mark.parametrize(
    ("dataset", "n"), [("carga-energia", 2), ("intercambio-nacional", 1)]
)
def test_segunda_rodada_nao_le_o_bruto(
    tmp_path: Path, leituras: list[str], dataset: str, n: int
) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    res = converter.convert(raw, lake, datasets=[dataset])
    assert not res.errors, res.errors
    assert (res.converted, res.skipped) == (n, 0)
    assert leituras

    leituras.clear()
    res2 = converter.convert(raw, lake, datasets=[dataset])
    assert (res2.converted, res2.skipped, res2.errors) == (0, n, [])
    assert leituras == []


def test_force_reconverte_lendo_o_bruto(tmp_path: Path, leituras: list[str]) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["carga-energia"])

    leituras.clear()
    res = converter.convert(raw, lake, datasets=["carga-energia"], force=True)
    assert (res.converted, res.skipped, res.errors) == (2, 0, [])
    assert leituras.count("parquet") == 2


def test_bruto_novo_converte_e_o_resto_pula(
    tmp_path: Path, leituras: list[str]
) -> None:
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["carga-energia"])
    antigo = raw / "carga" / "carga-energia_2024@20261101.parquet"
    pl.DataFrame(
        {
            "DAT_REFERENCIA": ["2024-01-01", "2024-01-02"],
            "NOM_SUBSISTEMA": ["SUDESTE", "SUL"],
            "VAL_CARGAENERGIA": [1.0, 2.0],
        }
    ).write_parquet(raw / "carga" / "carga-energia_2026@20261118.parquet")

    leituras.clear()
    res = converter.convert(raw, lake, datasets=["carga-energia"])
    assert not res.errors, res.errors
    assert (res.converted, res.skipped) == (1, 2)
    assert leituras == ["parquet"]
    assert antigo.exists()
