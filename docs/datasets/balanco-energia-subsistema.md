---
dataset:
  id: balanco-energia-subsistema
  fonte: ons
  titulo: "Balanço de Energia nos Subsistemas (ONS)"
  resumo: "Balanço de energia por subsistema em base horária: a carga e a oferta verificadas (geração hidráulica, térmica, eólica e fotovoltaica) e o intercâmbio líquido, em MWmed."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/balanco-energia-subsistema
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/balanco-energia-subsistema"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "o balanço de energia de um subsistema em uma hora"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste) e SIN", temporal: "horária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema, din_instante], colunas: 9}
  unidades_de_medida:
    val_gerhidraulica: "MWmed"
    val_gertermica: "MWmed"
    val_gereolica: "MWmed"
    val_gersolar: "MWmed"
    val_carga: "MWmed"
    val_intercambio: "MWmed"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Balanço de Energia nos Subsistemas

## Resumo

Balanço de energia por subsistema em base horária: a carga e a oferta verificadas (geração hidráulica, térmica, eólica e fotovoltaica) e o intercâmbio líquido, em MWmed.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/balanco-energia-subsistema` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/balanco-energia-subsistema |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/balanco-energia-subsistema |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | o balanço de energia de um subsistema em uma hora |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste) e SIN; temporal: horária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema`, `din_instante` |
| Colunas | 9 |
| Unidades de medida | `val_gerhidraulica`: MWmed; `val_gertermica`: MWmed; `val_gereolica`: MWmed; `val_gersolar`: MWmed; `val_carga`: MWmed; `val_intercambio`: MWmed |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `balanco-energia-subsistema`, https://dados.ons.org.br/dataset/balanco-energia-subsistema). Os arquivos ficam no bucket público S3 do ONS, em `dataset/balanco_energia_subsistema_ho/`.
- O ONS publica um arquivo por ano com o prefixo `BALANCO_ENERGIA_SUBSISTEMA` (`BALANCO_ENERGIA_SUBSISTEMA_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `intercambio/balanco-energia-subsistema_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: o balanço de energia de um subsistema em uma hora.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 43.915 linhas no primeiro e 38.040 no último; 1.177.557 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema da Usina | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `din_instante` | `din_instante` | data e hora | Data de Referência | — | todo |
| `val_gerhidraulica` | `val_gerhidraulica` | decimal | Valor verificado de geração hidráulica, em MWmed | MWmed | todo |
| `val_gertermica` | `val_gertermica` | decimal | Valor verificado de geração térmica, em MWmed | MWmed | todo |
| `val_gereolica` | `val_gereolica` | decimal | Valor verificado de geração eólica, em MWmed | MWmed | todo |
| `val_gersolar` | `val_gersolar` | decimal | Valor verificado de geração fotovoltaica, em MWmed | MWmed | todo |
| `val_carga` | `val_carga` | decimal | Valor verificado da carga, em MWmed | MWmed | todo |
| `val_intercambio` | `val_intercambio` | decimal | Valor verificado do intercâmbio líquido, em MWmed | MWmed | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/balanco-energia-subsistema`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`BALANCO_ENERGIA_SUBSISTEMA_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- O arquivo traz as linhas dos quatro subsistemas e a do total (`SIN`).
- O código do subsistema vem com espaços à direita em 2026 (`'N  '`, `'SE '`); aplique `trim` antes de agrupar ou juntar.
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `id_subsistema` (30.432 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Geração por fonte do SIN em 2026, em MWmed médios.

```python
import duckdb

duckdb.sql("""
    SELECT round(avg(val_gerhidraulica), 0) AS hidraulica, round(avg(val_gertermica), 0) AS termica,
           round(avg(val_gereolica), 0) AS eolica, round(avg(val_gersolar), 0) AS solar
    FROM read_parquet('lake/ons/balanco-energia-subsistema/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND id_subsistema = 'SIN'
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/balanco-energia-subsistema
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/balanco_energia_subsistema_ho/DicionarioDados_Balanco_Energia_Subsistema.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
