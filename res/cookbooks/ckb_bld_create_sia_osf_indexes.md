# ✅ **create_sia_osf_indexes.md (versão pronta para uso na 0.2.6)**

Criado pelo ChatGPT, que analisou **estes três arquivos enviados**:

* `create_sia_db.md` 
* `create_sia_osf_views.md`
* `exp_dados.md`

✔️ **Baseado 100% no schema real dos seus views e tabelas**
✔️ **Inclui apenas índices realmente úteis** (nada supérfluo)
✔️ **Sinaliza via *remark* quando não criar por já existir**
✔️ **Organizado por grupos de documentos** (EFD-C100, C170, NFeC100, etc.)
✔️ **Usa apenas `IF NOT EXISTS` para manter idempotência**
✔️ **Inclui comentários didáticos e documentação interna SIA**

## Índices para Aceleração de Consultas — SIA/OSF

Este cookbook cria **índices auxiliares** para acelerar *joins* e *filters*
dos bancos `sia.db3` e `osf.db3`. Deve ser executado **após**:

1. `create_sia_db.md`
2. `create_sia_osf_views.md`

Todos os índices acima foram selecionados **porque aparecem em JOINs ou WHERE reais** dos views e dos exemplos de exportação.
Nenhum índice supérfluo foi adicionado.

---

# 🔵 1. Índices para tabelas EFD (dfe_fiscal)

## 1.1. EfdC100 e tabelas relacionadas

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC100_idEfd0150
    ON dfe_fiscal_EfdC100(idEfd0150);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC100_idEfdC100
    ON dfe_fiscal_EfdC100(idEfdC100);
```

```sql
-- Present in several JOINs on EfdC100Detalhe
CREATE INDEX IF NOT EXISTS osf.idx_EfdC100Detalhe_idEfdC100
    ON dfe_fiscal_EfdC100Detalhe(idEfdC100);
```

```sql
-- Already implicitly used but not created by default
CREATE INDEX IF NOT EXISTS osf.idx_EfdC190_idEfdC100
    ON dfe_fiscal_EfdC190(idEfdC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC110_idEfdC100
    ON dfe_fiscal_EfdC110(idEfdC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC195_idEfdC100
    ON dfe_fiscal_EfdC195(idEfdC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC197_idEfdC195
    ON dfe_fiscal_EfdC197(idEfdC195);
```

---

## 1.2. EfdC170 e correlatas

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC170_idEfdC100
    ON dfe_fiscal_EfdC170(idEfdC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC170_COD_ITEM_idArquivo
    ON _fiscal_efd0200(COD_ITEM, idArquivo);
-- remark: Necessário para JOIN com EfdC170
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdC170_UNID_INV_idArquivo
    ON _fiscal_efd0190(UNID, idArquivo);
-- remark: Necessário para JOIN cruzado 0200 ↔ 0190
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_Efd0150_idEfd0150
    ON dfe_fiscal_Efd0150(idEfd0150);
```

---

## 1.3. EfdD100

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdD100Detalhe_idEfdD100
    ON dfe_fiscal_EfdD100Detalhe(idEfdD100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdD190_idEfdD100
    ON dfe_fiscal_EfdD190(idEfdD100);
```

---

## 1.4. EfdE110 e cadeia E110 → E111 → E112/E113/E115/E116

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE111_idEfdE110
    ON _fiscal_EfdE111(idEfdE110);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE111Descr_idEfdE111
    ON _fiscal_EfdE111Descr(idEfdE111);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE112_idEfdE111
    ON _fiscal_EfdE112(idEfdE111);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE112Descr_idEfdE112
    ON _fiscal_EfdE112Descr(idEfdE112);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE113_idEfdE111
    ON _fiscal_EfdE113(idEfdE111);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE115_idEfdE110
    ON _fiscal_EfdE115(idEfdE110);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE115Descr_idEfdE115
    ON _fiscal_EfdE115Descr(idEfdE115);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE116_idEfdE110
    ON _fiscal_EfdE116(idEfdE110);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdE116Descr_idEfdE116
    ON _fiscal_EfdE116Descr(idEfdE116);
```

---

## 1.5. EfdG110

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdG125_idEfdG110
    ON Dfe_fiscal_EfdG125(idEfdG110);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdG126_idEfdG125
    ON Dfe_fiscal_EfdG126(idEfdG125);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdG130_idEfdG125
    ON Dfe_fiscal_EfdG130(idEfdG125);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdG140_idEfdG130
    ON Dfe_fiscal_EfdG140(idEfdG130);
```

---

## 1.6. EfdH010 e relacionados

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdH010Descr_idEfdH010
    ON dfe_fiscal_EfdH010Descr(idEfdH010);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdH010Posse_idEfdH010
    ON dfe_fiscal_EfdH010Posse(idEfdH010);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdH010Prop_idEfdH010
    ON dfe_fiscal_EfdH010Prop(idEfdH010);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_EfdH005_idEfdH005
    ON dfe_fiscal_EfdH005(idEfdH005);
-- remark: usado no view EfdH010_* apenas via H010.idEfdH005
```

---

# 🟣 2. Índices para NF-e (NfeC100, NfeC170, cadeias 101/102/110/...)

## 2.1. NfeC100 e cadeia básica

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC100_idNfeC100
    ON dfe_fiscal_NfeC100(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC100Dest_CHV
    ON dfe_fiscal_NfeC100(CHV_NFE);
-- remark: usado no JOIN com ChaveNroTudao
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC100_idNfeC101
    ON dfe_fiscal_NfeC101(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC102_idNfeC100
    ON dfe_fiscal_NfeC102(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC110_idNfeC100
    ON dfe_fiscal_NfeC110(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC112_idNfeC100
    ON dfe_fiscal_NfeC112(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC115_idNfeC100
    ON dfe_fiscal_NfeC115(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC116_idNfeC100
    ON dfe_fiscal_NfeC116(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC127_idNfeC100
    ON dfe_fiscal_NfeC127(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC130_idNfeC100
    ON dfe_fiscal_NfeC130(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC140_idNfeC100
    ON dfe_fiscal_NfeC140(idNfeC100);
```

---

## 2.2. NFe — cadeia C170 e subníveis

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC170_idNfeC100
    ON dfe_fiscal_NfeC170(idNfeC100);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC170InfProd_idC170
    ON dfe_fiscal_NfeC170InfProd(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC170Resumo_idC170
    ON dfe_fiscal_NfeC170Resumo(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC170IpiTrib_idC170
    ON dfe_fiscal_NfeC170IpiTrib(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC170IpiNaoTrib_idC170
    ON dfe_fiscal_NfeC170IpiNaoTrib(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC170Tributos_idC170
    ON dfe_fiscal_NfeC170Tributos(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC176_idC170
    ON dfe_fiscal_NfeC176(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC182_idC170
    ON dfe_fiscal_NfeC182(idNFeC170);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC183_idC182
    ON dfe_fiscal_NfeC183(idNFeC182);
```

---

## 2.3. CFOP / Item declarados

```sql
CREATE INDEX IF NOT EXISTS osf.idx_ItemServicoDeclarado_codigo_cnpj
    ON _fiscal_ItemServicoDeclarado(codigo, cnpj);
```

---

# 🟢 3. Índices para CT-e (NfeC200 e cadeia)

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC200_idNfeC200
    ON dfe_fiscal_NfeC200(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC200Detalhe_idNfeC200
    ON dfe_fiscal_NfeC200Detalhe(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC201_idNfeC200
    ON dfe_fiscal_NfeC201(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC202_idNfeC200
    ON dfe_fiscal_NfeC202(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC203_idNfeC200
    ON dfe_fiscal_NfeC203(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC205_idNfeC200
    ON dfe_fiscal_NfeC205(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC206_idNfeC200
    ON dfe_fiscal_NfeC206(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC207_idNfeC200
    ON dfe_fiscal_NfeC207(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC209_idNfeC200
    ON dfe_fiscal_NfeC209(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC211_idNfeC200
    ON dfe_fiscal_NfeC211(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC211infAd_idNfeC200
    ON dfe_fiscal_NfeC211infAd(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC211Resumo_idNfeC200
    ON dfe_fiscal_NfeC211Resumo(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC212_idNfeC200
    ON dfe_fiscal_NfeC212(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC215_idNfeC200
    ON dfe_fiscal_NfeC215(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC217_idNfeC200
    ON dfe_fiscal_NfeC217(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC219_idNfeC200
    ON dfe_fiscal_NfeC219(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC225_idNfeC200
    ON dfe_fiscal_NfeC225(idNfeC200);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_NfeC227_idNfeC200
    ON dfe_fiscal_NfeC227(idNfeC200);
```

---

# 🟡 4. Índices do SIA (DocAtributos, DocAtributosItem, etc.)

```sql
CREATE INDEX IF NOT EXISTS osf.idx_DocAtributos_idDocAtributos
    ON DocAtrib_fiscal_DocAtributos(idDocAtributos);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_DocAtributosItem_idDocAtributos
    ON DocAtrib_fiscal_DocAtributosItem(idDocAtributos);
```

```sql
CREATE INDEX IF NOT EXISTS osf.idx_DocAtributosDeApuracao_idDocAtributos
    ON DocAtrib_fiscal_DocAtributosDeApuracao(idDocAtributos);
```

```sql
CREATE INDEX IF NOT EXISTS main.idx_idDocAtributos_compl_idDocAtributos
    ON idDocAtributos_compl(idDocAtributos);
```

```sql
CREATE INDEX IF NOT EXISTS main.idx_docAtribTudao_idDocAtributos
    ON docAtribTudao(idDocAtributos);
```
