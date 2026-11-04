"""Tests for ons-fetcher lake converter."""

from __future__ import annotations

from pathlib import Path

import polars as pl
from quantilica.analytics.lake import check_dataset

from ons_fetcher.lake import converter


def test_converter_metadata() -> None:
    """Verify converter source_id and dataset list."""
    assert converter.source_id == "ons"
    datasets = converter.datasets()
    assert isinstance(datasets, list)
    assert "carga-energia" in datasets
    assert "curva-carga" in datasets
    assert "capacidade-geracao" in datasets


def test_converter_empty_dir(tmp_path: Path) -> None:
    """Test convert with empty input directory."""
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    res = converter.convert(raw_dir, lake_dir)
    assert res.converted == 0
    assert res.skipped == 0
    assert not res.errors


def test_convert_datasets_end_to_end(tmp_path: Path) -> None:
    """Test conversion of Parquet and CSV files to Lake Hive."""
    raw_dir = tmp_path / "raw"
    carga_dir = raw_dir / "carga"
    cadastros_dir = raw_dir / "cadastros"
    carga_dir.mkdir(parents=True)
    cadastros_dir.mkdir(parents=True)

    lake_dir = tmp_path / "lake"
    lake_dir.mkdir()

    # 1. Annual dataset: carga-energia (Parquet)
    df_carga = pl.DataFrame(
        {
            "DAT_REFERENCIA": ["2024-01-01", "2024-01-02"],
            "NOM_SUBSISTEMA": ["SUDESTE", "SUL"],
            "VAL_CARGAENERGIA": [50000.5, 15000.2],
        }
    )
    carga_file = carga_dir / "carga-energia_2024@20261101.parquet"
    df_carga.write_parquet(carga_file)

    # 2. Monthly dataset: fator-capacidade-2 (Parquet)
    geracao_dir = raw_dir / "geracao"
    geracao_dir.mkdir(parents=True)
    df_curva = pl.DataFrame(
        {
            "DIN_INSTANTE": ["2024-05-01 00:00:00", "2024-05-01 01:00:00"],
            "NOM_SUBSISTEMA": ["SUDESTE", "SUDESTE"],
            "VAL_CARGAENERGIA": [42000.0, 41500.0],
        }
    )
    curva_file = geracao_dir / "fator-capacidade-2_2024-05@20261101.parquet"
    df_curva.write_parquet(curva_file)

    # 3. Static dataset: capacidade-geracao (CSV)
    csv_content = (
        "NOM_USINA;NOM_TIPO_USINA;VAL_POTENCIAEFETIVA\n"
        "Itaipu;Hidreletrica;14000,00\n"
        "Belo Monte;Hidreletrica;11233,10\n"
    )
    cap_file = cadastros_dir / "capacidade_geracao@20261101.csv"
    cap_file.write_text(csv_content, encoding="utf-8")

    # Run conversion
    res = converter.convert(raw_dir, lake_dir)
    assert res.converted == 3
    assert not res.errors

    # Verify Lake datasets using check_dataset
    lake_ons = lake_dir / "ons"

    # Verify carga-energia
    ds_carga = lake_ons / "carga-energia"
    assert ds_carga.is_dir()
    assert (ds_carga / "_dataset.json").exists()
    assert (ds_carga / "ano=2024").is_dir()
    errors_carga = check_dataset(ds_carga)
    assert not errors_carga, f"Errors in carga-energia: {errors_carga}"

    # Verify curva-carga
    ds_curva = lake_ons / "fator-capacidade-2"
    assert ds_curva.is_dir()
    assert (ds_curva / "_dataset.json").exists()
    assert (ds_curva / "ano=2024" / "mes=5").is_dir()
    errors_curva = check_dataset(ds_curva)
    assert not errors_curva, f"Errors in curva-carga: {errors_curva}"

    # Verify capacidade-geracao (static/unpartitioned)
    ds_cap = lake_ons / "capacidade-geracao"
    assert ds_cap.is_dir()
    assert (ds_cap / "_dataset.json").exists()
    errors_cap = check_dataset(ds_cap)
    assert not errors_cap, f"Errors in capacidade-geracao: {errors_cap}"


def test_granularidade_mista_sem_colisao_de_particoes(tmp_path: Path) -> None:
    """Anual (mes=0) e mensal coexistem no mesmo dataset sem sobrescrever."""
    raw = tmp_path / "raw" / "geracao"
    raw.mkdir(parents=True)
    lake = tmp_path / "lake"
    lake.mkdir()
    for nome in (
        "geracao-usina-2_2021",  # anual
        "geracao-usina-2_2022-01",  # mensal
        "geracao-usina-2_2022-02",
        "fator-capacidade-2_2021",
        "fator-capacidade-2_2022-01",
    ):
        pl.DataFrame({"VAL": [1.0, 2.0]}).write_parquet(
            raw / f"{nome}@20261101.parquet"
        )

    res = converter.convert(tmp_path / "raw", lake)
    assert not res.errors
    assert res.converted == 5

    for slug, n in (("geracao-usina-2", 3), ("fator-capacidade-2", 2)):
        ds = lake / "ons" / slug
        assert not check_dataset(ds)
        df = pl.concat(
            [pl.read_parquet(p) for p in ds.rglob("*.parquet")], how="diagonal"
        )
        assert df.height == 2 * n
        assert (ds / "ano=2021" / "mes=0").is_dir()
        assert (ds / "ano=2022" / "mes=1").is_dir()
        assert set(df["periodicidade"].unique().to_list()) == {"anual", "mensal"}
    assert (lake / "ons" / "geracao-usina-2" / "ano=2022" / "mes=2").is_dir()

    res2 = converter.convert(tmp_path / "raw", lake)
    assert (res2.converted, res2.skipped) == (0, 5)
