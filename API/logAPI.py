import logging
import os
import re

def gerar_nome_log() -> str:
    """
    Gera nome de arquivo de log numerado na pasta logs/.
    Ex.: logs/log_1.log, logs/log_2.log, etc.
    """
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    arquivos = os.listdir('logs')
    numeros = []

    for nome in arquivos:
        match = re.match(r'log_(\d+)\.log', nome)
        if match:
            numeros.append(int(match.group(1)))

    proximo_numero = max(numeros) + 1 if numeros else 1
    return f'logs/log_{proximo_numero}.log'

def setup_logging() -> logging.Logger:
    """
    Configura o logging e retorna o logger para ser usado em outros módulos.
    """
    log_filename = gerar_nome_log()
    
    logging.basicConfig(
        filename=log_filename,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    return logger

if __name__ == '__main__':
    pass