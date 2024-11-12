# In app/forms/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    profile_image = FileField('Profile Image')  # New field for profile image
    submit = SubmitField('Save Changes')
