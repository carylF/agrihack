from google.appengine.ext import db
from models.bus_route import BusRoute
from models.bus_driver import BusDriver


class Bus(db.Model):
  bus_id = db.StringProperty(default=None)
  # Defines bus's operational state.
  is_operational = db.BooleanProperty(default=False)
  # Shows whether bus is a premium, hence has altered route, etc.
  is_premium = db.BooleanProperty(default=False)
  arrival_time = db.StringProperty(default=None)
  departure_time = db.StringProperty(default=None)
  # Rework driver-bus references.
  bus_driver = db.ReferenceProperty(BusDriver, collection_name='bus_driver')
  route = db.ReferenceProperty(BusRoute)
  

  @classmethod
  def get_by_bus_id(cls, bus_id):
    return cls.all().filter('bus_id =', bus_id).get()