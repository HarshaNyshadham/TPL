from models.database import db

class Playoff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    division = db.Column(db.Float, nullable=False)  # e.g., 5.0, 4.5, 4.0
    game_type = db.Column(db.String(32), nullable=False)  # e.g., 'singles'
    content = db.Column(db.Text, nullable=False)  # Playoff text
    published = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
