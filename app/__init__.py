from flask import Flask
from flask_mysqldb import MySQL
from app.config import Config  # ← Caminho corrigido
from app.routes.auth import auth_routes
from app.routes.chat import chat_routes

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    # Registrar rotas
    auth_routes(app, mysql)
    chat_routes(app, mysql)

    return app
