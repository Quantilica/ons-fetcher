---
dataset:
  id: ena-diario-por-bacia
  fonte: ons
  titulo: "ENA Diário por Bacia (ONS)"
  resumo: "Energia natural afluente (ENA) diária por bacia hidro-energética, bruta e armazenável, em MWmed e como percentual da média de longo termo (MLT)."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ena-diario-por-bacia
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-bacia"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a ENA de uma bacia em um dia"
  granularidade: {espacial: "bacia hidro-energética", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, nom_bacia, ena_data], colunas: 6}
  unidades_de_medida:
    ena_bruta_bacia_mwmed: "MWmed"
    ena_bruta_bacia_percentualmlt: "% da MLT"
    ena_armazenavel_bacia_mwmed: "MWmed"
    ena_armazenavel_bacia_percentualmlt: "% da MLT"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# ENA Diário por Bacia

## Resumo

Energia natural afluente (ENA) diária por bacia hidro-energética, bruta e armazenável, em MWmed e como percentual da média de longo termo (MLT). A energia natural afluente (ENA) bruta é a energia produzível pela usina, calculada pelo produto das vazões naturais pelas produtividades a 65% dos volumes úteis; a ENA armazenável desconta as vazões vertidas.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ena-diario-por-bacia` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ena-diario-por-bacia |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-bacia |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a ENA de uma bacia em um dia |
| Granularidade | espacial: bacia hidro-energética; temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `nom_bacia`, `ena_data` |
| Colunas | 6 |
| Unidades de medida | `ena_bruta_bacia_mwmed`: MWmed; `ena_bruta_bacia_percentualmlt`: % da MLT; `ena_armazenavel_bacia_mwmed`: MWmed; `ena_armazenavel_bacia_percentualmlt`: % da MLT |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ena-diario-por-bacia`, https://dados.ons.org.br/dataset/ena-diario-por-bacia). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ena_bacia_di/`.
- O ONS publica um arquivo por ano com o prefixo `ENA_DIARIO_BACIAS` (`ENA_DIARIO_BACIAS_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `hidrologia/ena-diario-por-bacia_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a ENA de uma bacia em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 8.475 linhas no primeiro e 11.112 no último; 222.242 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `nom_bacia` | `nom_bacia` | texto | Nome curto da Bacia Hidro-Energética | — | todo |
| `ena_data` | `ena_data` | texto | Dia observado da medida | — | todo |
| `ena_bruta_bacia_mwmed` | `ena_bruta_bacia_mwmed` | decimal | Valor de ENA bruta por Bacia na unidade de medida MWmês. | MWmed | todo |
| `ena_bruta_bacia_percentualmlt` | `ena_bruta_bacia_percentualmlt` | decimal | Valor de ENA bruta por Bacia em percentual por média de longo termo-MLT (%) | % da MLT | todo |
| `ena_armazenavel_bacia_mwmed` | `ena_armazenavel_bacia_mwmed` | decimal | Valor de ENA armazenável por Bacia na unidade de medida MWmês | MWmed | todo |
| `ena_armazenavel_bacia_percentualmlt` | `ena_armazenavel_bacia_percentualmlt` | decimal | Valor de ENA armazenável por Bacia em percentual por média de longo termo-MLT (%) | % da MLT | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ena-diario-por-bacia`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`ENA_DIARIO_BACIAS_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- A descrição oficial das colunas `*_mwmed` diz 'MWmês'; o nome da coluna e o conjunto de ENA por reservatório usam MWmed.
- `ena_data` é texto (`AAAA-MM-DD`).

## Exemplos

ENA bruta (percentual da MLT) por bacia no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT nom_bacia, ena_data, ena_bruta_bacia_percentualmlt
    FROM read_parquet('lake/ons/ena-diario-por-bacia/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ena_data = (SELECT max(ena_data) FROM read_parquet('lake/ons/ena-diario-por-bacia/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 3 DESC
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-bacia
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_bacia_di/DicionarioDados_EnaPorBacia.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
