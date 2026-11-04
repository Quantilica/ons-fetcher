"""Testes do ``discover`` do ONS com amostra gravada do package_search."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from ons_fetcher.discover import discover, parse_period

FIXTURE = Path(__file__).parent / "fixtures" / "package_search_amostra.json"


def _packages() -> list[dict]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["packages"]


def test_parse_period() -> None:
    assert parse_period("CARGA_ENERGIA_2024.parquet") == "2024"
    assert parse_period("GERACAO_USINA-2_2024_03.csv") == "2024-03"
    assert parse_period("BALANCO_DESSEM_GERAL_2025_05_23.parquet") == "2025-05-23"
    assert parse_period("CAPACIDADE_GERACAO.csv") is None


def test_sem_novidades_na_amostra() -> None:
    """A amostra gravada coincide com o snapshot: nada novo; ausentes = removidos."""
    report = discover(_packages())
    assert report.new_packages == []
    assert report.moved_dirs == []
    assert report.new_periods == {}
    assert report.known == 5  # ambiente-colaborativo é excluído, não conta
    assert "carga-energia" not in report.removed_packages


def test_detecta_pacote_novo_periodo_novo_e_diretorio_movido() -> None:
    """Pacote inédito, ano posterior ao snapshot e s3_dir alterado são reportados."""
    packages = _packages()
    base = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset"
    carga = next(p for p in packages if p["name"] == "carga-energia")
    carga["resources"].append(
        {
            "url": f"{base}/carga_energia_di/CARGA_ENERGIA_2031.parquet",
            "format": "PARQUET",
        }
    )
    cmo = next(p for p in packages if p["name"] == "cmo-semanal")
    moved = copy.deepcopy(cmo)
    for res in moved["resources"]:
        res["url"] = res["url"].replace("/cmo_se/", "/cmo_se_novo/")
    packages[packages.index(cmo)] = moved
    packages.append(
        {
            "name": "conjunto-inedito",
            "title": "Conjunto inédito",
            "resources": [
                {
                    "url": f"{base}/inedito_ho/INEDITO_2026_01.parquet",
                    "format": "PARQUET",
                }
            ],
        }
    )

    report = discover(packages)

    assert [p["ckan_slug"] for p in report.new_packages] == ["conjunto-inedito"]
    assert report.new_packages[0]["s3_dir"] == "inedito_ho"
    assert report.new_periods["carga-energia"] == ["2031"]
    assert report.moved_dirs == [
        {"ckan_slug": "cmo-semanal", "catalogo": "cmo_se", "atual": "cmo_se_novo"}
    ]
    assert report.has_changes
