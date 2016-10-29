import uuid
import os

from flask_restful import Resource, reqparse
from flask_login import login_required
from flask import redirect, send_file, g, url_for

from massive import api, app
from massive.models import *
from massive.utils import *

from io import BytesIO

class Resource(Resource):
    method_decorators = [login_required]

@app.route('/')
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect('/index.html')
    else:
        return redirect("/login")

parser = reqparse.RequestParser()
parser.add_argument('url', type=str)
parser.add_argument('tags', type=str, default=None)


class links(Resource):
    def get(self):
        user = User.query.get(g.user.id)
        links = Link.query.join(User).filter(User.email == user.email)
        return [link.dump() for link in links]

    def post(self, linkId=None):
        args = parser.parse_args()
        user = User.query.get(g.user.id)

        if linkId:
            link = Link.query.get(id=linkId)
            if not link:
                return "no link found", 404

            #taglist = [t.name for t in link.tags]
            # for tag in args['tags']:
            #     if tag not in taglist:
            #         db_tag = Tags.get(name=tag)
            #         if not db_tag:
            #             db_tag = Tags(name=tag)
            #         link.tags.add(db_tag)

            return link.dump()

        url = args['url']
        tags = args['tags']

        #prepend if no protocole specified
        if url.find("http://") == -1 and url.find("https://") == -1:
            url = "http://%s" % url

        if Link.query.filter_by(url=url, user_id=user.id).first():
            return "already in db", 400 

        if tags:
            tags = tags.split(",")

        link = save_link(
            get_page_title(url),
            url,
            tags,
            user
        )

        return link.dump()

    def delete(self, linkId=None):
        if linkId == None:
            return "no link provided", 400

        link = Link.query.get(linkId)
        if not link:
            return "no link found", 404

        #delete favicon
        if link.favicon:
            favicon_path = os.path.join(app.config['FAVICON_REPO'],link.favicon)
            try:
                os.remove(favicon_path)
            except Exception as e:
                app.logger.warning("error while trying to remove a favicon")
                app.logger.warning(e)

        db.session.delete(link)
        db.session.commit()
        return ""


api.add_resource(links, '/links', '/links/<string:linkId>')


@app.route('/ico/<icoId>')
def get_avatar(icoId=None):
    file_path = os.path.join(app.config['FAVICON_REPO'],icoId)

    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "no favicon found",404


def save_link(title, url, tags=[], user=None):
    if not title:
        title = url.split('/')[-1]

    iconfile_name = "%s.ico" % str(uuid.uuid4())
    favicon = get_page_favicon(url,iconfile_name)

    link = Link(
        title=title,
        url=url,
        favicon=iconfile_name,
        #tags=db_tags,
        user=user
    )

    for tag in tags:
        db_tag = Tags.query.filter_by(name=tag).first()
        if not db_tag:
            db_tag = Tags(name=tag)
            db.session.add(db_tag)
        link.tags.append(db_tag)
    
    if favicon:
        link.favicon = favicon

    db.session.add(link)
    db.session.commit()

    return link
