from mongoengine import *
from flask.ext.mongoengine import *


class Users(Document):
    id = StringField()
    password = StringField()
    login = StringField()

    def get_id(self):
        return str(self.id)

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def is_authenticated(self):
        return True


class Favicon(Document):
    image = ImageField(
        size=(
            16,
            16,
            True),
        thumbnail_size=None,
        collection_name='favicon',
        required=True)


class Links(Document):
    tags = ListField(StringField())
    description = StringField()
    url = StringField()
    title = StringField()
    favicon = ReferenceField(Favicon)
    user = ReferenceField(Users)

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
