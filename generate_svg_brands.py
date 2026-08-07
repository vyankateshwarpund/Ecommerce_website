import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Brand

os.makedirs('media/brands', exist_ok=True)

svg_icons = {
    'Apple': '<path fill="#FFFFFF" d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.32c.67-.82 1.13-1.96.99-3.12-1 .04-2.19.67-2.88 1.48-.62.72-1.15 1.88-1.01 3.01 1.12.09 2.23-.55 2.9-1.37z"/>',
    'Google': '<path fill="#FFFFFF" d="M16 6a10 10 0 1 0 10 10A10 10 0 0 0 16 6zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"/><text x="16" y="21" fill="#FFFFFF" font-size="16" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">G</text>',
    'Microsoft': '<rect x="4" y="4" width="11" height="11" fill="#FFFFFF"/><rect x="17" y="4" width="11" height="11" fill="#FFFFFF"/><rect x="4" y="17" width="11" height="11" fill="#FFFFFF"/><rect x="17" y="17" width="11" height="11" fill="#FFFFFF"/>',
    'Samsung': '<text x="16" y="20" fill="#FFFFFF" font-size="9" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">SAMSUNG</text>',
    'Sony': '<text x="16" y="21" fill="#FFFFFF" font-size="11" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">SONY</text>',
    'Nike': '<path fill="#FFFFFF" d="M26.7 9.01c-6.83 4.14-11.4 7.64-13.72 10.51-1.63 2.02-1.97 3.51-1.04 4.47.8 1 2.5.8 5.1-.6 4.9-2.6 11.9-8.4 11.9-8.4s-9.9 5.3-13.4 6.6c-1.8.7-3.1.6-3.7-.1-.7-.8-.4-2.1 1-4.2C15.7 13.8 22.5 8.3 26.7 9.01z"/>',
    'Adidas': '<path fill="#FFFFFF" d="M4 26h5l3-5H7L4 26zm7 0h5l5-9h-5l-5 9zm7 0h5l5-13h-5l-5 13z"/>',
    'LG': '<text x="16" y="22" fill="#FFFFFF" font-size="16" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">LG</text>',
    'HP': '<text x="16" y="22" fill="#FFFFFF" font-size="16" font-style="italic" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">hp</text>',
    'Dell': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">DELL</text>',
    'Lenovo': '<text x="16" y="20" fill="#FFFFFF" font-size="10" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">Lenovo</text>',
    'ASUS': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">ASUS</text>',
    'Acer': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">acer</text>',
    'OnePlus': '<path fill="#FFFFFF" d="M4 4h24v24H4V4zm4 4v16h16V8H8zm4 4h4v8h-4v-8z"/>',
    'Xiaomi': '<text x="16" y="22" fill="#FFFFFF" font-size="16" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">mi</text>',
    'Realme': '<text x="16" y="20" fill="#FFFFFF" font-size="10" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">realme</text>',
    'Vivo': '<text x="16" y="21" fill="#FFFFFF" font-size="13" font-style="italic" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">vivo</text>',
    'Oppo': '<text x="16" y="21" fill="#FFFFFF" font-size="13" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">oppo</text>',
    'boAt': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">boAt</text>',
    'JBL': '<text x="16" y="22" fill="#FFFFFF" font-size="15" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">JBL</text>',
    'Bose': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">BOSE</text>',
    'Puma': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">PUMA</text>',
    'Levis': '<text x="16" y="20" fill="#FFFFFF" font-size="10" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">LEVI\'S</text>',
    'Zara': '<text x="16" y="21" fill="#FFFFFF" font-size="13" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">ZARA</text>',
    'Whirlpool': '<text x="16" y="19" fill="#FFFFFF" font-size="8" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">Whirlpool</text>',
    'Panasonic': '<text x="16" y="19" fill="#FFFFFF" font-size="8" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">Panasonic</text>',
    'Logitech': '<text x="16" y="20" fill="#FFFFFF" font-size="10" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">logitech</text>',
    'Canon': '<text x="16" y="21" fill="#FFFFFF" font-size="12" font-weight="900" font-family="Arial, sans-serif" text-anchor="middle">Canon</text>'
}

for b_name, svg_content in svg_icons.items():
    slug = b_name.lower().replace("'", "").replace(" ", "-")
    full_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">{svg_content}</svg>'
    img_path = f'media/brands/{slug}.svg'
    with open(img_path, 'w', encoding='utf-8') as f:
        f.write(full_svg)
    
    b, _ = Brand.objects.update_or_create(
        name=b_name,
        defaults={'slug': slug, 'logo': f'brands/{slug}.svg', 'is_featured': True, 'is_active': True}
    )
    print(f"Saved clean SVG symbol for {b.name} -> {b.logo.url}")

print("All 28 Brands updated with clean SVG official symbols!")
