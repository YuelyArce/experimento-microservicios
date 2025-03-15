from flask import Flask, request, jsonify
from utils.logger import log_event 

app = Flask(__name__)

@app.route('/evento', methods=['POST'])
def registrar_evento():
    """Recibe eventos de auditoría y los envía a Graylog"""
    data = request.get_json()
    
    usuario = data.get("usuario", "desconocido")
    estado = data.get("estado", "desconocido")
    rol= data.get("rol", "desconocido")
    detalles = data.get("detalles", "")

    log_event(usuario, rol, estado, detalles) 

    return jsonify({"mensaje": "Evento registrado con éxito"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)