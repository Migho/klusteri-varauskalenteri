from flask_wtf import FlaskForm
import datetime
from wtforms import PasswordField, StringField, BooleanField, IntegerField, SelectMultipleField, DateTimeField, validators, ValidationError
from wtforms_components import DateRange
from application.calendar.rooms.models import Room
from sqlalchemy.sql import text
from application import db
from flask import request

class SelectMultipleFieldWithRoomChoices(SelectMultipleField):
    # The original SelectMultipleField required choices to be specified in the attributes,
    # which caused the events with new rooms chosen to fail.
    def pre_validate(self, form):
        if self.data:
            choices=[(str(r.id)) for r in Room.query.all()]
            for d in self.data:
                if d not in choices:
                    raise ValueError(self.gettext("'%(value)s' is not a valid choice for this field") % dict(value=d))

def TimeNotOverlapping():
    def _TimeNotOverlapping(form, field):
        if form.data.get('start_time') is None or form.data.get('end_time') is None:
            raise ValidationError('There is something wrong with the dates, couldnt check if room available')
        start_time = form.data.get('start_time').strftime("%Y-%m-%d %H:%M:%S")
        end_time = form.data.get('end_time').strftime("%Y-%m-%d %H:%M:%S")
        for roomId in field.data:
            if form.data.get('event_id') is not None:
                ownEventRoomsStatement = " AND event_room.event_id != " + str(form.data.get('event_id'))
            else:
                ownEventRoomsStatement = ""
            # In a nutshell: check if any time is between any other time period, or exactly the same
            statement = text("SELECT * FROM Event INNER JOIN event_room ON event.id = event_room.event_id" +
                    " WHERE ('" + start_time + "' BETWEEN event.start_time AND event.end_time" +
                    " OR '" + end_time + "' BETWEEN event.start_time AND event.end_time" +
                    " OR event.start_time BETWEEN '" + start_time + "' AND '" + end_time + "'" +
                    " OR event.end_time BETWEEN '" + start_time + "' AND '" + end_time + "'" +
                    " OR event.start_time = '" + start_time + "' OR event.end_time = '" + end_time + "')" +
                    " AND event_room.room_id = " + roomId + ownEventRoomsStatement)
            
            result = db.engine.execute(statement)
            if result.first() is not None:
                print("Found overlapping when creating the event :(")
                raise ValidationError('Overlapping time periods')
            else:
                print("Did not find any overlappings")
    return _TimeNotOverlapping
 
class EventForm(FlaskForm):
    event_id = IntegerField()
    name = StringField("Event name", [validators.InputRequired()])
    start_time = DateTimeField("Event starting time YYYY-mm-dd HH:MM:SS",
            validators=[DateRange(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=365))])
    end_time = DateTimeField("Event ending time YYYY-mm-dd HH:MM:SS",
            validators=[DateRange(datetime.datetime.today(), datetime.datetime.today() + datetime.timedelta(days=365))])
    responsible = StringField("Responsible person", [validators.InputRequired()])
    description = StringField("Description for the event")

    roomsBooked = SelectMultipleFieldWithRoomChoices(validators=[TimeNotOverlapping(), validators.InputRequired()])
    privateReserve = SelectMultipleFieldWithRoomChoices("Private reserve")

    class Meta:
        csrf = False