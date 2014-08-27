from mongoengine import *
from flask.ext.mongoengine import *

class Favicon(Document):
    ImageField(size=(16, 16, True), thumbnail_size=None, collection_name='favicon',required=True)

class Links(Document):
    tags = ListField(StringField()) 
    description = StringField()
    url = StringField()
    #favicon = ReferenceField(User)

    def dump(self):
        return self.__dict__