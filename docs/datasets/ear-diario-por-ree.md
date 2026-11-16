---
dataset:
  id: ear-diario-por-ree
  fonte: ons
  titulo: "EAR Diário por REE - Reservatório Equivalente de Energia (ONS)"
  resumo: "Energia armazenada (EAR) diária por reservatório equivalente de energia (REE), em MWmês e percentual."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ear-diario-por-ree-reservatorio-equivalente-de-energia
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-ree-reservatorio-equivalente-de-energia"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2016, fim: em-curso}
  unidade: "a EAR de um REE em um dia"
  granularidade: {espacial: "reservatório equivalente de energia (REE)", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, nom_ree, ear_data], colunas: 5}
  unidades_de_medida:
    ear_max_ree: "MWmês"
    ear_verif_ree_mwmes: "MWmês"
    ear_verif_ree_percentual: "%"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# EAR Diário por REE - Reservatório Equivalente de Energia

## Resumo

Energia armazenada (EAR) diária por reservatório equivalente de energia (REE), em MWmês e percentual. A energia armazenada (EAR) é a energia associada ao volume de água nos reservatórios que pode virar geração na própria usina e em todas as usinas à jusante na cascata; a EAR máxima é a capacidade de armazenamento com todos os reservatórios cheios.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ear-diario-por-ree` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ear-diario-por-ree-reservatorio-equivalente-de-energia |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-ree-reservatorio-equivalente-de-energia |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2016 a em-curso |
| Unidade (uma linha) | a EAR de um REE em um dia |
| Granularidade | espacial: reservatório equivalente de energia (REE); temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `nom_ree`, `ear_data` |
| Colunas | 5 |
| Unidades de medida | `ear_max_ree`: MWmês; `ear_verif_ree_mwmes`: MWmês; `ear_verif_ree_percentual`: % |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ear-diario-por-ree-reservatorio-equivalente-de-energia`, https://dados.ons.org.br/dataset/ear-diario-por-ree-reservatorio-equivalente-de-energia). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ear_ree_di/`.
- O ONS publica um arquivo por ano com o prefixo `EAR_DIARIO_REE` (`EAR_DIARIO_REE_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 11 arquivos Parquet e 11 CSV, de 2016 a 2026.
- No bruto, o arquivo fica em `hidrologia/ear-diario-por-ree_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a EAR de um REE em um dia.
- 11 arquivos convertidos (todos os publicados), de 2016 a 2026: 3.294 linhas no primeiro e 3.816 no último; 45.465 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `nom_ree` | `nom_ree` | texto | Nome do Reservatório Equivalente | — | todo |
| `ear_data` | `ear_data` | texto | Dia Observado da Medida | — | todo |
| `ear_max_ree` | `ear_max_ree` | decimal | Valor de EAR Máxima, em Mwmês | MWmês | todo |
| `ear_verif_ree_mwmes` | `ear_verif_ree_mwmes` | decimal | Valor de EAR Verificada no Dia, em Mwmês | MWmês | todo |
| `ear_verif_ree_percentual` | `ear_verif_ree_percentual` | decimal | Valor de EAR Verificada no Dia, em % | % | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ear-diario-por-ree`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`EAR_DIARIO_REE_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **Os valores numéricos são texto na origem em todos os anos** (o arquivo do ONS grava `ear_max_ree`, `ear_verif_ree_mwmes` e `ear_verif_ree_percentual` como texto com oito casas decimais; zero aparece como `0E-8`). O conversor os grava como `double`; o zero vem como `0.0`.
- `ear_data` é texto (`AAAA-MM-DD`).

## Exemplos

EAR verificada (percentual) por REE no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT nom_ree, ear_data, ear_verif_ree_percentual AS ear_pct
    FROM read_parquet('lake/ons/ear-diario-por-ree/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ear_data = (SELECT max(ear_data) FROM read_parquet('lake/ons/ear-diario-por-ree/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 3 DESC
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-ree-reservatorio-equivalente-de-energia
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ear_ree_di/DicionarioDados_EarPorResEquivalente.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
