"""
[MICROAPP] INFO / DIAGNÓSTICO (v0.3.9)
Valida a integridade do ambiente Python Embedded, a presença do gerenciador 'uv'
e a saúde estrutural garantida pelo novo namespace 'sia.core'.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path

# --- CORE E INFRAESTRUTURA ---
# Agora utilizando o namespace consolidado do projeto
from sia.core import env 

# ---------------------------------------------------------------------
# Helpers de Diagnóstico
# ---------------------------------------------------------------------
def get_ip() -> str:
    """Tenta obter o IP local 'real' para debug de rede."""
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
    """Procura por python*._pth no diretório do executável (Modo Embedded)."""
    base = Path(sys.executable).resolve().parent
    matches = sorted(base.glob("python*._pth"))
    return matches[0] if matches else None

def read_text_safe(p: Path) -> str:
    """Lê arquivos de texto garantindo UTF-8."""
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Erro de leitura: {e}"

def check_uv() -> str:
    """Verifica se o gerenciador 'uv' está disponível no ambiente."""
    try:
        output = subprocess.check_output(
            ["uv", "--version"],
            text=True,
            stderr=subprocess.STDOUT,
        )
        return output.strip()
    except Exception as e:
        return f"NÃO ENCONTRADO / INACESSÍVEL ({e})"

def yn(v: bool) -> str:
    """Formata booleano para SIM/NÃO."""
    return "SIM" if v else "NÃO"

# ---------------------------------------------------------------------
# Motor de Impressão (Dashboard)
# ---------------------------------------------------------------------
def main() -> None:
    print("=" * 60)
    print(" 🛠️  SIA DIAGNOSTICS & SYSTEM HEALTH")
    print("=" * 60)

    # --- SISTEMA ---
    print("\n[SISTEMA] 💻 Informações do Host")
    print(f"  ├─ IP Local:    {get_ip()}")
    print(f"  └─ Diretório:   {os.getcwd()}")

    # --- PYTHON & UV ---
    print("\n[PYTHON]  🐍 Interpretador e Gerenciamento")
    print(f"  ├─ Versão:      {sys.version.split()[0]}")
    print(f"  ├─ Executável:  {sys.executable}")
    print(f"  ├─ UV Manager:  {check_uv()}")
    
    # Exibe variáveis apenas se existirem (injetadas pelo ambiente ou VS Code)
    pyhome = os.environ.get("PYTHONHOME")
    if pyhome: 
        print(f"  ├─ PYTHONHOME:  {pyhome}")
    
    # --- CORE (SINGLE SOURCE OF TRUTH) ---
    print("\n[CORE]    🏗️  Infraestrutura (sia.core)")
    print(f"  ├─ Raiz Projeto: {env.project_root}")
    print(f"  ├─ Pacote SIA:   {env.sia_package}")
    print(f"  ├─ Var Dir:      {env.var_dir} ({yn(env.var_dir.exists())})")
    print(f"  ├─ Logs Dir:     {env.logs_dir} ({yn(env.logs_dir.exists())})")
    print(f"  ├─ Temp Dir:     {env.temp_dir} ({yn(env.temp_dir.exists())})")
    print(f"  └─ Res Dir:      {env.res_dir} ({yn(env.res_dir.exists())})")
    
    db_main = env.db_config.get("db", "N/A")
    print(f"  └─ DB Principal: {db_main}")

    # --- EMBEDDED MODE ---
    pth = find_pth_file()
    embedded = pth is not None
    print(f"\n[EMBED]   📦 Status Portátil (Embedded): {yn(embedded)}")
    
    if embedded:
        print(f"  ├─ Arquivo _pth: {pth.name}")
        pth_text = read_text_safe(pth)
        
        # Checa a injeção do novo namespace no ._pth
        # Agora validamos se a raiz (onde está a pasta sia) está no path
        has_sia_root = "." in pth_text or ".." in pth_text
        has_site = "import site" in pth_text
        
        print(f"  ├─ Raiz no path: {yn(has_sia_root)}")
        print(f"  └─ import site:   {yn(has_site)}")

    # --- SYS.PATH (Depuração de namespaces) ---
    print("\n[PATH]    🛣️  Rotas de Importação (sys.path)")
    for i, p in enumerate(sys.path):
        if p.strip():
            # Destaca a entrada que permite o 'import sia'
            suffix = " <--- [RAIZ DO PROJETO]" if p == str(env.project_root) else ""
            print(f"  [{i}] {p}{suffix}")

    print("\n" + "=" * 60)
    print(" ✅ Diagnóstico Concluído.")
    print("=" * 60)

if __name__ == "__main__":
    main()