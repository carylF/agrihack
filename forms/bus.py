import wtforms
from wtforms import validators


class BusForm(wtforms.Form):

  bus_id = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=10)])

  is_premium = wtforms.BooleanField(validators=[
      validators.Required()])  

  is_operational = wtforms.BooleanField(validators=[
      validators.Required()])

  def validate_bus_id(self, field):
      field.data = field.data.strip()