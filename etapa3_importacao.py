import time
import logging
import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException

TITULO_SISTEMA = "Spiderware"


def verificar_foco(janela, acao=""):
    janela_ativa = gw.getActiveWindow()
    if janela_ativa != janela:
        titulo_intruso = janela_ativa.title if janela_ativa else "Nenhuma janela ativa"
        raise RuntimeError(
            f"A janela do Spiderware perdeu o foco durante a importação ({acao}). "
            f"Janela em foco no momento: '{titulo_intruso}'"
        )


def obter_janela(timeout=60, intervalo=3):
    """Localiza e ativa a janela do Spiderware com controle de timeout."""
    logging.info("Localizando e validando foco na janela do Spiderware...")
    inicio = time.monotonic()

    while (time.monotonic() - inicio) < timeout:
        janelas = [
            j for j in gw.getWindowsWithTitle(TITULO_SISTEMA)
            if j.visible
            and not j.isMinimized
            and j.width > 100
            and j.height > 100
        ]

        if janelas:
            janela = janelas[0]
            try:
                if gw.getActiveWindow() != janela:
                    janela.activate()
            except PyGetWindowException as e:
                logging.warning(f"Aviso ao tentar focar janela na importação: {e}")
                time.sleep(intervalo)
                continue

            # Pausa para o Windows estabilizar o foco
            time.sleep(2)

            if gw.getActiveWindow() == janela:
                logging.info(
                    f"Janela '{janela.title.strip()}' ativa "
                    f"(Posição: {janela.left},{janela.top} | Tamanho: {janela.width}x{janela.height})."
                )
                return janela

        time.sleep(intervalo)

    logging.error("Não foi possível localizar ou focar a janela do Spiderware na Etapa 3.")
    raise TimeoutError("Tempo limite esgotado ao aguardar a janela do Spiderware para importação.")


def clicar_proporcional(janela, perc_x, perc_y, mensagem, espera_pos=3):
    verificar_foco(janela, acao=mensagem)

    alvo_x = janela.left + int(janela.width * perc_x)
    alvo_y = janela.top + int(janela.height * perc_y)

    logging.info(f"{mensagem} -> Coordenada calculada: ({alvo_x}, {alvo_y})")
    pg.moveTo(alvo_x, alvo_y, duration=0.6)
    pg.click()
    time.sleep(espera_pos)


def realizar_importacao(timeout=60):
    # Respiro inicial para garantir que a tela principal carregou após o login
    time.sleep(3)

    # 1. Janela principal
    janela_principal = obter_janela(timeout=timeout)
    time.sleep(3)

    # 2. Clica no ícone principal de Importação
    clicar_proporcional(
        janela=janela_principal,
        perc_x=0.507,
        perc_y=0.796,
        mensagem="Clicando no ícone principal 'Importação'...",
        espera_pos=3,
    )

    # 3. Clica na opção Importação do submenu
    clicar_proporcional(
        janela=janela_principal,
        perc_x=0.513,
        perc_y=0.890,
        mensagem="Selecionando opção 'Importação' no submenu...",
        espera_pos=5,  # Pausa ampla para abertura e renderização da tela modal
    )

    # 4. Pega a tela modal 'Importação Internet'
    logging.info("Capturando janela modal 'Importação Internet'...")
    janela_modal = obter_janela(timeout=timeout)
    time.sleep(3)

    # 5. Clica no botão Conexão
    clicar_proporcional(
        janela=janela_modal,
        perc_x=0.422,
        perc_y=0.233,
        mensagem="Abrindo menu 'Conexão ▾'...",
        espera_pos=3,
    )

    # 6. Clica na opção Servidor 2
    clicar_proporcional(
        janela=janela_modal,
        perc_x=0.422,
        perc_y=0.340,
        mensagem="Selecionando 'Servidor 2'...",
        espera_pos=5,  # Pausa final para garantir o disparo da carga antes de encerrar
    )

    logging.info("Comando de carga no Servidor 2 disparado com sucesso.")
    return True