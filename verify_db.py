from app import create_app, db
from models import Customer

app = create_app()

with app.app_context():
    # Check if the customer table exists
    inspector = db.inspect(db.engine)
    if 'customer' in inspector.get_table_names():
        print("Customer table exists. Checking contents...")
        customers = Customer.query.all()
        if customers:
            print("\nCustomers in database:")
            print("-" * 50)
            for customer in customers:
                print(f"ID: {customer.id}")
                print(f"Name: {customer.name}")
                print(f"Email: {customer.email}")
                print(f"Phone: {customer.phone}")
                print(f"User ID: {customer.user_id}")
                print("-" * 50)
        else:
            print("No customers found in the database.")
    else:
        print("Customer table does not exist in the database.")
    
    # Print the database URL for reference
    print(f"\nDatabase URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Database file exists: {os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))}")
