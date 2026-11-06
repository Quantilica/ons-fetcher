# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Corrigido
- Falha ao listar o diretório de um conjunto no bucket do ONS deixa de sumir do catálogo em silêncio: é registrada em `warning` com o conjunto e o erro, o resultado parcial não é guardado em cache e `list`/`sync` terminam com erro (`CatalogListingError`).

### Alterado
- A saída do CLI passa a usar o console Rich em vez de `typer.echo`.

## [0.2.0] - 2026-11-04

### Adicionado
- Catálogo completo por domínio (`catalog_<dominio>.py`, 8 grupos): os 88 pacotes do CKAN do ONS (2026-11-03) estão catalogados (87 conjuntos + 1 link externo excluído), com `s3_dir`, prefixo, granularidade e `tier` (`r1` baixa hoje; `listed` = listado, download em release futura). R1 segue com 23 conjuntos; `programacao` (7) e `indicadores` (23) ficam como listados.
- `MACRO_ALIASES` (`avaliacao-da-operacao`, `programacao-da-operacao`, `integracao-de-instalacoes`, `energia`); `GROUP_ALIASES` agora mapeia para listas.
- `quantilica ons catalogo [grupo] [--tier]`: catálogo estático completo, sem rede.
- `quantilica ons discover [--json] [--fail-on-change]` e `ons_fetcher.discover.discover()`: detecta pacotes novos/removidos, diretórios S3 movidos e períodos posteriores ao snapshot (`catalog_snapshot.py`).
- `geracao-usina-2` e `fator-capacidade-2` com granularidade `mixed`: o catálogo cobre as duas faixas (anual `GERACAO_USINA-2_AAAA` / `FATOR_CAPACIDADE_AAAA`, esta com prefixo próprio, até 2021; mensal `..._AAAA_MM` desde 2022). No lake, partição `ano/mes` com `mes=0` para os arquivos anuais (sem colisão com o mensal) e coluna `periodicidade` (`anual`/`mensal`). Reconverter (`--force`) esses dois conjuntos se já houver parquet legado só da faixa mensal.
- `list`/`sync` continuam restritos aos conjuntos R1 (ids inalterados).

### Corrigido
- Lake: reconversão idempotente conta `skipped` (antes contava tudo como convertido).
- Política de frescor volta a F1 (`HEAD_OR_MANIFEST`): `REMOTE_ONLY` (F3, para fontes sem validadores) causava re-download diário de fontes com Last-Modified/ETag, porque descartava o Last-Modified e o nome do arquivo caía em `@hoje`.
- O catálogo passa a listar o bucket S3 público: diretórios e nomes mudaram
  (`curva-carga-ho`, `EAR_DIARIO_BACIAS`, `GERACAO_USINA-2`,
  `RELACIONAMENTO_USINA_CONJUNTO`), causando 404 em massa.
- Um formato por arquivo (parquet > csv > zip > xlsx), sem duplicar anos.
- Sem o extra `analysis`, o comando `convert` termina com código 1 e a instrução de instalação (`quantilica install ons --extra analysis`), sem traceback.

## [0.1.0] - 2026-11-01

### Adicionado
- Versão inicial do pacote `ons-fetcher` (`quantilica ons`).
- Suporte a `list`, `check`, `sync` e verificação de frescor via SDK `FetcherApp`.

- Conversor Universal Hive Parquet Lake com `DatasetSpec` em `lake.py`.

