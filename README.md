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
# Listar conjuntos disponíveis
quantilica ons list

# Verificar novos arquivos e frescor
quantilica ons check

# Sincronizar arquivos para o diretório local bruto
quantilica ons sync -o /data/ons

# Converter acervo bruto para o Universal Hive Parquet Lake
quantilica ons convert /data/ons /data/lake
```

## Licença

Distribuído sob licença MIT. Consulte [LICENSE](LICENSE) para mais detalhes.
