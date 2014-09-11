from forms.bus_driver import BusDriverForm
from handlers import base
from library import messages
from library.auth import role_required
from models.bus_driver import BusDriver


class BusDriverHandler(base.BaseHandler):

  @role_required(is_manager=True)
  def create(self): 
    form = BusDriverForm(self.request.POST)

    if self.request.method == 'POST' and form.validate():

      if BusDriver.get_by_driver_id(form.data['driver_id']):
        self.session.add_flash(messages.BUS_DRIVER_EXISTS,
                               level='error')
        return self.render_to_response('bus_driver/form.haml', {'form': form})

      bus_driver = BusDriver(driver_id=form.data['driver_id'],
                             parent=self.get_current_account())

      bus_driver.name = ' '.join((form.data['first_name'],
                                  form.data['last_name']))
      bus_driver.put()

      self.session.add_flash(messages.BUS_DRIVER_CREATE_SUCCESS, level='info')
      return self.redirect_to('bus_driver.list')

    self.session.add_flash(messages.BUS_DRIVER_CREATE_ERROR, level='error')
    return self.redirect_to('bus_driver.list')

  @role_required(is_manager=True)
  def delete(self, id):
    bus_driver = BusDriver.get_by_id(int(id), parent=self.get_current_account())

    if not bus_driver:
      self.session.add_flash(messages.BUS_DRIVER_NOT_FOUND, level='error')
      return self.redirect_to('bus_driver.list')

    bus_driver.delete()
    self.session.add_flash(messages.BUS_DRIVER_DELETE_SUCCESS)

    return self.redirect_to('bus_driver.list')

  @role_required(is_manager=True, is_editor=True)
  def update(self, id):
    bus_driver = BusDriver.get_by_id(int(id), parent=self.get_current_account())

    if not bus_driver:
      return self.redirect_to('bus_driver.list', messages.BUS_DRIVER_NOT_FOUND)

    form = BusDriverForm(self.request.POST, obj=bus_driver)

    if self.request.method == 'POST' and form.validate():
      form.populate_obj(bus_driver)
      bus_driver.name = ' '.join((form.data['first_name'],
                                  form.data['last_name']))
      bus_driver.put()

      self.session.add_flash(messages.BUS_DRIVER_UPDATE_SUCCESS)
      return self.redirect_to('bus_driver.list')

    return self.render_to_response('drivers/form.haml', {'form': form})

  def list(self):
    # We pass form so we can generate it with the modal using macros.
    return self.render_to_response('drivers/list.haml', {'form': BusDriverForm()})
