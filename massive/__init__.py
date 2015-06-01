from flask import Flask, g
from flask.ext import restful
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt
from pony.orm import Database

app = Flask(__name__, static_url_path='')

app.config.from_object('config')

api = restful.Api(app)
bcrypt = Bcrypt(app)
db = Database('sqlite', 'app.db', create_db=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user

import massive.auth
import massive.views
