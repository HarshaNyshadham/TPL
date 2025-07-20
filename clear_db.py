from app import app
from models import db, Player, Season, Schedule, Appointable

def clear_database():
    with app.app_context():
        try:
            # Delete all records from tables
            Schedule.query.delete()
            Appointable.query.delete()
            Player.query.delete()
            Season.query.delete()
            
            # Commit the changes
            db.session.commit()
            print("Database cleared successfully!")
        except Exception as e:
            print(f"Error clearing database: {e}")
            db.session.rollback()

if __name__ == "__main__":
    clear_database() 