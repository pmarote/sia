---
trigger: always_on
---

# Regras de Execução (SIA Project)

Este projeto utiliza Python PORTÁTIL (Embedded) em `usr/python`.

## Ambiente
- O ambiente Python é isolado. A presença do arquivo `python*._pth` faz com que o `PYTHONPATH` seja **ignorado**.
- O diretório `app` foi adicionado como raiz de importação no `._pth`.
- Utilize `usr/python/python.exe` para garantir o uso do interpretador correto.

## Como Executar
1. Sempre execute módulos a partir da raiz do projeto (`c:\srcP\sia`).
2. Utilize o comando `-m` seguido do caminho do módulo **sem** o prefixo `app`.

   Exemplos:
   - `usr\python\python.exe -m utils.info`
   - `usr\python\python.exe -m main` (se existir `app/main.py`)

3. **Dica:** Se o comando `python` no seu terminal já aponta para `usr/python/python.exe` (via `settings.json`), você pode usar:
   `python -m utils.info`

## Diagnóstico
Em caso de erro de importação ou dúvida sobre o ambiente, execute:
`usr\python\python.exe -m utils.info`

## Dependências
Nunca tente instalar pacotes no Python global do sistema. Use o Python em `usr/python`.