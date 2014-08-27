from flask.ext.restful import Resource
from massive import api, app
from massive.models import *

class getLinks(Resource):
    def get(self):
        links = Links.objects()

        return [link.dump for link in links]

api.add_resource(getLinks,'/links')#,'/trip/<string:ticketId>')