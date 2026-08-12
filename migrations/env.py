from __future__ import with_statement
import sys
import os
from logging.config import fileConfig

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from models import db

app = create_app()

with app.app_context():
    target_metadata = db.metadata

def run_migrations_offline():
    context.configure(url=app.config.get('SQLALCHEMY_DATABASE_URI'))

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = db.engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

