import wtforms
from wtforms import validators


class BusDriverForm(wtforms.Form):

    first_name = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=12)])

    last_name = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=15)])

    driver_id = wtforms.StringField(validators=[
      validators.Required(),
      validators.Length(max=10)])

    def validate_first_name(self, field):
      field.data = field.data.strip()

    def validate_last_name(self, field):
      field.data = field.data.strip()

    def validate_driver_id(self, field):
      field.data = field.data.strip()