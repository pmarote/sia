@echo off
echo ==========================================
echo      LIMPANDO CACHE DO PROJETO SIA
echo ==========================================

REM 1. Trava de Seguranca de Diretorio
REM Isso garante que o script va para a raiz do projeto de forma segura,
REM independentemente de onde voce o chamou no terminal.
cd /d "%~dp0.."

echo [INFO] Diretorio base: %CD%

REM 2. Limpeza Recursiva de Caches do Python
echo [INFO] Procurando e apagando pastas __pycache__...
FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"

echo [INFO] Apagando arquivos compilados orfaos (.pyc)...
del /s /q *.pyc >nul 2>&1

REM 3. Limpeza de Temporarios (Baseado no seu core.py)
echo [INFO] Limpando arquivos temporarios em var/temp...
if exist "var\temp" (
    del /q "var\temp\*.*" >nul 2>&1
)

echo.
echo ==========================================
echo [SUCESSO] Projeto limpo e pronto!
echo ==========================================
pause