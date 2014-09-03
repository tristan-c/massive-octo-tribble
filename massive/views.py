from flask.ext.restful import Resource, reqparse
from massive import api, app
from massive.models import *
from bs4 import BeautifulSoup

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('str', type=list, default=[])

class getLinks(Resource):
    def get(self):
        links = Links.objects()
        return [link.dump() for link in links]

    def post(self):
        args = parser.parse_args()


api.add_resource(getLinks,'/links')#,'/trip/<string:ticketId>')


def handle(self, file):
    file_path = args[0]
    file = open(file_path, 'rb')

    soup = BeautifulSoup(file.read())
    user = User.objects.get(id=options['user_id'])
    for td in soup.find_all('dt')[::-1]:
        self.stdout.write(td.a.get('href'))
        link = Link()
        link.title = td.a.text
        link.url = td.a.get('href')
        link.added = datetime.datetime.fromtimestamp(int(td.a.get('add_date')))
        link.tags = td.a.get('tags').replace(',', ' ')
        link.user = user
        link.save()