import argparse
import sys
import subprocess
import ast
from pathlib import Path
from typing import Tuple

def analyze_script(file_path: Path) -> Tuple[str, str, bool]:
    """
    Analisa o script estaticamente para decidir como extrair informações.
    Retorna: (Tipo, Descrição/Output, É_Seguro_Rodar)
    """
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return ("❌ ERRO", f"Não foi possível ler o arquivo: {e}", False)

    # 1. Verifica se usa argparse (Indício forte de CLI Tool)
    uses_argparse = "argparse" in source
    
    # 2. Extrai a Docstring (Comentário de topo) usando AST (seguro)
    docstring = "Sem descrição (Adicione uma Docstring no topo do arquivo)."
    try:
        module = ast.parse(source)
        doc_node = ast.get_docstring(module)
        if doc_node:
            docstring = doc_node.strip()
    except:
        pass

    if uses_argparse:
        return ("🛠️ TOOL", "", True)
    else:
        return ("📄 SCRIPT", docstring, False)

def get_cli_help(script_path: Path) -> str:
    """Executa o script com -h para pegar o help automático."""
    try:
        cmd = [sys.executable, str(script_path), "-h"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"[Simples Execução detectada ou Erro]\nUse docstrings para descrever este arquivo."
    except subprocess.TimeoutExpired:
        return "[ERRO] Timeout ao tentar obter help."
    except Exception as e:
        return f"[ERRO] {e}"

def list_tools(root: Path):
    # Coleta os scripts primeiro para mostrar a contagem no cabeçalho
    scripts = sorted([
        f for f in root.glob("*.py") 
        if f.name != "__init__.py" and not f.name.startswith("_")
    ])

    print(f"============================================================")
    print(f" 🧰  CATÁLOGO INTELIGENTE")
    print(f"============================================================")
    print(f" 📂 PASTA ALVO:      {root.name}")
    print(f" 📍 CAMINHO LOCAL:   {root}")
    print(f" 🔢 ITENS:           {len(scripts)} scripts encontrados")
    print(f"============================================================\n")

    if not scripts:
        print(f"[AVISO] Nenhum script Python encontrado nesta pasta.")
        return

    for script in scripts:
        tipo, conteudo, is_cli = analyze_script(script)
        
        print(f"{tipo}: {script.name}")
        print("-" * 60)

        if is_cli:
            output = get_cli_help(script)
            # Remove linhas de uso padrão para limpar o visual
            lines = [l for l in output.splitlines() if not l.startswith("usage:")]
            print("\n".join(lines).strip())
        else:
            print(f"   ℹ️  {conteudo}")
            print(f"\n   (Para executar: run.bat src/{script.name})")

        print("\n" + ("=" * 60) + "\n")

def main():
    parser = argparse.ArgumentParser(description="[Microapp Utilitário] Lista tools (via -h) e Scripts (via Docstring).")
    parser.add_argument("--root", required=True, help="Pasta contendo os scripts")
    args = parser.parse_args()
    
    # Resolve para obter o caminho absoluto (C:\...)
    root_path = Path(args.root).resolve()
    
    if not root_path.exists():
        print(f"[ERRO] Caminho não encontrado: {root_path}")
        sys.exit(1)

    list_tools(root_path)

if __name__ == "__main__":
    main()