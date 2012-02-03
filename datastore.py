from google.appengine.ext import db

class Users(db.Model):
    legacy = db.StringProperty()
    username = db.StringProperty()
    session = db.StringProperty()
    done = db.BooleanProperty(default=False)

class Songs(db.Model):
    artist = db.StringProperty()
    name = db.StringProperty()

class Scrobbles(db.Model):
    user = db.ReferenceProperty(Users, collection_name='Users_Scrobbles')
    song = db.ReferenceProperty(Songs, collection_name='Songs_Scrobbles')
    date = db.DateTimeProperty()