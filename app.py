import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from illumine import Illumine
from website.core import SiteManager
from website.views import init_website_routes
from website.auth import init_auth_routes

def main():
    # Initialize without global static folder
    # Illumine will auto-detect active theme's static folder
    app = Illumine(engine_type="flask")
    
    # Load Batteries
    app.load_battery("blog")
    app.load_battery("forum")
    
    # Load Website Resources (static/templates inside website/)
    app.load_website_resources("website")
    
    # Initialize separate views modules (Multi-file support demonstration)
    init_website_routes(app) # General views
    init_auth_routes(app)    # Authentication views
    
    # Initialize Site Manager
    site_manager = SiteManager(app.theme_manager)
    
    @app.route("/")
    def index():
        return site_manager.render_page(
            title="Welcome to Illumine", 
            content="""
            <div class="hero">
                <p>A generic, modern website framework for Python.</p>
            </div>

            <div class="features">
                <h3>Key Features</h3>
                <ul class="feature-list">
                    <li><strong>Modular Design:</strong> Built with batteries and plugins.</li>
                    <li><strong>Theme System:</strong> Easy to customize with Jinja2 templates.</li>
                    <li><strong>Flexible Core:</strong> Supports Flask and FastAPI engines.</li>
                </ul>
            </div>

            <div class="actions" style="margin-top: 2rem;">
                <h3>Explore Examples</h3>
                <p>Check out the included batteries and examples:</p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <a href="/blog" class="btn">Visit Blog</a>
                    <a href="/forum" class="btn">Visit Forum</a>
                    <a href="/products" class="btn">View Products</a>
                    <a href="/custom" class="btn">Custom Page</a>
                    <a href="/login" class="btn">Login Demo</a>
                </div>
            </div>
            """
        )

    # Run the app
    app.run(debug=True)

if __name__ == "__main__":
    main()
