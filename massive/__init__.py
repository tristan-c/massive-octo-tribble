from flask import Flask
from flask.ext import restful
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__, static_url_path='')

app.config['MONGODB_SETTINGS'] = {
                                        'DB': 'massive',
                                        'HOST':'127.0.0.1',
                                        'PORT':27017
                                    }

db = MongoEngine(app)
api = restful.Api(app)

import massive.views