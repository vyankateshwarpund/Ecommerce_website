import os
import io
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

def compress_and_convert_to_webp(image_file, max_size=(1200, 1200), quality=85):
    """
    Takes an uploaded or existing image file and converts it to optimized WebP format.
    Handles EXIF orientation, alpha transparency, and downscaling for fast web delivery.
    Returns a ContentFile with .webp extension, or None if conversion fails.
    """
    if not image_file:
        return None

    try:
        filename = getattr(image_file, 'name', '')
        
        # Read from beginning
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
            
        img = Image.open(image_file)

        # Correct rotation based on EXIF tag
        img = ImageOps.exif_transpose(img)

        # Handle color modes
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            img = img.convert('RGBA')
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Downscale if image dimensions exceed maximum threshold
        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        output = io.BytesIO()
        img.save(output, format='WEBP', quality=quality, optimize=True, method=6)
        output.seek(0)

        # Build clean .webp file name
        base_name, _ = os.path.splitext(os.path.basename(filename or 'image.jpg'))
        webp_filename = f"{base_name}.webp"

        return ContentFile(output.read(), name=webp_filename)
    except Exception as e:
        print(f"WebP conversion failed for {getattr(image_file, 'name', 'file')}: {e}")
        return None
