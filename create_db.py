# create_db.py

from app import create_app, db

# Create a Flask app instance
app = create_app()

# Use the application context to run db.create_all() within the context
with app.app_context():
    db.create_all()

print("Database created successfully!")
