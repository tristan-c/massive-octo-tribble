from os import urandom

from flask import Flask, g
from flask.ext import restful
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager, current_user
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__, static_url_path='')

app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = urandom(24)

app.config['MONGODB_SETTINGS'] = {
    'DB': 'massive',
    'HOST': '127.0.0.1',
    'PORT': 27017
}

db = MongoEngine(app)
api = restful.Api(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user

import massive.auth
import massive.views
