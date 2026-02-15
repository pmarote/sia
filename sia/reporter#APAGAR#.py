"""
[MICROAPP] REPORTER
Gera relatórios (Excel, Markdown, TSV) a partir de SQL.
Entrada: Argumentos via CLI e Configuração persistente via TOML.
"""
import sys
import argparse
import sqlite3
from pathlib import Path

# --- CORE E INFRAESTRUTURA --- # considerando sys.path[] esteja certinho incluindo a pasta app, como por ex. `C:\srcP\sia\app`
from sia.core import env  # O ambiente já entra validado aqui!
import sia.to_excel
import sia.to_markdown

def get_connection(db_path, attachments=None):
    """Conecta no SQLite e realiza os ATTACHs solicitados."""
    try:
        conn = sqlite3.connect(db_path)
        
        if attachments:
            for item in attachments:
                path = item.get('path')
                alias = item.get('alias')
                if path and alias:
                    # Cuidado: Parametrização não funciona em ATTACH, 
                    # mas como é uso interno/controlado, f-string é aceitável.
                    clean_path = str((env.project_root / path).resolve())
                    conn.execute(f"ATTACH DATABASE '{clean_path}' AS {alias}")
                    print(f"[INFO] Attached: {alias} -> {clean_path}")
        
        return conn
    except Exception as e:
        print(f"[ERRO] Falha na conexão/attach: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Microapp Reporter: SQL -> Arquivo")
    
    parser.add_argument("--out", required=True, help="Arquivo de saída (.txt, .xlsx, .md)")
    parser.add_argument("--sql", required=True, help="Caminho para arquivo .sql ou string contendo a query SQL")
    parser.add_argument("--title", help="Título para o cabeçalho (opcional)")

    args = parser.parse_args()

    # 1. Inferência de Formato via Extensão
    out_path = Path(args.out)
    ext = out_path.suffix.lower()
    
    if ext == '.txt':
        fmt = 'tsv'
    elif ext == '.xlsx':
        fmt = 'excel'
    elif ext == '.md':
        fmt = 'markdown'
    else:
        print(f"[ERRO CRÍTICO] Extensão de arquivo '{ext}' não suportada para --out.")
        print("Use apenas: .txt (TSV), .xlsx (Excel) ou .md (Markdown).")
        sys.exit(1)

    # 2. Resolução do SQL (Arquivo ou String)
    if args.sql.lower().endswith('.sql'):
        # Procura o arquivo SQL usando a raiz do projeto como base
        sql_file = env.project_root / args.sql
        if not sql_file.exists():
            print(f"[ERRO CRÍTICO] Arquivo SQL não encontrado: {sql_file}")
            sys.exit(1)
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_query = f.read()
            print(f"[REPORTER] 📄 SQL carregado do arquivo: {sql_file.name}")
        except Exception as e:
            print(f"[ERRO] Falha ao ler arquivo SQL: {e}")
            sys.exit(1)
    else:
        sql_query = args.sql
        print("[REPORTER] 💬 SQL recebido via string de comando.")

    # 3. Consumo da Configuração Persistente (Via Core)
    db_path_rel = env.db_config.get("db")
    attachments = env.db_config.get("attach", [])

    if not db_path_rel:
        print("[ERRO CRÍTICO] O arquivo db_config.toml deve conter a chave 'db'.")
        sys.exit(1)

    # Resolve o caminho do banco principal a partir da raiz do projeto
    db_path_abs = str((env.project_root / db_path_rel).resolve())

    # 4. Execução
    print(f"[REPORTER] 🔌 Conectando em: {db_path_abs}")
    conn = get_connection(db_path_abs, attachments)
    
    try:
        cursor = conn.cursor()
        print("[REPORTER] 🚀 Executando Query...")
        cursor.execute(sql_query)
        
        # Resolve o caminho de saída a partir da raiz do projeto
        out_path_abs = env.project_root / out_path
        print(f"[REPORTER] 💾 Salvando como {fmt.upper()}: {out_path_abs}")
        
        # 5. Roteamento para Exportadores
        if fmt == "excel":
            # Passamos o cursor diretamente. O exportador vai iterar.
            to_excel.export_excel(cursor, str(out_path_abs))
            
        elif fmt == "markdown":
            # Markdown precisa saber a query original para botar no <details>
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
                # Headers
                if cursor.description:
                    cols = [d[0] for d in cursor.description]
                    f.write("\t".join(cols) + "\n")
                
                row_count = 0
                # Rows (um a um, não é para dar readall)
                for row in cursor:
                    clean_row = []
                    for item in row:
                        if item is None:
                            val = ""
                        elif isinstance(item, float):
                            # [AJUSTE BR] Troca ponto por vírgula em números reais
                            val = str(item).replace('.', ',')
                        else:
                            # Remove tabs de textos para não quebrar colunas
                            val = str(item).replace("\t", " ")
                        
                        clean_row.append(val)

                    f.write("\t".join(clean_row) + "\n")
                    row_count += 1
            print(f"[REPORTER] 💾 Salvo TSV ({row_count} linhas)")

        print("[SUCESSO] Relatório gerado.")
        conn.close()
        sys.exit(0)

    except sqlite3.Error as e:
        print(f"[ERRO SQL] {e}")
        conn.close()
        sys.exit(1)
    except Exception as e:
        print(f"[ERRO GERAL] {e}")
        conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()