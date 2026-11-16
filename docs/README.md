# Operador Nacional do Sistema Elétrico — ONS (`ons`)

O `ons-fetcher` coleta os dados abertos do Operador Nacional do Sistema Elétrico (ONS), o órgão que coordena e controla a operação das usinas e das linhas de transmissão do Sistema Interligado Nacional (SIN), e os converte para o lake em Parquet particionado por ano (e mês, nos conjuntos horários mais recentes). Os dados cobrem carga, hidrologia (energia armazenada e afluente, vazões), geração, preços (CMO e CVU), intercâmbios e cadastros de usinas e reservatórios.

O fetcher declara **23 datasets**, os conjuntos que baixa hoje (o catálogo do fetcher lista outros conjuntos do ONS, ainda sem download).

## Carga

| Dataset | O que é | Granularidade | Cobertura | Página |
|---|---|---|---|---|
| `carga-energia` | Carga de Energia Diária | diária | 2000 a 2026 | [carga-energia](datasets/carga-energia.md) |
| `carga-mensal` | Carga de Energia Mensal | mensal | 2000 a 2026 | [carga-mensal](datasets/carga-mensal.md) |
| `curva-carga` | Curva de Carga Horária | horária | 2000 a 2026 | [curva-carga](datasets/curva-carga.md) |

## Hidrologia (EAR, ENA e dados hidráulicos)

| Dataset | O que é | Granularidade | Cobertura | Página |
|---|---|---|---|---|
| `ear-diario-por-bacia` | EAR Diário por Bacia | diária | 2000 a 2026 | [ear-diario-por-bacia](datasets/ear-diario-por-bacia.md) |
| `ear-diario-por-ree` | EAR Diário por REE - Reservatório Equivalente de Energia | diária | 2016 a 2026 | [ear-diario-por-ree](datasets/ear-diario-por-ree.md) |
| `ear-diario-por-reservatorio` | EAR Diário por Reservatório | diária | 2000 a 2026 | [ear-diario-por-reservatorio](datasets/ear-diario-por-reservatorio.md) |
| `ear-diario-por-subsistema` | EAR Diário por Subsistema | diária | 2000 a 2026 | [ear-diario-por-subsistema](datasets/ear-diario-por-subsistema.md) |
| `ena-diario-por-bacia` | ENA Diário por Bacia | diária | 2000 a 2026 | [ena-diario-por-bacia](datasets/ena-diario-por-bacia.md) |
| `ena-diario-por-ree` | ENA Diário por REE - Reservatório Equivalente de Energia | diária | 2016 a 2026 | [ena-diario-por-ree](datasets/ena-diario-por-ree.md) |
| `ena-diario-por-reservatorio` | ENA Diário por Reservatório | diária | 2000 a 2026 | [ena-diario-por-reservatorio](datasets/ena-diario-por-reservatorio.md) |
| `ena-diario-por-subsistema` | ENA Diário por Subsistema | diária | 2000 a 2026 | [ena-diario-por-subsistema](datasets/ena-diario-por-subsistema.md) |
| `dados-hidrologicos-res` | Dados Hidráulicos por Reservatório – Base diária | diária | 1960 a 2026 | [dados-hidrologicos-res](datasets/dados-hidrologicos-res.md) |

## Geração

| Dataset | O que é | Granularidade | Cobertura | Página |
|---|---|---|---|---|
| `geracao-usina-2` | Geração por Usina em Base Horária | horária | 2000 a 2026 | [geracao-usina-2](datasets/geracao-usina-2.md) |
| `fator-capacidade-2` | Fator de Capacidade de Geração Eólica e Solar | horária | 2009 a 2026 | [fator-capacidade-2](datasets/fator-capacidade-2.md) |

## Preços (CMO e CVU)

| Dataset | O que é | Granularidade | Cobertura | Página |
|---|---|---|---|---|
| `cmo-semanal` | CMO Semanal | semanal | 2005 a 2026 | [cmo-semanal](datasets/cmo-semanal.md) |
| `cmo-semi-horario` | CMO Semi-Horário | semi-horária (30 minutos) | 2020 a 2026 | [cmo-semi-horario](datasets/cmo-semi-horario.md) |
| `cvu-usitermica` | CVU das Usina Térmicas | semanal (por revisão do PMO) | 2005 a 2026 | [cvu-usitermica](datasets/cvu-usitermica.md) |

## Balanço e intercâmbio

| Dataset | O que é | Granularidade | Cobertura | Página |
|---|---|---|---|---|
| `balanco-energia-subsistema` | Balanço de Energia nos Subsistemas | horária | 2000 a 2026 | [balanco-energia-subsistema](datasets/balanco-energia-subsistema.md) |
| `intercambio-nacional` | Intercâmbios Entre Subsistemas | horária | 2000 a 2026 | [intercambio-nacional](datasets/intercambio-nacional.md) |
| `intercambio-internacional` | Intercâmbio do SIN com Outros Países | horária | 2000 a 2026 | [intercambio-internacional](datasets/intercambio-internacional.md) |

## Cadastros

| Dataset | O que é | Granularidade | Cobertura | Página |
|---|---|---|---|---|
| `capacidade-geracao` | Capacidade Instalada de Geração | retrato do dia (sem histórico) | retrato do dia | [capacidade-geracao](datasets/capacidade-geracao.md) |
| `reservatorio` | Reservatórios | retrato do dia (sem histórico) | retrato do dia | [reservatorio](datasets/reservatorio.md) |
| `usina_conjunto` | Dados do Relacionamento Entre Conjuntos e Usinas | histórico de vínculos (retrato do dia) | retrato do dia | [usina_conjunto](datasets/usina_conjunto.md) |

## Como o ONS publica

- O ONS mantém um portal CKAN de dados abertos (https://dados.ons.org.br) e hospeda os arquivos em um bucket S3 público (programa de dados abertos da AWS). Cada conjunto tem arquivos por ano (ou por mês), nos formatos Parquet, CSV e XLSX, e um dicionário de dados em PDF e JSON.
- Os conjuntos são atualizados todos os dias (em geral às 12h e 19h; os dados hidrológicos três vezes ao dia). O ONS avisa que os dados passam por consistência recorrente e podem ser corrigidos depois de publicados.
- Os arquivos do ano corrente são reenviados a cada atualização; os cadastros (capacidade, reservatórios, usinas e conjuntos) são retratos do dia, sem histórico.
- O fetcher lista o bucket, escolhe o melhor formato de cada período (Parquet, depois CSV, ZIP, XLSX) e baixa só os arquivos novos ou alterados.
- A licença do portal é Creative Commons Atribuição (CC BY).
- O conversor mantém o tipo de cada arquivo de origem: os conjuntos mais antigos têm valores numéricos gravados como texto (oito casas decimais, zero como `0E-8`) em parte dos anos. Cada página lista as colunas e os anos afetados.

## Como os conjuntos se relacionam

- Os subsistemas (`N`, `NE`, `S`, `SE`) e o total `SIN` ligam carga, balanço, EAR, ENA, CMO e intercâmbios por `id_subsistema` (o código vem com espaços à direita em parte dos arquivos).
- Os reservatórios ligam o cadastro (`reservatorio`), os dados hidrológicos, a EAR e a ENA por reservatório pelo nome e pelo código de planejamento (`cod_resplanejamento`), que se repete em alguns casos; confira a página de cada conjunto.
- Usinas aparecem em `geracao-usina-2`, `fator-capacidade-2` e `capacidade-geracao`, ligáveis pelo `ceg` (código da ANEEL) e pelo identificador do ONS (`id_ons`).

## Quebras que valem para mais de um dataset

| Desde | Mudança | Afeta |
|---|---|---|
| 2021-03 | A carga passa a incluir a previsão de geração das usinas não despachadas | `carga-energia`, `carga-mensal`, `curva-carga` |
| 2022-01 | Geração e fator de capacidade passam de arquivos anuais a mensais | `geracao-usina-2`, `fator-capacidade-2` |
| 2023-04-29 | A carga passa a incluir a micro e minigeração distribuída (MMGD) estimada | `carga-energia`, `carga-mensal`, `curva-carga` |
| 2023 | Os arquivos de intercâmbio passam de CSV a Parquet | `intercambio-nacional`, `intercambio-internacional` |
