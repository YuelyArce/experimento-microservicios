import requests
from flask import Flask, request, jsonify
from utils.logger import log_event 


app = Flask(__name__)

@app.route('/evento', methods=['POST'])
def registrar_evento():
    """Recibe eventos de auditoría y los envía a Graylog"""
    data = request.get_json()

    print(data)
    
    usuario = data.get("usuario", "desconocido")
    estado = data.get("estado", "desconocido")
    rol= data.get("rol", "desconocido")
    detalles = data.get("detalles", "")

    log_event(usuario, rol, estado, detalles) 

    return jsonify({"mensaje": "Evento registrado con éxito"}), 201


@app.route('/evento_graylog', methods=['POST'])
def registrar_evento_graylog():
    """Recibe eventos enviados desde Graylog y los registra en el sistema."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibió JSON válido"}), 400

    print("📥 Evento recibido desde Graylog")
    usuario = data.get('event', {}).get('fields', {}).get('usuario', 'Desconocido')
    print('el usuario es: ' + usuario)

    url = "http://localhost:3001/black"
    headers = {"Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJ1c3VhcmlvIjoib21hciIsImV4cCI6MTc0NDg2NjIxMH0.5iQQimWqPPyuxuuGWQwVs5mAvRKG44t0Hw6vGH9F8Fs"}  # Token válido para autenticar
    payload = {"usuario": usuario}

    response = requests.post(url, json=payload, headers=headers)

    return jsonify({"mensaje": "Usuario bloqueado correctamente. "})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)