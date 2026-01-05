# Supplier Management System

A Flask-based REST API for supplier management, following SOLID principles and design patterns.

## 🏗️ Architecture

- **Repository Pattern**: Data access layer abstraction
- **Service Layer Pattern**: Business logic separation  
- **Factory Pattern**: Flask application factory
- **Dependency Injection**: Loose coupling between components
- **Singleton Pattern**: Firebase authentication service

## 🎯 SOLID Principles Implementation

- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extendable without modification via base classes
- **Liskov Substitution**: Repository implementations are interchangeable
- **Interface Segregation**: Focused, specific interfaces
- **Dependency Inversion**: Depend on abstractions, not concrete classes

## 📋 Prerequisites

- Python 3.9+
- MySQL 8.0+ (via XAMPP or standalone)
- Git

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd product_management_system
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

1. Start XAMPP and ensure MySQL is running
2. Open phpMyAdmin (http://localhost/phpmyadmin)
3. Create a database named `supplier_management_db`

Alternatively, run from command line:
```bash
mysql -u root -p -e "CREATE DATABASE supplier_management_db;"
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_NAME=supplier_management_db

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this

# Application Configuration
PORT=5000
DEBUG=True
```

### 6. Initialize Database Tables

The application will automatically create tables on first run, but you can also initialize manually:

```bash
python
>>> from FlaskProjectSCD.app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 7. Run the Application

```bash
python run.py
```

The server will start at `http://localhost:5000`

## 📡 API Endpoints

### Suppliers

#### Get All Suppliers
```http
GET /api/suppliers?page=1&per_page=20&search=tech
```

#### Get Supplier by ID
```http
GET /api/suppliers/1
```

#### Create Supplier
```http
POST /api/suppliers
Content-Type: application/json

{
  "supplier_name": "Tech Supplies Inc",
  "contact_person": "John Doe",
  "email": "john@techsupplies.com",
  "phone": "+1234567890",
  "address": "123 Main St, City, Country"
}
```

#### Update Supplier
```http
PUT /api/suppliers/1
Content-Type: application/json

{
  "supplier_name": "Updated Tech Supplies Inc",
  "phone": "+0987654321"
}
```

#### Delete Supplier
```http
DELETE /api/suppliers/1
```

## 🧪 Testing with Postman

Example Postman Request:
- Method: GET
- URL: `http://localhost:5000/api/suppliers`
- Headers:
  - `Content-Type: application/json`

## 🗂️ Project Structure

```
supplier_management_system/
├── FlaskProjectSCD/
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── config.py                # Configuration management
│   │   ├── models/                  # Database models
│   │   │   └── supplier.py
│   │   ├── repositories/            # Data access layer
│   │   │   ├── base_repository.py
│   │   │   └── supplier_repository.py
│   │   ├── services/                # Business logic layer
│   │   │   └── supplier_service.py
│   │   ├── controllers/             # API endpoints
│   │   │   └── supplier_controller.py
│   │   ├── middleware/              # Middleware components
│   │   │   └── auth_middleware.py
│   │   └── utils/                   # Utility functions
│   │       └── response_handler.py
│   ├── templates/                   # HTML templates
│   │   ├── base.html
│   │   └── suppliers.html
│   └── static/                      # Static files (CSS, JS)
├── .env                             # Environment variables
├── requirements.txt                 # Python dependencies
├── run.py                           # Application entry point
└── README.md                        # This file
```

## 🛠️ Development

### Adding New Features

1. **Create Model**: Add new model in `FlaskProjectSCD/app/models/`
2. **Create Repository**: Extend `BaseRepository` in `FlaskProjectSCD/app/repositories/`
3. **Create Service**: Add business logic in `FlaskProjectSCD/app/services/`
4. **Create Controller**: Add API endpoints in `FlaskProjectSCD/app/controllers/`
5. **Register Blueprint**: Register in `FlaskProjectSCD/app/__init__.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for all functions
- Keep functions small and focused (SRP)

## 🐛 Troubleshooting

### MySQL Connection Error
```
Solution: Ensure XAMPP MySQL is running and credentials in .env are correct
```

### Module Not Found Error
```
Solution: Activate virtual environment and reinstall requirements
pip install -r requirements.txt
```

## 📝 Future Enhancements

- [ ] Add authentication and authorization
- [ ] Add more supplier-related features (ratings, contracts, etc.)
- [ ] Add file upload for supplier documents
- [ ] Implement audit logging
- [ ] Add unit and integration tests
- [ ] Add reporting and analytics

## 👥 Team Members

- Shozab Mehdi (70143698)
- Muhammad Shahbaz (70142324)
- Awais Shahid (70142466)

## 📄 License

This project is for educational purposes as part of Software Construction & Development course.

---

**University of Lahore - Department of Software Engineering**