@echo off
set SIA_SCRIPT_NAME=%~n0
set SIA_VERSION=%SIA_SCRIPT_NAME:terminal_sia_=%
title Terminal SIA v.%SIA_VERSION%

REM --- Carrega o Ambiente ---
call C:\srcP\sia_%SIA_VERSION%\usr\init_env.bat
if %errorlevel% neq 0 (
    pause
    exit /b
)

cls
REM Executa o teste inicial automaticamente
python -m sia.utils.info

doskey s=python -m sia.$*

REM --- Interface Visual ---
echo.
echo ==========================================================
echo        TERMINAL DO MICROAPP PYTHON (EMBEDDED)
echo ==========================================================
echo.
echo  Exemplos de modulos:
echo    python -m sia.utils.info
echo    python -m sia.reporter -h
echo.
echo  Atalho para uso (foi definido: doskey s=python -m sia.$*)
echo    s utils.info
echo    s utils.list_tools --root %SIA_ROOT_DIR%/sia
echo    s utils.list_tools --root %SIA_ROOT_DIR%/sia/utils
echo    s reporter --out rel_basicos.md --sql sql2.sql
echo.
echo  Workflow
echo  - Um simples gerador de var/db_config.toml
echo      s utils.gen_db_config --h
echo  - para executar um cookbook
echo      s cookbook_parser --in res/cookbooks/ckb_basicos.md
echo  - para gerar um cookbook automaticamente a partir de um db3
echo      s utils.gen_cookbook --db "(...)\13013199258_260122_132626.db3" --out "ckb_13013199258_260122_132626.md
echo  - mas, na pratica, vai usar prep_safic.py, que nao e modulo, e python na pasta de trabalho  
echo  - que verifica se o ambiente ta certinho, gera var/db_config.toml... e processa cookbook inicial
echo      python prep_safic.py
echo.
echo ========================================================
echo.

REM Mantém o terminal aberto para interação
cmd /k