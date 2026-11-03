"""Dataset catalog for ons-fetcher.

Os descritores em :data:`R1_DATASETS_META` dizem *o que* cada dataset é
(grupo, granularidade, prefixo), mas não *qual arquivo* existe hoje: o ONS
renomeia e muda a extensão dos objetos sem aviso. O catálogo lista o bucket
S3 público e monta uma entrada por objeto real, evitando 404 em massa.
"""

from __future__ import annotations

import re
from typing import Any

from ._catalog_base import DatasetEntry, GroupInfo
from .client import OnsClient
from .constants import R1_DATASETS_META, S3_BASE_URL

__all__ = [
    "DatasetEntry",
    "GroupInfo",
    "GROUPS",
    "GROUP_ALIASES",
    "list_datasets",
]

GROUP_NAMES: dict[str, str] = {
    "carga": "Carga e Demanda do SIN",
    "hidrologia": "Hidrologia, EAR e ENA",
    "geracao": "Geração e Fator de Capacidade",
    "precos": "Preços e Custo Marginal de Operação (CMO)",
    "intercambio": "Intercâmbio e Balanço de Energia",
    "cadastros": "Cadastros de Usinas e Reservatórios",
    "programacao": "Programação da Operação (R2)",
    "indicadores": "Indicadores de Desempenho e Qualidade (R2)",
}

# cache por processo: s3_dir -> lista de objetos
_KEYS_CACHE: dict[str, list[dict[str, Any]]] = {}
# cache por processo: grupo -> entradas montadas
_GROUP_CACHE: dict[str, list[dict[str, Any]]] = {}

_SKIP_NAME_HINTS = ("dicionario", "dictionary", "metadados")
_EXT_RANK = {"parquet": 0, "csv": 1, "zip": 2, "xlsx": 3}


def _best(objects: list[dict[str, Any]]) -> dict[str, Any]:
    """Escolhe o melhor formato disponível (parquet > csv > zip > xlsx)."""
    return min(
        objects,
        key=lambda o: (_EXT_RANK.get(_ext(o["name"]), 9), -int(o.get("size") or 0)),
    )


def _keys(s3_dir: str) -> list[dict[str, Any]]:
    """Lista (com cache) os objetos reais de um diretório do bucket."""
    if s3_dir not in _KEYS_CACHE:
        _KEYS_CACHE[s3_dir] = OnsClient().list_dataset_keys(s3_dir)
    return _KEYS_CACHE[s3_dir]


def _ext(name: str) -> str:
    return name.rsplit(".", 1)[-1].lower() if "." in name else "parquet"


def _entry(
    slug: str,
    meta: dict[str, Any],
    obj: dict[str, Any],
    *,
    year: int | None = None,
    month: int | None = None,
) -> DatasetEntry:
    period = ""
    if year is not None and month is not None:
        period = f" ({year}-{month:02d})"
    elif year is not None:
        period = f" ({year})"
    return DatasetEntry(
        id=(
            f"{slug}_{year}_{month:02d}"
            if year is not None and month is not None
            else f"{slug}_{year}"
            if year is not None
            else slug
        ),
        base_id=slug,
        name=f"{meta['name']}{period}",
        url=f"{S3_BASE_URL}/{meta['s3_dir']}/{obj['name']}",
        ext=_ext(obj["name"]),
        group=meta["group"],
        year=year,
        month=month,
    )


def _entries_for_dataset(slug: str, meta: dict[str, Any]) -> list[DatasetEntry]:
    """Monta as entradas de um dataset a partir dos objetos reais do S3."""
    prefix = str(meta["prefix"])
    granularity = meta["granularity"]
    objects = [
        o
        for o in _keys(meta["s3_dir"])
        if not any(h in o["name"].lower() for h in _SKIP_NAME_HINTS)
    ]

    if granularity == "annual":
        pattern = re.compile(
            rf"^{re.escape(prefix)}_(\d{{4}})\.(parquet|csv|zip|xlsx)$", re.IGNORECASE
        )
        por_ano: dict[int, list[dict[str, Any]]] = {}
        for obj in objects:
            match = pattern.match(obj["name"])
            if match:
                por_ano.setdefault(int(match.group(1)), []).append(obj)
        return [
            _entry(slug, meta, _best(objs), year=year)
            for year, objs in sorted(por_ano.items())
        ]

    if granularity == "monthly":
        pattern = re.compile(
            rf"^{re.escape(prefix)}_(\d{{4}})_(\d{{2}})\.(parquet|csv|zip|xlsx)$",
            re.IGNORECASE,
        )
        por_mes: dict[tuple[int, int], list[dict[str, Any]]] = {}
        for obj in objects:
            match = pattern.match(obj["name"])
            if match:
                key = (int(match.group(1)), int(match.group(2)))
                por_mes.setdefault(key, []).append(obj)
        return [
            _entry(slug, meta, _best(objs), year=year, month=month)
            for (year, month), objs in sorted(por_mes.items())
        ]

    # static: arquivos cujo nome contém o prefixo; senão, o maior objeto
    candidatos = [o for o in objects if prefix.upper() in o["name"].upper()] or sorted(
        objects, key=lambda o: int(o.get("size") or 0), reverse=True
    )
    return [_entry(slug, meta, _best(candidatos))] if candidatos else []


def _group_entries(group: str) -> list[dict[str, Any]]:
    """Entradas do grupo (descobertas uma vez por processo)."""
    if group in _GROUP_CACHE:
        return _GROUP_CACHE[group]
    entries: list[dict[str, Any]] = []
    for slug, meta in R1_DATASETS_META.items():
        if meta["group"] != group:
            continue
        try:
            entries.extend(e.to_dict() for e in _entries_for_dataset(slug, meta))
        except Exception:  # noqa: BLE001 - um diretório fora do ar não derruba o grupo
            continue
    _GROUP_CACHE[group] = entries
    return entries


GROUPS: dict[str, dict[str, Any]] = {
    grp: {"name": name, "entries": []} for grp, name in GROUP_NAMES.items()
}

GROUP_ALIASES: dict[str, str] = {
    "padrao": "carga",
    "sin": "carga",
    "hidro": "hidrologia",
    "ear": "hidrologia",
    "ena": "hidrologia",
    "cmo": "precos",
    "preco": "precos",
    "usinas": "geracao",
    "troca": "intercambio",
    "cadastro": "cadastros",
}


def list_datasets(group: str | None = None) -> list[dict[str, Any]]:
    """Lista os objetos reais do bucket, por grupo."""
    if group is None:
        entries: list[dict[str, Any]] = []
        for group_id in GROUPS:
            entries.extend(_group_entries(group_id))
        return entries

    canon = GROUP_ALIASES.get(group, group)
    if canon not in GROUPS:
        raise ValueError(f"Grupo desconhecido: {group!r}")
    return list(_group_entries(canon))
