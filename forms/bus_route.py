import wtforms
from wtforms import validators


class BusRouteForm(wtforms.Form):

  route_number = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=5)])

  stops = wtforms.TextAreaField(validators=[
      validators.Length(max=1000)])

  def validate_route_number(self, field):
      field.data = field.data.strip()

  def validate_stops(self, field):
      field.data = field.data.strip()
