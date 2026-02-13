# Criação de Views nos db3s sia e osf

## Criação de Views no db3 sia

## Criação de Views no db3 osf

```sql
DROP VIEW IF EXISTS osf.EfdC100_EfdC100Detalhe_Efd0150
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdC100_EfdC100Detalhe_Efd0150 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 0 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
  '[EfdC100]' AS tA, A.*, '[EfdC100Detalhe]' AS tB, B.*, '[Efd0150]' AS tG, G.*
   FROM dfe_fiscal_EfdC100 AS A
   LEFT OUTER JOIN dfe_fiscal_EfdC100Detalhe AS B ON B.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_Efd0150 AS G ON G.idEfd0150 = A.idEfd0150
```

```sql
DROP VIEW IF EXISTS osf.EfdC170_Efd0200_Efd0190_EfdC100_EfdC100Detalhe_Efd0150
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdC170_Efd0200_Efd0190_EfdC100_EfdC100Detalhe_Efd0150 AS
SELECT
  CASE WHEN B.IND_EMIT = 0 THEN
      CASE WHEN B.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN B.IND_OPER = 0 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN B.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN B.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN B.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN B.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
   '[EfdC170]' AS tA, A.*, '[Efd0200]' AS tD, D.*, '[Efd0190]' AS tE, E.*,
   '[EfdC100]' AS tB, B.*, '[EfdC100Detalhe]' AS tC, C.*, '[Efd0150]' AS tG, G.*
   FROM dfe_fiscal_EfdC170 AS A
   LEFT OUTER JOIN _fiscal_efd0200 AS D ON D.COD_ITEM = A.COD_ITEM AND D.idArquivo = A.idArquivo
   LEFT OUTER JOIN _fiscal_efd0190 AS E ON E.UNID = D.UNID_INV AND E.idArquivo = A.idArquivo
   LEFT OUTER JOIN dfe_fiscal_EfdC100 AS B ON B.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_EfdC100Detalhe AS C ON C.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_Efd0150 AS G ON G.idEfd0150 = B.idEfd0150
```

```sql
DROP VIEW IF EXISTS osf.EfdC100_EfdC100Detalhe_Efd0150_EfdC190
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdC100_EfdC100Detalhe_Efd0150_EfdC190 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 0 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
'[EfdC100]' AS tA, A.*, '[EfdC100Detalhe]' AS tB, '[Efd0150]' AS tG, G.*, B.*,
'[EfdC190]' AS tD, D.*
   FROM dfe_fiscal_EfdC190 AS D
   LEFT OUTER JOIN dfe_fiscal_EfdC100 AS A ON A.idEfdC100 = D.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_EfdC100Detalhe AS B ON B.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_Efd0150 AS G ON G.idEfd0150 = A.idEfd0150
```

```sql
DROP VIEW IF EXISTS osf.EfdC100_EfdC100Detalhe_Efd0150_EfdC110_EfdC190_EfdC195_EfdC197
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdC100_EfdC100Detalhe_Efd0150_EfdC110_EfdC190_EfdC195_EfdC197 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 0 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
'[EfdC100]' AS tA, A.*, '[EfdC100Detalhe]' AS tB, '[Efd0150]' AS tG, G.*, B.*, '[EfdC110]' AS tC, C.*,
'[EfdC190]' AS tD, D.*, '[EfdC195]' AS tE, E.*, '[EfdC197]' AS tF, F.*
   FROM dfe_fiscal_EfdC100 AS A
   LEFT OUTER JOIN dfe_fiscal_EfdC100Detalhe AS B ON B.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_EfdC110 AS C ON C.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_EfdC190 AS D ON D.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_EfdC195 AS E ON E.idEfdC100 = A.idEfdC100
   LEFT OUTER JOIN dfe_fiscal_EfdC197 AS F ON F.idEfdC195 = E.idEfdC195
   LEFT OUTER JOIN dfe_fiscal_Efd0150 AS G ON G.idEfd0150 = A.idEfd0150
```

```sql
DROP VIEW IF EXISTS osf.EfdD100_EfdD100Detalhe_EfdD190
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdD100_EfdD100Detalhe_EfdD190 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 0 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
   '[EfdD100]' AS tA, A.*, '[EfdD100Detalhe]' AS tB, B.*, '[EfdD190]' AS tC, C.*
   FROM dfe_fiscal_EfdD100 AS A
   LEFT OUTER JOIN dfe_fiscal_EfdD100Detalhe AS B ON B.idEfdD100 = A.idEfdD100
   LEFT OUTER JOIN dfe_fiscal_EfdD190 AS C ON C.idEfdD100 = A.idEfdD100
```

```sql
DROP VIEW IF EXISTS osf.EfdE110_EfdE111_EfdE111Descr_EfdE112_EfdE112Descr_EfdE113_EfdE115_EfdE115Descr_EfdE116_EfdE116Descr
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdE110_EfdE111_EfdE111Descr_EfdE112_EfdE112Descr_EfdE113_EfdE115_EfdE115Descr_EfdE116_EfdE116Descr AS
SELECT '[EfdE110]' AS tA, A.*, '[EfdE111]' AS tB, B.*, '[EfdE111Descr]' AS tC, C.*,
   '[EfdE112]' AS tD, D.*, '[EfdE112Descr]' AS tE, E.*,
   '[EfdE113]' AS tF, F.*,
   '[EfdE115]' AS tH, H.*, '[EfdE115Descr]' AS tI, I.*,
   '[EfdE116]' AS tJ, J.*, '[EfdE116Descr]' AS tK, K.*
   FROM _fiscal_EfdE110 AS A
   LEFT OUTER JOIN _fiscal_EfdE111 AS B ON B.idEfdE110 = A.idEfdE110
   LEFT OUTER JOIN _fiscal_EfdE111Descr AS C ON C.idEfdE111 = B.idEfdE111
   LEFT OUTER JOIN _fiscal_EfdE112 AS D ON D.idEfdE111 = B.idEfdE111
   LEFT OUTER JOIN _fiscal_EfdE112Descr AS E ON E.idEfdE112 = D.idEfdE112
   LEFT OUTER JOIN _fiscal_EfdE113 AS F ON F.idEfdE111 = B.idEfdE111
   LEFT OUTER JOIN _fiscal_EfdE115 AS H ON H.idEfdE110 = A.idEfdE110
   LEFT OUTER JOIN _fiscal_EfdE115Descr AS I ON I.idEfdE115 = H.idEfdE115
   LEFT OUTER JOIN _fiscal_EfdE116 AS J ON J.idEfdE110 = A.idEfdE110
   LEFT OUTER JOIN _fiscal_EfdE116Descr AS K ON K.idEfdE116 = J.idEfdE116
```

```sql
DROP VIEW IF EXISTS osf.EfdG110_EfdG125_EfdG126
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdG110_EfdG125_EfdG126 AS
SELECT '[EfdG110]' AS tA, A.*, '[EfdG125]' AS tB, B.*, '[EfdG126]' AS tC, C.*
   FROM Dfe_fiscal_EfdG110 AS A
   LEFT OUTER JOIN Dfe_fiscal_EfdG125 AS B ON B.idEfdG110 = A.idEfdG110
   LEFT OUTER JOIN Dfe_fiscal_EfdG126 AS C ON C.idEfdG125 = B.idEfdG125
```

```sql
DROP VIEW IF EXISTS osf.EfdG110_EfdG125_EfdG126_EfdG130_EfdG140
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdG110_EfdG125_EfdG126_EfdG130_EfdG140 AS
SELECT '[EfdG110]' AS tA, A.*, '[EfdG125]' AS tB, B.*, '[EfdG126]' AS tC, C.*, '[EfdG130]' AS tD, D.*, '[EfdG140]' AS tE, E.*
   FROM Dfe_fiscal_EfdG110 AS A
   LEFT OUTER JOIN Dfe_fiscal_EfdG125 AS B ON B.idEfdG110 = A.idEfdG110
   LEFT OUTER JOIN Dfe_fiscal_EfdG126 AS C ON C.idEfdG125 = B.idEfdG125
   LEFT OUTER JOIN Dfe_fiscal_EfdG130 AS D ON D.idEfdG125 = B.idEfdG125
   LEFT OUTER JOIN Dfe_fiscal_EfdG140 AS E ON E.idEfdG130 = D.idEfdG130
```

```sql
DROP VIEW IF EXISTS osf.EfdH010_ItemServicoDeclarado_EfdH005_EfdH010Descr_EfdH010Posse_EfdH010Prop
```

```sql
CREATE VIEW IF NOT EXISTS osf.EfdH010_ItemServicoDeclarado_EfdH005_EfdH010Descr_EfdH010Posse_EfdH010Prop AS
SELECT '[EfdH010]' AS tA, A.*, '[ItemServicoDeclarado]' AS tE, E.*, '[EfdH005]' AS tF, F.*, '[EfdH010Descr]' AS tB, B.*, '[EfdH010Posse]' AS tC, C.*, '[EfdH010Prop]' AS tD, D.*
   FROM dfe_fiscal_EfdH010 AS A
   LEFT OUTER JOIN dfe_fiscal_EfdH005 AS F ON F.idEfdH005 = A.idEfdH005
   LEFT OUTER JOIN dfe_fiscal_EfdH010Descr AS B ON B.idEfdH010 = A.idEfdH010
   LEFT OUTER JOIN dfe_fiscal_EfdH010Posse AS C ON C.idEfdH010 = A.idEfdH010
   LEFT OUTER JOIN dfe_fiscal_EfdH010Prop AS D ON D.idEfdH010 = A.idEfdH010
   LEFT OUTER JOIN _fiscal_ItemServicoDeclarado AS E ON E.codigo = A.COD_ITEM AND E.cnpj = D.CnpjCpf
```

```sql
DROP VIEW IF EXISTS osf.Efd0200_Efd0205_ItemServicoDeclarado
```

```sql
CREATE VIEW IF NOT EXISTS osf.Efd0200_Efd0205_ItemServicoDeclarado AS
SELECT '[Efd0200]' AS tA, A.*,'[Efd0205]' AS tB, B.*, '[ItemServicoDeclarado]' AS tC, C.*
   FROM _fiscal_Efd0200 AS A
   LEFT OUTER JOIN _fiscal_Efd0205 AS B ON B.idEfd0200 = A.idEfd0200
   LEFT OUTER JOIN _fiscal_Efd0206 AS C ON C.idEfd0200 = B.idEfd0200
```

```sql
DROP VIEW IF EXISTS osf.NfeC100_NfeC100Detalhe_NfeC101_NfeC102_NfeC110_NfeC112_NfeC115_NfeC116_NfeC127_NfeC130_NfeC140
```

```sql
CREATE VIEW IF NOT EXISTS osf.NfeC100_NfeC100Detalhe_NfeC101_NfeC102_NfeC110_NfeC112_NfeC115_NfeC116_NfeC127_NfeC130_NfeC140 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 1 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
'[NfeC100]' AS tA, A.*,
CASE WHEN A.IND_EMIT = 0 THEN A.CnpjDest || '_' || D.UF || '_' || D.NOME ELSE A.CnpjEmit || '_' || C.UF || '_' || C.NOME END AS Part,
'[NfeC100Detalhe]' AS tB, B.*, '[NfeC101-Emit]' AS tC, C.*,
'[NfeC102-Dest]' AS tD, D.*,
'[NfeC110-Obs]' AS tG, G.*, '[NfeC112-NFeReferenciada]' AS tH, H.*, '[NfeC115-Coleta]' AS tI, I.*,
'[NfeC116-Entrega]' AS tJ, J.*, '[NfeC127]' AS tL, L.*,
'[NfeC130-DemaisTribs]' AS tM, M.*, '[NfeC140-Fat]' AS tN, N.*
   FROM dfe_fiscal_NfeC100 AS A
   LEFT OUTER JOIN dfe_fiscal_NfeC100Detalhe AS B ON B.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC101 AS C ON C.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC102 AS D ON D.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC110 AS G ON G.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC112 AS H ON H.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC115 AS I ON I.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC116 AS J ON J.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC127 AS L ON L.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC130 AS M ON M.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC140 AS N ON N.idNfeC100 = A.idNfeC100
```

```sql
DROP VIEW IF EXISTS osf.NfeC100_PodeDuplicar_NfeC100Detalhe_NfeC101_NfeC102_NfeC103_NfeC104_NfeC106_NfeC110_NfeC112_NfeC115_NfeC116_NfeC119_NfeC127_NfeC130_NfeC140_NfeC141_NfeC160
```

```sql
CREATE VIEW IF NOT EXISTS osf.NfeC100_PodeDuplicar_NfeC100Detalhe_NfeC101_NfeC102_NfeC103_NfeC104_NfeC106_NfeC110_NfeC112_NfeC115_NfeC116_NfeC119_NfeC127_NfeC130_NfeC140_NfeC141_NfeC160 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 1 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
'[NfeC100]' AS tA, A.*,
CASE WHEN A.IND_EMIT = 0 THEN A.CnpjDest || '_' || D.UF || '_' || D.NOME ELSE A.CnpjEmit || '_' || C.UF || '_' || C.NOME END AS Part,
'[NfeC100Detalhe]' AS tB, B.*, '[NfeC101-Emit]' AS tC, C.*,
'[NfeC102-Dest]' AS tD, D.*, '[NfeC103-ConfOperacaoDestinatario]' AS tE, E.*, '[NfeC104-MotCancelam]' AS tP, P.*, '[NfeC106-CteRelacionado]' AS tF, F.*,
'[NfeC110-Obs]' AS tG, G.*, '[NfeC112-NFeRelacionada]' AS tH, H.*, '[NfeC115-DadosRetirada]' AS tI, I.*,
'[NfeC116-Entrega]' AS tJ, J.*, '[NfeC119-FormasPagto]' AS tK, K.*, '[NfeC127]' AS tL, L.*,
'[NfeC130-DemaisTribs]' AS tM, M.*, '[NfeC140-Fat]' AS tN, N.*, '[NfeC141-Duplics]' AS [tO], O.*, '[NfeC160-DadosTransporte]' AS [tQ], Q.*
   FROM dfe_fiscal_NfeC100 AS A
   LEFT OUTER JOIN dfe_fiscal_NfeC100Detalhe AS B ON B.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC101 AS C ON C.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC102 AS D ON D.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC103 AS E ON E.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC104 AS P ON P.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC106 AS F ON F.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC110 AS G ON G.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC112 AS H ON H.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC115 AS I ON I.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC116 AS J ON J.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC119 AS K ON K.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC127 AS L ON L.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC130 AS M ON M.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC140 AS N ON N.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC141 AS O ON O.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC160 AS Q ON Q.idNfeC100 = A.idNfeC100
```

```sql
DROP VIEW IF EXISTS osf.Evt189_NFeReferenciada
```

```sql
CREATE VIEW IF NOT EXISTS osf.Evt189_NFeReferenciada AS
SELECT '[Evt100]' AS tA, A.*, '[Evt189-EvtNotaFiscalReferenciada]' AS tB, B.*
   FROM dfe_fiscal_Evt100 AS A
   LEFT OUTER JOIN dfe_fiscal_Evt189 AS B ON B.idEvt100 = A.idEvt100
   WHERE B.idEvt100 IS NOT NULL
```

```sql
DROP VIEW IF EXISTS osf.Evt190_ZFM
```

```sql
CREATE VIEW IF NOT EXISTS osf.Evt190_ZFM AS
SELECT '[Evt100]' AS tA, A.*, '[Evt190-ZFM]' AS tC, C.*
   FROM dfe_fiscal_Evt100 AS A
   LEFT OUTER JOIN dfe_fiscal_Evt190 AS C ON C.idEvt100 = A.idEvt100
   WHERE C.idEvt100 IS NOT NULL
```

```sql
DROP VIEW IF EXISTS osf.Evt191_192_EFD_Part
```

```sql
CREATE VIEW IF NOT EXISTS osf.Evt191_192_EFD_Part AS
SELECT '[Evt100]' AS tA, A.*, '[Evt191-EfdPart]' AS tD, D.*, '[Evt192-EfdPart]' AS tE, E.*
   FROM dfe_fiscal_Evt100 AS A
   LEFT OUTER JOIN dfe_fiscal_Evt191 AS D ON D.idEvt100 = A.idEvt100
   LEFT OUTER JOIN dfe_fiscal_Evt192 AS E ON E.idEvt191 = D.idEvt191
   WHERE (D.idEvt100 IS NOT NULL OR E.idEvt191 IS NOT NULL)
```

```sql
DROP VIEW IF EXISTS osf.Evt100_e_subeventos
```

```sql
CREATE VIEW IF NOT EXISTS osf.Evt100_e_subeventos AS
SELECT '[Evt100]' AS tA, A.*, '[Evt101-Evt_Aut]' AS tB, B.*, '[Evt102AverbExp]' AS tC, C.*,
'[Evt103DadosExp]' AS tD, D.*, '[Evt104]' AS tE, E.*, '[Evt105-Canc_NFe]' AS tF, F.*,
'[Evt106-CartCorrecao]' AS tR, R.*, '[Evt107-Entrega]' AS tG, G.*, '[Evt111-Ciencia_ConfOperacao]' AS tH, H.*, '[Evt113-RegPassagemNfe]' AS tI, I.*,
'[Evt114-MDFe_Cte_Canc]' AS tJ, J.*, '[Evt115-CancMDFe]' AS tK, K.*, '[Evt119-Canc_Cte]' AS tL, L.*, '[Evt120-EntrSuframa]' AS tZF2, ZF2.*,
'[Evt121-NFe_Cte_MDFe]' AS tM, M.*, '[Evt122-NFe_Cte_MDFe]' AS tN, N.*, '[Evt123-NFe_Cte_MDFe]' AS [tO], O.*,
'[Evt127-RegPassagemFronteira]' AS tP, P.*, '[Evt131-VistSuframa]' AS tZF1, ZF1.*, '[Evt132-CteAutor]' AS tQ, Q.*
   FROM dfe_fiscal_Evt100 AS A
   LEFT OUTER JOIN dfe_fiscal_Evt101 AS B ON B.idEvt100 = A.idEvt100
   LEFT OUTER JOIN dfe_fiscal_Evt102 AS C ON C.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt103 AS D ON D.idEvt102 = C.idEvt102
   LEFT OUTER JOIN dfe_fiscal_Evt104 AS E ON E.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt105 AS F ON F.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt106 AS R ON R.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt107 AS G ON G.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt111 AS H ON H.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt113 AS I ON I.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt114 AS J ON J.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt115 AS K ON K.idEvt114 = J.idEvt114
   LEFT OUTER JOIN dfe_fiscal_Evt119 AS L ON L.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt120 AS ZF2 ON ZF2.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt121 AS M ON M.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt122 AS N ON N.idEvt121 = M.idEvt121
   LEFT OUTER JOIN dfe_fiscal_Evt123 AS O ON O.idEvt121 = M.idEvt121
   LEFT OUTER JOIN dfe_fiscal_Evt127 AS P ON P.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt131 AS ZF1 ON ZF1.idEvt101 = B.idEvt101
   LEFT OUTER JOIN dfe_fiscal_Evt132 AS Q ON Q.idEvt101 = B.idEvt101
```

```sql
DROP VIEW IF EXISTS osf.NFes_Itens_C100_C170_C176_C182_C183
```

```sql
CREATE VIEW IF NOT EXISTS osf.NFes_Itens_C100_C170_C176_C182_C183 AS
SELECT
  CASE WHEN A.IND_EMIT = 0 THEN
      CASE WHEN A.IND_OPER = 0 THEN 'EP' ELSE 'S' END
  ELSE
      CASE WHEN A.IND_OPER = 1 THEN 'ET' ELSE 'D' END
   END AS tp_oper,
  CASE WHEN A.COD_SIT = 2 THEN 'cancelado' ELSE
    CASE WHEN A.COD_SIT = 3 THEN 'cancelado' ELSE
      CASE WHEN A.COD_SIT = 4 THEN 'denegado' ELSE
        CASE WHEN A.COD_SIT = 5 THEN 'inutilizado' ELSE 'válido' END
      END
    END
  END AS tp_codSit,
'[NfeC100]' AS tA, A.*,
CASE WHEN A.IND_EMIT = 0 THEN A.CnpjDest || '_' || D102.UF || '_' || D102.NOME ELSE A.CnpjEmit || '_' || C101.UF || '_' || C101.NOME END AS Part,
'[NfeC170]' AS tB, B.*, '[NfeC170InfProd]' AS tC, C.*,
'[NfeC170IpiNaoTrib]' AS tD, D.*, '[NfeC170IpiTrib]' AS tE, E.*, '[NfeC170Resumo]' AS tF, F.*,
'[NfeC170Tributos]' AS tG, G.*, '[NfeC176]' AS tH, H.*, '[NfeC182]' AS tI, I.*,
'[NfeC183]' AS tJ, J.*
   FROM dfe_fiscal_NfeC100 AS A
   LEFT OUTER JOIN dfe_fiscal_NfeC101 AS C101 ON C101.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC102 AS D102 ON D102.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC170 AS B ON B.idNfeC100 = A.idNfeC100
   LEFT OUTER JOIN dfe_fiscal_NfeC170InfProd AS C ON C.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC170IpiNaoTrib AS D ON D.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC170IpiTrib AS E ON E.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC170Resumo AS F ON F.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC170Tributos AS G ON G.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC176 AS H ON H.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC182 AS I ON I.idNFeC170 = B.idNFeC170
   LEFT OUTER JOIN dfe_fiscal_NfeC183 AS J ON J.idNFeC182 = I.idNFeC182
```

```sql
DROP VIEW IF EXISTS osf.CTes_PodeDuplicar_NFeC200_e_demais
```

```sql
CREATE VIEW IF NOT EXISTS osf.CTes_PodeDuplicar_NFeC200_e_demais AS
SELECT
'[NfeC200]' AS tA, A.*, '[NfeC200Detalhe]' AS tB, B.*, '[NfeC201-Tomador]' AS tC, C.*,
'[NfeC202-Emitente]' AS tD, D.*, '[NfeC203-Remetente]' AS tE, E.*, '[NfeC205]' AS tF, F.*,
'[NfeC206]' AS tG, G.*, '[NfeC207]' AS tH, H.*, '[NfeC209]' AS tI, I.*,
'[NfeC211]' AS tK, K.*, '[NfeC211infAd]' AS tL, L.*,
'[NfeC211Resumo]' AS tM, M.*, '[NfeC212]' AS tN, N.*, '[NfeC215]' AS [tO], O.*,				
'[NfeC217]' AS tP, P.*, '[NfeC219]' AS tR, R.*,
'[NfeC225]' AS tS, S.*, '[NfeC227]' AS tT, T.*
   FROM dfe_fiscal_NfeC200 AS A							
   LEFT OUTER JOIN dfe_fiscal_NfeC200Detalhe AS B ON B.idNfeC200 = A.idNfeC200 							
   LEFT OUTER JOIN dfe_fiscal_NfeC201 AS C ON C.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC202 AS D ON D.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC203 AS E ON E.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC205 AS F ON F.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC206 AS G ON G.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC207 AS H ON H.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC209 AS I ON I.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC211 AS K ON K.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC211infAd AS L ON L.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC211Resumo AS M ON M.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC212 AS N ON N.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC215 AS O ON O.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC217 AS P ON P.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC219 AS R ON R.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC225 AS S ON S.idNfeC200 = A.idNfeC200
   LEFT OUTER JOIN dfe_fiscal_NfeC227 AS T ON T.idNfeC200 = A.idNfeC200
```
