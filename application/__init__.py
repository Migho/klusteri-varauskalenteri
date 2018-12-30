from flask import Flask
app = Flask(__name__)

# database connectivity and ORM
from flask_sqlalchemy import SQLAlchemy
import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"    
    app.config["SQLALCHEMY_ECHO"] = True    # debugging :)
db = SQLAlchemy(app)

# login functionality 1
from os import urandom
app.config["SECRET_KEY"] = urandom(32)
from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."

# roles in login_required
from functools import wraps
def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

# Database content
from application.accounts import models
from application.calendar.events import models
from application.calendar.rooms import models
from application.calendar.event_room import models

# Login functionality 2
from application.accounts.models import Account
@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(user_id)

# Database creation
try:
    db.create_all()
except:
    pass

# Load application content
from application import views
from application.auth import views
from application.accounts import views
from application.calendar.rooms import views
from application.calendar.events import views
