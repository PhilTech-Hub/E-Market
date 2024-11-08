from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)], places=2)
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=120)])
    category = SelectField('Category', choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('home', 'Home')], validators=[DataRequired()])
    submit = SubmitField('Add Product')
