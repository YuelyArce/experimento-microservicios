import logging
import graypy
import json

# Configurar el logger
logger = logging.getLogger('auditoria_logger')
logger.setLevel(logging.INFO)


GRAYLOG_HOST = '127.0.0.1'
GRAYLOG_PORT = 12201

handler = graypy.GELFUDPHandler(GRAYLOG_HOST, GRAYLOG_PORT)
logger.addHandler(handler)

def log_event(usuario, rol, estado, detalles=""):
    """Registra eventos en Graylog."""
    mensaje = {
        "usuario": usuario,
        "rol":rol,
        "estado": estado,
        "detalles": detalles
    }
    json_mensaje = json.dumps(mensaje, ensure_ascii=False)
    logger.info(json_mensaje)