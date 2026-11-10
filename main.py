import logging
import pyautogui as pg
from config import USUARIO_APP, SENHA_APP
from etapa1_abertura import iniciar_chamador
from etapa2_login import realizar_login

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("rpa_execucao.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# CONFIGURAÇÕES DO PYAUTOGUI
pg.FAILSAFE = True
pg.PAUSE = 0.5

def orquestrador():
    logging.info("=== INÍCIO DA AUTOMAÇÃO ===")
    
    try:
        # Etapa 1: Abre o sistema
        iniciar_chamador()
        
        # Etapa 2: Faz o login
        realizar_login(USUARIO_APP, SENHA_APP)
        
        logging.info("Login finalizado com sucesso. Robô pronto para a próxima ação.")
        
    except Exception as e:
        logging.error(f"Automação interrompida: {e}")
        
    finally:
        logging.info("=== FIM DA AUTOMAÇÃO ===")

if __name__ == "__main__":
    orquestrador()