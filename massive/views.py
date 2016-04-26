from flask.ext.restful import Resource, reqparse
from flask.ext.login import login_required
from flask import redirect, send_file, g

from massive import api, app
from massive.models import *
from massive.utils import *

from pony.orm import *

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
        with db_session:
            links = select(l for l in Links if l.user.id == g.user.id)
            return [link.dump() for link in links]

    def post(self, linkId=None):
        args = parser.parse_args()

        if linkId:
            with db_session:
                link = Links.get(id=linkId)
                if not link:
                    return 404

                taglist = [t.name for t in link.tags]
                for tag in args['tags']:
                    if tag not in taglist:
                        db_tag = Tags.get(name=tag)
                        if not db_tag:
                            db_tag = Tags(name=tag)
                        link.tags.add(db_tag)

                commit()

            return link.dump()

        url = args['url']

        #prepend if no protocole specified
        if url.find("http://") == -1 and url.find("https://") == -1:
            url = "http://%s" % url

        with db_session:
            if Links.get(url=url, user=g.user.get_id()):
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
        with db_session:
            link = Links.get(id=linkId)
            if not link:
                return 404

            link.delete()
            commit()
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

@db_session
def save_link(title, url, tags=[], favicon=None, user=None):
    
    db_tags = []
    for tag in tags:
        db_tag = Tags.get(name=tag)
        if not db_tag:
            db_tag = Tags(name=tag)
        db_tags.append(db_tag)

    if not title:
        title = url.split('/')[-1]

    link = Links(
        title=title,
        url=url,
        tags=db_tags,
        user=user.get_id()
    )

    # if favicon:
    #     link.favicon = favicon

    commit()

    return link
