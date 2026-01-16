from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS
import cv2

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os
import uuid
from pathlib import Path

from models.script_generator import generate_tiktok_script
from services.tts_service import generate_audio
from services.video_assembler import create_tiktok_video
from services.image_generator import generate_background_from_text
from services.ai_image_generator import generate_ai_image
from services.local_video_generator import generate_ai_video_free
from services.video_finder import find_and_download_video
from services.unified_video_generator import generate_advanced_video
from services.physics_video_generator import PhysicsVideoGenerator
from services.perplexity_service import PerplexityService
import os
from dotenv import load_dotenv

app = FastAPI(title="Text-to-TikTok API")

print("🚀 Starting Text-to-TikTok API...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ CORS middleware configured")

OUTPUT_DIR = Path("/tmp/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"✅ Output directory created: {OUTPUT_DIR}")

class VideoRequest(BaseModel):
    text: str
    is_custom: bool = False
    use_advanced: bool = False
    video_type: str = "cinematic"
    style: str = "cinematic"
    character_type: str = "person"
    emotion: str = "neutral"
    quality: str = "high"
    camera_movement: str = "dynamic"
    duration: float = 10.0

class VideoResponse(BaseModel):
    script: str
    video_url: str

class PhysicsVideoRequest(BaseModel):
    text: str
    enable_physics: bool = True
    enable_fluid: bool = True
    enable_particles: bool = True
    duration: float = 5.0
    fps: int = 30

@app.on_event("startup")
async def startup_event():
    print("🎉 Text-to-TikTok API is ready!")

@app.get("/")
async def root():
    return {"message": "Text-to-TikTok API is running", "status": "ok"}

@app.get("/test")
async def test_endpoint():
    return {"message": "Test endpoint working", "output_dir": str(OUTPUT_DIR), "dir_exists": OUTPUT_DIR.exists()}

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    try:
        session_id = str(uuid.uuid4())
        
        print(f"\n{'='*50}")
        print(f"📥 Request received - is_custom: {request.is_custom}, text: {request.text[:50]}...")
        print(f"🆔 Session ID: {session_id}")
        print(f"{'='*50}\n")
        
        load_dotenv()
        pexels_api_key = os.getenv("PEXELS_API_KEY")
        print(f"🔑 Pexels API Key: {'✅ Set' if pexels_api_key else '❌ Not set'}")
        
        if request.is_custom:
            script = request.text
            print(f"\n📝 Using custom script: {script[:50]}...")
            
            background_video = OUTPUT_DIR / f"{session_id}_background.mp4"
            print(f"🔍 Trying to download Pexels video...")
            success = find_and_download_video(script, str(background_video))
            
            if success:
                background_path = str(background_video)
                print(f"✅ Pexels video downloaded: {background_path}")
            else:
                print(f"⚠️  Pexels video failed, falling back to AI animated video...")
                background_video_ai = OUTPUT_DIR / f"{session_id}_background.mp4"
                generate_ai_video_free(script, str(background_video_ai))
                background_path = str(background_video_ai)
                print(f"✅ AI animated video generated: {background_path}")
        else:
            print(f"\n🤖 Generating AI script...")
            script = generate_tiktok_script(request.text)
            print(f"✅ AI generated script: {script[:50]}...")
            
            background_video_ai = OUTPUT_DIR / f"{session_id}_background.mp4"
            print(f"🎨 Generating AI animated video...")
            generate_ai_video_free(script, str(background_video_ai))
            background_path = str(background_video_ai)
            print(f"✅ AI animated video generated: {background_path}")
        
        audio_path = OUTPUT_DIR / f"{session_id}_audio.mp3"
        print(f"\n🎵 Generating TTS audio...")
        generate_audio(script, str(audio_path))
        print(f"✅ Audio generated: {audio_path}")

        video_path = OUTPUT_DIR / f"{session_id}_video.mp4"

        print(f"\n🎬 Creating video...")
        create_tiktok_video(
            script=script,
            audio_path=str(audio_path),
            background_path=background_path,
            output_path=str(video_path)
        )
        print(f"✅ Video created: {video_path}")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        video_url = f"{backend_url}/videos/{session_id}_video.mp4"
        
        print(f"\n✅ Video ready: {video_url}\n")
        
        return VideoResponse(
            script=script,
            video_url=video_url
        )
        
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"\n❌ Error generating video: {error_detail}\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-advanced-video", response_model=VideoResponse)
async def generate_advanced_video_endpoint(request: VideoRequest, background_tasks: BackgroundTasks):
    try:
        session_id = str(uuid.uuid4())
        
        print(f"\n{'='*60}")
        print(f"🚀 Advanced AI Video Generation Request")
        print(f"{'='*60}")
        print(f"📝 Text: {request.text[:100]}...")
        print(f"🎬 Video Type: {request.video_type}")
        print(f"🎨 Style: {request.style}")
        print(f"👤 Character: {request.character_type}")
        print(f"😊 Emotion: {request.emotion}")
        print(f"⚙️  Quality: {request.quality}")
        print(f"📷 Camera: {request.camera_movement}")
        print(f"⏱️  Duration: {request.duration}s")
        print(f"🆔 Session ID: {session_id}")
        print(f"{'='*60}\n")
        
        if request.is_custom:
            script = request.text
            print(f"\n📝 Using custom script: {script[:100]}...")
        else:
            print(f"\n🤖 Generating AI script...")
            script = generate_tiktok_script(request.text)
            print(f"✅ AI generated script: {script[:100]}...")
        
        perplexity_service = PerplexityService()
        
        print(f"\n🎯 Enhancing prompt with Perplexity AI...")
        try:
            enhanced_script = await perplexity_service.enhance_video_prompt(script, mode="advanced")
            print(f"✅ Prompt enhanced: {enhanced_script[:100]}...")
        except Exception as e:
            print(f"⚠️  Perplexity enhancement failed: {e}")
            enhanced_script = script
        
        audio_path = OUTPUT_DIR / f"{session_id}_audio.mp3"
        print(f"\n🎵 Generating TTS audio...")
        try:
            generate_audio(enhanced_script, str(audio_path))
            print(f"✅ Audio generated: {audio_path}")
        except Exception as e:
            print(f"❌ Audio generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")
        
        video_path = OUTPUT_DIR / f"{session_id}_video.mp4"
        
        print(f"\n🎬 Generating advanced video...")
        try:
            generate_advanced_video(
                prompt=enhanced_script,
                audio_path=str(audio_path),
                output_path=str(video_path),
                video_type=request.video_type,
                style=request.style,
                character_type=request.character_type,
                emotion=request.emotion,
                quality=request.quality,
                camera_movement=request.camera_movement,
                duration=request.duration
            )
            print(f"✅ Video generated: {video_path}")
        except Exception as e:
            print(f"❌ Video generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        video_url = f"{backend_url}/videos/{session_id}_video.mp4"
        
        print(f"\n✅ Advanced video ready: {video_url}\n")
        
        return VideoResponse(
            script=enhanced_script,
            video_url=video_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"\n❌ Error generating advanced video: {error_detail}\n")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/videos/{filename}")
async def get_video(filename: str):
    video_path = OUTPUT_DIR / filename
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/test-api")
async def test_api():
    """Test endpoint for debugging Perplexity API integration"""
    try:
        perplexity_service = PerplexityService()
        test_prompt = "A beautiful sunset over the ocean"
        enhanced = await perplexity_service.enhance_video_prompt(test_prompt, mode="advanced")
        return {
            "status": "success",
            "original": test_prompt,
            "enhanced": enhanced
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.post("/test-perplexity")
async def test_perplexity():
    """Simple endpoint to test Perplexity API"""
    try:
        perplexity_service = PerplexityService()
        print("Testing Perplexity API...")
        test_prompt = "Test prompt"
        enhanced = await perplexity_service.enhance_video_prompt(test_prompt, mode="advanced")
        return {"status": "success", "result": enhanced}
    except Exception as e:
        import traceback
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}

@app.post("/generate-physics-video", response_model=VideoResponse)
async def generate_physics_video_endpoint(request: PhysicsVideoRequest, background_tasks: BackgroundTasks):
    try:
        session_id = str(uuid.uuid4())
        
        print(f"\n{'='*60}")
        print(f"🌊 Physics-Based Video Generation Request")
        print(f"{'='*60}")
        print(f"📝 Text: {request.text[:100]}...")
        print(f"⚙️  Physics: {request.enable_physics}")
        print(f"💧 Fluid: {request.enable_fluid}")
        print(f"✨ Particles: {request.enable_particles}")
        print(f"⏱️  Duration: {request.duration}s")
        print(f"🎬 FPS: {request.fps}")
        print(f"🆔 Session ID: {session_id}")
        print(f"{'='*60}\n")
        
        from moviepy.editor import ImageSequenceClip, AudioFileClip, VideoFileClip, CompositeVideoClip
        
        perplexity_service = PerplexityService()
        
        print(f"\n🎯 Enhancing prompt with Perplexity AI...")
        enhanced_prompt = await perplexity_service.enhance_video_prompt(request.text, mode="physics")
        
        generator = PhysicsVideoGenerator()
        
        print(f"\n🎬 Generating physics-based video frames...")
        frames = generator.generate_physics_video(
            prompt=enhanced_prompt,
            duration=request.duration,
            fps=request.fps
        )
        
        if not frames:
            raise HTTPException(status_code=500, detail="Failed to generate physics video frames")
        
        print(f"\n🎞️  Creating video from {len(frames)} frames...")
        
        temp_frames_dir = OUTPUT_DIR / f"{session_id}_frames"
        temp_frames_dir.mkdir(parents=True, exist_ok=True)
        
        for i, frame in enumerate(frames):
            frame_path = temp_frames_dir / f"frame_{i:06d}.png"
            cv2.imwrite(str(frame_path), cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        
        print(f"✅ Frames saved to: {temp_frames_dir}")
        
        video_no_audio = OUTPUT_DIR / f"{session_id}_no_audio.mp4"
        
        clip = ImageSequenceClip(str(temp_frames_dir), fps=request.fps)
        clip.write_videofile(str(video_no_audio), codec='libx264', audio=False, logger=None)
        print(f"✅ Video without audio: {video_no_audio}")
        
        audio_path = OUTPUT_DIR / f"{session_id}_audio.mp3"
        print(f"\n🎵 Generating TTS audio...")
        generate_audio(request.text, str(audio_path))
        print(f"✅ Audio generated: {audio_path}")
        
        video_path = OUTPUT_DIR / f"{session_id}_video.mp4"
        
        print(f"\n🎬 Combining video and audio...")
        video_clip = VideoFileClip(str(video_no_audio))
        audio_clip = AudioFileClip(str(audio_path))
        
        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        else:
            audio_clip = audio_clip.loop(duration=video_clip.duration)
        
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(str(video_path), codec='libx264', audio_codec='aac', logger=None)
        
        print(f"✅ Final video: {video_path}")
        
        video_clip.close()
        audio_clip.close()
        
        import shutil
        shutil.rmtree(temp_frames_dir, ignore_errors=True)
        video_no_audio.unlink(missing_ok=True)
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        video_url = f"{backend_url}/videos/{session_id}_video.mp4"
        
        print(f"\n✅ Physics video ready: {video_url}\n")
        
        return VideoResponse(
            script=request.text,
            video_url=video_url
        )
        
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"\n❌ Error generating physics video: {error_detail}\n")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
