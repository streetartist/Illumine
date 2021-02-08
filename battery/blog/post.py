from battery.blog.db import Post

class Main:
    def __init__(self, env,path):
        self.env=env
        self.path=path
        self.name ="post"

    def main(self,request=None,arg=None,plugin=None):
        if arg != None:
            self.thus = self.env.get_template(self.path+"post.html")
            return self.thus.render(posts = Post.select().where(Post.title == arg))