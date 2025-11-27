# Day 29: Alembic Database Migrations Practice

This is a practice project for learning Alembic migrations with PostgreSQL. It's completely separate from the main blog API project.

## What is Alembic?

Alembic is a database migration tool for SQLAlchemy. Think of it like version control for your database schema. When you add or modify tables and columns, Alembic tracks those changes and lets you apply or rollback them safely.

## Project Structure

```
day29/migrations_practice/
├── app/
│   ├── __init__.py
│   ├── database.py
│   └── models/
│       ├── __init__.py
│       ├── user.py
│       ├── post.py
│       └── comment.py
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
└── README.md
```

## Setup Instructions

### 1. Install Required Packages

```bash
pip install sqlalchemy psycopg2-binary alembic
```

### 2. Create Practice Database

Create a separate PostgreSQL database for practice:

```sql
CREATE DATABASE blog_api_migrations_practice;
```

### 3. Configure Database Connection

Set your database URL as an environment variable:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/blog_api_migrations_practice"
```

Or use a `.env` file with python-dotenv.

## Database Configuration

- `app/database.py` contains the SQLAlchemy engine and Base
- `alembic/env.py` is configured to read DATABASE_URL from environment
- Alembic automatically detects your models through Base.metadata

## Working with Migrations

### Initialize Alembic (First Time Only)

If not already initialized:

```bash
alembic init alembic
```

### Create Initial Migration

Generate migration file based on your models:

```bash
alembic revision --autogenerate -m "Initial migration"
```

This creates a migration file in `alembic/versions/` with code to create your tables.

### Apply Migration to Database

Run the migration:

```bash
alembic upgrade head
```

Your database now has `users`, `posts`, and `comments` tables.

### Adding New Fields (Example)

Let's say you want to add a bio field to users:

1. Edit `app/models/user.py`:

```python
bio = Column(String(255), nullable=True)
```

2. Generate migration:

```bash
alembic revision --autogenerate -m "Add bio field to users"
```

3. Apply the migration:

```bash
alembic upgrade head
```

The `bio` column is now added to the users table.

### Rolling Back Changes

If you need to undo the last migration:

```bash
alembic downgrade -1
```

This removes the bio column. You can reapply it anytime with:

```bash
alembic upgrade head
```

### Viewing Migration History

See all migrations and current state:

```bash
alembic history
alembic current
```

## Important Tips

- Always use a practice database when learning migrations
- Never test migrations on production databases
- Review generated migration files before applying them
- Use descriptive migration messages
- Keep migrations small and focused on one change
- Test both upgrade and downgrade paths

## Common Commands Reference

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# View migration history
alembic history

# View current database version
alembic current
```

## What You'll Learn

- How to track database schema changes
- Creating and applying migrations
- Rolling back changes safely
- Managing database versions
- Handling schema changes in team environments

## Troubleshooting

**Migration not detecting changes?**

- Make sure your models import Base from database.py
- Check that alembic/env.py imports your models
- Verify DATABASE_URL is set correctly

**Duplicate column errors?**

- Check if migration was already applied
- Use `alembic current` to see database state

**Can't connect to database?**

- Verify DATABASE_URL format
- Check PostgreSQL is running
- Confirm database exists
