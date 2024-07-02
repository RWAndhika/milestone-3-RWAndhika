from flask import Flask
from dotenv import load_dotenv, find_dotenv
from connectors.mysql_connector import connection

from sqlalchemy.orm import sessionmaker

from controllers.users import users_routes

from flask_login import LoginManager
from models.users import Users

import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(users_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    Session = sessionmaker(connection)
    s = Session()
    return s.query(Users).get(int(user_id))

@app.route("/")
def hello_world():
    return "Hello World!"