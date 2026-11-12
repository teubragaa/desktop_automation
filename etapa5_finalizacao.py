import time
import logging
import pyautogui as pg
from automacao_base import SpiderwareUI


def realizar_importacao_final(timeout=60):
    """Marca o requerimento de secundário, ajusta o período e dispara a importação."""
    # 1. Valida o foco na modal 'Importação Internet'
    janela_modal = SpiderwareUI.obter_janela(timeout=timeout, larg_min=400, larg_max=800)
    time.sleep(1)

    # 2. Marca 'Requerimento de Secundário' (caso não esteja marcado)
    if not SpiderwareUI.checkbox_focado_marcado(janela_modal):
        SpiderwareUI.verificar_foco(janela_modal, "Marcando 'Requerimento de Secundário'")
        logging.info("Marcando 'Requerimento de Secundário' (Espaço)...")
        pg.press("space")
        time.sleep(1.5)

    # 3. Aciona o comando 'Importar' (Alt + I)
    SpiderwareUI.verificar_foco(janela_modal, "Acionando botão 'Importar'")
    logging.info("Acionando botão 'Importar' (Alt + I)...")
    pg.hotkey("alt", "i")

    # 4. Aguarda o modal 'Parâmetro' e seleciona o mês anterior
    SpiderwareUI.aguardar_popup(janela_modal, "Parâmetro de data", timeout=15)
    logging.info("Ajustando mês para o anterior (seta direita + seta baixo)...")
    pg.press("right")
    time.sleep(0.3)
    pg.press("down")
    time.sleep(0.5)

    # 5. Confirma o disparo da importação (Alt + O)
    SpiderwareUI.garantir_aberto("Confirmação da importação")
    logging.info("Confirmando início da importação (Alt + O)...")
    pg.hotkey("alt", "o")
    time.sleep(2)

    logging.info("Importação disparada com sucesso.")
    return True