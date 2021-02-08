from battery.blog.db import Post

class Main:
    def __init__(self, env,path):
        self.env=env
        self.path=path
        self.name ="archive"

    def main(self,request=None,arg=None,plugin=None):
        self.thus = self.env.get_template(self.path+"archive.html")
        return self.thus.render(posts = Post.select())