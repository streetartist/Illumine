import datetime

def format_date(dt):
    """Helper to format date."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_discount(price, discount_percent):
    """Helper to calculate discounted price."""
    return price * (1 - discount_percent / 100)
