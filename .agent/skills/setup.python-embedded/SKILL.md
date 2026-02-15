---
name: python-embedded
description: Gerencia o ambiente Python Portátil (Embedded) e instalação de pacotes via uv. Use esta skill sempre que precisar executar scripts, instalar dependências ou configurar o ambiente do projeto SIA.
---

# Python Embedded & UV Package Manager

Este projeto utiliza uma arquitetura **Python Embedded** (Portátil) localizada estritamente em `usr/python`. NÃO existe ambiente virtual padrão (`.venv`) e NÃO se deve usar o Python global do sistema.

## 1. Regras de Ambiente
- **Interpretador:** O único interpretador válido é `${workspaceFolder}/usr/python/python.exe`.
- **VS Code:** O ambiente já é injetado automaticamente nos terminais via `.vscode/settings.json`.
- **Caminhos:** Se for necessário referenciar o python explicitamente, use sempre caminhos relativos: `usr/python/python.exe`.

## 2. Instalação de Pacotes (UV + PIP)
O gerenciador de pacotes é o **uv**, mas ele deve ser usado em modo "pip" direcionado ao ambiente portátil.

### Como instalar pacotes (Adicionar dependência)
Para instalar uma nova biblioteca (ex: pandas), siga estritamente esta ordem:

1. **Instale no ambiente portátil:**
   Execute: `uv pip install pandas --python usr/python/python.exe`
   *(Nota: O flag `--python` é OBRIGATÓRIO para não criar um .venv isolado)*

2. **Registre no projeto (pyproject.toml):**
   Adicione o nome do pacote manualmente ao arquivo `pyproject.toml` na seção `dependencies`.

3. **Atualize o Lockfile:**
   Execute: `uv lock`
   *(Isso sincroniza a árvore de dependências do projeto com o que foi instalado)*

### Como listar pacotes
- Para ver o que está instalado no disco: `uv pip list --python usr/python/python.exe`
- Para ver a árvore do projeto: `uv tree`

## 3. Execução de Scripts
Sempre execute scripts assumindo que o terminal já tem as variáveis de ambiente carregadas (graças ao VS Code).
- **Correto:** `python -m sia.main`
- **Correto:** `python script.py`
- **Fallback (se der erro de comando):** `usr/python/python.exe -m app.main`

## 4. Setup Inicial (Onboarding)
Se o ambiente precisar ser recomposto ou verificado:

1. Verifique se `usr/python/python.exe` existe.
2. Se `pyproject.toml` existir mas o ambiente estiver vazio, instale tudo de uma vez:
   `uv pip sync pyproject.toml --python usr/python/python.exe`

---
**Erros Comuns a Evitar:**
- ❌ NUNCA rode `uv add <pacote>` sem configurar `UV_PROJECT_ENVIRONMENT`, pois isso cria um `.venv` separado.
- ❌ NUNCA rode `pip install` direto (use `uv pip install`).
- ❌ NUNCA sugira criar um venv (`python -m venv`). O `usr/python` É o ambiente.