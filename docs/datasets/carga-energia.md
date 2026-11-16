---
dataset:
  id: carga-energia
  fonte: ons
  titulo: "Carga de Energia Diária (ONS)"
  resumo: "Carga de energia por subsistema em base diária, em MWmed: quanto o Sistema Interligado Nacional (SIN) consumiu por dia em cada subsistema."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/carga-energia
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/carga-energia"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a carga de um subsistema em um dia"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste)", temporal: "diária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema, din_instante], colunas: 4}
  unidades_de_medida:
    val_cargaenergiamwmed: "MWmed"
  dados_pessoais: nenhum
  eras:
    - {desde: 2022, mudanca: "`val_cargaenergiamwmed`: texto até 2021, decimal desde 2022"}
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Carga de Energia Diária

## Resumo

Carga de energia por subsistema em base diária, em MWmed: quanto o Sistema Interligado Nacional (SIN) consumiu por dia em cada subsistema.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/carga-energia` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/carga-energia |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/carga-energia |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a carga de um subsistema em um dia |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste); temporal: diária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema`, `din_instante` |
| Colunas | 4 |
| Unidades de medida | `val_cargaenergiamwmed`: MWmed |
| Dados pessoais | nenhum |
| Eras | 2022: `val_cargaenergiamwmed`: texto até 2021, decimal desde 2022 |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `carga-energia`, https://dados.ons.org.br/dataset/carga-energia). Os arquivos ficam no bucket público S3 do ONS, em `dataset/carga_energia_di/`.
- O ONS publica um arquivo por ano com o prefixo `CARGA_ENERGIA` (`CARGA_ENERGIA_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `carga/carga-energia_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a carga de um subsistema em um dia.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 1.464 linhas no primeiro e 1.268 no último; 39.257 linhas no total. O arquivo do ano corrente cresce a cada atualização.
- Mudanças de tipo entre arquivos (conferidas nos Parquet convertidos):
    - 2022: `val_cargaenergiamwmed`: texto até 2021, decimal desde 2022.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `din_instante` | `din_instante` | data e hora | Data de referência | — | todo |
| `val_cargaenergiamwmed` | `val_cargaenergiamwmed` | decimal (texto em parte dos arquivos) | Valor da Carga de Energia, em MWmed | MWmed | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/carga-energia`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`CARGA_ENERGIA_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **A definição de carga mudou três vezes.** Até 2021-02, a carga é a atendida por usinas despachadas ou programadas pelo ONS; de 2021-03 a 2023-04, soma a previsão de geração das usinas não despachadas; desde 2023-04-29, soma também a micro e minigeração distribuída (MMGD) estimada. Séries que atravessam essas datas não são comparáveis sem ajuste (descrição oficial do conjunto).
- **Colunas numéricas com tipo misto entre arquivos.** 1 coluna(s) (`val_cargaenergiamwmed`) chegam como texto em alguns anos e como decimal em outros (o texto traz oito casas decimais e o zero como `0E-8`); veja as mudanças acima. Ao ler vários anos juntos, converta com `CAST(... AS DOUBLE)`.

## Exemplos

Carga média diária do SIN (soma dos subsistemas) em 2026, por mês, em MWmed.

```python
import duckdb

duckdb.sql("""
    SELECT date_trunc('month', din_instante) AS mes, round(avg(dia), 0) AS carga_media_mwmed
    FROM (
      SELECT din_instante, sum(CAST(val_cargaenergiamwmed AS DOUBLE)) AS dia
      FROM read_parquet('lake/ons/carga-energia/**/*.parquet', hive_partitioning = true, union_by_name = true)
      WHERE ano = 2026
      GROUP BY 1
    )
    GROUP BY 1
    ORDER BY 1
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/carga-energia
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/carga_energia_di/DicionarioDados_Carga_Energia_Diaria.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
