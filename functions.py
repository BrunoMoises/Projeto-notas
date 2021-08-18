import cx_Oracle
from selenium import webdriver
import os
import ftplib
import globalVar as gb

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
    profile.set_preference(
        "browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", gb.downloadFolder)
    return profile

# Pesquisar arquivos e renomear
def processFile(nomeFile):
    for diretorio, subpastas, arquivos in os.walk(gb.downloadFolder):
            for arquivo in arquivos:
                old_file = os.path.join(gb.downloadFolder, arquivo)
                new_file = os.path.join(gb.nfseFolder, "%s.pdf" % nomeFile)
                os.rename(old_file, new_file)

# Upload de arquivos para o banco
def uploadDB(nomeFile):
        caminho = gb.nfseFolder+nomeFile
        arquivo = open(caminho, "rb").read()
        nome = os.path.basename(caminho)
        tamanho = getSize(arquivo)

        conn = connectDB()
        cur = conn.cursor()
        sqlquery = ("insert into file"
                    " () "
                    " values ()")
        sqlargs = ()
        cur.execute(sqlquery, sqlargs)
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
        HOSTNAME = ""
        USERNAME = ""
        PASSWORD = ""
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD) 
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