import subprocess
import time
import logging
import pyautogui as pg
import pygetwindow as gw
from config import CAMINHO_ATALHO

def iniciar_chamador(timeout=30):
    logging.info("Disparando abertura do atalho...")
    
    comando = f'start "" "{CAMINHO_ATALHO}"'
    subprocess.Popen(comando, shell=True)
    
    tempo_esperado = 0
    intervalo = 2
    
    while tempo_esperado < timeout:
        janelas = gw.getWindowsWithTitle("Abrir Arquivo - Aviso de Segurança")
        
        if janelas:
            logging.info("Janela de segurança do Windows detectada.")
            janela = janelas[0]
            
            try:
                janela.activate()
            except Exception as e:
                logging.warning(f"Aviso ao focar janela de segurança: {e}")
            
            time.sleep(1.5)
            
            logging.info("Confirmando abertura com Alt + E...")
            pg.hotkey("alt", "e")
            
            time.sleep(3)
            logging.info("Comando de abertura enviado com sucesso.")
            return True
            
        time.sleep(intervalo)
        tempo_esperado += intervalo
        
    logging.error("A janela de segurança não apareceu dentro do tempo limite.")
    raise TimeoutError("Tempo limite esgotado ao aguardar confirmação de segurança.")