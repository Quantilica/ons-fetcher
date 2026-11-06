"""Dataset catalog for ons-fetcher.

Os descritores em :data:`R1_DATASETS_META` dizem *o que* cada dataset é
(grupo, granularidade, prefixo), mas não *qual arquivo* existe hoje: o ONS
renomeia e muda a extensão dos objetos sem aviso. O catálogo lista o bucket S3
público e monta uma entrada por objeto real, evitando 404 em massa.

O catálogo é em duas camadas, com um módulo ``catalog_<dominio>.py`` por grupo:

- ``tier="r1"``: baixa hoje; é o que :func:`list_datasets` devolve (e o que o
  ``sync`` baixa);
- ``tier="listed"``: conhecido e catalogado, com download em release futura;
  visível em :func:`catalog_rows` e no comando ``catalogo``.
"""

from __future__ import annotations

import re
from typing import Any

from quantilica.core.logging import get_logger

from . import (
    catalog_cadastros,
    catalog_carga,
    catalog_geracao,
    catalog_hidrologia,
    catalog_indicadores,
    catalog_intercambio,
    catalog_precos,
    catalog_programacao,
)
from ._catalog_base import DatasetEntry, GroupInfo, OnsDataset
from .client import OnsClient
from .constants import R1_DATASETS_META, S3_BASE_URL

__all__ = [
    "DatasetEntry",
    "GroupInfo",
    "GROUPS",
    "GROUP_ALIASES",
    "MACRO_ALIASES",
    "CATALOG",
    "OnsDataset",
    "catalog_rows",
    "expand_group",
    "list_datasets",
]

_MODULES = [
    catalog_carga,
    catalog_hidrologia,
    catalog_geracao,
    catalog_precos,
    catalog_intercambio,
    catalog_cadastros,
    catalog_programacao,
    catalog_indicadores,
]

# slug -> descritor, de todos os conjuntos catalogados (R1 e listados).
CATALOG: dict[str, OnsDataset] = {
    slug: ds for mod in _MODULES for slug, ds in mod.DATASETS.items()
}

GROUP_NAMES: dict[str, str] = {mod.GROUP: mod.NAME for mod in _MODULES}

logger = get_logger(__name__)

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

    entries: list[DatasetEntry] = []
    if granularity in ("annual", "mixed"):
        # faixa anual; em granularidade mista pode ter prefixo proprio
        annual_prefix = str(meta.get("annual_prefix") or prefix)
        pattern = re.compile(
            rf"^{re.escape(annual_prefix)}_(\d{{4}})\.(parquet|csv|zip|xlsx)$",
            re.IGNORECASE,
        )
        por_ano: dict[int, list[dict[str, Any]]] = {}
        for obj in objects:
            match = pattern.match(obj["name"])
            if match:
                por_ano.setdefault(int(match.group(1)), []).append(obj)
        entries += [
            _entry(slug, meta, _best(objs), year=year)
            for year, objs in sorted(por_ano.items())
        ]
        if granularity == "annual":
            return entries

    if granularity in ("monthly", "mixed"):
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
        entries += [
            _entry(slug, meta, _best(objs), year=year, month=month)
            for (year, month), objs in sorted(por_mes.items())
        ]
        return entries

    # static: arquivos cujo nome contém o prefixo; senão, o maior objeto
    candidatos = [o for o in objects if prefix.upper() in o["name"].upper()] or sorted(
        objects, key=lambda o: int(o.get("size") or 0), reverse=True
    )
    return [_entry(slug, meta, _best(candidatos))] if candidatos else []


class CatalogListingError(RuntimeError):
    """A listagem de um ou mais diretórios do bucket falhou."""


def _group_entries(group: str) -> list[dict[str, Any]]:
    """Entradas do grupo (descobertas uma vez por processo).

    Falha na listagem de um diretório é registrada (``warning``) e, ao final do
    grupo, levanta :class:`CatalogListingError`; o resultado parcial não é
    guardado em cache, para que um diretório fora do ar não suma do catálogo
    em silêncio.
    """
    if group in _GROUP_CACHE:
        return _GROUP_CACHE[group]
    entries: list[dict[str, Any]] = []
    falhas: list[str] = []
    for slug, meta in R1_DATASETS_META.items():
        if meta["group"] != group:
            continue
        try:
            entries.extend(e.to_dict() for e in _entries_for_dataset(slug, meta))
        except Exception as exc:  # noqa: BLE001 - registra e segue p/ listar todas as falhas
            logger.warning("Falha ao listar o diretório de %s: %s", slug, exc)
            falhas.append(slug)
    if falhas:
        raise CatalogListingError(
            f"Listagem falhou no grupo {group!r}: {', '.join(falhas)}"
        )
    _GROUP_CACHE[group] = entries
    return entries


GROUPS: dict[str, dict[str, Any]] = {
    grp: {"name": name, "entries": []} for grp, name in GROUP_NAMES.items()
}

# Macro-aliases: um apelido que engloba vários grupos canônicos (as áreas do CKAN).
MACRO_ALIASES: dict[str, list[str]] = {
    "avaliacao-da-operacao": [
        "carga",
        "hidrologia",
        "geracao",
        "intercambio",
        "indicadores",
    ],
    "programacao-da-operacao": ["programacao", "precos"],
    "integracao-de-instalacoes": ["cadastros"],
    "energia": ["carga", "geracao", "precos", "intercambio"],
}

GROUP_ALIASES: dict[str, list[str]] = {
    **MACRO_ALIASES,
    "padrao": ["carga"],
    "sin": ["carga"],
    "hidro": ["hidrologia"],
    "ear": ["hidrologia"],
    "ena": ["hidrologia"],
    "cmo": ["precos"],
    "preco": ["precos"],
    "usinas": ["geracao"],
    "troca": ["intercambio"],
    "cadastro": ["cadastros"],
}


def expand_group(key: str) -> list[str]:
    """Expande um grupo, alias ou macro-alias em ids canônicos de grupo.

    Raises:
        ValueError: Se ``key`` não for grupo nem alias.
    """
    if key in GROUPS:
        return [key]
    targets = GROUP_ALIASES.get(key)
    if targets is None:
        raise ValueError(f"Grupo desconhecido: {key!r}")
    return [t for t in targets if t in GROUPS]


def list_datasets(group: str | None = None) -> list[dict[str, Any]]:
    """Lista os objetos reais do bucket dos conjuntos R1, por grupo.

    Só o tier ``r1`` baixa hoje; os conjuntos ``listed`` aparecem em
    :func:`catalog_rows`.
    """
    groups = list(GROUPS) if group is None else expand_group(group)
    entries: list[dict[str, Any]] = []
    for group_id in groups:
        for entry in _group_entries(group_id):
            if entry not in entries:
                entries.append(entry)
    return entries


def catalog_rows(
    group: str | None = None, tier: str | None = None
) -> list[dict[str, Any]]:
    """Linhas do catálogo estático (um conjunto por linha), sem rede.

    Args:
        group: Grupo, alias ou macro-alias; ``None`` lista todos.
        tier: ``"r1"`` ou ``"listed"``; ``None`` lista ambos.
    """
    groups = set(GROUPS if group is None else expand_group(group))
    return [
        ds.to_dict()
        for ds in CATALOG.values()
        if ds.group in groups and (tier is None or ds.tier == tier)
    ]
