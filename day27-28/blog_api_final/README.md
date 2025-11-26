# Blog API

A RESTful API for managing blog posts, users, and comments built with FastAPI and PostgreSQL. This project demonstrates modern API development practices with proper project structure, comprehensive documentation, and database relationships.

## Project Description

This is a backend application that provides endpoints for creating and managing a blog platform. Users can create accounts, write posts, and add comments to posts. The API includes features like pagination, search, filtering, and sorting to handle data efficiently.

The project uses FastAPI for building the API, SQLAlchemy as the ORM for database operations, and PostgreSQL for data storage. All endpoints are automatically documented through Swagger UI and ReDoc.

## Features

- User account management with full CRUD operations
- Blog post creation and management
- Comment system for posts
- Search and filter posts by title or user
- Sort posts by different fields
- Pagination support for efficient data loading
- Automatic API documentation
- Input validation using Pydantic schemas
- Database relationships with cascade delete

## Technology Stack

- FastAPI 0.104+
- PostgreSQL
- SQLAlchemy 2.0+
- Pydantic v2
- Python 3.9+

## Project Structure

```
blog_api_final/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── crud/
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routers/
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── comments.py
│   └── utils/
│       └── errors.py
├── seed_data.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

Before you begin, make sure you have these installed:

- Python 3.9 or higher
- PostgreSQL 12 or higher
- pip package manager

### Setup Steps

1. Clone the repository and navigate to the project directory:

```bash
cd blog_api_final
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:

```bash
createdb blog_db
```

5. Configure environment variables by copying the example file:

```bash
copy .env.example .env
```

6. Edit the .env file with your database credentials:

```
DATABASE_URL=postgresql://username:password@localhost:5432/blog_db
```

7. Run the seeding script to populate the database with sample data:

```bash
python seed_data.py
```

8. Start the application:

```bash
uvicorn app.main:app --reload
```

9. Access the API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Users

- POST /users/ - Create a new user
- GET /users/ - Get list of users with pagination
- GET /users/{user_id} - Get a specific user by ID
- PUT /users/{user_id} - Update user information
- DELETE /users/{user_id} - Delete a user

### Posts

- POST /posts/ - Create a new blog post
- GET /posts/ - Get list of posts with filtering and sorting
- GET /posts/{post_id} - Get a specific post by ID
- GET /posts/user/{user_id} - Get all posts by a user
- PUT /posts/{post_id} - Update a post
- DELETE /posts/{post_id} - Delete a post

### Comments

- POST /comments/ - Add a comment to a post
- GET /comments/post/{post_id} - Get all comments for a post

## Usage Examples

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

### Create a Post

```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Post content here", "user_id": 1}'
```

### Get All Posts with Filters

```bash
curl "http://localhost:8000/posts/?skip=0&limit=10&sort=created_at&desc=true"
```

### Search Posts

```bash
curl "http://localhost:8000/posts/?search=FastAPI"
```

### Add a Comment

```bash
curl -X POST "http://localhost:8000/comments/" \
  -H "Content-Type: application/json" \
  -d '{"content": "Great post!", "post_id": 1}'
```

## Database Schema

The application uses three main tables:

**Users Table**

- id (Primary Key)
- email (Unique)
- name
- created_at

**Posts Table**

- id (Primary Key)
- title
- content
- user_id (Foreign Key to users)
- created_at

**Comments Table**

- id (Primary Key)
- content
- post_id (Foreign Key to posts)
- created_at

When a user is deleted, all their posts are also deleted. When a post is deleted, all its comments are deleted.

## Testing

You can test the API using the interactive Swagger UI documentation at http://localhost:8000/docs. This interface allows you to try out all endpoints directly from your browser.

For a complete workflow:

1. Create a user
2. Create a post for that user
3. Add comments to the post
4. Retrieve the post to see all comments
5. Filter or search posts
6. Update post content
7. Delete resources

## Development

The project follows a clean architecture pattern with separated concerns:

- Models define database tables
- Schemas handle data validation
- CRUD operations manage database queries
- Routers define API endpoints
- Dependencies handle shared functionality

When adding new features, follow this structure to maintain consistency.

## Troubleshooting

**Database Connection Issues**

If you cannot connect to the database, verify PostgreSQL is running:

```bash
psql -U postgres -l
```

**Port Already in Use**

If port 8000 is already in use, start the server on a different port:

```bash
uvicorn app.main:app --reload --port 8001
```

**Import Errors**

Make sure you are running commands from the project root directory, not from inside the app folder.

## Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic[email]==2.5.0
python-dotenv==1.0.0
```

## Contact

For questions or issues, please open an issue on the repository.
