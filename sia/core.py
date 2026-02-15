"""
[CORE] INICIALIZAÇÃO E VALIDAÇÃO DE AMBIENTE (v0.3.9)
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
# Garante UTF-8 no console para toda a aplicação, evitando erros no Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

@dataclass(frozen=True)
class AppEnv:
    """Estrutura imutável contendo as configurações vitais do sistema."""
    project_root: Path
    sia_package: Path
    var_dir: Path
    logs_dir: Path
    temp_dir: Path
    res_dir: Path
    db_config: dict[str, Any]

@lru_cache(maxsize=1)
def bootstrap() -> AppEnv:
    """
    Verifica a saúde do ambiente, cria diretórios dinâmicos e carrega configs.
    Roda apenas uma vez por execução.
    """
    # 1. Determina a localização do pacote 'sia'
    # Assume-se que core.py está em /sia/core.py
    sia_package = Path(__file__).resolve().parent
    
    # 2. Determina a raiz do projeto (pasta acima de /sia)
    project_root = sia_package.parent

    # 3. Verifica Pasta VAR (Crítica para estado e configs)
    var_dir = project_root / "var"
    if not var_dir.exists() or not var_dir.is_dir():
        # Fallback para pasta var dentro do pacote se não estiver na raiz
        var_dir = sia_package / "var"
        if not var_dir.exists():
            print(f"[ERRO CRÍTICO] Diretório /var não encontrado na raiz: {project_root}")
            sys.exit(1)

    # 4. Verifica Pasta RES (Recursos estáticos)
    res_dir = project_root / "res"

    # 5. Verifica TOML de Configuração de Banco (Crítico)
    # O sistema procura preferencialmente em /var conforme o padrão v0.3.8
    toml_path = var_dir / "db_config.toml"
    if not toml_path.exists():
        print(f"[ERRO CRÍTICO] Arquivo de configuração db_config.toml ausente.")
        sys.exit(1)

    # 6. Lê a configuração do Banco
    try:
        with open(toml_path, 'rb') as f:
            db_config = tomllib.load(f)
    except Exception as e:
        print(f"[ERRO CRÍTICO FATAL] Falha ao ler {toml_path.name}: {e}")
        sys.exit(1)

    # 7. Auto-Healing: Cria pastas auxiliares se não existirem
    logs_dir = var_dir / "logs"
    temp_dir = var_dir / "temp"

    for directory in (logs_dir, temp_dir):
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"[ERRO CRÍTICO] Sem permissão para criar diretório: {directory}")
                sys.exit(1)

    # 8. Retorna a "Verdade Absoluta" do ambiente
    return AppEnv(
        project_root=project_root,
        sia_package=sia_package,
        var_dir=var_dir,
        logs_dir=logs_dir,
        temp_dir=temp_dir,
        res_dir=res_dir,
        db_config=db_config
    )

# --- Instância Global Conveniente ---
# Importe 'env' nos outros módulos: from sia.core import env
env = bootstrap()