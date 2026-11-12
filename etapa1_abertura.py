import os
import subprocess
import time
import logging
import pyautogui as pg
import pygetwindow as gw
from config import CAMINHO_ATALHO

TITULO_SEGURANCA = "Abrir Arquivo - Aviso de Segurança"


def iniciar_chamador(timeout=60, intervalo=3):
    logging.info("Validando e disparando abertura do atalho...")
    
    if not os.path.exists(CAMINHO_ATALHO):
        raise FileNotFoundError(f"Atalho não encontrado no caminho: {CAMINHO_ATALHO}")

    comando = f'start "" "{CAMINHO_ATALHO}"'
    subprocess.Popen(comando, shell=True)
    
    # Tempo inicial para o Windows processar o comando e montar a janela na tela
    time.sleep(3)
    
    inicio = time.monotonic()
    
    while (time.monotonic() - inicio) < timeout:
        janelas = gw.getWindowsWithTitle(TITULO_SEGURANCA)
        
        if janelas:
            logging.info("Janela de segurança do Windows detectada.")
            janela = janelas[0]
            
            try:
                if gw.getActiveWindow() != janela:
                    janela.activate()
            except Exception as e:
                logging.warning(f"Aviso ao focar janela de segurança: {e}")
            
            # Tempo maior para garantir que a janela estabilizou o foco visualmente
            time.sleep(3)
            
            if gw.getActiveWindow() == janela:
                logging.info("Confirmando abertura com Alt + E...")
                pg.hotkey("alt", "e")
                
                # Popup fechar e o executável começar a carregar na rede
                time.sleep(5)
                
                if not gw.getWindowsWithTitle(TITULO_SEGURANCA):
                    logging.info("Comando de abertura confirmado e aviso fechado com sucesso.")
                    return True
                
                logging.warning("A janela de segurança permaneceu aberta. Tentando novamente...")
            else:
                logging.warning("Janela de segurança não está ativa no momento. Retentando foco...")
            
        time.sleep(intervalo)
        
    logging.error("A janela de segurança não apareceu ou não pôde ser confirmada dentro do tempo limite.")
    raise TimeoutError("Tempo limite esgotado ao aguardar confirmação de segurança.")