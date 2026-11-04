# ons-fetcher

[![CI](https://github.com/Quantilica/ons-fetcher/actions/workflows/test.yml/badge.svg)](https://github.com/Quantilica/ons-fetcher/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Coletor e conversor Lake Hive para dados abertos de **Operador Nacional do Sistema Elétrico** (`ons`), parte do ecossistema [Quantilica](https://quantilica.com).

## Instalação

### Via CLI Quantilica (recomendado)

```bash
quantilica install ons
```

Para instalar com suporte à conversão Parquet Lake:

```bash
quantilica install ons --extra analysis
```

### Como biblioteca Python

```bash
uv add ons-fetcher --index https://index.quantilica.com/simple/
```

Com o extra de análise analítica:

```bash
uv add 'ons-fetcher[analysis]' --index https://index.quantilica.com/simple/
```

## Uso via CLI

```bash
# Listar os arquivos dos conjuntos R1 (os que baixam hoje)
quantilica ons list

# Catálogo completo (R1 + listados) e descoberta de novidades na fonte
quantilica ons catalogo programacao
quantilica ons discover

# Verificar novos arquivos e frescor
quantilica ons check

# Sincronizar arquivos para o diretório local bruto
quantilica ons sync -o /data/ons

# Converter acervo bruto para o Universal Hive Parquet Lake
quantilica ons convert /data/ons /data/lake
```

## Cobertura do catálogo

O CKAN do ONS publica 88 pacotes (2026-11-03). O catálogo cobre os 88: 87 conjuntos
em 8 grupos e 1 link externo excluído.

| Grupo | Conjuntos | R1 (baixa) | Listado |
|---|---:|---:|---:|
| carga | 8 | 3 | 5 |
| hidrologia | 17 | 9 | 8 |
| geracao | 13 | 2 | 11 |
| precos | 4 | 3 | 1 |
| intercambio | 6 | 3 | 3 |
| cadastros | 9 | 3 | 6 |
| programacao | 7 | 0 | 7 |
| indicadores | 23 | 0 | 23 |

`list` e `sync` operam só no tier R1; os demais ficam listados (`catalogo`) com
download previsto para releases futuras.

## Licença

Distribuído sob licença MIT. Consulte [LICENSE](LICENSE) para mais detalhes.
