# E-Commerce API

A complete e-commerce backend built during Days 36-38 of my 90-Day Backend Engineering Journey. This project demonstrates complex database relationships, business logic, and production-ready patterns.

## What This API Does

This is a full backend for an online store with everything needed to manage products, orders, and users:

- User accounts with admin and customer roles
- Product catalog with multiple categories per product
- Order processing with automatic stock management
- Price tracking (orders remember what customers paid)
- Admin-protected routes for management operations

## Tech Stack

- **FastAPI** - Modern async web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy 2.0** - Async ORM for database operations
- **Alembic** - Database migrations
- **Pydantic v2** - Data validation
- **Bcrypt** - Secure password hashing

## Project Structure

```
ecommerce_api/
├── app/
│   ├── api/v1/
│   │   ├── __init__.py
│   │   └── router.py              # All API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Settings
│   │   └── security.py            # Password hashing
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py                  # Database connection
│   ├── models/                    # Database tables
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── association.py         # Many-to-many table
│   ├── repositories/              # Data access layer
│   │   ├── __init__.py
│   │   └── ...
│   ├── schemas/                   # Request/response models
│   │   ├── __init__.py
│   │   └── ...
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   └── ...
│   ├── dependencies.py
│   └── main.py
├── alembic/                       # Database migrations
├── requirements.txt
├── .env.example
├── create_admin.py                # Creates first admin user
└── README.md
```

## Quick Setup

### 1. Clone and Navigate

```bash
git clone https://github.com/your-username/backend-journey.git
cd day36-38/ecommerce_api
```

### 2. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/ecommerce_db
```

### 3. Start PostgreSQL

Using Docker:

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ecommerce_db \
  -p 5432:5432 \
  postgres:16
```

Or use your local PostgreSQL installation.

### 4. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Initialize Database

```bash
alembic upgrade head
```

Creates all tables in your database.

### 6. Create Admin User

```bash
python create_admin.py
```

Creates: `admin@shop.com` / `admin123`

### 7. Start the Server

```bash
uvicorn app.main:app --reload --port 8000
```

API is now running at http://localhost:8000

Visit http://localhost:8000/docs for interactive documentation.

## Database Schema

```
Users ──(1:many)──> Orders ──(1:many)──> Order Items ──(many:1)──> Products
                                                                        ↕
                                                                (many:many)
                                                                        ↕
                                                                  Categories
```

**Tables:**

- **Users**: id, email, name, hashed_password, role (admin/customer)
- **Categories**: id, name, description
- **Products**: id, name, description, price, stock
- **Orders**: id, user_id, total, status, created_at
- **Order Items**: id, order_id, product_id, quantity, price_at_purchase

## API Endpoints

### Categories (Admin Only)

```
POST   /v1/categories          Create category
GET    /v1/categories          List all
GET    /v1/categories/{id}     Get single category
PUT    /v1/categories/{id}     Update category
DELETE /v1/categories/{id}     Delete category
```

### Products (Admin Write, Public Read)

```
POST   /v1/products            Create product (admin)
GET    /v1/products            List with filters
GET    /v1/products/{id}       Get single product
PUT    /v1/products/{id}       Update product (admin)
DELETE /v1/products/{id}       Delete product (admin)
```

**Filtering Products:**

```bash
GET /v1/products?search=laptop
GET /v1/products?category_id=1&min_price=500&max_price=1500
GET /v1/products?skip=0&limit=10
```

### Orders (Authenticated Users)

```
POST   /v1/orders              Create order
GET    /v1/users/me/orders     Get user's orders
```

## Key Features

### Order Creation Logic

When creating an order:

1. Validates all products exist
2. Checks stock availability
3. Calculates total price
4. Reduces product stock
5. Creates order with order items
6. Saves price at purchase time
7. Rolls back everything if any step fails

Example order:

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 3, "quantity": 1 }
  ]
}
```

### Stock Management

- Validates stock before processing order
- Prevents overselling (returns error if insufficient stock)
- Reduces stock atomically in transaction
- Automatic rollback on failure

### Price Snapshots

Order items save `price_at_purchase` to preserve historical pricing. Product prices can change but order history stays accurate.

## Example Usage

### Create a Product

```bash
curl -X POST http://localhost:8000/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock": 10,
    "category_ids": [1]
  }'
```

### Create an Order

```bash
curl -X POST http://localhost:8000/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      { "product_id": 1, "quantity": 2 }
    ]
  }'
```

## Development Guide

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add field to table"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Check current version
alembic current
```

### Adding New Features

1. Update model in `app/models/`
2. Generate migration with Alembic
3. Create Pydantic schema in `app/schemas/`
4. Add repository in `app/repositories/`
5. Add business logic in `app/services/`
6. Add routes in `app/api/v1/router.py`

## Architecture

### Repository Pattern

Repositories handle all database operations. This separates data access from business logic and makes code testable.

### Service Layer

Services contain business logic and use repositories. They handle validation, transactions, and complex operations.

### Dependency Injection

FastAPI automatically injects dependencies (database sessions, services) into route handlers.

## Troubleshooting

**Connection refused:**
PostgreSQL isn't running. Start it with the Docker command above.

**Table already exists:**
Reset migrations (warning: deletes data):

```bash
alembic downgrade base
alembic upgrade head
```

**Module not found:**

```bash
cd day36-38/ecommerce_api
pip install -r requirements.txt
```

## What You Learn

- Complex database relationships (one-to-many, many-to-many)
- Transaction handling for data consistency
- Repository and service patterns
- Stock management systems
- Async SQLAlchemy with PostgreSQL
- Production-ready API architecture

## Future Enhancements

Possible additions:

- JWT authentication for all routes
- User registration endpoint
- Order status tracking
- Payment integration
- Product reviews and ratings
- Search with Elasticsearch
- Caching with Redis
