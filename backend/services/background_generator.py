import os
from PIL import Image, ImageDraw, ImageFont
import random

def generate_background(text: str, output_path: str, width=1080, height=1920):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        colors = [
            ['#667eea', '#764ba2'],
            ['#f093fb', '#f5576c'],
            ['#4facfe', '#00f2fe'],
            ['#43e97b', '#38f9d7'],
            ['#fa709a', '#fee140'],
            ['#a8edea', '#fed6e3'],
            ['#ff9a9e', '#fecfef'],
            ['#ffecd2', '#fcb69f']
        ]
        color_pair = random.choice(colors)
        
        for y in range(height):
            ratio = y / height
            r = int(int(color_pair[0][1:3], 16) * (1 - ratio) + int(color_pair[1][1:3], 16) * ratio)
            g = int(int(color_pair[0][3:5], 16) * (1 - ratio) + int(color_pair[1][3:5], 16) * ratio)
            b = int(int(color_pair[0][5:7], 16) * (1 - ratio) + int(color_pair[1][5:7], 16) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        for _ in range(30):
            x = random.randint(0, width)
            y = random.randint(0, height)
            radius = random.randint(5, 30)
            alpha = random.randint(20, 50)
            color = (255, 255, 255, alpha)
            shape_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            shape_draw = ImageDraw.Draw(shape_layer)
            shape_draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=color)
            img.paste(Image.alpha_composite(img.convert('RGBA'), shape_layer).convert('RGB'))
        
        img.save(output_path, 'JPEG', quality=90)
        print(f"Background saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error generating background: {e}")
        return False
