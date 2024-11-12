from app import create_app, db  # Import your app factory and db instance

from sqlalchemy import inspect

app = create_app()  # Create an instance of your app

# Use the app context to execute code that requires it
with app.app_context():
    # Print all table names
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")
