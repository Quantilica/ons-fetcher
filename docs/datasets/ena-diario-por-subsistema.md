---
dataset:
  id: ena-diario-por-subsistema
  fonte: ons
  titulo: "ENA Diário por Subsistema (ONS)"
  resumo: "Energia natural afluente (ENA) diária por subsistema, bruta e armazenável, em MWmed e percentual da média de longo termo (MLT)."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ena-diario-por-subsistema
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-subsistema"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a ENA de um subsistema em um dia"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste)", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema, ena_data], colunas: 7}
  unidades_de_medida:
    ena_bruta_regiao_mwmed: "MWmed"
    ena_bruta_regiao_percentualmlt: "% da MLT"
    ena_armazenavel_regiao_mwmed: "MWmed"
    ena_armazenavel_regiao_percentualmlt: "% da MLT"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# ENA Diário por Subsistema

## Resumo

Energia natural afluente (ENA) diária por subsistema, bruta e armazenável, em MWmed e percentual da média de longo termo (MLT). A energia natural afluente (ENA) bruta é a energia produzível pela usina, calculada pelo produto das vazões naturais pelas produtividades a 65% dos volumes úteis; a ENA armazenável desconta as vazões vertidas.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ena-diario-por-subsistema` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ena-diario-por-subsistema |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-subsistema |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a ENA de um subsistema em um dia |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste); temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema`, `ena_data` |
| Colunas | 7 |
| Unidades de medida | `ena_bruta_regiao_mwmed`: MWmed; `ena_bruta_regiao_percentualmlt`: % da MLT; `ena_armazenavel_regiao_mwmed`: MWmed; `ena_armazenavel_regiao_percentualmlt`: % da MLT |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ena-diario-por-subsistema`, https://dados.ons.org.br/dataset/ena-diario-por-subsistema). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ena_subsistema_di/`.
- O ONS publica um arquivo por ano com o prefixo `ENA_DIARIO_SUBSISTEMA` (`ENA_DIARIO_SUBSISTEMA_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `hidrologia/ena-diario-por-subsistema_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a ENA de um subsistema em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 1.464 linhas no primeiro e 1.272 no último; 39.260 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome da Subsistema | — | todo |
| `ena_data` | `ena_data` | texto | Dia observado da medida | — | todo |
| `ena_bruta_regiao_mwmed` | `ena_bruta_regiao_mwmed` | decimal | Valor de ENA bruta por Subsistema na unidade de medida MWmês | MWmed | todo |
| `ena_bruta_regiao_percentualmlt` | `ena_bruta_regiao_percentualmlt` | decimal | Valor de ENA bruta por Subsistema medido em percentual por média de longo termo-MLT (%) | % da MLT | todo |
| `ena_armazenavel_regiao_mwmed` | `ena_armazenavel_regiao_mwmed` | decimal | Valor de ENA armazenável por Subsistema na unidade de medida MWmês | MWmed | todo |
| `ena_armazenavel_regiao_percentualmlt` | `ena_armazenavel_regiao_percentualmlt` | decimal | Valor de ENA armazenável por subsistema em percentual por média de longo termo-MLT (%) | % da MLT | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ena-diario-por-subsistema`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`ENA_DIARIO_SUBSISTEMA_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- `ena_data` é texto (`AAAA-MM-DD`).
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `id_subsistema` (19.630 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

ENA bruta (percentual da MLT) por subsistema no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT id_subsistema, ena_data, ena_bruta_regiao_percentualmlt
    FROM read_parquet('lake/ons/ena-diario-por-subsistema/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ena_data = (SELECT max(ena_data) FROM read_parquet('lake/ons/ena-diario-por-subsistema/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 1
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-subsistema
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_subsistema_di/DicionarioDados_EnaPorSubsistema.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
