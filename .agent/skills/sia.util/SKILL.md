---
name: sia.util
description: Ferramentas de diagnóstico, introspecção e geração de contexto para IA. Use esta skill para validar o ambiente, listar ferramentas disponíveis ou gerar dumps de código.
---

# SIA Utilities & Diagnostics

O pacote `app.utils` contém ferramentas essenciais para manutenção, debug e documentação automática do sistema. Estas ferramentas são projetadas para serem robustas e funcionar mesmo quando o restante do sistema (banco de dados, relatórios) apresentar falhas.

## 1. Ferramentas Disponíveis

### A. Diagnóstico de Ambiente (`info.py`)
Valida o estado crítico do Python Embedded. Use-o quando houver erros de `ModuleNotFoundError` ou dúvidas sobre qual interpretador está rodando.

* **Comando:** `python -m app.utils.info`
* **O que ele faz:**
    * Exibe `sys.executable` e `sys.path`.
    * Lê e exibe o conteúdo do arquivo de configuração `._pth`.
    * Verifica se as pastas críticas (`app`, `usr`) estão visíveis.

> **Nota Técnica (Embedded):** O Python Embedded no Windows usa um arquivo `pythonXY._pth` para isolar o ambiente. Ele **ignora** variáveis de sistema como `PYTHONPATH`. O `info.py` confirma se o arquivo `._pth` está configurado corretamente para incluir `../../app`.

### B. Contexto para IA (`dump_code.py`)
Gera um arquivo Markdown consolidado contendo todo o código-fonte do projeto. Essencial para alimentar LLMs com o contexto atualizado do sistema.

* **Comando:**
    ```powershell
    python -m app.utils.dump_code --root . --dst res/docs/context_dump.md
    ```
* **Features:**
    * Respeita automaticamente exclusões de pastas binárias (`usr/`, `.git/`, `__pycache__`).
    * Formata o código em blocos Markdown com o caminho do arquivo no cabeçalho.

### C. Catálogo de Ferramentas (`list_tools.py`)
Ferramenta de introspecção que varre o pacote `app.utils` (ou outros) e lista os scripts disponíveis, extraindo suas docstrings e argumentos de CLI.

* **Comando:** `python -m app.utils.list_tools --root app/utils`
* **Saída:** Exibe um "Catálogo Inteligente" com descrição e modo de uso de cada script.

## 2. Padrões de Desenvolvimento (Utils)

Ao criar novos utilitários em `app.utils`, siga estritamente:

1.  **Independência:** Utilitários não devem depender de módulos pesados do sistema (como `app.reporter` ou `pandas`) a menos que estritamente necessário. Eles devem carregar rápido.
2.  **Type Hinting:** Obrigatório em todas as assinaturas (Python 3.13+).
3.  **Portabilidade (Caminhos Relativos):**
    * Como o sistema roda em pendrives, **nunca** use caminhos absolutos.
    * Use `pathlib.Path(__file__).parents[n]` para localizar recursos.

## 3. Exemplo de Uso (Diagnóstico)

Se o Agente ou o Usuário suspeitar de problemas no ambiente:

1.  Execute: `python -m app.utils.info`
2.  Verifique se o caminho do projeto aparece na lista `sys.path`.
3.  Se não aparecer, o problema está no arquivo `usr/python/python*._pth`.