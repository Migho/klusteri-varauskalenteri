from flask_wtf import FlaskForm
import datetime
from wtforms import PasswordField, StringField, BooleanField, SelectMultipleField, DateTimeField, validators
from wtforms_components import DateRange
from application.calendar.rooms.models import Room
 
class EventForm(FlaskForm):
    name = StringField("Event name (must be unique)", [validators.InputRequired()])
    startTime = DateTimeField("Event starting time YYYY-mm-dd HH:MM:SS", validators=[DateRange(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=365))])
    endTime = DateTimeField("Event ending time YYYY-mm-dd HH:MM:SS", validators=[DateRange(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=365))])
    responsible = StringField("Responsible person", [validators.InputRequired()])
    description = StringField("Description for the event")

    roomsBooked = SelectMultipleField(choices=[(str(r.id)) for r in Room.query.all()])
    privateReserve = SelectMultipleField("Private reserve", choices=[(str(r.id)) for r in Room.query.all()])

    class Meta:
        csrf = False