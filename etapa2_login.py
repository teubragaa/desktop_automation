import time
import logging
import pyautogui as pg
from automacao_base import SpiderwareUI


def realizar_login(usuario, senha, timeout=60):
    """Realiza a autenticação do usuário na tela inicial de login do Spiderware."""
    if not usuario or not senha:
        raise ValueError("Usuário ou senha não foram informados nas configurações.")

    # 1. Localiza e foca a janela de login
    janela_login = SpiderwareUI.obter_janela(timeout=timeout)
    time.sleep(3)

    # 2. Preenchimento do usuário
    SpiderwareUI.verificar_foco(janela_login, "Preenchimento do usuário")
    logging.info("Preenchendo usuário...")
    pg.write(str(usuario), interval=0.3)
    time.sleep(2)

    # 3. Navegação para o campo de senha
    SpiderwareUI.verificar_foco(janela_login, "Navegação para senha")
    logging.info("Avançando para o campo de senha (Tab)...")
    pg.press("tab")
    time.sleep(2)

    # 4. Preenchimento da senha
    SpiderwareUI.verificar_foco(janela_login, "Preenchimento da senha")
    logging.info("Preenchendo senha...")
    pg.write(str(senha), interval=0.3)
    time.sleep(2)

    # 5. Confirmação do login
    SpiderwareUI.verificar_foco(janela_login, "Confirmação com Alt + E")
    logging.info("Confirmando login (Alt + E)...")
    pg.hotkey("alt", "e")
    time.sleep(5)

    logging.info("Solicitação de login enviada com sucesso.")
    return True