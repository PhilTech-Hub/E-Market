from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    price = FloatField('Price', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    image = FileField('Product Image')
    submit = SubmitField('Add Product')
       