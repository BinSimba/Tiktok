from PIL import Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from pathlib import Path

os.environ['IMAGEIO_FFMPEG_EXE'] = '/usr/local/bin/ffmpeg'

def create_tiktok_video(
    script: str,
    audio_path: str,
    background_path: str,
    output_path: str,
    subtitle_color: str = "white",
    subtitle_size: int = 40
) -> str:
    try:
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        
        bg_ext = Path(background_path).suffix.lower()
        
        if bg_ext in ['.jpg', '.jpeg', '.png', '.webp']:
            video = ImageClip(background_path, duration=audio_duration)
        else:
            video = VideoFileClip(background_path)
            
            if video.duration > audio_duration:
                video = video.subclip(0, audio_duration)
            elif video.duration < audio_duration:
                video = video.loop(duration=audio_duration)
        
        video = video.resize(height=1920)
        video = video.crop(x1=video.size[0]//2 - 540, y1=0, x2=video.size[0]//2 + 540, y2=1920)
        
        subtitle_lines = wrap_text(script, max_chars=20)
        subtitles = []
        
        line_duration = audio_duration / len(subtitle_lines)
        
        for i, line in enumerate(subtitle_lines):
            try:
                txt_clip = TextClip(
                    line,
                    fontsize=subtitle_size,
                    color=subtitle_color,
                    font='Arial',
                    method='label',
                    size=(1000, None)
                ).set_position('center', 'bottom').set_start(i * line_duration).set_duration(line_duration)
                subtitles.append(txt_clip)
            except Exception as text_error:
                print(f"Error creating text clip: {text_error}")
                continue
        
        if subtitles:
            final_video = CompositeVideoClip([video] + subtitles)
        else:
            final_video = video
        
        final_video = final_video.set_audio(audio)
        
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            preset='ultrafast',
            threads=2
        )
        
        video.close()
        audio.close()
        final_video.close()
        
        return output_path
        
    except Exception as e:
        print(f"Error creating video: {e}")
        raise

def wrap_text(text: str, max_chars: int = 20) -> list[str]:
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line = current_line + " " + word if current_line else word
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines if lines else [text]
