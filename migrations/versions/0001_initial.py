"""initial full schema

Single clean initial migration for the new-siberia project.
Covers the complete current schema from models.py.

Revision ID: 0001_initial
Revises:
Create Date: 2026-08-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ── articles ────────────────────────────────────────────────────────
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── contacts ────────────────────────────────────────────────────────
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=False),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('addiction_type', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── users ───────────────────────────────────────────────────────────
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=80), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=True, server_default=sa.text('false')),
    )

    # ── personnel ───────────────────────────────────────────────────────
    op.create_table(
        'personnel',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('position', sa.String(length=120), nullable=True),
        sa.Column('photo', sa.String(length=255), nullable=True),
        sa.Column('achievements', sa.Text(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('intro', sa.Text(), nullable=True),
        sa.Column('full_bio', sa.Text(), nullable=True),
        sa.Column('education', sa.Text(), nullable=True),
        sa.Column('competencies', sa.Text(), nullable=True),
        sa.Column('personal_message', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── services ────────────────────────────────────────────────────────
    op.create_table(
        'services',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('meta_description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── gallery_images ──────────────────────────────────────────────────
    op.create_table(
        'gallery_images',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('folder', sa.String(length=255), nullable=False, server_default='gallery'),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── testimonials ────────────────────────────────────────────────────
    op.create_table(
        'testimonials',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('photo', sa.String(length=255), nullable=True),
        sa.Column('screenshot', sa.String(length=255), nullable=True),
        sa.Column('author_role', sa.String(length=100), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── statistics ──────────────────────────────────────────────────────
    op.create_table(
        'statistics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('label', sa.String(length=100), nullable=False),
        sa.Column('value', sa.String(length=50), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── advantages ──────────────────────────────────────────────────────
    op.create_table(
        'advantages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('fa_icon', sa.String(length=50), nullable=True, server_default='fa-check-circle'),
        sa.Column('icon_type', sa.String(length=10), nullable=False, server_default='fa'),
        sa.Column('svg_file', sa.String(length=255), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── certificates ────────────────────────────────────────────────────
    op.create_table(
        'certificates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('personnel_id', sa.Integer(), sa.ForeignKey('personnel.id'), nullable=True),
        sa.Column('file', sa.String(length=255), nullable=False),
        sa.Column('owner', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_certificates_personnel_id', 'certificates', ['personnel_id'])

    # ── daily_audio ─────────────────────────────────────────────────────
    op.create_table(
        'daily_audio',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('filename', sa.String(length=255), nullable=False),
        sa.Column('audio_date', sa.Date(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    # ── chat_messages ───────────────────────────────────────────────────
    op.create_table(
        'chat_messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(length=64), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_from_admin', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('is_read', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_chat_messages_session_id', 'chat_messages', ['session_id'])

    # ── settings ────────────────────────────────────────────────────────
    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('key', sa.String(length=100), nullable=False, unique=True),
        sa.Column('value', sa.Text(), nullable=True),
        sa.Column('question', sa.Text(), nullable=True),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('settings')
    op.drop_index('ix_chat_messages_session_id', table_name='chat_messages')
    op.drop_table('chat_messages')
    op.drop_table('daily_audio')
    op.drop_index('ix_certificates_personnel_id', table_name='certificates')
    op.drop_table('certificates')
    op.drop_table('advantages')
    op.drop_table('statistics')
    op.drop_table('testimonials')
    op.drop_table('gallery_images')
    op.drop_table('services')
    op.drop_table('personnel')
    op.drop_table('users')
    op.drop_table('contacts')
    op.drop_table('articles')
