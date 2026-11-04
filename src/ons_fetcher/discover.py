"""Descoberta de conjuntos e períodos novos do ONS em relação ao catálogo estático.

Compara o ``package_search`` do CKAN com :data:`ons_fetcher.catalog.CATALOG` e
com o snapshot de períodos em :mod:`ons_fetcher.catalog_snapshot`:

- pacotes novos no CKAN que o catálogo não conhece;
- pacotes do catálogo que sumiram do CKAN;
- diretórios S3 que mudaram (o diretório vem da URL dos recursos, nunca do slug);
- períodos posteriores ao último do snapshot em conjuntos periódicos.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Iterable
from dataclasses import asdict, dataclass, field
from typing import Any

from .catalog import CATALOG
from .catalog_snapshot import EXCLUDED, SNAPSHOT
from .client import OnsClient

__all__ = ["DiscoverReport", "discover", "parse_period"]

_DATA_EXTS = {"parquet", "csv", "xlsx", "zip"}
_PERIOD_RE = re.compile(
    r"^.*?[_-]?(\d{4})(?:_(\d{2}))?(?:_(\d{2}))?\.(\w+)$",
)
_S3_DIR_RE = re.compile(r"/dataset/([^/]+)/")
_SKIP_HINTS = ("dicionario", "dicion", "metadado")


def parse_period(filename: str) -> str | None:
    """Extrai ``AAAA``, ``AAAA-MM`` ou ``AAAA-MM-DD`` do nome do arquivo."""
    match = _PERIOD_RE.match(filename)
    if not match or not 1990 <= int(match.group(1)) <= 2100:
        return None
    return "-".join(part for part in match.groups()[:3] if part)


@dataclass
class DiscoverReport:
    """Resultado de :func:`discover`."""

    new_packages: list[dict[str, Any]] = field(default_factory=list)
    removed_packages: list[str] = field(default_factory=list)
    moved_dirs: list[dict[str, str]] = field(default_factory=list)
    new_periods: dict[str, list[str]] = field(default_factory=dict)
    known: int = 0

    @property
    def has_changes(self) -> bool:
        """Indica se há algo novo, removido ou movido em relação ao catálogo."""
        return bool(
            self.new_packages
            or self.removed_packages
            or self.moved_dirs
            or self.new_periods
        )

    def to_dict(self) -> dict[str, Any]:
        """Converte o relatório em dict serializável."""
        data = asdict(self)
        data["has_changes"] = self.has_changes
        return data


def _data_files(package: dict[str, Any]) -> tuple[str | None, list[str]]:
    """Retorna ``(diretório_s3, nomes_de_arquivos_de_dados)`` de um pacote."""
    dirs: Counter[str] = Counter()
    candidates: list[tuple[str, str]] = []
    for resource in package.get("resources") or []:
        url = str(resource.get("url") or "")
        match = _S3_DIR_RE.search(url)
        if not match:
            continue
        name = url.rsplit("/", 1)[-1]
        if any(h in name.lower() for h in _SKIP_HINTS):
            continue
        if name.rsplit(".", 1)[-1].lower() not in _DATA_EXTS:
            continue
        dirs[match.group(1)] += 1
        candidates.append((match.group(1), name))
    if not dirs:
        return None, []
    top = dirs.most_common(1)[0][0]
    return top, [name for d, name in candidates if d == top]


def discover(
    packages: Iterable[dict[str, Any]] | None = None,
    *,
    client: OnsClient | None = None,
) -> DiscoverReport:
    """Compara o CKAN do ONS com o catálogo estático.

    Args:
        packages: Pacotes do ``package_search``; se ``None``, consulta o CKAN.
        client: Cliente do ONS (usado só quando ``packages`` é ``None``).

    Returns:
        DiscoverReport: Pacotes novos/removidos, diretórios movidos e períodos novos.
    """
    if packages is None:
        packages = (client or OnsClient()).search_packages(rows=1000)

    by_slug = {str(p["name"]): p for p in packages}
    report = DiscoverReport()
    ckan_to_slug = {ds.ckan_slug: ds for ds in CATALOG.values()}

    for ckan_slug, package in sorted(by_slug.items()):
        if ckan_slug in EXCLUDED:
            continue
        s3_dir, files = _data_files(package)
        dataset = ckan_to_slug.get(ckan_slug)
        if dataset is None:
            periods = sorted({p for f in files if (p := parse_period(f))})
            report.new_packages.append(
                {
                    "ckan_slug": ckan_slug,
                    "title": package.get("title", ckan_slug),
                    "s3_dir": s3_dir or "",
                    "n_files": len(files),
                    "last_period": periods[-1] if periods else "",
                }
            )
            continue
        report.known += 1
        if s3_dir and s3_dir != dataset.s3_dir:
            report.moved_dirs.append(
                {"ckan_slug": ckan_slug, "catalogo": dataset.s3_dir, "atual": s3_dir}
            )
        if dataset.granularity not in {"annual", "monthly", "mixed", "daily"}:
            continue
        _, _, last = SNAPSHOT.get(ckan_slug, (0, "", ""))
        if not last:
            continue
        fresh = sorted(
            {
                p
                for f in files
                if (p := parse_period(f)) and p.count("-") == last.count("-")
                if p > last
            }
        )
        if fresh:
            report.new_periods[ckan_slug] = fresh

    report.removed_packages = sorted(
        ds.ckan_slug for ds in CATALOG.values() if ds.ckan_slug not in by_slug
    )
    return report
