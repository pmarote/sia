# Análises Econômicas

```sia_var
OUT = "rel_an_econ.md"
where = "1 = 1"
limite = '5'
```

#### Link para o menu de relatórios: [Menu de relatórios](menu_relatorios.md)

## Receitas

```sql
SELECT
  Part, SUM(es_valconEFD) AS es_valconEFD, SUM(es_icmsEFD) AS es_icmsEFD, SUM(es_icmsstEFD) AS es_icmsstEFD,
  SUM(es_valconDFe) AS es_valconDFe, SUM(es_icmsDFe) AS es_icmsDFe, SUM(es_icmsstDFe) AS es_icmsstDFe
FROM an_econ_base
WHERE g1 = '1-Receitas'
GROUP BY cnpjPart14
ORDER BY es_valconEFD DESC
```

## Compras Insumos

```sql
SELECT
  Part, SUM(es_valconEFD) AS es_valconEFD, SUM(es_icmsEFD) AS es_icmsEFD, SUM(es_icmsstEFD) AS es_icmsstEFD,
  SUM(es_valconDFe) AS es_valconDFe, SUM(es_icmsDFe) AS es_icmsDFe, SUM(es_icmsstDFe) AS es_icmsstDFe
FROM an_econ_base
WHERE g1 = '2-Compras Insumos'
GROUP BY cnpjPart14
ORDER BY es_valconEFD
```

## Compras Consumo

```sql
SELECT
  Part, SUM(es_valconEFD) AS es_valconEFD, SUM(es_icmsEFD) AS es_icmsEFD, SUM(es_icmsstEFD) AS es_icmsstEFD,
  SUM(es_valconDFe) AS es_valconDFe, SUM(es_icmsDFe) AS es_icmsDFe, SUM(es_icmsstDFe) AS es_icmsstDFe
FROM an_econ_base
WHERE g1 = '3-Compras Consumo'
GROUP BY cnpjPart14
ORDER BY es_valconEFD
```

## Ativo

```sql
SELECT
  Part, SUM(es_valconEFD) AS es_valconEFD, SUM(es_icmsEFD) AS es_icmsEFD, SUM(es_icmsstEFD) AS es_icmsstEFD,
  SUM(es_valconDFe) AS es_valconDFe, SUM(es_icmsDFe) AS es_icmsDFe, SUM(es_icmsstDFe) AS es_icmsstDFe
FROM an_econ_base
WHERE g1 = '4-Ativo'
GROUP BY cnpjPart14
ORDER BY es_valconEFD
```

## Entradas/Saídas

```sql
SELECT
  Part, g2, g3 || ' ' || classe || ' ' || descri_simplif AS cfop_tipo,
  SUM(es_valconEFD) AS es_valconEFD, SUM(es_icmsEFD) AS es_icmsEFD, SUM(es_icmsstEFD) AS es_icmsstEFD,
  SUM(es_valconDFe) AS es_valconDFe, SUM(es_icmsDFe) AS es_icmsDFe, SUM(es_icmsstDFe) AS es_icmsstDFe
FROM an_econ_base
WHERE g1 = '5-Entradas/Saídas' AND g2 = '01z - Produção - Outros'
GROUP BY cnpjPart14, g2, g3, classe
ORDER BY cnpjOrder, cnpjPart14, g2, g3, classe
```

## Outros

```sql
SELECT
  Part, g2, g3 || ' ' || classe || ' ' || descri_simplif AS cfop_tipo,
  SUM(es_valconEFD) AS es_valconEFD, SUM(es_icmsEFD) AS es_icmsEFD, SUM(es_icmsstEFD) AS es_icmsstEFD,
  SUM(es_valconDFe) AS es_valconDFe, SUM(es_icmsDFe) AS es_icmsDFe, SUM(es_icmsstDFe) AS es_icmsstDFe
FROM an_econ_base
WHERE g1 = '6-Outros' OR (g1 = '5-Entradas/Saídas' AND g2 <> '01z - Produção - Outros')
GROUP BY cnpjPart14, g2, g3, classe
ORDER BY cnpjOrder, cnpjPart14, g2, g3, classe
```
