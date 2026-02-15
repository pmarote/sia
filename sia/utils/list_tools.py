"""
[MICROAPP] LIST TOOLS (v0.3.9)
Lista ferramentas (via -h) e Scripts (via Docstring) no novo namespace 'sia'.
Garante a visibilidade das ferramentas disponíveis no diretório especificado.
"""
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
    except Exception:
        pass

    if uses_argparse:
        return ("🛠️ TOOL", "", True)
    else:
        return ("📄 SCRIPT", docstring, False)

def get_cli_help(script_path: Path) -> str:
    """Executa o script com -h para pegar o help automático dentro do ambiente v0.3.9."""
    try:
        # Tenta executar via módulo caso esteja dentro do pacote sia
        parts = script_path.parts
        if "sia" in parts:
            idx = parts.index("sia")
            module_path = ".".join(parts[idx:]).replace(".py", "")
            cmd = [sys.executable, "-m", module_path, "-h"]
        else:
            cmd = [sys.executable, str(script_path), "-h"]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "[Modo de execução simples ou Erro de Módulo]\nUse docstrings para descrever este arquivo."
    except subprocess.TimeoutExpired:
        return "[ERRO] Timeout ao tentar obter help."
    except Exception as e:
        return f"[ERRO] {e}"

def list_tools(root: Path) -> None:
    """Gera o catálogo visual de ferramentas."""
    scripts = sorted([
        f for f in root.glob("*.py") 
        if f.name != "__init__.py" and not f.name.startswith("_")
    ])

    print("=" * 60)
    print(" 🧰  SIA TOOL CATALOG (v0.3.9)")
    print("=" * 60)
    print(f" 📂 PASTA:           {root.name}")
    print(f" 📍 LOCAL:           {root}")
    print(f" 🔢 ITENS:           {len(scripts)} scripts encontrados")
    print("-" * 60 + "\n")

    if not scripts:
        print("[AVISO] Nenhum script Python encontrado nesta pasta.")
        return

    for script in scripts:
        tipo, conteudo, is_cli = analyze_script(script)
        
        print(f"{tipo}: {script.name}")
        print("-" * 30)

        if is_cli:
            output = get_cli_help(script)
            # Limpa o visual removendo a linha de usage padrão do argparse
            lines = [l for l in output.splitlines() if not l.lower().startswith("usage:")]
            print("\n".join(lines).strip())
        else:
            print(f"   ℹ️  {conteudo}")
            # Sugestão de comando baseada no novo padrão de execução
            print(f"\n   (Execução: python -m sia.{root.name}.{script.stem})")

        print("\n" + ("=" * 60) + "\n")

def main() -> None:
    parser = argparse.ArgumentParser(description="[Microapp] Lista tools v0.3.9.")
    parser.add_argument("--root", required=True, help="Pasta contendo os scripts (ex: sia/utils)")
    args = parser.parse_args()
    
    root_path = Path(args.root).resolve()
    
    if not root_path.exists():
        print(f"[ERRO] Caminho não encontrado: {root_path}")
        sys.exit(1)

    list_tools(root_path)

if __name__ == "__main__":
    main()