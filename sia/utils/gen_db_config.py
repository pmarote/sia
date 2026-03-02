import argparse
from pathlib import Path

from sia.core import env

def format_path(path_str: str) -> str:
    """Garante que o caminho use barras normais (padrão Linux/TOML) e não invertidas."""
    return path_str.replace("\\", "/")

def generate_config(db_path: str, attaches: list[list[str]] | None) -> None:
    """Gera o arquivo var/db_config.toml com o banco principal e os attaches."""
    
    config_dir = env.project_root / "var"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "db_config.toml"
    
    db_path_fmt = format_path(db_path)
    
    linhas: list[str] = [
        "# var/db_config.toml",
        "# Arquivo gerado automaticamente via sia.utils.gen_db_config",
        "",
        "# Banco principal (main)",
        f'db = "{db_path_fmt}"',
        ""
    ]
    
    if attaches:
        linhas.append("# Bancos auxiliares para ATTACH")
        for attach in attaches:
            # argparse com nargs=2 retorna uma sublista com 2 elementos: [path, alias]
            caminho = format_path(attach[0])
            alias = attach[1]
            
            linhas.extend([
                "[[attach]]",
                f'path = "{caminho}"',
                f'alias = "{alias}"',
                ""
            ])
            
    # Força quebra de linha no final do arquivo e junta tudo
    conteudo = "\n".join(linhas)
    
    # Salva garantindo a Regra de Ouro: encoding="utf-8"
    config_file.write_text(conteudo, encoding="utf-8")
    
    print(f"✅ Arquivo de configuração gerado com sucesso em: {config_file.relative_to(env.project_root)}")
    print(f"🗄️  Banco principal: {db_path_fmt}")
    if attaches:
        print(f"🔗 Bancos anexados: {len(attaches)}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Gerador do arquivo db_config.toml do SIA")
    
    parser.add_argument(
        "--db", 
        required=True, 
        help="Caminho completo ou relativo para o banco de dados principal (.db3/.sqlite)"
    )
    
    parser.add_argument(
        "--attach", 
        action="append", 
        nargs=2, 
        metavar=('PATH', 'ALIAS'),
        help="Caminho e alias para um banco auxiliar. Pode ser usado múltiplas vezes. Ex: --attach caminho/osf.db osf"
    )
    
    args = parser.parse_args()
    
    generate_config(args.db, args.attach)

if __name__ == "__main__":
    main()