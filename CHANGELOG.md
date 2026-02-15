# Changelog

O formato é livre, focado em registrar decisões de arquitetura e evolução do projeto SIA, e é baseado em [Keep a Changelog](https://keepachangelog.com/en/2.0.0/) e [Semantic Versioning](https://semver.org/spec/v2.0.0.html), sem tantas rígidas restrições.

## [0.3.9] - 2026-02-15
- **Padronização de Namespace:** A pasta raiz `/app` foi renomeada para `/sia`. O projeto agora opera como um pacote Python consolidado, permitindo chamadas via `python -m sia.<modulo>` e evitando colisões com bibliotecas globais.
- **Refatoração do `sia/core.py`:** Atualizada a lógica de detecção de caminhos para suportar o novo namespace. Adicionado suporte ao objeto `AppEnv` para incluir o caminho do pacote (`sia_package`) e a pasta de recursos (`res_dir`).
- **Evolução dos Utilitários:**
- `info.py`: Agora valida a integridade do novo namespace e destaca visualmente a raiz do projeto no `sys.path`.
- `dump_code.py`: Atualizado para capturar arquivos `.toml` e ignorar automaticamente a pasta `/var` para dumps mais limpos.
- `list_tools.py`: Implementada lógica inteligente para extrair o *help* de módulos usando o novo padrão `python -m sia...`.
- **Refatoração do `sia/reporter.py` e Exportadores:** - Atualização de todos os *imports* internos para o namespace `sia`.
- Implementação de **Type Hinting** em 100% das funções de suporte (`to_markdown.py`, `to_excel.py`).
- **Documentação de Agente (Skills):** Atualização completa das definições em `.agent/skills/` para refletir a nova arquitetura e os parâmetros obrigatórios da v0.3.9.
- **Suporte a TOML:** Inclusão de arquivos de configuração `.toml` no contexto de análise de IA através do `dump_code.py`.

## [0.3.8] - 2026-02-14
- **Criação do `app/core.py` (Single Source of Truth):** Novo módulo guardião que valida a infraestrutura na inicialização, gerencia os caminhos absolutos (`project_root`, `/var`, `/logs`, `/temp`) e carrega as configurações. Possui "auto-healing" para criar pastas ausentes.
- **Refatoração Profunda do `app.reporter`:**
  - Código limpo: consome a infraestrutura já validada pelo `core.py` em vez de adivinhar caminhos.
  - Inteligência de CLI: Infere automaticamente o formato de saída (Markdown, Excel, TSV) pela extensão do arquivo de saída (`--out`).
  - Flexibilidade de SQL: O parâmetro `--sql` agora aceita tanto a query em string quanto o caminho para um arquivo `.sql`.
  - Configuração via TOML: Conexões de banco (`main` e `attach`) foram movidas da CLI para o arquivo persistente `var/db_config.toml` (usando `tomllib` nativo do Python 3.13).
- **Melhorias Visuais no Markdown (`to_markdown.py`):** Adicionado suporte ao argumento `--title` (renderizado como H2) e inclusão automática da query SQL original em um bloco HTML retrátil (`<details>`).
- **Dashboard de Diagnóstico (`info.py`):** Totalmente reescrito. Agora gera um relatório visual por blocos (`[SISTEMA]`, `[CORE]`, `[EMBED]`), avaliando a saúde das pastas vitais, rotas de importação e presença do motor `uv`.
- **Evolução dos Utilitários Base (`/usr`):**
  - O `setup_python_embedded.bat` agora documenta no próprio terminal a arquitetura do `._pth` e atualizou os "próximos passos" para usar o padrão `uv`.
  - Substituição do script genérico de limpeza pelo novo **`clean_cache.bat`**, que atua recursivamente destruindo `__pycache__` e limpando o `/var/temp`.
- **Organização de Agentes de IA:** Reestruturação do `SKILL.md` em namespaces focados (`sia.main`, `sia.report`, `sia.util`, `setup.python-embedded`) para melhor roteamento cognitivo do IDE.
- **Fix Global:** Centralização do `sys.stdout.reconfigure(encoding='utf-8')` no `core.py` para prevenir falhas de acentuação no terminal do Windows em todos os scripts.

## [0.3.7] - 2026-02-13
- Configuração do gerenciador de pacotes `uv` para orquestrar dependências.
- Criação do `SKILL.md` (`python-embedded`) para ensinar o Agente a usar o ambiente `usr/python` corretamente e não criar venvs isolados.
- Configurações de `launch.json` e `settings.json` para injeção nativa de variáveis de ambiente no terminal do VS Code.

## [0.3.6] - 2026-02-13
- **Decisão:** Retorno ao uso do **Google Antigravity** como IDE principal.
- Reestruturação do módulo `app.reporter` (funcionalidade restaurada).
- Reinício da migração de lógica para o conceito de "cookbooks".

## [0.3.5] - 2026-02-10
- **Mudança Arquitetural Crítica:** Consolidação do ambiente Python. Agora existe apenas uma pasta `usr` centralizada, eliminando múltiplos ambientes embedded espalhados.
- Fim da estrutura de múltiplos microapps com ambientes isolados. Em outras palavras, desisti do conceito da estrutura base de **microapps**.
- Simplificação da estrutura de pastas para facilitar o reconhecimento pelo Agente.
- **Remoção:** O suporte a `tcl_tk` foi removido. O projeto agora é "Text-First". Interfaces gráficas futuras serão bibliotecas externas, que acionam o projeto/biblioteca sia.

## [0.3.4] - 2026-02-01
- Migração temporária do fluxo de trabalho para o **Gemini Web** (fora do IDE).
- Foco no desenvolvimento isolado de microapps devido a conflitos com múltiplos ambientes Python embedded no Antigravity.

## [0.3.3] - 2026-01-13

### Added
- Ferramentas de diagnóstico de ambiente.
- Suporte temporário às ferramentas integradas do Antigravity (devido a instabilidade com a arquitetura anterior).
- Arquivos de configuração `.vscode` iniciais para o Antigravity.

### Changed
- Melhorias no template base dos microapps.

## [0.3.2] - 2026-01-01
### Added
- Estrutura base de **microapps**.
- Definição dos contratos de Entrada/Saída (Input/Output protocols).