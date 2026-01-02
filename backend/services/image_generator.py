from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

def generate_ai_background(prompt: str, output_path: str) -> str:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    width = 1080
    height = 1920
    
    img = Image.new('RGB', (width, height), color='#0f0f23')
    draw = ImageDraw.Draw(img)
    
    colors = [
        (139, 92, 246),
        (6, 182, 212),
        (236, 72, 153),
        (34, 211, 238),
        (168, 85, 247)
    ]
    
    for i in range(0, height, 40):
        color_idx = i // (height // len(colors))
        color = colors[color_idx % len(colors)]
        
        alpha = int(100 * (i / height))
        r = int(color[0] * 0.3 + alpha * 0.7)
        g = int(color[1] * 0.3 + alpha * 0.7)
        b = int(color[2] * 0.3 + alpha * 0.7)
        
        bg_color = (
            min(255, max(0, r)),
            min(255, max(0, g)),
            min(255, max(0, b))
        )
        
        draw.rectangle([(0, i), (width, i + 40)], fill=bg_color)
    
    for i in range(15):
        import random
        x = random.randint(0, width - 200)
        y = random.randint(0, height - 200)
        size = random.randint(100, 300)
        
        color = random.choice(colors)
        draw.ellipse([x, y, x + size, y + size], fill=color + (30,))
    
    img.save(output_path, quality=95)
    print(f"Generated background for: {prompt}")
    
    return str(output_path)

def generate_background_from_text(text: str, output_path: str) -> str:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    return generate_ai_background(text, str(output_path))
