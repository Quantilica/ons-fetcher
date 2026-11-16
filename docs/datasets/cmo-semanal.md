---
dataset:
  id: cmo-semanal
  fonte: ons
  titulo: "CMO Semanal (ONS)"
  resumo: "Custo Marginal de Operação (CMO) semanal por subsistema e patamar de carga, estimado pelo modelo Decomp: o custo de atender a mais uma unidade de carga no SIN."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/cmo-semanal
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/cmo-semanal"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2005, fim: em-curso}
  unidade: "o CMO de um subsistema em uma semana operativa"
  granularidade: {espacial: "subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste)", temporal: "semanal"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, id_subsistema, din_instante], colunas: 7}
  unidades_de_medida:
    val_cmomediasemanal: "R$/MWh"
    val_cmoleve: "R$/MWh"
    val_cmomedia: "R$/MWh"
    val_cmopesada: "R$/MWh"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# CMO Semanal

## Resumo

Custo Marginal de Operação (CMO) semanal por subsistema e patamar de carga, estimado pelo modelo Decomp: o custo de atender a mais uma unidade de carga no SIN.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/cmo-semanal` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/cmo-semanal |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/cmo-semanal |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2005 a em-curso |
| Unidade (uma linha) | o CMO de um subsistema em uma semana operativa |
| Granularidade | espacial: subsistema (Norte, Nordeste, Sul e Sudeste/Centro-Oeste); temporal: semanal |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `id_subsistema`, `din_instante` |
| Colunas | 7 |
| Unidades de medida | `val_cmomediasemanal`: R$/MWh; `val_cmoleve`: R$/MWh; `val_cmomedia`: R$/MWh; `val_cmopesada`: R$/MWh |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `cmo-semanal`, https://dados.ons.org.br/dataset/cmo-semanal). Os arquivos ficam no bucket público S3 do ONS, em `dataset/cmo_se/`.
- O ONS publica um arquivo por ano com o prefixo `CMO_SEMANAL` (`CMO_SEMANAL_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 22 arquivos Parquet e 22 CSV, de 2005 a 2026.
- No bruto, o arquivo fica em `precos/cmo-semanal_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: o CMO de um subsistema em uma semana operativa.
- 22 arquivos convertidos (todos os publicados), de 2005 a 2026: 208 linhas no primeiro e 188 no último; 4.568 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `din_instante` | `din_instante` | data e hora | Data de referência da Semana Operativa | — | todo |
| `val_cmomediasemanal` | `val_cmomediasemanal` | decimal | CMO Médio Semanal, em R$/MW | R$/MWh | todo |
| `val_cmoleve` | `val_cmoleve` | decimal | CMO no patamar de carga leve, em R$/MWh | R$/MWh | todo |
| `val_cmomedia` | `val_cmomedia` | decimal | CMO no patamar de carga média, em R$/MWh | R$/MWh | todo |
| `val_cmopesada` | `val_cmopesada` | decimal | CMO no patamar de carga pesada, em R$/MWh | R$/MWh | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/cmo-semanal`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`CMO_SEMANAL_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- A descrição oficial de `val_cmomediasemanal` diz 'R$/MW'; as demais colunas dizem 'R$/MWh'. O valor é um preço por unidade de energia: trate todas como R$/MWh.
- O ONS avisa que os dados passam por consistência recorrente e podem ser atualizados depois de publicados.

## Exemplos

CMO médio semanal por subsistema em 2026, por mês, em R$/MWh.

```python
import duckdb

duckdb.sql("""
    SELECT id_subsistema, date_trunc('month', din_instante) AS mes,
           round(avg(val_cmomediasemanal), 2) AS cmo_medio
    FROM read_parquet('lake/ons/cmo-semanal/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026
    GROUP BY 1, 2
    ORDER BY 1, 2
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/cmo-semanal
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/cmo_se/DicionarioDados_Cmo_Semanal.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
