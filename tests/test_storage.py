"""Tests for ons_fetcher.storage module."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from ons_fetcher.storage import DataRepository


def test_path_for_entry_fallback_timestamp() -> None:
    """When last_modified=None, the filename gets today's @YYYYMMDD timestamp."""
    repo = DataRepository(Path("/tmp/test"))
    entry = {"group": "test", "base_id": "dataset", "ext": "csv"}

    path = repo.path_for_entry(entry, last_modified=None)

    today_stamp = dt.date.today().strftime("%Y%m%d")
    expected_filename = f"dataset@{today_stamp}.csv"
    assert path.name == expected_filename


def test_path_for_entry_with_last_modified() -> None:
    """When last_modified is provided, it is used for the timestamp."""
    repo = DataRepository(Path("/tmp/test"))
    entry = {"group": "test", "base_id": "dataset", "ext": "csv"}
    last_modified = dt.date(2024, 3, 15)

    path = repo.path_for_entry(entry, last_modified=last_modified)

    assert path.name == "dataset@20240315.csv"


def test_path_for_entry_with_year_month() -> None:
    """When year and month are provided, they are used in the partition."""
    repo = DataRepository(Path("/tmp/test"))
    entry = {
        "group": "test",
        "base_id": "dataset",
        "ext": "csv",
        "year": 2024,
        "month": 3,
    }
    last_modified = dt.date(2024, 3, 15)

    path = repo.path_for_entry(entry, last_modified=last_modified)

    assert path.name == "dataset_2024-03@20240315.csv"


def test_path_for_entry_with_year_quarter() -> None:
    """When year and quarter are provided, they are used in the partition."""
    repo = DataRepository(Path("/tmp/test"))
    entry = {
        "group": "test",
        "base_id": "dataset",
        "ext": "csv",
        "year": 2024,
        "quarter": 1,
    }
    last_modified = dt.date(2024, 3, 15)

    path = repo.path_for_entry(entry, last_modified=last_modified)

    assert path.name == "dataset_2024-T01@20240315.csv"


def test_path_for_entry_with_year_only() -> None:
    """When only year is provided, it is used as the partition."""
    repo = DataRepository(Path("/tmp/test"))
    entry = {
        "group": "test",
        "base_id": "dataset",
        "ext": "csv",
        "year": 2024,
    }
    last_modified = dt.date(2024, 3, 15)

    path = repo.path_for_entry(entry, last_modified=last_modified)

    assert path.name == "dataset_2024@20240315.csv"


def test_path_for_entry_with_slug() -> None:
    """When slug is provided, it is appended to the partition."""
    repo = DataRepository(Path("/tmp/test"))
    entry = {
        "group": "test",
        "base_id": "dataset",
        "ext": "csv",
        "year": 2024,
        "month": 3,
        "slug": "submarket",
    }
    last_modified = dt.date(2024, 3, 15)

    path = repo.path_for_entry(entry, last_modified=last_modified)

    assert path.name == "dataset_2024-03_submarket@20240315.csv"