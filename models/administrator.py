from google.appengine.ext import db


class Administrator(db.Model):
  # Basic information.
  name = db.TextProperty(default=None)
  email = db.EmailProperty(default=None)
  admin_key = db.IntegerProperty(default=None)
  admin_password = db.StringProperty(default=None)

  # Admin details.
  is_route_man = db.BooleanProperty(default=False)
  is_booking_man = db.BooleanProperty(default=False)
  is_floor_man = db.BooleanProperty(default=False)
  is_editor = db.BooleanProperty(default=False)
  is_sys_manager = db.BooleanProperty(default=False)


  def set_admin_key(self, admin_key):
  # hashed_password = webapp2_extras.security.generate_password_hash(password, method='sha1', length=22, pepper=None)
  # TODO: Randomly generate admin code and store copy of code in an admin file.
    return None

  def is_editable_by(sef):
    editor = (administrator.is_admin or administrator.is_sys_manager
              or administrator.key() == self.key())