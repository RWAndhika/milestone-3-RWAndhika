from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from controllers.users import users_routes, s
from controllers.accounts import accounts_routes
from controllers.transactions import transactions_routes

from flask_login import LoginManager
from models.users import Users

import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(users_routes)
app.register_blueprint(accounts_routes)
app.register_blueprint(transactions_routes)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return s.query(Users).get(int(user_id))

@app.route("/")
def hello_world():
    return "Copy and paste this for api docs: https://documenter.getpostman.com/view/33841449/2sA3dyir9T"