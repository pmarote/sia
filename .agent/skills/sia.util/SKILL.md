---
name: sia.util
description: Ferramentas de diagnóstico, introspecção e geração de contexto para IA. Use esta skill para validar o ambiente, listar ferramentas disponíveis ou gerar dumps de código.
---

# SIA Utilities & Diagnostics

O pacote `sia.utils` contém ferramentas essenciais para manutenção, debug e documentação automática do sistema. Estas ferramentas são projetadas para serem robustas e funcionar mesmo quando o restante do sistema (banco de dados, relatórios) apresentar falhas.

## 1. Ferramentas Disponíveis

### A. Diagnóstico de Ambiente (`info.py`)

Valida o estado crítico do Python Embedded e a saúde da infraestrutura baseada no módulo `core`.

* **Comando:** `python -m sia.utils.info`
* **O que ele faz:**
* Exibe `sys.executable`, `sys.path` e o IP local da rede.
* Verifica a disponibilidade e versão do gerenciador de pacotes **`uv`**.
* Valida caminhos críticos (`var`, `logs`, `temp`) e a configuração do banco de dados via `sia.core`.
* Analisa o arquivo `._pth` para confirmar as injeções de path (`sia`) e o `import site`.

### B. Contexto para IA (`dump_code.py`)

Gera um arquivo Markdown consolidado contendo o código-fonte e estrutura do projeto para alimentar LLMs.

* **Comando:**
```powershell
python -m sia.utils.dump_code --root . --context_dump.md

```

* **Features:**
* **Exclusão Inteligente:** Ignora automaticamente pastas de sistema, git, IDEs e builds (`.git`, `usr`, `.vscode`, `dist`, etc.).
* **Filtro de Extensões:** Coleta arquivos `.py`, `.md`, `.bat`, `.json` e `.sql`.
* **Árvore de Diretórios:** Inclui uma representação visual da estrutura de pastas no topo do arquivo.

### C. Catálogo de Ferramentas (`list_tools.py`)

Varre um diretório para listar scripts, diferenciando ferramentas de CLI de scripts comuns.

* **Comando:** `python -m sia.utils.list_tools --root %SIA_ROOT_DIR%/sia/utils`
* **Saída:**
* Identifica **🛠️ TOOL** (usa `argparse`) ou **📄 SCRIPT** (usa docstrings).
* Para ferramentas CLI, executa automaticamente o parâmetro `-h` para extrair as instruções de uso.

## 2. Padrões de Desenvolvimento (Utils)

Ao criar novos utilitários em `sia.utils`, siga estritamente:

1.  **Independência:** Utilitários não devem depender de módulos pesados do sistema (como `sia.reporter` ou `pandas`) a menos que estritamente necessário. Eles devem carregar rápido.
2.  **Type Hinting:** Obrigatório em todas as assinaturas (Python 3.13+).
3.  **Portabilidade (Caminhos Relativos):**
    * Como o sistema roda em pendrives, **nunca** use caminhos absolutos.
    * Use `pathlib.Path(__file__).parents[n]` para localizar recursos.

## 3. Exemplo de Uso (Diagnóstico)

Se o Agente ou o Usuário suspeitar de problemas no ambiente:

1.  Execute: `python -m sia.utils.info`
2.  Verifique se o caminho do projeto aparece na lista `sys.path`.
3.  Se não aparecer, o problema está no arquivo `usr/python/python*._pth`.