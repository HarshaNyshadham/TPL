from datetime import datetime, timedelta
from .database import db
from .appointable import Appointable, Season
from .schedule import Schedule

def seed_database():
    """Seed the database with initial data"""
    # Clear existing data
    Schedule.query.delete()
    Appointable.query.delete()
    Season.query.delete()
    
    # Create current season
    current_season = Season(
        name="Spring 2024",
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=90),
        is_active=True
    )
    db.session.add(current_season)
    db.session.commit()
    
    # Teams data structure by game type
    division_teams = {
        'singles': {
            5.0: {
                'A': [
                    'Lee & Andrew',
                    'Pankaj & Akshay',
                    'Carlos / Jorge',
                    'Chavel & Randy',
                    'Arun & Naveen'
                ],
                'B': [
                    'Nihar & Vatsalya',
                    'Ramana & Harpreet',
                    'Bin & Hong',
                    'David & Nirav Patel',
                    'Eric Salgado & Aaron'
                ]
            },
            4.5: {
                'A': [
                    'Puneet & Harpreet',
                    'Max Bough&Pruthvi',
                    'Adil and Mubashir',
                    'Jesus & Juan Ferrer',
                    'Madhu & Shamanth'
                ],
                'B': [
                    'Gurpreet/Shashank',
                    'Gunjan and Sanmay',
                    'Kyle and Carlos Chacin',
                    'Anil & Nikhil',
                    'Amol Bavare&Amol Phadke'
                ]
            },
            4.0: {
                'A': [
                    'Chengwei and Ravindra Singh (NP)',
                    'Surya & Srikanth',
                    'David Clerc&Diego Clerc',
                    'Vittal and Mouli',
                    'Sunil & Rohit Mahapatra'
                ],
                'B': [
                    'Dev and Gautam',
                    'Praveen & Mahesh',
                    'Sam P & Pawan S',
                    'Anand & Dnyanesh',
                    'Juan & Rohit'
                ]
            }
        },
        'doubles': {
            5.0: {
                'A': [
                    'Lee/Andrew Team',
                    'Pankaj/Akshay Team',
                    'Carlos/Jorge Team',
                    'Chavel/Randy Team'
                ],
                'B': [
                    'Nihar/Vatsalya Team',
                    'Ramana/Harpreet Team',
                    'Bin/Hong Team',
                    'David/Nirav Team'
                ]
            },
            4.5: {
                'A': [
                    'Puneet/Harpreet Team',
                    'Max/Pruthvi Team',
                    'Adil/Mubashir Team',
                    'Jesus/Juan Team'
                ],
                'B': [
                    'Gurpreet/Shashank Team',
                    'Gunjan/Sanmay Team',
                    'Kyle/Carlos Team',
                    'Anil/Nikhil Team'
                ]
            }
        },
        'mixed_doubles': {
            5.0: {
                'A': [
                    'Lee/Sarah Team',
                    'Pankaj/Maria Team',
                    'Carlos/Ana Team',
                    'Chavel/Emma Team'
                ],
                'B': [
                    'Nihar/Lisa Team',
                    'Ramana/Julia Team',
                    'Bin/Sophie Team',
                    'David/Rachel Team'
                ]
            },
            4.5: {
                'A': [
                    'Puneet/Amy Team',
                    'Max/Kate Team',
                    'Adil/Jane Team',
                    'Jesus/Laura Team'
                ],
                'B': [
                    'Gurpreet/Nina Team',
                    'Gunjan/Maya Team',
                    'Kyle/Zoe Team',
                    'Anil/Eva Team'
                ]
            }
        }
    }
    
    # Seed Appointable data
    for game_type, divisions in division_teams.items():
        for division, groups in divisions.items():
            for group, teams in groups.items():
                for team_name in teams:
                    team = Appointable(
                        team=team_name,
                        division=division,
                        matches=0,
                        won=0,
                        loss=0,
                        bonus=0,
                        points=0,
                        group=group,
                        games_total=0,
                        games_won=0,
                        games_percentage=0.0,
                        game_type=game_type,
                        season_id=current_season.id
                    )
                    db.session.add(team)
    
    db.session.commit()
    
    # Create schedule data
    start_date = datetime.now()
    for game_type, divisions in division_teams.items():
        for division in divisions.keys():
            teams = Appointable.query.filter_by(
                division=division,
                game_type=game_type,
                season_id=current_season.id
            ).all()
            
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    # Only create matches between teams in the same group
                    if teams[i].group == teams[j].group:
                        deadline = start_date + timedelta(days=(7 * (i + j)))
                        schedule = Schedule(
                            team1=teams[i].team,
                            team2=teams[j].team,
                            deadline=deadline,
                            division=division,
                            game_type=game_type,
                            season_id=current_season.id
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