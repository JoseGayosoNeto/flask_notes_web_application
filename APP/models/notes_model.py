from APP import db
from datetime import datetime


class Note(db.Model):

    def get_formatted_time():

        current_time = datetime.now()
        formatted_time = current_time.replace(microsecond=0)
        return formatted_time


    __tablename__="notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    note_name = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default = get_formatted_time, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usuario = db.relationship("User", back_populates="notes")

    contents = db.relationship("Note_Content", back_populates="note", lazy="dynamic")

    def __init__(self, note_name, user_id):
        self.note_name = note_name
        self.user_id = user_id


    


