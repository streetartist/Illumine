from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from illumine.core import Illumine

def init_admin(app: 'Illumine'):
    """
    Initialize the admin interface.
    """
    
    @app.route("/admin")
    def admin_dashboard():
        # In a real app, this would use the theme manager or a separate admin template
        return """
        <h1>Admin Dashboard</h1>
        <ul>
            <li><a href="/admin/plugins">Manage Plugins</a></li>
            <li><a href="/">Back to Site</a></li>
        </ul>
        """

    @app.route("/admin/plugins")
    def admin_plugins():
        plugins_list = "<ul>"
        for name in app.plugin_manager.plugins:
            plugins_list += f"<li>{name}</li>"
        plugins_list += "</ul>"
        return f"<h1>Plugins</h1>{plugins_list}<br><a href='/admin'>Back</a>"
