# Modular E-Commerce Backend

A production-ready e-commerce backend built during Days 53-56 of the 90-Day Backend Engineering Journey. This project demonstrates professional modular architecture with complete authentication, authorization, and business logic.

## What This Application Does

A fully functional online store backend with everything organized into independent modules:

- **Authentication**: Secure registration, login, JWT tokens, refresh tokens
- **User Management**: Profile management and admin controls
- **Product Catalog**: Products with categories, reviews, search, and filtering
- **Order System**: Checkout with stock validation and order history
- **Admin Dashboard**: User management, role updates, and sales analytics

## Tech Stack

- **FastAPI** - Modern async web framework
- **PostgreSQL** - Production database
- **SQLAlchemy 2.0** - Async ORM
- **Alembic** - Database migrations
- **JWT** - Token-based authentication
- **Bcrypt** - Password hashing

## Project Architecture

```
modular_ecommerce/
├── app/
│   ├── main.py              # Application entry
│   ├── config.py            # Settings
│   ├── database.py          # DB connection
│   ├── modules/
│   │   ├── auth/            # Authentication & authorization
│   │   │   ├── models.py    # User, RefreshToken, Permission
│   │   │   ├── schemas.py   # Request/response models
│   │   │   ├── service.py   # Auth logic
│   │   │   ├── dependencies.py  # Auth dependencies
│   │   │   └── router.py    # Auth endpoints
│   │   ├── users/           # User profiles
│   │   │   ├── models.py
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   ├── products/        # Product catalog
│   │   │   ├── models.py    # Product, Category, Review
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   ├── orders/          # Order processing
│   │   │   ├── models.py    # Order, OrderItem
│   │   │   ├── service.py
│   │   │   └── router.py
│   │   └── admin/           # Admin operations
│   │       ├── service.py
│   │       └── router.py
│   ├── shared/              # Shared utilities
│   │   └── exceptions.py
│   └── tests/
├── alembic/                 # Database migrations
├── .env                     # Environment variables
├── requirements.txt
└── README.md
```

## Quick Setup

### 1. Navigate to Project

```bash
cd day53-56/modular_ecommerce
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce_db
SECRET_KEY=your-secret-key-here
DEBUG=True
PROJECT_NAME=Modular E-Commerce
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Setup Database

```bash
alembic upgrade head
```

### 6. Run Server

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## Module Overview

### Auth Module (`/auth`)

Handles all authentication and authorization:

```
POST   /auth/register         Register new user
POST   /auth/login            Login (get tokens)
POST   /auth/refresh          Refresh access token
POST   /auth/revoke           Logout (revoke refresh token)
```

Features:

- JWT access tokens (30 min expiry)
- Refresh tokens (7 day expiry)
- Role-based access control
- Permission system

### Users Module (`/users`)

User profile management:

```
GET    /users/me              Get current user profile
PUT    /users/me              Update profile
GET    /users/{id}            Get user profile (public)
```

### Products Module (`/products`)

Product catalog with reviews:

```
POST   /products              Create product (admin)
GET    /products              List products (with filters)
GET    /products/{id}         Get product details
PUT    /products/{id}         Update product (admin)
DELETE /products/{id}         Delete product (admin)
POST   /products/{id}/reviews Add review
GET    /products/{id}/reviews List reviews
```

Filtering:

```bash
GET /products?search=laptop&category_id=1&min_price=500&max_price=2000
```

### Orders Module (`/orders`)

Order processing and history:

```
POST   /orders                Create order
GET    /orders                List user's orders
GET    /orders/{id}           Get order details
```

Order creation validates stock and uses atomic transactions:

```json
{
  "items": [{ "product_id": 1, "quantity": 2 }]
}
```

### Admin Module (`/admin`)

Admin-only operations:

```
GET    /admin/users           List all users
PATCH  /admin/users/{id}/role Update user role
PATCH  /admin/users/{id}/ban  Ban/unban user
GET    /admin/reports/sales   Sales analytics
```

## Key Features

### Modular Architecture

Each module is completely independent:

- Own models, schemas, services, and routes
- Can be developed and tested separately
- Easy to add new modules
- Clear separation of concerns

### Authentication & Authorization

**JWT Tokens:**

- Access tokens for API requests
- Refresh tokens for staying logged in
- Token rotation on refresh

**Role-Based Access:**

- Admin: Full access to everything
- User: Access to own data and public endpoints

**Permission System:**

- Granular permissions (create:product, delete:user, etc.)
- Flexible authorization checks
- Easy to add new permissions

### Order Processing

**Atomic Transactions:**

```
1. Validate products exist
2. Check stock availability
3. Calculate total
4. Reduce stock
5. Create order
→ Rollback if any step fails
```

**Stock Management:**

- Prevents overselling
- Updates stock atomically
- Rollback on failure

### Admin Analytics

Track business metrics:

- Total sales and revenue
- Order status distribution
- Top-selling products
- User activity

## Testing the Application

### Using Swagger UI

1. Open http://localhost:8000/docs
2. Register a new user
3. Login to get access token
4. Click "Authorize" and enter token
5. Test any endpoint

### Test Scenarios

**User Flow:**

1. Register account
2. Browse products
3. Add review to product
4. Create order
5. View order history

**Admin Flow:**

1. Login as admin (admin@example.com / admin123)
2. View all users
3. Update user role
4. Check sales analytics

## Development

### Adding a New Module

1. Create module folder in `app/modules/`
2. Add models, schemas, service, router
3. Register router in `app/main.py`
4. Create migration if needed

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Common Issues

**Database connection error:**
Check DATABASE_URL in `.env` and ensure PostgreSQL is running.

**Module import errors:**
Make sure you're in the correct directory and virtual environment is activated.

**Token errors:**
Check SECRET_KEY is set in `.env` and matches between restarts.

## What You Learn

- Modular application architecture
- JWT authentication with refresh tokens
- Role-based access control (RBAC)
- Permission systems
- Atomic transactions
- Stock management
- Business analytics
- Production-ready patterns

## Future Enhancements

- Email verification
- Password reset flow
- Payment gateway integration
- Product recommendations
- Advanced analytics
- Caching with Redis
- Real-time notifications
