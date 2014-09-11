from webapp2_extras.routes import RedirectRoute

from handlers.home import HomeHandler
from handlers.login import LoginHandler
from handlers.profile import ProfileHandler
from handlers.signup import SignupHandler
from handlers.static import PublicStaticHandler
from handlers.search_routes import SearchRoutesHandler
from handlers.contact import ContactHandler
# from handlers.bus import BusHandler
# from handlers.bus_route import BusRouteHandler
# from handlers.bus_driver import BusDriverHandler


__all__ = ['application_routes']

application_routes = []

_route_info = [

    # Public handlers.
    ('contact', None, '/contact/', ContactHandler, 'contact'),
    ('home', 'GET', '/', HomeHandler, 'home'),
    ('signup', None, '/signup/', SignupHandler, 'signup'),
    ('search',None, '/search/' ,SearchRoutesHandler, 'search'),

    # Authentication-related handlers.
    ('login', None, '/login/', LoginHandler, 'login'),
    ('logout', 'GET', '/logout/', LoginHandler, 'logout'),
    ('forgot-password', None, '/forgot-password/',
        LoginHandler, 'forgot_password'),

    ('profile.activate', None, '/profile/activate/',
        ProfileHandler, 'activate'),
    ('profile.view', None, '/profile/', ProfileHandler, 'view'),

    # ('bus.create', None, '/bus/create/', BusHandler, 'create'),
    # ('bus.delete', None, '/bus/<id:\d+>/delete/',
    #     BusHandler, 'delete'), 
    # ('bus.update_times', None, '/bus/<id:\d+>/update_times/',
    #     BusHandler, 'update_times'), 
    # ('bus.assign_driver', None, '/bus/<id:\d+>/assign_driver/',
    #     BusHandler, 'assign_driver'),
    # ('bus.list', None, '/bus/', BusHandler, 'list'),
    # ('bus.update', None, '/bus/<id:\d+>/update/',
    #     BusHandler, 'update'),

    # ('bus_route.create', None, '/bus_route/create/', BusRouteHandler, 'create'),
    # ('bus_route.delete', None, '/bus_route/<id:\d+>/delete/',
    #     BusRouteHandler, 'delete'),    
    # ('bus_route.list', None, '/bus_route/', BusRouteHandler, 'list'),
    # ('bus_route.update', None, '/bus_route/<id:\d+>/update/',
    #     BusRouteHandler, 'update'),

    # ('bus_driver.create', None, '/bus_driver/create/', BusDriverHandler, 'create'),
    # ('bus_driver.delete', None, '/bus_driver/<id:\d+>/delete/',
    #     BusDriverHandler, 'delete'),
    # ('bus_driver.list', None, '/bus_driver/', BusDriverHandler, 'list'),
    # ('bus_driver.update', None, '/bus_driver/<id:\d+>/update/',
    #     BusDriverHandler, 'update'),
]

for name, methods, pattern, handler_cls, handler_method in _route_info:
  # Allow a single string, but this has to be changed to a list.
  if isinstance(methods, basestring):
    methods = [methods]

  # Create the route.
  route = RedirectRoute(name=name, template=pattern, methods=methods,
                        handler=handler_cls, handler_method=handler_method)

  # Add the route to the proper public list.
  application_routes.append(route)
