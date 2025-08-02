from .database import db
from datetime import datetime

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(100), nullable=False)  # Team 1 name
    season_id = db.Column(db.Integer, nullable=True)  # Foreign key to Season (not enforced)
    team2 = db.Column(db.String(100), nullable=False)  # Team 2 name
    score = db.Column(db.String(50))  # Match score
    deadline = db.Column(db.DateTime, nullable=False)
    division = db.Column(db.String(10), nullable=False)  # Division as string
    game_type = db.Column(db.String(20), nullable=False)  # 'singles', 'doubles', 'mixed_doubles'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Schedule {self.team1} vs {self.team2} - {self.division} {self.game_type}>'

    def to_dict(self):
        return {
            'id': self.id,
            'team1': self.team1,
            'team2': self.team2,
            'score': self.score,
            'deadline': self.deadline.isoformat(),
            'division': self.division,
            'game_type': self.game_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }