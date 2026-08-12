"""
Thumbnail generation utilities using PIL.
Generates preview-sized images to speed up page load times.
"""
import os
import tempfile
from PIL import Image


def generate_thumbnail(source_path, thumb_path, size=(300, 300), quality=85):
    """
    Generate a thumbnail image from the source file.

    Writes to a temp file first and atomically renames it into place, so
    concurrent requests (multiple gunicorn workers) can never serve a
    partially-written image.

    Args:
        source_path: Full path to the original image.
        thumb_path: Full path where the thumbnail should be saved.
        size: (width, height) tuple for maximum dimensions.
        quality: JPEG save quality (1-100).

    Returns:
        True if thumbnail was created, False if it already existed or failed.
    """
    if os.path.exists(thumb_path):
        return False  # Already exists

    dest_dir = os.path.dirname(thumb_path)
    os.makedirs(dest_dir, exist_ok=True)

    try:
        img = Image.open(source_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        # Convert RGBA/P to RGB for JPEG compatibility — use WHITE background
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background

        # Write to a temp file in the same directory, then atomically replace
        fd, tmp_path = tempfile.mkstemp(dir=dest_dir, suffix='.img.tmp')
        os.close(fd)
        try:
            # format must be explicit: PIL can't infer it from the .tmp suffix.
            # Derive it from the target path so PNG sources stay PNG (e.g. personnel photos),
            # and webp/gif stay in their own format.
            ext = os.path.splitext(thumb_path)[1].lower()
            fmt = {'.jpg': 'JPEG', '.jpeg': 'JPEG', '.png': 'PNG',
                   '.webp': 'WEBP', '.gif': 'GIF'}.get(ext, 'JPEG')
            img.save(tmp_path, format=fmt, quality=quality)
            # mkstemp creates 0600 files; make them world-readable for nginx
            os.chmod(tmp_path, 0o644)
            os.replace(tmp_path, thumb_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        return True
    except Exception as e:
        print(f"Thumbnail error for {source_path}: {e}")
        return False


def ensure_personnel_thumbnail(app, person):
    """
    Ensure a thumbnail exists for the given personnel member's photo.

    Returns the thumbnail URL (relative to 'static/') if successful,
    or the original photo URL as fallback.
    """
    if not person.photo:
        return None

    photo_dir = app.config.get('PERSONNEL_PHOTO_DIR', 'uploads/personnel')
    source_path = os.path.join(app.root_path, 'static', photo_dir, person.photo)
    thumb_filename = f'thumbs/{person.photo}'
    thumb_path = os.path.join(app.root_path, 'static', photo_dir, thumb_filename)

    # Also check whether the source exists at all
    if not os.path.exists(source_path):
        return None

    generate_thumbnail(source_path, thumb_path)
    if os.path.exists(thumb_path):
        return f'{photo_dir}/{thumb_filename}'

    # Fallback: return the original photo URL
    return f'{photo_dir}/{person.photo}'


def ensure_image_variants(app, rel_dir, filename, thumb_size=(800, 800), web_size=(1600, 1600),
                          thumb_quality=80, web_quality=85):
    """
    Ensure thumbnail + web-optimized versions exist for an image under static/{rel_dir}.

    Generates (and caches on disk):
      static/{rel_dir}/thumbs/{base}.jpg  – small preview for grids/carousels
      static/{rel_dir}/web/{base}.jpg     – optimized full view for lightbox

    Returns a tuple (thumb_rel, web_rel) of paths relative to 'static/',
    or (None, None) if the source is missing.
    Falls back to the original file if a variant can't be generated.
    """
    if not filename:
        return None, None

    source_path = os.path.join(app.root_path, 'static', rel_dir, filename)
    if not os.path.exists(source_path):
        return None, None

    base = os.path.splitext(filename)[0]
    thumb_rel = f'{rel_dir}/thumbs/{base}.jpg'
    web_rel = f'{rel_dir}/web/{base}.jpg'
    thumb_path = os.path.join(app.root_path, 'static', thumb_rel)
    web_path = os.path.join(app.root_path, 'static', web_rel)

    generate_thumbnail(source_path, thumb_path, size=thumb_size, quality=thumb_quality)
    generate_thumbnail(source_path, web_path, size=web_size, quality=web_quality)

    # Fall back to original if generation failed
    if not os.path.exists(thumb_path):
        thumb_rel = f'{rel_dir}/{filename}'
    if not os.path.exists(web_path):
        web_rel = f'{rel_dir}/{filename}'
    return thumb_rel, web_rel
