@echo off
title Terminal SIA - Python Portable

REM --- Carrega o Ambiente ---
call C:\srcP\sia_0.3.9\usr\init_env.bat
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
echo ========================================================
echo.

REM Mantém o terminal aberto para interação
cmd /k