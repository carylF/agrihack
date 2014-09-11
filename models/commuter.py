from google.appengine.ext import db

class Commuter(db.Model):
  name = db.TextProperty(default=None)
  email = db.EmailProperty(default=None)
  tel = db.IntegerProperty(default=None)
  is_member =db.Boolean(default=False)
  id_number = db.Boolean(default=None)