import numpy as np
import cv2
from pathlib import Path
from typing import Dict, List, Optional
import uuid
from moviepy.editor import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.fx.all import audio_loop

from services.advanced_video_engine import AdvancedVideoEngine, VideoConfig, VideoStyle, QualityPreset, CameraMovement
from services.advanced_character_animator import AdvancedCharacterAnimator, EmotionType
import requests
import urllib.parse

class UnifiedVideoGenerator:
    def __init__(self):
        self.video_engine = AdvancedVideoEngine()
        self.character_animator = AdvancedCharacterAnimator()
        
    def generate_cinematic_video(self, prompt: str, audio_path: str, output_path: str,
                                  style: str = "cinematic", quality: str = "balanced",
                                  camera_movement: str = "static", duration: float = 5.0) -> str:
        try:
            print(f"\n{'='*60}")
            print(f"🎬 Generating Advanced AI Video")
            print(f"{'='*60}")
            print(f"📝 Prompt: {prompt[:100]}...")
            print(f"🎨 Style: {style}")
            print(f"⚙️  Quality: {quality}")
            print(f"📷 Camera: {camera_movement}")
            print(f"⏱️  Duration: {duration}s")
            print(f"{'='*60}\n")
            
            video_style = VideoStyle(style)
            quality_preset = QualityPreset[quality.upper()]
            camera = CameraMovement(camera_movement)
            
            config = VideoConfig(
                style=video_style,
                quality=quality_preset,
                camera_movement=camera,
                duration=duration,
                enable_optical_flow=True,
                enable_style_transfer=True,
                enable_lighting_effects=True,
                enable_atmospheric_effects=True
            )
            
            frames = self.video_engine.generate_video_frames(config, prompt)
            
            print(f"\n🎬 Composing video from {len(frames)} frames...")
            
            clip = ImageSequenceClip(frames, fps=quality_preset.value["fps"])
            
            audio_clip = AudioFileClip(audio_path)
            
            if audio_clip.duration > duration:
                audio_clip = audio_clip.subclip(0, duration)
            elif audio_clip.duration < duration:
                audio_clip = audio_loop(audio_clip, duration=duration)
            
            final_clip = clip.set_audio(audio_clip)
            
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            final_clip.write_videofile(
                output_path,
                fps=quality_preset.value["fps"],
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                bitrate=quality_preset.value["bitrate"],
                threads=4,
                logger=None
            )
            
            clip.close()
            audio_clip.close()
            final_clip.close()
            
            print(f"\n✅ Advanced video created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"\n❌ Error generating cinematic video: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def generate_character_video(self, prompt: str, audio_path: str, output_path: str,
                                  character_type: str = "person", emotion: str = "neutral",
                                  quality: str = "balanced", duration: float = 5.0) -> str:
        try:
            print(f"\n{'='*60}")
            print(f"🎭 Generating Advanced Character Video")
            print(f"{'='*60}")
            print(f"📝 Prompt: {prompt[:100]}...")
            print(f"👤 Character: {character_type}")
            print(f"😊 Emotion: {emotion}")
            print(f"⚙️  Quality: {quality}")
            print(f"⏱️  Duration: {duration}s")
            print(f"{'='*60}\n")
            
            character_prompt = self._get_character_prompt(character_type)
            full_prompt = f"{character_prompt} {prompt}"
            
            cleaned_prompt = full_prompt.replace('\n', ' ').replace('\r', ' ')
            cleaned_prompt = ' '.join(cleaned_prompt.split())
            cleaned_prompt = cleaned_prompt[:200]
            
            encoded_prompt = urllib.parse.quote(cleaned_prompt)
            
            quality_preset = QualityPreset[quality.upper()]
            resolution = quality_preset.value["resolution"]
            
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={resolution[0]}&height={resolution[1]}&nologo=true&seed={uuid.uuid4().hex[:8]}"
            
            print(f"📥 Generating character image...")
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()
            
            temp_dir = Path("/tmp/output")
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            temp_image_path = temp_dir / f"char_{uuid.uuid4().hex}.png"
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Character image generated: {temp_image_path}")
            
            emotion_enum = EmotionType(emotion)
            
            video_path = self.character_animator.create_animated_video(
                base_image_path=str(temp_image_path),
                audio_path=audio_path,
                output_path=output_path,
                emotion=emotion_enum,
                duration=duration,
                fps=quality_preset.value["fps"]
            )
            
            temp_image_path.unlink(missing_ok=True)
            
            print(f"\n✅ Advanced character video created successfully: {video_path}")
            return video_path
            
        except Exception as e:
            print(f"\n❌ Error generating character video: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _get_character_prompt(self, character_type: str) -> str:
        character_prompts = {
            "person": "professional portrait, realistic human, clear face, high detail",
            "monkey": "realistic wise monkey, intelligent looking, detailed fur, clear face",
            "anime": "anime character, vibrant colors, clean lines, studio ghibli style",
            "cartoon": "cartoon character, colorful, expressive face, 3d render style",
            "robot": "futuristic robot, advanced AI, mechanical details, glowing eyes",
            "animal": "realistic animal, detailed fur, expressive face, natural lighting",
            "fantasy": "fantasy character, magical, ethereal, detailed features",
            "cyborg": "cyborg character, half human half machine, neon accents"
        }
        return character_prompts.get(character_type, "professional portrait, realistic human, clear face")
    
    def generate_hybrid_video(self, prompt: str, audio_path: str, output_path: str,
                              style: str = "cinematic", character_type: str = "person",
                              emotion: str = "neutral", quality: str = "balanced",
                              camera_movement: str = "static", duration: float = 5.0) -> str:
        try:
            print(f"\n{'='*60}")
            print(f"🎬 Generating Hybrid Video (Character + Background)")
            print(f"{'='*60}\n")
            
            character_prompt = self._get_character_prompt(character_type)
            character_image_url = self._generate_character_image(character_prompt, quality)
            
            background_frames = self._generate_background_frames(prompt, style, quality, camera_movement, duration)
            
            video_path = self._compose_hybrid_video(
                character_image_url=character_image_url,
                background_frames=background_frames,
                audio_path=audio_path,
                output_path=output_path,
                emotion=emotion,
                quality=quality,
                duration=duration
            )
            
            print(f"\n✅ Hybrid video created successfully: {video_path}")
            return video_path
            
        except Exception as e:
            print(f"\n❌ Error generating hybrid video: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _generate_character_image(self, prompt: str, quality: str) -> str:
        cleaned_prompt = prompt.replace('\n', ' ').replace('\r', ' ')
        cleaned_prompt = ' '.join(cleaned_prompt.split())
        cleaned_prompt = cleaned_prompt[:200]
        
        quality_preset = QualityPreset[quality.upper()]
        resolution = quality_preset.value["resolution"]
        width, height = resolution
        
        from services.ai_image_generator import get_cached_image, cache_image
        cached_path = get_cached_image(cleaned_prompt, width, height)
        if cached_path:
            print(f"🔄 Using cached character image from: {cached_path}")
            return f"file://{cached_path}"
        
        encoded_prompt = urllib.parse.quote(cleaned_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={uuid.uuid4().hex[:8]}"
        
        max_retries = 5
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                print(f"📥 Attempt {attempt + 1}/{max_retries}: Fetching character image from: {image_url}")
                response = requests.get(image_url, timeout=60)
                
                print(f"📊 Response status: {response.status_code}, content length: {len(response.content)}")
                
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
                    print(f"⏳ Rate limit reached. Waiting {retry_after}s before retry...")
                    import time
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                
                cached_path = cache_image(cleaned_prompt, response.content, width, height)
                if cached_path:
                    print(f"✅ Character image cached: {cached_path}")
                    return f"file://{cached_path}"
                
                return image_url
                
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout on attempt {attempt + 1}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"⏳ Waiting {delay}s before retry...")
                    import time
                    time.sleep(delay)
                continue
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print(f"🚫 Rate limit on attempt {attempt + 1}")
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        print(f"⏳ Waiting {delay}s before retry...")
                        import time
                        time.sleep(delay)
                    continue
                else:
                    raise
        
        print(f"❌ Max retries reached for character image generation")
        return image_url
    
    def _generate_background_frames(self, prompt: str, style: str, quality: str, 
                                     camera_movement: str, duration: float) -> List[np.ndarray]:
        video_style = VideoStyle(style)
        quality_preset = QualityPreset[quality.upper()]
        camera = CameraMovement(camera_movement)
        
        config = VideoConfig(
            style=video_style,
            quality=quality_preset,
            camera_movement=camera,
            duration=duration,
            enable_optical_flow=True,
            enable_style_transfer=True,
            enable_lighting_effects=True,
            enable_atmospheric_effects=True
        )
        
        return self.video_engine.generate_video_frames(config, prompt)
    
    def _compose_hybrid_video(self, character_image_url: str, background_frames: List[np.ndarray],
                               audio_path: str, output_path: str, emotion: str,
                               quality: str, duration: float) -> str:
        import requests
        from PIL import Image
        
        response = requests.get(character_image_url, timeout=60)
        response.raise_for_status()
        
        temp_dir = Path("/tmp/output")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_char_path = temp_dir / f"char_{uuid.uuid4().hex}.png"
        with open(temp_char_path, 'wb') as f:
            f.write(response.content)
        
        char_img = Image.open(temp_char_path)
        char_array = np.array(char_img)
        
        if char_img.mode != 'RGB':
            char_img = char_img.convert('RGB')
            char_array = np.array(char_img)
        
        quality_preset = QualityPreset[quality.upper()]
        fps = quality_preset.value["fps"]
        total_frames = len(background_frames)
        
        combined_frames = []
        
        for i, bg_frame in enumerate(background_frames):
            h, w = bg_frame.shape[:2]
            
            char_resized = cv2.resize(char_array, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
            
            char_x = w - char_resized.shape[1] - 50
            char_y = h - char_resized.shape[0] - 100
            
            combined = bg_frame.copy()
            
            if char_x >= 0 and char_y >= 0:
                mask = np.zeros((char_resized.shape[0], char_resized.shape[1]), dtype=np.uint8)
                cv2.circle(mask, 
                          (char_resized.shape[1] // 2, char_resized.shape[0] // 2), 
                          min(char_resized.shape[:2]) // 2, 255, -1)
                
                mask = mask / 255.0
                mask = mask[:, :, np.newaxis]
                
                char_region = combined[char_y:char_y + char_resized.shape[0], 
                                      char_x:char_x + char_resized.shape[1]]
                
                blended = (char_region * (1 - mask * 0.3) + char_resized * mask * 0.3).astype(np.uint8)
                
                combined[char_y:char_y + char_resized.shape[0], 
                        char_x:char_x + char_resized.shape[1]] = blended
            
            combined_frames.append(combined)
        
        clip = ImageSequenceClip(combined_frames, fps=fps)
        
        audio_clip = AudioFileClip(audio_path)
        
        if audio_clip.duration > duration:
            audio_clip = audio_clip.subclip(0, duration)
        elif audio_clip.duration < duration:
            audio_clip = audio_loop(audio_clip, duration=duration)
        
        final_clip = clip.set_audio(audio_clip)
        
        final_clip.write_videofile(
            output_path,
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            bitrate=quality_preset.value["bitrate"],
            threads=4,
            logger=None
        )
        
        clip.close()
        audio_clip.close()
        final_clip.close()
        
        temp_char_path.unlink(missing_ok=True)
        
        return output_path

def generate_advanced_video(prompt: str, audio_path: str, output_path: str,
                            video_type: str = "cinematic", style: str = "cinematic",
                            character_type: str = "person", emotion: str = "neutral",
                            quality: str = "balanced", camera_movement: str = "static",
                            duration: float = 5.0) -> str:
    generator = UnifiedVideoGenerator()
    
    if video_type == "cinematic":
        return generator.generate_cinematic_video(prompt, audio_path, output_path, 
                                                   style, quality, camera_movement, duration)
    elif video_type == "character":
        return generator.generate_character_video(prompt, audio_path, output_path,
                                                    character_type, emotion, quality, duration)
    elif video_type == "hybrid":
        return generator.generate_hybrid_video(prompt, audio_path, output_path,
                                               style, character_type, emotion, quality,
                                               camera_movement, duration)
    else:
        raise ValueError(f"Unknown video type: {video_type}")
