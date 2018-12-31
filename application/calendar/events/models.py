from application import db
from application.models import Base

class Event(Base):

    __tablename__ = "event"
    name = db.Column(db.String(50), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)
    responsible = db.Column(db.String(50))
    description = db.Column(db.Text)
    accountId = db.Column(db.Integer, db.ForeignKey('account.id'))
    rooms = db.relationship('Room', secondary='event_room')

    def __init__(self, name, startTime, endTime, responsible, description, accountId):
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.description = description
        self.responsible = responsible
        self.accountId = accountId