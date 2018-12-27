from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
 
class AddAccountForm(FlaskForm):
    username = StringField("Username for new user", [validators.InputRequired()])
    password = PasswordField("Password for new user", [validators.InputRequired()])

    class Meta:
        csrf = False

class EditAccountForm(FlaskForm):
    username = StringField("Username for the user", [validators.InputRequired()])
    password = PasswordField("Password for the user (leave blank for no update)")

    class Meta:
        csrf = False
