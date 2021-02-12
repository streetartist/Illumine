from flask import Flask,render_template,request, session, url_for
import pickle
from peewee import *
import filter

import importlib # 动态导入

#f = filter.DFAFilter()
#f.parse("/home/artsite/mysite/keywords")
#print(f.filter("hello sexy baby"))

path = "/home/artsite/mysite"

def module(string):
    tool = importlib.import_module('tool.'+string)
    the = tool.Main()
    return the.main()

db = SqliteDatabase('this.db')

class Chat(Model):
    massage = CharField()
    class Meta:
        database = db

class Dicuss(Model):
    path = CharField()
    class Meta:
        database = db

class User(Model):
    name = CharField()
    password = CharField()
    type = CharField()
    class Meta:
        database = db

class Post_(Model):
    time = CharField()
    content = CharField()
    author = CharField()
    tag = CharField()
    title = CharField()
    class Meta:
        database = db

class Tool(Model):
    name = CharField()
    html = CharField()
    py = CharField()
    class Meta:
        database = db

db.create_tables([Chat, Post_, User,Tool])

#p = Posts(tag='测试', time="2020-12-26", author = "测试", content = "#第一个Markdown测试文章",title = "测试MD文章")
#p.save()

#u = User(name="admin",password="wenjiaxian",type="admin")
#u.save()

#t = Tool(name="test",html="<h1>这是一个测试插件</h1>",py="")
#t.save()

app = Flask(__name__, static_folder='static')

app.config['SECRET_KEY'] = 'XXXXX'

#下面两行不要忘记加入！
env = app.jinja_env#取得运行环境
env.filters['module'] = module#注册自定义过滤

def isadmin(func):
    def wrapper(*args, **kwargs):
        if "log_in" in session:
            if session["type"] == "admin":
                return func(*args, **kwargs)
            else:
                return "您没有管理权限"
        else:
            return "您没有登录"
    return wrapper

@app.route("/tool/<name>")
def open_tool(name):
    tool = importlib.import_module('tool.'+name)
    the = tool.Main()
    return the.main()

@app.route("/new_tool/name=<name>;html=<html>;py=<py>")
def new_tool(html,py):
    pass

@app.route("/delete/<title>")
def delete_post(title):
    Post_.delete().where(Post_.title==title).execute()
    return "删除成功"


@app.route('/',methods=["POST", "GET"])
def myindex():
    tool = Tool.select()
    with open("./count.txt","rb") as f:
        count = pickle.load(f)
    with open("./count.txt","wb") as f:
        pickle.dump(count + 1,f)
    if request.method == "GET":
        if "log_in" in session:
            welcome = "欢迎，" + session["name"]
        else:
            welcome = "尚未登录！"
        return render_template("home.html",welcome = welcome,count = count,says = Chat.select(),tool = tool,posts = Post_.select())
    if request.method == "POST":
        f = filter.DFAFilter()
        f.parse(path +"/zanghua.txt")
        word1 = request.form.get("word")
        word = f.filter(word1)
        if len(word) > 100:
            return "字数太多了！"
        else:
            new=Chat(massage=word)
            new.save()
        #users.append({"text": word})
        return render_template("home.html",count = count,says = Chat.select(), tool=tool,posts = Post_.select())


@app.route('/archive',methods=["POST", "GET"])
def archive():
    if request.method == "GET":
        return render_template("archive.html",posts = Post_.select())


@app.route("/post/<title>",methods= ["POST","GET"])
def post(title):
    if request.method == "GET":
        return render_template("post.html", posts = Post_.select().where(Post_.title == title))


@app.route("/new",methods= ["POST","GET"])
def new():
    if request.method == "GET":
        if 'log_in' in session:
            if session["type"] == "admin":
                welcome = True
            else:
                welcome = False
        else:
                welcome = False
        return render_template("new.html",welcome = welcome,post=Post_.select())
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        time = request.form.get("time")
        author = request.form.get("author")
        tag = request.form.get("tag")
        change = request.form.get("change")
        if change != "1":
            p = Post_(tag=tag, time=time, author = author, content = text,title = title)
            p.save()
            return "创建成功！"
        else:
            Post_.update(tag=tag, time=time, author=author, content=text, title=title).where(Post_.title == title).execute()
            return "修改成功"

@app.route('/menu',methods=["POST", "GET"])
def hello_menu():
    return render_template("menu.html")


@app.route("/help",methods=["POST","GET"])
def help():
    if request.method == "GET":
        return render_template("help.html")
    elif request.method == "POST":
        return "该功能正在开发！"

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        try:
            yes = User.get(User.name == name)
        except:
            return "登录错误"
        if yes.password == password:
            session["log_in"] = True
            session["name"] = name
            session["type"] = yes.type
            return "登录成功"
        else:
            return "密码错误"
    if request.method == "GET":
        return render_template("login.html")

@isadmin
@app.route('/admin', methods=["GET","POST"])
def admin():
    if request.method == "GET":
        return render_template("admin.html",welcome="欢迎")

@isadmin
@app.route('/the_tool', methods=["GET","POST"])
def thetool():
    if request.method == "GET":
        return render_template("tool.html")


@app.route('/blog')
def index():
    return render_template('welcome.html', title="Welcome")


@app.route('/home')
def home():
    return render_template('base.html', title="Home")
