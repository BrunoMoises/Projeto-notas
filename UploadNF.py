from time import sleep
import functions as fn

conn = fn.connectDB()
cur = conn.cursor()
cur.execute('SELECT * FROM SIAOS.VW_NF_UP_ARQUIVO T')

while True:
    row = cur.fetchone()
    if row is None:
        break
    else:
        nomeFile = row[7]
        descricao = row[8]
        order_no = row[6]
        par_sistema = row[9]
        par_filtro = row[10]
        ace_codigo = row[11]
        fn.uploadDB(nomeFile,descricao,order_no,par_sistema,par_filtro,ace_codigo)
        break

cur.close()
conn.close()