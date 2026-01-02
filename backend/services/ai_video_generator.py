import requests
import time
from pathlib import Path
from typing import Optional

def generate_ai_video(prompt: str, output_path: str, duration: int = 4) -> bool:
    """
    Generate an AI video from text prompt using Replicate API.
    
    Args:
        prompt: Text description for the video
        output_path: Where to save the video file
        duration: Video duration in seconds (default 4 for Stable Video Diffusion)
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
        
        if not replicate_api_token:
            print("❌ REPLICATE_API_TOKEN not found in .env file")
            print("Please get a free token from: https://replicate.com/account/api-tokens")
            return False
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"🎬 Generating AI video for: {prompt[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {replicate_api_token}",
            "Content-Type": "application/json"
        }
        
        prediction_data = {
            "version": "3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
            "input": {
                "prompt": prompt,
                "num_frames": 24 * duration,
                "num_inference_steps": 25,
                "fps": 24,
                "frame_rate": 24,
                "motion_bucket_id": 127,
                "cond_aug": 0.02
            }
        }
        
        print("📤 Creating prediction...")
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            json=prediction_data,
            headers=headers
        )
        response.raise_for_status()
        
        prediction = response.json()
        prediction_url = prediction["urls"]["get"]
        
        print(f"⏳ Video generation started (ID: {prediction['id']})...")
        print("   This may take 1-3 minutes...")
        
        max_wait_time = 300
        start_time = time.time()
        
        while True:
            if time.time() - start_time > max_wait_time:
                print("❌ Video generation timed out")
                return False
            
            response = requests.get(prediction_url, headers=headers)
            response.raise_for_status()
            status = response.json()
            
            if status["status"] == "succeeded":
                video_url = status["output"]
                print("📥 Downloading video...")
                
                video_response = requests.get(video_url, timeout=60)
                video_response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(video_response.content)
                
                print(f"✅ AI video saved to: {output_path}")
                return True
                
            elif status["status"] == "failed":
                error = status.get("error", "Unknown error")
                print(f"❌ Video generation failed: {error}")
                return False
            
            elif status["status"] in ["starting", "processing", "cancelling"]:
                elapsed = int(time.time() - start_time)
                print(f"   Status: {status['status']} ({elapsed}s elapsed)...")
                time.sleep(5)
            
            else:
                print(f"⚠️ Unknown status: {status['status']}")
                time.sleep(5)
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error generating video: {e}")
        return False
    except Exception as e:
        print(f"❌ Error generating AI video: {e}")
        return False


def generate_multiple_scene_videos(script: str, output_dir: Path) -> Optional[Path]:
    """
    Generate videos for multiple scenes from a script.
    For now, generates one video for the entire script.
    
    Args:
        script: The script text
        output_dir: Directory to save videos
    
    Returns:
        Path to the generated video file or None if failed
    """
    try:
        output_path = output_dir / "ai_generated_video.mp4"
        
        success = generate_ai_video(script, str(output_path))
        
        if success:
            return output_path
        return None
        
    except Exception as e:
        print(f"❌ Error in generate_multiple_scene_videos: {e}")
        return None
