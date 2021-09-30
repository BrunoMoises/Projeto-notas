# DB parameters

DBhost = 'srv_oracle'
DBport = '1521'
DBserviceName = 'smar'
DBuser = 'integracao'
DBpassword = 'integra'

# General parameters

nCnpj = "29.321.094/0001-82"
downloadFolder = r"F:\Area\Operacoes\Faturamento\NFSE_DOWNLOAD"
nfseFolder = r"F:\Area\Operacoes\Faturamento\NFSE"
link = 'http://nfe.sertaozinho.sp.gov.br:9083/tbw/loginWeb.jsp?execobj=NFENotaFiscalBuscarDireto'

sqlSelect = """SELECT X.*
  FROM (SELECT F.F2_FILIAL,
               F.F2_DOC,
               TRIM(F.F2_CODNFE) F2_CODNFE,
               TRIM(F.F2_EMISSAO) DT_EMISSAO
          FROM SF2010_RET FRET
         INNER JOIN PROTPROD.SF2010 F ON F.F2_FILIAL = FRET.F2_FILIAL
                                     AND F.F2_DOC = FRET.F2_DOC
                                     AND F.F2_SERIE = FRET.F2_SERIE
         WHERE (FRET.DT_ALTERACAO IS NOT NULL
           AND FRET.US_INCLUSAO = 'PROTHEUS'
           AND FRET.DT_INCLUSAO >= TO_DATE('01-01-2021', 'dd-mm-yyyy')
           AND FRET.F2_SERIE = 'RPS'
           AND FRET.DT_DOWNLOAD IS NULL)
           AND F.D_E_L_E_T_ = ' '
         ORDER BY
               FRET.DT_INCLUSAO DESC) X
 WHERE ROWNUM < 5"""

HOSTNAME = ""
USERNAME = ""
PASSWORD = ""