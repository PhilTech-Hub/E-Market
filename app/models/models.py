# models.py
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
    image_url = db.Column(db.String(200), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationship to the User model
    seller = db.relationship("User", backref="seller_products", lazy="joined")

    def __repr__(self):
        return f"<Product {self.name}>"

    @staticmethod
    def save_image(form_picture):
        # Set the file path and ensure the filename is secure
        picture_fn = secure_filename(form_picture.filename)
        picture_path = os.path.join("static/images", picture_fn)
        form_picture.save(picture_path)
        return picture_fn


# Base model for all user types (buyer, seller, admin)
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(
        db.String(50), nullable=False, default="user"
    )  # 'buyer', 'seller', 'admin'
    location = db.Column(db.String(100))
    gender = db.Column(db.String(100), nullable=True)

    # Add profile_image field to store the path of the profile image
    profile_image = db.Column(
        db.String(200), nullable=True, default="default_profile.png"
    )  # default image if none provided

    # Relationship for sellers
    products = db.relationship("Product", backref="owner", lazy=True)

    # Relationship for buyers
    sales = db.relationship("Sales", backref="buyer", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash

        return check_password_hash(self.password, password)

    def is_seller(self):
        return self.role == "seller"

    # Check if user is a buyer
    def is_buyer(self):
        return self.role == "buyer"

    # Check if user is an admin
    def is_admin(self):
        return self.role == "admin"

    # Add roles or permissions logic
    def has_permission(self, permission_name):
        if self.is_admin:
            return True  # Admins have access to all permissions
        # Define permission logic for sellers and buyers
        permissions = {
            "view_settings": self.is_seller or self.is_buyer,
            "view_orders": self.is_buyer,  # Only buyers
            "view_product_list": self.is_buyer,  # Only buyers
            "view_profile": True,  # All authenticated users
            "manage_products": self.is_seller,  # Only sellers
            "view_sales_reports": self.is_seller,  # Only sellers
        }
        return permissions.get(permission_name, False)


# Model for Sales (tracks purchases)
class Sales(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    date_sold = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product = db.relationship("Product")
    amount = db.Column(db.Float, nullable=False)
    buyer_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # Foreign key linking sale to buyer
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )  # Foreign key linking sale to product
    payment_status = db.Column(db.String(20))  # "paid", "pending", "rejected", etc.

    def __repr__(self):
        return f"<Sales {self.id} - Product {self.product_id} sold to Buyer {self.buyer_id}>"


# Example model for Admin users to manage the platform
class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # Linking admin to User
    permissions = db.Column(
        db.String(200),
        nullable=False,
        default="manage users, manage products, view analytics",
    )

    user = db.relationship("User", backref="admin", uselist=False)

    def __repr__(self):
        return f"<Admin {self.admin_id}>"


# Example function for creating the database
def init_db():
    db.create_all()
