from flask import Flask,request
import jinja2

import importlib

import sys
#import conf

theme = 'goodold'
path = '/home/streetartist'

sys.path.append(path+"/plugins/")

app = Flask(__name__)

import plugins.dispose

env = jinja2.Environment(loader=jinja2.FileSystemLoader(path+'/theme/'+theme))

def use_plugin(plugin,using,request=""):
    if using=="":
        return plugin.main()
    elif plugin.get_name() == using:
        return plugin.main(request)
    else:
        return plugin.main()

env.filters['use_plugin'] = use_plugin # 注册自定义过滤器

@app.route('/')
@app.route('/<using>',methods=['GET','POST'])
def myindex(using=""):
    # Event Index_start
    the_plugins = plugins.dispose.Index_start()
    index_temp = env.get_template('index.html')
    if request.method=="POST":
        return index_temp.render(hi="你好", plugins=the_plugins, request=request,using=using)
    else:
        return index_temp.render(hi="你好",plugins=the_plugins, request="",using=using)

@app.route('/plugins/<name>')
def the_plugins(name):
    plugin = importlib.import_module('plugins.'+name).Main()
    return plugin.main()
