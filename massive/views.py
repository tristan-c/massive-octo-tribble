from flask.ext.restful import Resource, reqparse
from flask.ext.login import login_required
from flask import redirect, send_file, g

from massive import api, app
from massive.models import *
from massive.utils import *


class Resource(Resource):
    method_decorators = [login_required]


@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated():
        return redirect("/index.html")
    else:
        return redirect("/login")

parser = reqparse.RequestParser()
parser.add_argument('url', type=str)
parser.add_argument('tags', type=list, default=[])


class links(Resource):

    def get(self):
        links = Links.objects(user=g.user.get_id())
        return [link.dump() for link in links]

    def post(self, linkId=None):
        args = parser.parse_args()

        if linkId:
            link = Links.objects.get_or_404(id=linkId)
            for tag in args['tags']:
                if tag not in link.tags:
                    link.tags.append(tag)
            link.save()
            return link.dump()

        url = args['url']

        if url.find("http://") == -1 and url.find("https://") == -1:
            url = "http://%s" % url

        if len(Links.objects(url=url, user=g.user.get_id())) != 0:
            return "already in db", 400

        link = save_link(
            get_page_title(url),
            url,
            args['tags'],
            get_page_favicon(url),
            g.user
        )
        return link.dump()

    def delete(self, linkId=None):
        link = Links.objects.get_or_404(id=linkId)
        link.delete()
        return ""


api.add_resource(links, '/links', '/links/<string:linkId>')


@app.route('/ico/<icoId>')
def get_avatar(icoId=None):
    if not icoId:
        return "not found", 404

    link = Links.objects.get(id=icoId)
    if link.favicon:
        image = link.favicon.image.get()
        return send_file(image)
    else:
        return "no favicon", 404


def save_link(title, url, tags=[], favicon=None, user=None):
    link = Links(
        title=title,
        url=url,
        tags=tags,
        user=user.get_id()
    )

    if favicon:
        link.favicon = favicon

    link.save()

    return link
