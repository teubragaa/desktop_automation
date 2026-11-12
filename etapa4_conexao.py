import time
import logging
import pyautogui as pg
from automacao_base import SpiderwareUI

PERC_X_CONEXAO = 0.422
PERC_Y_CONEXAO = 0.233
PERC_Y_SERVIDOR_2 = 0.340


def realizar_conexao(timeout=60):
    """Desmarca o parâmetro de secundário e estabelece conexão com o Servidor 2."""
    # 1. Localiza a janela modal 'Importação Internet' (largura entre 400 e 800)
    janela_modal = SpiderwareUI.obter_janela(timeout=timeout, larg_min=400, larg_max=800)
    time.sleep(1.5)

    # 2. Garante que 'Requerimento de Secundário' esteja desmarcado antes da conexão
    if SpiderwareUI.checkbox_focado_marcado(janela_modal):
        SpiderwareUI.verificar_foco(janela_modal, "Desmarcando 'Requerimento de Secundário'")
        logging.info("Desmarcando 'Requerimento de Secundário' (Espaço)...")
        pg.press("space")
        time.sleep(1.5)
    else:
        logging.info("'Requerimento de Secundário' já está desmarcado.")

    # 3. Abre menu 'Conexão' e seleciona 'Servidor 2'
    SpiderwareUI.clicar_proporcional(janela_modal, PERC_X_CONEXAO, PERC_Y_CONEXAO, "Abrindo menu 'Conexão ▾'...")
    SpiderwareUI.clicar_proporcional(janela_modal, PERC_X_CONEXAO, PERC_Y_SERVIDOR_2, "Selecionando 'Servidor 2'...", espera_pos=1.5)

    # 4. Aguarda o aviso de conexão e confirma com Enter
    SpiderwareUI.aguardar_popup(janela_modal, "Confirmação de conexão", timeout=30)
    logging.info("Confirmando conexão com Servidor 2 (Enter)...")
    pg.press("enter")
    time.sleep(2)
    return True