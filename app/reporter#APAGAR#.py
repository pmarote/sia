"""
[MICROAPP] REPORTER
Gera relatórios (Excel, Markdown, TSV) a partir de SQL.
Entrada: Argumentos via CLI ou Arquivo JSON.
"""
import sys
import argparse
import sqlite3
import json
import os
from pathlib import Path

# --- PULO DO GATO: CORREÇÃO DE IMPORT ---
# Garante que o Python enxergue a pasta onde este script está (src),
# permitindo importar os vizinhos 'to_excel' e 'to_markdown' 
# sem erros, não importa de qual pasta você chamou o comando.
base_dir = Path(__file__).parent.resolve()
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

import to_excel
import to_markdown
# ----------------------------------------

# Garante UTF-8 no console
sys.stdout.reconfigure(encoding='utf-8')

def load_config_from_json(json_path):
    """Lê o arquivo JSON e valida campos obrigatórios."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"[ERRO] Falha ao ler JSON: {e}")
        sys.exit(1)

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
                    clean_path = str(Path(path).resolve())
                    conn.execute(f"ATTACH DATABASE '{clean_path}' AS {alias}")
                    print(f"[INFO] Attached: {alias} -> {clean_path}")
        
        return conn
    except Exception as e:
        print(f"[ERRO] Falha na conexão/attach: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Microapp Reporter: SQL -> Arquivo")
    
    # Argumento Mestre: JSON
    parser.add_argument("--json", help="Caminho para arquivo JSON de configuração (substitui outros args)")

    # Argumentos Legado/CLI (agora opcionais no argparse, mas validados manualmente)
    parser.add_argument("--db", help="Banco de dados SQLite principal")
    parser.add_argument("--out", help="Arquivo de saída")
    parser.add_argument("--format", choices=["tsv", "excel", "markdown"], help="Formato de saída")
    parser.add_argument("--sql", help="Query SQL a ser executada")

    args = parser.parse_args()

    # 1. Unificação da Configuração
    config = {}

    if args.json:
        # Modo JSON (Prioritário)
        print(f"[REPORTER] 📄 Modo JSON: {args.json}")
        config = load_config_from_json(args.json)
    else:
        # Modo CLI
        print("[REPORTER] ⌨️ Modo CLI")
        # Validação Manual dos Obrigatórios
        if not all([args.db, args.out, args.format, args.sql]):
            parser.error("No modo CLI, os argumentos --db, --out, --format e --sql são OBRIGATÓRIOS.")
        
        config = {
            "db": args.db,
            "out": args.out,
            "format": args.format,
            "sql": args.sql,
            "attach": [] # CLI não suporta attach complexo facilmente, deixamos vazio
        }

    # 2. Extração e Validação Final
    db_path = config.get("db")
    out_path = config.get("out")
    fmt = config.get("format")
    sql_query = config.get("sql")
    attachments = config.get("attach", [])

    if not all([db_path, out_path, fmt, sql_query]):
        print("[ERRO] Configuração incompleta. Verifique o JSON ou os argumentos.")
        sys.exit(1)


    # 3. Execução
    print(f"[REPORTER] 🔌 Conectando em: {db_path}")
    conn = get_connection(db_path, attachments)
    
    try:
        cursor = conn.cursor()
        print("[REPORTER] 🚀 Executando Query...")
        cursor.execute(sql_query)
        
        # REMOVIDO: data = cursor.fetchall()  <-- ISSO EXPLODIA A MEMÓRIA
        # REMOVIDO: row_count check prévio. Agora confiamos no exportador.

        # 4. Roteamento para Exportadores
        print(f"[REPORTER] 💾 Salvando como {fmt.upper()}: {out_path}")
        
        if fmt == "excel":
            # Passamos o cursor diretamente. O exportador vai iterar.
            to_excel.export_excel(cursor, out_path)
            
        elif fmt == "markdown":
            # Markdown precisa saber a query original para botar no <details>
            to_markdown.export_markdown(cursor, out_path, sql_query=sql_query, db_path=db_path, attachments=attachments)
            
        elif fmt == "tsv":
            # TSV com tratamento de decimais BR
            with open(out_path, "w", encoding="utf-8") as f:
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

        else:
            # Trava de Segurança
            print(f"[ERRO CRÍTICO] Formato desconhecido ou não suportado: '{fmt}'")
            print("Formatos aceitos: excel, markdown, tsv")
            conn.close()
            sys.exit(1)

        print("[SUCESSO] Relatório gerado.")
        # IMPORTANTE: Só fecha depois de exportar, pois o cursor precisa da conexão aberta
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