import os
import urllib.request
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings.dev')
django.setup()

from products.models import Brand

os.makedirs('media/brands', exist_ok=True)

# Map Brand Name -> (simple_icons_slug, official_hex_color)
simple_icons_map = {
    'Apple': ('apple', '#000000'),
    'Samsung': ('samsung', '#1428A0'),
    'Sony': ('sony', '#000000'),
    'ASUS': ('asus', '#00539B'),
    'Acer': ('acer', '#83B81A'),
    'AMD': ('amd', '#ED1C24'),
    'Intel': ('intel', '#0071C5'),
    'NVIDIA': ('nvidia', '#76B900'),
    'Dell': ('dell', '#0076CE'),
    'HP': ('hp', '#0096D6'),
    'Lenovo': ('lenovo', '#E2231A'),
    'LG': ('lg', '#A50034'),
    'Bose': ('bose', '#000000'),
    'JBL': ('jbl', '#FF6600'),
    'Logitech': ('logitech', '#00B8FC'),
    'Xiaomi': ('xiaomi', '#FF6900'),
    'OnePlus': ('oneplus', '#F31514'),
    'Nike': ('nike', '#000000'),
    'Adidas': ('adidas', '#000000'),
    'Puma': ('puma', '#000000')
}

headers = {'User-Agent': 'Mozilla/5.0'}

for name, (icon_slug, hex_color) in simple_icons_map.items():
    slug = name.lower().replace("'", "").replace(" ", "-")
    cdn_url = f"https://cdn.jsdelivr.net/npm/simple-icons@v10/icons/{icon_slug}.svg"
    file_path = f"media/brands/{slug}.svg"
    
    try:
        req = urllib.request.Request(cdn_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            svg_content = response.read().decode('utf-8')
            
            # Inject official brand color into SVG path fill attribute
            if '<path ' in svg_content and 'fill=' not in svg_content:
                svg_content = svg_content.replace('<path ', f'<path fill="{hex_color}" ')
            elif 'fill="' in svg_content:
                import re
                svg_content = re.sub(r'fill="[^"]*"', f'fill="{hex_color}"', svg_content)
            else:
                svg_content = svg_content.replace('<svg ', f'<svg fill="{hex_color}" ')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
                
            b, _ = Brand.objects.update_or_create(
                name=name,
                defaults={
                    'slug': slug,
                    'logo': f'brands/{slug}.svg',
                    'is_featured': True,
                    'is_active': True
                }
            )
            print(f"Simple Icons SVG downloaded & saved: {b.name} -> {b.logo.url}")
    except Exception as e:
        print(f"Failed to fetch {name} ({icon_slug}): {e}")

print("All Simple Icons official SVGs successfully fetched & saved into DB!")
