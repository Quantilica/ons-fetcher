"""HTTP and CKAN client for ONS open data."""

from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from quantilica.core.ckan import CkanClient, pick_resources
from quantilica.core.http import HttpClient
from quantilica.core.logging import get_logger
from quantilica.core.manifests import DownloadManifest

from .constants import CKAN_BASE_URL, S3_LIST_URL

logger = get_logger(__name__)


class OnsClient:
    """Client for discovering and downloading ONS datasets via CKAN and S3."""

    def __init__(
        self,
        *,
        base_url: str = CKAN_BASE_URL,
        client: HttpClient | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.client = client or HttpClient()
        self.logger = logger or get_logger(__name__)
        self.ckan = CkanClient(base_url, client=self.client, logger=self.logger)

    def package_show(self, package_id: str) -> dict[str, Any]:
        """Fetch package details from ONS CKAN."""
        return self.ckan.package_show(package_id)

    def search_packages(
        self, q: str | None = None, rows: int = 1000
    ) -> list[dict[str, Any]]:
        """Search ONS CKAN packages."""
        return list(self.ckan.iter_packages(q=q, rows=rows))

    def pick_package_resources(
        self,
        package: dict[str, Any],
        *,
        prefer: Sequence[str] = ("PARQUET", "CSV", "ZIP"),
    ) -> list[dict[str, Any]]:
        """Pick best resources from package, prioritizing Parquet over CSV."""
        return pick_resources(package, prefer=prefer, dedupe_by_name=True)

    def download_resource(
        self,
        url: str,
        dest: Path,
        *,
        manifest_path: Path | None = None,
    ) -> DownloadManifest:
        """Download an S3 or CKAN resource with SHA-256 manifest sidecar."""
        return self.client.download_with_manifest(
            url,
            dest,
            manifest_path=manifest_path,
        )

    def list_dataset_keys(self, s3_dir: str) -> list[dict[str, Any]]:
        """Lista os objetos reais de ``dataset/<s3_dir>/`` no bucket público.

        Os nomes e a extensão dos arquivos do ONS mudam sem aviso (por exemplo,
        ``USINA_CONJUNTO.parquet`` virou ``RELACIONAMENTO_USINA_CONJUNTO.csv``).
        A listagem do S3 é a fonte de verdade do catálogo.

        Args:
            s3_dir: Diretório do dataset dentro do prefixo ``dataset/``.

        Returns:
            Lista de dicts com ``key``, ``name``, ``size`` e ``last_modified``.
        """
        namespace = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        resultados: list[dict[str, Any]] = []
        token: str | None = None
        while True:
            params: dict[str, Any] = {
                "list-type": "2",
                "prefix": f"dataset/{s3_dir}/",
                "max-keys": "1000",
            }
            if token:
                params["continuation-token"] = token
            response = self.client.get(S3_LIST_URL, params=params)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            for item in root.findall("s3:Contents", namespace):
                key = item.findtext("s3:Key", default="", namespaces=namespace)
                if not key or key.endswith("/"):
                    continue
                size_text = item.findtext("s3:Size", default="0", namespaces=namespace)
                resultados.append(
                    {
                        "key": key,
                        "name": key.rsplit("/", 1)[-1],
                        "size": int(size_text or 0),
                        "last_modified": item.findtext(
                            "s3:LastModified", default=None, namespaces=namespace
                        ),
                    }
                )
            truncated = (
                root.findtext("s3:IsTruncated", default="false", namespaces=namespace)
                == "true"
            )
            token = root.findtext(
                "s3:NextContinuationToken", default=None, namespaces=namespace
            )
            if not (truncated and token):
                break
        return resultados
