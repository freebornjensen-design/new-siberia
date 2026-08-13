"""add service SEO columns (slug, meta_title, keywords)

Revision ID: 0003_service_seo
Revises: 0002_new_models
Create Date: 2026-08-13 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = '0003_service_seo'
down_revision = '0002_new_models'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('services', sa.Column('slug', sa.String(length=255), nullable=True))
    op.add_column('services', sa.Column('meta_title', sa.String(length=255), nullable=True))
    op.add_column('services', sa.Column('keywords', sa.String(length=500), nullable=True))
    op.create_index('ix_services_slug', 'services', ['slug'], unique=True)


def downgrade():
    op.drop_index('ix_services_slug', table_name='services')
    op.drop_column('services', 'keywords')
    op.drop_column('services', 'meta_title')
    op.drop_column('services', 'slug')
