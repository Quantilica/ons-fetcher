"""Colunas numéricas de cada dataset, pelo nome normalizado do lake.

O ONS publica o mesmo conjunto com tipos diferentes por ano e por formato: o
Parquet antigo grava número como texto (oito casas decimais, zero como
``0E-8``), o CSV usa ponto decimal e traz tudo como texto para quem lê com
vírgula decimal. O conversor grava estas colunas como ``double`` em todos os
anos.

A lista vem do dicionário de dados do ONS (as descrições dão a unidade: MWmed,
MWmês, %, MW, m, hm3, graus) e dos esquemas em ``docs/datasets``. Códigos
(``id_*``, ``cod_*``), nomes, datas e o texto ``val_tipoperda`` ficam de fora e
mantêm o tipo do arquivo de origem.
"""

from __future__ import annotations

_HIDROLOGICOS = (
    "val_nivelmontante",
    "val_niveljusante",
    "val_volumeutilcon",
    "val_vazaoafluente",
    "val_vazaoturbinada",
    "val_vazaovertida",
    "val_vazaooutrasestruturas",
    "val_vazaodefluente",
    "val_vazaotransferida",
    "val_vazaonatural",
    "val_vazaoartificial",
    "val_vazaoincremental",
    "val_vazaoevaporacaoliquida",
    "val_vazaousoconsuntivo",
    "val_vazaoincrementalbruta",
)

COLUNAS_NUMERICAS: dict[str, tuple[str, ...]] = {
    "carga-energia": ("val_cargaenergiamwmed",),
    "carga-mensal": ("val_cargaenergiamwmed",),
    "curva-carga": ("val_cargaenergiahomwmed",),
    "ear-diario-por-bacia": (
        "ear_max_bacia",
        "ear_verif_bacia_mwmes",
        "ear_verif_bacia_percentual",
    ),
    "ear-diario-por-ree": (
        "ear_max_ree",
        "ear_verif_ree_mwmes",
        "ear_verif_ree_percentual",
    ),
    "ear-diario-por-reservatorio": (
        "ear_reservatorio_subsistema_proprio_mwmes",
        "ear_reservatorio_subsistema_jusante_mwmes",
        "earmax_reservatorio_subsistema_proprio_mwmes",
        "earmax_reservatorio_subsistema_jusante_mwmes",
        "ear_reservatorio_percentual",
        "ear_total_mwmes",
        "ear_maxima_total_mwmes",
        "val_contribearbacia",
        "val_contribearmaxbacia",
        "val_contribearsubsistema",
        "val_contribearmaxsubsistema",
        "val_contribearsubsistemajusante",
        "val_contribearmaxsubsistemajusante",
        "val_contribearsin",
        "val_contribearmaxsin",
    ),
    "ear-diario-por-subsistema": (
        "ear_max_subsistema",
        "ear_verif_subsistema_mwmes",
        "ear_verif_subsistema_percentual",
    ),
    "ena-diario-por-bacia": (
        "ena_bruta_bacia_mwmed",
        "ena_bruta_bacia_percentualmlt",
        "ena_armazenavel_bacia_mwmed",
        "ena_armazenavel_bacia_percentualmlt",
    ),
    "ena-diario-por-ree": (
        "ena_bruta_ree_mwmed",
        "ena_bruta_ree_percentualmlt",
        "ena_armazenavel_ree_mwmed",
        "ena_armazenavel_ree_percentualmlt",
    ),
    "ena-diario-por-reservatorio": (
        "ena_bruta_res_mwmed",
        "ena_bruta_res_percentualmlt",
        "ena_armazenavel_res_mwmed",
        "ena_armazenavel_res_percentualmlt",
        "ena_queda_bruta",
        "mlt_ena",
    ),
    "ena-diario-por-subsistema": (
        "ena_bruta_regiao_mwmed",
        "ena_bruta_regiao_percentualmlt",
        "ena_armazenavel_regiao_mwmed",
        "ena_armazenavel_regiao_percentualmlt",
    ),
    "dados-hidrologicos-res": _HIDROLOGICOS,
    "geracao-usina-2": ("val_geracao",),
    "fator-capacidade-2": (
        "val_latitudesecoletora",
        "val_longitudesecoletora",
        "val_latitudepontoconexao",
        "val_longitudepontoconexao",
        "val_geracaoprogramada",
        "val_geracaoverificada",
        "val_capacidadeinstalada",
        "val_fatorcapacidade",
    ),
    "cmo-semanal": (
        "val_cmomediasemanal",
        "val_cmoleve",
        "val_cmomedia",
        "val_cmopesada",
    ),
    "cmo-semi-horario": ("val_cmo",),
    "cvu-usitermica": ("val_cvu",),
    "balanco-energia-subsistema": (
        "val_gerhidraulica",
        "val_gertermica",
        "val_gereolica",
        "val_gersolar",
        "val_carga",
        "val_intercambio",
    ),
    "intercambio-nacional": ("val_intercambiomwmed", "val_intercambioprogmwmed"),
    "intercambio-internacional": (
        "val_intercambiomwmed",
        "val_intercambioprogmwmed",
    ),
    "capacidade-geracao": ("val_potenciaefetiva",),
    "reservatorio": (
        "val_cotamaxima",
        "val_cotaminima",
        "val_volmax",
        "val_volmin",
        "val_volutiltot",
        "val_produtibilidadeespecifica",
        "val_produtividade65volutil",
        "val_perda",
        "val_latitude",
        "val_longitude",
    ),
    "usina_conjunto": (),
}
