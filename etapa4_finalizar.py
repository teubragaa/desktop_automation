import time
import logging
import pyautogui as pg

def realizar_finalizacao():
    logging.info("Confirmando a conexão com êxito...")
    
    # Aguarda 1 segundo por segurança e dá o Enter no botão OK
    time.sleep(1)
    pg.press("enter")
    logging.info("Janela confirmada.")

    # Aguarda o pop-up fechar e o foco voltar para a tela
    time.sleep(1.5)

    # Aciona o botão Importar pelo atalho da letra 'i'
    logging.info("Acionando o botão 'Importar'...")
    pg.hotkey("alt", "i")
    logging.info("Botão 'Importar' acionado com sucesso.")