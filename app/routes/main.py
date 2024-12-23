import os
from flask import Blueprint, render_template, redirect, request, flash, url_for
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models import Product, Sales
from app.forms import ProductForm, EditProfileForm
from flask import current_app
from app import db
import paypalrestsdk

main = Blueprint("main", __name__)


@main.route("/")
def home():
    
    return render_template("index.html")


# @main.route('/home')
# def simple_test():
#     return "This route works."

# @main.route('/about')
# def about():
#     return render_template('about.html')


# app/routes/main.py
# In your auth blueprint or main app file
@main.route("/profile")
@login_required
def profile():
    # Add logic to display the user's profile
    # Get the current logged-in user's information using `current_user`
    # user = current_user

    # Pass the user's information to the template
    return render_template("profile.html", user=current_user)


@main.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    # Add logic to display the user's profile
    ## Instantiate the form
    form = EditProfileForm()

    # Pre-populate the form with the current user's information
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.gender.data = current_user.gender
        form.location.data = current_user.location

    # Handle form submission (POST request)
    if form.validate_on_submit():
        # Update the user's information
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.gender = form.gender.data
        current_user.location = form.location.data

        # Handle profile image update
        if form.profile_image.data:
            # Secure the file name
            filename = secure_filename(form.profile_image.data.filename)
            # Define the folder where files will be uploaded
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            # Save the file in the upload folder
            filepath = os.path.join(upload_folder, filename)
            form.profile_image.data.save(filepath)

            # Update the user's profile image URL in the database
            current_user.profile_image = filepath

        # Commit the changes to the database
        db.session.commit()

        # Flash success message and redirect to profile page (or any other page)
        flash("Your profile has been updated!", "success")
        return redirect(url_for("main.profile"))

    # Pass the user's information to the template
    return render_template("edit_profile.html", form=form)


# Seller Dashboard Route
@main.route("/dashboard")
@login_required
def user_dashboard():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template("user_dashboard.html", products=products)


# Add Product Route
@main.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    image_url = None  # Initialize image_url for template use

    if form.validate_on_submit():
        # Check if an image was uploaded and handle it
        if form.image.data:
            image_file = form.image.data
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(
                current_app.root_path, "static/uploads", image_filename
            )
            image_file.save(image_path)
            image_url = image_filename  # Set the image URL to the saved filename
        else:
            image_url = "default_product.png"  # Fallback if no image is provided

        # Create and save the new product
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            location=form.location.data,
            seller_id=current_user.id,
            image_url=image_url,
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("main.user_dashboard"))

    return render_template("add_product.html", form=form, image_url=image_url)


# Edit Product Route
@main.route("/edit_product/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    product = Product.query.get(id)
    if product and product.seller_id == current_user.id:
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            product.category = form.category.data
            product.location = form.location.data
            db.session.commit()
            return redirect(url_for("main.seller_dashboard"))
        return render_template("edit_product.html", form=form, product=product)
    return redirect(url_for("main.seller_dashboard"))


# Delete Product Route
@main.route("/delete_product/<int:id>")
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if product and product.seller_id == current_user.id:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for("main.seller_dashboard"))


# Seller Analytics Route
@main.route("/analytics")
@login_required
def seller_analytics():
    sales_data = Sales.query.filter_by(seller_id=current_user.id).all()
    # You can expand this to show analysis or visualizations
    return render_template("seller_analytics.html", sales_data=sales_data)


# Example route to create a PayPal payment

paypalrestsdk.configure(
    {
        "mode": "sandbox",  # sandbox or live
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
    }
)


@main.route("/pay/<int:product_id>", methods=["GET", "POST"])
@login_required
def pay_product(product_id):
    product = Product.query.get(product_id)
    if product:
        payment = paypalrestsdk.Payment(
            {
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "transactions": [
                    {
                        "amount": {"total": str(product.price), "currency": "KSH"},
                        "description": product.name,
                    }
                ],
                "redirect_urls": {
                    "return_url": url_for("main.payment_success", _external=True),
                    "cancel_url": url_for("main.payment_cancel", _external=True),
                },
            }
        )

        if payment.create():
            return redirect(payment.links[1].href)
        else:
            return "Payment creation failed"
    return redirect(url_for("main.seller_dashboard"))


# You can add more routes for your main blueprint here

@main.route('/browse_products')
def browse_products():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort_by', '')

    # Query products
    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    if category:
        query = query.filter_by(category=category)

    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())

    products = query.paginate(page=page, per_page=10)

    categories = Product.query.with_entities(Product.category.distinct()).all()
    categories = [cat[0] for cat in categories]

    return render_template('browse_products.html', products=products, categories=categories)

@main.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_details.html', product=product)

@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Add the product to the user's cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('main.product_details', product_id=product_id))

@main.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
def add_to_wishlist(product_id):
    # Add the product to the user's wishlist
    flash('Product added to wishlist!', 'success')
    return redirect(url_for('main.product_details', product_id=product_id))
