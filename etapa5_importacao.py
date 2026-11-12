import time
import logging
import pyautogui as pg
import pygetwindow as gw

from etapa4_conexao import (
    TITULO_SISTEMA,
    obter_janela,
    verificar_foco,
)


def garantir_spiderware_aberto(acao=""):
    janelas = [
        j for j in gw.getWindowsWithTitle(TITULO_SISTEMA)
        if j.visible and not j.isMinimized
    ]
    if not janelas:
        raise RuntimeError(f"O Spiderware foi fechado ou não está visível ({acao}).")


def realizar_importacao_final(timeout=60):
    # 1. Garante foco na janela modal 'Importação Internet'
    janela_modal = obter_janela(timeout=timeout)
    time.sleep(1)

    # 2. Marca "Requerimento de Secundário" com Espaço (já vem pré-selecionado)
    verificar_foco(janela_modal, acao="Marcando 'Requerimento de Secundário'")
    logging.info("Marcando 'Requerimento de Secundário' com tecla Espaço...")
    pg.press("space")
    time.sleep(1.5)

    # 3. Aciona o botão Importar (Alt + I)
    verificar_foco(janela_modal, acao="Acionando botão 'Importar'")
    logging.info("Acionando o botão 'Importar'...")
    pg.hotkey("alt", "i")

    # 4. Aguarda abrir a janelinha de "Parâmetro" e ajusta o mês
    time.sleep(2)
    garantir_spiderware_aberto("Ajuste do mês em Parâmetro")
    logging.info("Ajustando o mês para o anterior (seta direita + seta baixo)...")
    pg.press("right")
    time.sleep(0.3)
    pg.press("down")
    time.sleep(0.5)

    # 5. Aciona o botão "Confirmar" (Alt + O)
    garantir_spiderware_aberto("Confirmação da importação")
    logging.info("Confirmando a importação (Alt + O)...")
    pg.hotkey("alt", "o")

    # 6. Aguarda a mensagem final e dá Enter no último "OK"
    time.sleep(3)
    garantir_spiderware_aberto("Confirmação do OK final")
    logging.info("Confirmando o 'OK' final...")
    pg.press("enter")

    logging.info("Importação concluída e confirmada com sucesso.")
    return True