from datetime import datetime
import uuid

from google.appengine.ext import db
import pytz
from webapp2_extras import auth


class Profile(db.Model):
  default_TIMEZONE = 'America/Jamaica'
  EXCEPTION_NO_PARENT = "`parent` property must be an `Account` object."

  # Tie back to webapp2 auth
  auth_user_id = db.IntegerProperty()

  # Administrative details
  created = db.DateProperty(auto_now_add=True)
  is_admin = db.BooleanProperty(default=False)
  is_manager = db.BooleanProperty(default=False)
  is_editor = db.BooleanProperty(default=False)
  beta_tester = db.BooleanProperty(default=False)

  # Basic details
  name = db.StringProperty()
  email = db.EmailProperty()
  timezone = db.StringProperty()
  activated = db.BooleanProperty(default=False)
  activation_key = db.StringProperty()

  @classmethod
  def get_by_email(cls, email):
    return cls.all().filter('email =', email).get()

  @classmethod
  def get_by_activation_key(cls, activation_key):
    return cls.all().filter('activation_key =', activation_key).get()

  @classmethod
  def get_by_auth_user_id(cls, id):
    return cls.all().filter('auth_user_id =', id).get()

  @classmethod
  def get_by_access_code(cls, access_code):
    from models.access_code import AccessCode
    code = AccessCode.all().filter('access_code =', access_code).get()
    if code:
      return code.profile

  def get_account(self):
    return self.parent()

  def get_auth_user(self):
    return auth.get_auth().store.user_model.get_by_id(self.auth_user_id)

  def get_current_time(self):
    utc_now = pytz.utc.localize(datetime.utcnow())
    return utc_now.astimezone(self.get_timezone())

  def get_enrollments(self):
    # Used to prevent ciruclar dependencies.
    from models.enrollment import Enrollment
    return Enrollment.all().filter('profile = ', self)

  def get_timezone(self):
    return pytz.timezone(self.timezone or self.default_TIMEZONE)

  def is_editable_by(self, profile):
    same_account = self.get_account().key() == profile.get_account().key()
    can_edit = (profile.is_admin or profile.is_manager
                or profile.key() == self.key())

    return same_account and can_edit

  def is_enrolled_in(self, BUS_ROUTE):
    return bool(self.get_enrollments().filter('BUS_ROUTE =', BUS_ROUTE).get())

  def put(self, *args, **kwargs):
    # This is not at the top to prevent circular imports.
    from models.account import Account
    parent = self.parent()
    if not parent or not isinstance(parent, Account):
      raise ValueError(self.EXCEPTION_NO_PARENT)

    if not self.activation_key:
      self.activation_key = str(uuid.uuid4())
    return super(Profile, self).put(*args, **kwargs)
