"""
[MICROAPP] REPORTER (v0.3.9)
Gera relatórios (Excel, Markdown, TSV) a partir de SQL.
Utiliza o namespace 'sia' e configurações centralizadas via TOML.
"""
import sys
import argparse
import sqlite3
from pathlib import Path
from typing import Any, List, Optional

# --- CORE E INFRAESTRUTURA ---
from sia.core import env 
import sia.to_excel as to_excel
import sia.to_markdown as to_markdown

def resolve_path(path_str: str) -> Path:
    """Resolve caminho absoluto ou relativo ao diretório atual."""
    """Se o argumento vier com caminho absoluto → usa ele."""
    """Se vier relativo → resolve contra Path.cwd()."""
    """Isso é padrão profissional para CLI tools."""
    p = Path(path_str)
    return p if p.is_absolute() else (Path.cwd() / p)


def get_connection(db_path: str, attachments: Optional[List[dict[str, str]]] = None) -> sqlite3.Connection:
    """Conecta no SQLite e realiza os ATTACHs solicitados."""
    try:
        conn = sqlite3.connect(db_path)
        
        if attachments:
            for item in attachments:
                path = item.get('path')
                alias = item.get('alias')
                if path and alias:
                    p = Path(path)
                    clean_path = str(p if p.is_absolute() else (Path.cwd() / p).resolve())
                    conn.execute(f"ATTACH DATABASE '{clean_path}' AS {alias}")
                    print(f"[INFO] Attached: {alias} -> {clean_path}")
        
        return conn
    except Exception as e:
        print(f"[ERRO] Falha na conexão/attach: {e}")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Microapp Reporter v0.3.9: SQL -> Arquivo")
    
    parser.add_argument("--out", required=True, help="Arquivo de saída (.txt, .xlsx, .md)")
    parser.add_argument("--sql", required=True, help="Caminho para arquivo .sql ou query SQL direta")
    parser.add_argument("--title", help="Título para o cabeçalho (opcional)")

    args = parser.parse_args()

    # 1. Inferência de Formato
    out_path = Path(args.out)
    ext = out_path.suffix.lower()
    
    format_map = {'.txt': 'tsv', '.xlsx': 'excel', '.md': 'markdown'}
    fmt = format_map.get(ext)

    if not fmt:
        print(f"[ERRO CRÍTICO] Extensão '{ext}' não suportada. Use: .txt, .xlsx ou .md")
        sys.exit(1)

    # 2. Resolução do SQL
    if args.sql.lower().endswith('.sql'):
        sql_file = resolve_path(args.sql)
        if not sql_file.exists():
            print(f"[ERRO CRÍTICO] Arquivo SQL não encontrado: {sql_file}")
            sys.exit(1)
        sql_query = sql_file.read_text(encoding='utf-8')
        print(f"[REPORTER] 📄 SQL carregado: {sql_file.name}")
    else:
        sql_query = args.sql
        print("[REPORTER] 💬 SQL recebido via string.")

    # 3. Configuração via Core (Single Source of Truth)
    db_path_rel = env.db_config.get("db")
    attachments = env.db_config.get("attach", [])

    if not db_path_rel:
        print("[ERRO CRÍTICO] Configuração 'db' ausente no db_config.toml.")
        sys.exit(1)

    db_path_abs = resolve_path(db_path_rel)

    # 4. Execução
    print(f"[REPORTER] 🔌 Conectando em: {db_path_abs}")
    conn = get_connection(db_path_abs, attachments)
    
    try:
        cursor = conn.cursor()
        print("[REPORTER] 🚀 Executando Query...")
        cursor.execute(sql_query)
        
        # Resolve caminho de saída relativo à raiz
        out_path_abs = resolve_path(args.out)
        
        # 5. Roteamento
        if fmt == "excel":
            to_excel.export_excel(cursor, str(out_path_abs))
            
        elif fmt == "markdown":
            to_markdown.export_markdown(
                cursor, 
                str(out_path_abs), 
                sql_query=sql_query, 
                db_path=db_path_abs, 
                attachments=str(attachments),
                title=args.title
            )
            
        elif fmt == "tsv":
            # TSV com tratamento de decimais BR
            with open(out_path_abs, "w", encoding="utf-8") as f:
                if cursor.description:
                    f.write("\t".join(d[0] for d in cursor.description) + "\n")
                
                row_count = 0
                # Rows (um a um, não é para dar readall)
                for row in cursor:
                    clean_row = []
                    for item in row:
                        # [AJUSTE BR] Troca ponto por vírgula em números reais
                        # Remove tabs de textos para não quebrar colunas
                        if item is None: val = ""
                        elif isinstance(item, float): val = str(item).replace('.', ',')
                        else: val = str(item).replace("\t", " ")
                        clean_row.append(val)
                    f.write("\t".join(clean_row) + "\n")
                    row_count += 1
            print(f"[REPORTER] 💾 Salvo TSV ({row_count} linhas)")

        print("[SUCESSO] Relatório gerado em: " + str(out_path))
        conn.close()
    except Exception as e:
        print(f"[ERRO GERAL] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()