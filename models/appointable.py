from datetime import datetime
from . import db

class Appointable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(100), nullable=False)  # Changed from name to team
    matches = db.Column(db.Integer, default=0)
    won = db.Column(db.Integer, default=0)
    loss = db.Column(db.Integer, default=0)
    bonus = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)
    group = db.Column(db.Integer, nullable=False)
    games_total = db.Column(db.Integer, default=0)
    games_won = db.Column(db.Integer, default=0)
    games_percentage = db.Column(db.Float, default=0.0)  # For %games
    division = db.Column(db.Float, nullable=False)  # For storing division like 4.0, 4.5, 5.0
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Appointable {self.team}>'

    def to_dict(self):
        return {
            'id': self.id,
            'team': self.team,
            'matches': self.matches,
            'won': self.won,
            'loss': self.loss,
            'bonus': self.bonus,
            'points': self.points,
            'group': self.group,
            'games_total': self.games_total,
            'games_won': self.games_won,
            'games_percentage': self.games_percentage,
            'division': self.division,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def calculate_games_percentage(self):
        """Calculate and update the games percentage"""
        if self.games_total > 0:
            self.games_percentage = (self.games_won / self.games_total) * 100
        else:
            self.games_percentage = 0.0 