---
dataset:
  id: usina_conjunto
  fonte: ons
  titulo: "Dados do Relacionamento Entre Conjuntos e Usinas (ONS)"
  resumo: "Relacionamento entre usinas Tipo II-C e os conjuntos de usinas de que fazem parte, com as datas de início e fim do vínculo."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/usina_conjunto
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/usina_conjunto"
  periodicidade: "diária (retrato, com histórico de vínculos)"
  cobertura: {inicio: 2026-11, fim: em-curso}
  unidade: "o vínculo entre uma usina e um conjunto de usinas, com o início e o fim do relacionamento"
  granularidade: {espacial: "usina e conjunto de usinas", temporal: "histórico de vínculos (retrato do dia)"}
  formato_bruto: "um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização"
  lake: {estado: convertido, particoes: [], chave: [id_ons_usina, dat_iniciorelacionamento], colunas: 14}
  unidades_de_medida:
    id_conjuntousina: "código (sem unidade)"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Dados do Relacionamento Entre Conjuntos e Usinas

## Resumo

Relacionamento entre usinas Tipo II-C e os conjuntos de usinas de que fazem parte, com as datas de início e fim do vínculo.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/usina_conjunto` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/usina_conjunto |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/usina_conjunto |
| Periodicidade | diária (retrato, com histórico de vínculos) |
| Cobertura | 2026-11 a em-curso |
| Unidade (uma linha) | o vínculo entre uma usina e um conjunto de usinas, com o início e o fim do relacionamento |
| Granularidade | espacial: usina e conjunto de usinas; temporal: histórico de vínculos (retrato do dia) |
| Formato bruto | um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização |
| Estado no lake | convertido |
| Partições | — |
| Chave | `id_ons_usina`, `dat_iniciorelacionamento` |
| Colunas | 14 |
| Unidades de medida | `id_conjuntousina`: código (sem unidade) |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `usina_conjunto`, https://dados.ons.org.br/dataset/usina_conjunto). Os arquivos ficam no bucket público S3 do ONS, em `dataset/usina_conjunto/`.
- O ONS publica um arquivo único (`USINA_CONJUNTO.parquet`, e as mesmas tabelas em CSV e XLSX) e o atualiza todo dia, sem guardar histórico.
- No bruto, o arquivo fica em `cadastros/usina_conjunto_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: o vínculo entre uma usina e um conjunto de usinas, com o início e o fim do relacionamento.
- Uma única carga com 2.457 linhas em 2026-11-15 (retrato do dia; sem histórico).

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Identificador do subsistema do conjunto de usinas | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do subsistema do conjunto de usinas | — | todo |
| `estad_id` | `estad_id` | texto | Identificador do estado da subestação coletora do conjunto de usinas | — | todo |
| `nom_estado` | `nom_estado` | texto | Nome do estado da subestação coletora do conjunto de usinas | — | todo |
| `id_tipousina` | `id_tipousina` | texto | Tipo da usina | — | todo |
| `nom_tipousina` | `nom_tipousina` | texto | Nome do Tipo da usina | — | todo |
| `id_conjuntousina` | `id_conjuntousina` | inteiro | Código ONS do Conjunto Usina | código (sem unidade) | todo |
| `id_ons_conjunto` | `id_ons_conjunto` | texto | Identificador do conjunto de usinas no ONS. Se o valor for vazio, significa que esta usina não tem associação com conjunto. | — | todo |
| `id_ons_usina` | `id_ons_usina` | texto | Identificador da usina no ONS | — | todo |
| `nom_conjunto` | `nom_conjunto` | texto | Nome do conjunto de usinas. Se o valor for vazio, significa que esta usina não tem associação com conjunto. | — | todo |
| `nom_usina` | `nom_usina` | texto | Nome da usina | — | todo |
| `ceg` | `ceg` | texto | Código Único do Empreendimento de Geração (CEG), estabelecido pela ANEEL | — | todo |
| `dat_iniciorelacionamento` | `dat_iniciorelacionamento` | texto | Data de início do relacionamento da usina e no conjunto. Se a informação do campo “id_ons_conjunto “ for vazia, está data representa data de entrada de operação da Usina | — | todo |
| `dat_fimrelacionamento` | `dat_fimrelacionamento` | texto | Data de fim do relacionamento da usina e no conjunto. Se o valor for vazio, significa que esta usina não tem associação com conjunto | — | todo |

## No lake

- Dataset `ons/usina_conjunto`, sem partição (arquivo único); um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.

## Cuidados de uso

- **Retrato do dia.** O ONS lê os dados das origens e atualiza o arquivo todo dia; o lake guarda só a versão mais recente, que traz 2.457 vínculos com datas de início de 1924-03-01 a 2026-10-29. `dat_fimrelacionamento` nula (2.041 linhas) indica vínculo vigente.
- `id_ons_conjunto` e `nom_conjunto` são nulos (298 linhas) nas usinas sem conjunto, conforme o dicionário oficial.
- As colunas de datas (`dat_iniciorelacionamento`, `dat_fimrelacionamento`) são texto (`AAAA-MM-DD`); o identificador `id_ons_usina` vem com espaços à direita em 222 linhas.
- O nome da coluna do estado é `estad_id` (como no dicionário oficial).
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `id_ons_usina` (222 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Quantidade de usinas por conjunto com vínculo vigente.

```python
import duckdb

duckdb.sql("""
    SELECT nom_conjunto, count(*) AS usinas
    FROM read_parquet('lake/ons/usina_conjunto/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE dat_fimrelacionamento IS NULL AND nom_conjunto IS NOT NULL
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/usina_conjunto
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/usina_conjunto/DicionarioDados_Usina_Conjunto.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
