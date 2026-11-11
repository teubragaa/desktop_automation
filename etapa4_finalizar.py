import time
import logging
import pyautogui as pg

def realizar_finalizacao():
    logging.info("Confirmando a conexão com êxito...")
    
    # 1. Confirma o pop-up inicial (OK)
    time.sleep(1)
    pg.press("enter")
    logging.info("Janela confirmada.")

    # 2. Aciona o botão Importar (Alt + I)
    time.sleep(1.5)
    logging.info("Acionando o botão 'Importar'...")
    pg.hotkey("alt", "i")
    
    # 3. Aguarda abrir a janelinha de "Parâmetro" e ajusta o mês
    time.sleep(1.5)
    logging.info("Ajustando o mês para o anterior (seta direita + seta baixo)...")
    pg.press("right")
    time.sleep(0.3)
    pg.press("down")
    time.sleep(0.5)

    # 4. Aciona o botão "Confirmar" (Alt + O)
    logging.info("Confirmando a importação...")
    pg.hotkey("alt", "o")

    # 5. Aguarda a mensagem final e dá Enter no último "OK"
    time.sleep(3)
    logging.info("Confirmando o 'OK' final...")
    pg.press("enter")
    logging.info("Importação concluída e confirmada com sucesso.")