@echo off
title Terminal SIA - Python Portable

REM --- Carrega o Ambiente ---
call usr\init_env.bat
if %errorlevel% neq 0 (
    pause
    exit /b
)

cls
REM Executa o teste inicial automaticamente
python -m utils.info

REM --- Interface Visual ---
echo.
echo ==========================================================
echo        TERMINAL DO MICROAPP PYTHON (EMBEDDED)
echo ==========================================================
echo.
echo  Comandos exemplo:
echo  python -m reporter -h
echo.
echo ========================================================
echo.

REM Mantém o terminal aberto para interação
cmd /k