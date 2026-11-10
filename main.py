import logging
import pyautogui as pg
from config import USUARIO_APP, SENHA_APP
from etapa1_abertura import iniciar_chamador
from etapa2_login import realizar_login
from etapa3_importacao import realizar_importacao

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("rpa_execucao.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Configurações de segurança do PyAutoGUI
pg.FAILSAFE = True
pg.PAUSE = 0.5

def orquestrador():
    logging.info("[INÍCIO] Execução da Automação - Spiderware")

    try:
        # Etapa 1: Abertura do aplicativo
        logging.info("[ETAPA 1] Iniciando abertura do aplicativo e aviso de segurança...")
        iniciar_chamador()
        logging.info("[ETAPA 1] Concluída com sucesso.")

        # Etapa 2: Autenticação
        logging.info("[ETAPA 2] Iniciando login no Spiderware...")
        realizar_login(USUARIO_APP, SENHA_APP)
        logging.info("[ETAPA 2] Login realizado com sucesso.")

        # Etapa 3: Navegação e Importação
        logging.info("[ETAPA 3] Iniciando processo de importação de dados...")
        realizar_importacao()
        logging.info("[ETAPA 3] Importação concluída com sucesso.")

    except Exception as e:
        logging.error(f"[FALHA] Processo interrompido: {e}") 
        raise


if __name__ == "__main__":
    orquestrador()