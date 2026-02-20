from app import app, db

def check_and_fix_advance_amount():
    with app.app_context():
        # Check if the column exists
        try:
            # Try to query the advance_amount column
            db.session.execute('SELECT advance_amount FROM saved_measurement LIMIT 1')
            print("advance_amount column exists in saved_measurement table")
        except Exception as e:
            print("advance_amount column does not exist. Adding it now...")
            try:
                # Add the column
                db.session.execute('ALTER TABLE saved_measurement ADD COLUMN advance_amount FLOAT DEFAULT 0.0')
                db.session.commit()
                print("Successfully added advance_amount column")
            except Exception as e:
                print(f"Error adding column: {str(e)}")
                db.session.rollback()
        
        # Verify the column exists
        try:
            result = db.session.execute('SELECT advance_amount FROM saved_measurement LIMIT 1')
            print("Verification: Column exists and is accessible")
            print(f"Sample value: {result.fetchone()}")
        except Exception as e:
            print(f"Verification failed: {str(e)}")

if __name__ == '__main__':
    check_and_fix_advance_amount()
