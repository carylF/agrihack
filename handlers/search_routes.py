from handlers import base
from library.auth import login_not_required

class SearchRoutesHandler(base.BaseHandler):

  @login_not_required
  def search(self):
    return self.render_to_response('search_routes.haml', use_cache=True)