# Blog API Project

A production-ready backend API for a blogging platform built with FastAPI. This project demonstrates clean architecture and best practices for building scalable REST APIs. Users can register accounts, create blog posts, comment on content, and retrieve data efficiently through well-designed endpoints.

---

## Features

- **User Management:** Complete CRUD operations for user accounts
- **Post Management:** Full lifecycle management of blog posts with author attribution
- **Comment Management:** Threaded comment system tied to posts
- **Pagination:** Efficient data retrieval using skip and limit parameters
- **Filtering:** Query posts by specific authors
- **Nested Data Retrieval:** Fetch users with all their posts in a single API call
- **Consistent API Design:** RESTful endpoints following industry standards

---

## Prerequisites

Before getting started, make sure you have:

- Python 3.10 or higher installed
- PostgreSQL
- An API client like Postman or Insomnia for testing (optional)

---

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/blog-api.git
cd blog-api
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

The database will be created automatically when you first run the application.

---

## Running the Application

Start the development server with auto-reload enabled:

```bash
uvicorn app.main:app --reload
```

Once running, you can access the interactive API documentation at http://127.0.0.1:8000/docs. This interface lets you explore and test all available endpoints directly from your browser.

---

## API Examples

Here are some common operations you can perform:

**Create a new user:**

```
POST /users/
```

**Retrieve paginated posts:**

```
GET /posts/?skip=0&limit=10
```

**Get a user with all their posts:**

```
GET /users/{user_id}/posts
```

**Add a comment to a post:**

```
POST /posts/{post_id}/comments
```

---

## Project Structure

```
blog_api/
├── app/
│   ├── main.py              # Application entry point
│   ├── database.py          # Database configuration
│   ├── dependencies.py      # Shared dependencies
│   ├── models/              # SQLAlchemy database models
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/             # Pydantic validation schemas
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── crud/                # Database operations
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   └── routers/             # API route definitions
│       ├── users.py
│       ├── posts.py
│       └── comments.py
└── requirements.txt
```

This structure separates concerns clearly, making the codebase easier to maintain and scale as features are added.

---

## Technologies Used

- **FastAPI:** Modern Python web framework for building APIs
- **SQLAlchemy:** SQL toolkit and ORM for database operations
- **Pydantic:** Data validation using Python type hints
- **Uvicorn:** Lightning-fast ASGI server
- **Python 3.10+:** Latest language features and improvements

---

## Key Learnings

Building this project provided valuable insights into professional API development:

- Separating code into models, routers, and CRUD operations creates a maintainable architecture
- Pagination and filtering are critical for handling large datasets in production
- Consistent API design makes the system intuitive for frontend developers
- This structure mirrors patterns used in real-world FastAPI applications

---

## Troubleshooting

**Database errors:** Verify that the database file exists and your system has proper write permissions to the project directory.

**Dependency issues:** Make sure your virtual environment is activated, then run `pip install -r requirements.txt` again.

**API testing:** Use the built-in Swagger UI at `/docs` or external tools like Postman to validate endpoint behavior.

**Port conflicts:** If port 8000 is already in use, specify a different port: `uvicorn app.main:app --reload --port 8001`

---

## Contributing

This project was built as a learning exercise, but feedback and improvements are always welcome. Feel free to open an issue or submit a pull request with your suggestions.

---

## License

This project is released under the MIT License. You are free to use, modify, and distribute it for personal or commercial projects.
