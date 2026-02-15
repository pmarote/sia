---
name: sia.main
description: Skill MESTRA do Projeto SIA. Define a arquitetura central, estrutura de pastas e regras globais de desenvolvimento. LEIA ESTE SKILL PRIMEIRO antes de iniciar qualquer tarefa.
---

# SIA - Core Architecture & Routing

## 1. O que é o SIA?

O **SIA** é um Sistema de Auditoria Fiscal modular focado em produtividade e transparência.

* **Filosofia:** "Text-First" (Interface via Terminal), Reprodutibilidade total e Imutabilidade dos dados de entrada.
* **Stack:** Python 3.13+ (Embedded), `uv` (Package Manager), SQLite.
* **Namespace:** O projeto utiliza o pacote raiz `sia` para evitar colisões de nomes.
* **UI:** Apenas Terminal (via biblioteca `rich`). **Proibido** uso de GUI nativa.

## 2. Mapa de Habilidades (Skill Routing)

Para tarefas específicas, consulte as Skills especializadas. Use sempre o namespace `sia.<modulo>`:

| Domínio | Skill Namespace | Quando usar? |
| --- | --- | --- |
| **Ambiente & Pacotes** | `setup.python-embedded` | Configurar interpretador, caminhos (`._pth`) ou gerenciar dependências com `uv`. |
| **Relatórios & Saída** | `sia.report` | Gerar Markdown, Excel ou TSV via `sia.reporter`. |
| **Utilitários & Tools** | `sia.util` | Diagnósticos (`sia.utils.info`), dumps de código ou listagem de ferramentas. |
| **Arquitetura Geral** | `sia.main` (Aqui) | Regras de ouro, estrutura de pastas e padrões globais de código. |

## 3. Estrutura de Diretórios

O projeto segue um padrão estrito para garantir portabilidade:

- **`/usr`** 🐍 (System): Python Embedded e dependências.
- **`/sia`** 🧠 (Package): Código fonte consolidado (Namespace principal).
  - `sia/core.py`: O guardião do ambiente (SST).
- **`/var`** 📝 (Dados Variáveis):
  - `/var/logs`: Logs de execução.
  - `/var/temp`: Cache e temporários.
  - `var/db_config.toml`: Configuração central de bancos.
- **`/res`** 📦 (Recursos Estáticos):
  - `/res/cookbooks`: Receitas de auditoria.
  - `/res/sql`: Scripts SQL puros.
  -  `/res/docs`: Documentação gerada e contexto.
- **`/data`** 💾 (Dados do Usuário): Entrada (Read-Only) e Saída de relatórios.

## 4. Regras de Ouro (Engenharia)

### A. Caminhos e Filesystem

* **Pathlib Only:** Use estritamente `pathlib.Path`.
* **Raiz do Projeto:** Todos os caminhos devem ser resolvidos via `env.project_root` definido no `sia.core`.

### B. Padrões de Código

* **Type Hinting:** Obrigatório em 100% das funções e métodos.
* **Namespace:** Nunca crie módulos na raiz. Use sempre a estrutura dentro da pasta `sia/`.
* **Invocação:** O padrão de execução é `python -m sia.<subpasta>.<modulo>`.
* **Encoding:** Sempre force `encoding='utf-8'` em operações de arquivo.