import os
from app import app, db

def reset_database():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Recreate upload directories
        os.makedirs(os.path.join('static', 'uploads', 'samples'), exist_ok=True)
        os.makedirs(os.path.join('static', 'uploads', 'measurements'), exist_ok=True)
        
        print("Database has been reset successfully!")

if __name__ == '__main__':
    reset_database()
