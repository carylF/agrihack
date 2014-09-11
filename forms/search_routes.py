import wtforms
from wtforms import validators


class SearchRoutesForm(wtforms.Form):

  bus_number = wtforms.TextField(validators=[validators.Required()])
  location = wtforms.TextField(validators=[validators.Required()])
 
