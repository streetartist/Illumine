# from flask import Flask,request,url_for,send_file
from fastapi import FastAPI
from flask import send_file

app = FastAPI()

import jinja2

import importlib

import sys
import os

is_pythonanywhere = False
theme = 'goodold'

if not is_pythonanywhere:
    path = os.path.abspath('.')
else:
    path = os.sep.join(['','home','streetartist'])

sys.path.append(os.sep.join([path, "plugins",'']))
sys.path.append(os.sep.join([path,"battery",""]))

import conf

# app = Flask(__name__)

import plugins.dispose

env = jinja2.Environment(loader=jinja2.FileSystemLoader(path))

def use_plugin(plugin,using,request=""):
    if using=="":
        return plugin.main()
    elif plugin.get_name() == using:
        return plugin.main(request)
    else:
        return plugin.main()

env.filters['use_plugin'] = use_plugin # 注册自定义过滤器


def url_to(theme,filename):
    return "/file/" + theme + '/' + filename

env.filters['url_to'] = url_to

# @app.route('/file/<theme>/<filename>')
@app.get('/file/{theme}/{filename}')
async def get_file(theme,filename):
    file_path = os.sep.join([path, "theme",theme ,filename])
    return send_file(file_path)

@app.get('/')
@app.get('/{using}')
@app.get('/{using}/{arg}/{plugin}')
@app.get('/{using}/{arg}')
async def getweb(using="",arg=None,plugin=None):
    # Battery Include
    for I in conf.setting:
        this = I(env=env,path='/'.join(["battery",conf.battery,""]))
        if using == this.name:
            if request.method=="POST":
                return this.main(request=request,arg=arg,plugin=plugin)
            else:
                return this.main(arg=arg,plugin=plugin)
    # Event Index_start
    the_plugins = plugins.dispose.Index_start()
    index_temp = env.get_template('/'.join(['theme',theme,'index.html']))

    return index_temp.render(plugins=the_plugins, request="",using=using)

@app.post('/')
@app.post('/{using}')
@app.post('/{using}/{arg}/{plugin}')
@app.post('/{using}/{arg}')
async def getweb(using="",arg=None,plugin=None):
    # Battery Include
    for I in conf.setting:
        this = I(env=env,path='/'.join(["battery",conf.battery,""]))
        if using == this.name:
            if request.method=="POST":
                return this.main(request=request,arg=arg,plugin=plugin)
            else:
                return this.main(arg=arg,plugin=plugin)
    # Event Index_start
    the_plugins = plugins.dispose.Index_start()
    index_temp = env.get_template('/'.join(['theme',theme,'index.html']))

    return index_temp.render(plugins=the_plugins, request="",using=using)


@app.get('/plugins/{name}')
async def the_plugins(name):
    plugin = importlib.import_module('plugins.'+name).Main()
    return plugin.main()

if __name__ == '__main__':
   app.run(debug=True)
