### Steps to execute script
### flask shell
### exec(open('insert_product_data.py').read())

from app import db
from models import User, Product, Categories
import requests

categories = ["men's clothing", "jewelery", "electronics", "women's clothing"]

if len(Categories.query.all()) == 0:
    for category in categories:
        db.session.add(Categories(name=category))
        db.session.commit()

product_data = requests.get("https://fakestoreapi.com/products").json()


if len(Product.query.all()) == 0:
    for product in product_data:
        db.session.add(Product(name=product['title'], description=product['description'], price=product['price'], image_url=product['image'], category_id=categories.index(product['category']) + 1))
        db.session.commit()