# Experimento Microservicios 1

    Este proyecto contiene dos microservicios: recomendación y ventas, que se comunican a través de Kafka.

    ## Instalación

    1. Clona el repositorio.
    2. cd experimento-microservicios

    ### Instalar el entorno por proyecto - ventas_service y recomendacion_service

    cd ventas_service

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    cd recomendacion_service

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

    ### abrir prometeus
    entrar a http://localhost:9090/

    ### abrir grafana
    entrar a http://localhost:3000/
    usuario: admin
    contraseña: admin
    data connection: http://prometheus:9090

# Experimento Microservicios 2

    Este proyecto contiene dos microservicios: login y logistica_service
    ## Instalación

    1. Clona el repositorio.
    2. cd experimento-microservicios

    ### Levantar los contenedores
    docker compose up -d
    Ingresar desde el navegador a:http://localhost:9000
        usuario:admin
        contraseña:password

    configurar graylog:
    1️⃣ Ve a Graylog → “System / Inputs”
    2️⃣ Selecciona “GELF UDP” y haz clic en “Launch new input”
    3️⃣ poner un nombre y verificar que la conexión en el puerto: 12201

    ### Instalar el entorno por proyecto - login y logistica_service

    cd login

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    cd logistica_service

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
    ### Levantar proyectos
    Ejecutar login en una terminal
    python3 app.py

    En otra terminal ejecutar logistica_service
    python3 app.py

    ### Prueba de login
    curl -X POST "http://localhost:5001/login" \
     -H "Content-Type: application/json" \
     -d '{"usuario": "adriana", "password": "1234"}'

    ### Prueba de modificación de método de conservación en logistica_service
    curl -X PUT "http://127.0.0.1:4001/producto/1" \
     -H "Content-Type: application/json" \
     -H "Token: se copia el token generado" \
     -d '{"tipo_almacenamiento": "Congelado"}'