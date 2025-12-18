# Modular FastAPI Backend – Day 43 Complete

Clean, production-ready FastAPI project using **modular monolith** architecture – exactly as required in the 90-day roadmap.

### Current Features (Read-Only API)

- `GET /users/{user_id}` → Get a user by ID
- `GET /products` → List all products
- `GET /products/{product_id}` → Get single product

Fully modular, scalable, and ready for authentication (Day 44+).

### Project Structure

```
app/
├── main.py              → App factory (registers modules)
├── config.py            → Settings loader
├── database.py          → Async SQLAlchemy engine + Base
├── dependencies.py      → Shared DB dependency
│
├── modules/
│   ├── users/           → Complete user module (read-only)
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── router.py    → GET /users/{id}
│   │
│   └── products/        → Complete product module (read-only)
│       ├── models.py    → Product + Category models
│       ├── schemas.py
│       ├── repository.py
│       ├── service.py
│       └── router.py    → GET /products & /products/{id}
│
└── shared/
    ├── exceptions.py    → Custom HTTP exceptions
    └── utils.py         → Helper functions
```

### How to Run

```bash
# Install
pip install fastapi uvicorn sqlalchemy asyncpg pydantic-settings

# Set DB URL in .env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/modular_db

# Create tables
python -c "from app.database import engine, Base; import asyncio; async def go(): async with engine.begin() as c: await c.run_sync(Base.metadata.create_all); asyncio.run(go())"

# Start
uvicorn app.main:app --reload
```
