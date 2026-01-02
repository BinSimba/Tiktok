from pathlib import Path

def generate_ai_video_free(prompt: str, output_path: str) -> bool:
    """
    Generate AI video using free alternatives.
    Uses Pollinations AI for images + MoviePy for animation.
    """
    try:
        from services.ai_image_generator import generate_ai_image
        
        output_path = Path(output_path)
        
        print(f"🎬 Generating AI video (free) for: {prompt[:50]}...")
        
        image_path = output_path.parent / f"{output_path.stem}_temp.jpg"
        
        success = generate_ai_image(prompt, str(image_path))
        
        if success:
            success = create_animated_video_from_image(str(image_path), str(output_path))
            if success:
                print(f"✅ AI video saved to: {output_path}")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error generating AI video: {e}")
        return False


def create_animated_video_from_image(image_path: str, output_path: str) -> bool:
    """
    Create an animated video from a static image using MoviePy.
    This is a free alternative to paid AI video generation.
    """
    try:
        from moviepy.editor import ImageClip
        import numpy as np
        from PIL import Image
        
        print("   Creating animated video from image...")
        
        image = ImageClip(image_path, duration=5)
        w, h = image.size
        
        def dynamic_animation(get_frame, t):
            frame = get_frame(t)
            
            progress = t / 5
            
            zoom = 1 + 0.4 * np.sin(progress * np.pi)
            
            new_w = int(w * zoom)
            new_h = int(h * zoom)
            
            img = Image.fromarray(frame)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            
            pan_x = int((new_w - w) * (0.3 + 0.4 * np.sin(progress * 2 * np.pi)))
            pan_y = int((new_h - h) * (0.3 + 0.4 * np.cos(progress * 2 * np.pi)))
            
            img = img.crop((pan_x, pan_y, pan_x + w, pan_y + h))
            
            return np.array(img)
        
        frames = [dynamic_animation(image.get_frame, t / 30) for t in range(0, 150)]
        
        from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
        video = ImageSequenceClip(frames, fps=30)
        
        video.write_videofile(output_path, codec='libx264', fps=30, audio=False, verbose=False)
        
        print("   ✅ Animation complete!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating animated video: {e}")
        return False
