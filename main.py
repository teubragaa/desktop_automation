import os
import time
import logging
import pyautogui as pg


# CONFIGURAÇÕES DO AMBIENTE
CAMINHO_REDE = r"S:\SpiderSQL\PROGS\Chamador.exe"

logging.basicConfig(
    filename="rpa_execucao.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

pg.FAILSAFE = True
pg.PAUSE = 0.5


# PRINCIPAIS FUNÇÕES 

def acionar_sistema_operacional():
    logging.info(f"Solicitando ao Windows a execução de: {CAMINHO_REDE}")
    try:
        # Aciona o executável diretamente da unidade S:
        os.startfile(CAMINHO_REDE)
        return True
    except FileNotFoundError:
        logging.critical(f"ARQUIVO NÃO ENCONTRADO. Verifique se a unidade S: está mapeada.")
        return False
    except Exception as e:
        logging.critical(f"Falha crítica ao acionar o sistema: {e}")
        return False

def confirmar_aviso_seguranca():
    # Aguarda a janela de segurança do Windows (que ocorre ao rodar arquivos da rede)
    logging.info("Aguardando 1.5s para o alerta de segurança obter o foco...")
    time.sleep(1.5)
    
    try:
        logging.info("Injetando comando Alt + E (Executar)...")
        pg.hotkey('alt', 'e')
        
        time.sleep(0.5)
        pg.press('enter')
        
        logging.info("Confirmação enviada. Aguardando inicialização do software...")
        time.sleep(2) 
    except Exception as e:
        logging.error(f"Falha ao enviar comandos de teclado: {e}")


# FLUXO PRINCIPAL
def executar_robo():
    print("Iniciando RPA direto da rede...")
    logging.info("--- INÍCIO DA EXECUÇÃO ---")
    
    if acionar_sistema_operacional():
        confirmar_aviso_seguranca()
        print("SUCESSO: Comando nativo enviado e segurança confirmada.")
        logging.info("--- EXECUÇÃO CONCLUÍDA COM SUCESSO ---")
    else:
        print("ERRO: O robô foi interrompido. Verifique o arquivo rpa_execucao.log.")
        logging.error("--- EXECUÇÃO ABORTADA ---")

if __name__ == "__main__":
    executar_robo()