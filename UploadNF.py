from time import sleep
import functions as fn

conn = fn.connectDB()
cur = conn.cursor()
cur.execute('SELECT * FROM TABELA')

while True:
    row = cur.fetchone()
    if row is None:
        break
    else:
        doc_num = row[0]
        nf_num = row[1]
        serie = row[2]
        filial = row[3]
        emissao = row[4]
        order_no = row[6]
        nomeFile = row[7]
        descricao = row[8]
        par_sistema = row[9]
        par_filtro = row[10]
        ace_codigo = row[11]
        fn.uploadDB(nomeFile,descricao,order_no,par_sistema,par_filtro,ace_codigo,doc_num,nf_num,serie,filial,emissao)

cur.close()
conn.close()
