---
dataset:
  id: reservatorio
  fonte: ons
  titulo: "Reservatórios (ONS)"
  resumo: "Cadastro dos reservatórios do sistema: tipo, usina, bacia, rio, REE, cotas e volumes operativos, produtividade e perda de carga."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/reservatorio
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/reservatorio"
  periodicidade: "diária (retrato, sem histórico)"
  cobertura: {inicio: 2026-11, fim: em-curso}
  unidade: "um reservatório (ou conjunto reservatório e usina)"
  granularidade: {espacial: "reservatório", temporal: "retrato do dia (sem histórico)"}
  formato_bruto: "um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização"
  lake: {estado: convertido, particoes: [], chave: [nom_reservatorio, nom_usina, cod_posto], colunas: 24}
  unidades_de_medida:
    val_cotamaxima: "m"
    val_cotaminima: "m"
    val_volmax: "hm3"
    val_volmin: "hm3"
    val_volutiltot: "hm3"
    val_produtibilidadeespecifica: "MW por altura de queda (unidade não detalhada pela fonte)"
    val_produtividade65volutil: "% (descrição oficial)"
    val_perda: "% ou m, conforme val_tipoperda"
    val_latitude: "graus"
    val_longitude: "graus"
    cod_resplanejamento: "código (sem unidade)"
    cod_posto: "código (sem unidade)"
  dados_pessoais: nenhum
  eras: []
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Reservatórios

## Resumo

Cadastro dos reservatórios do sistema: tipo, usina, bacia, rio, REE, cotas e volumes operativos, produtividade e perda de carga.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/reservatorio` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/reservatorio |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/reservatorio |
| Periodicidade | diária (retrato, sem histórico) |
| Cobertura | 2026-11 a em-curso |
| Unidade (uma linha) | um reservatório (ou conjunto reservatório e usina) |
| Granularidade | espacial: reservatório; temporal: retrato do dia (sem histórico) |
| Formato bruto | um arquivo Parquet (ou CSV) único no bucket público S3 do ONS, substituído a cada atualização |
| Estado no lake | convertido |
| Partições | — |
| Chave | `nom_reservatorio`, `nom_usina`, `cod_posto` |
| Colunas | 24 |
| Unidades de medida | `val_cotamaxima`: m; `val_cotaminima`: m; `val_volmax`: hm3; `val_volmin`: hm3; `val_volutiltot`: hm3; `val_produtibilidadeespecifica`: MW por altura de queda (unidade não detalhada pela fonte); `val_produtividade65volutil`: % (descrição oficial); `val_perda`: % ou m, conforme val_tipoperda; `val_latitude`: graus; `val_longitude`: graus; `cod_resplanejamento`: código (sem unidade); `cod_posto`: código (sem unidade) |
| Dados pessoais | nenhum |
| Eras | nenhuma |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `reservatorio`, https://dados.ons.org.br/dataset/reservatorio). Os arquivos ficam no bucket público S3 do ONS, em `dataset/reservatorio/`.
- O ONS publica um arquivo único (`RESERVATORIOS.parquet`, e as mesmas tabelas em CSV e XLSX) e o atualiza todo dia, sem guardar histórico.
- No bruto, o arquivo fica em `cadastros/reservatorio_AAAA@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.

## Conteúdo

- Unidade de análise: um reservatório (ou conjunto reservatório e usina).
- Uma única carga com 162 linhas em 2026-11-15 (retrato do dia; sem histórico).

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `nom_reservatorio` | `nom_reservatorio` | texto | Nome do Reservatório | — | todo |
| `tip_reservatorio` | `tip_reservatorio` | texto | Tipo de Reservatório | — | todo |
| `cod_resplanejamento` | `cod_resplanejamento` | inteiro | Código do Reservatório nos Modelos de Planejamento | código (sem unidade) | todo |
| `cod_posto` | `cod_posto` | inteiro | Posto de Vazão da Usina | código (sem unidade) | todo |
| `nom_usina` | `nom_usina` | texto | Nome da Usina | — | todo |
| `ceg` | `ceg` | texto | Código Único do Empreendimento de Geração (CEG), estabelecido pela ANEEL | — | todo |
| `id_subsistema` | `id_subsistema` | texto | Código do Subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do Subsistema | — | todo |
| `nom_bacia` | `nom_bacia` | texto | Nome da Bacia Hidro-Energética | — | todo |
| `nom_rio` | `nom_rio` | texto | Nome do Rio | — | todo |
| `nom_ree` | `nom_ree` | texto | Nome do Reservatório Equivalente | — | todo |
| `dat_entrada` | `dat_entrada` | texto | Data de Entrada em Operação | — | todo |
| `val_cotamaxima` | `val_cotamaxima` | decimal | Cota Máxima Para Operação. Altura máxima do nível d'água de um reservatório, considerado para fins de operação normal medido em metros(m) | m | todo |
| `val_cotaminima` | `val_cotaminima` | decimal | Cota Mínima Para Operação. Altura mínima do nível d'água de um reservatório considerado para fins de operação normal medido em metros(m). | m | todo |
| `val_volmax` | `val_volmax` | decimal | Volume Máximo. Volume do reservatório correspondente ao nível máximo operativo medido em hectômetro cúbico (hm3) | hm3 | todo |
| `val_volmin` | `val_volmin` | decimal | Volume Mínimo. Volume do reservatório correspondente ao nível mínimo operativo medido em hectômetro cúbico (hm3) | hm3 | todo |
| `val_volutiltot` | `val_volutiltot` | decimal | Volume Útil Total. Volume do reservatório compreendido entre o nível máximo de operação e mínimo normal de operação medido em hectômetro cúbico (hm3) | hm3 | todo |
| `val_produtibilidadeespecifica` | `val_produtibilidadeespecifica` | decimal | Produtividade Específica, que indica quantos MW serão ganhos pela altura da queda | MW por altura de queda (unidade não detalhada pela fonte) | todo |
| `val_produtividade65volutil` | `val_produtividade65volutil` | decimal | Produtividade a 65% do volume útil medido em % | % (descrição oficial) | todo |
| `val_tipoperda` | `val_tipoperda` | texto | Tipo da Perda de Carga. Indica se o tipo de perda de carga está em porcentagem (%) ou Metros(m). | — | todo |
| `val_perda` | `val_perda` | decimal | Valor da perda de carga. Estes valores são os mesmos utilizados pelo programa Newave. | % ou m, conforme val_tipoperda | todo |
| `val_latitude` | `val_latitude` | decimal | Latitude do Reservatório | graus | todo |
| `val_longitude` | `val_longitude` | decimal | Longitude do Reservatório | graus | todo |
| `res_id` | `res_id` | texto | Sem descrição no dicionário oficial (coluna presente no arquivo). | — | todo |

Colunas do dicionário oficial que o arquivo não traz: `id_reservatorio`.

## No lake

- Dataset `ons/reservatorio`, sem partição (arquivo único); um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, UTF-8 ou ISO-8859-1), detecta o separador decimal de cada coluna numérica (os CSV do ONS usam ponto decimal), normaliza os nomes de coluna e grava as colunas numéricas como `double` em todos os anos, inclusive as que o ONS publica como texto (oito casas decimais, zero como `0E-8`); texto vazio vira nulo. Códigos, nomes e datas **mantêm o tipo do arquivo de origem**.

## Cuidados de uso

- **Sem histórico.** O ONS lê os dados das origens e atualiza o arquivo todo dia; o lake guarda só o retrato mais recente.
- As colunas de cotas e volumes (`val_cotamaxima`, `val_cotaminima`, `val_volmax`, `val_volmin`, `val_volutiltot`) são texto com três casas decimais na origem; o conversor os grava como `double`. A unidade dos volumes é hm3 e a das cotas, metros (descrição oficial).
- `val_tipoperda` indica se `val_perda` está em porcentagem ou em metros (`m` ou `%`; nulo em parte dos reservatórios).
- `cod_resplanejamento` se repete em 3 códigos (`ITAIPU`, `P. AFONSO 1,2,3` e `HENRY BORDEN` têm mais de uma linha); use o nome do reservatório, a usina e o posto de vazão.
- **Espaços nas pontas do texto.** Há valores preenchidos com espaços em: `res_id` (19 linhas). Aplique `trim` antes de juntar ou agrupar.

## Exemplos

Reservatórios com maior volume útil total, em hm3.

```python
import duckdb

duckdb.sql("""
    SELECT nom_reservatorio, nom_usina, val_volutiltot AS volume_util_hm3
    FROM read_parquet('lake/ons/reservatorio/**/*.parquet', hive_partitioning = true, union_by_name = true)
    ORDER BY 3 DESC NULLS LAST
    LIMIT 10
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/reservatorio
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/reservatorio/DicionarioDados_Reservatorio.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
