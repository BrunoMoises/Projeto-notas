import cx_Oracle
from selenium import webdriver
import os
import ftplib
import globalVar as gb
import pathlib

# Conectar com banco
def connectDB():
    dsn_tns = cx_Oracle.makedsn(gb.DBhost, gb.DBport, service_name=gb.DBserviceName)
    conn = cx_Oracle.connect(user=gb.DBuser, password=gb.DBpassword, dsn=dsn_tns)
    return conn

# Grava data de download na tabela
def setDownload(filial, doc):
    conn = connectDB()
    sqlU = ("UPDATE SF2010_RET T "
            "    SET T.DT_DOWNLOAD = SYSDATE "
            "  WHERE T.F2_FILIAL = '"+filial+"'"
            "   AND T.F2_DOC = '"+doc+"'"
            "   AND T.F2_SERIE = 'RPS' ")
    cur = conn.cursor()
    cur.execute(sqlU)
    conn.commit()
    cur.close()
    conn.close()

# Setar perfil do navegador para download em pasta especifica
def profile():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting",False)
    profile.set_preference("browser.download.dir", gb.downloadFolder)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    return profile

# Pesquisar arquivos e renomear
def processFile(nomeFile):
    for diretorio, subpastas, arquivos in os.walk(gb.downloadFolder):
            for arquivo in arquivos:
                old_file = os.path.join(gb.downloadFolder, arquivo)
                new_file = os.path.join(gb.nfseFolder, "%s.pdf" % nomeFile)
                if os.path.exists(new_file):
                    os.remove(old_file)
                else:
                    os.rename(old_file, new_file)

# Upload de arquivos para o banco
def uploadDB(nomeFile,descricao,order,sistema,filtro,codigo,doc_num,nf_num,serie,filial,emissao):
        if serie == 'RPS':
            caminho = pathlib.Path(gb.nfseFolder)
        else:
            caminho = pathlib.Path(gb.nfeFolder)

        arquivos = caminho.glob(nomeFile+'*')
        tipo = 1
        conn = connectDB()
        cur = conn.cursor()
        entrou = 0
        for arquivo in arquivos:
            entrou = 1
            nome = os.path.basename(arquivo)
            n_par_codigo = cur.var(cx_Oracle.NUMBER)
            sqlquery = ("INSERT INTO SIAOS.PROP_ARQUIVO"
                        "(PAR_NOME,PAR_DESCRICAO,ORDER_NO,PAR_TIPO,PAR_ARQUIVO,PAR_SISTEMA,PAR_FILTRO,ACE_CODIGO) "
                        "VALUES (:1,:2,:3,:4,:5,:6,:7,:8)"
                        "RETURNING PAR_CODIGO INTO :9")
            sqlargs = (nome,descricao,order,tipo,arquivo.open('rb').read(),sistema,filtro,codigo,n_par_codigo)
            cur.execute(sqlquery, sqlargs)
            n_par_codigo = int(n_par_codigo.getvalue()[0])
            conn.commit()
            moveFile(doc_num,nf_num,serie,filial,emissao,n_par_codigo,nome)
        if entrou == 0:
            sqlquery = ("UPDATE INTEGRACAO.SF2010_RET SET DT_DOWNLOAD = '' WHERE DOCNUM = '"+doc_num+"'")
            cur.execute(sqlquery)
            conn.commit()
        cur.close()
        conn.close()
        return

# Mover arquivo para pasta correta
def moveFile(doc_num,nf_num,serie,filial,emissao,n_par_codigo,nome):
    print('entrou '+str(n_par_codigo))
    conn = connectDB()
    cur = conn.cursor()
    sqlproc = ("BEGIN SIAOS.PCK_NOTA_FISCAL.SP_NF_ARQUIVO(:1,:2,:3,:4,:5,:6);END;")
    sqlprocarg = (doc_num,nf_num,serie,filial,emissao,n_par_codigo)
    cur.execute(sqlproc, sqlprocarg)
    conn.commit()
    cur.close()
    conn.close()

# Obter tamanho do arquivo
def getSize(file):
    file.seek(0,2)
    size = file.tell()
    return size

#Subir para servidor por FTP
def uploadForFTP(nomeFile):
        ftp_server = ftplib.FTP(gb.HOSTNAME, gb.USERNAME, gb.PASSWORD) 
        ftp_server.encoding = "utf-8"
        filename = gb.nfseFolder+nomeFile
        ftp_server.cwd("dqanet/nfes")

        with open(filename, "rb") as file: 
            ftp_server.storbinary(f"STOR {filename}", file)
            ftp_server.quit()

# Deletar arquivos da pasta local
def deleteFile(nomeFile):
        arquivo = str("%s.pdf" % nomeFile)
        diretorio = os.listdir(gb.nfseFolder)
        if arquivo in diretorio:
            os.remove('{}/{}'.format(gb.nfseFolder, arquivo))