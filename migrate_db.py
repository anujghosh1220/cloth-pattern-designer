from app import create_app, db

def migrate_database():
    app = create_app()
    with app.app_context():
        # This will create all tables that don't exist yet
        db.create_all()
        print("Database migration completed successfully!")

if __name__ == '__main__':
    migrate_database()
