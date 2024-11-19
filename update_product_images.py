from app import db
from app.models import Product

def update_product_images():
    products = Product.query.all()
    for product in products:
        if not product.image:
            product.image = 'default_product.png'
            db.session.add(product)
    db.session.commit()
    print("Product images updated successfully!")

if __name__ == "__main__":
    from app import create_app
    app = create_app()  # Adjust this if you use a different app factory function

    with app.app_context():
        update_product_images()
