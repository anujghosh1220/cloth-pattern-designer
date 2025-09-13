# Draping Threadss - Tailoring Management System

A comprehensive web application for managing tailoring orders, customer measurements, and pattern generation, built with Flask and modern web technologies. This system streamlines the workflow of tailoring businesses by digitizing customer information, measurements, and order tracking.

## 🚀 Features

### Core Functionality
- **User Authentication**
  - Secure login/register system
  - Role-based access control (Admin/User roles)
  - Password hashing for security
  - Session management

- **Customer Management**
  - Add, edit, and delete customer profiles
  - Store contact information and addresses
  - View customer order history
  - Search and filter customers

- **Order Management**
  - Create and track orders with unique job numbers
  - Monitor order status (pending, in-progress, completed, delivered)
  - Record advance payments and track balances
  - Set and manage delivery dates with reminders
  - Generate order invoices

- **Measurement System**
  - Comprehensive measurement recording
  - Support for different garment types
  - Visual measurement guides
  - Measurement history tracking
  - Export measurements to PDF

- **Advanced Features**
  - Pattern generation based on measurements
  - Image upload for design references
  - Audio notes for special instructions
  - Responsive design for all devices
  - Data export/import capabilities

## 🛠️ Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite (included with Python)
- Modern web browser (Chrome, Firefox, Edge, or Safari)

## 🚀 Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/cloth-pattern-designer.git
cd cloth-pattern-designer
```

### 2. Set Up Virtual Environment (Recommended)
#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
1. Create a `.env` file in the project root with the following content:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   FLASK_SECRET_KEY=your-secure-secret-key-here
   DATABASE_URL=sqlite:///cloth.db
   UPLOAD_FOLDER=./static/uploads
   MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB max file size
   ```

2. Initialize the database:
   ```bash
   flask init-db
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
flask run
```
Then open your browser and navigate to `http://localhost:5000`

### Production Deployment
For production deployment, consider using:
- Gunicorn or uWSGI as the WSGI server
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
