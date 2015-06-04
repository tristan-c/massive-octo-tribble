from massive import db
from pony.orm import *

class Users(db.Entity):
    password = Required(str)
    login = Required(str,unique=True)
    links = Set("Links", cascade_delete=True)

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


# class Favicon(db.Entity):
#     image = ImageField(
#         size=(
#             16,
#             16,
#             True),
#         thumbnail_size=None,
#         collection_name='favicon',
#         required=True)

class Tags(db.Entity):
    name = Required(str)
    links = Set("Links")

class Links(db.Entity):
    description = Optional(str)
    url = Optional(str)
    title = Optional(str)
    #favicon = ReferenceField(Favicon)
    user = Required(Users)
    tags = Set(Tags)

    def dump(self):
        tags = [t.name for t in self.tags]

        return {
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "tags": tags
        }

    def __repr__(self):
        return '<Link %r>' % (self.url)

# class Favicon(db.Entity):
#     link = 

db.generate_mapping(create_tables=True)