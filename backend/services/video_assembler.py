from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, TextClip, CompositeVideoClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from pathlib import Path

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
            
            w, h = video.size
            
            def pan_zoom_effect(get_frame, t):
                import numpy as np
                from PIL import Image
                
                frame = get_frame(t)
                
                zoom_factor = 1 + (t / audio_duration) * 0.3
                
                new_w = int(w * zoom_factor)
                new_h = int(h * zoom_factor)
                
                img = Image.fromarray(frame)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                
                progress = t / audio_duration
                x_offset = int((new_w - w) * (0.5 + 0.3 * progress))
                y_offset = int((new_h - h) * (0.5 + 0.2 * progress))
                
                img = img.crop((x_offset, y_offset, x_offset + w, y_offset + h))
                return np.array(img)
            
            from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
            frames = [pan_zoom_effect(video.get_frame, t / 30) for t in range(0, int(audio_duration * 30))]
            video = ImageSequenceClip(frames, fps=30)
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
            txt_clip = TextClip(
                line,
                fontsize=subtitle_size,
                color=subtitle_color,
                font='Arial-Bold',
                stroke_color='black',
                stroke_width=2,
                align='center',
                method='caption'
            ).set_position('center').set_start(i * line_duration).set_duration(line_duration)
            
            subtitles.append(txt_clip)
        
        final_video = CompositeVideoClip([video] + subtitles)
        final_video = final_video.set_audio(audio)
        
        final_video.write_videofile(
            output_path,
            fps=30,
            codec='libx264',
            audio_codec='aac',
            preset='fast',
            threads=4
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
