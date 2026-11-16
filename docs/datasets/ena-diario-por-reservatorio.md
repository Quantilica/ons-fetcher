---
dataset:
  id: ena-diario-por-reservatorio
  fonte: ons
  titulo: "ENA Diário por Reservatório (ONS)"
  resumo: "Energia natural afluente (ENA) diária por reservatório, bruta, armazenável e por queda, com a média de longo termo (MLT)."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ena-diario-por-reservatorio
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-reservatorio"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a ENA de um reservatório em um dia"
  granularidade: {espacial: "reservatório", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, cod_resplanejamento, nom_reservatorio, ena_data], colunas: 14}
  unidades_de_medida:
    ena_bruta_res_mwmed: "MWmed"
    ena_bruta_res_percentualmlt: "% da MLT"
    ena_armazenavel_res_mwmed: "MWmed"
    ena_armazenavel_res_percentualmlt: "% da MLT"
    ena_queda_bruta: "MWmed"
    mlt_ena: "MWmed"
    cod_resplanejamento: "código (sem unidade)"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# ENA Diário por Reservatório

## Resumo

Energia natural afluente (ENA) diária por reservatório, bruta, armazenável e por queda, com a média de longo termo (MLT). A energia natural afluente (ENA) bruta é a energia produzível pela usina, calculada pelo produto das vazões naturais pelas produtividades a 65% dos volumes úteis; a ENA armazenável desconta as vazões vertidas.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ena-diario-por-reservatorio` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ena-diario-por-reservatorio |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-reservatorio |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a ENA de um reservatório em um dia |
| Granularidade | espacial: reservatório; temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `cod_resplanejamento`, `nom_reservatorio`, `ena_data` |
| Colunas | 14 |
| Unidades de medida | `ena_bruta_res_mwmed`: MWmed; `ena_bruta_res_percentualmlt`: % da MLT; `ena_armazenavel_res_mwmed`: MWmed; `ena_armazenavel_res_percentualmlt`: % da MLT; `ena_queda_bruta`: MWmed; `mlt_ena`: MWmed; `cod_resplanejamento`: código (sem unidade) |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ena-diario-por-reservatorio`, https://dados.ons.org.br/dataset/ena-diario-por-reservatorio). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ena_reservatorio_di/`.
- O ONS publica um arquivo por ano com o prefixo `ENA_DIARIO_RESERVATORIOS` (`ENA_DIARIO_RESERVATORIOS_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `hidrologia/ena-diario-por-reservatorio_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a ENA de um reservatório em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 55.980 linhas no primeiro e 49.135 no último; 1.511.617 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `nom_reservatorio` | `nom_reservatorio` | texto | Nome do Reservatório | — | todo |
| `cod_resplanejamento` | `cod_resplanejamento` | inteiro | Código do Reservatório nos modelos de planejamento | código (sem unidade) | todo |
| `tip_reservatorio` | `tip_reservatorio` | texto | Tipo de Reservatório | — | todo |
| `nom_bacia` | `nom_bacia` | texto | Nome da Bacia | — | todo |
| `nom_ree` | `nom_ree` | texto | Nome do Reservatório Equivalente de Energia (REE) | — | todo |
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `ena_data` | `ena_data` | texto | Dia observado da medida | — | todo |
| `ena_bruta_res_mwmed` | `ena_bruta_res_mwmed` | decimal | Valor de ENA bruta em MWmed | MWmed | todo |
| `ena_bruta_res_percentualmlt` | `ena_bruta_res_percentualmlt` | decimal | Valor de ENA bruta, em % da média de longo termo (MLT) | % da MLT | todo |
| `ena_armazenavel_res_mwmed` | `ena_armazenavel_res_mwmed` | decimal | Valor de ENA armazenável em MWmed | MWmed | todo |
| `ena_armazenavel_res_percentualmlt` | `ena_armazenavel_res_percentualmlt` | decimal | Valor de ENA armazenável, em % da média de longo termo (MLT) | % da MLT | todo |
| `ena_queda_bruta` | `ena_queda_bruta` | decimal | Valor de ENA por queda, em MWmed | MWmed | todo |
| `mlt_ena` | `mlt_ena` | decimal | Valor média de longo termo (MLT) de ENA, em MWmed | MWmed | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ena-diario-por-reservatorio`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`ENA_DIARIO_RESERVATORIOS_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- `cod_resplanejamento` sozinho não identifica o reservatório (o mesmo código aparece com nomes diferentes); use o nome junto. Em 2025 há uma repetição mesmo com o nome.
- `ena_data` é texto (`AAAA-MM-DD`).

## Exemplos

Reservatórios com maior ENA bruta no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT nom_reservatorio, nom_ree, ena_bruta_res_mwmed
    FROM read_parquet('lake/ons/ena-diario-por-reservatorio/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ena_data = (SELECT max(ena_data) FROM read_parquet('lake/ons/ena-diario-por-reservatorio/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 3 DESC
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ena-diario-por-reservatorio
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_reservatorio_di/DicionarioDados_EnaPorReservatorio.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
