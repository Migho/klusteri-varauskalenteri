from application import db
from application.models import Base

class eventRoom(Base):

    __tablename__ = "event_room"
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    privateEvent = db.Column(db.Boolean, server_default="0")