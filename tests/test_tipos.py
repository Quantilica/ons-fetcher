"""Tipos numéricos do conversor: texto, ponto e vírgula decimais viram double."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import polars as pl
import pytest

from ons_fetcher.lake import converter, converter_numericas
from ons_fetcher.tipos import COLUNAS_NUMERICAS

FIXTURES = Path(__file__).parent / "fixtures"
DOCS = Path(__file__).parents[1] / "docs" / "datasets"


def _converter(tmp_path: Path, pasta: str, fixture: str, destino: str):
    raw = tmp_path / "raw" / pasta
    raw.mkdir(parents=True)
    shutil.copy(FIXTURES / fixture, raw / destino)
    lake = tmp_path / "lake"
    res = converter.convert(tmp_path / "raw", lake)
    return res, lake / "ons"


def _ler(ds: Path) -> pl.DataFrame:
    return pl.concat(
        [pl.read_parquet(p) for p in sorted(ds.rglob("*.parquet"))], how="diagonal"
    )


def test_csv_com_ponto_decimal_sai_numerico(tmp_path: Path) -> None:
    """CSV do ONS (ponto decimal, 0 casas inteiras) deixa de virar texto."""
    res, lake = _converter(
        tmp_path,
        "intercambio",
        "intercambio-nacional_2000.csv",
        "intercambio-nacional_2000@20261101.csv",
    )
    assert not res.errors
    df = _ler(lake / "intercambio-nacional")
    assert df.height == 6
    assert df.schema["val_intercambiomwmed"] == pl.Float64
    assert df["val_intercambiomwmed"].to_list() == [
        2.5,
        46.3,
        761.7,
        2.9,
        434.8,
        1452.2,
    ]
    assert df["val_intercambiomwmed"].null_count() == 0
    # códigos e nomes continuam texto
    assert df.schema["id_subsistema_origem"] == pl.String
    assert df["id_subsistema_origem"].to_list()[:2] == ["N", "N"]


def test_csv_com_virgula_decimal_sai_numerico(tmp_path: Path) -> None:
    """O separador é detectado por coluna: vírgula também funciona."""
    raw = tmp_path / "raw" / "intercambio"
    raw.mkdir(parents=True)
    (raw / "intercambio-nacional_2010@20261101.csv").write_text(
        "din_instante;id_subsistema_origem;val_intercambiomwmed;"
        "val_intercambioprogmwmed\n"
        "2010-01-01 00:00:00;N;2,5;10\n"
        "2010-01-01 01:00:00;SE;-1452,25;\n",
        encoding="utf-8",
    )
    res = converter.convert(tmp_path / "raw", tmp_path / "lake")
    assert not res.errors
    df = _ler(tmp_path / "lake" / "ons" / "intercambio-nacional")
    assert df["val_intercambiomwmed"].to_list() == [2.5, -1452.25]
    assert df["val_intercambioprogmwmed"].to_list() == [10.0, None]
    assert df.schema["val_intercambioprogmwmed"] == pl.Float64


def test_csv_iso_8859_1_com_numero_texto(tmp_path: Path) -> None:
    raw = tmp_path / "raw" / "cadastros"
    raw.mkdir(parents=True)
    (raw / "reservatorio@20261101.csv").write_bytes(
        "nom_reservatorio;val_cotamaxima;val_tipoperda;val_perda\n"
        "Itá;104,000;m;0,74\n".encode("iso-8859-1")
    )
    res = converter.convert(tmp_path / "raw", tmp_path / "lake")
    assert not res.errors
    df = _ler(tmp_path / "lake" / "ons" / "reservatorio")
    assert df["nom_reservatorio"].to_list() == ["Itá"]
    assert df["val_cotamaxima"].to_list() == [104.0]
    assert df["val_perda"].to_list() == [0.74]
    # texto de verdade continua texto
    assert df["val_tipoperda"].to_list() == ["m"]


def test_parquet_com_texto_numerico(tmp_path: Path) -> None:
    """Parquet antigo (oito casas, 0E-8, vazio) vira double; vazio vira nulo."""
    origem = pl.read_parquet(FIXTURES / "balanco-energia-subsistema_2000.parquet")
    assert origem.schema["val_gereolica"] == pl.String
    res, lake = _converter(
        tmp_path,
        "balanco",
        "balanco-energia-subsistema_2000.parquet",
        "balanco-energia-subsistema_2000@20261101.parquet",
    )
    assert not res.errors
    df = _ler(lake / "balanco-energia-subsistema")
    assert df.height == origem.height == 6
    colunas = COLUNAS_NUMERICAS["balanco-energia-subsistema"]
    for col in colunas:
        assert df.schema[col] == pl.Float64
        vazios = int((origem[col].str.strip_chars() == "").sum())
        # nenhum valor não nulo vira nulo: só o texto vazio passa a nulo
        assert df[col].null_count() == origem[col].null_count() + vazios
    assert df["val_gereolica"].to_list() == [0.0, 0.0, 0.0, None, None, None]
    assert df["val_gerhidraulica"][0] == 5337.7
    assert df["val_intercambio"][0] == -2.5
    assert df.schema["id_subsistema"] == pl.String
    assert df.schema["din_instante"] != pl.String


def test_parquet_misto_mensal_fator_capacidade(tmp_path: Path) -> None:
    origem = pl.read_parquet(FIXTURES / "fator-capacidade-2_2022-01.parquet")
    res, lake = _converter(
        tmp_path,
        "geracao",
        "fator-capacidade-2_2022-01.parquet",
        "fator-capacidade-2_2022-01@20261101.parquet",
    )
    assert not res.errors
    df = _ler(lake / "fator-capacidade-2")
    assert df.height == origem.height
    for col in (
        "val_geracaoprogramada",
        "val_geracaoverificada",
        "val_capacidadeinstalada",
        "val_fatorcapacidade",
    ):
        assert df.schema[col] == pl.Float64
    assert df["val_geracaoprogramada"].to_list() == [50.5, 9.0, 25.5, None, None]
    assert df["val_geracaoverificada"].null_count() == 0
    assert df["val_fatorcapacidade"][1] == 0.0
    assert df["val_fatorcapacidade"][0] == pytest.approx(0.2379178403755869)
    # a partição e a periodicidade seguem como antes
    assert (lake / "fator-capacidade-2" / "ano=2022" / "mes=1").is_dir()


def test_tipo_estavel_entre_anos(tmp_path: Path) -> None:
    """Texto (Parquet antigo), inteiro (CSV) e double (Parquet novo): tudo double."""
    raw = tmp_path / "raw" / "carga"
    raw.mkdir(parents=True)
    pl.DataFrame({"val_cargaenergiamwmed": ["2243.51250000", "0E-8"]}).write_parquet(
        raw / "carga-energia_2000@20261101.parquet"
    )
    (raw / "carga-energia_2001@20261101.csv").write_text(
        "val_cargaenergiamwmed\n10\n20\n", encoding="utf-8"
    )
    pl.DataFrame({"val_cargaenergiamwmed": [7649.4, 1.5]}).write_parquet(
        raw / "carga-energia_2026@20261101.parquet"
    )
    res = converter.convert(tmp_path / "raw", tmp_path / "lake")
    assert not res.errors
    ds = tmp_path / "lake" / "ons" / "carga-energia"
    tipos = {
        pl.read_parquet(p).schema["val_cargaenergiamwmed"]
        for p in ds.rglob("*.parquet")
    }
    assert tipos == {pl.Float64}


def test_valor_nao_numerico_e_erro_nunca_nulo(tmp_path: Path) -> None:
    raw = tmp_path / "raw" / "carga"
    raw.mkdir(parents=True)
    pl.DataFrame({"val_cargaenergiamwmed": ["1.5", "abc"]}).write_parquet(
        raw / "carga-energia_2000@20261101.parquet"
    )
    res = converter.convert(tmp_path / "raw", tmp_path / "lake")
    assert res.converted == 0
    assert len(res.errors) == 1
    assert "val_cargaenergiamwmed" in res.errors[0]
    assert "abc" in res.errors[0]


def test_separador_ambiguo_e_erro() -> None:
    df = pl.DataFrame({"val_cargaenergiamwmed": ["1.234,5", "2,5"]})
    with pytest.raises(ValueError, match="ambiguo"):
        converter_numericas(df, "carga-energia")


def test_colunas_de_outro_dataset_ficam_como_estao() -> None:
    df = pl.DataFrame({"val_cargaenergiamwmed": ["1.5"], "cod": ["001"]})
    assert converter_numericas(df, "usina_conjunto").equals(df)


def test_tipos_cobrem_so_datasets_declarados() -> None:
    assert set(COLUNAS_NUMERICAS) == set(converter.datasets())


def test_esquemas_de_referencia_numericos_sao_double() -> None:
    """Os .schema.json descrevem o lake já reconvertido: double nas numéricas."""
    for dataset, colunas in COLUNAS_NUMERICAS.items():
        schema = json.loads((DOCS / f"{dataset}.schema.json").read_text("utf-8"))
        por_nome = {c["nome"]: c["tipos"] for c in schema["colunas"]}
        for col in colunas:
            if col in por_nome:
                assert por_nome[col] == ["double"], (dataset, col, por_nome[col])
