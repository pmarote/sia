# 🧠 SIA — Sistema Integrado de Auditoria Fiscal
> **Versão:** 0.3.7 (02_2026)  
> **Arquitetura:** Python Portátil (Embedded) para Windows

## 📋 Visão Geral
O **SIA** é um sistema modular de auditoria fiscal projetado para automatizar o ciclo de vida dos dados de auditoria, desde a ingestão de bases brutas até a geração de relatórios sofisticados e auditáveis. O foco está na **produtividade, transparência e reprodutibilidade**, operando sem dependências globais no sistema.

### 📌 Objetivo
Transformar bancos SQLite brutos em relatórios consistentes e auditáveis usando apenas **Python + Markdown + SQL**.

---

## 🏗️ Estrutura Técnica (Baseada no Código)

O SIA utiliza uma distribuição **Python Embedded (3.13)** rica em portabilidade, garantindo que o sistema funcione em qualquer ambiente Windows sem instalação prévia.

### 🌳 Arquitetura de Pastas
- `/app`: Núcleo do sistema (MVC/Processamento).
- `/usr`: Binários do Python e ambiente isolado (não versionado).
- `terminal.bat`: Ponto de entrada para operações manuais e diagnóstico.
- `SKILL.md`: Documentação de padrões de desenvolvimento para agentes de IA e desenvolvedores.

### ⚙️ Regras de Execução e Ambiente
O sistema ignora o `PYTHONPATH` global para evitar conflitos. A raiz de importação é a pasta `/app`, configurada via arquivo `._pth`.

**Comando Padrão:**
```powershell
usr\python\python.exe -m <subpasta>.<modulo>
```
*Exemplo: `usr\python\python.exe -m utils.info`*

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

---

## 🛠️ Como Usar: Reporter (`app.reporter`)

O módulo `reporter` é o coração da extração de dados. Ele permite executar consultas SQL e salvar os resultados em diferentes formatos.

### ⌨️ Modo CLI (Linha de Comando)
Ideal para consultas rápidas e diretas:
```powershell
usr\python\python.exe -m reporter --db banco.sqlite --sql "SELECT * FROM auditoria" --format excel --out relatorio.xlsx
```

### 📄 Modo JSON (Configuração Especializada)
Ideal para tarefas complexas, permitindo anexar múltiplos bancos (ATTACH):
```powershell
usr\python\python.exe -m reporter --json config.json
```

**Exemplo de `config.json`:**
```json
{
  "db": "database/principal.sqlite",
  "out": "out/resultado.md",
  "format": "markdown",
  "sql": "SELECT p.nome, a.valor FROM principal.usuarios p JOIN extra.auditoria a ON p.id = a.user_id",
  "attach": [
    { "path": "database/extra_data.sqlite", "alias": "extra" }
  ]
}
```

---

## 🛠️ Ferramentas Utilitárias
*   **Dump Code (`app/utils/dump_code.py`):** Gera um arquivo Markdown consolidado com todo o código fonte (respeitando regras de exclusão de pastas como `usr/` e `.git/`). Ideal para fornecer contexto a sistemas de IA.
*   **Info Python (`app/utils/info.py`):** Ferramenta de diagnóstico para validar o estado do ambiente embedded, caminhos de importação e conectividade.

---

## 📐 Padrões de Projeto
*   **Type Hinting:** Obrigatório em todas as assinaturas (Python 3.13).
*   **Arquitetura Limpa:** Separação entre lógica de auditoria (SQL/Cookbooks) e motores de geração de relatórios.
*   **Portabilidade:** Uso estrito de caminhos relativos para garantir execução a partir de pendrives ou redes compartilhadas.

---
*Documentação gerada automaticamente baseada na estrutura do projeto e diretrizes de negócio.*
