---
dataset:
  id: capacidade-geracao
  fonte: ons
  titulo: "Capacidade Instalada de Geração (ONS)"
  resumo: "Cadastro da potência nominal das unidades geradoras das usinas despachadas pelo ONS (modalidades Tipo I, II-A, II-B e II-C), em MW."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/capacidade-geracao
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/capacidade-geracao"
  periodicidade: "diária (retrato, sem histórico)"
  cobertura: {inicio: 2026-11, fim: em-curso}
  unidade: "uma unidade geradora de uma usina despachada"
  granularidade: {espacial: "unidade geradora (com usina, subsistema e estado)", temporal: "retrato do dia (sem histórico)"}
  formato_bruto: "um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização"
  lake: {estado: convertido, particoes: [], chave: [cod_equipamento], colunas: 18}
  unidades_de_medida:
    val_potenciaefetiva: "MW"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Capacidade Instalada de Geração

## Resumo

Cadastro da potência nominal das unidades geradoras das usinas despachadas pelo ONS (modalidades Tipo I, II-A, II-B e II-C), em MW.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/capacidade-geracao` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/capacidade-geracao |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/capacidade-geracao |
| Periodicidade | diária (retrato, sem histórico) |
| Cobertura | 2026-11 a em-curso |
| Unidade (uma linha) | uma unidade geradora de uma usina despachada |
| Granularidade | espacial: unidade geradora (com usina, subsistema e estado); temporal: retrato do dia (sem histórico) |
| Formato bruto | um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização |
| Estado no lake | convertido |
| Partições | — |
| Chave | `cod_equipamento` |
| Colunas | 18 |
| Unidades de medida | `val_potenciaefetiva`: MW |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `capacidade-geracao`, https://dados.ons.org.br/dataset/capacidade-geracao). Os arquivos ficam no bucket público S3 do ONS, em `dataset/capacidade-geracao/`.
- O ONS publica um arquivo único (`CAPACIDADE_GERACAO.parquet`, e as mesmas tabelas em CSV e XLSX) e o atualiza todo dia, sem guardar histórico.
- No bruto, o arquivo fica em `cadastros/capacidade-geracao_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: uma unidade geradora de uma usina despachada.
- Uma única carga com 5.837 linhas em 2026-11-15 (retrato do dia; sem histórico).

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema da Usina | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `id_estado` | `id_estado` | texto | Sigla do Estado Onde Está Localizada a Usina | — | todo |
| `nom_estado` | `nom_estado` | texto | Nome do Estado | — | todo |
| `nom_modalidadeoperacao` | `nom_modalidadeoperacao` | texto | Modalidade de Operação da Usina | — | todo |
| `nom_agenteproprietario` | `nom_agenteproprietario` | texto | Agente Proprietário da Usina | — | todo |
| `nom_agenteoperador` | `nom_agenteoperador` | texto | Agente Operador da Usina | — | todo |
| `nom_tipousina` | `nom_tipousina` | texto | Tipo da Usina. Temos os tipos de Usinas:EOLIELÉTRICA, FOTOVOLTAICA, HIDROELÉTRICA, NUCLEAR, TÉRMICA | — | todo |
| `nom_usina` | `nom_usina` | texto | Nome da Usina | — | todo |
| `ceg` | `ceg` | texto | Código Único do Empreendimento de Geração (CEG), estabelecido pela ANEEL | — | todo |
| `nom_unidadegeradora` | `nom_unidadegeradora` | texto | Nome da Unidade Geradora | — | todo |
| `cod_equipamento` | `cod_equipamento` | texto | Código do Equipamento – Unidade Geradora | — | todo |
| `num_unidadegeradora` | `num_unidadegeradora` | texto | Código Operacional da Unidade Geradora | — | todo |
| `nom_combustivel` | `nom_combustivel` | texto | Combustível da Unidade Geradora | — | todo |
| `dat_entradateste` | `dat_entradateste` | texto | Data da Liberação para Entrada em Comissionamento | — | todo |
| `dat_entradaoperacao` | `dat_entradaoperacao` | texto | Data da Liberação para Entrada em Operação Comercial | — | todo |
| `dat_desativacao` | `dat_desativacao` | texto | Data de Desativação da Unidade GeradoraO conteúdo NULL (ou vazio) representa que a unidade geradora está ativa. | — | todo |
| `val_potenciaefetiva` | `val_potenciaefetiva` | decimal | Potência Nominal da Unidade Geradora, Conforme Documento Normativo da ANEEL, em MW | MW | todo |

Colunas do dicionário oficial que o arquivo não traz: `id_ons`.

## No lake

- Dataset `ons/capacidade-geracao`, sem partição (arquivo único); um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.

## Cuidados de uso

- **Sem histórico.** O ONS lê os dados das origens e atualiza o arquivo todo dia; o lake guarda só o retrato mais recente. Para uma série, guarde as versões do bruto.
- `dat_desativacao` nula significa unidade ativa (4.736 das 5.837 unidades em 2026-11).
- O dicionário oficial lista `id_ons` (identificador da usina), mas o arquivo do ONS não traz essa coluna.
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `nom_subsistema` (5.837 linhas); `cod_equipamento` (5.837 linhas); `num_unidadegeradora` (5.837 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Potência efetiva ativa por tipo de usina e subsistema, em MW.

```python
import duckdb

duckdb.sql("""
    SELECT nom_tipousina, id_subsistema, round(sum(val_potenciaefetiva), 0) AS mw
    FROM read_parquet('lake/ons/capacidade-geracao/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE dat_desativacao IS NULL
    GROUP BY 1, 2
    ORDER BY 3 DESC
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/capacidade-geracao
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/capacidade-geracao/DicionarioDados_Capacidade_Instalada_Geracao.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
