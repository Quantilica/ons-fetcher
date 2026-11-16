---
dataset:
  id: ear-diario-por-reservatorio
  fonte: ons
  titulo: "EAR Diário por Reservatório (ONS)"
  resumo: "Energia armazenada (EAR) diária por reservatório, separada entre o próprio subsistema e o subsistema à jusante, com a contribuição de cada reservatório para a EAR da bacia, do subsistema e do SIN."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ear-diario-por-reservatorio
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-reservatorio"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a EAR de um reservatório em um dia"
  granularidade: {espacial: "reservatório", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, cod_resplanejamento, nom_reservatorio, ear_data], colunas: 25}
  unidades_de_medida:
    ear_reservatorio_subsistema_proprio_mwmes: "MWmês"
    ear_reservatorio_subsistema_jusante_mwmes: "MWmês"
    earmax_reservatorio_subsistema_proprio_mwmes: "MWmês"
    earmax_reservatorio_subsistema_jusante_mwmes: "MWmês"
    ear_reservatorio_percentual: "% da EAR máxima"
    ear_total_mwmes: "MWmês"
    ear_maxima_total_mwmes: "MWmês"
    cod_resplanejamento: "código (sem unidade)"
    val_contribearbacia: "% (contribuição)"
    val_contribearmaxbacia: "% (contribuição)"
    val_contribearsubsistema: "% (contribuição)"
    val_contribearmaxsubsistema: "% (contribuição)"
    val_contribearsubsistemajusante: "% (contribuição)"
    val_contribearmaxsubsistemajusante: "% (contribuição)"
    val_contribearsin: "% (contribuição)"
    val_contribearmaxsin: "% (contribuição)"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# EAR Diário por Reservatório

## Resumo

Energia armazenada (EAR) diária por reservatório, separada entre o próprio subsistema e o subsistema à jusante, com a contribuição de cada reservatório para a EAR da bacia, do subsistema e do SIN. A energia armazenada (EAR) é a energia associada ao volume de água nos reservatórios que pode virar geração na própria usina e em todas as usinas à jusante na cascata; a EAR máxima é a capacidade de armazenamento com todos os reservatórios cheios.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ear-diario-por-reservatorio` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ear-diario-por-reservatorio |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-reservatorio |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a EAR de um reservatório em um dia |
| Granularidade | espacial: reservatório; temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `cod_resplanejamento`, `nom_reservatorio`, `ear_data` |
| Colunas | 25 |
| Unidades de medida | `ear_reservatorio_subsistema_proprio_mwmes`: MWmês; `ear_reservatorio_subsistema_jusante_mwmes`: MWmês; `earmax_reservatorio_subsistema_proprio_mwmes`: MWmês; `earmax_reservatorio_subsistema_jusante_mwmes`: MWmês; `ear_reservatorio_percentual`: % da EAR máxima; `ear_total_mwmes`: MWmês; `ear_maxima_total_mwmes`: MWmês; `cod_resplanejamento`: código (sem unidade); `val_contribearbacia`: % (contribuição); `val_contribearmaxbacia`: % (contribuição); `val_contribearsubsistema`: % (contribuição); `val_contribearmaxsubsistema`: % (contribuição); `val_contribearsubsistemajusante`: % (contribuição); `val_contribearmaxsubsistemajusante`: % (contribuição); `val_contribearsin`: % (contribuição); `val_contribearmaxsin`: % (contribuição) |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ear-diario-por-reservatorio`, https://dados.ons.org.br/dataset/ear-diario-por-reservatorio). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ear_reservatorio_di/`.
- O ONS publica um arquivo por ano com o prefixo `EAR_DIARIO_RESERVATORIOS` (`EAR_DIARIO_RESERVATORIOS_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `hidrologia/ear-diario-por-reservatorio_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a EAR de um reservatório em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 25.978 linhas no primeiro e 24.092 no último; 709.754 linhas no total. O arquivo do ano corrente cresce a cada atualização.

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
| `id_subsistema_jusante` | `id_subsistema_jusante` | texto | Código do Subsistema Jusante | — | todo |
| `nom_subsistema_jusante` | `nom_subsistema_jusante` | texto | Nome do Subsistema Jusante | — | todo |
| `ear_data` | `ear_data` | texto | Dia Observado da Medida | — | todo |
| `ear_reservatorio_subsistema_proprio_mwmes` | `ear_reservatorio_subsistema_proprio_mwmes` | decimal | Valor de EAR para o próprio subsistema, em MWmês | MWmês | todo |
| `ear_reservatorio_subsistema_jusante_mwmes` | `ear_reservatorio_subsistema_jusante_mwmes` | decimal | Valor de EAR para o subsistema à jusante, em MWmês | MWmês | todo |
| `earmax_reservatorio_subsistema_proprio_mwmes` | `earmax_reservatorio_subsistema_proprio_mwmes` | decimal | Valor de EAR máxima para o próprio subsistema, em MWmês | MWmês | todo |
| `earmax_reservatorio_subsistema_jusante_mwmes` | `earmax_reservatorio_subsistema_jusante_mwmes` | decimal | Valor de EAR máxima para o subsistema à jusante, em MWmês | MWmês | todo |
| `ear_reservatorio_percentual` | `ear_reservatorio_percentual` | decimal | Valor de EAR, em % da EAR máxima | % da EAR máxima | todo |
| `ear_total_mwmes` | `ear_total_mwmes` | decimal | EAR total no reservatório (no próprio subsistema + no subsistema jusante) em MWmês | MWmês | todo |
| `ear_maxima_total_mwmes` | `ear_maxima_total_mwmes` | decimal | EAR máxima total no reservatório (no próprio subsistema + no subsistema jusante) em MWmês | MWmês | todo |
| `val_contribearbacia` | `val_contribearbacia` | decimal | Contribuição do reservatório para a EAR da Bacia, em % | % (contribuição) | todo |
| `val_contribearmaxbacia` | `val_contribearmaxbacia` | decimal | Contribuição do reservatório para a EAR máxima da Bacia, em % | % (contribuição) | todo |
| `val_contribearsubsistema` | `val_contribearsubsistema` | decimal | Contribuição do reservatório para a EAR do próprio subsistema, em % | % (contribuição) | todo |
| `val_contribearmaxsubsistema` | `val_contribearmaxsubsistema` | decimal | Contribuição do reservatório para a EAR máxima do próprio subsistema, em % | % (contribuição) | todo |
| `val_contribearsubsistemajusante` | `val_contribearsubsistemajusante` | decimal | Contribuição do reservatório para a EAR do subsistema jusante, em % | % (contribuição) | todo |
| `val_contribearmaxsubsistemajusante` | `val_contribearmaxsubsistemajusante` | decimal | Contribuição do reservatório para a EAR máxima do subsistema jusante, em % | % (contribuição) | todo |
| `val_contribearsin` | `val_contribearsin` | decimal | Contribuição do reservatório para a EAR do SIN, em % | % (contribuição) | todo |
| `val_contribearmaxsin` | `val_contribearmaxsin` | decimal | Contribuição do reservatório para a EAR máxima do SIN, em % | % (contribuição) | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ear-diario-por-reservatorio`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`EAR_DIARIO_RESERVATORIOS_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- `cod_resplanejamento` sozinho não identifica o reservatório: o mesmo código aparece com nomes diferentes em 2024, 2025 e 2026 (730 repetições em 2025 em `cod_resplanejamento` e `ear_data`); use o nome junto.
- `ear_data` é texto (`AAAA-MM-DD`).

## Exemplos

Reservatórios com maior EAR percentual no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT nom_reservatorio, nom_ree, ear_reservatorio_percentual
    FROM read_parquet('lake/ons/ear-diario-por-reservatorio/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ear_data = (SELECT max(ear_data) FROM read_parquet('lake/ons/ear-diario-por-reservatorio/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 3 DESC
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-reservatorio
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ear_reservatorio_di/DicionarioDados_EarPorReservatorio.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
