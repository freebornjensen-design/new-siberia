"""add price_items, clinic_licenses, menu_items

Revision ID: 0002_new_models
Revises: 0001_initial
Create Date: 2026-08-12 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = '0002_new_models'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # ── price_items ──────────────────────────────────────────────────────
    op.create_table(
        'price_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('category', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('price', sa.String(length=100), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── clinic_licenses ──────────────────────────────────────────────────
    op.create_table(
        'clinic_licenses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('file', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── menu_items ───────────────────────────────────────────────────────
    op.create_table(
        'menu_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('parent_id', sa.Integer(), sa.ForeignKey('menu_items.id'), nullable=True),
        sa.Column('title', sa.String(length=120), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_menu_items_parent_id', 'menu_items', ['parent_id'])


def downgrade():
    op.drop_index('ix_menu_items_parent_id', table_name='menu_items')
    op.drop_table('menu_items')
    op.drop_table('clinic_licenses')
    op.drop_table('price_items')
