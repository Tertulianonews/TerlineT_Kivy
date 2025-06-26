import logging
import sys

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Criar logger principal
logger = logging.getLogger('TerlineT')


def info(message):
    logger.info(message)


def error(message, exc_info=False):
    logger.error(message, exc_info=exc_info)


def warning(message):
    logger.warning(message)


def debug(message):
    logger.debug(message)
