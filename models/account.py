from datetime import datetime

from google.appengine.ext import db
import pytz

from models.profile import Profile


class Account(db.Model):
  DEFAULT_TIMEZONE = 'America/Jamaica'

  name = db.StringProperty()
  email = db.EmailProperty()
  timezone = db.StringProperty()
  activated = db.BooleanProperty(default=False)
  activation_key = db.StringProperty()

  # Administrative details
  created = db.DateProperty(auto_now_add=True)

  def get_profiles(self):
    return Profile.all().ancestor(self)

  def get_employees(self):
    return self.get_profiles().filter(
        'is_editor =', False).filter('is_manager = ', False)

  def get_BusRoutes(self):
    # This is not at the top to prevent circular imports.
    from models.bus_route import BusRoute
    return BusRoute.all().ancestor(self)

  def get_Bus(self):
    # This is not at the top to prevent circular imports.
    from models.bus import Bus
    return Bus.all().ancestor(self)

  def get_BusDriver(self):
    # This is not at the top to prevent circular imports.
    from models.bus_driver import BusDriver
    return BusDriver.all().ancestor(self) 

  def get_timezone(self):
    return pytz.timezone(self.timezone or self.DEFAULT_TIMEZONE)

  def get_current_time(self):
    utc_now = pytz.utc.localize(datetime.utcnow())
    return utc_now.astimezone(self.get_timezone())
