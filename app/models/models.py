import os
from app import db
from flask_login import UserMixin
from werkzeug.utils import secure_filename
from datetime import datetime


# Model for Products (only relevant to sellers)
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image = db.Column(db.String(200), default="default_product.png")  # Default image
    seller_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_products_seller_id"),
        nullable=False
    )

    # Relationship to the User model
    seller = db.relationship("User", backref="products", lazy="joined")

    def __repr__(self):
        return f"<Product {self.name} - Seller {self.seller.username}>"

    @staticmethod
    def save_image(form_picture):
        picture_fn = secure_filename(form_picture.filename)
        picture_path = os.path.join("static/images", picture_fn)
        form_picture.save(picture_path)
        return picture_fn


# Base model for Add to Cart
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    # Relationships (optional for easier navigation)
    user = db.relationship('User', backref='cart_items', lazy=True)
    product = db.relationship('Product', backref='cart_items', lazy=True)


# Base model for all user types (buyer, seller, admin)
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(
        db.String(50), nullable=False, default="Buyer"
    )  # 'buyer', 'seller', 'admin'
    location = db.Column(db.String(100))
    gender = db.Column(db.String(20), nullable=True)  # "male", "female", "rather_not_say"
    profile_image = db.Column(
        db.String(200), nullable=True, default="default_profile.png"
    )  # Default profile image

    def __repr__(self):
        return f"<User {self.username} - Role {self.role}>"

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)

    # Role checks
    def is_seller(self):
        return self.role.lower() == "seller"

    def is_buyer(self):
        return self.role.lower() == "buyer"

    def is_admin(self):
        return self.role.lower() == "admin"


# Model for Sales (tracks purchases)
class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_sales_seller_id"),
        nullable=False
    )  # Seller is a User
    buyer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_sales_buyer_id"),
        nullable=False
    )  # Buyer is also a User
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id", name="fk_sales_product_id"),
        nullable=False
    )
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default="pending")  # "paid", "pending", etc.

    # Relationships
    product = db.relationship("Product", backref="sales", lazy="joined")

    def __repr__(self):
        return f"<Sales {self.id} - Product {self.product_id}>"


# Model for Admin users to manage the platform
class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", name="fk_admin_user_id"),
        nullable=False
    )
    permissions = db.Column(
        db.String(200),
        nullable=False,
        default="manage users, manage products, view analytics",
    )

    user = db.relationship("User", backref="admin_profile", uselist=False)

    def __repr__(self):
        return f"<Admin {self.user_id}>"


# Example function for creating the database
def init_db():
    db.create_all()
