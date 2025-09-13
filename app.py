import os
import time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64
import json
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    return app

app = create_app()

def init_db():
    with app.app_context():
        # Create uploads directory if it doesn't exist
        os.makedirs(os.path.join('static', 'uploads', 'samples'), exist_ok=True)
        os.makedirs(os.path.join('static', 'uploads', 'measurements'), exist_ok=True)
        os.makedirs(os.path.join('static', 'uploads', 'audio'), exist_ok=True)
        
        # Create all tables if they don't exist
        db.create_all()
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        print("Tables in database:", inspector.get_table_names())
        
        # Verify customer table columns
        if 'customer' in inspector.get_table_names():
            print("Customer table columns:", [col['name'] for col in inspector.get_columns('customer')])
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin2214')
            db.session.add(admin)
            db.session.commit()
            print("Created admin user")
        else:
            print("Admin user already exists")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BlousePattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    measurements = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text)
    total_amount = db.Column(db.Float, default=0.0)  # Total amount across all orders
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                         onupdate=db.func.current_timestamp())
    
    # Relationships
    orders = db.relationship('Order', back_populates='customer_obj', lazy=True, cascade='all, delete-orphan')
    measurements = db.relationship('SavedMeasurement', back_populates='customer_obj', lazy=True, 
                                 cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Customer {self.name}>'

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    advance_amount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    category = db.Column(db.String(50), default='blouse')  # Add category field
    notes = db.Column(db.Text)
    order_date = db.Column(db.Date, nullable=False, default=datetime.now().date)
    delivery_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                         onupdate=db.func.current_timestamp())
    
    # Relationships
    customer_obj = db.relationship('Customer', back_populates='orders')
    measurements = db.relationship('SavedMeasurement', back_populates='order', lazy=True, 
                                 cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'

class SavedMeasurement(db.Model):
    __tablename__ = 'saved_measurement'
    
    # Primary key and foreign keys
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)  # Optional for now, will be required later
    
    # Relationships
    customer_obj = db.relationship('Customer', back_populates='measurements')
    order = db.relationship('Order', back_populates='measurements')
    
    # Basic info
    category = db.Column(db.String(20), nullable=False, default='blouse')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                         onupdate=db.func.current_timestamp())
    image_path = db.Column(db.String(255), nullable=True)
    
    # Common measurements
    length = db.Column(db.Float, nullable=True)
    across_shoulder = db.Column(db.Float, nullable=True)
    upper_chest = db.Column(db.Float, nullable=True)
    chest = db.Column(db.Float, nullable=True)
    
    # Payment information
    advance_amount = db.Column(db.Float, nullable=True, default=0.0)
    waist = db.Column(db.Float, nullable=True)
    
    # Blouse & Kurti specific
    front_neck_depth = db.Column(db.Float, nullable=True)
    back_neck_depth = db.Column(db.Float, nullable=True)
    sleeve_length = db.Column(db.Float, nullable=True)
    armhole = db.Column(db.Float, nullable=True)
    biceps = db.Column(db.Float, nullable=True)
    sleeve_cuff = db.Column(db.Float, nullable=True)
    shoulder_apex = db.Column(db.Float, nullable=True)  # Blouse only
    
    # Lehenga & Pant specific
    hip = db.Column(db.Float, nullable=True)
    waist_floor = db.Column(db.Float, nullable=True)  # Lehenga & Pant
    belt = db.Column(db.Float, nullable=True)  # Lehenga & Pant
    
    # Pant specific
    waist_ankle = db.Column(db.Float, nullable=True)  # Pant only
    thigh = db.Column(db.Float, nullable=True)  # Pant only
    ankle = db.Column(db.Float, nullable=True)  # Pant only
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    
    # Order and delivery dates
    order_date = db.Column(db.Date, nullable=True)
    delivery_date = db.Column(db.Date, nullable=True)
    
    # Audio recording
    audio_path = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<SavedMeasurement {self.id} - {self.category}>'

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.username != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/orders', methods=['POST'])
@login_required
def create_order():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        amount = float(data.get('amount', 0))
        advance_amount = float(data.get('advance_amount', 0))
        category = data.get('category', 'blouse')
        
        if not customer_id:
            return jsonify({'error': 'Customer ID is required'}), 400
        
        # Get the customer
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({'error': 'Customer not found'}), 404
            
        # Always create a new order
        order = Order(
            user_id=current_user.id,
            customer_id=customer_id,
            amount=amount,
            advance_amount=advance_amount,
            status='pending',
            order_date=datetime.now().date(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            category=category
        )
        db.session.add(order)
        
        # Commit the order without updating customer's total amount
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'message': 'Order saved successfully',
            'order': {
                'id': order.id,
                'amount': order.amount,
                'advance_amount': order.advance_amount,
                'status': order.status,
                'category': order.category,
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'delivery_date': order.delivery_date.isoformat() if order.delivery_date else None
            }
        }), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': 'Invalid amount or advance amount'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error creating order: {str(e)}')
        return jsonify({'error': 'Failed to create order'}), 500

# Pattern Generation Functions
def bezier(p0, p1, p2, n=50):
    t = np.linspace(0, 1, n)
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t**2*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t**2*p2[1]
    return x, y

def generate_pattern_image(measurements, pattern_type='all'):
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Sample pattern generation (simplified from original code)
    # This is a placeholder - you'll need to adapt the actual pattern generation code
    if pattern_type == 'front' or pattern_type == 'all':
        # Front pattern
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y, 'r-', label='Front')
    
    if pattern_type == 'back' or pattern_type == 'all':
        # Back pattern
        x = np.linspace(0, 10, 100)
        y = np.cos(x)
        ax.plot(x, y, 'b-', label='Back')
    
    if pattern_type == 'sleeve' or pattern_type == 'all':
        # Sleeve pattern
        x = np.linspace(0, 10, 100)
        y = np.sin(x) * 0.5 + 2
        ax.plot(x, y, 'g-', label='Sleeve')
    
    ax.set_title('Cloth Pattern')
    ax.legend()
    ax.grid(True)
    
    # Save plot to a bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    # Convert to base64 for embedding in HTML
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"

# API Endpoints
@app.route('/api/save_measurements', methods=['POST'])
@login_required
def save_measurements():
    print("\n=== Received form data ===")
    print("Form data:", request.form)
    print("Files:", request.files)
    
    if request.content_type and 'multipart/form-data' in request.content_type:
        measurements = {}
        # Get all form data
        for key, value in request.form.items():
            if key != 'measurements':
                measurements[key] = value
        
        # If there's a measurements JSON string, update with its contents
        if 'measurements' in request.form:
            try:
                measurements.update(json.loads(request.form['measurements']))
            except json.JSONDecodeError:
                print("Failed to parse measurements JSON")
        
        print("Parsed measurements:", measurements)
        
        image_path = None
        if 'cloth_image' in request.files:
            file = request.files['cloth_image']
            if file.filename != '' and allowed_file(file.filename):
                # Create the upload directory if it doesn't exist
                upload_dir = os.path.join('static', 'uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate a unique filename
                filename = secure_filename(f"{current_user.id}_{int(time.time())}_{file.filename}")
                filepath = os.path.join(upload_dir, filename)
                
                # Save the file
                file.save(filepath)
                
                # Store the relative path for the database
                image_path = os.path.join('uploads', filename).replace('\\', '/')
    else:
        measurements = request.get_json()
    
    category = measurements.get('category', 'blouse')
    
    # Get customer_id from the form data or JSON
    customer_id = None
    if request.is_json and 'customer_id' in measurements:
        customer_id = measurements.get('customer_id')
    elif 'customer_id' in request.form:
        customer_id = request.form.get('customer_id')
    
    if not customer_id:
        return jsonify({
            'status': 'error',
            'message': 'Customer ID is required'
        }), 400
    
    # Verify the customer exists and belongs to the current user
    customer = Customer.query.filter_by(id=customer_id, user_id=current_user.id).first()
    if not customer:
        return jsonify({
            'status': 'error',
            'message': 'Invalid customer ID or unauthorized access'
        }), 403
    
    # Get amount and advance amount from the form data
    amount = float(measurements.get('amount', 0.0))
    advance_amount = float(measurements.get('advance_amount', 0.0))
    
    # Get order date from form data or use current date
    order_date = measurements.get('order_date')
    if order_date:
        try:
            order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            order_date = datetime.now().date()
    else:
        order_date = datetime.now().date()
    
    # Always create a new order for each measurement
    order = Order(
        user_id=current_user.id,
        customer_id=customer_id,
        amount=amount if amount > 0 else 0.0,
        advance_amount=advance_amount if advance_amount > 0 else 0.0,
        status='pending',
        category=category,
        order_date=order_date,
        delivery_date=datetime.strptime(measurements.get('delivery_date'), '%Y-%m-%d').date() if measurements.get('delivery_date') else None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(order)
    
    # Commit the order first to ensure we have an ID
    db.session.commit()
    
    # Create new measurement with basic info and link to the order
    measurement = SavedMeasurement(
        user_id=current_user.id,
        customer_id=customer_id,
        order_id=order.id,  # Link to the order
        category=category,
        image_path=image_path,
        created_at=datetime.utcnow()
    )
    
    # Define all possible measurement fields
    all_measurement_fields = [
        'length', 'across_shoulder', 'upper_chest', 'chest', 'waist',
        'front_neck_depth', 'back_neck_depth', 'sleeve_length',
        'armhole', 'biceps', 'sleeve_cuff', 'shoulder_apex',
        'hip', 'waist_floor', 'belt', 'waist_ankle', 'thigh', 'ankle',
        'advance_amount'  # Added advance_amount to the list of fields to process
    ]
    
    # Process all measurement fields from the form data
    for field in all_measurement_fields:
        if field in measurements and measurements[field] not in (None, ''):
            try:
                # Convert to float if it's a string that can be converted
                value = measurements[field]
                if isinstance(value, str):
                    value = float(value) if value.strip() else None
                setattr(measurement, field, value)
            except (ValueError, TypeError) as e:
                print(f"Warning: Could not convert {field} value '{measurements[field]}' to float: {e}")
                setattr(measurement, field, None)
        else:
            setattr(measurement, field, None)
    
    # Process order and delivery dates
    if 'order_date' in measurements and measurements['order_date']:
        try:
            measurement.order_date = datetime.strptime(measurements['order_date'], '%Y-%m-%d').date()
        except (ValueError, TypeError) as e:
            print(f"Warning: Could not parse order_date '{measurements['order_date']}': {e}")
    
    if 'delivery_date' in measurements and measurements['delivery_date']:
        try:
            measurement.delivery_date = datetime.strptime(measurements['delivery_date'], '%Y-%m-%d').date()
        except (ValueError, TypeError) as e:
            print(f"Warning: Could not parse delivery_date '{measurements['delivery_date']}': {e}")
    
    db.session.add(measurement)
    
    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Measurements saved successfully',
            'measurement_id': measurement.id,
            'category': measurement.category
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Error saving measurements: {str(e)}'
        }), 500

@app.route('/api/measurements', methods=['GET'])
@login_required
def get_measurements():
    measurements = SavedMeasurement.query.filter_by(user_id=current_user.id).order_by(SavedMeasurement.created_at.desc()).all()
    
    def measurement_to_dict(m):
        # Base measurement data
        measurement_data = {
            'id': m.id,
            'category': m.category,
            'image_path': m.image_path,
            'created_at': m.created_at.isoformat() if m.created_at else None
        }
        
        # Common fields for all categories
        common_fields = [
            'length', 'across_shoulder', 'upper_chest', 'chest', 'waist',
            'front_neck_depth', 'back_neck_depth', 'sleeve_length',
            'armhole', 'biceps', 'sleeve_cuff', 'shoulder_apex',
            'hip', 'waist_floor', 'belt', 'waist_ankle', 'thigh', 'ankle'
        ]
        
        # Add common fields
        for field in common_fields:
            value = getattr(m, field, None)
            if value is not None:
                measurement_data[field] = value
        
        # Add category-specific fields
        category = m.category
        if category == 'blouse' and hasattr(m, 'shoulder_apex') and m.shoulder_apex is not None:
            measurement_data['shoulder_apex'] = m.shoulder_apex
        
        elif category == 'kurti' and hasattr(m, 'hip') and m.hip is not None:
            measurement_data['hip'] = m.hip
        
        elif category == 'lehenga':
            if m.hip is not None:
                measurement_data['hip'] = m.hip
            if m.waist_floor is not None:
                measurement_data['waist_floor'] = m.waist_floor
            if m.belt is not None:
                measurement_data['belt'] = m.belt
        
        elif category == 'pant':
            if m.hip is not None:
                measurement_data['hip'] = m.hip
            if m.waist_ankle is not None:
                measurement_data['waist_ankle'] = m.waist_ankle
            if m.waist_floor is not None:
                measurement_data['waist_floor'] = m.waist_floor
            if m.belt is not None:
                measurement_data['belt'] = m.belt
            if m.thigh is not None:
                measurement_data['thigh'] = m.thigh
            if m.ankle is not None:
                measurement_data['ankle'] = m.ankle
        
        return measurement_data
    
    return jsonify([measurement_to_dict(m) for m in measurements])

@app.route('/api/measurements/<int:measurement_id>', methods=['GET'])
@login_required
def get_measurement(measurement_id):
    measurement = SavedMeasurement.query.filter_by(id=measurement_id, user_id=current_user.id).first_or_404()
    
    # Start with basic measurement data
    measurement_data = {
        'id': measurement.id,
        'category': measurement.category,
        'image_path': measurement.image_path,
        'created_at': measurement.created_at.isoformat() if measurement.created_at else None
    }
    
    # Common fields for all categories
    common_fields = [
        'length', 'across_shoulder', 'upper_chest', 'chest', 'waist',
        'front_neck_depth', 'back_neck_depth', 'sleeve_length',
        'armhole', 'biceps', 'sleeve_cuff'
    ]
    
    # Add common fields
    for field in common_fields:
        measurement_data[field] = getattr(measurement, field, None)
    
    # Add category-specific fields
    if measurement.category == 'blouse':
        measurement_data['shoulder_apex'] = measurement.shoulder_apex
    elif measurement.category == 'kurti':
        measurement_data['hip'] = measurement.hip
    elif measurement.category == 'lehenga':
        measurement_data.update({
            'hip': measurement.hip,
            'waist_floor': measurement.waist_floor,
            'belt': measurement.belt
        })
    elif measurement.category == 'pant':
        measurement_data.update({
            'hip': measurement.hip,
            'waist_ankle': measurement.waist_ankle,
            'waist_floor': measurement.waist_floor,
            'belt': measurement.belt,
            'thigh': measurement.thigh,
            'ankle': measurement.ankle
        })
    
    # Remove None values
    measurement_data = {k: v for k, v in measurement_data.items() if v is not None}
    
    return jsonify(measurement_data)

# Admin routes
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Serve uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Convert any backslashes to forward slashes for URL compatibility
    filename = filename.replace('\\', '/')
    return send_from_directory('static/uploads', filename)

@app.route('/my-measurements')
@login_required
def my_measurements():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Get current user's customers with their measurements
    customers = Customer.query.filter_by(
        user_id=current_user.id
    ).options(
        db.joinedload(Customer.measurements)
        .joinedload(SavedMeasurement.customer)
        .load_only('name', 'phone', 'email')
    ).order_by(Customer.name).all()
    
    # Organize measurements by customer
    customer_data = []
    for customer in customers:
        if customer.measurements:  # Only include customers with measurements
            customer_measurements = sorted(
                customer.measurements,
                key=lambda m: m.created_at,
                reverse=True
            )
            customer_data.append({
                'id': customer.id,
                'name': customer.name,
                'phone': customer.phone,
                'email': customer.email,
                'measurements': customer_measurements,
                'measurement_count': len(customer_measurements)
            })
    
    return render_template('my_measurements.html', customers=customer_data)

@app.route('/customers')
@login_required
def customers():
    # Get all customers for the current user
    customers = Customer.query.filter_by(user_id=current_user.id).order_by(Customer.name).all()
    return render_template('customers.html', customers=customers)

@app.route('/customer/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        try:
            # Handle both form data and JSON
            if request.is_json:
                data = request.get_json()
                name = data.get('name')
                email = data.get('email')
                phone = data.get('phone')
                address = data.get('address')
            else:
                name = request.form.get('name')
                email = request.form.get('email')
                phone = request.form.get('phone')
                address = request.form.get('address')

            print(f"Received customer data - Name: {name}, Email: {email}")  # Debug log

            # Validate required fields
            if not name or not email:
                flash('Name and email are required fields.', 'error')
                if request.is_json:
                    return jsonify({'success': False, 'error': 'Name and email are required'}), 400
                return redirect(url_for('add_customer'))

            # Check if email already exists
            existing_customer = Customer.query.filter_by(email=email).first()
            if existing_customer:
                error_msg = 'A customer with this email already exists.'
                flash(error_msg, 'error')
                if request.is_json:
                    return jsonify({'success': False, 'error': error_msg}), 400
                return redirect(url_for('add_customer'))
                
            # Check if phone number already exists
            if phone:  # Only check if phone is provided
                existing_phone = Customer.query.filter_by(phone=phone).first()
                if existing_phone:
                    error_msg = 'This phone number is already registered with another customer.'
                    flash(error_msg, 'error')
                    if request.is_json:
                        return jsonify({'success': False, 'error': error_msg}), 400
                    return redirect(url_for('add_customer'))

            # Create new customer
            customer = Customer(
                user_id=current_user.id,
                name=name,
                email=email,
                phone=phone,
                address=address
            )

            db.session.add(customer)
            db.session.commit()
            print(f"Customer created successfully with ID: {customer.id}")  # Debug log

            if request.is_json:
                return jsonify({
                    'success': True, 
                    'message': 'Customer added successfully',
                    'customer_id': customer.id
                })

            flash('Customer added successfully!', 'success')
            return redirect(url_for('customers'))

        except Exception as e:
            db.session.rollback()
            error_msg = f'Error adding customer: {str(e)}'
            print(error_msg)  # Debug log
            if request.is_json:
                return jsonify({'success': False, 'error': error_msg}), 500
            flash(error_msg, 'error')
            return redirect(url_for('add_customer'))

    return render_template('add_customer.html')

@app.route('/customer/<int:customer_id>/update_payment', methods=['POST'])
@login_required
def update_customer_payment(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        
        # Ensure the customer belongs to the current user
        if customer.user_id != current_user.id:
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
            
        # Get the latest measurement for this customer
        latest_measurement = SavedMeasurement.query.filter_by(
            customer_id=customer.id
        ).order_by(SavedMeasurement.created_at.desc()).first()
        
        if latest_measurement:
            # Update the advance amount to be equal to the total amount
            if customer.total_amount:
                latest_measurement.advance_amount = float(customer.total_amount)
                db.session.commit()
                return jsonify({
                    'success': True,
                    'message': 'Payment marked as paid successfully',
                    'advance_amount': float(customer.total_amount)
                })
        
        return jsonify({'success': False, 'error': 'No measurement found for this customer'}), 404
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating payment status: {str(e)}')
        return jsonify({'success': False, 'error': 'Failed to update payment status'}), 500

@app.route('/customer/search')
@login_required
def search_customer():
    phone = request.args.get('phone')
    if not phone:
        return jsonify({'message': 'Phone number is required'}), 400
        
    try:
        # Search for customer by phone (case-insensitive, partial match)
        customer = Customer.query.filter(
            Customer.phone.ilike(f'%{phone}%'),
            Customer.user_id == current_user.id
        ).first()
        
        if customer:
            # Get all orders for this customer
            orders = Order.query.filter_by(
                customer_id=customer.id
            ).order_by(Order.created_at.desc()).all()
            
            # Calculate total amount and get the latest advance amount
            total_amount = sum(float(order.amount or 0) for order in orders)
            
            # Get the latest measurement's advance amount if it exists
            latest_measurement = SavedMeasurement.query.filter_by(
                customer_id=customer.id
            ).order_by(SavedMeasurement.created_at.desc()).first()
            
            advance_amount = 0.0
            if latest_measurement and hasattr(latest_measurement, 'advance_amount'):
                advance_amount = float(latest_measurement.advance_amount) if latest_measurement.advance_amount is not None else 0.0
            
            # Get the latest order for display
            latest_order = orders[0] if orders else None
            
            # Prepare orders data
            orders_data = [{
                'id': order.id,
                'amount': float(order.amount) if order.amount else 0.0,
                'advance_amount': float(order.advance_amount) if order.advance_amount else 0.0,
                'status': order.status,
                'category': order.category or 'general',
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'delivery_date': order.delivery_date.isoformat() if order.delivery_date else None,
                'created_at': order.created_at.isoformat() if order.created_at else None
            } for order in orders]
            
            return jsonify({
                'customer': {
                    'id': customer.id,
                    'name': customer.name,
                    'email': customer.email,
                    'phone': customer.phone,
                    'address': customer.address,
                    'amount': total_amount,  # Total of all orders
                    'advance_amount': advance_amount,
                    'orders': orders_data,
                    'created_at': customer.created_at.isoformat() if customer.created_at else None,
                    'updated_at': customer.updated_at.isoformat() if customer.updated_at else None
                }
            })
        else:
            return jsonify({'message': 'Customer not found'}), 404
            
    except Exception as e:
        app.logger.error(f'Error searching for customer: {str(e)}')
        return jsonify({'error': 'An error occurred while searching for the customer'}), 500


@app.route('/customer/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    # Ensure the customer belongs to the current user
    if customer.user_id != current_user.id:
        flash('You are not authorized to edit this customer.', 'error')
        return redirect(url_for('customers'))

    if request.method == 'POST':
        new_email = request.form.get('email')
        new_phone = request.form.get('phone')
        
        # Check if email is being changed and already exists
        if new_email != customer.email:
            existing_email = Customer.query.filter_by(email=new_email).first()
            if existing_email:
                flash('A customer with this email already exists.', 'error')
                return render_template('edit_customer.html', customer=customer)
        
        # Check if phone is being changed and already exists
        if new_phone and new_phone != customer.phone:
            existing_phone = Customer.query.filter_by(phone=new_phone).first()
            if existing_phone:
                flash('This phone number is already registered with another customer.', 'error')
                return render_template('edit_customer.html', customer=customer)
        
        try:
            customer.name = request.form.get('name')
            customer.email = new_email
            customer.phone = new_phone
            customer.address = request.form.get('address')

            db.session.commit()
            flash('Customer updated successfully!', 'success')
            return redirect(url_for('customers'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating customer: {str(e)}', 'error')
            return render_template('edit_customer.html', customer=customer)

    return render_template('edit_customer.html', customer=customer)

@app.route('/customer/<int:customer_id>/amount', methods=['POST'])
@login_required
def update_customer_amount(customer_id):
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    total_amount = data.get('amount')
    
    if total_amount is None:
        return jsonify({'error': 'Amount is required'}), 400
    
    try:
        total_amount = float(total_amount)
        if total_amount < 0:
            return jsonify({'error': 'Amount cannot be negative'}), 400
            
        customer = Customer.query.get_or_404(customer_id)
        
        # Only update the customer's total amount
        customer.total_amount = total_amount
        
        # We don't modify any existing orders here
        # The order amount will be set when creating a new order in save_measurements
        
        db.session.commit()
        
        return jsonify({
            'message': 'Customer amount updated successfully',
            'amount': total_amount
        })
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/customer/<int:customer_id>/delete', methods=['POST'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)

    # Ensure the customer belongs to the current user
    if customer.user_id != current_user.id:
        flash('You are not authorized to delete this customer.', 'error')
        return redirect(url_for('customers'))

    db.session.delete(customer)
    db.session.commit()

    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('customers'))

@app.route('/admin/measurements')
@login_required
def admin_measurements():
    if not current_user.username == 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
        
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    user_id = request.args.get('user_id')
    query = SavedMeasurement.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    measurements = query.order_by(SavedMeasurement.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    users = User.query.all()
    
    return render_template('admin_measurements.html', measurements=measurements, users=users, selected_user=user_id)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.username == 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    if current_user.id == user_id:
        flash('You cannot delete your own account while logged in.', 'danger')
        return redirect(url_for('admin_users'))
    
    user = User.query.get_or_404(user_id)
    
    if user.username == 'admin':
        flash('Cannot delete the admin account.', 'danger')
        return redirect(url_for('admin_users'))
    
    try:
        # Delete all related data first (handled by cascade deletes in models)
        db.session.delete(user)
        db.session.commit()
        flash('User and all associated data have been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting user {user_id}: {str(e)}')
        flash('An error occurred while deleting the user.', 'danger')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/measurements/delete/<int:measurement_id>', methods=['POST'])
@login_required
def delete_measurement(measurement_id):
    if not current_user.is_authenticated or current_user.username != 'admin':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
    measurement = SavedMeasurement.query.get_or_404(measurement_id)
    db.session.delete(measurement)
    db.session.commit()
    
    flash('Measurement deleted successfully!', 'success')
    return jsonify({'success': True})

@app.route('/customer-measurements')
@login_required
def customer_measurements():
    phone = request.args.get('phone')
    
    # Base query with descending job numbers (most recent = 1)
    subquery = db.session.query(
        SavedMeasurement.id,
        db.func.row_number().over(
            order_by=db.desc(SavedMeasurement.created_at)
        ).label('row_num')
    ).filter(
        SavedMeasurement.user_id == current_user.id
    ).subquery()
    
    query = db.session.query(
        SavedMeasurement,
        Customer,
        (db.func.count().over() - subquery.c.row_num + 1).label('job_number')
    ).join(
        Customer,
        SavedMeasurement.customer_id == Customer.id
    ).join(
        subquery,
        SavedMeasurement.id == subquery.c.id
    ).filter(
        SavedMeasurement.user_id == current_user.id
    )
    
    # Apply phone number filter if provided
    if phone:
        query = query.filter(Customer.phone.ilike(f'%{phone}%'))
    
    # Execute query
    measurements = query.order_by(SavedMeasurement.created_at.desc()).all()
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'success': True,
            'html': render_template('_measurement_rows.html', measurements=measurements)
        })
    
    return render_template('customer_measurements.html', measurements=measurements)

@app.route('/measurement/<int:measurement_id>/update_notes', methods=['POST'])
@login_required
def update_measurement_notes(measurement_id):
    data = request.get_json()
    if not data or 'notes' not in data:
        return jsonify({'error': 'Missing notes data'}), 400
    
    measurement = SavedMeasurement.query.get_or_404(measurement_id)
    if measurement.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Not authorized'}), 403
    
    try:
        measurement.notes = data['notes']
        db.session.commit()
        return jsonify({'success': True, 'message': 'Notes updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/measurement/<int:measurement_id>/json')
@login_required
def get_measurement_json(measurement_id):
    # Get the measurement with customer and order details
    measurement = db.session.query(
        SavedMeasurement,
        Customer,
        Order
    ).join(
        Customer,
        SavedMeasurement.customer_id == Customer.id
    ).outerjoin(
        Order,
        (SavedMeasurement.order_id == Order.id) & (Order.customer_id == Customer.id)
    ).filter(
        SavedMeasurement.id == measurement_id,
        SavedMeasurement.user_id == current_user.id
    ).first_or_404()
    
    # Get all measurement fields from the model
    measurement_fields = [
        'length', 'across_shoulder', 'upper_chest', 'chest', 'waist',
        'front_neck_depth', 'back_neck_depth', 'sleeve_length', 'armhole',
        'biceps', 'sleeve_cuff', 'shoulder_apex', 'hip', 'waist_floor',
        'belt', 'waist_ankle', 'thigh', 'ankle'
    ]
    
    # Convert to dictionary
    measurement_dict = {
        'id': measurement.SavedMeasurement.id,
        'customer_name': measurement.Customer.name,
        'customer_amount': measurement.Order.amount if measurement.Order else 0.0,
        'advance_amount': measurement.Order.advance_amount if measurement.Order and measurement.Order.advance_amount else 0.0,
        'category': measurement.SavedMeasurement.category,
        'created_at': measurement.SavedMeasurement.created_at.isoformat(),
        'updated_at': measurement.SavedMeasurement.updated_at.isoformat() if measurement.SavedMeasurement.updated_at else None,
        'order_date': (measurement.SavedMeasurement.order_date.isoformat() if measurement.SavedMeasurement.order_date 
                      else (measurement.Order.order_date.isoformat() if measurement.Order and measurement.Order.order_date 
                           else measurement.SavedMeasurement.created_at.date().isoformat())),
        'delivery_date': (measurement.SavedMeasurement.delivery_date.isoformat() if measurement.SavedMeasurement.delivery_date
                         else (measurement.Order.delivery_date.isoformat() 
                              if measurement.Order and measurement.Order.delivery_date else None)),
        'notes': measurement.SavedMeasurement.notes or '',
        'measurements': {}
    }
    
    # Add measurement fields
    for field in measurement_fields:
        value = getattr(measurement.SavedMeasurement, field, None)
        if value is not None:
            measurement_dict['measurements'][field] = float(value) if value is not None else None
    
    # Add image path if available
    if measurement.SavedMeasurement.image_path:
        measurement_dict['image_url'] = url_for('uploaded_file', filename=os.path.basename(measurement.SavedMeasurement.image_path))
    
    # Add audio URL if available
    if measurement.SavedMeasurement.audio_path:
        measurement_dict['audio_url'] = url_for('get_audio', filename=os.path.basename(measurement.SavedMeasurement.audio_path))
    
    return jsonify(measurement_dict)

@app.route('/measurement/<int:measurement_id>/audio', methods=['POST'])
@login_required
def upload_measurement_audio(measurement_id):
    try:
        # Check if the post request has the file part
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
            
        audio_file = request.files['audio']
        
        # If user does not select file, browser also submit an empty part without filename
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Get the measurement
        measurement = SavedMeasurement.query.get_or_404(measurement_id)
        
        # Check if the current user is the owner or an admin
        if measurement.user_id != current_user.id and not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Generate a secure filename
        filename = f"audio_{measurement_id}_{int(time.time())}.wav"
        filepath = os.path.join('static', 'uploads', 'audio', filename)
        
        # Save the file
        audio_file.save(filepath)
        
        # Delete old audio file if exists
        if measurement.audio_path and os.path.exists(measurement.audio_path):
            try:
                os.remove(measurement.audio_path)
            except Exception as e:
                app.logger.error(f"Error deleting old audio file: {str(e)}")
        
        # Update the measurement with the new audio path
        measurement.audio_path = filepath
        measurement.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'audio_url': url_for('get_audio', filename=filename)
        })
        
    except Exception as e:
        app.logger.error(f"Error uploading audio: {str(e)}")
        return jsonify({'error': 'Failed to upload audio'}), 500

@app.route('/audio/<path:filename>')
@login_required
def get_audio(filename):
    try:
        # Security check to prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            return jsonify({'error': 'Invalid filename'}), 400
            
        # Get the measurement that has this audio file
        audio_path = os.path.join('static', 'uploads', 'audio', filename)
        
        # Find the measurement that has this audio file
        measurement = SavedMeasurement.query.filter_by(audio_path=audio_path).first()
        
        # Check if the current user is the owner or an admin
        if not measurement or (measurement.user_id != current_user.id and not current_user.is_admin):
            return jsonify({'error': 'Unauthorized'}), 403
            
        return send_from_directory('static/uploads/audio', filename)
        
    except Exception as e:
        app.logger.error(f"Error serving audio file: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        # Create the audio directory if it doesn't exist
        os.makedirs(os.path.join('static', 'uploads', 'audio'), exist_ok=True)
    init_db()
    app.run(debug=True)
