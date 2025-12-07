from illumine.core import Illumine
from .models import Product
from .utils import calculate_discount

def init_website_routes(app: Illumine):
    """
    Initialize general website routes.
    """
    
    @app.route("/custom")
    def custom_page():
        return app.theme_manager.render(
            "custom_page.html", 
            title="Custom Multi-file Page", 
            message="Hello from website/views.py! This demonstrates multi-file organization."
        )
        
    @app.route("/website-template")
    def website_template_demo():
        # Renders a template located in website/templates/
        return app.theme_manager.render("website_page.html")

    @app.route("/products")
    def products():
        # Example using models and utils
        # In a real app, you'd query the DB: products = db.query(Product).all()
        # Here we mock it for demonstration
        mock_products = [
            {"name": "Laptop", "price": 1000},
            {"name": "Wireless Mouse", "price": 50},
            {"name": "Mechanical Keyboard", "price": 120},
            {"name": "HD Monitor", "price": 300},
        ]
        
        products_data = []
        for p in mock_products:
            discounted = calculate_discount(p['price'], 10) # 10% off
            products_data.append({
                "name": p['name'],
                "price": p['price'],
                "discounted_price": discounted
            })
        
        return app.theme_manager.render(
            "products.html",
            products=products_data
        )
