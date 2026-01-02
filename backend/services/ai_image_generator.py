import requests
from pathlib import Path
import urllib.parse

def generate_ai_image(prompt: str, output_path: str) -> bool:
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true"
        
        response = requests.get(image_url, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ AI image generated and saved to: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating AI image: {e}")
        return False
