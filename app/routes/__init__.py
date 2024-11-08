from flask import Blueprint  # noqa: F401



# Initialize Blueprint for the app
def register_routes(app):
    # Import routes from other files
    from .auth import auth  # noqa
    from .main import main  # noqa
    # Register blueprints for auth and main routes
    app.register_blueprint(auth)
    app.register_blueprint(main)
