from APP import db
from sqlalchemy.sql import func


class Note(db.Model):

    def get_formatted_time():

        current_time = func.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        return formatted_time


    __tablename__="notes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    note_name = db.Column(db.String(50), unique=True, nullable=False)
    data = db.Column(db.String(10000), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default = get_formatted_time, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usuario = db.relationship("User", back_populates="notes")

    def __init__(self, note_name,  data, user_id):
        self.note_name = note_name
        self.data = data
        self.user_id = user_id


    


