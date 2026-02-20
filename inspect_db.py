import sqlite3
import os

def check_db():
    db_path = 'instance/cloth.db'
    
    if not os.path.exists(db_path):
        print(f"Database file not found at: {os.path.abspath(db_path)}")
        print("Current working directory:", os.getcwd())
        print("Files in current directory:", os.listdir('.'))
        if os.path.exists('instance'):
            print("Files in instance directory:", os.listdir('instance'))
        return
    
    try:
        print(f"\nChecking database at: {os.path.abspath(db_path)}")
        print("-" * 50)
        
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
            for col in columns:
                print(f"- {col[1]} ({col[2]})")
            
            print("\nCustomer data:")
            cursor.execute("SELECT * FROM customer")
            customers = cursor.fetchall()
            if customers:
                for idx, customer in enumerate(customers, 1):
                    print(f"\nCustomer {idx}:")
                    for col, value in zip(columns, customer):
                        print(f"  {col[1]}: {value}")
            else:
                print("No customer records found in the database.")
        
    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_db()
