import time
import logging
from automacao_base import SpiderwareUI

PERC_X_MENU_IMP = 0.507
PERC_Y_MENU_IMP = 0.796
PERC_X_SUBMENU_IMP = 0.513
PERC_Y_SUBMENU_IMP = 0.890


def realizar_importacao(timeout=60):
    """Navega pela tela principal e abre o módulo 'Importação Internet'."""
    time.sleep(3)

    # 1. Localiza a janela principal (largura > 800)
    janela_principal = SpiderwareUI.obter_janela(timeout=timeout, larg_min=800)
    time.sleep(2)

    # 2. Aciona o ícone principal 'Importação'
    SpiderwareUI.clicar_proporcional(
        janela=janela_principal,
        perc_x=PERC_X_MENU_IMP,
        perc_y=PERC_Y_MENU_IMP,
        mensagem="Clicando no ícone principal 'Importação'...",
        espera_pos=3,
    )

    # 3. Aciona a opção 'Importação' no submenu suspenso
    SpiderwareUI.clicar_proporcional(
        janela=janela_principal,
        perc_x=PERC_X_SUBMENU_IMP,
        perc_y=PERC_Y_SUBMENU_IMP,
        mensagem="Selecionando opção 'Importação' no submenu...",
        espera_pos=5,
    )

    logging.info("Tela de 'Importação Internet' aberta com sucesso.")
    return True