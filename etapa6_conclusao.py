import time
import ctypes
import logging
import subprocess
import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException
from automacao_base import SpiderwareUI

TITULO_CONCLUSAO = "Information"


def encerrar_spiderware():
    """Fecha a janela modal e a janela principal do Spiderware via interface."""
    logging.info("Encerrando o aplicativo Spiderware...")

    # 1. Fecha a janela modal 'Importação Internet' com o botão Cancelar (Alt + C)
    modais = [
        j for j in gw.getWindowsWithTitle(SpiderwareUI.TITULO)
        if j.title.strip() == SpiderwareUI.TITULO and j.visible and 400 < j.width < 800
    ]
    if modais:
        try:
            modais[0].activate()
            time.sleep(0.5)
        except PyGetWindowException:
            pass
        logging.info("Fechando janela 'Importação Internet' (Alt + C)...")
        pg.hotkey("alt", "c")
        time.sleep(2)

    # 2. Fecha a janela principal do Spiderware (Alt + F4)
    principais = [
        j for j in gw.getWindowsWithTitle(SpiderwareUI.TITULO)
        if j.title.strip() == SpiderwareUI.TITULO and j.visible and j.width >= 800
    ]
    if principais:
        janela_principal = principais[0]
        try:
            janela_principal.activate()
            time.sleep(0.5)
        except PyGetWindowException:
            pass
        logging.info("Fechando janela principal do Spiderware (Alt + F4)...")
        pg.hotkey("alt", "f4")
        time.sleep(2)

    logging.info("Spiderware encerrado com sucesso.")
    return True

def aguardar_conclusao_importacao(timeout_minutos=10, intervalo=3):
    """Aguarda a janela 'Information' (limite de 10 min), confirma o OK e encerra o Spiderware."""
    timeout_segundos = timeout_minutos * 60
    logging.info(
        f"Importação em andamento... Aguardando janela '{TITULO_CONCLUSAO}' "
        f"(limite máximo: {timeout_minutos} min)."
    )

    inicio = time.monotonic()

    while (time.monotonic() - inicio) < timeout_segundos:
        SpiderwareUI.garantir_aberto("Aguardando conclusão da importação")

        janelas_info = [
            j for j in gw.getWindowsWithTitle(TITULO_CONCLUSAO)
            if j.title.strip() == TITULO_CONCLUSAO and j.visible and not j.isMinimized
        ]

        if janelas_info:
            janela_ok = janelas_info[0]
            tempo_decorrido = int(time.monotonic() - inicio)
            minutos, segundos = divmod(tempo_decorrido, 60)

            logging.info(
                f"Janela '{TITULO_CONCLUSAO}' detectada após {minutos}m {segundos}s!"
            )

            try:
                if gw.getActiveWindow() != janela_ok:
                    janela_ok.activate()
                time.sleep(1)
            except PyGetWindowException:
                pass

            logging.info("Confirmando 'Importação efetuada com êxito !' (Enter)...")
            pg.press("enter")
            time.sleep(2)

            # Fecha o aplicativo Spiderware
            encerrar_spiderware()
            return True

        time.sleep(intervalo)

    raise TimeoutError(
        f"Tempo limite de {timeout_minutos} minutos esgotado sem aparecer a janela '{TITULO_CONCLUSAO}'."
    )