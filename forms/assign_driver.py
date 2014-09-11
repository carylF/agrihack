import wtforms
from wtforms import validators
from models.bus_driver import BusDriver
from models.bus import Bus


class AssignDriverForm(wtforms.Form):

  driver_id = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=10)])

  def validate_driver_id(self, field):
      field.data = field.data.strip()