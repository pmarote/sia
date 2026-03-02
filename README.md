# Projeto SIA - Sistema Integrado de Auditoria

Bem-vindo ao desenvolvimento do SIA.

## 🤖 Para o Agente (Google Antigravity)

A documentação técnica e as regras de desenvolvimento deste projeto estão organizadas em **Skills**.

**Por favor, inicie lendo a [SKILL MESTRA](.agent/skills/sia.main/SKILL.md):**
👉 **`.agent/skills/sia.main/SKILL.md`**

Ela irá guiá-lo sobre:
1. Como o ambiente Python Embedded funciona.
2. Onde encontrar regras para Relatórios e Utilitários.
3. A estrutura de pastas obrigatória.

---

> **Versão:** - Consulte [`pyproject.toml`](pyproject.toml) e histórico em [`CHANGELOG.md`](CHANGELOG.md)
> **Arquitetura:** Python Portátil (Embedded) para Windows

## 📋 Visão Geral
O **SIA** é um sistema modular de auditoria fiscal projetado para automatizar o ciclo de vida dos dados de auditoria, desde a ingestão de bases brutas até a geração de relatórios sofisticados e auditáveis. O foco está na **produtividade, transparência e reprodutibilidade**, operando sem dependências globais no sistema.

### 📌 Objetivo
Transformar bancos SQLite brutos em relatórios consistentes e auditáveis usando apenas **Python + Markdown + SQL**.

---

### ⚙️ Regras de Execução e Ambiente
O SIA utiliza uma distribuição **Python Embedded (3.13)** rica em portabilidade, garantindo que o sistema funcione em qualquer ambiente Windows sem instalação prévia.
O sistema ignora o `PYTHONPATH` global para evitar conflitos. A raiz de importação é a pasta `/app`, configurada via arquivo `._pth`.

**Abrir o terminal.bat. Após, o comando padrão é:**
```powershell
python -m sia.<subpasta>.<modulo>
```
ou
```powershell
s <subpasta>.<modulo>
```

*Exemplos:*
*`sia sia.utils.info`*
*`sia sia.utils.list_tools --root app`*

---

## 🚀 Funcionalidades Principais

| Módulo / Recurso | Descrição |
| :--- | :--- |
| **Ingestão e Setup** | Scripts como `prep_safic.py` preparam cópias de templates SQLite (`.db3`) de forma segura contra sobrescritas. |
| **Configuração Dinâmica** | Uso do `gen_db_config` para orquestrar a conexão principal e os `ATTACH` de bancos de dados via `var/db_config.toml`. |
| **Motor de Cookbooks** | O coração do relatório. O `sia.cookbook_parser` interpreta arquivos Markdown recheados de SQL, executando a lógica e substituindo o código pelas tabelas de resultados prontas. |
| **Relatórios Auditáveis** | Geração automática otimizada em Markdown, Excel e TSV, com queries auto-documentadas dentro de tags `<details>` (Auditabilidade transparente). |
| **Exploração de Dados** | Geração autônoma de cookbooks (`gen_cookbook.py`) para explorar a estrutura e fazer test-drive rápido em bancos desconhecidos. |
| **Documentação Local** | Ferramentas de diagnóstico nativas como `info.py`, `list_tools.py` e `dump_code.py` para mapeamento de arquitetura. |

---

### 🛠️ Primeiros Passos (Exemplo de Uso)

1. **Ative o ambiente:** Execute `terminal_sia_0.x.x.bat` para carregar o Python Embedded na memória sem sujar o SO.
2. **Prepare uma base de trabalho:**
```powershell
   python prep_safic.py
```

*(Este script inicializa um novo ambiente seguro copiando o modelo de dados de auditoria e configurando o `db_config.toml`).*
3. **Execute um Cookbook:**

```powershell
python -m sia.cookbook_parser --in res/cookbooks/ckb_basicos.md

```

O SIA lerá o Markdown, processará todo o SQL embutido e gerará o relatório final formatado na mesma pasta, pronto para leitura ou conversão em PDF.
