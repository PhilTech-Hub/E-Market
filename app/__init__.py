# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate  # Import Migrate
from app.models import User # Import your User model
from .routes import auth  # Make sure you don't accidentally import `register` here


class Base(DeclarativeBase):
  pass
# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()  # Initialize Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'ecommerce.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['DEBUG'] = True  
    app.register_blueprint(auth, url_prefix='/auth')  # Register the blueprint with a prefix if needed


    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with app and db
    
    
    
    
    # Import routes and models
    #from app.routes import main, auth
    from .routes import register_routes
    # Register routes
    register_routes(app)
    # app.register_blueprint(main)
    # app.register_blueprint(auth)

    

    # Setup login manager
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    
    
    


    return app
