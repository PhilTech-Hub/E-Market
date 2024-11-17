from app import create_app, db
from flask_bcrypt import Bcrypt  # Import Bcrypt separately
from app.models import User

# Initialize the app and Bcrypt
app = create_app()  # Assuming create_app is your function to initialize the app
bcrypt = Bcrypt(app)

def rehash_passwords():
    with app.app_context():  # Use the app context here
        users = User.query.all()
        print(f"Found {len(users)} users.")
        
        for user in users:
            if user.password:
                print(f"Rehashing password for: {user.username}")
                user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')
                db.session.commit()

        print("All passwords have been rehashed.")

if __name__ == "__main__":
    rehash_passwords()
