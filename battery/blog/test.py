from db import Post

p = Post(tag='测试', time="2020-12-26", author = "测试", content = "#第一个Markdown测试文章",title = "测试MD文章")
p.save()

print('DONE')