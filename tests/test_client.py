"""Tests for OnsClient."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from quantilica.core.manifests import DownloadManifest

from ons_fetcher.client import OnsClient


def test_client_init() -> None:
    client = OnsClient()
    assert client.base_url == "https://dados.ons.org.br/api/3"


def test_package_show() -> None:
    client = OnsClient()
    fake_pkg = {"id": "carga-energia", "name": "carga-energia", "resources": []}
    with patch.object(client.ckan, "package_show", return_value=fake_pkg) as mock_show:
        res = client.package_show("carga-energia")
        assert res["id"] == "carga-energia"
        mock_show.assert_called_once_with("carga-energia")


def test_search_packages() -> None:
    client = OnsClient()
    fake_pkgs = [{"id": "carga-energia"}, {"id": "cmo-semanal"}]
    with patch.object(client.ckan, "iter_packages", return_value=iter(fake_pkgs)):
        res = client.search_packages(q="energia")
        assert len(res) == 2
        assert res[0]["id"] == "carga-energia"


def test_pick_package_resources_prefers_parquet() -> None:
    client = OnsClient()
    package = {
        "resources": [
            {
                "id": "r1",
                "name": "CARGA_ENERGIA_2024",
                "format": "CSV",
                "url": "https://s3/CARGA_ENERGIA_2024.csv",
                "size": 5000000,
            },
            {
                "id": "r2",
                "name": "CARGA_ENERGIA_2024",
                "format": "PARQUET",
                "url": "https://s3/CARGA_ENERGIA_2024.parquet",
                "size": 300000,
            },
        ]
    }
    chosen = client.pick_package_resources(package)
    assert len(chosen) == 1
    assert chosen[0]["format"] == "PARQUET"
    assert chosen[0]["id"] == "r2"


def test_download_resource(tmp_path) -> None:
    client = OnsClient()
    target_file = tmp_path / "test.parquet"
    mock_manifest = MagicMock(spec=DownloadManifest)
    with patch.object(
        client.client, "download_with_manifest", return_value=mock_manifest
    ):
        res = client.download_resource("https://fake.url/file.parquet", target_file)
        assert res == mock_manifest
