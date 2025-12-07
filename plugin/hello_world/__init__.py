def init_plugin(app):
    print("Hello World Plugin Initialized!")
    
    @app.route("/plugin/hello")
    def plugin_hello():
        return "Hello from Plugin!"
