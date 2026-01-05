# Product Management System

A comprehensive Flask-based REST API for product management with Firebase authentication, following SOLID principles and design patterns.

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
- Firebase account with service account credentials
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
3. Import the `database_setup.sql` file or run it manually
4. The database `product_management_db` will be created

Alternatively, run from command line:
```bash
mysql -u root -p < database_setup.sql
```

### 5. Set Up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing one
3. Enable **Authentication** > **Sign-in method** > Enable **Email/Password**
4. Go to **Project Settings** > **Service Accounts**
5. Click **Generate New Private Key**
6. Save the JSON file as `firebase-config.json` in the project root

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=
DATABASE_NAME=product_management_db

# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this

# Firebase Configuration
FIREBASE_CONFIG_PATH=firebase-config.json

# Application Configuration
PORT=5000
DEBUG=True
```

### 7. Initialize Database Tables

The application will automatically create tables on first run, but you can also initialize manually:

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 8. Run the Application

```bash
python run.py
```

The server will start at `http://localhost:5000`

## 📡 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "id_token": "firebase_id_token_here",
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "staff"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "id_token": "firebase_id_token_here"
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <firebase_id_token>
```

### Products

#### Get All Products
```http
GET /api/products?page=1&per_page=20&search=laptop
Authorization: Bearer <firebase_id_token>
```

#### Get Product by ID
```http
GET /api/products/1
Authorization: Bearer <firebase_id_token>
```

#### Create Product (Admin/Manager only)
```http
POST /api/products
Authorization: Bearer <firebase_id_token>
Content-Type: application/json

{
  "product_name": "Laptop Dell XPS 15",
  "sku": "LAP-DELL-001",
  "description": "High-performance laptop",
  "category_id": 2,
  "price": 1500.00,
  "cost_price": 1200.00,
  "quantity_in_stock": 10,
  "reorder_level": 5,
  "supplier_id": 1,
  "barcode": "123456789",
  "weight": 2.5,
  "dimensions": "35x25x2 cm"
}
```

#### Update Product (Admin/Manager only)
```http
PUT /api/products/1
Authorization: Bearer <firebase_id_token>
Content-Type: application/json

{
  "price": 1450.00,
  "quantity_in_stock": 15
}
```

#### Delete Product (Admin only)
```http
DELETE /api/products/1
Authorization: Bearer <firebase_id_token>
```

#### Get Low Stock Products
```http
GET /api/products/low-stock
Authorization: Bearer <firebase_id_token>
```

#### Get Inventory Value (Admin/Manager only)
```http
GET /api/products/inventory-value
Authorization: Bearer <firebase_id_token>
```

## 🧪 Testing with Postman

1. **Set Up Firebase Authentication:**
   - Use Firebase Authentication SDK in your frontend/testing client
   - Get ID token after successful authentication
   - Use this token in Authorization header

2. **Example Postman Request:**
   - Method: GET
   - URL: `http://localhost:5000/api/products`
   - Headers:
     - `Authorization: Bearer <your_firebase_id_token>`
     - `Content-Type: application/json`

## 🔒 Role-Based Access Control

- **Admin**: Full access to all endpoints
- **Manager**: Can manage products, inventory, and sales
- **Staff**: Can view products and record sales

## 🗂️ Project Structure

```
product_management_system/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration management
│   ├── models/                  # Database models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── supplier.py
│   │   ├── inventory.py
│   │   └── sales.py
│   ├── repositories/            # Data access layer
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   └── product_repository.py
│   ├── services/                # Business logic layer
│   │   ├── auth_service.py
│   │   └── product_service.py
│   ├── controllers/             # API endpoints
│   │   ├── auth_controller.py
│   │   └── product_controller.py
│   ├── middleware/              # Authentication middleware
│   │   └── auth_middleware.py
│   └── utils/                   # Utility functions
│       └── response_handler.py
├── firebase-config.json         # Firebase credentials
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── database_setup.sql           # Database schema
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🛠️ Development

### Adding New Features

1. **Create Model**: Add new model in `app/models/`
2. **Create Repository**: Extend `BaseRepository` in `app/repositories/`
3. **Create Service**: Add business logic in `app/services/`
4. **Create Controller**: Add API endpoints in `app/controllers/`
5. **Register Blueprint**: Register in `app/__init__.py`

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

### Firebase Authentication Error
```
Solution: Verify firebase-config.json path and Firebase project settings
```

### Module Not Found Error
```
Solution: Activate virtual environment and reinstall requirements
pip install -r requirements.txt
```

## 📝 Future Enhancements

- [ ] Add inventory transaction endpoints
- [ ] Add sales endpoints
- [ ] Add category management endpoints
- [ ] Add supplier management endpoints
- [ ] Implement bulk product import (CSV)
- [ ] Add reporting and analytics endpoints
- [ ] Add file upload for product images
- [ ] Implement audit logging
- [ ] Add unit and integration tests

## 👥 Team Members

- Shozab Mehdi (70143698)
- Muhammad Shahbaz (70142324)
- Awais Shahid (70142466)

## 📄 License

This project is for educational purposes as part of Software Construction & Development course.

---

**University of Lahore - Department of Software Engineering**