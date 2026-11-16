---
dataset:
  id: geracao-usina-2
  fonte: ons
  titulo: "Geração por Usina em Base Horária (ONS)"
  resumo: "Geração verificada de usinas, conjuntos de usinas e grupos de pequenas usinas em base horária, em MWmed."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/geracao-usina-2
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/geracao-usina-2"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "a geração de uma usina, conjunto ou grupo de usinas em uma hora"
  granularidade: {espacial: "usina ou conjunto de usinas (com subsistema e estado)", temporal: "horária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano e, desde 2022, um por mês"
  lake: {estado: convertido, particoes: [ano, mes], chave: [ano, mes, nom_usina, id_ons, din_instante], colunas: 13}
  unidades_de_medida:
    val_geracao: "MWmed"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Geração por Usina em Base Horária

## Resumo

Geração verificada de usinas, conjuntos de usinas e grupos de pequenas usinas em base horária, em MWmed.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/geracao-usina-2` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/geracao-usina-2 |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/geracao-usina-2 |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | a geração de uma usina, conjunto ou grupo de usinas em uma hora |
| Granularidade | espacial: usina ou conjunto de usinas (com subsistema e estado); temporal: horária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano e, desde 2022, um por mês |
| Estado no lake | convertido |
| Partições | `ano`, `mes` |
| Chave | `ano`, `mes`, `nom_usina`, `id_ons`, `din_instante` |
| Colunas | 13 |
| Unidades de medida | `val_geracao`: MWmed |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `geracao-usina-2`, https://dados.ons.org.br/dataset/geracao-usina-2). Os arquivos ficam no bucket público S3 do ONS, em `dataset/geracao_usina_2_ho/`.
- O ONS publica um arquivo por ano (2000 a 2021) e por mês (desde 2022) com o prefixo `GERACAO_USINA-2` (`GERACAO_USINA-2_AAAA.parquet`; mensais `..._AAAA_MM`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 81 arquivos Parquet e 81 CSV, de 2000 a 2026.
- No bruto, o arquivo fica em `geracao/geracao-usina-2_AAAA[_MM]@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.
- **Conferência por amostra.** Os arquivos deste conjunto são grandes; esta página foi conferida em 6 arquivos (de 81 Parquet publicados), escolhidos para cobrir os extremos e as quebras de formato.

## Conteúdo

- Unidade de análise: a geração de uma usina, conjunto ou grupo de usinas em uma hora.
- 6 arquivos convertidos (amostra), de 2000 a 2026-10: 993.556 linhas no primeiro e 537.384 no último; 9.422.737 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `din_instante` | `din_instante` | data e hora | Data de referência | — | todo |
| `id_subsistema` | `id_subsistema` | texto | Subsistema da Usina | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `id_estado` | `id_estado` | texto | Estado onde está localizado a Usina | — | todo |
| `nom_estado` | `nom_estado` | texto | Nome do Estado | — | todo |
| `cod_modalidadeoperacao` | `cod_modalidadeoperacao` | texto | Modalidade de Operação da Usina | — | todo |
| `nom_tipousina` | `nom_tipousina` | texto | Tipo da Usina | — | todo |
| `nom_tipocombustivel` | `nom_tipocombustivel` | texto | Tipo de Combustível | — | todo |
| `nom_usina` | `nom_usina` | texto | Nome da Usina | — | todo |
| `id_ons` | `id_ons` | texto | Identificador ONS | — | todo |
| `ceg` | `ceg` | texto | Código Único do Empreendimento de Geração (CEG), estabelecido pela ANEEL | — | todo |
| `val_geracao` | `val_geracao` | decimal | Geração de Energia na unidade de medida MWmed | MWmed | todo |
| `periodicidade` | — (gerada) | texto | Periodicidade do arquivo de origem: `anual` ou `mensal` | `anual`, `mensal` | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |
| `mes` | — (partição) | inteiro | Mês do arquivo de origem; 0 nos arquivos anuais | — | todo |

## No lake

- Dataset `ons/geracao-usina-2`, particionado por `ano`, `mes`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`GERACAO_USINA-2_AAAA`; `_AAAA_MM` nos mensais, com `mes = 0` nos anuais); se o arquivo não tiver a coluna, o conversor a acrescenta.
- A coluna `periodicidade` (`anual` ou `mensal`) é acrescentada pelo conversor.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **Granularidade mista:** de 2000 a 2021 o ONS publica um arquivo por ano; desde 2022, um por mês. O lake guarda as duas em `ano` e `mes`, com `mes = 0` para os arquivos anuais, e a coluna `periodicidade` (`anual` ou `mensal`).
- Os conjuntos de usinas (Tipo II-C) vêm de ajustamentos operativos; os grupos de pequenas usinas (Tipo III) não têm relacionamento com o ONS e os valores são previsões de geração. Essas linhas não têm `id_ons`: em 2026-10 são 87.048 linhas de 537.384 sem `id_ons`; use `nom_usina` junto na chave.
- Volume: um mês de 2026 tem mais de 500 mil linhas; filtre por `ano` e `mes` antes de agregar.

## Exemplos

Geração média por tipo de usina em 2026-10, em MWmed.

```python
import duckdb

duckdb.sql("""
    SELECT nom_tipousina, round(sum(val_geracao) / count(DISTINCT din_instante), 0) AS geracao_media_mwmed
    FROM read_parquet('lake/ons/geracao-usina-2/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND mes = 10
    GROUP BY 1
    ORDER BY 2 DESC
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/geracao-usina-2
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/geracao_usina_2_ho/DicionarioDados_GeracaoPorUsina.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
