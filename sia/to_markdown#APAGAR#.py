"""
[SUB-ROTINA] MARKDOWN EXPORTER
Gera tabelas MD ricas com SQL embutido.
Otimizado para memória: Não carrega tudo na RAM para alinhar pipes.
"""
import sys
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

def fmt_br(val):
    """Formata valores para string BR com injeção HTML para negativos."""
    if val is None: return ""
    if isinstance(val, (float, int)):
        if isinstance(val, float):
            text_val = f"{val:_.2f}".replace('.', ',').replace('_', '.')
        else:
            text_val = str(val)
        if val < 0:
            return f'<span style="color:red">{text_val}</span>'
        return text_val
    return str(val)

def export_markdown(cursor, out_path, sql_query="", db_path="", attachments="", title=""):
    """
    Gera Markdown streamando o cursor.
    Nota: O arquivo .md bruto não terá colunas alinhadas visualmente (espaços),
    mas o render (HTML/GitHub) ficará perfeito. Isso economiza RAM.
    """
    if cursor.description:
        headers = [desc[0] for desc in cursor.description]
    else:
        headers = []

    # Tenta pegar a primeira linha para decidir tipos de alinhamento
    first_row = cursor.fetchone()
    
    with open(out_path, "w", encoding="utf-8") as f:

        # --- NOVA LÓGICA DO TÍTULO ---
        if title:
            f.write(f"## {title}\n\n")

        if sql_query:
            f.write("<details>\n")
            f.write('  <summary><span style="font-size:0.9em; color:gray; cursor:pointer">🔍 Ver Query SQL Original</span></summary>\n\n')
            f.write("```sql\n")
            f.write(sql_query.strip() + "\n")
            f.write("```\n")
            f.write("</details>\n\n")
        
        if not headers:
            f.write("> ⚠️ A consulta não retornou colunas.\n")
            return

        # --- CONSTRUÇÃO DA TABELA ---
        # 1. Header Row
        f.write("| " + " | ".join(headers) + " |\n")
        
        # 2. Separator Row (Alinhamento)
        separators = []
        for i, _ in enumerate(headers):
            # Se tivermos a primeira linha, checamos se é número para alinhar à direita
            is_numeric = False
            if first_row and len(first_row) > i:
                val = first_row[i]
                is_numeric = isinstance(val, (int, float))
            
            if is_numeric:
                separators.append("---:") # Direita
            else:
                separators.append(":---") # Esquerda
        
        f.write("| " + " | ".join(separators) + " |\n")
        
        # 3. Write First Row (se existir)
        row_count = 0
        if first_row:
            fmt_row = [fmt_br(c) for c in first_row]
            f.write("| " + " | ".join(fmt_row) + " |\n")
            row_count += 1
            
        # 4. Write Remaining Rows (Streaming)
        for row in cursor:
            fmt_row = [fmt_br(c) for c in row]
            f.write("| " + " | ".join(fmt_row) + " |\n")
            row_count += 1

        if row_count == 0:
            f.write("\n> ⚠️ A consulta não retornou dados.\n")

        # --- RICH FOOTER ---
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        f.write(f"> 📅 **Gerado em:** {data_hora} &nbsp;|&nbsp; 🗄️ **Base:** `{db_path}` &nbsp;|&nbsp; 🗄🗄️ **Attachments:** `{attachments}` &nbsp;|&nbsp; 📊 **Linhas:** {row_count}\n\n")

    print(f"[MARKDOWN] 💾 Salvo: {Path(out_path).name} ({row_count} linhas)")

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