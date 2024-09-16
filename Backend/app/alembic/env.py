# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Import your models' Base and the engine
from database import Base
from database import DATABASE_URL, engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Set your SQLAlchemy URL directly from your app settings
config.set_main_option('sqlalchemy.url', DATABASE_URL)

# Add the models' MetaData object for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
