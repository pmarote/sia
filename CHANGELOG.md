# Changelog

O formato é livre, focado em registrar decisões de arquitetura e evolução do projeto SIA, e é baseado em [Keep a Changelog](https://keepachangelog.com/en/2.0.0/) e [Semantic Versioning](https://semver.org/spec/v2.0.0.html), sem tantas rígidas restrições.

## [0.3.7] - 2026-02-13 (Atual)
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