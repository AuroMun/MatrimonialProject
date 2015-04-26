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
    form=auth()
    """
    if request.args(0)=='login':
        if form.process().accepted:
            redirect(URL('search'))
    """
    return dict(form=form)

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

def view_user():
    user = db(db.auth_user.last_name == request.args[0]).select()
    return dict(user = user)

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
