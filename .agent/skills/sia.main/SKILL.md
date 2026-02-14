---
name: sia.main
description: Skill MESTRA do Projeto SIA. Define a arquitetura central, estrutura de pastas e regras globais de desenvolvimento. LEIA ESTE SKILL PRIMEIRO antes de iniciar qualquer tarefa.
---

# SIA - Core Architecture & Routing

## 1. O que é o SIA?
O **SIA** é um Sistema de Auditoria Fiscal modular focado em produtividade e transparência.
- **Filosofia:** "Text-First" (Interface via Terminal), Reprodutibilidade total e Imutabilidade dos dados de entrada.
- **Stack:** Python 3.13+ (Embedded), `uv` (Package Manager), SQLite.
- **UI:** Apenas Terminal (via biblioteca `rich`). **Proibido** uso de GUI nativa (Tkinter, Qt, etc).

## 2. Mapa de Habilidades (Skill Routing)
Para tarefas específicas, consulte as Skills especializadas abaixo. Não tente adivinhar; use a skill correta:

| Domínio | Skill Namespace | Quando usar? |
| :--- | :--- | :--- |
| **Ambiente & Pacotes** | `setup.python-embedded` | Instalar libs (`uv`), configurar paths, erros de importação ou setup do interpretador. |
| **Relatórios & Saída** | `sia.report` | Gerar Markdown, HTML, Excel, manipular templates Jinja2 ou acessar `/res/assets`. |
| **Utilitários & Tools** | `sia.util` | Funções de log (`app.reporter`), manipulação de arquivos, strings ou diagnósticos. |
| **Arquitetura Geral** | `sia.main` (Aqui) | Dúvidas sobre onde salvar arquivos, regras de nomenclatura e padrões globais. |

## 3. Estrutura de Diretórios (Global)
O projeto segue um padrão Unix-like estrito:

- **`/usr`** 🐍 (System)
  - Python Embedded e dependências. *Gerenciado por `setup.python-embedded`.*
- **`/app`** 🧠 (Core)
  - Código fonte (MVC).
- **`/var`** 📝 (Dados Variáveis)
  - `/var/logs`: Logs de execução.
  - `/var/temp`: Cache e temporários.
- **`/res`** 📦 (Recursos Estáticos)
  - `/res/assets`: Imagens e estilos para relatórios (*ver `sia.report`*).
    - `/res/assets/img`: Logos, assinaturas digitais, ícones para Markdown/HTML.
    - `/res/assets/styles`: CSS ou scripts para relatórios HTML.
  - `/res/cookbooks`: Receitas de automação (`.ckb`).
  - `/res/sql`: Scripts SQL puros.
- **`/data`** 💾 (Dados do Usuário)
  - Entrada (Leitura) e Saída (Escrita).
  - `/res/templates`: Modelos Jinja2, esqueletos Markdown ou Excel base.
  - `/res/docs`: Documentação técnica do sistema.
- **`.vscode`** ⚙️ (IDE Config)
  - Injeção de ambiente nativa. (Scripts `.bat` legados podem existir na raiz apenas como fallback).

## 4. Regras de Ouro (Engenharia)

### A. Caminhos e Filesystem
- **Pathlib Only:** Use estritamente `pathlib.Path`. Evite `os.path` e strings puras para caminhos.
- **Raiz do Projeto:** Todos os caminhos devem ser relativos à raiz do projeto.
  - ✅ `ROOT_DIR = pathlib.Path(__file__).parents[n]`

### B. Integridade de Dados
- **Imutabilidade de Input:** Arquivos em `/data` (SPED, CSV, Bancos Originais) são **READ-ONLY**. Nunca sobrescreva um arquivo de entrada.
- **Idempotência:** Scripts devem poder rodar múltiplas vezes sem duplicar dados ou quebrar o estado.

### C. Padrões de Código
- **Type Hinting:** Obrigatório em 100% das funções.
- **Encoding:** Sempre force `encoding='utf-8'` em operações de arquivo.
- **Saída:** Use `app.reporter` ou `rich`. Nunca use `print()` nativo para informações críticas.
