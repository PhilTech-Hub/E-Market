# models.py
from app.db import db
from flask_login import UserMixin

from datetime import datetime




# Model for Products (only relevant to sellers)
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Correct the relationship by using a valid loading strategy
    seller = db.relationship('User', backref='seller_products', lazy='joined')

    def __repr__(self):
        return f'<Product {self.name}>'

    
# Base model for all user types (buyer, seller, admin)
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'buyer', 'seller', 'admin'
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))

    # Relationship for sellers and buyers
    products = db.relationship('Product', backref='owner', lazy=True)  # For sellers
    sales = db.relationship('Sales', backref='buyer', lazy=True)  # For buyers
    products = db.relationship('Product', foreign_keys=[Product.seller_id], lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    

    

# Model for Sales (tracks purchases)
class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product = db.relationship('Product')
    amount = db.Column(db.Float, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key linking sale to buyer
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key linking sale to product
    payment_status = db.Column(db.String(20))  # "paid", "pending", "rejected", etc.

    def __repr__(self):
        return f'<Sales {self.id} - Product {self.product_id} sold to Buyer {self.buyer_id}>'
    
   
    

# Example model for Admin users to manage the platform
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Linking admin to User
    permissions = db.Column(db.String(200), nullable=False, default="manage users, manage products, view analytics")

    user = db.relationship('User', backref='admin', uselist=False)

    def __repr__(self):
        return f'<Admin {self.admin_id}>'

# Example function for creating the database
def init_db():
    db.create_all()
