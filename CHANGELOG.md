# Changelog

Todas as alterações notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Corrigido
- O catálogo passa a listar o bucket S3 público: diretórios e nomes mudaram
  (`curva-carga-ho`, `EAR_DIARIO_BACIAS`, `GERACAO_USINA-2`,
  `RELACIONAMENTO_USINA_CONJUNTO`), causando 404 em massa.
- Um formato por arquivo (parquet > csv > zip > xlsx), sem duplicar anos.

## [0.1.0] - 2026-11-01

### Adicionado
- Versão inicial do pacote `ons-fetcher` (`quantilica ons`).
- Suporte a `list`, `check`, `sync` e verificação de frescor via SDK `FetcherApp`.

- Conversor Universal Hive Parquet Lake com `DatasetSpec` em `lake.py`.

