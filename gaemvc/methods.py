import re, os
# from appengine
import jinja2
from webapp2_extras import json
from google.appengine.api import users
# from application
import views

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader( os.path.dirname(views.__file__) ), trim_blocks=True, line_statement_prefix="#", line_comment_prefix="##")

def controller(area, pagetheme=None, adminonly=False):
    handlers = {}
    
    def container(): pass
    
    def http_decorator(routes=[], response_type="html", redirect_to=None, template=None, folder=None, admin_only=False):
        def http_handler(fn):
            def handler(gae_handler):
                # prepare
                request  = gae_handler.request
                response = gae_handler.response
                route = {}
                params   = dict(gae_handler.request.params)
                
                if adminonly or admin_only:
                    user = users.get_current_user()
                    if not user:
                        url = users.create_login_url(request.uri)
                    elif not users.is_current_user_admin():
                        url = '/%s/' % area
                    gae_handler.redirect(url)
                
                if routes:
                    for r in routes:
                        if re.search(r, request.path):
                            route = re.search(r, request.path).groupdict()
                
                try:
                    context = fn(gae_handler, params, route)
                except TypeError as te:
                    context = fn(gae_handler)
                
                if redirect_to:
                    return gae_handler.redirect(redirect_to)
                
                tmpl_name = template or fn.__name__ + ".html"
                tmpl_path = "%s/%s" % (folder or area,tmpl_name)
                tmpl_file = jinja_environment.get_template(tmpl_path)
                
                if response_type == "html":
                    context.update({
                        'request'     : request,
                        'app_version' : os.environ["CURRENT_VERSION_ID"],
                        'is_dev_env'  : os.environ["SERVER_SOFTWARE"].startswith("Dev"),
                        'session'     : gae_handler.session,
                        'page_theme'  : pagetheme or "shared/_master.html",
                    })
                    return tmpl_file.render( context )
                elif response_type == "json":
                    response.headers["Content-Type"] = "application/json"
                    return json.encode( context )
            handler.__name__ = fn.__name__
            handlers[fn.__name__] = handler
            return fn
        return http_handler
    container.all  = handlers
    container.area = area
    container.view = http_decorator
    return container
