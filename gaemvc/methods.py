import re, os
# from appengine
import jinja2
from webapp2_extras import json
from google.appengine.api import users
# from application
import views

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader( os.path.dirname(views.__file__) ), trim_blocks=True, line_statement_prefix="#", line_comment_prefix="##")

def setup_environment():
    global jinja_environment
    import bfunctions as templatetags
    fns = [fn for fn in dir(templatetags) if "__" not in fn]
    for fn in fns:
        jinja_environment.filters[fn] = getattr(templatetags,fn)

#setup_environment()

def View(admin_only=False,routes=[]):
    def view_wrap(fn):
        def tmpl(self):
            if admin_only or self.AdminOnly:
                user = users.get_current_user()
                if not user:
                    self.handler.redirect(users.create_login_url(this.request.uri))
                elif not users.is_current_user_admin():
                    self.handler.redirect('/%s/' % self.Area)
            # if routes defined, assign them to the controller
            if routes:
                self.route = {}
                for route in routes:
                    if re.search(route,self.request.path):
                        self.route = re.search(route,self.request.path).groupdict()
            gets   = self.request
            kwargs = {}
            args   = gets.arguments()
            # create a CGI dictionary
            [kwargs.update({str(k):gets.get(k)}) for k in args]
            
            view_data = {}
            try:
                view_data     = fn(self,**kwargs)
            except Exception,ex:
                view_data     = fn(self)
            
            view_data.update({"request":self.request})
            view_data.update({"version":os.environ["CURRENT_VERSION_ID"]})
            view_data.update({"development_environment":os.environ['SERVER_SOFTWARE'].startswith('Dev')})
            view_data.update({"session":self.session})
            
            # apply custom master page if assigned
            view_data.update({ "page_theme":self.Theme or "shared/_master.html" })
            
            _template    = self.Template if self.Template else fn.__name__ + '.html'
            tmpl_path = "%(area)s/%(file)s" % {"area":self.Area,"file":_template}
            
            compiled = jinja_environment.get_template(tmpl_path)
            
            return compiled.render( view_data )
        tmpl.__name__ = fn.__name__
        return tmpl
    return view_wrap

def Action(redirect=None,responseType="text",area=None,tmpl=None):
    def action_wrap(fn):
        def action(self):
            gets = self.request
            kwargs = {}
            args   = gets.arguments()
            Area = area if area else self.Area
            # create a CGI dictionary
            [kwargs.update({str(k):gets.get(k)}) for k in args]
            
            view_data = fn(self,**kwargs)
            if not redirect: #return values
                if responseType == "json":
                    self.response.headers["Content-Type"] = "application/json"
                    return json.encode( view_data )
                elif responseType == "template" and tmpl is not None:
                    view_data.update({"Routes":self.routes})
                    TemplatePath = "%(area)s/%(file)s.html" % {"area":Area,"file":tmpl}
                    compiled     = jinja_environment.get_template(TemplatePath)
                    return compiled.render( view_data )
                return view_data
            else: #redirect
                self.handler.redirect(redirect)
        action.__name__ = fn.__name__
        return action
    return action_wrap
