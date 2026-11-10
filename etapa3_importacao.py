import time
import logging

import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException


def verificar_foco(janela):
    if gw.getActiveWindow() != janela:
        raise RuntimeError("A janela do Spiderware perdeu o foco durante a importação.")


def obter_janela():
    """Localiza e ativa a janela do Spiderware."""
    while True:
        janelas = [
            j for j in gw.getWindowsWithTitle("Spiderware")
            if j.visible and not j.isMinimized
        ]
        if janelas:
            janela = janelas[0]
            try:
                if gw.getActiveWindow() != janela:
                    janela.activate()
            except PyGetWindowException:
                time.sleep(1)
                continue
            if gw.getActiveWindow() == janela:
                return janela
        time.sleep(1)


def clicar_proporcional(janela, perc_x, perc_y, mensagem):
    verificar_foco(janela)
    alvo_x = janela.left + int(janela.width * perc_x)
    alvo_y = janela.top + int(janela.height * perc_y)

    logging.info(f"{mensagem}")
    pg.moveTo(alvo_x, alvo_y, duration=0.3)
    pg.click()
    time.sleep(1.5)


def realizar_importacao():
    # 1. Janela principal
    janela_principal = obter_janela()
    time.sleep(2)

    # 2. Clica no ícone principal de Importação
    clicar_proporcional(
        janela=janela_principal,
        perc_x=0.507,
        perc_y=0.796,
        mensagem="Clicando no ícone 'Importação'...",
    )

    # 3. Clica na opção Importação do submenu
    clicar_proporcional(
        janela=janela_principal,
        perc_x=0.513,
        perc_y=0.890,
        mensagem="Selecionando opção 'Importação' no submenu...",
    )

    # Aguarda a tela modal abrir
    time.sleep(2.5)

    # 4. Pega a tela modal 'Importação Internet'
    janela_modal = obter_janela()

    # 5. Clica no botão Conexão
    clicar_proporcional(
        janela=janela_modal,
        perc_x=0.422,
        perc_y=0.233,
        mensagem="Abrindo menu 'Conexão ▾'...",
    )

    # 6. Clica na opção Servidor 2
    clicar_proporcional(
        janela=janela_modal,
        perc_x=0.422,
        perc_y=0.340,
        mensagem="Selecionando 'Servidor 2'...",
    )

    logging.info("Comando de carga no Servidor 2 disparado com sucesso.")
    return True