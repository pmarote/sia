@echo off
setlocal

echo ==========================================
echo      CONFIGURADOR DE MICROAPP PYTHON
echo ==========================================

REM 1. Verificacao de Seguranca
REM Checa se o python embedded ja foi instalado (verifica se tem pip)
if exist "python\Scripts\pip.exe" (
    echo [ERRO] Ja houve a instalacao, nao da pra instalar de novo.
    echo Ao menos, encontrei o pip em: python\Scripts\pip.exe
    echo Se quiser instalar novamente do zero, delete a pasta python e reze.
    echo E entao execute novamente este setup_python_embedded.bat!
    pause
    exit /b
)


REM 2. Padronizar nome da pasta Python
if exist "python" (
    echo [OK] Pasta 'python' ja existe.
) else (
    echo Procurando pasta do Python Embed...
    REM Procura qualquer pasta que comece com "python-" e termina com "amd64"
    for /d %%i in (python-*-embed-amd64) do (
        echo Renomeando %%i para 'python'...
        ren "%%i" "python"
    )
)

if not exist "python\python.exe" (
    echo [ERRO] Nao encontrei a pasta do Python Embed descompactada.
    echo Certifique-se de extrair o zip aqui e que o nome comece com 'python-'.
    pause
    exit /b
)

REM 3. Configurar o arquivo ._pth (Habilitar import site, incluir Lib e incluir ..\..\app)
echo.
echo Configurando o arquivo ._pth (Habilitar import site e incluir Lib + ..\..\app)...

cd python
for %%f in (*._pth) do (
    echo Processando: %%f

    powershell -NoProfile -ExecutionPolicy Bypass -Command ^
      "$f='%%f'; $txt=Get-Content $f -Raw; " ^
      "$txt=$txt.Replace(\".`r`n\", \".`r`nLib`r`n\"); " ^
      "$txt=$txt.Replace(\"Lib`r`n`r`n\", \"Lib`r`n../../app`r`n`r`n\"); " ^
      "$txt=$txt.Replace('#import site','import site'); " ^
      "$txt=$txt.Replace('# Uncomment to run site.main() automatically`r`n#import site', '# Uncomment to run site.main() automatically`r`nimport site'); " ^
      "Set-Content $f $txt -NoNewline"
)
cd ..

REM 4. Baixar get-pip.py
echo.
if not exist "get-pip.py" (
    echo Baixando get-pip.py...
    curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
)

REM 5. Instalar PIP
echo.
echo Instalando PIP (isso pode demorar um pouco)...
python\python.exe get-pip.py --no-warn-script-location

REM 6. Limpeza
if exist "get-pip.py" del "get-pip.py"

echo.
echo ==========================================
echo      MICROAPP CONFIGURADO COM SUCESSO!
echo ==========================================
echo.
echo Para testar, execute o arquivo terminal.bat que esta na pasta principal (nao esta nesta pasta usr)
echo.
pause