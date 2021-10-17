from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FloatField


class UserForm(FlaskForm):
    user_id = StringField(label="User ID")
    user_first_name = StringField(label="First Name")
    user_last_name = StringField(label="Last Name")
    user_email = StringField(label="E-mail")
    user_phone = StringField(label="Phone")
    user_is_admin = StringField(label="Admin")
    user_note = StringField(label="User Notes")
