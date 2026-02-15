---
trigger: always_on
---

# Regras de Execução (SIA Project)

Este projeto utiliza Python PORTÁTIL (Embedded) em `usr/python`.

## Ambiente
- O ambiente Python é isolado. A presença do arquivo `python*._pth` faz com que o `PYTHONPATH` seja **ignorado**.
- O diretório raiz do projeto sia foi adicionado como raiz de importação no `._pth`.
- Utilize `usr/python/python.exe` para garantir o uso do interpretador correto.

## Como Executar
1. Execute módulos a partir dr qualquer pasta, utilize o comando `-m` seguido do caminho do módulo **com** o prefixo `sia`.

   Exemplos:
   - `python -m sia.utils.info`
   - `python -m sia.main` (executa `sia/main.py`)

## Diagnóstico
Em caso de erro de importação ou dúvida sobre o ambiente, execute:
`python -m sia.utils.info`

## Dependências
Nunca tente instalar pacotes no Python global do sistema. Use o Python em `usr/python`.