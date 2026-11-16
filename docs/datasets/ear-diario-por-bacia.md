---
dataset:
  id: ear-diario-por-bacia
  fonte: ons
  titulo: "EAR Diário por Bacia (ONS)"
  resumo: "Energia armazenada (EAR) diária por bacia hidro-energética, em MWmês e em percentual da EAR máxima."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/ear-diario-por-bacia
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-bacia"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a EAR de uma bacia em um dia"
  granularidade: {espacial: "bacia hidro-energética", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, nomecurto, ear_data], colunas: 5}
  unidades_de_medida:
    ear_max_bacia: "MWmês"
    ear_verif_bacia_mwmes: "MWmês"
    ear_verif_bacia_percentual: "%"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# EAR Diário por Bacia

## Resumo

Energia armazenada (EAR) diária por bacia hidro-energética, em MWmês e em percentual da EAR máxima. A energia armazenada (EAR) é a energia associada ao volume de água nos reservatórios que pode virar geração na própria usina e em todas as usinas à jusante na cascata; a EAR máxima é a capacidade de armazenamento com todos os reservatórios cheios.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/ear-diario-por-bacia` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/ear-diario-por-bacia |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-bacia |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a EAR de uma bacia em um dia |
| Granularidade | espacial: bacia hidro-energética; temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `nomecurto`, `ear_data` |
| Colunas | 5 |
| Unidades de medida | `ear_max_bacia`: MWmês; `ear_verif_bacia_mwmes`: MWmês; `ear_verif_bacia_percentual`: % |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `ear-diario-por-bacia`, https://dados.ons.org.br/dataset/ear-diario-por-bacia). Os arquivos ficam no bucket público S3 do ONS, em `dataset/ear_bacia_di/`.
- O ONS publica um arquivo por ano com o prefixo `EAR_DIARIO_BACIAS` (`EAR_DIARIO_BACIAS_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `hidrologia/ear-diario-por-bacia_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a EAR de uma bacia em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 8.475 linhas no primeiro e 11.112 no último; 222.242 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `nomecurto` | `nom_curto` | texto | Nome Curto da Bacia Hidro Energética | — | todo |
| `ear_data` | `ear_data` | texto | Dia observado da medida | — | todo |
| `ear_max_bacia` | `ear_max_bacia` | decimal | Valor de EAR Máxima por Bacia, em MWmês | MWmês | todo |
| `ear_verif_bacia_mwmes` | `ear_verif_bacia_mwmes` | decimal | Valor de EAR Verificada no Dia por Bacia, em MWmês | MWmês | todo |
| `ear_verif_bacia_percentual` | `ear_verif_bacia_percentual` | decimal | Valor de EAR Verificada no Dia por Bacia, em % | % | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/ear-diario-por-bacia`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`EAR_DIARIO_BACIAS_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- O nome da coluna da bacia no lake é `nomecurto` (o dicionário oficial escreve `nom_curto`).
- `ear_data` é texto (`AAAA-MM-DD`), não data.

## Exemplos

EAR verificada (percentual) por bacia no último dia publicado.

```python
import duckdb

duckdb.sql("""
    SELECT nomecurto, ear_data, ear_verif_bacia_percentual
    FROM read_parquet('lake/ons/ear-diario-por-bacia/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND ear_data = (SELECT max(ear_data) FROM read_parquet('lake/ons/ear-diario-por-bacia/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    ORDER BY 3 DESC
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/ear-diario-por-bacia
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ear_bacia_di/DicionarioDados_EarPorBacia.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
