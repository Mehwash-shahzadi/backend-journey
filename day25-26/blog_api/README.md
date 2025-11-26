# Blog API Project

Build a production-ready backend API for a blogging platform. Users can register, create posts, comment on posts, and retrieve nested data efficiently. The API is structured for maintainability, scalability, and real-world use.

---

## Features

- **User Management:** Full CRUD (Create, Read, Update, Delete) for users.
- **Post Management:** Each post belongs to a user with complete CRUD operations.
- **Comment Management:** Each comment belongs to a post, with full CRUD support.
- **Pagination:** Retrieve posts in chunks using `skip` and `limit` parameters.
- **Filtering:** Filter posts by author ID.
- **Nested Data Retrieval:** Fetch a user with all their posts in a single request.
- **Consistent API Design:** Logical endpoints with proper HTTP methods.

---

## Prerequisites

- Python 3.10+
- SQLite (default) or any SQL database
- Optional: Postman or any API client for testing

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/blog-api.git
cd blog-api
```

## Installation and Usage

1. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up the database:**
   The project uses SQLite by default. Ensure database.db is created automatically when running the app.

4. **Start the FastAPI server:**

```bash
uvicorn app.main:app --reload
```

5. **Access the API documentation:**

Open your browser at http://127.0.0.1:8000/docs to explore all endpoints.

6 .**Example endpoints:**

POST /users/ – Create a new user

GET /posts/?skip=0&limit=10 – Retrieve paginated posts

GET /users/{user_id}/posts – Retrieve a user with all posts

---

**_Project Structure:_**

```
blog_api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/          # Database models
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/         # Pydantic models
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── crud/            # Database operations
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routers/         # API endpoints
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── comments.py
│   └── dependencies.py
└── requirements.txt
```

---

**Technologies Used**
Backend Framework: FastAPI

Database: SQLite (default), can switch to PostgreSQL or MySQL

ORM: SQLAlchemy

Data Validation: Pydantic

API Documentation: FastAPI automatic Swagger UI

Language: Python 3.10+

**Key Learnings**
Organizing code into models, routers, and crud improves maintainability.

Pagination and filtering are essential for real-world APIs.

Proper API design ensures consistency and ease of use.

This project structure reflects patterns used in production-grade FastAPI applications.

**License**
MIT License – free to use and modify for personal or professional projects.

**Contributing**
This is a personal project, but suggestions and improvements are welcome! Open an issue or submit a pull request.

**Troubleshooting**
Database Errors: Ensure the database file exists and your environment has write permissions.

Dependency Issues: Activate virtual environment and run pip install -r requirements.txt.

API Testing: Use Postman or Swagger UI at /docs to validate endpoints.
