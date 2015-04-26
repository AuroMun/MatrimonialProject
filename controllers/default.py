# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    """
    response.flash = T("Welcome to web2py!")
    form = SQLFORM(db.users)
    if form.process().accepted:
        response.flash("Registered!")
    return dict(message=T('Hello World'), form=form)
    """
    """
    if request.args(0)=='login':
        if form.process().accepted:
            redirect(URL('search'))
    """
    if auth.user: redirect(URL('user/profile'))
    return dict(form=auth())

@auth.requires_login()
def search():
    form = crud.create(db.find)
    if(form.process().accepted):
        redirect(URL('default','result',vars=form.vars))
    return dict(form=form)

@auth.requires_login()
def result():
    q1 = db.auth_user.sex==request.vars.sex
    amin = db.auth_user.age > request.vars.minimum_age
    amax = db.auth_user.age < request.vars.maximum_age
    sal = db.auth_user.salary > request.vars.minimum_salary
    rows=db(q1 & amin & amax & sal).select(db.auth_user.first_name, db.auth_user.last_name, db.auth_user.age, db.auth_user.salary)
    return dict(rows=rows)
    #return dict(sex=request.vars.sex)
    
def view_users():
    dic = db(db.auth_user).select()
    return dict(dic = dic)

@auth.requires_login()
def view_user():
    user = db(db.auth_user.last_name == request.args[0]).select()
    return dict(user = user)

def message():
    db.messages.me.default=auth.user.last_name
    db.messages.dest.default=request.args[0]
    db.messages.sent_on.default=request.now
    form=crud.create(db.messages)
    q1=db.messages.me==auth.user.last_name
    q2=db.messages.dest==request.args[0]
    q3=db.messages.me==request.args[0]
    q4=db.messages.dest==auth.user.last_name
    prev=db(q1&q2 | q3&q4).select(orderby=db.messages.sent_on,limitby=(0,10))
    return locals()

@auth.requires_login()
def inbox():
    q1=db.messages.dest==auth.user.last_name
    one=db(q1).select(db.messages.me,distinct=True,orderby=db.messages.sent_on)
    return locals()

@auth.requires_login()
def outbox():
    q1=db.messages.me==auth.user.last_name
    one=db(q1).select(db.messages.dest,distinct=True,orderby=db.messages.sent_on)
    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def register():
    form = SQLFORM(db.users);
    return dict(form = form)

@auth.requires_login()
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
