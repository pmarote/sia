"""
[MICROAPP] INFO / DIAGNÓSTICO
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

def read_text_safe(path: Path) -> str:
    """Lê arquivos de texto garantindo UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""

def get_uv_version() -> str:
    """Tenta obter a versão do 'uv' via linha de comando."""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "Não encontrado (uv não está no PATH)"
    except subprocess.CalledProcessError:
        return "Erro ao executar uv"

def yn(condition: bool) -> str:
    """Formata booleanos com emojis padrão."""
    return "✅ OK" if condition else "❌ FALHA"

# ---------------------------------------------------------------------
# Motor de Impressão (Dashboard)
# ---------------------------------------------------------------------
def main() -> None:
    print("="*60)
    print(" 🔍 SIA - Relatório de Diagnóstico do Sistema")
    print("="*60)

    # --- SISTEMA ---
    print(f"\n[SISTEMA] 💻 Computador e SO")
    print(f"  ├─ OS:           {os.name.upper()}")
    print(f"  ├─ Hostname:     {socket.gethostname()}")
    print(f"  └─ IP Local:     {get_ip()}")

    # --- PYTHON ---
    print(f"\n[PYTHON]  🐍 Ambiente de Execução")
    print(f"  ├─ Versão:       {sys.version.split()[0]}")
    print(f"  ├─ Executável:   {sys.executable}")
    print(f"  └─ Prefixo:      {sys.prefix}")

    # --- UV MANAGER ---
    print(f"\n[UV]      ⚡ Gerenciador de Pacotes")
    print(f"  └─ Versão:       {get_uv_version()}")

    # --- CORE ---
    print(f"\n[CORE]    🧠 Resolução de Caminhos (Namespace: {env.project_root.name})")
    print(f"  ├─ Raiz do SIA:  {env.project_root} ({yn(env.project_root.exists())})")
    print(f"  ├─ Pacote SIA:   {env.sia_package} ({yn(env.sia_package.exists())})")
    print(f"  ├─ Var Dir:      {env.var_dir} ({yn(env.var_dir.exists())})")
    print(f"  ├─ Logs Dir:     {env.logs_dir} ({yn(env.logs_dir.exists())})")
    print(f"  ├─ Temp Dir:     {env.temp_dir} ({yn(env.temp_dir.exists())})")
    print(f"  ├─ Res Dir:      {env.res_dir} ({yn(env.res_dir.exists())})")
    
    # Validação inteligente da configuração do Banco de Dados
    config_file = env.var_dir / "db_config.toml"
    try:
        rel_config_file = config_file.relative_to(env.project_root)
    except ValueError:
        rel_config_file = config_file.name

    if not config_file.exists():
        print(f"  └─ Config BD:    🚨 AVISO CRÍTICO: Arquivo '{rel_config_file}' não encontrado!")
    else:
        print(f"  ├─ Config BD:    📄 Lido de '{rel_config_file}'")
        db_main = env.db_config.get("db")
        
        if not db_main:
            print(f"  └─ DB Principal: 🚨 ERRO: Banco principal não definido no TOML!")
        else:
            attaches = env.db_config.get("attach", [])
            # Se houver attach, a linha do main leva um "├─", senão fecha com "└─"
            prefix = "├─" if attaches else "└─"
            print(f"  {prefix} DB Principal: {db_main}")
            
            if attaches:
                print(f"  └─ Anexos (ATTACH):")
                for i, att in enumerate(attaches):
                    char = "└─" if i == len(attaches) - 1 else "├─"
                    print(f"     {char} [{att.get('alias', '???')}] -> {att.get('path', '???')}")

    # --- EMBEDDED MODE ---
    pth = find_pth_file()
    embedded = pth is not None
    print(f"\n[EMBED]   📦 Status Portátil (Embedded): {yn(embedded)}")
    
    if embedded:
        print(f"  ├─ Arquivo _pth: {pth.name}")
        pth_text = read_text_safe(pth)
        
        # Checa a injeção do novo namespace no ._pth
        has_sia_root = "." in pth_text or ".." in pth_text
        has_site = "import site" in pth_text
        
        print(f"  ├─ Raiz no path: {yn(has_sia_root)}")
        print(f"  └─ import site:  {yn(has_site)}")   

    # --- SYS.PATH (Depuração de namespaces) ---
    print("\n[PATH]    🛣️  Rotas de Importação (sys.path)")
    for i, p in enumerate(sys.path):
        if p.strip():
            # Destaca a entrada que permite o 'import sia'
            suffix = " <--- [RAIZ DO PROJETO]" if p == str(env.project_root) else ""
            print(f"  [{i}] {p}{suffix}")

    print("\n" + "=" * 60)
    print(" ✅ Diagnóstico Concluído.")
    print("="*60)

if __name__ == "__main__":
    main()