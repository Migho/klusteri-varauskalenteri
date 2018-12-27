from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, validators
 
class AddAccountForm(FlaskForm):
    username = StringField("Username for new user (must be unique)", [validators.InputRequired()])
    password = PasswordField("Password for new user", [validators.InputRequired()])

    class Meta:
        csrf = False

class EditAccountForm(FlaskForm):
    username = StringField("Username for the user", [validators.InputRequired()])
    password = PasswordField("Password for the user (leave blank for no update)")
    hidden = BooleanField("Disable user")

    class Meta:
        csrf = False
