from APP import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
from secrets import token_urlsafe

class User(db.Model, UserMixin):

    def get_formatted_time():

        current_time = datetime.now()

        formatted_time = current_time.replace(microsecond=0)

        return formatted_time


    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default = get_formatted_time, nullable=False)
    account_token = db.Column(db.String(50), nullable=False)
    token_confirmed = db.Column(db.Boolean, nullable = False, default = False)
    token_generated_at = db.Column(db.DateTime(timezone=True), nullable = False, default= datetime.utcnow)

    notes = db.relationship("Note", back_populates="user", lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, email, full_name, password, account_token):
        self.email = email
        self.full_name = full_name
        self.password = password
        self.account_token = account_token
