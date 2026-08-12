"""One-time photo migration: consolidate scattered photos into static/uploads/.

Usage: flask migrate-photos
"""
import os
import shutil

import click
from flask import current_app


def register(app):
    """Register the migrate-photos CLI command on the Flask app."""

    @app.cli.command('migrate-photos')
    def migrate_photos():
        """Consolidate all photos into static/uploads/<folder>/ structure."""
        static = current_app.static_folder
        uploads_root = os.path.join(static, 'uploads')
        os.makedirs(uploads_root, exist_ok=True)

        migrations = [
            # (source_dir, target_subdir)
            ('photo/gallery', 'gallery'),
            ('photo/personnel', 'personnel'),
            ('gallery/photo', 'personnel'),  # old personnel photos
        ]

        copied = 0
        for src_rel, dst_rel in migrations:
            src_dir = os.path.join(static, src_rel)
            dst_dir = os.path.join(uploads_root, dst_rel)
            if not os.path.isdir(src_dir):
                click.echo(f'  SKIP: {src_rel} (not found)')
                continue

            os.makedirs(dst_dir, exist_ok=True)
            for fn in os.listdir(src_dir):
                if fn.startswith('.'):
                    continue
                src_path = os.path.join(src_dir, fn)
                dst_path = os.path.join(dst_dir, fn)
                if os.path.isfile(src_path) and not os.path.exists(dst_path):
                    shutil.copy2(src_path, dst_path)
                    click.echo(f'  COPY: {src_rel}/{fn} -> uploads/{dst_rel}/{fn}')
                    copied += 1

        # Also create empty dirs for other gallery folders
        for folder in ('before', 'after', 'procedures'):
            os.makedirs(os.path.join(uploads_root, folder), exist_ok=True)
            click.echo(f'  MKDIR: uploads/{folder}/')

        click.echo(f'\nDone. Copied {copied} files. '
                   f'Existing files were NOT overwritten.')
