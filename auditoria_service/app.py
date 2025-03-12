# app.py
from flask import Flask, request, jsonify
from utils.logger import registrar_evento

app = Flask(__name__)

@app.route('/evento', methods=['POST'])
def registrar():
    """Registra eventos de auditoría desde otros microservicios"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ("usuario", "accion", "producto_id", "detalles")):
        return jsonify({"error": "El cuerpo de la solicitud debe incluir 'usuario', 'accion', 'producto_id' y 'detalles'"}), 400

    usuario = data["usuario"]
    accion = data["accion"]
    producto_id = data["producto_id"]
    detalles = data["detalles"]

    # Llamar a la función para registrar el evento
    registrar_evento(usuario, accion, producto_id, detalles)
    
    return jsonify({"mensaje": "Evento registrado con éxito"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
