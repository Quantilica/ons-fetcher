"""HTTP and CKAN client for ONS open data."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from quantilica.core.ckan import CkanClient, pick_resources
from quantilica.core.http import HttpClient
from quantilica.core.logging import get_logger
from quantilica.core.manifests import DownloadManifest

from .constants import CKAN_BASE_URL

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
