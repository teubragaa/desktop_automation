import subprocess
import pyautogui as pg
import pygetwindow as gw
import time
import logging
from config import CAMINHO_ATALHO

def iniciar_chamador():
    logging.info("Abrindo o atalho...")
    
    comando = f'start "" "{CAMINHO_ATALHO}"'
    subprocess.Popen(comando, shell=True)
    
    time.sleep(5)
    tempo_esperado = 0
    
    while tempo_esperado < 30:
        janelas = gw.getWindowsWithTitle("Abrir Arquivo - Aviso de Segurança")
        
        if janelas:
            logging.info("Janela de segurança encontrada.")
            janela = janelas[0]
            
            try:
                janela.activate()
            except:
                pass 
            
            time.sleep(2)
            
            logging.info("Confirmando abertura... Pressionando Alt + E.")
            pg.hotkey('alt', 'e')
            
            time.sleep(3)
            logging.info("Processo concluído. Aplicativo aberto.")
            return True 
            
        time.sleep(2)
        tempo_esperado += 2
        
    logging.error("A janela de segurança não apareceu no tempo limite.")
    raise Exception("Timeout na abertura do aplicativo.")