from .database import db
from datetime import datetime

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    partner_name = db.Column(db.String(100))  # For doubles/mixed doubles
    game_type = db.Column(db.String(20), nullable=False)  # 'singles', 'doubles', 'mixed_doubles'
    division = db.Column(db.Float)  # Will be set when assigned to a division
    group = db.Column(db.String(1))  # Will be set when assigned to a group
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        if self.partner_name:
            return f'<Player {self.name} & {self.partner_name}>'
        return f'<Player {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'partner_name': self.partner_name,
            'game_type': self.game_type,
            'division': self.division,
            'group': self.group,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 