---
dataset:
  id: ena-diario-por-ree
  fonte: ons
  titulo: "ENA Diário por REE - Reservatório Equivalente de Energia (ONS)"
  resumo: "Energia natural afluente (ENA) diária por reservatório equivalente de energia (REE), bruta e armazenável."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ena-diario-por-ree-reservatorio-equivalente-de-energia
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-ree-reservatorio-equivalente-de-energia"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2016, fim: em-curso}
  unidade: "a ENA de um REE em um dia"
  granularidade: {espacial: "reservatório equivalente de energia (REE)", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, nom_reservatorioee, ena_data], colunas: 6}
  unidades_de_medida:
    ena_bruta_ree_mwmed: "MWmed"
    ena_bruta_ree_percentualmlt: "% da MLT"
    ena_armazenavel_ree_mwmed: "MWmed"
    ena_armazenavel_ree_percentualmlt: "% da MLT"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# ENA Diário por REE - Reservatório Equivalente de Energia

## Resumo

Energia natural afluente (ENA) diária por reservatório equivalente de energia (REE), bruta e armazenável. A energia natural afluente (ENA) bruta é a energia produzível pela usina, calculada pelo produto das vazões naturais pelas produtividades a 65% dos volumes úteis; a ENA armazenável desconta as vazões vertidas.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ena-diario-por-ree` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ena-diario-por-ree-reservatorio-equivalente-de-energia |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-ree-reservatorio-equivalente-de-energia |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2016 a em-curso |
| Unidade (uma linha) | a ENA de um REE em um dia |
| Granularidade | espacial: reservatório equivalente de energia (REE); temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `nom_reservatorioee`, `ena_data` |
| Colunas | 6 |
| Unidades de medida | `ena_bruta_ree_mwmed`: MWmed; `ena_bruta_ree_percentualmlt`: % da MLT; `ena_armazenavel_ree_mwmed`: MWmed; `ena_armazenavel_ree_percentualmlt`: % da MLT |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ena-diario-por-ree-reservatorio-equivalente-de-energia`, https://dados.ons.org.br/dataset/ena-diario-por-ree-reservatorio-equivalente-de-energia). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ena_ree_di/`.
- O ONS publica um arquivo por ano com o prefixo `ENA_DIARIO_REE` (`ENA_DIARIO_REE_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 11 arquivos Parquet e 11 CSV, de 2016 a 2026.
- No bruto, o arquivo fica em `hidrologia/ena-diario-por-ree_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a ENA de um REE em um dia.
- 11 arquivos convertidos (todos os publicados), de 2016 a 2026: 3.294 linhas no primeiro e 3.816 no último; 45.465 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `nom_reservatorioee` | `nom_ree` | texto | Nome do Reservatório Equivalente | — | todo |
| `ena_data` | `ena_data` | texto | Dia observado da medida | — | todo |
| `ena_bruta_ree_mwmed` | `ena_bruta_ree_mwmed` | decimal | Valor de ENA bruta na unidade de medida MWmês | MWmed | todo |
| `ena_bruta_ree_percentualmlt` | `ena_bruta_ree_percentualmlt` | decimal | Valor de ENA bruta percentual da média de longo termo-MLT (%) | % da MLT | todo |
| `ena_armazenavel_ree_mwmed` | `ena_armazenavel_ree_mwmed` | decimal | Valor de ENA armazenável na unidade de medida MWmês | MWmed | todo |
| `ena_armazenavel_ree_percentualmlt` | `ena_armazenavel_ree_percentualmlt` | decimal | Valor de ENA armazenável percentual da média de longo termo-MLT (%) | % da MLT | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ena-diario-por-ree`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`ENA_DIARIO_REE_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **Os valores numéricos são texto na origem em todos os anos** (texto com oito casas decimais; zero aparece como `0E-8`). O conversor os grava como `double`; o zero vem como `0.0`.
- A coluna do REE chama-se `nom_reservatorioee` no lake (o dicionário oficial escreve `nom_ree`).
- `ena_data` é texto (`AAAA-MM-DD`).

## Exemplos

ENA bruta (percentual da MLT) por REE no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT nom_reservatorioee, ena_data, ena_bruta_ree_percentualmlt AS ena_pct_mlt
    FROM read_parquet('lake/ons/ena-diario-por-ree/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ena_data = (SELECT max(ena_data) FROM read_parquet('lake/ons/ena-diario-por-ree/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 3 DESC
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-ree-reservatorio-equivalente-de-energia
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_ree_di/DicionarioDados_EnaPorResEquivalente.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
