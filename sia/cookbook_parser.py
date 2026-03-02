import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Importa o ambiente global do projeto
from sia.core import env

def clean_temp_files(temp_dir: Path) -> None:
    """Apaga arquivos em var/temp que não sejam do dia de hoje."""
    hoje = datetime.now().strftime("%y%m%d")
    
    if not temp_dir.exists():
        temp_dir.mkdir(parents=True, exist_ok=True)
        return

    for arquivo in temp_dir.iterdir():
        if arquivo.is_file():
            # Se o nome do arquivo não começar com a data de hoje (ex: 250215), apaga
            if not arquivo.name.startswith(hoje):
                try:
                    arquivo.unlink()
                except Exception as e:
                    print(f"⚠️ Não foi possível apagar arquivo temporário {arquivo.name}: {e}")

def process_cookbook(input_path: Path) -> None:
    """Lê o cookbook, extrai SQLs, executa o reporter e gera o relatório final."""
    
    # Define o caminho de saída (trocando ckb_ por rel_ na mesma pasta)
    out_name = input_path.name.replace("ckb_", "rel_")
    output_path = input_path.parent / out_name
    
    temp_dir = env.project_root / "var" / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Lê o conteúdo original do cookbook
    conteudo = input_path.read_text(encoding="utf-8")
    
    # Regex para encontrar blocos SQL: procura tudo entre ```sql e ```
    padrao_sql = re.compile(r'```sql\n(.*?)\n```', re.DOTALL | re.IGNORECASE)
    
    # Função interna para substituir cada bloco encontrado
    def processar_bloco(match: re.Match) -> str:
        codigo_sql = match.group(1).strip()
        
        # Gera o prefixo de timestamp: AnoMesDiaHoraMinutoSegundoMilissegundo
        ts = datetime.now().strftime("%y%m%d%H%M%S%f")[:14]
        
        temp_sql = temp_dir / f"{ts}.sql"
        temp_md = temp_dir / f"{ts}.md"
        
        # 1. Salva o código SQL no arquivo temporário
        temp_sql.write_text(codigo_sql, encoding="utf-8")
        
        print(f"🔄 Processando bloco SQL temporário: {temp_sql.name}...")
        
        # 2. Chama o sia.reporter via subprocess (usando o mesmo executável Python)
        # sys.executable garante que estamos usando o Python Embedded do projeto
        comando = [
            sys.executable, "-m", "sia.reporter",
            "--out", str(temp_md),
            "--sql", str(temp_sql)
        ]
        
        # Executa o comando a partir da raiz do projeto
        resultado = subprocess.run(comando, cwd=env.project_root, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"❌ Erro ao executar o bloco SQL {temp_sql.name}:\n{resultado.stderr}")
            return f"> **Erro ao processar SQL:**\n> `{resultado.stderr.strip()}`\n\n```sql\n{codigo_sql}\n```"
        
        # 3. Lê o resultado gerado e retorna para substituir no texto original
        if temp_md.exists():
            tabela_md = temp_md.read_text(encoding="utf-8")
            return tabela_md
        else:
            return f"> **Aviso:** O arquivo de saída {temp_md.name} não foi gerado."

    # Substitui todos os blocos SQL encontrados invocando a função acima
    print(f"📖 Lendo cookbook: {input_path.name}")
    novo_conteudo = padrao_sql.sub(processar_bloco, conteudo)
    
    # Salva o arquivo final
    output_path.write_text(novo_conteudo, encoding="utf-8")
    print(f"✅ Relatório gerado com sucesso: {output_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Parser de Cookbooks do SIA")
    parser.add_argument("--in", dest="input_file", required=True, help="Caminho para o arquivo cookbook (.md)")
    args = parser.parse_args()
    
    input_path = Path(args.input_file)
    
    if not input_path.exists():
        print(f"❌ Arquivo de entrada não encontrado: {input_path}")
        sys.exit(1)
    
    # Inicia o processamento
    process_cookbook(input_path)
        
    # Limpa os temporários antigos após terminar
    temp_dir = env.project_root / "var" / "temp"
    clean_temp_files(temp_dir)

if __name__ == "__main__":
    main()