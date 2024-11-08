from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Product, Sales
from app.forms import ProductForm
from app import db
import paypalrestsdk

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')

@main.route('/home')
def simple_test():
    return "This route works."

@main.route('/about')
def about():
    return render_template('about.html')

# app/routes/main.py

# Seller Dashboard Route
@main.route('/dashboard')
@login_required
def seller_dashboard():
    products = Product.query.filter_by(seller_id=current_user.id).all()
    return render_template('seller_dashboard.html', products=products)

# Add Product Route
@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, description=form.description.data, price=form.price.data, category=form.category.data, location=form.location.data, seller_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('main.seller_dashboard'))
    return render_template('add_product.html', form=form)

# Edit Product Route
@main.route('/edit_product/<int:id>', methods=['GET', 'POST'])
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
            return redirect(url_for('main.seller_dashboard'))
        return render_template('edit_product.html', form=form, product=product)
    return redirect(url_for('main.seller_dashboard'))

# Delete Product Route
@main.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if product and product.seller_id == current_user.id:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('main.seller_dashboard'))

# Seller Analytics Route
@main.route('/analytics')
@login_required
def seller_analytics():
    sales_data = Sales.query.filter_by(seller_id=current_user.id).all()
    # You can expand this to show analysis or visualizations
    return render_template('seller_analytics.html', sales_data=sales_data)


# Example route to create a PayPal payment

paypalrestsdk.configure({
  'mode': 'sandbox',  # sandbox or live
  'client_id': 'your_client_id',
  'client_secret': 'your_client_secret'
})



@main.route('/pay/<int:product_id>', methods=['GET', 'POST'])
@login_required
def pay_product(product_id):
    product = Product.query.get(product_id)
    if product:
        payment = paypalrestsdk.Payment({
            'intent': 'sale',
            'payer': {'payment_method': 'paypal'},
            'transactions': [{
                'amount': {
                    'total': str(product.price),
                    'currency': 'KSH'
                },
                'description': product.name
            }],
            'redirect_urls': {
                'return_url': url_for('main.payment_success', _external=True),
                'cancel_url': url_for('main.payment_cancel', _external=True)
            }
        })
        
        if payment.create():
            return redirect(payment.links[1].href)
        else:
            return "Payment creation failed"
    return redirect(url_for('main.seller_dashboard'))




# You can add more routes for your main blueprint here
