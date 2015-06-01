from massive import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256), index=True, unique=True)
    login = db.Column(db.String(64), index=True, unique=True)

    def get_id(self):
        return str(self.id)

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def __repr__(self):
        return '<User %r>' % (self.login)


# class Favicon(db.Model):
#     image = ImageField(
#         size=(
#             16,
#             16,
#             True),
#         thumbnail_size=None,
#         collection_name='favicon',
#         required=True)

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

tags_join = db.Table('tags_join',
    db.Column('tag_id', db.Integer, db.ForeignKey('Tags.id')),
    db.Column('link_id', db.Integer, db.ForeignKey('Links.id'))
)

class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(456), index=True, unique=True)
    url = db.Column(db.String(256), index=True, unique=True)
    title = db.Column(db.String(256), index=True, unique=True)
    #favicon = ReferenceField(Favicon)
    user = db.relationship('Users',
        backref=db.backref('links', lazy='dynamic'))

    tags = db.relationship('Links', 
                            primaryjoin=(tags_join.c.tag_id == id), 
                            secondaryjoin=(tags_join.c.link_id == id),
                            backref=db.backref('link', lazy='dynamic'), 
                            lazy='dynamic')

    def dump(self):
        output = self.__dict__["_data"]
        if "id" in output:
            output['_id'] = str(output['id'])
            del output['id']
        if output['favicon']:
            output['favicon'] = True
        try:
            del output['user']
        except:
            pass
        return output

    def __repr__(self):
        return '<Link %r>' % (self.url)

class Favicon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.relationship('Links',
        backref=db.backref('favicons', lazy='dynamic'))
