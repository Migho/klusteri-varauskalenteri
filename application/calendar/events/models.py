from application import db
from application.models import Base

class Event(Base):

    __tablename__ = "event"
    name = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    responsible = db.Column(db.String(50))
    description = db.Column(db.Text)
    accountId = db.Column(db.Integer, db.ForeignKey('account.id'))
    rooms = db.relationship('Room', secondary='event_room')

    def __init__(self, name, start_time, end_time, responsible, description, accountId):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.responsible = responsible
        self.accountId = accountId