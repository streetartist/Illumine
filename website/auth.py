from illumine.core import Illumine
from .utils import format_date
import datetime

def init_auth_routes(app: Illumine):
    """
    Initialize authentication routes.
    """
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        now = format_date(datetime.datetime.now())
        return app.theme_manager.render(
            "page.html",
            title="Login",
            content=f"""
            <form method='post'>
                Username: <input type='text' name='username'><br>
                Password: <input type='password' name='password'><br>
                <button type='submit'>Login</button>
            </form>
            <p><small>Server time: {now}</small></p>
            """
        )

    @app.route("/logout")
    def logout():
        return "Logged out"
