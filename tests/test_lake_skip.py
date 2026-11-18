"""O build do lake pula, sem ler o bruto, o que já está em dia."""

from __future__ import annotations

import builtins
import hashlib
import io
import json
from pathlib import Path

import polars as pl
import pytest
import quantilica.core.manifests as manifests_mod

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
    _sidecars(raw)
    return raw


def _sidecars(raiz: Path) -> None:
    """Sidecar ``.manifest.json`` com o sha256 de cada bruto, como o fetcher grava:
    o hash do bruto sai dele, sem ler o arquivo."""
    for f in sorted(raiz.rglob("*")):
        if f.is_file() and not f.name.endswith(".manifest.json"):
            Path(f"{f}.manifest.json").write_text(
                json.dumps(
                    {
                        "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
                        "size_bytes": f.stat().st_size,
                    }
                ),
                encoding="utf-8",
            )


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
    monkeypatch.setattr(
        manifests_mod, "sha256_file", espia("hash", manifests_mod.sha256_file)
    )

    original_open = builtins.open
    original_io_open = io.open
    original_path_open = Path.open

    def do_bruto(arquivo) -> bool:  # noqa: ANN001
        # O sidecar pode (e deve) ser lido: é dele que sai o sha256 do bruto.
        nome = str(arquivo)
        return "/raw/" in nome and not nome.endswith(".manifest.json")

    def open_espia(file, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        if do_bruto(file):
            vistas.append(f"open:{Path(file).name}")
        return original_open(file, *args, **kwargs)

    def io_open_espia(file, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        if do_bruto(file):
            vistas.append(f"io.open:{Path(file).name}")
        return original_io_open(file, *args, **kwargs)

    def path_open_espia(self, *args, **kwargs):  # noqa: ANN001, ANN002, ANN003, ANN202
        if do_bruto(self):
            vistas.append(f"Path.open:{self.name}")
        return original_path_open(self, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", open_espia)
    monkeypatch.setattr(io, "open", io_open_espia)
    monkeypatch.setattr(Path, "open", path_open_espia)
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
    _sidecars(raw)

    leituras.clear()
    res = converter.convert(raw, lake, datasets=["carga-energia"])
    assert not res.errors, res.errors
    assert (res.converted, res.skipped) == (1, 2)
    assert leituras == ["parquet"]
    assert antigo.exists()


def test_sem_sidecar_o_espiao_de_hash_dispara(
    tmp_path: Path, leituras: list[str]
) -> None:
    # Prova de que o espião funciona: sem sidecar o bruto é hasheado lendo-o.
    raw, lake = _bruto(tmp_path), tmp_path / "lake"
    converter.convert(raw, lake, datasets=["carga-energia"])
    for sidecar in raw.rglob("*.manifest.json"):
        sidecar.unlink()
    leituras.clear()
    converter.convert(raw, lake, datasets=["carga-energia"])
    assert "hash" in leituras
