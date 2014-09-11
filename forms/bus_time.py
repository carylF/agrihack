import wtforms
from wtforms import validators
from models.bus import Bus


class BusTimeForm(wtforms.Form):

  arrival_time = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=10)])

  departure_time = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=10)])

  def validate_arrival_time(self, field):
      field.data = field.data.strip()

  def validate_departure_time(self, field):
      field.data = field.data.strip()