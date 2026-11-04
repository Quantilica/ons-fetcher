"""Constants and endpoint definitions for ons-fetcher."""

from __future__ import annotations

from typing import Any

CKAN_BASE_URL = "https://dados.ons.org.br/api/3"
S3_BASE_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/dataset"
S3_LIST_URL = "https://ons-aws-prod-opendata.s3.amazonaws.com/"

# Chaves R1 cujo slug CKAN difere da chave (a chave é o id estável no disco/lake).
R1_CKAN_SLUGS: dict[str, str] = {
    "ear-diario-por-ree": "ear-diario-por-ree-reservatorio-equivalente-de-energia",
    "ena-diario-por-ree": "ena-diario-por-ree-reservatorio-equivalente-de-energia",
}

# S3 dataset descriptors for R1 datasets:
# (ckan_slug, s3_dir, file_prefix, group, granularity, start_year)
R1_DATASETS_META: dict[str, dict[str, Any]] = {
    # Carga
    "carga-energia": {
        "s3_dir": "carga_energia_di",
        "prefix": "CARGA_ENERGIA",
        "group": "carga",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Carga de Energia Diária",
    },
    "carga-mensal": {
        "s3_dir": "carga_energia_me",
        "prefix": "CARGA_MENSAL",
        "group": "carga",
        "granularity": "static",
        "start_year": 2000,
        "name": "Carga de Energia Mensal",
    },
    "curva-carga": {
        "s3_dir": "curva-carga-ho",
        "prefix": "CURVA_CARGA",
        "group": "carga",
        "granularity": "annual",
        "start_year": 2020,
        "name": "Curva de Carga Horária",
    },
    # Hidrologia (EAR e ENA diários x4 + dados hidrológicos)
    "ear-diario-por-bacia": {
        "s3_dir": "ear_bacia_di",
        "prefix": "EAR_DIARIO_BACIAS",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Armazenada (EAR) Diária por Bacia",
    },
    "ear-diario-por-ree": {
        "s3_dir": "ear_ree_di",
        "prefix": "EAR_DIARIO_REE",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Armazenada (EAR) Diária por REE",
    },
    "ear-diario-por-reservatorio": {
        "s3_dir": "ear_reservatorio_di",
        "prefix": "EAR_DIARIO_RESERVATORIOS",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Armazenada (EAR) Diária por Reservatório",
    },
    "ear-diario-por-subsistema": {
        "s3_dir": "ear_subsistema_di",
        "prefix": "EAR_DIARIO_SUBSISTEMA",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Armazenada (EAR) Diária por Subsistema",
    },
    "ena-diario-por-bacia": {
        "s3_dir": "ena_bacia_di",
        "prefix": "ENA_DIARIO_BACIAS",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Natural Afluente (ENA) Diária por Bacia",
    },
    "ena-diario-por-ree": {
        "s3_dir": "ena_ree_di",
        "prefix": "ENA_DIARIO_REE",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Natural Afluente (ENA) Diária por REE",
    },
    "ena-diario-por-reservatorio": {
        "s3_dir": "ena_reservatorio_di",
        "prefix": "ENA_DIARIO_RESERVATORIOS",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Natural Afluente (ENA) Diária por Reservatório",
    },
    "ena-diario-por-subsistema": {
        "s3_dir": "ena_subsistema_di",
        "prefix": "ENA_DIARIO_SUBSISTEMA",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Energia Natural Afluente (ENA) Diária por Subsistema",
    },
    "dados-hidrologicos-res": {
        "s3_dir": "dados_hidrologicos_di",
        "prefix": "DADOS_HIDROLOGICOS_RES",
        "group": "hidrologia",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Dados Hidrológicos Diários por Reservatório",
    },
    # Geração
    "geracao-usina-2": {
        "s3_dir": "geracao_usina_2_ho",
        "prefix": "GERACAO_USINA-2",
        "group": "geracao",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Geração de Energia por Usina (Horária)",
    },
    "fator-capacidade-2": {
        "s3_dir": "fator_capacidade_2_di",
        "prefix": "FATOR_CAPACIDADE-2",
        "group": "geracao",
        "granularity": "monthly",
        "start_year": 2012,
        "name": "Fator de Capacidade por Usina (Mensal)",
    },
    # Preços
    "cmo-semanal": {
        "s3_dir": "cmo_se",
        "prefix": "CMO_SEMANAL",
        "group": "precos",
        "granularity": "annual",
        "start_year": 2001,
        "name": "Custo Marginal de Operação (CMO) Semanal",
    },
    "cmo-semi-horario": {
        "s3_dir": "cmo_tm",
        "prefix": "CMO_SEMIHORARIO",
        "group": "precos",
        "granularity": "annual",
        "start_year": 2021,
        "name": "Custo Marginal de Operação (CMO) Semi-Horário",
    },
    "cvu-usitermica": {
        "s3_dir": "cvu_usitermica_se",
        "prefix": "CVU_USINA_TERMICA",
        "group": "precos",
        "granularity": "annual",
        "start_year": 2013,
        "name": "Custo Variável Unitário (CVU) de Usinas Térmicas",
    },
    # Intercâmbio
    "balanco-energia-subsistema": {
        "s3_dir": "balanco_energia_subsistema_ho",
        "prefix": "BALANCO_ENERGIA_SUBSISTEMA",
        "group": "intercambio",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Balanço de Energia por Subsistema",
    },
    "intercambio-nacional": {
        "s3_dir": "intercambio_nacional_ho",
        "prefix": "INTERCAMBIO_NACIONAL",
        "group": "intercambio",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Intercâmbio de Energia Nacional",
    },
    "intercambio-internacional": {
        "s3_dir": "intercambio_internacional_ho",
        "prefix": "INTERCAMBIO_INTERNACIONAL",
        "group": "intercambio",
        "granularity": "annual",
        "start_year": 2000,
        "name": "Intercâmbio de Energia Internacional",
    },
    # Cadastros
    "capacidade-geracao": {
        "s3_dir": "capacidade-geracao",
        "prefix": "CAPACIDADE_GERACAO",
        "group": "cadastros",
        "granularity": "static",
        "start_year": None,
        "name": "Cadastro de Capacidade de Geração",
    },
    "reservatorio": {
        "s3_dir": "reservatorio",
        "prefix": "RESERVATORIOS",
        "group": "cadastros",
        "granularity": "static",
        "start_year": None,
        "name": "Cadastro de Reservatórios",
    },
    "usina_conjunto": {
        "s3_dir": "usina_conjunto",
        "prefix": "USINA_CONJUNTO",
        "group": "cadastros",
        "granularity": "static",
        "start_year": None,
        "name": "Cadastro de Usinas e Conjuntos",
    },
}
