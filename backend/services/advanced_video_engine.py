import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pathlib import Path
import random
import math
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import torch
import torchvision.transforms as transforms
from torchvision.models import vgg19
import requests
import urllib.parse

class VideoStyle(Enum):
    CINEMATIC = "cinematic"
    ANIME = "anime"
    REALISTIC = "realistic"
    ABSTRACT = "abstract"
    VINTAGE = "vintage"
    NEON = "neon"
    NOIR = "noir"
    WATERCOLOR = "watercolor"

class QualityPreset(Enum):
    SPEED = {"fps": 15, "resolution": (720, 1280), "bitrate": "2000k"}
    BALANCED = {"fps": 30, "resolution": (1080, 1920), "bitrate": "5000k"}
    QUALITY = {"fps": 30, "resolution": (1080, 1920), "bitrate": "10000k"}
    HIGH = {"fps": 30, "resolution": (1440, 2560), "bitrate": "15000k"}
    ULTRA = {"fps": 60, "resolution": (2160, 3840), "bitrate": "25000k"}

class CameraMovement(Enum):
    STATIC = "static"
    SLOW_ZOOM_IN = "slow_zoom_in"
    SLOW_ZOOM_OUT = "slow_zoom_out"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ORBIT = "orbit"
    DOLLY = "dolly"
    CRANE = "crane"

@dataclass
class VideoConfig:
    style: VideoStyle = VideoStyle.CINEMATIC
    quality: QualityPreset = QualityPreset.BALANCED
    camera_movement: CameraMovement = CameraMovement.STATIC
    duration: float = 5.0
    enable_optical_flow: bool = True
    enable_style_transfer: bool = True
    enable_lighting_effects: bool = True
    enable_atmospheric_effects: bool = True

class AdvancedVideoEngine:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.optical_flow_cache = {}
        self.style_transfer_model = None
        self.load_style_transfer_model()
        
    def load_style_transfer_model(self):
        try:
            vgg = vgg19(pretrained=True).features.to(self.device).eval()
            self.style_transfer_model = vgg
            print("✅ Style transfer model loaded")
        except Exception as e:
            print(f"⚠️  Could not load style transfer model: {e}")
            self.style_transfer_model = None
    
    def generate_base_image(self, prompt: str, style: VideoStyle, output_path: str) -> bool:
        try:
            style_prefix = self._get_style_prefix(style)
            full_prompt = f"{style_prefix} {prompt}"
            
            cleaned_prompt = full_prompt.replace('\n', ' ').replace('\r', ' ')
            cleaned_prompt = ' '.join(cleaned_prompt.split())
            cleaned_prompt = cleaned_prompt[:200]
            
            width, height = 1080, 1920
            
            from services.ai_image_generator import get_cached_image, cache_image
            cached_path = get_cached_image(cleaned_prompt, width, height)
            if cached_path:
                print(f"🔄 Using cached base image from: {cached_path}")
                import shutil
                shutil.copy2(cached_path, output_path)
                print(f"✅ Cached base image saved: {output_path}")
                return True
            
            encoded_prompt = urllib.parse.quote(cleaned_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={random.randint(1, 10000)}"
            
            max_retries = 5
            base_delay = 2
            
            for attempt in range(max_retries):
                try:
                    print(f"📥 Attempt {attempt + 1}/{max_retries}: Fetching base image from: {image_url}")
                    response = requests.get(image_url, timeout=60)
                    
                    print(f"📊 Response status: {response.status_code}, content length: {len(response.content)}")
                    
                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
                        print(f"⏳ Rate limit reached. Waiting {retry_after}s before retry...")
                        import time
                        time.sleep(retry_after)
                        continue
                    
                    response.raise_for_status()
                    
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    cache_image(cleaned_prompt, response.content, width, height)
                    
                    print(f"✅ Base image generated: {output_path}")
                    return True
                    
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
            
            print(f"❌ Max retries reached for base image generation")
            return False
            
        except Exception as e:
            print(f"❌ Error generating base image: {e}")
            return False
    
    def _get_style_prefix(self, style: VideoStyle) -> str:
        style_prompts = {
            VideoStyle.CINEMATIC: "cinematic, film grain, professional lighting, depth of field, high dynamic range, dramatic",
            VideoStyle.ANIME: "anime style, vibrant colors, clean lines, studio ghibli inspired",
            VideoStyle.REALISTIC: "photorealistic, ultra detailed, 8k, sharp focus, natural lighting",
            VideoStyle.ABSTRACT: "abstract art, surreal, geometric shapes, vibrant colors, artistic",
            VideoStyle.VINTAGE: "vintage film, sepia tones, film grain, retro aesthetic",
            VideoStyle.NEON: "cyberpunk, neon lights, glowing, futuristic, synthwave",
            VideoStyle.NOIR: "film noir, black and white, high contrast, dramatic shadows",
            VideoStyle.WATERCOLOR: "watercolor painting, soft edges, artistic, hand-painted style"
        }
        return style_prompts.get(style, "")
    
    def apply_style_transfer(self, image_array: np.ndarray, style: VideoStyle, enable_style_transfer: bool = True) -> np.ndarray:
        if not enable_style_transfer or self.style_transfer_model is None:
            return image_array
        
        img = Image.fromarray(image_array)
        
        if style == VideoStyle.VINTAGE:
            return self._apply_vintage_filter(img)
        elif style == VideoStyle.NOIR:
            return self._apply_noir_filter(img)
        elif style == VideoStyle.NEON:
            return self._apply_neon_filter(img)
        elif style == VideoStyle.WATERCOLOR:
            return self._apply_watercolor_filter(img)
        elif style == VideoStyle.ANIME:
            return self._apply_anime_filter(img)
        
        return np.array(img)
    
    def _apply_vintage_filter(self, img: Image) -> np.ndarray:
        img = img.convert('RGB')
        
        sepia_matrix = [
            0.393, 0.769, 0.189,
            0.349, 0.686, 0.168,
            0.272, 0.534, 0.131
        ]
        
        sepia_img = img.convert('RGB')
        pixels = sepia_img.load()
        
        for i in range(sepia_img.size[0]):
            for j in range(sepia_img.size[1]):
                r, g, b = pixels[i, j]
                tr = int(r * sepia_matrix[0] + g * sepia_matrix[1] + b * sepia_matrix[2])
                tg = int(r * sepia_matrix[3] + g * sepia_matrix[4] + b * sepia_matrix[5])
                tb = int(r * sepia_matrix[6] + g * sepia_matrix[7] + b * sepia_matrix[8])
                pixels[i, j] = (min(255, tr), min(255, tg), min(255, tb))
        
        enhancer = ImageEnhance.Contrast(sepia_img)
        sepia_img = enhancer.enhance(1.2)
        
        enhancer = ImageEnhance.Brightness(sepia_img)
        sepia_img = enhancer.enhance(0.9)
        
        noise = np.random.randint(0, 30, (sepia_img.size[1], sepia_img.size[0], 3), dtype=np.uint8)
        sepia_array = np.array(sepia_img)
        sepia_array = cv2.add(sepia_array, noise)
        
        return sepia_array
    
    def _apply_noir_filter(self, img: Image) -> np.ndarray:
        img = img.convert('L')
        img = img.convert('RGB')
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.8)
        
        img_array = np.array(img)
        
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        img_array = cv2.equalizeHist(img_array)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        
        return img_array
    
    def _apply_neon_filter(self, img: Image) -> np.ndarray:
        img = img.convert('RGB')
        
        img_array = np.array(img)
        
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        h, s, v = cv2.split(hsv)
        
        s = cv2.multiply(s, 1.5)
        v = cv2.multiply(v, 1.2)
        
        hsv = cv2.merge([h, s, v])
        neon_array = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        glow = cv2.GaussianBlur(neon_array, (21, 21), 0)
        glow = cv2.addWeighted(neon_array, 0.7, glow, 0.3, 0)
        
        return glow
    
    def _apply_watercolor_filter(self, img: Image) -> np.ndarray:
        img = img.filter(ImageFilter.SMOOTH_MORE)
        img = img.filter(ImageFilter.SMOOTH_MORE)
        
        img_array = np.array(img)
        
        img_array = cv2.edgePreservingFilter(img_array, flags=1, sigma_s=60, sigma_r=0.4)
        
        img_array = cv2.stylization(img_array, sigma_s=150, sigma_r=0.25)
        
        return img_array
    
    def _apply_anime_filter(self, img: Image) -> np.ndarray:
        img = img.convert('RGB')
        img_array = np.array(img)
        
        edges = cv2.Canny(img_array, 100, 200)
        edges = cv2.dilate(edges, None)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        
        smoothed = cv2.bilateralFilter(img_array, 15, 80, 80)
        
        anime_array = cv2.addWeighted(smoothed, 0.9, edges, 0.1, 0)
        
        return anime_array
    
    def calculate_optical_flow(self, prev_frame: np.ndarray, curr_frame: np.ndarray) -> np.ndarray:
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_RGB2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_RGB2GRAY)
        
        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray, None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2,
            flags=0
        )
        
        return flow
    
    def apply_optical_flow_warp(self, frame: np.ndarray, flow: np.ndarray) -> np.ndarray:
        h, w = flow.shape[:2]
        
        flow = -flow
        
        flow[:, :, 0] += np.arange(w)
        flow[:, :, 1] += np.arange(h)[:, np.newaxis]
        
        warped = cv2.remap(frame, flow, None, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        
        return warped
    
    def apply_camera_movement(self, frame: np.ndarray, frame_num: int, total_frames: int, 
                             movement: CameraMovement) -> np.ndarray:
        if movement == CameraMovement.STATIC:
            return frame
        
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        
        progress = frame_num / max(total_frames - 1, 1)
        
        if movement == CameraMovement.SLOW_ZOOM_IN:
            scale = 1.0 + (progress * 0.3)
            return self._apply_zoom(frame, scale, center_x, center_y)
        
        elif movement == CameraMovement.SLOW_ZOOM_OUT:
            scale = 1.3 - (progress * 0.3)
            return self._apply_zoom(frame, scale, center_x, center_y)
        
        elif movement == CameraMovement.PAN_LEFT:
            shift_x = int(progress * w * 0.15)
            return self._apply_pan(frame, -shift_x, 0)
        
        elif movement == CameraMovement.PAN_RIGHT:
            shift_x = int(progress * w * 0.15)
            return self._apply_pan(frame, shift_x, 0)
        
        elif movement == CameraMovement.TILT_UP:
            shift_y = int(progress * h * 0.15)
            return self._apply_pan(frame, 0, -shift_y)
        
        elif movement == CameraMovement.TILT_DOWN:
            shift_y = int(progress * h * 0.15)
            return self._apply_pan(frame, 0, shift_y)
        
        elif movement == CameraMovement.ORBIT:
            angle = progress * 15
            return self._apply_rotation(frame, angle)
        
        elif movement == CameraMovement.DOLLY:
            scale = 1.0 + math.sin(progress * math.pi) * 0.2
            return self._apply_zoom(frame, scale, center_x, center_y)
        
        elif movement == CameraMovement.CRANE:
            shift_y = int(math.sin(progress * math.pi) * h * 0.1)
            return self._apply_pan(frame, 0, -shift_y)
        
        return frame
    
    def _apply_zoom(self, frame: np.ndarray, scale: float, center_x: int, center_y: int) -> np.ndarray:
        h, w = frame.shape[:2]
        
        new_w = int(w / scale)
        new_h = int(h / scale)
        
        x1 = max(0, center_x - new_w // 2)
        y1 = max(0, center_y - new_h // 2)
        x2 = min(w, x1 + new_w)
        y2 = min(h, y1 + new_h)
        
        cropped = frame[y1:y2, x1:x2]
        
        if cropped.size == 0:
            return frame
        
        zoomed = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
        
        return zoomed
    
    def _apply_pan(self, frame: np.ndarray, shift_x: int, shift_y: int) -> np.ndarray:
        h, w = frame.shape[:2]
        
        M = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        shifted = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
        return shifted
    
    def _apply_rotation(self, frame: np.ndarray, angle: float) -> np.ndarray:
        h, w = frame.shape[:2]
        center = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(frame, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        
        return rotated
    
    def apply_dynamic_lighting(self, frame: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        progress = frame_num / max(total_frames - 1, 1)
        
        frame_array = frame.astype(np.float32)
        
        brightness_variation = 0.05 * math.sin(progress * 2 * math.pi)
        frame_array = frame_array * (1.0 + brightness_variation)
        
        frame_array = np.clip(frame_array, 0, 255)
        
        return frame_array.astype(np.uint8)
    
    def apply_atmospheric_effects(self, frame: np.ndarray, frame_num: int) -> np.ndarray:
        h, w = frame.shape[:2]
        
        fog_density = 0.02 + 0.01 * math.sin(frame_num * 0.1)
        fog_color = np.array([200, 200, 210], dtype=np.float32)
        
        frame_array = frame.astype(np.float32)
        fogged = frame_array * (1 - fog_density) + fog_color * fog_density
        
        return fogged.astype(np.uint8)
    
    def create_temporal_smooth_transition(self, frame1: np.ndarray, frame2: np.ndarray, 
                                          alpha: float) -> np.ndarray:
        alpha = np.clip(alpha, 0, 1)
        
        blended = (frame1.astype(np.float32) * (1 - alpha) + 
                  frame2.astype(np.float32) * alpha)
        
        return blended.astype(np.uint8)
    
    def generate_video_frames(self, config: VideoConfig, prompt: str) -> List[np.ndarray]:
        print(f"🎬 Generating video frames with {config.style.value} style...")
        
        base_image_path = Path("/tmp/output") / f"base_{random.randint(10000, 99999)}.png"
        self.generate_base_image(prompt, config.style, str(base_image_path))
        
        base_img = Image.open(base_image_path)
        quality_settings = config.quality.value
        target_w, target_h = quality_settings["resolution"]
        
        base_img = base_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        base_array = np.array(base_img)
        
        if base_img.mode != 'RGB':
            base_img = base_img.convert('RGB')
        
        total_frames = int(config.duration * quality_settings["fps"])
        frames = []
        
        prev_frame = None
        prev_flow = None
        
        for frame_num in range(total_frames):
            frame = base_array.copy()
            
            frame = self.apply_style_transfer(frame, config.style, config.enable_style_transfer)
            
            if config.enable_lighting_effects:
                frame = self.apply_dynamic_lighting(frame, frame_num, total_frames)
            
            if config.enable_atmospheric_effects:
                frame = self.apply_atmospheric_effects(frame, frame_num)
            
            if prev_frame is not None and config.enable_optical_flow:
                flow = self.calculate_optical_flow(prev_frame, frame)
                
                flow_intensity = 0.3
                warped_frame = self.apply_optical_flow_warp(prev_frame, flow * flow_intensity)
                
                blend_alpha = 0.5 + 0.3 * math.sin(frame_num * 0.2)
                frame = self.create_temporal_smooth_transition(warped_frame, frame, blend_alpha)
            
            frame = self.apply_camera_movement(frame, frame_num, total_frames, config.camera_movement)
            
            frames.append(frame)
            prev_frame = frame.copy()
            
            if (frame_num + 1) % 10 == 0:
                print(f"  Progress: {frame_num + 1}/{total_frames} frames")
        
        base_image_path.unlink(missing_ok=True)
        
        return frames
