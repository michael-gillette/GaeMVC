import re, os, cgi
import functools
from collections import defaultdict
# from appengine
import jinja2
from webapp2_extras import json
from google.appengine.ext import blobstore
from google.appengine.api import users
# from application
import views

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader( os.path.dirname(views.__file__) ), trim_blocks=True)

def controller(area, pagetheme=None, adminonly=False):
    handlers = {}
    
    def container(): pass
    
    def http_decorator(routes=[], response_type="html", uploader=False, redirect_to=None, template=None, folder=None, admin_only=False, view_name=None):
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
                
                if uploader:
                    uploads = defaultdict(list)
                    for k,v in gae_handler.params.items():
                        if isinstance(v,cgi.FieldStorage) and 'blob-key' in v.type_options:
                            uploads[k].append( blobstore.parse_blob_info(v))
                
                fn_args = uploader and [uploads, gae_handler] or [gae_handler, route, params]
                
                try:
                    context = fn(gae_handler, route, params)
                except TypeError as te:
                    context = fn(gae_handler)
                
                tmpl     = template if template else context.get("__template",None)
                redirect = redirect_to or context.get("__redirect_to",None)
                
                if redirect:
                    return gae_handler.redirect(redirect)
                
                if response_type == "html":
                    tmpl_name = tmpl or fn.__name__ + ".html"
                    tmpl_path = "%s/%s" % (folder or area,tmpl_name)
                    tmpl_file = jinja_environment.get_template(tmpl_path)
                    
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
            handlers[view_name or fn.__name__] = handler
            return fn
        return http_handler
    
    http_json_short_hand = functools.partial(http_decorator, response_type="json")
    http_upload_decorator = functools.partial(http_decorator, uploader=True)
    http_admin_only = functools.partial(http_decorator, admin_only=True)
    
    container.all  = handlers
    container.area = area
    container.view = http_decorator
    container.uploader = http_upload_decorator
    container.json  = http_json_short_hand
    container.admin = http_admin_only
    return container
