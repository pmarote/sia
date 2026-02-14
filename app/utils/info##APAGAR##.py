"""
[DIAGNÓSTICO] Ambiente Python Embedded (Windows) + caminhos de importação

Este utilitário existe para explicar *por que* o comando `python -m ...` às vezes
não encontra seus módulos em uma instalação "embedded/portable" do Python.

Pontos-chave (resumo técnico):

1) Em distribuições Python *embedded* no Windows, a presença de um arquivo
   `pythonXY._pth` ao lado do executável ativa um modo de "path controlado"
   (equivalente prático a um modo isolado):
   - `sys.path` passa a ser definido *somente* pelas linhas do `._pth`;
   - variáveis de ambiente como `PYTHONPATH` (e, em geral, customizações externas)
     tornam-se inúteis para resolver imports — e, por isso, não é recomendado
     depender delas nesse tipo de setup;
   - o carregamento de `site` (e `site-packages`) também é controlado pelo
     próprio `._pth` (linha `import site`).

2) Para que módulos do projeto sejam importáveis "de qualquer lugar", o caminho
   do projeto deve estar no `._pth`. Neste setup, foi incluída a linha:

       ../../app

   dentro de:
       <pasta-do-python>/python313._pth

   Isso faz com que o diretório `app` do projeto entre no `sys.path`, permitindo
   executar este módulo assim, independentemente do diretório atual:

       python -m utils.info

3) Este script imprime:
   - `sys.executable`
   - `PYTHONHOME` / `PYTHONPATH` (se existirem)
   - conteúdo do arquivo `python*._pth` (se existir)
   - `sys.path` (equivalente a: `python -c "import sys; print(sys.path)"`)
"""

from __future__ import annotations

import glob
import os
import socket
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def get_ip() -> str:
    """Tenta obter o IP local 'real' (não 127.0.0.1)."""
    try:
        # Truque para pegar o IP real da rede (não o 127.0.0.1)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def find_pth_file() -> Path | None:
    """Procura por python*._pth no mesmo diretório do executável."""
    base = Path(sys.executable).resolve().parent
    matches = sorted(base.glob("python*._pth"))
    return matches[0] if matches else None


def read_text_safe(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"[ERRO] Não foi possível ler {p}: {e}"


def check_pip() -> str:
    """Verifica se pip está instalado e funcional (quando aplicável)."""
    base_dir = Path(sys.executable).resolve().parent
    pip_exe = base_dir / "Scripts" / "pip.exe"

    if not pip_exe.exists():
        return "NAO ENCONTRADO (Execute setup_app.bat para instalar)"

    # Se existe, pergunta a versão
    try:
        output = subprocess.check_output(
            [sys.executable, "-m", "pip", "--version"],
            text=True,
            stderr=subprocess.STDOUT,
        )
        # O output é algo como "pip 24.0 from ...", pegamos a segunda palavra
        version = output.split()[1]
        return f"INSTALADO (v{version})"
    except Exception as e:
        return f"ERRO AO VERIFICAR: {e}"


def env(name: str) -> str:
    return os.environ.get(name, "")


def yn(v: bool) -> str:
    return "SIM" if v else "NAO"


# ---------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------
print("-" * 72)
print(f"PYTHON:      {sys.version.split()[0]}")
print(f"EXECUTAVEL:  {sys.executable}")
print(f"DIRETORIO:   {os.getcwd()}")
print(f"IP LOCAL:    {get_ip()}")
print(f"PIP:         {check_pip()}")
print("-" * 72)

pyhome = env("PYTHONHOME")
pypath = env("PYTHONPATH")
print(f"PYTHONHOME:  {pyhome if pyhome else '(nao definido)'}")
print(f"PYTHONPATH:  {pypath if pypath else '(nao definido)'}")

pth = find_pth_file()
embedded = pth is not None
print(f"EMBEDDED:    {yn(embedded)} (arquivo ._pth {'encontrado' if embedded else 'nao encontrado'})")

if embedded:
    print("-" * 72)
    print(f"ARQUIVO ._pth: {pth}")
    pth_text = read_text_safe(pth)
    print("CONTEUDO:")
    print(pth_text.rstrip())

    # Checagens específicas do nosso setup
    expected_entry = "../../app"
    has_entry = expected_entry in pth_text
    has_import_site = "\nimport site" in ("\n" + pth_text.replace("\r\n", "\n"))
    print("-" * 72)
    print(f"Entrou '{expected_entry}' no ._pth? {yn(has_entry)}")
    print(f"'import site' habilitado no ._pth? {yn(has_import_site)}")

    # Explica tecnicamente (curto e objetivo) o porquê do PYTHONPATH ser inútil aqui
    # e verifica se, na prática, ele foi ignorado (não aparecendo em sys.path)
    if pypath:
        ignored = pypath not in sys.path
        print(f"PYTHONPATH aparece em sys.path? {yn(not ignored)}")
        if ignored:
            print("OBS: Neste modo, sys.path é controlado pelo ._pth; por isso PYTHONPATH tende a ser ignorado.")
else:
    print("OBS: Sem ._pth, sys.path tende a incluir o diretório atual e pode respeitar PYTHONPATH.")

print("-" * 72)
print("sys.path (equivalente a: python -c \"import sys; print(sys.path)\"):")
for i, p in enumerate(sys.path):
    print(f"  [{i}] {p}")

print("-" * 72)
print("Como executar este módulo de qualquer lugar (com ../../app no ._pth):")
print("  python -m utils.info")
print("-" * 72)
