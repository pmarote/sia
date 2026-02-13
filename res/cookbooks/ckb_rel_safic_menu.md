# Análises do Safic

```sia_var
OUT = "rel_safic_menu.md"
where = "1 = 1"
limite = '5'
```

#### Link para o menu de relatórios: [Menu de relatórios](menu_relatorios.md)

## Resumão de Menu Safic

```sql
/* 1. Isola a junção base de documentos e atributos */
WITH DadosBase AS (
    SELECT 
        A.idClassificacao, 
        B.vlTotalDoc, 
        B.vlIcmsProprio, 
        B.vlIcmsSt
    FROM docatrib_fiscal_DocClassificado AS A
    LEFT JOIN docatrib_fiscal_DocAtributos AS B 
        ON B.idDocAtributos = A.idDocAtributos
),

/* 2. Junta com as tabelas de classificação e calcula os totais por Menu */
CalculoPorMenu AS (
    SELECT 
        DB.idClassificacao, 

        /* --- Lógica de Quebra de Linha: descMenu (PCD.descricao) --- */
        CASE 
            WHEN length(PCD.descricao) <= 60 THEN 
                PCD.descricao
            
            WHEN length(PCD.descricao) <= 120 THEN 
                substr(PCD.descricao, 1, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 61)

            WHEN length(PCD.descricao) <= 180 THEN 
                substr(PCD.descricao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 121)

            WHEN length(PCD.descricao) <= 240 THEN 
                substr(PCD.descricao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 121, 60) || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 181)

            ELSE /* Maior que 240 */
                substr(PCD.descricao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 121, 60) || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 181, 60) || '<br>&nbsp;&nbsp;' || 
                substr(PCD.descricao, 241)
        END AS descMenu,

        /* --- Lógica de Quebra de Linha: descricao (C.descricao) --- */
        CASE 
            WHEN length(C.descricao) <= 60 THEN 
                C.descricao
            
            WHEN length(C.descricao) <= 120 THEN 
                substr(C.descricao, 1, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 61)

            WHEN length(C.descricao) <= 180 THEN 
                substr(C.descricao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 121)

            WHEN length(C.descricao) <= 240 THEN 
                substr(C.descricao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 121, 60) || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 181)

            ELSE 
                substr(C.descricao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 121, 60) || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 181, 60) || '<br>&nbsp;&nbsp;' || 
                substr(C.descricao, 241)
        END AS descricao,

        /* --- Lógica de Quebra de Linha: descrParaAgregacao --- */
        CASE 
            WHEN length(C.descrParaAgregacao) <= 60 THEN 
                C.descrParaAgregacao
            
            WHEN length(C.descrParaAgregacao) <= 120 THEN 
                substr(C.descrParaAgregacao, 1, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 61)

            WHEN length(C.descrParaAgregacao) <= 180 THEN 
                substr(C.descrParaAgregacao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 121)

            WHEN length(C.descrParaAgregacao) <= 240 THEN 
                substr(C.descrParaAgregacao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 121, 60) || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 181)

            ELSE 
                substr(C.descrParaAgregacao, 1, 60)   || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 61, 60)  || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 121, 60) || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 181, 60) || '<br>&nbsp;&nbsp;' || 
                substr(C.descrParaAgregacao, 241)
        END AS descrParaAgregacao,

        COUNT(DB.idClassificacao)   AS qtdidClassificacao, 
        SUM(DB.vlTotalDoc)          AS vlTotalDoc, 
        SUM(DB.vlIcmsProprio)       AS vlIcmsProprio, 
        SUM(DB.vlIcmsSt)            AS vlIcmsSt
    FROM DadosBase AS DB
    LEFT JOIN _fiscal_Classificacao AS C 
        ON C.idClassificacao = DB.idClassificacao
    LEFT JOIN _fiscal_ParamConsultaDocClassificacao AS PCDC 
        ON PCDC.idClassificacao = DB.idClassificacao
    LEFT JOIN _fiscal_ParamConsultaDoc AS PCD 
        ON PCD.idParamConsultaDoc = PCDC.idParamConsultaDoc
    WHERE {where}
    GROUP BY DB.idClassificacao, PCD.descricao
)

/* 3. Agrupamento final: Consolida a lista de menus numa string só */
SELECT
    idClassificacao AS IdClassif, 
    group_concat(descMenu, ' <br> ') AS itens_menu, 
    descricao, 
    descrParaAgregacao, 
    qtdidClassificacao AS qtd, 
    vlTotalDoc, 
    vlIcmsProprio AS vlIcms, 
    vlIcmsSt
FROM CalculoPorMenu
GROUP BY idClassificacao;
```
