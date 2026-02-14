---
name: sia.report
description: Especialista em geração de relatórios (Markdown, Excel, HTML), exportação de dados e execução de SQL via módulo `app.reporter`. Use esta skill para transformar dados brutos em documentos finais.
---

# SIA Reporting & Data Extraction

Esta skill gerencia a camada de **Saída (Output)** do sistema SIA. Sua função principal é extrair dados de bancos SQLite e formatá-los para consumo humano ou auditoria.

## 1. O Motor: `app.reporter`
O módulo `app.reporter` é o coração da extração. Ele suporta execução de queries, anexação de múltiplos bancos (ATTACH) e formatação automática.

### A. Modo CLI (Linha de Comando)
Ideal para consultas rápidas (`ad-hoc`) ou testes simples.

**Sintaxe:**
```powershell
sia app.reporter --db <caminho_banco> --sql "<query>" --format <fmt> --out <arquivo_saida>
```

**Exemplo:**

```powershell
sia app.reporter --db data/entrada/sped.sqlite --sql "SELECT * FROM notas WHERE valor > 1000" --format excel --out data/saida/auditoria_notas.xlsx

```

### B. Modo JSON (Configuração Avançada)

Ideal para rotinas complexas, relatórios oficiais e junção de múltiplos bancos (ex: Cruzamento SPED vs Contabilidade).

**Sintaxe:**

```powershell
sia app.reporter --json res/cookbooks/auditoria_icms.json

```

**Estrutura do JSON de Configuração:**
O arquivo de configuração deve seguir este esquema estrito:

```json
{
  "db": "data/entrada/principal.sqlite",    // Banco principal (main)
  "out": "data/saida/relatorio_final.md",   // Caminho de saída
  "format": "markdown",                     // Opções: markdown, excel, html, csv
  "sql": "SELECT p.nome, a.valor FROM main.usuarios p JOIN extra.auditoria a ON p.id = a.user_id",
  "attach": [
    // Lista de bancos auxiliares para o comando ATTACH DATABASE
    { "path": "data/entrada/extra_data.sqlite", "alias": "extra" },
    { "path": "data/entrada/auxiliar.sqlite", "alias": "aux" }
  ],
  "title": "Relatório de Auditoria Fiscal"  // Título para o cabeçalho (opcional)
}

```

## 2. Formatos e Assets

O sistema segue a filosofia **"Text-First"**, priorizando formatos abertos e legíveis.

### Markdown & HTML

* **Templates:** Devem ser armazenados em `res/templates/`.
* **Imagens:** Logos e diagramas devem ser lidos de `res/assets/img/`.
* **Estilos:** CSS para relatórios HTML ficam em `res/assets/styles/`.

### Excel

* Use apenas para dados tabulares brutos que exigem recálculo pelo usuário.
* Formatação visual deve ser mínima (cabeçalhos em negrito), priorizando os dados.

## 3. Regras de Desenvolvimento

1. **Caminhos Relativos:** Nunca use caminhos absolutos no JSON ou na CLI. Tudo é relativo à raiz do projeto (`cwd`).
2. **Encoding:** O output de texto (Markdown/HTML/JSON) deve ser sempre **UTF-8**.
3. **Não-Destrutivo:** O `app.reporter` nunca deve alterar os bancos de dados de entrada (`db` ou `attach`). Apenas leitura (`SELECT`).

### Detalhes Importantes:
1.  **Ajuste de Caminho:** Usei `sia app.reporter` em vez de apenas `reporter`, assumindo que seu código está dentro da pasta `app` (padrão MVC definido no `main`). Se estiver na raiz, você pode ajustar.
2.  **Integração:** Citei as pastas `/data/entrada` e `/res/cookbooks` para reforçar o padrão de organização.
