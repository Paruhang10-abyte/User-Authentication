from db import SessionLocal
from model import User
from utils import pwd_context

def migrate_passwords():
    # Create a new database session
    db = SessionLocal()
    try:
        # Fetch all users from the database
        users = db.query(User).all()
        
        # Loop through each user
        for user in users:
            # Check if the password is already a bcrypt hash
            # Bcrypt hashes always start with "$2b$"
            if not user.password.startswith("$2b$"):
                print(f"Migrating {user.email}")  # Log which user is being updated
                # Replace plain text password with a bcrypt hash
                user.password = pwd_context.hash(user.password)
        
        # Save all changes to the database
        db.commit()
        print("Migration complete!")  # Confirmation message
    finally:
        # Always close the session to free resources
        db.close()

# Run migration only if this file is executed directly
if __name__ == "__main__":
    migrate_passwords()
