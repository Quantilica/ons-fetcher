---
dataset:
  id: curva-carga
  fonte: ons
  titulo: "Curva de Carga Horária (ONS)"
  resumo: "Curva de carga horária: o perfil de consumo de energia elétrica por subsistema, hora a hora, em MWmed."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/curva-carga
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/curva-carga"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a carga de um subsistema em uma hora"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste)", temporal: "horária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema, din_instante], colunas: 4}
  unidades_de_medida:
    val_cargaenergiahomwmed: "MWmed"
  dados_pessoais: nenhum
  eras:
    - {desde: 2025, mudanca: "`val_cargaenergiahomwmed`: texto até 2024, decimal desde 2025"}
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Curva de Carga Horária

## Resumo

Curva de carga horária: o perfil de consumo de energia elétrica por subsistema, hora a hora, em MWmed.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/curva-carga` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/curva-carga |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/curva-carga |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a carga de um subsistema em uma hora |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste); temporal: horária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema`, `din_instante` |
| Colunas | 4 |
| Unidades de medida | `val_cargaenergiahomwmed`: MWmed |
| Dados pessoais | nenhum |
| Eras | 2025: `val_cargaenergiahomwmed`: texto até 2024, decimal desde 2025 |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `curva-carga`, https://dados.ons.org.br/dataset/curva-carga). Os arquivos ficam no bucket público S3 do ONS, em `dataset/curva-carga-ho/`.
- O ONS publica um arquivo por ano com o prefixo `CURVA_CARGA` (`CURVA_CARGA_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 27 arquivos Parquet e 27 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `carga/curva-carga_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: a carga de um subsistema em uma hora.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 35.132 linhas no primeiro e 30.432 no último; 942.040 linhas no total. O arquivo do ano corrente cresce a cada atualização.
- Mudanças de tipo entre arquivos (conferidas nos Parquet convertidos):
    - 2025: `val_cargaenergiahomwmed`: texto até 2024, decimal desde 2025.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `din_instante` | `din_instante` | data e hora | Data de referência | — | todo |
| `val_cargaenergiahomwmed` | `val_cargaenergiahomwmed` | decimal (texto em parte dos arquivos) | Valor da Carga de Energia, em MWmed | MWmed | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/curva-carga`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`CURVA_CARGA_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- O ONS avisa que os dados passam por consistência recorrente e podem ser atualizados depois de publicados; o fetcher baixa de novo o arquivo do ano corrente e o lake o reconverte quando o conteúdo muda.
- **Colunas numéricas com tipo misto entre arquivos.** 1 coluna(s) (`val_cargaenergiahomwmed`) chegam como texto em alguns anos e como decimal em outros (o texto traz oito casas decimais e o zero como `0E-8`); veja as mudanças acima. Ao ler vários anos juntos, converta com `CAST(... AS DOUBLE)`.

## Exemplos

Carga horária média do SIN por hora do dia em 2026, em MWmed.

```python
import duckdb

duckdb.sql("""
    SELECT hour(din_instante) AS hora, round(avg(soma), 0) AS carga_mwmed
    FROM (
      SELECT din_instante, sum(CAST(val_cargaenergiahomwmed AS DOUBLE)) AS soma
      FROM read_parquet('lake/ons/curva-carga/**/*.parquet', hive_partitioning = true, union_by_name = true)
      WHERE ano = 2026
      GROUP BY 1
    )
    GROUP BY 1
    ORDER BY 1
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/curva-carga
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/curva-carga-ho/DicionarioDados_CurvaCarga.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
