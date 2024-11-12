# app/__init__.py
import os
from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate  # Import Migrate
from config import Config

# from app.routes.auth import auth  # Import the blueprint, not the module

class Base(DeclarativeBase):
  pass
# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()  # Initialize Migrate
db_path = os.path.join(os.getcwd(), 'instance', 'ecommerce.db')
print(f"Database path: {db_path}")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'adb9decb06425cc8149d7438be15a4bfd362728eb66d72059da0ac02013aee25')
    app.config['DEBUG'] = True  
    app.config.from_object(Config)
    csrf = CSRFProtect(app)  # Enable CSRF protection
    # app.register_blueprint(auth, url_prefix='/auth')  # Register the blueprint with a prefix if needed


    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with app and db
    
    
    
    from app.models import User, Product, Sales, Admin  # Ensure models are imported
    
    # Import and register your blueprints after initializing the app
    # from .routes.auth import auth
    # app.register_blueprint(auth, url_prefix='/auth')
    
    # Import routes and models
    #from app.routes import main, auth
    # from .routes.auth import register_routes
    from app.routes import register_routes

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
  
  
