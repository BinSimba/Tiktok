from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_background():
    width = 1080
    height = 1920
    
    img = Image.new('RGB', (width, height), color='#1a1a2e')
    
    draw = ImageDraw.Draw(img)
    
    for i in range(0, height, 20):
        alpha = int(50 * (i / height))
        color = (26 + alpha, 26 + alpha, 46 + alpha)
        draw.rectangle([(0, i), (width, i + 20)], fill=color)
    
    draw.ellipse([width//2 - 200, height//2 - 200, width//2 + 200, height//2 + 200], 
                 fill=(139, 92, 246), outline=(6, 182, 212), width=10)
    
    img.save('assets/backgrounds/default_bg.jpg', quality=95)
    print("Background created successfully!")

if __name__ == "__main__":
    create_background()
