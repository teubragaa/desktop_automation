import os
import sys
import time
import ctypes
import logging
import pyautogui as pg

from config import USUARIO_APP, SENHA_APP
from etapa1_abertura import iniciar_chamador
from etapa2_login import realizar_login
from etapa3_importacao import realizar_importacao
from etapa4_conexao import realizar_conexao
from etapa5_finalizacao import realizar_importacao_final

# Define o diretório base para gravação do log (compatível com script .py e executável .exe)
if getattr(sys, "frozen", False):
    PASTA_BASE = os.path.dirname(sys.executable)
else:
    PASTA_BASE = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOG = os.path.join(PASTA_BASE, "rpa_execucao.log")

# Configuração global de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(CAMINHO_LOG, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

pg.FAILSAFE = False
pg.PAUSE = 1.0


def configurar_dpi_windows():
    """Configura a aplicação como DPI-Aware no Windows para evitar distorção de coordenadas."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def orquestrador():
    """Orquestra a execução sequencial das 5 etapas da automação no Spiderware."""
    configurar_dpi_windows()
    logging.info("[INÍCIO] Execução da Automação - Spiderware")

    try:
        # Etapa 1: Abertura do aplicativo
        logging.info("[ETAPA 1] Iniciando abertura do aplicativo...")
        iniciar_chamador()
        logging.info("[ETAPA 1] Concluída.")
        time.sleep(3)

        # Etapa 2: Autenticação
        logging.info("[ETAPA 2] Iniciando login no Spiderware...")
        realizar_login(USUARIO_APP, SENHA_APP)
        logging.info("[ETAPA 2] Login realizado.")
        time.sleep(3)

        # Etapa 3: Navegação até o módulo de importação
        logging.info("[ETAPA 3] Acessando módulo 'Importação Internet'...")
        realizar_importacao()
        logging.info("[ETAPA 3] Módulo aberto.")
        time.sleep(3)

        # Etapa 4: Desmarcação preventiva e conexão no Servidor 2
        logging.info("[ETAPA 4] Iniciando conexão com Servidor 2...")
        realizar_conexao()
        logging.info("[ETAPA 4] Conexão concluída.")
        time.sleep(2)

        # Etapa 5: Marcação de parâmetro, ajuste de período e importação final
        logging.info("[ETAPA 5] Iniciando importação final...")
        realizar_importacao_final()
        logging.info("[ETAPA 5] Importação final concluída.")

        logging.info("[SUCESSO] Fluxo completo finalizado sem erros.")

    except Exception as e:
        logging.error(f"[FALHA] Processo interrompido: {e}")
        sys.exit(1)


if __name__ == "__main__":
    orquestrador()