from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, validators
 
class AddRoomForm(FlaskForm):
    name = StringField("Room name (must be unique)", [validators.InputRequired()])
    description = StringField("Description for the room")

    class Meta:
        csrf = False

class EditRoomForm(FlaskForm):
    name = StringField("New room name", [validators.InputRequired()])
    description = StringField("New description")
    hidden = BooleanField("Disable room")

    class Meta:
        csrf = False
