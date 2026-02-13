# Anáalises do Safic - Detalhes

```sia_var
OUT = "rel_safic_menu_det.md"
where = "1 = 1"
limite = '5'
top_n = '15'
order_by = 'sum(vl_icmsEFD) DESC, sum(vl_icmsDFe) DESC, sum(vl_icmsDFe) DESC'
campos_adic = ''
```

```sia_var
MENU_TOP_TEMPLATE = '''
WITH BaseDados AS (
    SELECT {campos_adic}
        tp_codSit, 
        tp_oper, 
        /* Lógica para quebrar linhas (Máximo 2 BRs) */
        CASE 
            WHEN length(Part) > 70 THEN 
                substr(Part, 1, 35) || '<br>' || substr(Part, 36, 35) || '<br>' || substr(Part, 71)
            WHEN length(Part) > 35 THEN 
                substr(Part, 1, 35) || '<br>' || substr(Part, 36)
            /* Se for pequeno, mantém original */
           ELSE Part 
        END AS Part,
        ChNrOrigem, 
        ChNrCfops,
        count(numero)        AS qtd, 
        sum(dif_vl_doc)      AS dif_vl_doc, 
        sum(dif_icms)        AS dif_icms, 
        sum(dif_icmsstSP)    AS dif_icmsstSP,
        sum(vl_icmsDFe)      AS vl_icmsDFe, 
        sum(vl_icmsEFD)      AS vl_icmsEFD, 
        sum(vl_icmsstSP_DFe) AS vl_icmsstSP_DFe, 
        sum(vl_icmsstSP_EFD) AS vl_icmsstSP_EFD,
		sum(vl_docDFe)       AS vl_docDFe,
		sum(vl_docEFD)       AS vl_docEFD,
        CASE 
            WHEN length(DFeDescris) > 70 THEN 
                substr(DFeDescris, 1, 35) || '<br>' || substr(DFeDescris, 36, 35) || '<br>' || substr(DFeDescris, 71, 35)
            WHEN length(DFeDescris) > 35 THEN 
                substr(DFeDescris, 1, 35) || '<br>' || substr(DFeDescris, 36)
            /* Se for pequeno, mantém original */
           ELSE DFeDescris
        END AS AmostraDFeDescris,
        CASE 
            WHEN length(obs) > 70 THEN 
                substr(obs, 1, 35) || '<br>' || substr(obs, 36, 35) || '<br>' || substr(obs, 71, 35)
            WHEN length(obs) > 35 THEN 
                substr(obs, 1, 35) || '<br>' || substr(obs, 36)
            /* Se for pequeno, mantém original */
           ELSE obs
        END AS AmostraObs,
        ROW_NUMBER() OVER (ORDER BY {order_by}) AS ranking
    FROM chaveNroTudao
    WHERE ChNrClassifs LIKE '%{classif}%'
    GROUP BY {campos_adic} tp_codSit, tp_oper, Part, ChNrOrigem, ChNrCfops
)
-- Top N
SELECT 
    {campos_adic} tp_codSit AS codSit, tp_oper AS op, Part, ChNrOrigem, ChNrCfops,
    qtd, dif_vl_doc, dif_icms, dif_icmsstSP,
    vl_icmsDFe AS icmsDFe, vl_icmsEFD AS icmsEFD, 
	vl_icmsstSP_DFe AS icmsstDFeSP, vl_icmsstSP_EFD AS icmsstEFDSP, 
	vl_docDFe, vl_docEFD,
	AmostraDFeDescris, AmostraObs
FROM BaseDados
WHERE ranking <= {top_n}

UNION ALL

-- Demais itens somados
SELECT {campos_adic}
    '---'                 AS tp_codSit,
    '---'                 AS tp_oper,
    'DEMAIS ITENS (SOMA)' AS Part,
    '---'                 AS ChNrOrigem,
    '---'                 AS ChNrCfops,
    SUM(qtd)              AS qtd,
    SUM(dif_vl_doc)       AS dif_vl_doc,
    SUM(dif_icms)         AS dif_icms,
    SUM(dif_icmsstSP)     AS dif_icmsstSP,
    SUM(vl_icmsDFe)       AS vl_icmsDFe,
    SUM(vl_icmsEFD)       AS vl_icmsEFD,
    SUM(vl_icmsstSP_DFe)  AS vl_icmsstSP_DFe,
    SUM(vl_icmsstSP_EFD)  AS vl_icmsstSP_EFD,
    SUM(vl_docDFe)        AS vl_docDFe,
    SUM(vl_docEFD)        AS vl_docEFD,
    AmostraDFeDescris, AmostraObs
FROM BaseDados
WHERE ranking > {top_n}
HAVING COUNT(*) > 0;
'''
```

#### Link para o menu de relatórios: [Menu de relatórios](menu_relatorios.md)

## Resumão de Menu Safic

### [2] E 1.13 - documentos escriturados em duplicidade

```sql
SELECT tp_codSit, tp_oper, Part, ChNrOrigem, ChNrCfops,
count(numero) AS qtd, sum(dif_vl_doc) AS dif_vl_doc, 
sum(dif_icms) AS dif_icms, sum(dif_icmsstSP) AS dif_icmsstSP,
sum(vl_icmsDFe) AS vl_icmsDFe, sum(vl_icmsEFD) AS vl_icmsEFD, 
sum(vl_icmsstSP_DFe) AS vl_icmsstSP_DFe, sum(vl_icmsstSP_EFD) AS vl_icmsstSP_EFD
FROM
(SELECT * FROM chaveNroTudao
WHERE ChNrClassifs LIKE "%[2]%"
ORDER BY numero)
GROUP BY tp_codSit, tp_oper, Part, ChNrOrigem, ChNrCfops
ORDER BY dif_icms
```

### [9] E 1.17 - operações realizadas com fornecedores com a inscrição suspensa, inapta, baixada ou nula no cadastro de contribuintes

```sql
SELECT tp_codSit, tp_oper, Part, ChNrOrigem, ChNrCfops,
count(numero) AS qtd, sum(dif_vl_doc) AS dif_vl_doc, 
sum(dif_icms) AS dif_icms, sum(dif_icmsstSP) AS dif_icmsstSP,
sum(vl_icmsDFe) AS vl_icmsDFe, sum(vl_icmsEFD) AS vl_icmsEFD, 
sum(vl_icmsstSP_DFe) AS vl_icmsstSP_DFe, sum(vl_icmsstSP_EFD) AS vl_icmsstSP_EFD
FROM
(SELECT * FROM chaveNroTudao
WHERE ChNrClassifs LIKE "%[9]%"
ORDER BY numero)
GROUP BY tp_codSit, tp_oper, Part, ChNrOrigem, ChNrCfops
ORDER BY dif_icms
```

### [12] E 1.14 - crédito de ICMS operação própria maior que o destacado no documento fiscal

```sql
-- classif = '[12]'
-- top_n = '18'
-- order_by = 'sum(dif_icms)'
{MENU_TOP_TEMPLATE}
```

### [14] E 1.20 - documentos de entrada não escriturados

```sql
-- classif = '[14]'
-- top_n = '18'
-- order_by = 'sum(dif_vl_doc) DESC'
{MENU_TOP_TEMPLATE}
```

### [15] S 1.1 - inconsistência na escrituração: saídas não escrituradas

```sql
-- classif = '[15]'
-- top_n = '18'
-- order_by = 'sum(dif_vl_doc) DESC'
{MENU_TOP_TEMPLATE}
```

### [16] S 1.1 - E 1.6 - simulação de entrada: documentos CANCELADOS escriturados como Válidos, mas são entradas SEM crédito

```sql
-- classif = '[16]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [20] NFes, CTes, NFCes e CFe SATs CANCELADOS destinados ao contribuinte auditado

```sql
-- classif = '[20]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [35] CIAP 1.2 - saída de bens do ativo imobilizado

```sql
-- classif = '[35]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [36] CIAP 1.3 - apropriação de crédito de ativo imobilizado

```sql
-- classif = '[36]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [41] operações com energia elétrica

```sql
-- classif = '[41]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [42] operações de aquisição de transporte

```sql
-- classif = '[42]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [43] operações de serv. de comunicação

```sql
-- classif = '[43]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [46] ES 1.1 - análise de operações com industrialização

```sql
-- classif = '[46]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [48] E 1.17 - operações realizadas com fornecedores com a inscrição suspensa...

```sql
-- classif = '[48]'
-- order_by = 'sum(dif_vl_doc) DESC'
{MENU_TOP_TEMPLATE}
```

### [53] 9.3 l) margem de lucro ou preço de varejo inferior ao previsto na legislação nas operações de substituição tributária

```sql
-- classif = '[53]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [56] S 1.9 - operações com destinatários inscritos no cadastro de contribuintes, com situação cadastral inativa

```sql
-- classif = '[56]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [62] S 1.8 - operações com destinatários incluídos no cadastro de inidôneos

```sql
-- classif = '[62]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [63] S 1.8 - operações com destinatários incluídos no cadastro de inidôneos

```sql
-- classif = '[63]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [64] E 1.18 - crédito de operações próprias com substituição tributária

```sql
-- classif = '[64]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [67] S 2.6 - operações com destinatários localizados no Estado, mas não inscritos no cadastro de contribuintes

```sql
-- classif = '[67]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [69] E 1.16 - crédito indevido: entrada escriturada com CFOP que geralmente não aceita crédito

```sql
-- classif = '[69]'
{MENU_TOP_TEMPLATE}
```

### [70] CIAP 1.1 - entrada de bens para o ativo imobilizado

```sql
-- classif = '[70]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [71] E 3.1 - análise de entradas interestaduais de produtos importados, com alíquota do imposto superior a 4%

```sql
-- classif = '[71]'
{MENU_TOP_TEMPLATE}
```

### [72] E 3.2 - análise de crédito em operações com devolução de mercadorias

```sql
-- classif = '[72]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [73] ES 1.4 - análise de operações com CFOP 1949 / 2949 / 3949 / 5949 / 6949 / 7949

```sql
-- classif = '[73]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [90] E 3.4 - análise de operações de devolução de mercadorias de maior valor

```sql
-- classif = '[90]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [98] E 1.5 - crédito indevido: documentos CANCELADOS escriturados COM crédito

```sql
-- classif = '[98]'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [99] E 1.7 - crédito indevido: documento fiscal de saída escriturado como entrada com crédito

```sql
-- classif = '[99]'
{MENU_TOP_TEMPLATE}
```
	
### [100] E 1.15 - crédito de ICMS ST maior que o destacado no documento fiscal

```sql
-- classif = '[100]'
{MENU_TOP_TEMPLATE}
```

### [104] S 1.3 - débito a menor: saídas regulares escrituradas como canceladas ou denegadas

```sql
-- classif = '[104]'
{MENU_TOP_TEMPLATE}
```

### [106] S 1.10 - documentos eletrônicos emitidos com sequência numérica com intervalos

```sql
-- classif = '[106]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [108] S 1.11 - nota fiscal cancelada após o prazo de 24h da emissão

```sql
-- classif = '[108]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [109] E 2.5 - operações de entrada escrituradas com crédito de ICMS OP

```sql
-- classif = '[109]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [111] AP 1.4 - verificação do Difal nas operações de entrada interestaduais com uso e consumo e ativo imobilizado

```sql
-- classif = '[111]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [114] NFes de emissão própria escrituradas com crédito

```sql
-- classif = '[114]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [115] NFes de emissão de terceiro escrituradas com crédito

```sql
-- classif = '[115]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [117] E 1.12 - simulação de entrada: escrituração, sem crédito, de documento com manifestação do destinatário negando a operação

```sql
-- classif = '[117]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [118] 118	S 1.16 - operações de saída escrituradas, com débito, de documento com manifestação do destinatário negando a operação

```sql
-- classif = '[118]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [284] S 1.23 - operações internas de saída para contribuinte sem escrituração na EFD do participante

```sql
-- classif = '[284]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [285] S 1.24 - operações interestaduais de saída para contribuinte sem escrituração na EFD do participante

```sql
-- classif = '[285]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [367] E 2.2 - análise de alíquotas de operações internas

```sql
-- classif = '[367]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [368] E 2.3 - análise de alíquotas de operações interestaduais

```sql
-- classif = '[368]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [371] E 4.0 - análise de devoluções com lig. de ítem emissão própria

```sql
-- classif = '[371]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [372] 4.0 - análise de devoluções com lig. de ítem emissão terceiros

```sql
-- classif = '[372]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [374] E 4.2 - análise de devoluções sem lig. de ítem emissão terceiros

```sql
-- classif = '[374]'
-- top_n = '18'
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [375] E 2.2 - análise de alíquotas de operações internas

```sql
-- classif = '[375]'
-- top_n = '18'
-- campos_adic = 'DFeAliqs, EfdAliqs, '
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```

### [376] E 2.4 - análise de alíquota em operações de transporte

```sql
-- classif = '[376]'
-- top_n = '18'
-- campos_adic = 'DFeAliqs, EfdAliqs, '
-- order_by = 'sum(vl_docDFe) DESC'
{MENU_TOP_TEMPLATE}
```
