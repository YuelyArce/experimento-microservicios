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

    Este proyecto contiene dos microservicios: login, auditoria_service, black_list_service y logistica_service
    ## Instalación

    1. Clona el repositorio.
    2. cd experimento-microservicios

    ### Levantar los contenedores
    docker compose up -d
    Ingresar desde el navegador a:http://localhost:9000
        usuario:admin
        contraseña:password

    configurar graylog 5.1:

        1.configuración de rastreo de eventos:
            1️⃣ Ve a Graylog → “System / Inputs”
            2️⃣ Selecciona “GELF UDP” y haz clic en “Launch new input”
            3️⃣ poner un nombre y verificar que la conexión en el puerto: 12201

        2.configurar extractor de datos:
            1️⃣ Ve a Graylog → “Manage extractors” → create extractors → buscar 'message'
            2️⃣ Selecciona “JSON' y luego Try para verificar funcionamiento
            3️⃣ create extrator

        3.configurar notificación:
            1️⃣ Ve a Graylog → “Alerts” → "notifications" → create notification
            2️⃣ Poner titulo, seleccionar tipo HTTP, usar esta url: http://host.docker.internal:5004/evento_graylog
            3️⃣ create notifiación

        4.definición del evento:
            1️⃣ Ve a Graylog → “Alerts” → "event definition" → create event definition
            2️⃣ Poner titulo, poner pripridad del evento, seleccionar condiciones: 'Filter & Aggregation, definir query: 'NOT rol:admin', seleccionar streams: default stream,
            3️⃣ seguir a notificaciones y seleccionar la notificcación antes creada y crear.

        5.optimización del evento:
            1️⃣ Ve a Graylog → “Alerts” → "event definition" → editar el evento antes creado
            2️⃣ ir a Filter & Aggregation y configurar:
                Search within the last:10 segundos
                Execute search every: 10 segundos
            3️⃣ ir a fields y 'add custom fields' y configurar:
                name:usuario
                set value from: template
                Template:${source.usuario}
            4️⃣ en notifications configurar:
                Grace Period:0
                Message Backlog:0


    ### Instalar el entorno por proyecto - login, auditoria_service, black_list_service y logistica_service

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

    cd auditoria_service

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    cd black_list_service

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

    En otra terminal ejecutar auditoria_service
    python3 app.py

    En otra terminal ejecutar black_list_service
    python3 app.py


    con esta prueba se bloqueara el usuario adriana:

    ### Prueba de login
    curl -X POST "http://localhost:5001/login" \
     -H "Content-Type: application/json" \
     -d '{"usuario": "adriana", "password": "1234"}'

    ### Prueba de modificación de método de conservación en logistica_service
    curl -X PUT "http://127.0.0.1:4001/producto/1" \
     -H "Content-Type: application/json" \
     -H "Token: se copia el token generado" \
     -d '{"tipo_almacenamiento": "Congelado"}'