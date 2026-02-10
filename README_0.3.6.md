# ARQUITETURA DE MICROAPPS PARA AUDITORIA (v0.3.4)

## 1. Visão Geral e Filosofia
Este projeto utiliza uma arquitetura de **Microapps Independentes** orquestrados por um Maestro (SIA), focada em **Vibe Coding** (desenvolvimento assistido por IA) e operação local em Windows.

### Princípios Fundamentais (The "No-API" Manifesto)
1.  **Independência Total:** Cada microapp possui seu próprio interpretador Python (Embedded), suas próprias dependências e não sabe da existência dos outros.
2.  **Comunicação via Sistema de Arquivos:** Não existe TCP/IP, HTTP ou APIs. A troca de dados é feita persistindo arquivos em disco (SQLite, Excel, Logs).
3.  **Interface Universal (.bat):** O mundo exterior não chama o Python diretamente. Chama scripts de lote (`run.bat`) que configuram o ambiente isolado.
4.  **Pipeline ELT:** Priorizamos Extrair e Carregar para SQLite primeiro, para transformar/auditar depois.
5.  **Encoding Robusto:** Todo Entry Point força `PYTHONUTF8=1` para garantir suporte a emojis e acentos no console Windows.

> **Por que ELT para Auditoria?**
> 1. **Extract:** Tira do Firebird/Fonte Externa.
> 2. **Load:** Carrega para o "Data Lake" local (SQLite), preservando dados brutos.
> 3. **Transform:** Scripts rodam *em cima* desse SQLite para gerar relatórios.
> *Vantagem:* Se a regra muda, reprocessa-se o SQLite local (rápido) sem precisar reconectar no cliente (lento).

---

## 2. Estrutura Global de Diretórios
A raiz do projeto é `C:\srcP\py`.

```text
C:\srcP\py\
│
├── app_base\          # [TEMPLATE] A semente. Python Embedded limpo + estrutura padrão.
│                      # Todo novo app começa duplicando esta pasta. **Nunca altere arquivos aqui manualmente.**
│
├── sia\               # [MAESTRO] GUI (FreeSimpleGUI).
│                      # Orquestra os microapps, gerencia configs e exibe logs.
│
├── utils\             # [FERRAMENTAS] Microapp funcional de referência.
│   ├── src\           # dump_code.py, info.py, list_tools.py.
│   ├── usr\           # Python Embedded.
│   ├── run.bat        # Entry Point para Automação.
│   └── terminal.bat   # Entry Point para Humanos.
│
├── reporter\          # [SAÍDA] Microapp Especialista em gerar Excel/Markdown.
│   ├── src\           # main.py (Router), to_excel.py, to_markdown.py.
│   └── ...            # "Lightweight": Não usa Pandas, apenas Openpyxl e Python Puro.
│
├── pr\                # [ENGINE] Pipeline Runner Executa "Cookbooks" (Pipelines em Markdown)
│   ├── src\           # Lê .md, executa blocos ```python e chama o reporter para ```sql.
│   └── ...
│
└── extractor\         # [ENTRADA] (Futuro) Focado em ler fontes (Firebird, CSV) -> SQLite.

```

---

## 3. Anatomia de um Microapp (O Padrão Ouro)

Para garantir que a IA consiga manter o código e que o isolamento funcione, **todo microapp** deve seguir rigorosamente esta estrutura interna:

### 3.1. Pastas Internas

* **`src/`**: Onde vivem os scripts `.py`. (Ex: `main.py`, `core.py`).
* **`usr/`**: Onde vive o motor. Contém a pasta `python` (o interpretador embedded) e `tcl_tk` (se houver GUI). **Nunca altere arquivos aqui manualmente.**
* **`var/`**: Área para arquivos temporários, logs locais ou configs (`settings.json`).

### 3.2. Os "Entry Points" (Pontos de Entrada)

Existem três formas de interagir, cada uma com um propósito:

#### A. `terminal.bat` (Modo Humano)

* **Função:** Abre um terminal preto (CMD) configurado.
* **Uso:** Instalar libs (`pip install`), rodar testes manuais.
* **Comportamento:** Mantém a janela aberta (`cmd /k`).

#### B. `run.bat` (Modo Robô/Maestro)

* **Função:** Wrapper silencioso para automação.
* **Uso:** Chamado pelo SIA ou scripts `subprocess`.
* **Comportamento:** Recebe argumentos: `run.bat src/script.py --arg valor` -> Configura ambiente -> Executa comando -> Retorna Exit Code -> Fecha.

#### C. `SIA.bat` (Modo Launcher GUI)

* **Uso:** Apenas para o app `sia`.
* **Comportamento:** Usa `start "" pythonw.exe` para lançar a interface gráfica sem deixar telas pretas de console abertas.


### 3.3. Exemplificando

Abra o seu CMD do Windows normal (fora do ambiente) e navegue até a pasta `utils`.

**Teste 1: Gerar o dump usando o `run.bat`**

```cmd
run.bat src/dump_code.py --root . --dst teste_via_run.md

```

*O que acontece:* Ele configura o Python silenciosamente, roda o script, gera o arquivo e devolve o controle para o terminal.

**Teste 2: Ver a versão do Python**

```cmd
run.bat --version

```

*O que acontece:* Ele cospe `Python 3.x.x` e termina.

**Teste 3: O Maestro chamando (Exemplo mental)**
No futuro, seu app SIA (feito em Python ou C# ou Delphi) vai fazer isso:

```python
# Código do MAESTRO (SIA)
subprocess.run([
    "C:/srcP/py/utils/run.bat",  # Chama o Wrapper
    "src/dump_code.py",          # O Script Python
    "--root", "../app_cliente",  # Argumento 1
    "--dst", "log.md"            # Argumento 2
], check=True)

```

Isso torna os microapps **universais**. Qualquer coisa que saiba rodar um `.bat` consegue usar suas ferramentas de IA agora.

---

## 4. O Contrato de Comunicação

### 4.1. Inputs (Entrada)

Os scripts Python em `src` devem usar `argparse`.

```python
parser.add_argument("--db", required=True, help="Caminho do SQLite")
parser.add_argument("--out", required=True, help="Caminho do arquivo final")

```

### 4.2. Outputs (Saída e Controle)

* **Exit Code 0:** Sucesso.
* **Exit Code 1:** Erro.
* **Logs:** O SIA captura o `stdout`. Use prints informativos: `print("[INFO] Processando...")` `print("[INFO] Lendo arquivo...")` `print("[ERRO] Arquivo corrompido")`.

---

## 5. Fluxo de Trabalho (Pipeline)

1. **RAW (Extração):** `extractor` lê Fonte Externa -> Grava em `projeto.sqlite`.
2. **TRUSTED (Engine):** `pr` (pr = pipeline runner) lê um **Cookbook (.md)** -> Executa Python/SQL -> Gera Relatório Markdown processado.
3. **REFINED (Reporter):** `reporter` é chamado pelo Engine ou SIA para materializar tabelas em Excel/Markdown.

---

## 6. Guia para "Vibe Coding" (Prompt Engineering)

Ao pedir para a IA criar ou manter um microapp, copie e cole este bloco de contexto:

> **CONTEXTO DO PROJETO (Microapps Windows/Python Embedded):**
> 1. **Estrutura:** O script roda dentro de `src/`. O interpretador está em `usr/python/`.
> 2. **Entry Points:** O script será chamado via `run.bat` (automação) ou `terminal.bat` (debug). Não assuma Python global.
> 3. **Inputs:** Use `argparse` para receber caminhos de arquivos (DBs, configs).
> 4. **Outputs:** Use `sys.exit(0)` para sucesso e `sys.exit(1)` para falha. Prints são logs.
> 5. **Encoding:** O ambiente força `PYTHONUTF8=1`. Pode usar emojis e acentos.
> 6. **Dependências:** Prefira **Python Puro** ou libs leves (`openpyxl`, `sqlite3`). Evite Pandas a menos que estritamente necessário (tamanho e performance).
> 7. **No-Install:** Não tente usar `venv`. Use as libs já instaladas em `usr` ou peça para eu rodar o `pip install` no `terminal.bat`.

---

## 7. Catálogo de Microapps

### 🎛️ sia (Maestro)

Interface Gráfica (FreeSimpleGUI) que centraliza a operação.

* **Features:** Console de Logs em tempo real, persistência de diretório de trabalho (`sia.settings.json`), lança processos via `subprocess` sem travar a UI.

### 🛠️ utils (Ferramentas)

* `src/list_tools.py`: Varre uma pasta e gera um catálogo automático das ferramentas (lendo Docstrings e help CLI).Script de diagnóstico que verifica IP, versão do Python, PIP e status de bibliotecas gráficas (Tkinter/FreeSimpleGUI). **Comando:** `run.bat src/info.py`
* `src/dump_code.py`: Gera um Markdown com a árvore de arquivos e o conteúdo do código para dar contexto à IA. **Comando:** `run.bat src/dump_code.py --root . --dst contexto.md`
* `src/info.py`: Diagnóstico de ambiente.

Localizado em `C:\srcP\py\utils`.

### 📊 reporter (Saída)

Microapp otimizado (sem Pandas) para exportação.

* `src/main.py`: Roteador. Gera TSV nativo ou delega.
* `src/to_excel.py`: Gera Excel com `openpyxl`. Formata cabeçalhos, congela painéis e tipa números corretamente.
* `src/to_markdown.py`: Gera Markdown com HTML injetado (vermelho para negativos), badges de metadados e SQL colapsável (`<details>`).

### ⚙️ pr (Pipeline Runner - Processador)

O "Jupyter Notebook" em texto puro. Aqui tem a biblioteca Pandas, para fazer análises mais complexas.

* **Entrada:** Um arquivo Markdown "Cookbook" contendo texto, blocos ````python` e ````sql`.
* **Processo:** Executa Python (mantendo estado de variáveis), chama o `reporter` para processar SQL.
* **Saída:** Um novo Markdown com os resultados injetados.


---

## Histórico de Versões
- **v0.3.2:** Estrutura base de microapps e contratos de entrada/saída.
- **v0.3.3:** Ferramentas de diagnóstico, melhorias no template e configuração de arquivos .vscode para antigravity.
- **v0.3.4:** Desenvolvimento direto no Gemini, sem antigravity. A impressão que tenho é que o Gemini, direto, trabalhando separadamente em cada microapp, tem sido mais produtivo. O antigravity dá muitos erros, porque trabalha com o projeto como um todo e, ao que parece, ele não lida bem com esse monte de python embedded diferente para cada pasta.

### Novidades da v0.3.4
1.  Foco em produção, trabalhando cada microapp separadamente no Gemini.

### Novidades da v0.3.3
1.  **Check-Health:** Novo utilitário em `utils/src/check_health.py` para validar a integridade dos microapps.
2.  **Template core.py:** `app_base/src/core.py` agora inclui exemplos de boas práticas para `argparse` e `sys.exit`.
3.  **Refinamento de Contexto:** Consolidação das diretrizes de "Vibe Coding".
