from flask import Flask, request, jsonify
from flask_restful import Api
from vistas import Home, Ventas

app = Flask(__name__)
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(Home, '/')
api.add_resource(Ventas, '/registroVenta')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
