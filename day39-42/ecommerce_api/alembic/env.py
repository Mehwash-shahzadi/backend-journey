from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

# ------------------------------------------------------------------
# 1. Import your Base (this is the ONLY thing that was wrong before)
# ------------------------------------------------------------------
from app.models import Base          # <-- THIS LINE IS CRUCIAL
target_metadata = Base.metadata      # <-- and this one too

# ------------------------------------------------------------------
# 2. Load the .ini config and set up logging
# ------------------------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------
# 3. Get the async engine we created in app/database/db.py
# ------------------------------------------------------------------
from app.database.db import engine   # <-- async engine

# ------------------------------------------------------------------
# 4. OFFLINE mode (rarely used)
# ------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------------
# 5. ONLINE mode – this is what we actually use (async)
# ------------------------------------------------------------------
def run_migrations_online() -> None:
    """Run migrations in 'online' mode with our async engine."""

    # For async drivers (asyncpg) we need to use engine.begin() + run_sync
    def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,          # needed for SQLite, harmless for Postgres
        )

        with context.begin_transaction():
            context.run_migrations()

    # engine is an AsyncEngine → we must use .sync_engine or .begin()
    async def async_run():
        async with engine.begin() as conn:
            await conn.run_sync(do_run_migrations)

    # Run the async function synchronously (Alembic itself is sync)
    import asyncio
    asyncio.run(async_run())


# ------------------------------------------------------------------
# 6. Choose offline or online
# ------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()