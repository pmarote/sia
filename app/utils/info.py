"""
[MICROAPP] INFO / DIAGNÓSTICO
Valida a integridade do ambiente Python Embedded, a presença do gerenciador 'uv'
e a saúde estrutural garantida pelo módulo 'core.py'.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path

# --- CORE E INFRAESTRUTURA --- # consi/derando sys.path[] esteja certinho incluindo a pasta app, como por ex. `C:\srcP\sia\app`
from core import env  # O ambiente já entra validado aqui!

# ---------------------------------------------------------------------
# Helpers de Diagnóstico
# ---------------------------------------------------------------------
def get_ip() -> str:
    """Tenta obter o IP local 'real' (não 127.0.0.1) para debug de rede."""
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
    return "SIM" if v else "NÃO"

# ---------------------------------------------------------------------
# Motor de Impressão (Dashboard)
# ---------------------------------------------------------------------
def main():
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
    
    # Exibe variáveis apenas se existirem (injetadas pelo VS Code)
    pyhome = os.environ.get("PYTHONHOME")
    if pyhome: print(f"  ├─ PYTHONHOME:  {pyhome}")
    
    # --- CORE (SINGLE SOURCE OF TRUTH) ---
    print("\n[CORE]    🏗️  Infraestrutura (app.core)")
    print(f"  ├─ Raiz:        {env.project_root}")
    print(f"  ├─ Var Dir:     {env.var_dir} ({yn(env.var_dir.exists())})")
    print(f"  ├─ Logs Dir:    {env.logs_dir} ({yn(env.logs_dir.exists())})")
    print(f"  ├─ Temp Dir:    {env.temp_dir} ({yn(env.temp_dir.exists())})")
    
    db_main = env.db_config.get("db", "N/A")
    print(f"  └─ DB Principal: {db_main}")

    # --- EMBEDDED MODE (O coração do setup portátil) ---
    pth = find_pth_file()
    embedded = pth is not None
    print(f"\n[EMBED]   📦 Status Portátil (Embedded): {yn(embedded)}")
    
    if embedded:
        print(f"  ├─ Arquivo _pth: {pth.name}")
        pth_text = read_text_safe(pth)
        
        # Checa as injeções críticas no ._pth
        has_app = "../../app" in pth_text or "../app" in pth_text
        has_site = "import site" in pth_text
        
        print(f"  ├─ 'app' no path: {yn(has_app)}")
        print(f"  └─ import site:   {yn(has_site)}")

    # --- SYS.PATH (Para debug de importações) ---
    print("\n[PATH]    🛣️  Rotas de Importação (sys.path)")
    for i, p in enumerate(sys.path):
        if p.strip(): # Ignora linhas vazias
            print(f"  [{i}] {p}")

    print("\n" + "=" * 60)
    print(" ✅ Diagnóstico Concluído.")
    print("=" * 60)

if __name__ == "__main__":
    main()