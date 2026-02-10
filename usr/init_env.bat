@echo off

REM --- Verificação de Existência ---
REM Como este script está em 'usr', procuramos 'python\python.exe' relativo a ele mesmo
if not exist "%~dp0python\python.exe" (
    echo [ERRO CRITICO] Python Embed nao encontrado em "%~dp0python".
    echo Execute 'setup_python_embedded.bat' primeiro.
    exit /b 1
)

REM --- Configuração de Caminhos ---
REM %~dp0 é o caminho onde este script está (pasta usr\)
set "USR_DIR=%~dp0"
REM Remove a barra invertida final para evitar duplicações em alguns contextos
set "USR_DIR=%USR_DIR:~0,-1%"

set "PYTHONHOME=%USR_DIR%\python"

REM [CRÍTICO] Encoding UTF-8 e Bytecode
set "PYTHONUTF8=1"
set "PYTHONDONTWRITEBYTECODE=1"

REM Adiciona Python ao PATH da sessão atual
set "PATH=%PYTHONHOME%;%PYTHONHOME%\Scripts;%PATH%"

REM --- Atalhos do Sistema (Aliases) ---
doskey test=python -m utils.info
doskey clean=rmdir /s /q __pycache__ 2^>nul
doskey sia=python -m app.main $*

REM Feedback silencioso de sucesso (opcional, útil para debug)
REM echo Environment loaded from %USR_DIR%