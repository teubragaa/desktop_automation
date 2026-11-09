
import pyautogui as pg
import pygetwindow as gw
import time
import logging

# Configurações
APP = "Ferramenta de Captura"
TITULO_JANELA = "Ferramenta de Captura"

# Coordenadas do botão Iniciar (ajustar conforme a tela)
BOTAO_INICIAR = (25, 1050)

logging.basicConfig(
    filename="rpa.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

pg.FAILSAFE = True
pg.PAUSE = 0.3


def verificar_janela():
    """Verifica se o aplicativo está aberto."""
    janelas = gw.getWindowsWithTitle(TITULO_JANELA)
    return any(janela.visible for janela in janelas)


def aguardar_janela(timeout=8):
    """Espera a janela aparecer."""
    inicio = time.monotonic()

    while time.monotonic() - inicio < timeout:
        if verificar_janela():
            return True

        time.sleep(0.5)

    return False


def abrir_pelo_teclado():
    """Primeira estratégia: pesquisa pelo menu Iniciar."""
    logging.info("Tentando abrir pelo teclado")

    pg.press("win")
    time.sleep(1)

    pg.write(APP, interval=0.05)
    time.sleep(2)

    pg.press("enter")

    return aguardar_janela()


def abrir_pelo_mouse():
    """Segunda estratégia: clicar no menu Iniciar."""
    logging.info("Tentando abrir pelo mouse")

    pg.click(*BOTAO_INICIAR)
    time.sleep(1)

    pg.write(APP, interval=0.05)
    time.sleep(2)

    pg.press("enter")

    return aguardar_janela()


def executar():
    # Evita abrir novamente se já estiver aberto
    if verificar_janela():
        logging.info("Aplicativo já estava aberto")
        print("Aplicativo já está aberto!")
        return

    if abrir_pelo_teclado():
        logging.info("Aplicativo aberto pelo teclado")
        print("SUCESSO: aberto pelo teclado!")
        return


    logging.warning("Tentativa pelo teclado falhou")

    if abrir_pelo_mouse():
        logging.info("Aplicativo aberto pelo mouse")
        print("SUCESSO: aberto pelo mouse!")
        return

    logging.error("Falha nas duas estratégias")
    raise RuntimeError("Não foi possível abrir o aplicativo")


if __name__ == "__main__":
    executar()
