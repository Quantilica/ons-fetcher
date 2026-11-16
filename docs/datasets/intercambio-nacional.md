---
dataset:
  id: intercambio-nacional
  fonte: ons
  titulo: "Intercâmbios Entre Subsistemas (ONS)"
  resumo: "Intercâmbio de energia entre subsistemas em base horária, em MWmed: a soma do fluxo de potência ativa nas linhas de transmissão de fronteira entre dois subsistemas."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/intercambio-nacional
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/intercambio-nacional"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2000, fim: em-curso}
  unidade: "o intercâmbio de um par de subsistemas (origem e destino) em uma hora"
  granularidade: {espacial: "par de subsistemas", temporal: "horária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema_origem, id_subsistema_destino, din_instante], colunas: 7}
  unidades_de_medida:
    val_intercambiomwmed: "MWmed"
    val_intercambioprogmwmed: "MWmed"
  dados_pessoais: nenhum
  eras:
    - {desde: 2023, mudanca: "`din_instante`: texto até 2022, data e hora desde 2023"}
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Intercâmbios Entre Subsistemas

## Resumo

Intercâmbio de energia entre subsistemas em base horária, em MWmed: a soma do fluxo de potência ativa nas linhas de transmissão de fronteira entre dois subsistemas.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/intercambio-nacional` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/intercambio-nacional |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/intercambio-nacional |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2000 a em-curso |
| Unidade (uma linha) | o intercâmbio de um par de subsistemas (origem e destino) em uma hora |
| Granularidade | espacial: par de subsistemas; temporal: horária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema_origem`, `id_subsistema_destino`, `din_instante` |
| Colunas | 7 |
| Unidades de medida | `val_intercambiomwmed`: MWmed; `val_intercambioprogmwmed`: MWmed |
| Dados pessoais | nenhum |
| Eras | 2023: `din_instante`: texto até 2022, data e hora desde 2023 |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `intercambio-nacional`, https://dados.ons.org.br/dataset/intercambio-nacional). Os arquivos ficam no bucket público S3 do ONS, em `dataset/intercambio_nacional_ho/`.
- O ONS publica um arquivo por ano com o prefixo `INTERCAMBIO_NACIONAL` (`INTERCAMBIO_NACIONAL_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 4 arquivos Parquet e 27 CSV, de 2000 a 2026.
- **Só há Parquet para parte dos anos**: o fetcher escolhe o melhor formato de cada período (Parquet, depois CSV, ZIP e XLSX); os anos sem Parquet vêm do CSV.
- No bruto, o arquivo fica em `intercambio/intercambio-nacional_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: o intercâmbio de um par de subsistemas (origem e destino) em uma hora.
- 27 arquivos convertidos (todos os publicados), de 2000 a 2026: 26.349 linhas no primeiro e 30.528 no último; 914.759 linhas no total. O arquivo do ano corrente cresce a cada atualização.
- Mudanças de tipo entre arquivos (conferidas nos Parquet convertidos):
    - 2023: `din_instante`: texto até 2022, data e hora desde 2023.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `din_instante` | `din_instante` | data e hora / texto | Data/hora (início do período de agregação) | — | todo |
| `id_subsistema_origem` | `id_subsistema_origem` | texto | Código do Subsistema de Origem | — | todo |
| `nom_subsistema_origem` | `nom_subsistema_origem` | texto | Nome do Subsistema de Origem | — | todo |
| `id_subsistema_destino` | `id_subsistema_destino` | texto | Código do Subsistema de Destino | — | todo |
| `nom_subsistema_destino` | `nom_subsistema_destino` | texto | Nome do Subsistema de Destino | — | todo |
| `val_intercambiomwmed` | `val_intercambiomwmed` | decimal | Intercâmbio verificado em base horária, representando a soma das medidas de fluxo de potência ativa nas linhas de transmissão de fronteira entre os subsistemas em MWmed | MWmed | todo |
| `val_intercambioprogmwmed` | `val_intercambioprogmwmed` | decimal | Intercâmbio programado em base horária em MWmed | MWmed | 2026 a 2026 |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/intercambio-nacional`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`INTERCAMBIO_NACIONAL_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **Formatos mistos.** De 2000 a 2022 o ONS só publica CSV, com ponto decimal; nesses anos `din_instante` fica como texto (o conversor não converte datas). Desde 2023 há Parquet, com data e hora. Converta `din_instante` com `CAST` nos arquivos antigos; os valores numéricos são `double` em todos os anos.
- O valor é negativo quando o fluxo vai no sentido contrário ao par origem e destino da linha (nas amostras conferidas há pares com sinal negativo).
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `nom_subsistema_origem` (30.528 linhas); `nom_subsistema_destino` (30.528 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Intercâmbio líquido médio entre pares de subsistemas em 2026, em MWmed.

```python
import duckdb

duckdb.sql("""
    SELECT id_subsistema_origem, id_subsistema_destino, round(avg(val_intercambiomwmed), 0) AS mwmed
    FROM read_parquet('lake/ons/intercambio-nacional/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026
    GROUP BY 1, 2
    ORDER BY 1, 2
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/intercambio-nacional
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/intercambio_nacional_ho/DicionarioDados_Intercambio_Nacional.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
