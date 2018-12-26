from application import db
from application.models import Base

class Event(Base):

    __tablename__ = "event"
    name = db.Column(db.String(50), unique=True, nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    responsible = db.Column(db.String(50))
    accountId = db.Column(db.Integer, db.ForeignKey('account.id'))
    events = db.relationship('Room', secondary='event_room')

    def __init__(self, name, startTime, endTime, description, privateEvent, responsible, accountId):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.description = description
        self.privateEvent = privateEvent
        self.responsible = responsible
        self.accountId = accountId