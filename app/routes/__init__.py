from flask import Blueprint  # noqa: F401




# app/routes/auth.py
__all__ = ['auth']  # Optional, to specify exports explicitly

# Initialize Blueprint for the app
def register_routes(app):
    # Import routes from other files
    from app.routes.auth import auth  
    from app.routes.main import main  
    # Register blueprints for auth and main routes
    app.register_blueprint(auth)
    app.register_blueprint(main)
