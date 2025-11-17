from models.database import db

class PlayoffMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    division = db.Column(db.Float, nullable=False)
    game_type = db.Column(db.String(32), nullable=False)
    round = db.Column(db.String(16), nullable=False)  # 'RO16', 'QF', 'SF', 'F'
    position = db.Column(db.Integer, nullable=False)  # position in bracket
    player1 = db.Column(db.String(64), nullable=False)
    player2 = db.Column(db.String(64), nullable=False)
    score = db.Column(db.String(32), nullable=True)
    winner = db.Column(db.String(64), nullable=True)
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
