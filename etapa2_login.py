import time
import logging
import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException

TITULO_LOGIN = "Spiderware"


def verificar_foco(janela, etapa_acao=""):
    janela_ativa = gw.getActiveWindow()
    if janela_ativa != janela:
        titulo_intruso = janela_ativa.title if janela_ativa else "Nenhuma janela ativa"
        raise RuntimeError(
            f"A janela do Spiderware perdeu o foco durante o login ({etapa_acao}). "
            f"Janela em foco no momento: '{titulo_intruso}'"
        )


def realizar_login(usuario, senha, timeout=60, intervalo=3):
    if not usuario or not senha:
        raise ValueError("Usuário ou senha não foram informados nas configurações.")

    logging.info("Aguardando a janela de login do Spiderware...")

    inicio = time.monotonic()
    janela_app = None

    while (time.monotonic() - inicio) < timeout:
        janelas = [
            janela
            for janela in gw.getWindowsWithTitle(TITULO_LOGIN)
            if janela.title.strip() == TITULO_LOGIN
            and janela.visible
            and not janela.isMinimized
        ]

        if len(janelas) > 1:
            logging.warning(
                f"Foram detectadas {len(janelas)} janelas '{TITULO_LOGIN}' abertas simultaneamente. "
                "Selecionando a primeira instância disponível..."
            )

        if len(janelas) >= 1:
            candidata = janelas[0]

            try:
                if gw.getActiveWindow() != candidata:
                    candidata.activate()
            except PyGetWindowException as e:
                logging.warning(f"Aviso ao tentar focar janela de login: {e}")
                time.sleep(intervalo)
                continue

            # Pausa para o Windows estabilizar o foco na janela localizada
            time.sleep(2)

            if gw.getActiveWindow() == candidata:
                janela_app = candidata
                logging.info("Janela de login localizada e focada com sucesso.")
                break

        time.sleep(intervalo)

    if not janela_app:
        logging.error("A janela de login do Spiderware não apareceu dentro do tempo limite.")
        raise TimeoutError("Tempo limite esgotado ao aguardar a janela de login do Spiderware.")

    # Respiro amplo para garantir que o cursor já está posicionado no campo de usuário
    time.sleep(5)

    # 1. Preenchimento do usuário
    verificar_foco(janela_app, "Preenchimento do usuário")
    logging.info("Preenchendo usuário...")
    pg.write(str(usuario), interval=0.3)
    time.sleep(3)

    # 2. Navegação para o campo de senha
    verificar_foco(janela_app, "Navegação com Tab para senha")
    logging.info("Avançando para o campo de senha (Tab)...")
    pg.press("tab")
    time.sleep(3)

    # 3. Preenchimento da senha
    verificar_foco(janela_app, "Preenchimento da senha")
    logging.info("Preenchendo senha...")
    pg.write(str(senha), interval=0.3)
    time.sleep(3)

    # 4. Envio do login
    verificar_foco(janela_app, "Confirmação com Alt + E")
    logging.info("Confirmando login com Alt + E...")
    pg.hotkey("alt", "e")

    # Pausa pós-envio para o sistema processar a autenticação antes de iniciar a Etapa 3
    time.sleep(5)

    logging.info("Solicitação de login enviada com sucesso.")
    return True