import time
import ctypes
import logging
import pyautogui as pg
import pygetwindow as gw
from pygetwindow import PyGetWindowException


class _GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("hwndActive", ctypes.c_void_p),
        ("hwndFocus", ctypes.c_void_p),
        ("hwndCapture", ctypes.c_void_p),
        ("hwndMenuOwner", ctypes.c_void_p),
        ("hwndMoveSize", ctypes.c_void_p),
        ("hwndCaret", ctypes.c_void_p),
        ("rcCaret", ctypes.c_long * 4),
    ]


class SpiderwareUI:
    """Centraliza o gerenciamento de janelas, foco e interações no Spiderware."""

    TITULO = "Spiderware"

    @classmethod
    def garantir_aberto(cls, acao=""):
        """Verifica se há pelo menos uma janela visível do sistema em execução."""
        janelas = [
            j for j in gw.getWindowsWithTitle(cls.TITULO)
            if j.visible and not j.isMinimized
        ]
        if not janelas:
            raise RuntimeError(f"O Spiderware foi fechado ou não está visível ({acao}).")

    @staticmethod
    def verificar_foco(janela, acao=""):
        """Valida se a janela alvo está em foco, tentando reativá-la uma vez antes de falhar."""
        if gw.getActiveWindow() != janela:
            try:
                janela.activate()
                time.sleep(0.5)
            except PyGetWindowException:
                pass

        janela_ativa = gw.getActiveWindow()
        if janela_ativa != janela:
            intruso = janela_ativa.title if janela_ativa else "Nenhuma janela ativa"
            raise RuntimeError(f"Perda de foco ({acao}). Janela ativa: '{intruso}'")

    @classmethod
    def obter_janela(cls, timeout=60, intervalo=2, larg_min=100, larg_max=9999):
        """Localiza e ativa uma janela do sistema dentro da faixa de largura informada."""
        logging.info("Localizando e validando foco na janela do Spiderware...")
        inicio = time.monotonic()

        while (time.monotonic() - inicio) < timeout:
            janelas = [
                j for j in gw.getWindowsWithTitle(cls.TITULO)
                if j.title.strip() == cls.TITULO
                and j.visible
                and not j.isMinimized
                and larg_min < j.width < larg_max
                and j.height > 100
            ]

            if janelas:
                janela = janelas[0]
                try:
                    if gw.getActiveWindow() != janela:
                        janela.activate()
                    time.sleep(1.5)
                    if gw.getActiveWindow() == janela:
                        logging.info(
                            f"Janela '{janela.title.strip()}' ativa "
                            f"(Posição: {janela.left},{janela.top} | Tamanho: {janela.width}x{janela.height})."
                        )
                        return janela
                except PyGetWindowException as e:
                    logging.warning(f"Aviso ao focar janela: {e}")

            time.sleep(intervalo)

        raise TimeoutError("Tempo limite esgotado ao aguardar a janela do Spiderware.")

    @classmethod
    def clicar_proporcional(cls, janela, perc_x, perc_y, mensagem, espera_pos=2.5):
        """Move o cursor e realiza clique proporcional às dimensões da janela."""
        cls.verificar_foco(janela, acao=mensagem)
        alvo_x = janela.left + int(janela.width * perc_x)
        alvo_y = janela.top + int(janela.height * perc_y)

        logging.info(f"{mensagem} -> Coordenada calculada: ({alvo_x}, {alvo_y})")
        pg.moveTo(alvo_x, alvo_y, duration=0.6)
        pg.click()
        time.sleep(espera_pos)

    @classmethod
    def aguardar_popup(cls, janela_referencia, descricao, timeout=60):
        """Aguarda a abertura de um modal secundário ou aviso de confirmação."""
        logging.info(f"Aguardando janela: {descricao}...")
        inicio = time.monotonic()

        while (time.monotonic() - inicio) < timeout:
            cls.garantir_aberto(descricao)
            ativa = gw.getActiveWindow()
            if ativa and (ativa != janela_referencia or ativa.width < 450):
                time.sleep(0.5)
                return ativa
            time.sleep(0.5)

        logging.warning(f"Tempo limite ({timeout}s) atingido aguardando '{descricao}'. Prosseguindo...")
        return gw.getActiveWindow()

    @staticmethod
    def checkbox_focado_marcado(janela):
        """Consulta via API Win32 (BM_GETCHECK) se o checkbox em foco está marcado."""
        user32 = ctypes.windll.user32
        gti = _GUITHREADINFO(cbSize=ctypes.sizeof(_GUITHREADINFO))
        tid = user32.GetWindowThreadProcessId(janela._hWnd, None)

        if user32.GetGUIThreadInfo(tid, ctypes.byref(gti)) and gti.hwndFocus:
            estado = user32.SendMessageW(gti.hwndFocus, 0x00F0, 0, 0)
            marcado = (estado == 1)
            logging.info(f"Estado do checkbox (BM_GETCHECK={estado}) | Marcado={marcado}")
            return marcado

        raise RuntimeError("Não foi possível identificar o controle em foco na janela.")