import logging
import pyautogui as pg
from config import USUARIO_APP, SENHA_APP
from etapa1_abertura import iniciar_chamador
from etapa2_login import realizar_login

# Configuração de log com a sintaxe corrigida
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
    logging.info("=== INÍCIO DA AUTOMAÇÃO ===")
    
    try:
        # Etapa 1: Abre o atalho e trata avisos do Windows
        iniciar_chamador()
        
        # Etapa 2: Preenche e envia o login
        realizar_login(USUARIO_APP, SENHA_APP)
        
        logging.info("Login concluído com sucesso. Robô pronto para a Etapa 3.")
        
    except Exception as e:
        # exc_info=True grava o traceback detalhado no arquivo de log
        logging.error(f"Automação interrompida: {e}", exc_info=True)
        raise
        
    finally:
        logging.info("=== FIM DA AUTOMAÇÃO ===")

if __name__ == "__main__":
    orquestrador()