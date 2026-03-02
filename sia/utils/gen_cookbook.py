import argparse
import sqlite3
import sys
from pathlib import Path

def generate_cookbook(db_path: Path, out_path: Path, limit: int) -> None:
    """Explora o SQLite e gera um cookbook Markdown para análise de dados."""
    
    if not db_path.exists():
        print(f"❌ ERRO: Banco de dados não encontrado: {db_path}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Busca todas as tabelas e views, ignorando as tabelas internas do SQLite
        cursor.execute("""
            SELECT name, type 
            FROM sqlite_master 
            WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' 
            ORDER BY type, name;
        """)
        objects = cursor.fetchall()

        if not objects:
            print(f"⚠️ AVISO: Nenhuma tabela ou view encontrada em '{db_path.name}'.")
            conn.close()
            return

        print(f"🔍 Explorando '{db_path.name}'...")
        print(f"   Encontrados(as) {len(objects)} tabelas/views. Gerando SQLs...")

        linhas_md = [
            f"# 📖 Cookbook de Exploração: `{db_path.name}`",
            "> Arquivo gerado automaticamente via `sia.utils.gen_cookbook`.",
            f"> **Objetivo:** Amostragem das tabelas e views (Limite: {limit} linhas).",
            ""
        ]

        for obj_name, obj_type in objects:
            # PRAGMA table_info retorna informações de cada coluna da tabela/view
            cursor.execute(f"PRAGMA table_info('{obj_name}');")
            columns_info = cursor.fetchall()
            
            if not columns_info:
                continue

            # A posição [1] do retorno do PRAGMA contém o nome da coluna
            col_names = [info[1] for info in columns_info]
            
            # Formata as colunas com indentação para ficar bonito no SQL
            colunas_formatadas = ",\n    ".join(col_names)

            linhas_md.append(f"## {obj_type.upper()}: `{obj_name}`")
            linhas_md.append("```sql")
            linhas_md.append(f"SELECT\n    {colunas_formatadas}\nFROM\n    {obj_name}\nLIMIT {limit};")
            linhas_md.append("```")
            linhas_md.append("")

        conn.close()

        # Garante que a pasta de destino exista
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Salva garantindo a Regra de Ouro: encoding="utf-8"
        out_path.write_text("\n".join(linhas_md), encoding="utf-8")

        print(f"\n✅ SUCESSO! Cookbook exploratório gerado.")
        print(f"📁 Destino: {out_path}")
        print(f"💡 Dica: Rode agora:")
        print(f"❯ python -m sia.cookbook_parser --in {out_path}")

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao processar banco de dados: {e}")
        sys.exit(1)

def main() -> None:
    parser = argparse.ArgumentParser(description="Gerador de Cookbook Exploratório do SIA")
    
    parser.add_argument(
        "--db", 
        required=True, 
        help="Caminho para o arquivo de banco de dados (.db3/.sqlite)"
    )
    parser.add_argument(
        "--out", 
        required=True, 
        help="Caminho onde o cookbook (.md) será salvo. Ex: ckb_exploracao.md"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=2, 
        help="Quantidade limite de registros no SELECT (padrão: 2)"
    )
    
    args = parser.parse_args()
    
    # Resolve caminhos
    db_path = Path(args.db).resolve()
    out_path = Path(args.out).resolve()
    
    generate_cookbook(db_path, out_path, args.limit)

if __name__ == "__main__":
    main()