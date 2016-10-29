from flask_security import UserMixin, RoleMixin

from massive import db

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

relationship_table=db.Table('relationship_table',                            
                             db.Column('link_id', db.Integer,db.ForeignKey('link.id'), nullable=False),
                             db.Column('tags_id',db.Integer,db.ForeignKey('tags.id'),nullable=False),
                             db.PrimaryKeyConstraint('link_id', 'tags_id') )
 

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
    links = db.relationship('Link', backref='user', lazy='dynamic')



    def __repr__(self):
        return '<User %r>' % (self.email)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255))
    url = db.Column(db.String(140))
    title = db.Column(db.String(140))
    favicon = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags=db.relationship('Tags', secondary=relationship_table, backref='links' )

    def dump(self):
        tags = [t.name for t in self.tags]

        return {
            "_id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "tags": tags,
            "favicon": self.favicon
        }

    def __repr__(self):
        return '<Link %r>' % (self.url)

class Tags(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))


