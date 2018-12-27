from application import db
from application.models import Base

class Account(Base):

    __tablename__ = "account"
    username = db.Column(db.String(144), unique=True, nullable=False)
    password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Boolean(), server_default="0")
    hidden = db.Column(db.Boolean(), server_default="0")
    events = db.relationship('Event', backref='creator')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_id(self):
        return self.id
  
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        if self.username == "admin":
            return ["ADMIN", "SUPERADMIN"]
        elif self.admin is True:
            return ["ADMIN"]
        else:
            return ["account"]
