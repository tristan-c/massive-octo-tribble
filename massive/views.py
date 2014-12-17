from flask.ext.restful import Resource, reqparse
from flask import redirect, send_file
from massive import api, app
from massive.models import *
from massive.utils import *

@app.route('/')
def index():
    return redirect("/index.html")

parser = reqparse.RequestParser()
parser.add_argument('url', type=str)
parser.add_argument('tags', type=list, default=[])

class links(Resource):
    def get(self):
        links = Links.objects()
        return [link.dump() for link in links]

    def post(self,linkId=None):
        args = parser.parse_args()

        if linkId:
            link = Links.objects.get_or_404(id =linkId)
            for tag in args['tags']:
                if tag not in link.tags:
                    link.tags.append(tag)
            link.save()
            return link.dump()

        if len(Links.objects(url=args['url'])) != 0:
            return "already in db", 400

        link = saveLink(
            getPageTitle(args['url']),
            args['url'],
            args['tags'],
            getPageFavicon(args['url'])
        )
        return link.dump()


api.add_resource(links,'/links','/links/<string:linkId>')

@app.route('/ico/<icoId>')
def getAvatar(icoId=None):
    if not icoId:
        return "not found",404

    link = Links.objects.get(id=icoId)
    if link.favicon:
        image = link.favicon.image.get()
        return send_file(image)
    else:
        return "no favicon",404


def saveLink(title,url,tags=[],favicon=None):
    link = Links(
        title = title,
        url = url,
        tags = tags,
    )
    if favicon:
        link.favicon = favicon

    link.save()

    return link