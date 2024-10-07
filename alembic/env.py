from __future__ import with_statement
import sys
import os
from logging.config import fileConfig
from dotenv import load_dotenv 

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Load the Alembic configuration
config = context.config
fileConfig(config.config_file_name)

# Add the app directory to the Python path for imports
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Import your models
from app.backend.models import UserAccount  # Adjust import based on your structure
from app.backend.util import encode_password, escape_password
# Target metadata for 'autogenerate' support
target_metadata = UserAccount.metadata

load_dotenv()

# Get database credentials from environment variables
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

encoded_password = encode_password(DB_PASSWORD)
escaped_password = escape_password(encoded_password)

# Construct the database URL using environment variables
if all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    database_url = f'postgresql://{DB_USERNAME}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    config.set_main_option('sqlalchemy.url', database_url)
else:
    raise ValueError("Database credentials not fully set. Please check your environment variables.")

def run_migrations_offline():
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

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if we are running in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
