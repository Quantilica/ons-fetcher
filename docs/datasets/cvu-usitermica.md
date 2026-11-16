---
dataset:
  id: cvu-usitermica
  fonte: ons
  titulo: "CVU das Usina Térmicas (ONS)"
  resumo: "Custo Variável Unitário (CVU) das usinas térmicas considerado no Programa Mensal da Operação (PMO), usado nos modelos NEWAVE, DECOMP e DESSEM e na programação da operação."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/cvu-usitermica
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/cvu-usitermica"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2005, fim: em-curso}
  unidade: "o CVU de uma usina térmica em uma semana operativa (revisão do PMO)"
  granularidade: {espacial: "usina térmica (com subsistema)", temporal: "semanal (por revisão do PMO)"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano"
  lake: {estado: convertido, particoes: [ano], chave: [ano, dat_iniciosemana, cod_usinaplanejamento, num_revisao], colunas: 11}
  unidades_de_medida:
    val_cvu: "R$/MWh"
    ano_referencia: "ano"
    mes_referencia: "mês (1 a 12)"
    num_revisao: "número da revisão do PMO"
    cod_usinaplanejamento: "código (sem unidade)"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# CVU das Usina Térmicas

## Resumo

Custo Variável Unitário (CVU) das usinas térmicas considerado no Programa Mensal da Operação (PMO), usado nos modelos NEWAVE, DECOMP e DESSEM e na programação da operação.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/cvu-usitermica` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/cvu-usitermica |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/cvu-usitermica |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2005 a em-curso |
| Unidade (uma linha) | o CVU de uma usina térmica em uma semana operativa (revisão do PMO) |
| Granularidade | espacial: usina térmica (com subsistema); temporal: semanal (por revisão do PMO) |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano |
| Estado no lake | convertido |
| Partições | `ano` |
| Chave | `ano`, `dat_iniciosemana`, `cod_usinaplanejamento`, `num_revisao` |
| Colunas | 11 |
| Unidades de medida | `val_cvu`: R$/MWh; `ano_referencia`: ano; `mes_referencia`: mês (1 a 12); `num_revisao`: número da revisão do PMO; `cod_usinaplanejamento`: código (sem unidade) |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `cvu-usitermica`, https://dados.ons.org.br/dataset/cvu-usitermica). Os arquivos ficam no bucket público S3 do ONS, em `dataset/cvu_usitermica_se/`.
- O ONS publica um arquivo por ano com o prefixo `CVU_USINA_TERMICA` (`CVU_USINA_TERMICA_AAAA.parquet`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 22 arquivos Parquet e 22 CSV, de 2005 a 2026.
- No bruto, o arquivo fica em `precos/cvu-usitermica_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: o CVU de uma usina térmica em uma semana operativa (revisão do PMO).
- 22 arquivos convertidos (todos os publicados), de 2005 a 2026: 3.085 linhas no primeiro e 4.776 no último; 107.395 linhas no total. O arquivo do ano corrente cresce a cada atualização.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `dat_iniciosemana` | `dat_iniciosemana` | data e hora | Data de Início da Semana Operativa | — | todo |
| `dat_fimsemana` | `dat_fimsemana` | data e hora | Data de Fim da Semana Operativa | — | todo |
| `ano_referencia` | `ano_referencia` | inteiro | Ano de Referência do PMO | ano | todo |
| `mes_referencia` | `mes_referencia` | inteiro | Mês de Referência do PMO | mês (1 a 12) | todo |
| `num_revisao` | `num_revisao` | inteiro | Número da Revisão PMO | número da revisão do PMO | todo |
| `nom_semanaoperativa` | `nom_semanaoperativa` | texto | Nome do Estudo da Semana Operativa | — | todo |
| `cod_usinaplanejamento` | `cod_usinaplanejamento` | inteiro | Código da usina nos modelos de planejamento e programação da operação | código (sem unidade) | todo |
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `nom_usina` | `nom_usina` | texto | Nome da Usina | — | todo |
| `val_cvu` | `val_cvu` | decimal | Valor do Custo Variável Unitário – CVU, em R$/MWh | R$/MWh | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |

## No lake

- Dataset `ons/cvu-usitermica`, particionado por `ano`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.
- A partição vem do nome do arquivo (`CVU_USINA_TERMICA_AAAA`); se o arquivo não tiver a coluna, o conversor a acrescenta.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- Em 2026 há 45 linhas repetidas mesmo com a revisão na chave; o ONS avisa que os dados passam por consistência recorrente e podem ser atualizados depois de publicados.
- Cada revisão do PMO republica o CVU da semana; para o valor vigente, use a maior `num_revisao` da semana.

## Exemplos

CVU mais alto por usina na última semana publicada, em R$/MWh.

```python
import duckdb

duckdb.sql("""
    SELECT nom_usina, id_subsistema, val_cvu
    FROM read_parquet('lake/ons/cvu-usitermica/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND dat_iniciosemana = (SELECT max(dat_iniciosemana) FROM read_parquet('lake/ons/cvu-usitermica/**/*.parquet', hive_partitioning = true, union_by_name = true) WHERE ano = 2026)
    QUALIFY num_revisao = max(num_revisao) OVER (PARTITION BY dat_iniciosemana)
    ORDER BY val_cvu DESC
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/cvu-usitermica
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/cvu_usitermica_se/DicionarioDados_CVU_UsinaTermica.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
