# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado
- Catálogo completo por domínio (`catalog_<dominio>.py`, 8 grupos): os 88 pacotes do CKAN do ONS (2026-11-03) estão catalogados (87 conjuntos + 1 link externo excluído), com `s3_dir`, prefixo, granularidade e `tier` (`r1` baixa hoje; `listed` = listado, download em release futura). R1 segue com 23 conjuntos; `programacao` (7) e `indicadores` (23) ficam como listados.
- `MACRO_ALIASES` (`avaliacao-da-operacao`, `programacao-da-operacao`, `integracao-de-instalacoes`, `energia`); `GROUP_ALIASES` agora mapeia para listas.
- `quantilica ons catalogo [grupo] [--tier]`: catálogo estático completo, sem rede.
- `quantilica ons discover [--json] [--fail-on-change]` e `ons_fetcher.discover.discover()`: detecta pacotes novos/removidos, diretórios S3 movidos e períodos posteriores ao snapshot (`catalog_snapshot.py`).
- Pendência conhecida (não alterada nesta entrega): `geracao-usina-2` (anual até 2021, mensal desde 2022) e `fator-capacidade-2` (anual 2009-2021, mensal desde 2022) têm granularidade mista na fonte; o R1 baixa só uma das faixas. Exige decisão sobre as chaves de partição do lake.
- `list`/`sync` continuam restritos aos conjuntos R1 (ids inalterados).

### Corrigido
- Política de frescor volta a F1 (`HEAD_OR_MANIFEST`): `REMOTE_ONLY` (F3, para fontes sem validadores) causava re-download diário de fontes com Last-Modified/ETag, porque descartava o Last-Modified e o nome do arquivo caía em `@hoje`.
- O catálogo passa a listar o bucket S3 público: diretórios e nomes mudaram
  (`curva-carga-ho`, `EAR_DIARIO_BACIAS`, `GERACAO_USINA-2`,
  `RELACIONAMENTO_USINA_CONJUNTO`), causando 404 em massa.
- Um formato por arquivo (parquet > csv > zip > xlsx), sem duplicar anos.

## [0.1.0] - 2026-11-01

### Adicionado
- Versão inicial do pacote `ons-fetcher` (`quantilica ons`).
- Suporte a `list`, `check`, `sync` e verificação de frescor via SDK `FetcherApp`.

- Conversor Universal Hive Parquet Lake com `DatasetSpec` em `lake.py`.

