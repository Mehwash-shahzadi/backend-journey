# Day 30: Advanced Queries and Filtering

This project demonstrates advanced database querying techniques in FastAPI. It builds a powerful search and filtering system for blog posts with multiple criteria support.

## What This Project Does

The main `/posts/` endpoint supports complex queries:

- Search posts by title or content
- Filter by author
- Filter by date range
- Filter by tags
- Sort by any column in ascending or descending order
- Optimized with database indexes for fast queries

## Project Structure

```
day30/advanced_queries/
├── app/
│   ├── main.py          # FastAPI application with enhanced /posts endpoint
│   ├── models.py        # Post and Tag database models with indexes
│   ├── database.py      # Database connection and session management
│   ├── schemas.py       # Pydantic schemas for request/response
│   └── crud.py          # Query logic with filtering functions
├── seed.py              # Script to populate database with sample data
├── alembic/             # Database migrations for indexes
├── requirements.txt
└── README.md
```

## Setup and Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database

Make sure your PostgreSQL database is running and set the connection string:

```bash
export DATABASE_URL="postgresql://user:password@localhost/dbname"
```

### 3. Run Migrations

Apply database migrations to create tables and indexes:

```bash
alembic upgrade head
```

### 4. Seed Sample Data

Populate the database with test posts and tags:

```bash
python seed.py
```

This creates sample posts with various authors, dates, and tags for testing.

### 5. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### 6. Test the API

Open the interactive documentation:

```
http://127.0.0.1:8000/docs
```

## Query Examples

### Basic Search

Search for posts containing "python" in title or content:

```
GET /posts/?search=python
```

### Filter by Author

Get all posts by a specific author:

```
GET /posts/?author=mehwash
```

### Sort Results

Get posts sorted by creation date (newest first):

```
GET /posts/?sort=created_at&order=desc
```

### Date Range Filter

Get posts from a specific time period:

```
GET /posts/?from_date=2025-01-01&to_date=2025-12-31
```

### Filter by Tags

Get posts tagged with "python" or "fastapi":

```
GET /posts/?tags=python,fastapi
```

### Combined Filters

Combine multiple filters:

```
GET /posts/?author=john&search=api&sort=created_at&order=desc
```

## Query Parameters Reference

| Parameter   | Type   | Description                 | Example                |
| ----------- | ------ | --------------------------- | ---------------------- |
| `search`    | string | Search in title and content | `search=python`        |
| `author`    | string | Filter by author name       | `author=mehwash`       |
| `from_date` | date   | Start date for range filter | `from_date=2025-01-01` |
| `to_date`   | date   | End date for range filter   | `to_date=2025-12-31`   |
| `tags`      | string | Comma-separated tag names   | `tags=python,fastapi`  |
| `sort`      | string | Column to sort by           | `sort=created_at`      |
| `order`     | string | Sort order (asc/desc)       | `order=desc`           |

## Key SQLAlchemy Concepts Used

### filter()

Flexible filtering with AND/OR conditions:

```python
query = query.filter(Post.author == author)
```

### ilike()

Case-insensitive search:

```python
query = query.filter(Post.title.ilike(f"%{search}%"))
```

### between()

Date range filtering:

```python
query = query.filter(Post.created_at.between(from_date, to_date))
```

### join()

Filter by related tables (tags):

```python
query = query.join(Post.tags).filter(Tag.name.in_(tag_list))
```

### order_by()

Sort results:

```python
query = query.order_by(desc(Post.created_at))
```

## Database Optimization

### Indexes

This project uses database indexes on frequently queried columns:

- `title` - for text search
- `author` - for author filtering
- `created_at` - for date sorting and range queries
- `tags.name` - for tag filtering

Indexes dramatically improve query performance on large datasets.

### Why Indexes Matter

Without indexes, the database scans every row. With indexes, it can jump directly to relevant data. Think of it like a book's index - you don't read every page to find a topic.

## Common Issues and Solutions

**Queries are slow**

- Check that migrations were applied (`alembic upgrade head`)
- Verify indexes exist in database
- Use `.explain()` on queries to see execution plan

**No results returned**

- Verify seed data was loaded (`python seed.py`)
- Check date formats (YYYY-MM-DD)
- Tag names are case-sensitive

**Tags not filtering correctly**

- Make sure to use comma-separated values with no spaces
- Correct: `tags=python,fastapi`
- Incorrect: `tags=python, fastapi`

## What You'll Learn

- Building complex query filters dynamically
- Implementing search functionality
- Using database indexes for performance
- Joining tables in SQLAlchemy
- Sorting and ordering results
- Handling multiple optional query parameters
- Best practices for API filtering

## Next Steps

After mastering these queries, you can:

- Add pagination (limit/offset)
- Implement full-text search with PostgreSQL
- Add fuzzy search for typo tolerance
- Create saved searches for users
- Build query result caching
