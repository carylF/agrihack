from google.appengine.ext import db


class BusRoute(db.Model):
  EXCEPTION_NO_PARENT = "`parent` property must be an `Account` object."

  route_number = db.StringProperty(default=None)
  stops = db.StringProperty(default=[])

  def get_account(self):
    return self.parent()

  def stops_list(self):
    return self.stops.split(',')
    
  @classmethod
  def get_by_route_number(cls, route_number):
    return cls.all().filter('route_number =', route_number).get()

  def put(self, *args, **kwargs):
    # This is not at the top to prevent circular imports.
    from models.account import Account
    parent = self.parent()
    if not parent or not isinstance(parent, Account):
      raise ValueError(self.EXCEPTION_NO_PARENT)

    return super(BusRoute, self).put(*args, **kwargs)
