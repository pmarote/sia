@echo off
title Terminal SIA - Python Portable

REM --- Carrega o Ambiente ---
call usr\init_env.bat
if %errorlevel% neq 0 (
    pause
    exit /b
)

REM --- Interface Visual ---
cls
echo ==========================================================
echo        TERMINAL DO MICROAPP PYTHON (EMBEDDED)
echo ==========================================================
echo.
echo  [AMBIENTE CARREGADO]
echo.
echo  Pasta App:  %CD%\app
echo  Python:     %PYTHONHOME%\python.exe
echo.
echo  Comandos disponiveis:
echo    test   - Roda o diagnostico (utils.info)
echo    clean  - Limpa caches (__pycache__)
echo    sia    - (Futuro) Executara o sistema principal
echo.
echo ========================================================
echo.

REM Executa o teste inicial automaticamente
python -m utils.info

REM Mantém o terminal aberto para interação
cmd /k