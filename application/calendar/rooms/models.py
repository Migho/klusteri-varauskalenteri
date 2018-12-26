from application import db
from application.models import Base

class Room(Base):

    __tablename__ = "room"
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    events = db.relationship('Event', secondary='event_room')

    def __init__(self, name, description):
        self.name = name
        self.description = description