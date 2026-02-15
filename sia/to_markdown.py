"""
[SUB-ROTINA] MARKDOWN EXPORTER (v0.3.9)
Gera tabelas MD ricas a partir de um cursor SQLite.
Otimizado para memória: Não carrega tudo na RAM para alinhar pipes.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

def fmt_br(val: Any) -> str:
    """Formata valores para o padrão brasileiro com suporte a cores HTML para negativos."""
    if val is None: return ""
    if isinstance(val, (float, int)):
        if isinstance(val, float):
            text_val = f"{val:_.2f}".replace('.', ',').replace('_', '.')
        else:
            text_val = str(val)
        return f'<span style="color:red">{text_val}</span>' if val < 0 else text_val
    return str(val)

def export_markdown(
    cursor: sqlite3.Cursor, 
    out_path: str, 
    sql_query: str = "", 
    db_path: str = "", 
    attachments: str = "", 
    title: Optional[str] = None
) -> None:
    """Gera o arquivo Markdown via streaming de cursor."""
    """
    Gera Markdown streamando o cursor.
    Nota: O arquivo .md bruto não terá colunas alinhadas visualmente (espaços),
    mas o render (HTML/GitHub) ficará perfeito. Isso economiza RAM.
    """
    headers = [desc[0] for desc in cursor.description] if cursor.description else []
    first_row = cursor.fetchone()
    
    with open(out_path, "w", encoding="utf-8") as f:
        if title:
            f.write(f"## {title}\n\n")

        if sql_query:
            f.write('<details>\n  <summary><span style="font-size:0.9em; color:gray; cursor:pointer">🔍 Ver Query SQL Original</summary>\n\n')
            f.write(f"```sql\n{sql_query.strip()}\n```\n</details>\n\n")
        
        if not headers:
            f.write("> ⚠️ A consulta não retornou colunas.\n")
            return

        # Header e Separador (Alinhamento)
        # --- CONSTRUÇÃO DA TABELA ---
        # 1. Header Row
        f.write("| " + " | ".join(headers) + " |\n")

        # 2. Separator Row (Alinhamento)
        separators = []
        for i, _ in enumerate(headers):
            # Se tivermos a primeira linha, checamos se é número para alinhar à direita
            is_num = isinstance(first_row[i], (int, float)) if first_row else False
            separators.append("---:" if is_num else ":---")
        f.write("| " + " | ".join(separators) + " |\n")

        # 3. Write First Row (se existir)        
        row_count = 0
        if first_row:
            f.write("| " + " | ".join(fmt_br(c) for c in first_row) + " |\n")
            row_count += 1

        # 4. Write Remaining Rows (Streaming)            
        for row in cursor:
            f.write("| " + " | ".join(fmt_br(c) for c in row) + " |\n")
            row_count += 1

        # --- RICH FOOTER ---
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        f.write(f"> 📅 **Gerado em:** {data_hora} &nbsp;|&nbsp; 🗄️ **Base:** `{db_path}` &nbsp;|&nbsp; 🗄🗄️ **Attachments:** `{attachments}` &nbsp;|&nbsp; 📊 **Linhas:** {row_count}\n\n")

    print(f"[MARKDOWN] 💾 Salvo: {Path(out_path).name}")


# --- MODO STANDALONE ---
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--sql", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--title", default="", help="Título do relatório")
    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.db)
        cursor = conn.cursor()
        cursor.execute(args.sql)
        
        export_markdown(cursor, args.out, sql_query=args.sql, title=args.title)
        
        conn.close()
        sys.exit(0)
    except Exception as e:
        print(f"[ERRO MD] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()