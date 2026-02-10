# SKILL.md - SIA (Sistema de Auditoria SQL Portátil)

## 1. Arquitetura do Projeto
- **Tipo:** Aplicação Desktop Portátil (Windows).
- **Linguagem:** Python 3.13+ (Embedded Distribution).
- **Estrutura de Pastas:**
  - `/root`: Scripts de inicialização (`terminal.bat`).
  - `/usr`: Binários e Python Embed (NÃO versionado, gerado via `setup_python_embedded.bat`).
  - `/app`: Código fonte do projeto (MVC).
  - `/data`: Arquivos de dados (JSON, SQLite) manipulados pelo usuário.

## 2. Regras de Ambiente (CRÍTICO)
- **NÃO use venv/virtualenv:** O ambiente é isolado via arquivo `._pth`.
- **Imports:** A pasta `app/` já está no `sys.path`. Importe módulos como `import utils.info` ou `from modules.audit import core`.
- **Instalação de Libs:** Use sempre `python\python.exe -m pip install ...` via terminal portátil, ou o script de automação.
- **Paths:** Use caminhos relativos baseados em `os.path.dirname(__file__)` para portabilidade total.

## 3. Padrões de Código
- **Type Hinting:** Obrigatório em todas as assinaturas de função (Python 3.13).
- **Tratamento de Erros:** Logs devem ser salvos em arquivo local, pois o usuário final pode não ver o console.
- **UI:** (Definir aqui se usará TUI, Flet, TKinter ou Webview).