from datetime import datetime, timedelta
from .database import db
from .appointable import Appointable
from .schedule import Schedule

def seed_database():
    """Seed the database with initial data"""
    # Clear existing data
    Schedule.query.delete()
    Appointable.query.delete()
    
    # Seed Appointable data for each division
    divisions = [5.0, 4.5, 4.0]
    for division in divisions:
        for i in range(1, 6):  # 5 teams per division
            team = Appointable(
                team=f'Team {i} - {division}',
                division=division,
                matches=0,
                won=0,
                loss=0,
                bonus=0,
                points=0,
                group=f'Group {(i-1)//2 + 1}',
                games_total=0,
                games_won=0,
                games_percentage=0.0
            )
            db.session.add(team)
    
    db.session.commit()  # Commit to get IDs for the teams
    
    # Create schedule data
    start_date = datetime.now()
    for division in divisions:
        teams = Appointable.query.filter_by(division=division).all()
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                # Create a match between team[i] and team[j]
                deadline = start_date + timedelta(days=(7 * (i + j)))
                schedule = Schedule(
                    team1=teams[i].team,
                    team2=teams[j].team,
                    deadline=deadline,
                    division=division
                )
                db.session.add(schedule)
    
    db.session.commit()

if __name__ == '__main__':
    from flask import Flask
    from database import init_db
    
    app = Flask(__name__)
    init_db(app)
    
    with app.app_context():
        seed_database() 