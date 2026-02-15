"""
[MICROAPP] DUMP CODE
Gera um arquivo Markdown consolidado com a árvore de diretórios e o 
código fonte do projeto. Essencial para dar contexto atualizado à IA.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Set

# --- GARA# --- CORE E INFRAESTRUTURA --- # consi/derando sys.path[] esteja certinho incluindo a pasta app, como por ex. `C:\srcP\sia\app`
from core import env  # O ambiente já entra validado aqui!

# --- CONFIGURAÇÃO (O Contrato) ---
# Ignorar pastas de sistema, git, dados do usuário e caches/temporários
IGNORE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", ".idea", ".vscode", 
    "usr", "build", "dist", "temp", "logs", "data"
}

# Extensões que queremos ler para dar contexto à IA (Adicionado .toml)
TARGET_EXTENSIONS = {".py", ".md", ".bat", ".json", ".sql", ".toml"}

def build_tree(root: Path) -> str:
    """
    Gera uma representação visual da árvore de diretórios.
    Retorna uma string formatada.
    """
    lines: List[str] = []

    def walk(dir_path: Path, prefix: str = "") -> None:
        try:
            # Filtra e ordena (Pastas primeiro, alfabético depois)
            entries = sorted([
                e for e in dir_path.iterdir() 
                if e.name not in IGNORE_DIRS
            ], key=lambda x: (x.is_file(), x.name)) 
        except PermissionError:
            lines.append(f"{prefix}├── [ERRO DE PERMISSÃO: {dir_path.name}]")
            return

        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            
            lines.append(f"{prefix}{connector}{entry.name}")

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                walk(entry, prefix + extension)

    lines.append(root.name)
    walk(root)
    return "\n".join(lines)

def collect_files(root: Path) -> List[Path]:
    """
    Coleta todos os arquivos que correspondem às extensões alvo,
    respeitando os diretórios ignorados.
    """
    collected = []
    
    # rglob('*') pega tudo, depois filtramos manualmente para respeitar o IGNORE_DIRS
    for path in root.rglob('*'):
        if path.is_file() and path.suffix.lower() in TARGET_EXTENSIONS:
            # Verifica se alguma parte do caminho (pasta raiz até o arquivo) está na lista negra
            if not any(part in IGNORE_DIRS for part in path.parts):
                collected.append(path)
                
    return sorted(collected)

def make_markdown(root: Path) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parts = []
    
    # Cabeçalho
    parts.append(f"# 🧠 CONTEXTO DO PROJETO: {root.name}")
    parts.append(f"> Gerado automaticamente em: {now}")
    parts.append("")
    
    # 1. Estrutura Visual
    parts.append("## 1. 🌳 Estrutura de Diretórios")
    parts.append("```text")
    parts.append(build_tree(root))
    parts.append("```")
    parts.append("")

    # 2. Conteúdo dos Arquivos
    files = collect_files(root)
    parts.append(f"## 2. 📦 Conteúdo dos Arquivos ({len(files)} arquivos encontrados)")
    parts.append("")

    for file_path in files:
        rel_path = file_path.relative_to(root).as_posix()
        ext = file_path.suffix.lower().replace(".", "")
        
        # Mapeamento para syntax highlighting do markdown
        lang_map = {
            "py": "python",
            "md": "markdown",
            "bat": "batch",
            "json": "json",
            "sql": "sql",
            "toml": "toml"
        }
        lang = lang_map.get(ext, "text")

        parts.append(f"### 📄 `{rel_path}`")
        parts.append(f"```{lang}")
        
        try:
            # Tenta ler utf-8, se falhar tenta latin-1 (comum em Windows/Bat antigos)
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = file_path.read_text(encoding="latin-1")
                
            parts.append(content.strip())
        except Exception as e:
            parts.append(f"[ERRO AO LER ARQUIVO: {e}]")
            
        parts.append("```")
        parts.append("---")
        parts.append("")

    return "\n".join(parts)

def main():
    # 1. Configuração do CLI (Interface do Contrato)
    parser = argparse.ArgumentParser(
        description="[Microapp Utilitário] Gera dump de código para contexto de IA."
    )
    # Valores default setados usando o env.project_root do nosso core!
    parser.add_argument("--root", default=str(env.project_root), help="Pasta raiz do projeto para análise")
    parser.add_argument("--dst", default=str(env.project_root / "res" / "docs" / "context_dump.md"), help="Caminho do arquivo Markdown de saída")
    
    args = parser.parse_args()
    
    root_path = Path(args.root).resolve()
    dst_path = Path(args.dst).resolve()

    print(f"[INFO] Iniciando dump de: {root_path}")
    print(f"[INFO] Destino: {dst_path}")

    # 2. Validação
    if not root_path.exists():
        print(f"[ERRO] Diretório raiz não encontrado: {root_path}")
        sys.exit(1)

    try:
        # 3. Processamento (Core)
        full_markdown = make_markdown(root_path)
        
        # Garante que a pasta de destino exista
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 4. Saída (Persistência)
        dst_path.write_text(full_markdown, encoding="utf-8")
        
        print(f"[SUCESSO] Arquivo gerado com sucesso. Tamanho: {len(full_markdown)/1024:.2f} KB")
        sys.exit(0) # Código de sucesso para o Maestro

    except Exception as e:
        print(f"[FATAL] Ocorreu um erro não tratado: {e}")
        sys.exit(1) # Código de erro para o Maestro

if __name__ == "__main__":
    main()