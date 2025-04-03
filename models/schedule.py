from .database import db
from datetime import datetime

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    score = db.Column(db.String(50))  # Nullable since score won't be set initially
    deadline = db.Column(db.DateTime, nullable=False)
    division = db.Column(db.Float, nullable=True)  # Making division optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Schedule {self.team1} vs {self.team2}>' 