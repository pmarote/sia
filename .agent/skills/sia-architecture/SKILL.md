# SKILL.md - SIA Architecture & Standards

## 1. Visão Geral e Arquitetura
- **Propósito:** Sistema de Auditoria Fiscal e Análise de Dados.
- **Filosofia:** "Text-First", Reprodutibilidade, Imutabilidade dos Dados de Entrada.
- **Stack:** Python 3.13+ (Embedded), `uv` (Package Manager), SQLite (Engine).
- **Tipo:** Aplicação Desktop Portátil (Windows) / CLI First.

## 2. Estrutura de Diretórios (File System)
A estrutura segue o padrão Unix-like adaptado para portabilidade:

- **`/usr`** 🐍 (System Binaries)
  - Contém o Python Embedded e dependências instaladas via `uv`.
  - *Gerenciado estritamente pela skill: `python-embedded`.*

- **`/app`** 🧠 (Source Code)
  - O núcleo da lógica de negócio (MVC).

- **`/var`** 📝 (Variable Data)
  - `/var/logs`: Logs de execução (Sempre no plural).
  - `/var/temp`: Arquivos temporários (cache, dumps voláteis).

- **`/res`** 📦 (Resources & Static Assets)
  - `/res/assets`: Arquivos estáticos para compor relatórios.
    - `/res/assets/img`: Logos, assinaturas digitais, ícones para Markdown/HTML.
    - `/res/assets/styles`: CSS ou scripts para relatórios HTML.
  - `/res/cookbooks`: Receitas de automação e regras de negócio (`.ckb`).
  - `/res/sql`: Queries e scripts SQL puros (Singular).
  - `/res/templates`: Modelos Jinja2, esqueletos Markdown ou Excel base.
  - `/res/docs`: Documentação técnica do sistema.

- **`/data`** 💾 (User Data)
  - Área de *Input* (leitura) e *Output* (escrita) do usuário.

- **`.vscode`** ⚙️ (IDE Config)
  - Injeção de ambiente nativa. (Scripts `.bat` legados podem existir na raiz apenas como fallback).

## 3. Regras de Engenharia de Software

### A. Caminhos e Sistema de Arquivos
- **Pathlib First:** Use sempre `pathlib.Path` em vez de strings ou `os.path`.
  - ✅ `BASE_DIR = pathlib.Path(__file__).parents[1]`
  - ❌ `BASE_DIR = os.path.dirname(...)`
- **Caminhos Relativos:** O código deve ser agnóstico à letra do drive (`C:` ou `D:`). Tudo é relativo à raiz do projeto.

### B. Manipulação de Dados (Auditoria)
- **Imutabilidade:** Arquivos de entrada em `/data` (ex: SPED, CSVs, Bancos originais) devem ser tratados como **Read-Only**.
- **Idempotência:** Rodar a mesma análise duas vezes deve produzir o mesmo resultado (ou substituir o output de forma limpa).

### C. Padrões de Código
- **Type Hinting:** Estritamente obrigatório. Use `typing.Optional`, `list[str]`, etc.
- **Encoding:** Sempre explicitar `encoding='utf-8'` ao abrir arquivos de texto/json/markdown.
- **Logging:** Use `app.reporter` ou `logging`. Nunca use `print()` para informações críticas, pois elas se perdem se o terminal fechar.

### D. Interface (UI/UX)
- **Console Rico:** Utilize a biblioteca `rich` para tabelas, progress bars e formatação no terminal.
- **Zero GUI:** Não utilize `tkinter`, `Qt` ou similares. A interface é o Terminal ou os Relatórios gerados.

## 4. Integração com Agente
- **Instalação de Pacotes:** Consulte a skill **`python-embedded`**.
- **Geração de Relatórios:** Ao criar relatórios Markdown, busque imagens e estilos em `/res/assets`.