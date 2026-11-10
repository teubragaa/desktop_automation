import logging
import time

import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException


def verificar_foco(janela):
    if gw.getActiveWindow() != janela:
        raise RuntimeError("A janela do Spiderware perdeu o foco durante o login.")


def realizar_login(usuario, senha):
    logging.info("Aguardando a janela do Spiderware...")

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
                break

        time.sleep(1)

    time.sleep(5)

    verificar_foco(janela_app)
    pg.write(usuario, interval=0.25)
    time.sleep(2)

    verificar_foco(janela_app)
    pg.press("tab")
    time.sleep(2)

    verificar_foco(janela_app)
    pg.write(senha, interval=0.25)
    time.sleep(2)

    verificar_foco(janela_app)
    pg.hotkey("alt", "e")

    logging.info("Solicitação de login enviada ao Spiderware.")
    return True