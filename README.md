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
python -m <subpasta>.<modulo>
```
ou
```powershell
sia <subpasta>.<modulo>
```

*Exemplos:*
*`sia utils.info`*
*`sia utils.list_tools --root app`*

---

## 🚀 Funcionalidades Principais

| Módulo | Descrição |
| :--- | :--- |
| **Ingestão** | Conversão de bases heterogêneas para SQLite. |
| **Cookbooks** | Geração de bancos derivados e transformações de dados. |
| **Relatórios** | Produção automática em Markdown, HTML, Excel e TXT. |
| **Documentação** | Ferramentas como o `dump_code.py` para autocontexto e documentação de bancos. |
| **Pipelines** | Encadeamento de tarefas de auditoria para execução sequencial. |
| **Gestão de Auditoria** | Cookbooks por contribuinte e complementos vinculados a seções de relatórios. |

