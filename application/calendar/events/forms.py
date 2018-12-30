from flask_wtf import FlaskForm
import datetime
from wtforms import PasswordField, StringField, BooleanField, SelectMultipleField, DateTimeField, validators, ValidationError
from wtforms_components import DateRange
from application.calendar.rooms.models import Room
from sqlalchemy.sql import text
from application import db

def TimeNotOverlapping(form, field):
    if form.data.get('startTime') is None or form.data.get('endTime') is None:
        raise ValidationError('Check the dates')
    startTime = form.data.get('startTime').strftime("%Y-%m-%d %H:%M:%S")
    endTime = form.data.get('endTime').strftime("%Y-%m-%d, %H:%M:%S")
    print("start:", startTime, "end:", endTime)
    for roomId in field.data:
        statement = text(("SELECT * FROM Event INNER JOIN event_room ON event.id = event_room.event_id" +
                " WHERE ('" + startTime + "' BETWEEN startTime AND endTime" +
                " OR '" + endTime + "' BETWEEN startTime AND endTime" +
                " OR startTime BETWEEN '" + startTime + "' AND '" + endTime + "'" +
                " OR endTime BETWEEN '" + startTime + "' AND '" + endTime + "'" +
                " OR startTime = '" + startTime + "' OR endTime = '" + endTime + "')" +
                " AND event_room.room_id = " + roomId))
        result = db.engine.execute(statement)
        if result.first() is not None:
            print("Found overlapping when creating the event :(")
            raise ValidationError('Overlapping time periods')
        else:
            print("Did not find any overlappings")
 
class EventForm(FlaskForm):
    name = StringField("Event name (must be unique)", [validators.InputRequired()])
    startTime = DateTimeField("Event starting time YYYY-mm-dd HH:MM:SS",
            validators=[DateRange(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=365))])
    endTime = DateTimeField("Event ending time YYYY-mm-dd HH:MM:SS",
            validators=[DateRange(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=365))])
    responsible = StringField("Responsible person", [validators.InputRequired()])
    description = StringField("Description for the event")

    roomsBooked = SelectMultipleField(choices=[(str(r.id)) for r in Room.query.all()], 
            validators=[TimeNotOverlapping])
    privateReserve = SelectMultipleField("Private reserve", choices=[(str(r.id)) for r in Room.query.all()])

    class Meta:
        csrf = False