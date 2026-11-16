---
dataset:
  id: ear-diario-por-subsistema
  fonte: ons
  titulo: "EAR Diário por Subsistema (ONS)"
  resumo: "Energia armazenada (EAR) diária por subsistema, em MWmês e percentual da EAR máxima."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ear-diario-por-subsistema
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-subsistema"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a EAR de um subsistema em um dia"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste)", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema, ear_data], colunas: 6}
  unidades_de_medida:
    ear_max_subsistema: "MWmês"
    ear_verif_subsistema_mwmes: "MWmês"
    ear_verif_subsistema_percentual: "%"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# EAR Diário por Subsistema

## Resumo

Energia armazenada (EAR) diária por subsistema, em MWmês e percentual da EAR máxima. A energia armazenada (EAR) é a energia associada ao volume de água nos reservatórios que pode virar geração na própria usina e em todas as usinas à jusante na cascata; a EAR máxima é a capacidade de armazenamento com todos os reservatórios cheios.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ear-diario-por-subsistema` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ear-diario-por-subsistema |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-subsistema |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a EAR de um subsistema em um dia |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste); temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema`, `ear_data` |
| Colunas | 6 |
| Unidades de medida | `ear_max_subsistema`: MWmês; `ear_verif_subsistema_mwmes`: MWmês; `ear_verif_subsistema_percentual`: % |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ear-diario-por-subsistema`, https://dados.ons.org.br/dataset/ear-diario-por-subsistema). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ear_subsistema_di/`.
- O ONS publica um arquivo por ano com o prefixo `EAR_DIARIO_SUBSISTEMA` (`EAR_DIARIO_SUBSISTEMA_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 29 CSV, de 2000 a 2026.
- **Só há Parquet para parte dos anos**: o fetcher escolhe o melhor formato de cada período (Parquet, depois CSV, ZIP e XLSX); os anos sem Parquet vêm do CSV.
- No bruto, o arquivo fica em `hidrologia/ear-diario-por-subsistema_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a EAR de um subsistema em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 1.464 linhas no primeiro e 1.272 no último; 39.260 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome da Subsistema | — | todo |
| `ear_data` | `ear_data` | texto | Dia observado da medida | — | todo |
| `ear_max_subsistema` | `ear_max_subsistema` | decimal | Valor de EAR máxima por subsistema na unidade de medida MWmês | MWmês | todo |
| `ear_verif_subsistema_mwmes` | `ear_verif_subsistema_mwmes` | decimal | Valor de EAR verificada no dia por subsistema na unidade de medida MWmês | MWmês | todo |
| `ear_verif_subsistema_percentual` | `ear_verif_subsistema_percentual` | decimal | Valor de EAR verificada no dia por subsistema na unidade de medida % | % | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ear-diario-por-subsistema`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`EAR_DIARIO_SUBSISTEMA_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- `ear_data` é texto (`AAAA-MM-DD`).
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `id_subsistema` (19.630 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

EAR verificada (percentual) por subsistema no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT id_subsistema, ear_data, ear_verif_subsistema_percentual
    FROM read_parquet('lake/ons/ear-diario-por-subsistema/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ear_data = (SELECT max(ear_data) FROM read_parquet('lake/ons/ear-diario-por-subsistema/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 1
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-subsistema
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ear_subsistema_di/DicionarioDados_EarPorSubsistema.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
