---
dataset:
  id: dados-hidrologicos-res
  fonte: ons
  titulo: "Dados Hidráulicos por Reservatório – Base diária (ONS)"
  resumo: "Dados hidráulicos verificados dos reservatórios, em base diária: níveis a montante e a jusante, volume útil e as vazões afluente, turbinada, vertida, defluente, natural e outras."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/dados-hidrologicos-res
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/dados-hidrologicos-res"
  periodicidade: "diária (o ONS atualiza três vezes ao dia)"
  cobertura: {inicio: 1960, fim: em-curso}
  unidade: "um reservatório em um dia"
  granularidade: {espacial: "reservatório", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_reservatorio, din_instante], colunas: 25}
  unidades_de_medida:
    val_nivelmontante: "m"
    val_niveljusante: "m"
    val_volumeutilcon: "% (volume útil)"
    val_vazaoafluente: "m3/s"
    val_vazaoturbinada: "m3/s"
    val_vazaovertida: "m3/s"
    val_vazaooutrasestruturas: "m3/s"
    val_vazaodefluente: "m3/s"
    val_vazaotransferida: "m3/s"
    val_vazaonatural: "m3/s"
    val_vazaoartificial: "m3/s"
    val_vazaoincremental: "m3/s"
    val_vazaoevaporacaoliquida: "m3/s"
    val_vazaousoconsuntivo: "m3/s"
    val_vazaoincrementalbruta: "m3/s"
    num_ordemcs: "código (sem unidade)"
    cod_usina: "código (sem unidade)"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Dados Hidráulicos por Reservatório – Base diária

## Resumo

Dados hidráulicos verificados dos reservatórios, em base diária: níveis a montante e a jusante, volume útil e as vazões afluente, turbinada, vertida, defluente, natural e outras.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/dados-hidrologicos-res` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/dados-hidrologicos-res |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/dados-hidrologicos-res |
| Periodicidade | diária (o ONS atualiza três vezes ao dia) |
| Cobertura | 1960 a em-curso |
| Unidade (uma linha) | um reservatório em um dia |
| Granularidade | espacial: reservatório; temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_reservatorio`, `din_instante` |
| Colunas | 25 |
| Unidades de medida | `val_nivelmontante`: m; `val_niveljusante`: m; `val_volumeutilcon`: % (volume útil); `val_vazaoafluente`: m3/s; `val_vazaoturbinada`: m3/s; `val_vazaovertida`: m3/s; `val_vazaooutrasestruturas`: m3/s; `val_vazaodefluente`: m3/s; `val_vazaotransferida`: m3/s; `val_vazaonatural`: m3/s; `val_vazaoartificial`: m3/s; `val_vazaoincremental`: m3/s; `val_vazaoevaporacaoliquida`: m3/s; `val_vazaousoconsuntivo`: m3/s; `val_vazaoincrementalbruta`: m3/s; `num_ordemcs`: código (sem unidade); `cod_usina`: código (sem unidade) |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `dados-hidrologicos-res`, https://dados.ons.org.br/dataset/dados-hidrologicos-res). Os arquivos ficam no bucket público S3 do ONS, em `dataset/dados_hidrologicos_di/`.
- O ONS publica um arquivo por ano com o prefixo `DADOS_HIDROLOGICOS_RES` (`DADOS_HIDROLOGICOS_RES_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 62 arquivos Parquet e 62 CSV, de 1960 a 2026.
- No bruto, o arquivo fica em `hidrologia/dados-hidrologicos-res_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: um reservatório em um dia.
- 62 arquivos convertidos (todos os publicados), de 1960 a 2026: 40.779 linhas no primeiro e 55.601 no último; 3.531.997 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Identificador do subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do subsistema | — | todo |
| `tip_reservatorio` | `tip_reservatorio` | texto | Tipo do reservatório | — | todo |
| `nom_bacia` | `nom_bacia` | texto | Nome da bacia em que o reservatório está localizado | — | todo |
| `nom_ree` | `nom_ree` | texto | Nome do reservatório equivalente de energia do reservatório | — | todo |
| `id_reservatorio` | `id_reservatorio` | texto | Identificador do reservatório | — | todo |
| `nom_reservatorio` | `nom_reservatorio` | texto | Nome do reservatório | — | todo |
| `num_ordemcs` | `num_ordemcs` | inteiro | Ordem do reservatório na cascata | código (sem unidade) | todo |
| `cod_usina` | `cod_usina` | inteiro | Código da usina nos modelos de otimização | código (sem unidade) | todo |
| `din_instante` | `din_instante` | data e hora | Data | — | todo |
| `val_nivelmontante` | `val_nivelmontante` | decimal | Valor do nível montante, em metros | m | todo |
| `val_niveljusante` | `val_niveljusante` | decimal | Valor do nível jusante, em metros | m | todo |
| `val_volumeutilcon` | `val_volumeutilcon` | decimal | Valor do volume útil consistido (%) | % (volume útil) | todo |
| `val_vazaoafluente` | `val_vazaoafluente` | decimal | Vazão afluente em m3/s | m3/s | todo |
| `val_vazaoturbinada` | `val_vazaoturbinada` | decimal | Vazão turbinada, em m3/s | m3/s | todo |
| `val_vazaovertida` | `val_vazaovertida` | decimal | Vazão vertida, em m3/s | m3/s | todo |
| `val_vazaooutrasestruturas` | `val_vazaooutrasestruturas` | decimal | Vazão de outras estruturadas, em m3/s | m3/s | todo |
| `val_vazaodefluente` | `val_vazaodefluente` | decimal | Vazão defluente, em m3/s | m3/s | todo |
| `val_vazaotransferida` | `val_vazaotransferida` | decimal | Vazão transferida, em m3/s | m3/s | todo |
| `val_vazaonatural` | `val_vazaonatural` | decimal | Vazão natural, em m3/s | m3/s | todo |
| `val_vazaoartificial` | `val_vazaoartificial` | decimal | Vazão artificial, em m3/s | m3/s | todo |
| `val_vazaoincremental` | `val_vazaoincremental` | decimal | Vazão incremental, em m3/s | m3/s | todo |
| `val_vazaoevaporacaoliquida` | `val_vazaoevaporacaoliquida` | decimal | Vazão de evaporação líquida, em m3/s | m3/s | todo |
| `val_vazaousoconsuntivo` | `val_vazaousoconsuntivo` | decimal | Vazão de uso consuntivo, em m3/s | m3/s | todo |
| `val_vazaoincrementalbruta` | `val_vazaoincrementalbruta` | decimal | Vazão incremental bruta, em m3/s | m3/s | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/dados-hidrologicos-res`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`DADOS_HIDROLOGICOS_RES_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- O ONS atualiza este conjunto três vezes ao dia (9h15, 14h15 e 17h) e avisa que os dados passam por consistência recorrente.
- Em 2025 há duas repetições de `id_reservatorio` e `din_instante` (reservatórios `PPPRNP` e `AMSAPI`, 2025-01-01) com `cod_usina` diferentes.
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `id_subsistema` (914.873 linhas); `nom_bacia` (3.507.984 linhas); `nom_ree` (665.664 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Vazão turbinada média por reservatório em 2026, em m3/s, dos dez maiores.

```python
import duckdb

duckdb.sql("""
    SELECT nom_reservatorio, round(avg(val_vazaoturbinada), 1) AS turbinada_media_m3s
    FROM read_parquet('lake/ons/dados-hidrologicos-res/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/dados-hidrologicos-res
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/dados_hidrologicos_di/DicionarioDados_DadosHidrologicosDiarios.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
