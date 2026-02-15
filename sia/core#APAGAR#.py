"""
[CORE] INICIALIZAÇÃO E VALIDAÇÃO DE AMBIENTE
Garante que a estrutura de pastas e arquivos críticos existe antes 
de qualquer módulo rodar. Age como 'Single Source of Truth' para caminhos.
"""
import sys
import tomllib
from pathlib import Path
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

# --- CONFIGURAÇÃO GLOBAL DE CONSOLE ---
# Garante UTF-8 no console para toda a aplicação, evitando erros de acentuação no Windows
sys.stdout.reconfigure(encoding='utf-8')

@dataclass(frozen=True)
class AppEnv:
    """Estrutura imutável contendo as configurações vitais do sistema."""
    project_root: Path
    var_dir: Path
    logs_dir: Path
    temp_dir: Path
    db_config: dict[str, Any]

@lru_cache(maxsize=1)
def bootstrap() -> AppEnv:
    """
    Verifica a saúde do ambiente, cria diretórios dinâmicos e carrega configs.
    Roda apenas uma vez por execução.
    """
    # 1. Determina a raiz do projeto (assume que core.py está em /app)
    current_dir = Path(__file__).resolve().parent
    project_root = current_dir.parent

    # 2. Verifica Pasta VAR (Crítica)
    var_dir = project_root / "var"
    if not var_dir.exists() or not var_dir.is_dir():
        print(f"[ERRO CRÍTICO FATAL] Diretório base não encontrado: {var_dir}")
        print("O sistema não pode iniciar sem a pasta /var na raiz do projeto.")
        sys.exit(1)

    # 3. Verifica TOML (Crítico)
    toml_path = var_dir / "db_config.toml"
    if not toml_path.exists():
        print(f"[ERRO CRÍTICO FATAL] Arquivo de configuração ausente: {toml_path}")
        sys.exit(1)

    # 4. Lê a configuração do Banco
    try:
        with open(toml_path, 'rb') as f:
            db_config = tomllib.load(f)
    except Exception as e:
        print(f"[ERRO CRÍTICO FATAL] Falha ao ler {toml_path.name}: {e}")
        sys.exit(1)

    # 5. Auto-Healing: Cria pastas auxiliares se não existirem
    logs_dir = var_dir / "logs"
    temp_dir = var_dir / "temp"

    for directory in (logs_dir, temp_dir):
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"[ERRO CRÍTICO FATAL] Sem permissão para criar diretório: {directory}")
                print(f"Detalhe: {e}")
                sys.exit(1)

    # 6. Retorna a "Verdade Absoluta" do ambiente
    return AppEnv(
        project_root=project_root,
        var_dir=var_dir,
        logs_dir=logs_dir,
        temp_dir=temp_dir,
        db_config=db_config
    )

# --- Instância Global Conveniente ---
# Importe 'env' nos outros módulos para acessar as configurações imediatamente
env = bootstrap()