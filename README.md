# Experimento Microservicios

Este proyecto contiene dos microservicios: recomendación y ventas, que se comunican a través de Kafka.

## Instalación

1. Clona el repositorio.
2. cd recomendacion_service

### Instalar el entorno

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Levantar los contenedores de Kafka y Zookeeper
docker compose up -d

### Levantar proyectos
Ejecutar el producer en una terminal
python3 ventas_service/app.py

En otra terminal ejecutar el consumer
python3 recomendacion_service/app.py

### Prueba
curl -X POST http://127.0.0.1:5002/recomendar -H "Content-Type: application/json" -d '{"video_id": "1111"}'