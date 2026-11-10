import time
import logging

import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException


def verificar_foco(janela):
    if gw.getActiveWindow() != janela:
        raise RuntimeError("A janela do Spiderware perdeu o foco durante o login.")


def realizar_login(usuario, senha):
    logging.info(" Aguardando a janela de login do Spiderware...")

    while True:
        janelas = [
            janela
            for janela in gw.getWindowsWithTitle("Spiderware")
            if janela.title.strip() == "Spiderware"
            and janela.visible
            and not janela.isMinimized
        ]

        if len(janelas) == 1:
            janela_app = janelas[0]

            try:
                if gw.getActiveWindow() != janela_app:
                    janela_app.activate()
            except PyGetWindowException:
                time.sleep(1)
                continue

            if gw.getActiveWindow() == janela_app:
                logging.info("Janela de login localizada e focada.")
                break

        time.sleep(1)

    time.sleep(5)

    # Preenchimento do usuário
    verificar_foco(janela_app)
    logging.info("Preenchendo credenciais...")
    pg.write(usuario, interval=0.25)
    time.sleep(2)

    # Campo de senha
    verificar_foco(janela_app)
    pg.press("tab")
    time.sleep(2)

    verificar_foco(janela_app)
    pg.write(senha, interval=0.25)
    time.sleep(2)

    # Envio do login
    verificar_foco(janela_app)
    logging.info("Confirmando login com Alt + E...")
    pg.hotkey("alt", "e")

    logging.info("Solicitação de login enviada com sucesso.")
    return True