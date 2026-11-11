import os
import sys
import time
import ctypes
import logging
from datetime import datetime
import pyautogui as pg

from config import USUARIO_APP, SENHA_APP
from etapa1_abertura import iniciar_chamador
from etapa2_login import realizar_login
from etapa3_importacao import realizar_importacao

# Garante que logs e prints sejam salvos na mesma pasta do .exe ou do script main.py
if getattr(sys, "frozen", False):
    PASTA_BASE = os.path.dirname(sys.executable)
else:
    PASTA_BASE = os.path.dirname(os.path.abspath(__file__))

CAMINHO_LOG = os.path.join(PASTA_BASE, "rpa_execucao.log")
PASTA_ERROS = os.path.join(PASTA_BASE, "erros_screenshots")

# Configuração de logs com caminho absoluto seguro
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(CAMINHO_LOG, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

# Configurações do PyAutoGUI ajustadas para servidor e execução cadenciada
pg.FAILSAFE = False
pg.PAUSE = 1.0


def configurar_dpi_windows():
    """Evita que escalas de zoom do Windows (125%, 150%) desalinhem os cliques da Etapa 3."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def registrar_print_erro():
    """Salva uma imagem da tela no momento exato da falha para facilitar o diagnóstico."""
    try:
        os.makedirs(PASTA_ERROS, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_print = os.path.join(PASTA_ERROS, f"falha_{timestamp}.png")
        pg.screenshot(arquivo_print)
        logging.info(f"Evidência visual do erro salva em: {arquivo_print}")
    except Exception as erro_print:
        logging.warning(f"Não foi possível salvar o print da tela: {erro_print}")

def limpar_arquivos_antigos(dias_retencao=7):
    """Remove automaticamente logs e prints de erro com mais de 7 dias (1 semana)."""
    limite_tempo = datetime.now() - timedelta(days=dias_retencao)
    
    # 1. Limpeza de prints antigos na pasta de erros
    if os.path.exists(PASTA_ERROS):
        for arquivo in os.listdir(PASTA_ERROS):
            caminho_arquivo = os.path.join(PASTA_ERROS, arquivo)
            if os.path.isfile(caminho_arquivo):
                data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
                if data_modificacao < limite_tempo:
                    try:
                        os.remove(caminho_arquivo)
                        logging.info(f"[FAXINA] Print antigo removido (> 7 dias): {arquivo}")
                    except Exception as e:
                        logging.warning(f"[FAXINA] Não foi possível remover o print {arquivo}: {e}")

    # 2. Gerenciamento do arquivo de log principal (rpa_execucao.log)
    if os.path.exists(CAMINHO_LOG):
        data_mod_log = datetime.fromtimestamp(os.path.getmtime(CAMINHO_LOG))
        if data_mod_log < limite_tempo:
            try:
                os.remove(CAMINHO_LOG)
                logging.info("[FAXINA] Log principal antigo resetado por expurgo de 7 dias.")
            except Exception as e:
                logging.warning(f"[FAXINA] Não foi possível limpar o log antigo: {e}")
                
def orquestrador():
    configurar_dpi_windows()
    logging.info("[INÍCIO] Execução da Automação - Spiderware")

    try:
        # Etapa 1: Abertura do aplicativo
        logging.info("[ETAPA 1] Iniciando abertura do aplicativo e aviso de segurança...")
        iniciar_chamador()
        logging.info("[ETAPA 1] Concluída com sucesso.")
        time.sleep(3)

        # Etapa 2: Autenticação
        logging.info("[ETAPA 2] Iniciando login no Spiderware...")
        realizar_login(USUARIO_APP, SENHA_APP)
        logging.info("[ETAPA 2] Login realizado com sucesso.")
        time.sleep(3)

        # Etapa 3: Navegação e Importação
        logging.info("[ETAPA 3] Iniciando processo de importação de dados...")
        realizar_importacao()
        logging.info("[ETAPA 3] Importação concluída com sucesso.")

        logging.info("[SUCESSO] Fluxo completo finalizado sem erros.")

    except Exception as e:
        logging.exception(f"[FALHA] Processo interrompido: {e}")
        registrar_print_erro()
        sys.exit(1)


if __name__ == "__main__":
    orquestrador()