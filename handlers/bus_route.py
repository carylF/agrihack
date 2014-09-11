from forms.bus_route import BusRouteForm
from handlers import base
from library import messages
from library.auth import role_required
from models.bus_route import BusRoute


class BusRouteHandler(base.BaseHandler):

  @role_required(is_manager=True)
  def create(self): 
    form = BusRouteForm(self.request.POST)

    if self.request.method == 'POST' and form.validate():

      if BusRoute.get_by_route_number(form.data['route_number']):
        self.session.add_flash(messages.BUS_ROUTE_NAME_EXISTS,
                               level='error')
        return self.render_to_response('bus_route/form.haml', {'form': form})

      busRoute = BusRoute(route_number=form.data['route_number'],
                          stops=form.data['stops'],
                          parent=self.get_current_account())
      busRoute.put()

      self.session.add_flash(messages.BUS_ROUTE_CREATE_SUCCESS, level='info')
      return self.redirect_to('bus_route.list')

    self.session.add_flash(messages.BUS_ROUTE_CREATE_ERROR, level='error')
    return self.redirect_to('bus_route.list')

  @role_required(is_manager=True)
  def delete(self, id):
    busRoute = BusRoute.get_by_id(int(id), parent=self.get_current_account())

    if not busRoute:
      self.session.add_flash(messages.BUS_ROUTE_NOT_FOUND, level='error')
      return self.redirect_to('bus_route.list')

    busRoute.delete()
    self.session.add_flash(messages.BUS_ROUTE_DELETE_SUCCESS)

    return self.redirect_to('bus_route.list')

  def list(self):
    # We pass form so we can generate it with the modal using macros.
    return self.render_to_response('bus_route/list.haml', {'form': BusRouteForm()})

 
  @role_required(is_manager=True, is_editor=True)
  def update(self, id):
    busRoute = BusRoute.get_by_id(int(id), parent=self.get_current_account())

    if not busRoute:
      self.session.add_flash(messages.BUS_ROUTE_NOT_FOUND,
                             level='error')
      return self.redirect_to('bus_route.list')

    form = BusRouteForm(self.request.POST, obj=busRoute)

    if self.request.method == 'POST' and form.validate():
      form.populate_obj(busRoute)
      busRoute.put()

      self.session.add_flash(messages.BUS_ROUTE_UPDATE_SUCCESS)
      return self.redirect_to('bus_route.list')

    return self.render_to_response('bus_route/form.haml', {'form': form})
