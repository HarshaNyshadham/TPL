from .database import db
from datetime import datetime

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Player or team name
    game_type = db.Column(db.String(20), nullable=False)  # 'singles', 'doubles', 'mixed_doubles'
    division = db.Column(db.String(10))  # Division as string, e.g. '4.0', '4.5', '5.0'
    group = db.Column(db.String(2))  # Group, e.g. 'A', 'B', or 'AA'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

    def __repr__(self):
        return f'<Player {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'game_type': self.game_type,
            'division': self.division,
            'group': self.group,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }