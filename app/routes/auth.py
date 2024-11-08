from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from app.models import User
from app.forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

# Initialize the Blueprint for authentication
auth = Blueprint("auth", __name__)

# Initialize Bcrypt
bcrypt = Bcrypt()


# User Registration Route
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            location=form.location.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


# Seller Login Route (to be implemented)
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Placeholder for login functionality (using Flask-Login)
    form = LoginForm()
    if form.validate_on_submit():
        # Fetch the user object based on username
        user = User.query.filter_by(username=form.username.data).first()

        # Check if user exists and password matches
        if user and user.check_password(form.password.data):
            login_user(user)  # Pass the user object to login_user
            flash("Login successful!", "success")
            return redirect(
                url_for("main.home")
            )  # Redirect to the home page or a protected route
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")

    return render_template("login.html", form=form)


# Seller Logout Route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
