from flask import Flask,request,url_for,send_file
import jinja2

import importlib

import sys
import os

is_pythonanywhere = True
theme = 'goodold'

if not is_pythonanywhere:
    path = os.path.abspath('.')
else:
    path = os.sep.join(['','home','streetartist'])

sys.path.append(os.sep.join([path, "plugins",'']))
sys.path.append(os.sep.join([path,"battery",""]))

import conf

app = Flask(__name__)

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
    return "./file/" + theme + '/' + filename

env.filters['url_to'] = url_to

@app.route('/file/<theme>/<filename>')
def get_file(theme,filename):
    file_path = os.sep.join([path, "theme",theme ,filename])
    return send_file(file_path)

@app.route('/')
@app.route('/<using>',methods=['GET','POST'])
def myindex(using=""):
    # Battery Include
    for I in conf.setting:
        this = I(env=env,path=os.sep.join(["battery",conf.battery,""]))
        if using == this.name:
            return this.main()
    # Event Index_start
    the_plugins = plugins.dispose.Index_start()
    index_temp = env.get_template(os.sep.join(['theme',theme,'index.html']))
    if request.method=="POST":
        return index_temp.render(hi="你好", plugins=the_plugins, request=request,using=using)
    else:
        return index_temp.render(hi="你好",plugins=the_plugins, request="",using=using)

@app.route('/plugins/<name>')
def the_plugins(name):
    plugin = importlib.import_module('plugins.'+name).Main()
    return plugin.main()

if __name__ == '__main__':
   app.run(debug=True)
