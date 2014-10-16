from mongoengine import *
from flask.ext.mongoengine import *

class Favicon(Document):
    image = ImageField(size=(16, 16, True), thumbnail_size=None, collection_name='favicon',required=True)

class Links(Document):
    tags = ListField(StringField()) 
    description = StringField()
    url = StringField()
    title = StringField()
    favicon = ReferenceField(Favicon)

    def dump(self):
        output = self.__dict__["_data"]
        if "id" in output:
            output['_id'] = str(output['id'])
            del output['id']
        if output['favicon']:
            output['favicon'] = True
            
        return output

