import time
import logging
import pyautogui as pg

def realizar_finalizacao():
    logging.info("Confirmando a conexão com êxito...")
    
    # Aguarda 1 segundo por segurança e dá o Enter no botão OK
    time.sleep(1)
    pg.press("enter")
    
    logging.info("Janela confirmada.")