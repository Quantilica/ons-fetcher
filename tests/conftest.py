"""Pytest configuration and fixtures for ons-fetcher."""

from __future__ import annotations

import pytest

from ons_fetcher import catalog
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
    """Substitui a listagem do S3 e limpa os caches do catálogo (sem rede)."""
    monkeypatch.setattr(catalog, "_KEYS_CACHE", {})
    monkeypatch.setattr(catalog, "_GROUP_CACHE", {})
    monkeypatch.setattr(
        catalog.OnsClient, "list_dataset_keys", lambda self, s3_dir: _fake_keys(s3_dir)
    )
