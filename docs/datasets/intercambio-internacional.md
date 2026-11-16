---
dataset:
  id: intercambio-internacional
  fonte: ons
  titulo: "Intercâmbio do SIN com Outros Países (ONS)"
  resumo: "Intercâmbio do SIN com outros países em base horária, em MWmed: a soma do fluxo de potência ativa nas conversoras de frequência de fronteira (Argentina, Uruguai e Paraguai)."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/intercambio-internacional
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/intercambio-internacional"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "o intercâmbio com um país em uma hora"
  granularidade: {espacial: "país de destino", temporal: "horária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, nom_paisdestino, din_instante], colunas: 4}
  unidades_de_medida:
    val_intercambiomwmed: "MWmed"
    val_intercambioprogmwmed: "MWmed"
  dados_pessoais: nenhum
  eras:
    - {desde: 2023, mudanca: "`din_instante`: texto até 2022, data e hora desde 2023"}
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Intercâmbio do SIN com Outros Países

## Resumo

Intercâmbio do SIN com outros países em base horária, em MWmed: a soma do fluxo de potência ativa nas conversoras de frequência de fronteira (Argentina, Uruguai e Paraguai).

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/intercambio-internacional` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/intercambio-internacional |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/intercambio-internacional |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | o intercâmbio com um país em uma hora |
| Granularidade | espacial: país de destino; temporal: horária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `nom_paisdestino`, `din_instante` |
| Colunas | 4 |
| Unidades de medida | `val_intercambiomwmed`: MWmed; `val_intercambioprogmwmed`: MWmed |
| Dados pessoais | nenhum |
| Eras | 2023: `din_instante`: texto até 2022, data e hora desde 2023 |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `intercambio-internacional`, https://dados.ons.org.br/dataset/intercambio-internacional). Os arquivos ficam no bucket público S3 do ONS, em `dataset/intercambio_internacional_ho/`.
- O ONS publica um arquivo por ano com o prefixo `INTERCAMBIO_INTERNACIONAL` (`INTERCAMBIO_INTERNACIONAL_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 4 arquivos Parquet e 27 CSV, de 2000 a 2026.
- **Só há Parquet para parte dos anos**: o fetcher escolhe o melhor formato de cada período (Parquet, depois CSV, ZIP e XLSX); os anos sem Parquet vêm do CSV.
- No bruto, o arquivo fica em `intercambio/intercambio-internacional_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: o intercâmbio com um país em uma hora.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 17.566 linhas no primeiro e 15.168 no último; 659.057 linhas no total. O arquivo do ano corrente cresce a cada atualização.
- Mudanças de tipo entre arquivos (conferidas nos Parquet convertidos):
    - 2023: `din_instante`: texto até 2022, data e hora desde 2023.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `din_instante` | `din_instante` | data e hora / texto | Data/hora (início do período de agregação) | — | todo |
| `nom_paisdestino` | `nom_paisdestino` | texto | Nome do país de destino da energia | — | todo |
| `val_intercambiomwmed` | `val_intercambiomwmed` | decimal | Intercâmbio verificado em base horária, representando a soma das medidas de fluxo de potência ativa nas conversoras de frequência de fronteira entre os dois países medido, em MWmed. Dados positivos indicam exportação de energia do Brasil para outros países | MWmed | todo |
| `val_intercambioprogmwmed` | `val_intercambioprogmwmed` | decimal | Intercâmbio programado em base horária em MWmed | MWmed | 2026 a 2026 |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/intercambio-internacional`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`INTERCAMBIO_INTERNACIONAL_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **Formatos mistos.** De 2000 a 2022 o ONS só publica CSV, com ponto decimal; nesses anos `din_instante` fica como texto (o conversor não converte datas). Desde 2023 há Parquet, com data e hora. Os valores numéricos são `double` em todos os anos.
- O nome do país vem preenchido com espaços à direita (30 caracteres): use `trim`.
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `nom_paisdestino` (15.168 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Intercâmbio médio com cada país em 2026, em MWmed.

```python
import duckdb

duckdb.sql("""
    SELECT trim(nom_paisdestino) AS pais, round(avg(val_intercambiomwmed), 0) AS mwmed
    FROM read_parquet('lake/ons/intercambio-internacional/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026
    GROUP BY 1
    ORDER BY 1
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/intercambio-internacional
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/intercambio_internacional_ho/DicionarioDados_Intercambio_Internacional.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
