# Experimento Microservicios

Este proyecto contiene dos microservicios: recomendación y ventas, que se comunican a través de Kafka.

## Instalación

1. Clona el repositorio.
2. cd recomendacion_service

### Instalar el entorno por proyecto

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Levantar los contenedores de Kafka y Zookeeper
docker compose up -d

### Levantar proyectos
Ejecutar el producer en una terminal-ventas_service
python3 app.py

En otra terminal ejecutar el consumer-recomendacion_service
python3 app.py

### Prueba de reomendación
curl -X POST http://127.0.0.1:5001/recomendar -H "Content-Type: application/json" -d '{"video_id": "12345"}'

### Prueba de ventas
curl -X POST http://localhost:5002/registroVenta -H "Content-Type: application/json" -d '{"producto_id": "123", "cantidad": 2, "precio": 10.5}'