from app import create_app, db
from models import Customer

app = create_app()

with app.app_context():
    try:
        # Get all customers
        customers = Customer.query.all()
        print(f"Found {len(customers)} customers")
        
        # Print each customer's details
        for customer in customers:
            print(f"ID: {customer.id}")
            print(f"Name: {customer.name}")
            print(f"Email: {customer.email}")
            print(f"Phone: {customer.phone}")
            print(f"Created At: {customer.created_at}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")
        
    # Also print raw SQL query for debugging
    try:
        print("\nRaw SQL Query:")
        print(str(Customer.query))
    except Exception as e:
        print(f"Error getting raw query: {e}")
