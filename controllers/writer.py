import time
from google.appengine.ext import db
from gaemvc.methods import controller
from models import Writer, Entry
writer = controller("writer")

@writer.view()
def index(handler):
    context = {}
    if handler.session.get('account',False):
        context['drafts'] = Entry.all().filter('author =', db.Key(handler.session['account']))
    else:
        pass
    return context

@writer.view(routes=[r'/(?P<key>[a-zA-Z0-9\-_]+)/$'])
def draft(handler, route, params):
    if route.get("key",False):
        draft = Entry.get_by_key_name(route.get("key"))
        if draft and str(draft._author) == handler.session.get('account',False):
            return { "draft": draft }
    return { "draft": { 'title': 'untitled', 'content': '', 'saved': 'never' } }

@writer.view(routes=[r'/(?P<key>[a-zA-Z0-9\-_]+)/$'])
def article(handler, route, params):
    if route.get("key",False):
        draft = Entry.get_by_key_name(route.get("key"))
        return { 'article': draft }
    return { "__redirect_to": "/writer/" }

@writer.view(redirect_to="/writer/draft/")
def new_account(handler, route, params):
    username = params.get('nickname',None)
    password = params.get('password',None)
    if Writer.get_by_key_name(username):
        raise Exception("I don't think so")
    if not username or not password:
        raise Exception("Invalid request")
    account = Writer.get_or_insert(username,nickname=username,password=password)
    handler.session['account'] = str(account.key())
    return {}

@writer.view(redirect_to="/writer/")
def load_account(handler, route, params):
    if params.get("confirm",False):
        return {}
    return {}

@writer.json()
def autosave(handler, route, params):
    title = params.get("title","")
    content = params.get("content","")
    key   = params.get("key",None)
    user  = handler.session.get('account',False)
    if not title or not content:
        return { 'saved': False }
    if not user:
        return { 'account': False, 'saved': False }
    if key:
        draft = Entry.get_by_key_name(key)
        if str(draft._author) != user:
            raise Exception("You are not this article's author")
    else:
        key   = str(time.time()).replace('.','')
        draft = Entry(key_name=key,author=db.Key(user))
    draft.title   = title
    draft.content = content
    draft.put()
    return { 'saved': key, 'time': draft.isodate }

@writer.json()
def doesuserexist(handler, route, params):
    return { 'exists': Writer.get_by_key_name(params.get('nickname',None)) and True or False }
