import sqlite3
import os

def check_db():
    db_path = 'instance/cloth.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {os.path.abspath(db_path)}")
        return
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("\nTables in database:")
        for table in tables:
            print(f"- {table[0]}")
        
        # Check customer table
        if ('customer',) in tables:
            print("\nCustomer table structure:")
            cursor.execute("PRAGMA table_info(customer)")
            columns = cursor.fetchall()
            print("Columns in customer table:")
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
            
            # Get customer data
            cursor.execute("SELECT * FROM customer")
            customers = cursor.fetchall()
            print(f"\nFound {len(customers)} customers:")
            for customer in customers:
                print("\nCustomer:")
                for col, value in zip(columns, customer):
                    print(f"  {col[1]}: {value}")
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_db()
