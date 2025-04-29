from flask import Flask
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    # Importa o Blueprint e registra
    from app.routes.auth import auth_bp, init_auth_routes
    init_auth_routes(app, mysql)

    return app
