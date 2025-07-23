from datetime import datetime
from . import db

class Appointable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(100), nullable=False)  # Team name (unique per group/division/type)
    matches = db.Column(db.Integer, default=0)  # Matches played
    won = db.Column(db.Integer, default=0)      # Matches won
    loss = db.Column(db.Integer, default=0)     # Matches lost
    bonus = db.Column(db.Integer, default=0)    # Bonus points
    points = db.Column(db.Integer, default=0)   # Total points
    group = db.Column(db.String(2), nullable=False)  # Group, e.g. 'A', 'B', or 'AA'
    games_total = db.Column(db.Integer, default=0)   # Total games played
    games_won = db.Column(db.Integer, default=0)     # Games won
    games_percentage = db.Column(db.Float, default=0.0)  # Games win %
    division = db.Column(db.String(10), nullable=False)   # Division as string, e.g. '4.0', '4.5', '5.0'
    game_type = db.Column(db.String(20), nullable=False)  # 'singles', 'doubles', 'mixed_doubles'
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Appointable {self.team} - {self.division} {self.game_type}>'

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
            'game_type': self.game_type,
            'season_id': self.season_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def calculate_games_percentage(self):
        """Calculate and update the games percentage"""
        if self.games_total > 0:
            self.games_percentage = (self.games_won / self.games_total) * 100
        else:
            self.games_percentage = 0.0

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g. "Spring 2024"
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teams = db.relationship('Appointable', backref='season', lazy=True)
    schedules = db.relationship('Schedule', backref='season', lazy=True)

    def __repr__(self):
        return f'<Season {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }