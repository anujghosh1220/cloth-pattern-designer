# Draping Threads - Tailoring Management System

![Draping Threads Logo](static/images/logo.png)

A comprehensive, production-ready web application for modern tailoring businesses. Draping Threads streamlines the entire tailoring workflow, from customer management to order tracking and pattern generation, all built with Flask and modern web technologies.

## 🌟 Key Features

### 👤 User Management
- **Authentication & Authorization**
  - Secure login/registration system
  - Role-based access control (Admin/User)
  - Password hashing with bcrypt
  - Session management with Flask-Login

### 👔 Customer Management
- **Customer Profiles**
  - Comprehensive customer database
  - Contact information and addresses
  - Customer history and preferences
  - Advanced search and filtering

### 📦 Order Management
- **Order Processing**
  - Create and track orders with unique job numbers
  - Real-time order status updates
  - Payment tracking (advance, balance, total)
  - Delivery date management with reminders
  - Invoice generation

### 📏 Measurement System
- **Precise Measurements**
  - Comprehensive body measurement recording
  - Support for various garment types
  - Visual measurement guides
  - Measurement history and versioning
  - PDF export functionality

### ✂️ Advanced Features
- **Pattern Generation**
  - Automated pattern creation from measurements
  - Custom pattern adjustments
  - Print-ready pattern exports
- **Media Management**
  - Image uploads for design references
  - Audio notes for special instructions
  - Document storage
- **Reporting**
  - Sales and revenue reports
  - Order status overview
  - Customer analytics

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- SQLite (included with Python)
- Modern web browser (Chrome, Firefox, Edge, or Safari)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/cloth-pattern-designer.git
   cd cloth-pattern-designer
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   Create a `.env` file in the project root:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_SECRET_KEY=your-secure-secret-key-here
   DATABASE_URL=sqlite:///cloth.db
   UPLOAD_FOLDER=./static/uploads
   MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
   ```

5. **Initialize Database**
   ```bash
   flask init-db
   ```

## 🏃 Running the Application

### Development Mode
```bash
flask run
```
Access the application at `http://localhost:5000`

### Production Deployment
For production deployment, we recommend using:
- Gunicorn or uWSGI as the WSGI server
- Nginx as the reverse proxy
- PostgreSQL or MySQL for the database
- Environment variables for configuration

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📂 Project Structure
```
cloth-pattern-designer/
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Project dependencies
├── static/                # Static files (CSS, JS, images)
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── uploads/           # User uploads
├── templates/             # HTML templates
├── migrations/            # Database migrations
└── instance/              # Instance folder for local configuration
```

## 📚 Documentation

### Database Models
- **User**: Manages user accounts and authentication
- **Customer**: Stores customer information
- **Order**: Tracks orders and their status
- **Measurement**: Stores body measurements
- **Pattern**: Manages generated patterns

### API Endpoints
- `/api/customers`: Customer management
- `/api/orders`: Order processing
- `/api/measurements`: Measurement handling
- `/api/patterns`: Pattern generation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask and modern web technologies
- Inspired by the needs of modern tailoring businesses
- Special thanks to all contributors

## 📞 Support

For support, email support@drapingthreads.com or open an issue in the GitHub repository.
- Nginx or Apache as the reverse proxy
- PostgreSQL or MySQL for the database

## 🔐 Default Admin Account

- **Username:** `admin`
- **Password:** `admin2214`

> **⚠️ Security Note:** Change the default admin password immediately after first login.

## 📁 Project Structure

```
cloth-pattern-designer/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── instance/             # Instance-specific files (not in version control)
│   └── cloth.db          # SQLite database
├── migrations/           # Database migrations (Alembic)
├── static/               # Static files
│   ├── css/              # Custom stylesheets
│   ├── js/               # JavaScript files
│   ├── images/           # Static images
│   └── uploads/          # User-uploaded files
│       ├── audio/        # Audio notes
│       ├── measurements/ # Measurement images
│       └── samples/      # Sample images
└── templates/            # Jinja2 templates
    ├── base.html         # Base template
    ├── dashboard.html    # Main dashboard
    ├── customers/        # Customer-related templates
    │   ├── list.html     # Customer listing
    │   ├── view.html     # Customer details
    │   └── edit.html     # Edit customer
    ├── orders/           # Order management
    │   ├── list.html     # Order listing
    │   ├── view.html     # Order details
    │   └── create.html   # Create new order
    └── admin/            # Admin section
        ├── users/        # User management
        └── settings.html # Application settings
```

## 📋 Features in Detail

### 🔍 Customer Management
- **Customer Profiles**
  - Store complete customer information
  - Track order history and preferences
  - Add multiple contact methods
  - Customer categorization and tagging

### 📦 Order Processing
- **Order Creation**
  - Multiple items per order
  - Custom order specifications
  - Priority levels
  - Delivery scheduling

- **Order Tracking**
  - Real-time status updates
  - Delivery timeline
  - Payment tracking
  - Order history and reports

### 📏 Measurement System
- **Measurement Types**
  - Standard body measurements
  - Garment-specific measurements
  - Custom measurement fields
  - Measurement templates

- **Pattern Generation**
  - Automatic pattern creation
  - Custom pattern adjustments
  - Print and save patterns
  - Pattern versioning

## 🛠️ Advanced Configuration

### Database Configuration
By default, the application uses SQLite. To use a different database:
1. Install the appropriate database driver (e.g., `psycopg2` for PostgreSQL)
2. Update the `DATABASE_URL` in `.env`
3. Run database migrations: `flask db upgrade`

### File Storage
- Default storage is local file system
- Configure `UPLOAD_FOLDER` in `.env`
- Ensure proper permissions are set on the upload directory

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments
- Built with Flask and modern web technologies
- Uses Bootstrap for responsive design
- Icons by Font Awesome

## 📧 Support
For support, email support@drapingthreads.com or open an issue in the GitHub repository.

### Customer Management
- Store customer contact information
- Track total order amounts
- View order history
- Manage customer measurements

### Measurement System
- Store detailed body measurements
- Attach reference images
- Record audio notes
- Generate pattern visualizations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
