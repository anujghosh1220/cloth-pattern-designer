from app import app, db

def add_advance_amount_column():
    with app.app_context():
        # Check if the column already exists
        inspector = db.inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('saved_measurement')]
        
        if 'advance_amount' not in columns:
            # Add the column
            db.engine.execute('ALTER TABLE saved_measurement ADD COLUMN advance_amount FLOAT DEFAULT 0.0')
            print("Successfully added advance_amount column to saved_measurement table")
        else:
            print("advance_amount column already exists in saved_measurement table")

if __name__ == '__main__':
    add_advance_amount_column()
