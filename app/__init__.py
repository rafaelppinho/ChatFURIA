from flask import Flask
from flask_mysqldb import MySQL
from app.config import Config
from app.auth import init_auth_routes

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)
    init_auth_routes(app, mysql)

    return app
