---
name: sia.report
description: Especialista em geração de relatórios (Markdown, Excel, TSV) a partir de SQL via módulo `app.reporter`. Gerencia a extração de dados utilizando configurações centralizadas em TOML.
---

# SIA Reporting & Data Extraction

Esta skill gerencia a camada de **Saída (Output)** do sistema SIA, transformando consultas SQL em documentos auditáveis e formatados.

## 1. O Motor: `app.reporter`

O módulo `app.reporter` centraliza a execução de queries e o roteamento para os exportadores. Ele não recebe caminhos de banco de dados via linha de comando, mas utiliza a infraestrutura do `app.core` para ler o estado global do sistema e ler os bancos de dados definidos em `var/db_config.toml`.

### A. Uso via CLI (Linha de Comando)

O formato de saída é detectado automaticamente pela extensão do arquivo fornecido no parâmetro `--out`.

**Sintaxe:**

```powershell
python -m sia.reporter --out <caminho/arquivo.ext> --sql <query_ou_arquivo.sql> [--title "Título"]

```

**Exemplos:**

* **Markdown:** `python -m sia.reporter --out relatorio.md --sql "SELECT * FROM v_criticas" --title "Críticas de Auditoria"`
* **Excel:** `python -m sia.reporter --out dados.xlsx --sql res/sql/extrair_itens.sql`
* **TSV (Texto):** `python -m sia.app.reporter --out export.txt --sql "SELECT * FROM notas"`

## 2. Configuração Centralizada (`var/db_config.toml`)

O `reporter.py` depende das definições carregadas em `env.db_config` pelo módulo `core.py`, que lê os bancos de dados definidos em `var/db_config.toml`. Esse arquivo TOML deve seguir esta estrutura:

```toml
# Banco de dados principal da auditoria
db = "data/entrada/principal.sqlite"

# Bancos de dados adicionais para cruzamento (ATTACH)
[[attach]]
path = "data/entrada/sped_fiscal.sqlite"
alias = "sped"

[[attach]]
path = "data/entrada/contabilidade.sqlite"
alias = "contabil"

```

* **db**: Define o banco de dados primário (`main`).
* **attach**: Lista de tabelas/objetos contendo `path` (caminho relativo à raiz) e `alias` (nome usado no SQL para referenciar o banco).

## 3. Exportadores e Formatação

O sistema segue a filosofia **"Text-First"**, priorizando formatos abertos e legíveis.

### Markdown (`to_markdown.py`)

* **Streaming:** Otimizado para memória, processando linha a linha (cursor) sem carregar todo o banco na RAM.
* **Auto-Documentação:** Inclui um bloco `<details>` contendo a query SQL original para fins de auditabilidade.
* **Alinhamento Inteligente:** Alinha colunas numéricas à direita e colunas de texto à esquerda automaticamente.
* **Estilo BR:** Formata números com separador de milhar (ponto) e decimal (vírgula), além de destacar valores negativos em vermelho via HTML.

### Excel (`to_excel.py`)

* Gera arquivos `.xlsx` a partir do cursor SQL.

### TSV / TXT

* Gera arquivos separados por tabulação com tratamento para decimais no padrão brasileiro (vírgula).

## 4. Regras de Desenvolvimento (Reports)

1. **Caminhos Relativos:** Todos os caminhos (SQL, Bancos, Saída) são resolvidos a partir da raiz do projeto (`env.project_root`).
2. **Imutabilidade:** O reporter opera apenas em leitura; nunca altere dados de origem.
3. **UTF-8:** Operações de arquivo devem forçar explicitamente `encoding='utf-8'`.
