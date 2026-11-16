---
dataset:
  id: fator-capacidade-2
  fonte: ons
  titulo: "Fator de Capacidade de Geração Eólica e Solar (ONS)"
  resumo: "Fator de capacidade de usinas e conjuntos eólicos e solares despachados pelo ONS, em base horária: a razão entre a geração e a capacidade instalada."
  orgao: Operador Nacional do Sistema Elétrico (ONS)
  pagina_oficial: https://dados.ons.org.br/dataset/fator-capacidade-2
  licenca: "Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/fator-capacidade-2"
  periodicidade: "diária (o ONS atualiza duas vezes ao dia)"
  cobertura: {inicio: 2009, fim: em-curso}
  unidade: "o fator de capacidade de uma usina ou conjunto eólico ou solar em uma hora"
  granularidade: {espacial: "usina ou conjunto, com ponto de conexão e coordenadas", temporal: "horária"}
  formato_bruto: "arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano e, desde 2022, um por mês"
  lake: {estado: convertido, particoes: [ano, mes], chave: [ano, mes, nom_usina_conjunto, id_ons, din_instante], colunas: 22}
  unidades_de_medida:
    val_latitudesecoletora: "graus"
    val_longitudesecoletora: "graus"
    val_latitudepontoconexao: "graus"
    val_longitudepontoconexao: "graus"
    val_geracaoprogramada: "MWmed (texto)"
    val_geracaoverificada: "MWmed (texto)"
    val_capacidadeinstalada: "MW (texto)"
    val_fatorcapacidade: "razão geração/capacidade (texto até 2025)"
  dados_pessoais: nenhum
  eras:
    - {desde: 2026, mudanca: "`val_fatorcapacidade`: texto até 2025, decimal desde 2026"}
  revisado_em: 2026-11-15
  versao_fetcher: 0.3.0
---

# Fator de Capacidade de Geração Eólica e Solar

## Resumo

Fator de capacidade de usinas e conjuntos eólicos e solares despachados pelo ONS, em base horária: a razão entre a geração e a capacidade instalada.

## Ficha técnica

<!-- gerado:ficha -->

| Campo | Valor |
|---|---|
| Dataset | `ons/fator-capacidade-2` |
| Órgão | Operador Nacional do Sistema Elétrico (ONS) |
| Página oficial | https://dados.ons.org.br/dataset/fator-capacidade-2 |
| Licença | Creative Commons Atribuição (CC BY), conforme o portal de dados abertos do ONS: https://dados.ons.org.br/dataset/fator-capacidade-2 |
| Periodicidade | diária (o ONS atualiza duas vezes ao dia) |
| Cobertura | 2009 a em-curso |
| Unidade (uma linha) | o fator de capacidade de uma usina ou conjunto eólico ou solar em uma hora |
| Granularidade | espacial: usina ou conjunto, com ponto de conexão e coordenadas; temporal: horária |
| Formato bruto | arquivos Parquet (ou CSV com ponto e vírgula, quando não há Parquet) no bucket público S3 do ONS, um por ano e, desde 2022, um por mês |
| Estado no lake | convertido |
| Partições | `ano`, `mes` |
| Chave | `ano`, `mes`, `nom_usina_conjunto`, `id_ons`, `din_instante` |
| Colunas | 22 |
| Unidades de medida | `val_latitudesecoletora`: graus; `val_longitudesecoletora`: graus; `val_latitudepontoconexao`: graus; `val_longitudepontoconexao`: graus; `val_geracaoprogramada`: MWmed (texto); `val_geracaoverificada`: MWmed (texto); `val_capacidadeinstalada`: MW (texto); `val_fatorcapacidade`: razão geração/capacidade (texto até 2025) |
| Dados pessoais | nenhum |
| Eras | 2026: `val_fatorcapacidade`: texto até 2025, decimal desde 2026 |
| Revisado em | 2026-11-15 |
| Versão do fetcher | 0.3.0 |

## Origem e coleta

- Fonte: Portal de Dados Abertos do ONS (conjunto `fator-capacidade-2`, https://dados.ons.org.br/dataset/fator-capacidade-2). Os arquivos ficam no bucket público S3 do ONS, em `dataset/fator_capacidade_2_di/`.
- O ONS publica um arquivo por ano (2000 a 2021) e por mês (desde 2022) com o prefixo `FATOR_CAPACIDADE-2` (`FATOR_CAPACIDADE-2_AAAA.parquet`; mensais `..._AAAA_MM`), cada um também em CSV e em XLSX. Listagem do bucket em 2026-11-15: 72 arquivos Parquet e 72 CSV, de 2009 a 2026.
- No bruto, o arquivo fica em `geracao/fator-capacidade-2_AAAA[_MM]@AAAAMMDD.<extensão>`; o carimbo é a data da coleta e o lake converte a versão mais recente.
- O dicionário de dados do ONS (PDF e JSON) fica no mesmo diretório e o fetcher não o baixa; as descrições da seção Variáveis vêm do JSON do dicionário, conferidas contra os valores observados.
- **Conferência por amostra.** Os arquivos deste conjunto são grandes; esta página foi conferida em 5 arquivos (de 72 Parquet publicados), escolhidos para cobrir os extremos e as quebras de formato.

## Conteúdo

- Unidade de análise: o fator de capacidade de uma usina ou conjunto eólico ou solar em uma hora.
- 5 arquivos convertidos (amostra), de 2009 a 2026-10: 6.958 linhas no primeiro e 175.560 no último; 1.764.382 linhas no total. O arquivo do ano corrente cresce a cada atualização.
- Mudanças de tipo entre arquivos (conferidas nos Parquet convertidos):
    - 2026: `val_fatorcapacidade`: texto até 2025, decimal desde 2026.

## Variáveis

Descrições do dicionário de dados do ONS (JSON publicado com o conjunto). O conversor normaliza os nomes de coluna (minúsculas, sem acento e sem separadores soltos); quando o nome do lake difere do dicionário, a coluna 'Na fonte' mostra o nome do dicionário.

| Coluna no lake | Na fonte | Tipo | Descrição | Unidade / códigos | Período |
|---|---|---|---|---|---|
| `id_subsistema` | `id_subsistema` | texto | Identificador do subsistema | — | todo |
| `nom_subsistema` | `nom_subsistema` | texto | Nome do subsistema | — | todo |
| `id_estado` | `id_estado` | texto | Sigla do Estado | — | todo |
| `nom_estado` | `nom_estado` | texto | Nome do Estado | — | todo |
| `cod_pontoconexao` | `cod_pontoconexao` | texto | Código do ponto de conexão da usina/conjunto | — | todo |
| `nom_pontoconexao` | `nom_pontoconexao` | texto | Nome do ponto de conexão da usina/conjunto | — | todo |
| `nom_localizacao` | `nom_localizacao` | texto | Localização da usina/conjunto O conteúdo está disponível apenas para Usinas da região Nordeste | — | todo |
| `val_latitudesecoletora` | `val_latitudesecoletora` | decimal | Latitude da usina/conjunto | graus | todo |
| `val_longitudesecoletora` | `val_longitudesecoletora` | decimal | Longitude da usina/conjunto | graus | todo |
| `val_latitudepontoconexao` | `val_latitudepontoconexao` | decimal | Latitude do Ponto de Conexão | graus | todo |
| `val_longitudepontoconexao` | `val_longitudepontoconexao` | decimal | Longitude do Ponto de Conexão | graus | todo |
| `nom_modalidadeoperacao` | `nom_modalidadeoperacao` | texto | Modalidade de operação | — | todo |
| `nom_tipousina` | `nom_tipousina` | texto | Tipo da usina | — | todo |
| `nom_usina_conjunto` | `nom_usina_conjunto` | texto | Nome da usina/conjunto | — | todo |
| `id_ons` | `id_ons` | texto | Identificador da usina ou conjunto no ONS | — | todo |
| `ceg` | `ceg` | texto | Código Único do Empreendimento de Geração (CEG), estabelecido pela ANEEL | — | todo |
| `din_instante` | `din_instante` | data e hora | Data | — | todo |
| `val_geracaoprogramada` | `val_geracaoprogramada` | texto | Geração Programada, em MWmed | MWmed (texto) | todo |
| `val_geracaoverificada` | `val_geracaoverificada` | texto | Geração Verificada, em MWmed | MWmed (texto) | todo |
| `val_capacidadeinstalada` | `val_capacidadeinstalada` | texto | Capacidade instalada, em MW | MW (texto) | todo |
| `val_fatorcapacidade` | `val_fatorcapacidade` | decimal (texto em parte dos arquivos) | Fator de capacidade, obtida pela relação entre a geração e a capacidade instalada | razão geração/capacidade (texto até 2025) | todo |
| `periodicidade` | — (gerada) | texto | Periodicidade do arquivo de origem: `anual` ou `mensal` | `anual`, `mensal` | todo |
| `ano` | — (partição) | inteiro | Ano do arquivo de origem | — | todo |
| `mes` | — (partição) | inteiro | Mês do arquivo de origem; 0 nos arquivos anuais | — | todo |

## No lake

- Dataset `ons/fator-capacidade-2`, particionado por `ano`, `mes`; um Parquet por arquivo de origem.
- O conversor lê o Parquet ou o CSV (separador `;`, vírgula decimal, UTF-8 ou ISO-8859-1; os CSV do ONS usam ponto decimal, então as colunas numéricas lidas de CSV ficam como texto), normaliza os nomes de coluna e **mantém os tipos do arquivo de origem**: não converte texto em número nem em data.
- A partição vem do nome do arquivo (`FATOR_CAPACIDADE-2_AAAA`; `_AAAA_MM` nos mensais, com `mes = 0` nos anuais); se o arquivo não tiver a coluna, o conversor a acrescenta.
- A coluna `periodicidade` (`anual` ou `mensal`) é acrescentada pelo conversor.

## Cuidados de uso

- **Cada arquivo é a série do período, com o ano corrente em atualização.** O ONS reenvia o arquivo do ano (ou do mês) corrente e avisa que os dados passam por consistência; valores já publicados podem mudar. Reconverta depois de cada atualização antes de fechar um período.
- **Granularidade mista:** os arquivos anuais (de 2009 a 2021, com o prefixo `FATOR_CAPACIDADE`) e os mensais (desde 2022, `FATOR_CAPACIDADE-2`) convivem em `ano` e `mes`, com `mes = 0` para os anuais e a coluna `periodicidade`.
- `val_geracaoprogramada`, `val_geracaoverificada` e `val_capacidadeinstalada` chegam como texto em todos os arquivos (`val_fatorcapacidade` também, exceto no arquivo mais recente convertido); converta com `CAST`.
- A coluna `nom_localizacao` só tem conteúdo para usinas da região Nordeste (descrição oficial).
- **Colunas numéricas com tipo misto entre arquivos.** 1 coluna(s) (`val_fatorcapacidade`) chegam como texto em alguns anos e como decimal em outros (o texto traz oito casas decimais e o zero como `0E-8`); veja as mudanças acima. Ao ler vários anos juntos, converta com `CAST(... AS DOUBLE)`.

## Exemplos

Fator de capacidade médio das usinas solares e eólicas em 2026-10, por tipo.

```python
import duckdb

duckdb.sql("""
    SELECT nom_tipousina, round(avg(CAST(val_fatorcapacidade AS DOUBLE)), 3) AS fator_medio
    FROM read_parquet('lake/ons/fator-capacidade-2/**/*.parquet', hive_partitioning = true, union_by_name = true)
    WHERE ano = 2026 AND mes = 10
    GROUP BY 1
""").show()
```

## Referências

- Conjunto no portal de dados abertos do ONS: https://dados.ons.org.br/dataset/fator-capacidade-2
- Dicionário de dados (PDF): https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/fator_capacidade_2_di/DicionarioDados_FatorCapacidade.pdf
- Programa de dados abertos da AWS com o catálogo do ONS: https://registry.opendata.aws/ons-opendata-portal/
