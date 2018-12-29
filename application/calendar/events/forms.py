from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, SelectMultipleField, DateTimeField, validators
from application.calendar.rooms.models import Room
 
class EventForm(FlaskForm):
    name = StringField("Event name (must be unique)", [validators.InputRequired()])
    startTime = DateTimeField("Event starting time YYYY-mm-dd HH:MM:SS")
    endTime = DateTimeField("Event ending time YYYY-mm-dd HH:MM:SS")
    responsible = StringField("Responsible person")
    description = StringField("Description for the event")

    roomsBooked = SelectMultipleField(choices=[(str(r.id)) for r in Room.query.all()])
    privateReserve = SelectMultipleField("Private reserve", choices=[(str(r.id)) for r in Room.query.all()])

    class Meta:
        csrf = False