from google.appengine.ext import db


class BusDriver(db.Model):
  name = db.StringProperty(default=None)
  email = db.EmailProperty(default=None)
  driver_id = db.StringProperty(default=None)
  is_premium_driver = db.BooleanProperty(default=False)
  is_on_duty = db.BooleanProperty(default=False)


  @classmethod
  def get_by_driver_id(cls, driver_id):
    return cls.all().filter('driver_id =', driver_id).get()