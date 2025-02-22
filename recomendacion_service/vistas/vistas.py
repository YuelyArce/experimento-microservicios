from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_restful import Resource

class Home(Resource):

    def get(self):
        return "Servicio de Recomendaciones en ejecución"


class Recomendaciones(Resource):

    def post(self):
        data = request.json
        video_id = data.get("video_id")

        if not video_id:
            return jsonify({"error": "Falta el video_id"}), 400

        # Generar recomendaciones
        recomendaciones = [f"video_recomendado_{i}" for i in range(1, 4)]

        return jsonify({"video_id": video_id, "recomendaciones": recomendaciones})
    