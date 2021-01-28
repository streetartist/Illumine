class Main:
    def __init__(self):
        self.name='test'

    def main(self,request=None):
        if request == None:
            return '''<h1>欢迎使用插件TEST！</h1>
            <form method="post" action="/'''+'test'+'''">
              <input type="text" value="World" name="name" />
              <button type="submit">Give it now!</button>
            </form>
            '''
        else:
            return "欢迎，" + request.form.get("name")


    def get_name(self):
        return self.name
