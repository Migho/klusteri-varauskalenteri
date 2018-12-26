from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
 
class AddAccountForm(FlaskForm):
    username = StringField("Username for new user", [validators.InputRequired()])
    password = PasswordField("Password for new user", [validators.InputRequired()])

    class Meta:
        csrf = False
