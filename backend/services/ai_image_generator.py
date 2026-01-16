import requests
from pathlib import Path
import urllib.parse
import time
import hashlib
import os
from functools import lru_cache

CACHE_DIR = Path("/tmp/image_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_key(prompt: str, width: int, height: int) -> str:
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    return f"{prompt_hash}_{width}x{height}.jpg"

def get_cached_image(prompt: str, width: int, height: int) -> Path:
    cache_key = get_cache_key(prompt, width, height)
    cache_path = CACHE_DIR / cache_key
    if cache_path.exists():
        return cache_path
    return None

def cache_image(prompt: str, image_data: bytes, width: int, height: int):
    cache_key = get_cache_key(prompt, width, height)
    cache_path = CACHE_DIR / cache_key
    try:
        with open(cache_path, 'wb') as f:
            f.write(image_data)
        return cache_path
    except Exception as e:
        print(f"⚠️ Failed to cache image: {e}")
        return None

def generate_ai_image(prompt: str, output_path: str) -> bool:
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        cleaned_prompt = prompt.replace('\n', ' ').replace('\r', ' ')
        cleaned_prompt = ' '.join(cleaned_prompt.split())
        cleaned_prompt = cleaned_prompt[:500]
        
        print(f"📝 Original prompt length: {len(prompt)}")
        print(f"📝 Cleaned prompt length: {len(cleaned_prompt)}")
        
        width, height = 1080, 1920
        
        cached_path = get_cached_image(cleaned_prompt, width, height)
        if cached_path:
            print(f"🔄 Using cached image from: {cached_path}")
            import shutil
            shutil.copy2(cached_path, output_path)
            print(f"✅ Cached image saved to: {output_path}")
            return True
        
        encoded_prompt = urllib.parse.quote(cleaned_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true"
        
        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"📥 Attempt {attempt + 1}/{max_retries}: Fetching image from: {image_url}")
                response = requests.get(image_url, timeout=60)
                
                print(f"📊 Response status: {response.status_code}, content length: {len(response.content)}")
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
                    print(f"⏳ Rate limit reached. Waiting {retry_after}s before retry...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                
                print(f"💾 Writing to: {output_path}")
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                cache_image(cleaned_prompt, response.content, width, height)
                
                print(f"✅ File exists: {output_path.exists()}, size: {output_path.stat().st_size} bytes")
                print(f"✅ AI image generated and saved to: {output_path}")
                return True
                
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"⏳ Waiting {delay}s before retry...")
                    time.sleep(delay)
                continue
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"🚫 Rate limit on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"⏳ Waiting {delay}s before retry...")
                        time.sleep(delay)
                    continue
                else:
                    raise
        
        print(f"❌ Max retries reached for image generation")
        return False
        
    except Exception as e:
        print(f"❌ Error generating AI image: {e}")
        import traceback
        traceback.print_exc()
        return False
