from APP import db
from datetime import datetime

class Note_Content(db.Model):
    __tablename__ = "note_content"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Date, nullable=False,default = datetime.now().date())

    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'))
    note = db.relationship("Note", back_populates="contents")

    def __init__(self,content, note_id):
        self.content = content
        self.note_id = note_id
    
    