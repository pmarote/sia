@echo off
chcp 65001 >nul

:: --------------------------------------------------------
::  BLOCO DE CORES (ESC, Yellow, Cyan, Reset)
:: --------------------------------------------------------
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "ESC=%%b"
)
set "Yellow=%ESC%[93m"
set "Cyan=%ESC%[96m"
set "Reset=%ESC%[0m"
set "Magenta=%ESC%[95m"
set "Green=%ESC%[92m"
:: --------------------------------------------------------

:: Garante execução na própria pasta do script
cd /d "%~dp0"

REM --- Carrega o Ambiente ---
call usr\init_env.bat
if %errorlevel% neq 0 (
    pause
    exit /b
)

cls
echo ==========================================================
echo        TERMINAL DO MICROAPP PYTHON (EMBEDDED)
echo ==========================================================
echo  Pasta App:  %CD%\app
echo  Python:     %PYTHONHOME%\python.exe
echo ========================================================
echo.

rem python -c "import pandas as pd; import sia; print('Pandas ok, versao:', pd.__version__, ' / SIA ok, versao:', sia.__version__)"

python -m main
if errorlevel 1 (
    echo.
    echo %Yellow%*****************************************************%Reset%
    echo %Yellow% ERRO:%Reset% Nao foi possivel executar %Cyan%sia%Reset%.
    echo Verifique se o Python embarcado e o pacote SIA estao corretos:
    echo   - Diretórios configurado: %Yellow%%PYTHONHOME%%Reset%
    echo   - Path: %Yellow%xxxx%Reset%
    echo %Yellow%*****************************************************%Reset%
    echo.
    pause
    goto fim
)

title SIA - Sistema de Auditoria

goto menu2

:menu
cls
:menu2
echo ==================================================
echo                %Cyan%SIA - Sistema de Auditoria%Reset%
echo ==================================================
echo.
echo   %Yellow%E ai, o que vamos fazer?%Reset%
echo.
echo   1 - Rodar %Cyan%python -m sia.app.sia_pipeline%Reset%
echo   2 - Listar ferramentas CLI do SIA  [%Cyan%python -m sia.app.list_tools%Reset%]
echo   3 - Abrir um Prompt de Comando nesta pasta
echo   4 - Abrir um Explorer nesta pasta de trabalho
echo   5 - Abrir um Explorer na pasta SIA  [%Cyan%\srcP\sia%Reset%]
echo   6 - Abrir Notepad++ da pasta usr do SIA  [%Cyan%\srcP\sia\usr%Reset%]
echo   7 - Abrir Sqliteman da pasta usr do SIA  [%Cyan%\srcP\sia\usr%Reset%]
echo   0 - Sair
echo.
set /p op="Escolha uma opcao e tecle ENTER: "

if "%op%"=="1" goto pipeline
if "%op%"=="2" goto listtools
if "%op%"=="3" goto opencmd
if "%op%"=="4" goto openexplorerpwd
if "%op%"=="5" goto openexploresia
if "%op%"=="6" goto opennotepadsia
if "%op%"=="7" goto opensqlitemansia
if "%op%"=="0" goto fim

echo.
echo %Yellow%Opcao invalida.%Reset% Tente novamente.
pause >nul
goto menu

:pipeline
cls
echo ==================================================
echo   Executando: %Cyan%python -m sia.app.sia_pipeline%Reset%
echo ==================================================
echo.
python -m sia.app.sia_pipeline
echo.
echo --------------------------------------------------
echo   %Yellow%Pipeline concluido (ou encerrado pelo Python).%Reset%
echo --------------------------------------------------
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:listtools
cls
echo ==================================================
echo   Executando: %Cyan%python -m sia.app.list_tools%Reset%
echo ==================================================
echo.
python -m sia.app.list_tools
echo.
echo --------------------------------------------------
echo   %Yellow%Fim da lista de ferramentas do SIA.%Reset%
echo --------------------------------------------------
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:opencmd
cls
echo ==================================================
echo   Abrindo um Prompt de Comando nesta pasta:
echo   %Yellow%%CD%%Reset%
echo ==================================================
echo.
echo "Prompt SIA" cmd /k "title Prompt SIA & cd /d "%CD%"
start "Prompt SIA" cmd /k "title Prompt SIA & cd /d "%CD%"
echo.
echo %Cyan%Você pode usar o novo prompt, %Yellow%que abriu em nova janela%Reset%.
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:openexplorerpwd
cls
echo ==================================================
echo   Abrindo Windows Explorer na pasta de trabalho atual:
echo   %Yellow%%CD%%Reset%
echo ==================================================
echo.
start "" explorer "%CD%"
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:openexploresia
cls
echo ==================================================
echo   Abrindo Windows Explorer na pasta SIA:
echo   %Yellow%\srcP\sia%Reset%
echo ==================================================
echo.
start "" explorer "\srcP\sia"
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:opennotepadsia
cls
echo ==================================================
echo   Abrindo Notepad++ da pasta usr do SIA  
echo   %Yellow%\srcP\sia\usr%Reset%
echo ==================================================
echo.
start "" \srcP\sia\usr\npp.8.8.7.portable.x64\notepad++.exe
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:opensqlitemansia
cls
echo ==================================================
echo   Abrindo Sqliteman da pasta usr do SIA  
echo   %Yellow%\srcP\sia\usr%Reset%
echo ==================================================
echo.
start "" \srcP\sia\usr\Sqliteman-1.2.2\sqliteman.exe
echo.
echo Pressione qualquer tecla para voltar ao menu do SIA...
pause >nul
goto menu

:fim
cls
echo %Magenta%Siga o coelho branco, só que não.%Reset%
echo %Green%I'll be back. -- Ass: Skynet%Reset%
timeout /t 2 >nul
exit /b
