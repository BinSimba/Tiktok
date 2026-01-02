import os
import requests
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def download_pexels_video(query: str, output_path: str) -> bool:
    try:
        if not PEXELS_API_KEY:
            print("⚠️  PEXELS_API_KEY not found in .env file")
            return False

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"🔍 Searching Pexels for: {query[:50]}...")

        headers = {
            "Authorization": PEXELS_API_KEY
        }

        search_url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=landscape"
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("videos"):
            print(f"⚠️  No videos found for: {query}")
            return False

        video = data["videos"][0]
        video_files = video.get("video_files", [])

        best_video = None
        for vf in video_files:
            if vf.get("quality") == "hd" and vf.get("width", 0) >= 1920:
                best_video = vf
                break

        if not best_video and video_files:
            best_video = video_files[0]

        if not best_video:
            print("❌ No video files available")
            return False

        video_url = best_video["link"]
        print(f"⬇️  Downloading video from Pexels...")

        video_response = requests.get(video_url, timeout=60, stream=True)
        video_response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Video downloaded: {output_path}")
        return True

    except Exception as e:
        print(f"❌ Error downloading Pexels video: {e}")
        return False

def find_and_download_video(query: str, output_path: str) -> bool:
    return download_pexels_video(query, output_path)
