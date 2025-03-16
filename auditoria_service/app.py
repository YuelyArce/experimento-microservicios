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

    return jsonify({"mensaje": "Evento recibido y registrado con éxito"}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)