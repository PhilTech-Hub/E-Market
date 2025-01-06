from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo



# forms.py

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # role = SelectField('Login as:', choices=[('buyer', 'Buyer'), ('seller', 'Seller'), ('admin', 'Admin')], validators=[DataRequired()])
    
    

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    location = StringField('Location')
    role = SelectField('Register as:', choices=[('buyer', 'Buyer'), ('seller', 'Seller')], validators=[DataRequired()])
    gender = SelectField('Gender:', choices=[('male', 'Male'), ('female', 'Female'), ('rather_not_say', 'Rather Not Say')], validators=[DataRequired()])
    submit = SubmitField('Register')
