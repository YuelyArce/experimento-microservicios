import logging
import graypy

# Configurar el logger
logger = logging.getLogger('auditoria_logger')
logger.setLevel(logging.INFO)

# Reemplaza con la IP de tu servidor Graylog
GRAYLOG_HOST = '127.0.0.1'
GRAYLOG_PORT = 12201

handler = graypy.GELFUDPHandler(GRAYLOG_HOST, GRAYLOG_PORT)
logger.addHandler(handler)

def log_event(usuario, rol, estado, detalles=""):
    """Registra eventos en Graylog."""
    mensaje = {
        "usuario": usuario,
        'rol':rol,
        "estado": estado,
        "detalles": detalles
    }
    logger.info(mensaje)