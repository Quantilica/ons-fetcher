---
dataset:
  id: carga-mensal
  fonte: ons
  titulo: "Carga de Energia Mensal (ONS)"
  resumo: "Carga de energia por subsistema em base mensal, em MWmed, apurada com os dados de medição para faturamento enviados pela CCEE ao ONS."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/carga-mensal
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/carga-mensal"
  periodicidade: "mensal (arquivo único, atualizado diariamente)"
  cobertura: {inicio: 2000-01, fim: em-curso}
  unidade: "a carga de um subsistema em um mês"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste)", temporal: "mensal"}
  formato_bruto: "um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização"
  lake: {estado: convertido, particoes: [], chave: [id_subsistema, din_instante], colunas: 4}
  unidades_de_medida:
    val_cargaenergiamwmed: "MWmed"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Carga de Energia Mensal

## Resumo

Carga de energia por subsistema em base mensal, em MWmed, apurada com os dados de medição para faturamento enviados pela CCEE ao ONS.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/carga-mensal` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/carga-mensal |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/carga-mensal |
| Periodicidade | mensal (arquivo único, atualizado diariamente) |
| Cobertura | 2000-01 a em-curso |
| Unidade (uma linha) | a carga de um subsistema em um mês |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste); temporal: mensal |
| Formato bruto | um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização |
| Estado no lake | convertido |
| Partições | — |
| Chave | `id_subsistema`, `din_instante` |
| Colunas | 4 |
| Unidades de medida | `val_cargaenergiamwmed`: MWmed |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `carga-mensal`, https://dados.ons.org.br/dataset/carga-mensal). Os arquivos ficam no bucket público S3 do ONS, em `dataset/carga_energia_me/`.
- O ONS publica um arquivo único (`CARGA_MENSAL.parquet`, e as mesmas tabelas em CSV e XLSX) com a série mensal inteira, desde 2000-01, e o reenvia a cada atualização.
- No bruto, o arquivo fica em `carga/carga-mensal_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a carga de um subsistema em um mês.
- Um único arquivo com 1.292 linhas em 2026-11-15: a série mensal de 2000-01 a 2026-11 para os quatro subsistemas.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `din_instante` | `din_instante` | data e hora | Data de referência | — | todo |
| `val_cargaenergiamwmed` | `val_cargaenergiamwmed` | decimal | Valor da Carga de Energia, em MWmed | MWmed | todo |

## No lake

- Dataset `ons/carga-mensal`, sem partição (arquivo único); um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.

## Cuidados de uso

- **A definição de carga mudou.** Até 2014-12, é a carga atendida por usinas despachadas ou programadas pelo ONS; de 2015-01 a 2021-02, soma as não despachadas; desde 2023-04-29, soma a micro e minigeração distribuída (MMGD) estimada (descrição oficial do conjunto).
- O código do subsistema vem com espaço à direita em parte das linhas (`'N '`, `'S '`); aplique `trim` antes de juntar com outras tabelas.
- **Os dois últimos meses vêm zerados.** Em 2026-11-15, as linhas de 2026-10-31 e de 2026-11-30 trazem carga zero (o ONS grava `0E-8`) para os quatro subsistemas: o mês ainda não foi apurado. Descarte meses com carga zero antes de analisar.
- O arquivo traz um único Parquet sem histórico por ano: o ONS republica a série inteira a cada atualização, e o lake guarda só a última versão.
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `id_subsistema` (646 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Carga mensal do SIN (soma dos subsistemas) dos últimos 12 meses publicados, em MWmed.

```python
import duckdb

duckdb.sql("""
    SELECT din_instante, round(sum(val_cargaenergiamwmed), 0) AS carga_mwmed
    FROM read_parquet('lake/ons/carga-mensal/**/*.parquet', hive_partitioning = true, union_by_name = true)
    GROUP BY 1
    HAVING sum(val_cargaenergiamwmed) > 0
    ORDER BY 1 DESC
    LIMIT 12
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/carga-mensal
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/carga_energia_me/DicionarioDados_Carga_Energia_Mensal.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
