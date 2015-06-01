from flask import Flask, g
from flask.ext import restful
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')

app.config.from_object('config')

api = restful.Api(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user

import massive.auth
import massive.views
