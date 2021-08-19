from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyautogui
import functions as fn
import globalVar as gb

conn = fn.connectDB()
cur = conn.cursor()
cur.execute(gb.sqlSelect)

while True:
    row = cur.fetchone()
    if row is None:
        break
    else:
        NFV = row[1]
        chaveV = row[2]
        nomeFile = row[0]+"_"+row[1]+"_RPS_"+row[3]

        profile = fn.profile()

        # Abrir navegador e preenchimento de dados

        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get(gb.link)
        sleep(2)
        cnpj = driver.find_element_by_id("cnpj")
        nNF = driver.find_element_by_id("numero")
        chave = driver.find_element_by_id("chave")
        sleep(2)
        cnpj.send_keys(gb.nCnpj)
        nNF.send_keys(NFV)
        chave.send_keys(chaveV)
        sleep(1)
        chave.send_keys(Keys.ENTER)
        sleep(2)
        dwn = driver.find_element_by_id("download")
        dwn.send_keys(Keys.ENTER)
        sleep(3)
        pyautogui.press('enter')
        sleep(1)
        pyautogui.hotkey('alt', 'F4')
        sleep(1)

        fn.processFile(nomeFile)

        fn.setDownload(row[0], row[1])

        #fn.uploadDB(nomeFile)

cur.close()
conn.close()