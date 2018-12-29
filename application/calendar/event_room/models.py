from application import db
from application.models import Base

class EventRoom(Base):

    __tablename__ = "event_room"
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    privateEvent = db.Column(db.Boolean, server_default="0")

    def __init__(self, event_id, room_id, privateEvent):
        self.event_id = event_id
        self.room_id = room_id
        self.privateEvent = privateEvent