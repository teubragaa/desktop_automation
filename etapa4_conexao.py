import time
import ctypes
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
            f"A janela do Spiderware perdeu o foco ({acao}). "
            f"Janela em foco no momento: '{titulo_intruso}'"
        )


def garantir_spiderware_aberto(acao=""):
    janelas = [
        j for j in gw.getWindowsWithTitle(TITULO_SISTEMA)
        if j.visible and not j.isMinimized
    ]
    if not janelas:
        raise RuntimeError(
            f"O Spiderware foi fechado ou não está visível ({acao})."
        )


def obter_janela(timeout=60, intervalo=3):
    """Localiza e ativa especificamente a janela modal 'Importação Internet'."""
    logging.info("Localizando e validando foco na janela 'Importação Internet'...")
    inicio = time.monotonic()

    while (time.monotonic() - inicio) < timeout:
        janelas = [
            j for j in gw.getWindowsWithTitle(TITULO_SISTEMA)
            if j.visible
            and not j.isMinimized
            and 100 < j.width < 800
            and j.height > 100
        ]

        if janelas:
            janela = janelas[0]
            try:
                if gw.getActiveWindow() != janela:
                    janela.activate()
            except PyGetWindowException as e:
                logging.warning(f"Aviso ao tentar focar janela modal: {e}")
                time.sleep(intervalo)
                continue

            time.sleep(2)

            if gw.getActiveWindow() == janela:
                logging.info(
                    f"Janela '{janela.title.strip()}' ativa "
                    f"(Posição: {janela.left},{janela.top} | Tamanho: {janela.width}x{janela.height})."
                )
                return janela

        time.sleep(intervalo)

    logging.error("Não foi possível localizar ou focar a janela 'Importação Internet' na Etapa 4.")
    raise TimeoutError("Tempo limite esgotado ao aguardar a janela 'Importação Internet'.")


def clicar_proporcional(janela, perc_x, perc_y, mensagem, espera_pos=3):
    verificar_foco(janela, acao=mensagem)

    alvo_x = janela.left + int(janela.width * perc_x)
    alvo_y = janela.top + int(janela.height * perc_y)

    logging.info(f"{mensagem} -> Coordenada calculada: ({alvo_x}, {alvo_y})")
    pg.moveTo(alvo_x, alvo_y, duration=0.6)
    pg.click()
    time.sleep(espera_pos)


def checkbox_esta_marcado(janela, perc_x=0.095, perc_y=0.723):
    """Verifica se o checkbox 'Requerimento de Secundário' está marcado (ignora borda cinza)."""
    centro_x = janela.left + int(janela.width * perc_x)
    centro_y = janela.top + int(janela.height * perc_y)

    hdc = ctypes.windll.user32.GetDC(0)
    marcado = False
    try:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                cor = ctypes.windll.gdi32.GetPixel(hdc, centro_x + dx, centro_y + dy)
                r = cor & 0xFF
                g = (cor >> 8) & 0xFF
                b = (cor >> 16) & 0xFF
                # Só considera marcado se achar pixel bem preto (< 60), ignorando borda cinza (105)
                if r < 60 and g < 60 and b < 60:
                    marcado = True
                    break
            if marcado:
                break
    finally:
        ctypes.windll.user32.ReleaseDC(0, hdc)

    logging.info(f"Verificação 'Requerimento de Secundário' em ({centro_x}, {centro_y}) | Marcado={marcado}")
    return marcado


def realizar_conexao(timeout=60):
    # 1. Captura a janela modal 'Importação Internet' aberta na Etapa 3
    janela_modal = obter_janela(timeout=timeout)
    time.sleep(2)

    # 2. Se "Requerimento de Secundário" estiver marcado, desmarca via teclado (Espaço)
    if checkbox_esta_marcado(janela_modal, perc_x=0.095, perc_y=0.723):
        verificar_foco(janela_modal, acao="Desmarcando 'Requerimento de Secundário'")
        logging.info("Desmarcando 'Requerimento de Secundário' com tecla Espaço...")
        pg.press("space")
        time.sleep(1.5)
    else:
        logging.info("'Requerimento de Secundário' já está desmarcado.")

    # 3. Clica no botão Conexão (aqui precisa de mouse porque Alt+C aciona Cancelar)
    clicar_proporcional(
        janela=janela_modal,
        perc_x=0.422,
        perc_y=0.233,
        mensagem="Abrindo menu 'Conexão ▾'...",
        espera_pos=3,
    )

    # 4. Clica na opção Servidor 2
    clicar_proporcional(
        janela=janela_modal,
        perc_x=0.422,
        perc_y=0.340,
        mensagem="Selecionando 'Servidor 2'...",
        espera_pos=3,
    )

    # 5. Confirma o pop-up inicial de conexão (OK)
    garantir_spiderware_aberto("Confirmação da conexão")
    logging.info("Confirmando a conexão com êxito...")
    time.sleep(1)
    pg.press("enter")
    logging.info("Janela de conexão confirmada.")
    time.sleep(2)
    return True