from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, init_db, User, Appointable
from models.seed_data import seed_database
from routes import init_routes
import os

def create_app():
    # Debug: print the resolved path to tpl.db
    print('DEBUG: Current working directory:', os.getcwd())
    print('DEBUG: __file__:', __file__)
    print('DEBUG: tpl.db expected at:', os.path.join(os.getcwd(), 'tpl.db'))
    app = Flask(__name__)
    migrate = Migrate(app, db)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tpl.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the database
    init_db(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize routes
    init_routes(app)
    
    # Create admin user if it doesn't exist
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')  # Change this to a secure password
            db.session.add(admin)
            db.session.commit()
    
    return app

app = create_app()

# Create database tables and seed with initial data if empty
with app.app_context():
    try:
        if not Appointable.query.first():
            seed_database()
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == '__main__':
    app.run(debug=True)