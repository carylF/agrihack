from forms.bus import BusForm
from forms.bus_time import BusTimeForm
from forms.assign_driver import AssignDriverForm
from handlers import base
from library import messages
from library.auth import role_required
from models.bus import Bus
from models.bus_driver import BusDriver


class BusHandler(base.BaseHandler):

  @role_required(is_manager=True)
  def create(self): 
    form = BusForm(self.request.POST)

    if self.request.method == 'POST' and form.validate():

      if Bus.get_by_bus_id(form.data['bus_id']):
        self.session.add_flash(messages.BUS_EXISTS,
                               level='error')
        return self.render_to_response('bus/form.haml', {'form': form})

      bus = Bus(bus_id=form.data['bus_id'],
                is_premium=form.data['is_premium'],
                is_operational=form.data['is_operational'],
                parent=self.get_current_account())
      bus.put()

      self.session.add_flash(messages.BUS_CREATE_SUCCESS, level='info')
      return self.redirect_to('bus.list')

    self.session.add_flash(messages.BUS_CREATE_ERROR, level='error')
    return self.redirect_to('bus.list')

  @role_required(is_manager=True)
  def delete(self, id):
    bus = Bus.get_by_id(int(id), parent=self.get_current_account())

    if not bus:
      self.session.add_flash(messages.BUS_NOT_FOUND, level='error')
      return self.redirect_to('bus.list')

    bus.delete()
    self.session.add_flash(messages.BUS_DELETE_SUCCESS)

    return self.redirect_to('bus.list')

  def list(self):
    # We pass form so we can generate it with the modal using macros.
    return self.render_to_response('bus/list.haml', {'form': BusForm()})

  @role_required(is_manager=True, is_editor=True)
  def update_times(self, id):
    bus = Bus.get_by_id(int(id), parent=self.get_current_account())

    if not bus:
      return self.redirect_to('bus.list', messages.BUS_NOT_FOUND)

    form = BusTimeForm(self.request.POST, obj=bus)

    if self.request.method == 'POST' and form.validate():
      form.populate_obj(bus)
      bus.put()

      self.session.add_flash(messages.BUS_Times_SUCCESS)
      return self.redirect_to('bus.list')

    return self.render_to_response('bus/form.haml', {'form': form})
  

  @role_required(is_manager=True, is_editor=True)
  def assign_driver(self, id):
    bus = Bus.get_by_id(int(id), parent=self.get_current_account())

    if not bus:
      return self.redirect_to('bus.list', messages.BUS_NOT_FOUND)

    form = AssignDriverForm(self.request.POST, obj=bus)

    if self.request.method == 'POST' and form.validate():
      busDriver = BusDriver.get_by_driver_id(form.data['driver_id'])
      bus.bus_driver = busDriver.key()
      bus.put()

      self.session.add_flash(messages.BUS_DRIVER_ASSIGN_SUCCESS)
      return self.redirect_to('bus.list')
    # Unable to flash ASS_DRIVER_ERROR because request returns 302.
    # Form may not be validating correctly in the above, hence the
    # the form call below is the one that actually renders the
    # correct form.
    return self.render_to_response('bus/form.haml', {'form': form})


  @role_required(is_manager=True, is_editor=True)
  def update(self, id):
    bus = Bus.get_by_id(int(id), parent=self.get_current_account())

    if not bus:
      return self.redirect_to('bus.list', messages.BUS_NOT_FOUND)

    form = BusForm(self.request.POST, obj=bus)

    if self.request.method == 'POST' and form.validate():
      form.populate_obj(bus)
      bus.put()

      self.session.add_flash(messages.BUS_UPDATE_SUCCESS)
      return self.redirect_to('bus.list')

    return self.render_to_response('bus/form.haml', {'form': form})