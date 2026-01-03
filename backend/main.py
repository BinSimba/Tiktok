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
import os
from dotenv import load_dotenv

app = FastAPI(title="Text-to-TikTok API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://192.168.1.169:3000", "https://text-to-tiktok-pi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = Path("/tmp/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class VideoRequest(BaseModel):
    text: str
    is_custom: bool = False

class VideoResponse(BaseModel):
    script: str
    video_url: str

@app.get("/")
async def root():
    return {"message": "Text-to-TikTok API is running"}

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    try:
        session_id = str(uuid.uuid4())
        
        print(f"Request received - is_custom: {request.is_custom}, text: {request.text[:50]}...")
        
        load_dotenv()
        pexels_api_key = os.getenv("PEXELS_API_KEY")
        
        if request.is_custom:
            script = request.text
            print(f"Using custom script: {script[:50]}...")
            
            background_video = OUTPUT_DIR / f"{session_id}_background.mp4"
            success = find_and_download_video(script, str(background_video))
            
            if success:
                background_path = str(background_video)
            else:
                background_image = OUTPUT_DIR / f"{session_id}_background.jpg"
                generate_ai_image(script, str(background_image))
                background_path = str(background_image)
        else:
            script = generate_tiktok_script(request.text)
            print(f"Using AI generated script: {script[:50]}...")
            
            background_image = OUTPUT_DIR / f"{session_id}_background.jpg"
            generate_ai_image(script, str(background_image))
            background_path = str(background_image)
        
        audio_path = OUTPUT_DIR / f"{session_id}_audio.mp3"
        generate_audio(script, str(audio_path))
        
        video_path = OUTPUT_DIR / f"{session_id}_video.mp4"
        
        create_tiktok_video(
            script=script,
            audio_path=str(audio_path),
            background_path=background_path,
            output_path=str(video_path)
        )
        
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
        video_url = f"{backend_url}/videos/{session_id}_video.mp4"
        
        return VideoResponse(
            script=script,
            video_url=video_url
        )
        
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Error generating video: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos/{filename}")
async def get_video(filename: str):
    video_path = OUTPUT_DIR / filename
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_path)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
