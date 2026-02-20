from app import create_app, db
from models import Customer

app = create_app()

with app.app_context():
    # Get all customers
    customers = Customer.query.all()
    
    if not customers:
        print("No customers found in the database.")
    else:
        print("\nCustomers in database:")
        print("-" * 50)
        for idx, customer in enumerate(customers, 1):
            print(f"Customer {idx}:")
            print(f"  ID: {customer.id}")
            print(f"  Name: {customer.name}")
            print(f"  Email: {customer.email}")
            print(f"  Phone: {customer.phone}")
            print(f"  Created: {customer.created_at}")
            print("-" * 50)
