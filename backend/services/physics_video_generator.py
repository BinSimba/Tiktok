import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
from pathlib import Path
import random
import math
import time
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import requests
import urllib.parse
from services.ai_image_generator import get_cached_image, cache_image

class PhysicsType(Enum):
    GRAVITY = "gravity"
    FLUID = "fluid"
    COLLISION = "collision"
    EXPLOSION = "explosion"
    WIND = "wind"
    SMOKE = "smoke"
    FIRE = "fire"

class Particle:
    def __init__(self, x: float, y: float, vx: float = 0.0, vy: float = 0.0, 
                 size: float = 5.0, color: Tuple[int, int, int] = (255, 255, 255),
                 lifetime: float = 1.0, physics_type: PhysicsType = PhysicsType.GRAVITY):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.size = size
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.physics_type = physics_type
        self.gravity = 9.8
        self.drag = 0.99
        self.elasticity = 0.7
        self.mass = size * 0.1
        self.rotation = random.uniform(0, 360)
        self.angular_velocity = random.uniform(-5, 5)
        self.trail = []
        self.max_trail_length = 5

    def update(self, dt: float, width: int, height: int, obstacles: List[Dict] = None):
        if self.lifetime <= 0:
            return

        if obstacles is None:
            obstacles = []

        if self.physics_type == PhysicsType.FLUID:
            self._update_fluid(dt, width, height)
        elif self.physics_type == PhysicsType.EXPLOSION:
            self._update_explosion(dt)
        elif self.physics_type == PhysicsType.WIND:
            self._update_wind(dt, width, height)
        elif self.physics_type == PhysicsType.SMOKE:
            self._update_smoke(dt)
        elif self.physics_type == PhysicsType.FIRE:
            self._update_fire(dt)
        else:
            self._update_gravity(dt, width, height)

        for obstacle in obstacles:
            self._check_collision(obstacle)

        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        self.lifetime -= dt
        self.rotation += self.angular_velocity * dt

    def _update_gravity(self, dt: float, width: int, height: int):
        self.vy += self.gravity * dt * 50
        self.vx *= self.drag
        self.vy *= self.drag
        self.x += self.vx * dt * 50
        self.y += self.vy * dt * 50

        if self.y + self.size > height:
            self.y = height - self.size
            self.vy *= -self.elasticity
            self.vx *= 0.9
            if abs(self.vy) < 1:
                self.vy = 0

        if self.x < self.size:
            self.x = self.size
            self.vx *= -self.elasticity
        elif self.x > width - self.size:
            self.x = width - self.size
            self.vx *= -self.elasticity

    def _update_fluid(self, dt: float, width: int, height: int):
        self.gravity = 5.0
        self.drag = 0.95
        self.elasticity = 0.3

        self.vy += self.gravity * dt * 30
        self.vx *= self.drag
        self.vy *= self.drag

        turbulence_x = math.sin(self.y * 0.02 + time.time() * 2) * 2
        turbulence_y = math.cos(self.x * 0.02 + time.time() * 2) * 1

        self.vx += turbulence_x
        self.vy += turbulence_y

        self.x += self.vx * dt * 50
        self.y += self.vy * dt * 50

        surface_y = height * 0.7
        if self.y > surface_y:
            self.y = surface_y + (surface_y - self.y) * 0.3
            self.vy *= -0.2
            self.vx += random.uniform(-2, 2)

        if self.x < self.size:
            self.x = self.size
            self.vx *= -0.5
        elif self.x > width - self.size:
            self.x = width - self.size
            self.vx *= -0.5

    def _update_explosion(self, dt: float):
        self.drag = 0.92
        self.gravity = 2.0

        self.vy += self.gravity * dt * 30
        self.vx *= self.drag
        self.vy *= self.drag

        self.x += self.vx * dt * 50
        self.y += self.vy * dt * 50

    def _update_wind(self, dt: float, width: int, height: int):
        self.gravity = 1.0
        self.drag = 0.99

        wind_force = 15.0
        wind_variation = math.sin(time.time() * 3 + self.y * 0.01) * 5

        self.vx += (wind_force + wind_variation) * dt * 10
        self.vy += self.gravity * dt * 10

        self.vx *= self.drag
        self.vy *= self.drag

        self.x += self.vx * dt * 50
        self.y += self.vy * dt * 50

        if self.y > height - self.size:
            self.y = height - self.size
            self.vy *= -0.3
        if self.x < self.size:
            self.x = self.size
            self.vx *= -0.5
        elif self.x > width - self.size:
            self.x = width - self.size
            self.vx *= -0.5

    def _update_smoke(self, dt: float):
        self.gravity = -3.0
        self.drag = 0.98
        self.size += 0.5

        self.vy += self.gravity * dt * 20
        self.vx *= self.drag
        self.vy *= self.drag

        turbulence = math.sin(time.time() * 2 + self.x * 0.01) * 0.5
        self.vx += turbulence

        self.x += self.vx * dt * 30
        self.y += self.vy * dt * 30

        self.lifetime -= dt * 0.5

    def _update_fire(self, dt: float):
        self.gravity = -8.0
        self.drag = 0.95

        self.vy += self.gravity * dt * 30
        self.vx *= self.drag
        self.vy *= self.drag

        turbulence = math.sin(time.time() * 5 + self.x * 0.02) * 2
        self.vx += turbulence

        self.x += self.vx * dt * 40
        self.y += self.vy * dt * 40

        self.size *= 0.98
        self.lifetime -= dt * 1.5

    def _check_collision(self, obstacle: Dict):
        ox, oy, ow, oh = obstacle.get('x', 0), obstacle.get('y', 0), obstacle.get('width', 0), obstacle.get('height', 0)

        if (self.x + self.size > ox and self.x - self.size < ox + ow and
            self.y + self.size > oy and self.y - self.size < oy + oh):

            overlap_left = self.x + self.size - ox
            overlap_right = ox + ow - (self.x - self.size)
            overlap_top = self.y + self.size - oy
            overlap_bottom = oy + oh - (self.y - self.size)

            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_left:
                self.x = ox - self.size
                self.vx *= -self.elasticity
            elif min_overlap == overlap_right:
                self.x = ox + ow + self.size
                self.vx *= -self.elasticity
            elif min_overlap == overlap_top:
                self.y = oy - self.size
                self.vy *= -self.elasticity
            elif min_overlap == overlap_bottom:
                self.y = oy + oh + self.size
                self.vy *= -self.elasticity

    def draw(self, frame: np.ndarray) -> np.ndarray:
        if self.lifetime <= 0:
            return frame

        alpha = self.lifetime / self.max_lifetime
        alpha = max(0, min(1, alpha))

        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                t_alpha = (i / len(self.trail)) * alpha * 0.5
                pt1 = (int(self.trail[i][0]), int(self.trail[i][1]))
                pt2 = (int(self.trail[i+1][0]), int(self.trail[i+1][1]))
                color = [int(c * t_alpha) for c in self.color]
                cv2.line(frame, pt1, pt2, color, 2)

        if self.physics_type in [PhysicsType.FLUID, PhysicsType.FIRE]:
            gradient_frame = self._draw_fluid_gradient(frame, alpha)
        else:
            gradient_frame = self._draw_particle(frame, alpha)

        return gradient_frame

    def _draw_particle(self, frame: np.ndarray, alpha: float) -> np.ndarray:
        x, y = int(self.x), int(self.y)
        radius = int(self.size)

        overlay = frame.copy()

        color = [int(c * alpha) for c in self.color]

        cv2.circle(overlay, (x, y), radius, color, -1)

        highlight = [min(255, c + 50) for c in color]
        cv2.circle(overlay, (x - radius//3, y - radius//3), radius//3, highlight, -1)

        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        return frame

    def _draw_fluid_gradient(self, frame: np.ndarray, alpha: float) -> np.ndarray:
        x, y = int(self.x), int(self.y)
        radius = int(self.size * 1.5)

        for i in range(radius, 0, -2):
            gradient_alpha = (1 - i / radius) * alpha * 0.3
            color = [int(c * gradient_alpha) for c in self.color]
            cv2.circle(frame, (x, y), i, color, -1)

        return frame

@dataclass
class PhysicsConfig:
    enable_physics: bool = True
    enable_fluid: bool = True
    enable_particles: bool = True
    gravity: float = 9.8
    air_resistance: float = 0.99
    simulation_steps: int = 2

class PhysicsVideoGenerator:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.particles: List[Particle] = []
        self.obstacles: List[Dict] = []

    def parse_scene_description(self, prompt: str) -> Dict:
        scene_data = {
            'main_objects': [],
            'physics_effects': [],
            'camera_moves': [],
            'lighting': [],
            'transitions': []
        }

        prompt_lower = prompt.lower()

        if any(word in prompt_lower for word in ['water', 'liquid', 'juice', 'drop', 'splash']):
            scene_data['physics_effects'].append(PhysicsType.FLUID)
            scene_data['main_objects'].append('liquid')

        if any(word in prompt_lower for word in ['falling', 'drop', 'gravity']):
            scene_data['physics_effects'].append(PhysicsType.GRAVITY)

        if any(word in prompt_lower for word in ['glass', 'table', 'wood', 'surface']):
            scene_data['main_objects'].append('solid')
            self.obstacles.append({'x': 0, 'y': int(self.height * 0.7), 'width': self.width, 'height': int(self.height * 0.3)})

        if any(word in prompt_lower for word in ['explosion', 'burst', 'explode']):
            scene_data['physics_effects'].append(PhysicsType.EXPLOSION)

        if any(word in prompt_lower for word in ['wind', 'blow', 'breeze']):
            scene_data['physics_effects'].append(PhysicsType.WIND)

        if any(word in prompt_lower for word in ['smoke', 'steam', 'mist']):
            scene_data['physics_effects'].append(PhysicsType.SMOKE)

        if any(word in prompt_lower for word in ['fire', 'flame', 'burn']):
            scene_data['physics_effects'].append(PhysicsType.FIRE)

        if any(word in prompt_lower for word in ['slow motion', 'slow-mo', 'slowmo']):
            scene_data['camera_moves'].append('slow_motion')

        if any(word in prompt_lower for word in ['sunlight', 'warm', 'light']):
            scene_data['lighting'].append('warm')

        return scene_data

    def generate_keyframe_images(self, prompt: str, scene_data: Dict, num_keyframes: int = 5) -> List[str]:
        print(f"🎨 Generating {num_keyframes} keyframe images...")

        keyframe_prompts = self._generate_keyframe_prompts(prompt, scene_data, num_keyframes)
        keyframe_paths = []

        for i, kf_prompt in enumerate(keyframe_prompts):
            keyframe_path = Path("/tmp/output") / f"keyframe_{random.randint(10000, 99999)}_{i}.png"
            keyframe_path.parent.mkdir(parents=True, exist_ok=True)

            success = self._fetch_image_with_retry(kf_prompt, str(keyframe_path), self.width, self.height)

            if success:
                keyframe_paths.append(str(keyframe_path))
                print(f"✅ Keyframe {i+1}/{num_keyframes} generated")
            else:
                print(f"❌ Failed to generate keyframe {i+1}")

        return keyframe_paths

    def _generate_keyframe_prompts(self, prompt: str, scene_data: Dict, num_keyframes: int) -> List[str]:
        keyframe_prompts = []

        for i in range(num_keyframes):
            progress = i / (num_keyframes - 1) if num_keyframes > 1 else 0

            modified_prompt = str(prompt)

            if 'liquid' in scene_data['main_objects']:
                if progress < 0.3:
                    modified_prompt = f"close-up, transparent glass with orange juice falling in slow motion, {prompt}"
                elif progress < 0.6:
                    modified_prompt = f"glass hitting wooden table, orange juice splashing in droplets, {prompt}"
                else:
                    modified_prompt = f"orange juice droplet rolling across wood grain texture, warm sunlight, {prompt}"

            if 'slow_motion' in scene_data['camera_moves']:
                modified_prompt = f"slow motion, {modified_prompt}"

            if 'warm' in scene_data['lighting']:
                modified_prompt = f"warm golden hour lighting, {modified_prompt}"

            modified_prompt = f"cinematic, 8k, ultra detailed, {modified_prompt}"
            modified_prompt = modified_prompt[:300]

            keyframe_prompts.append(modified_prompt)

        return keyframe_prompts

    def _fetch_image_with_retry(self, prompt: str, output_path: str, width: int, height: int, max_retries: int = 5) -> bool:
        try:
            cleaned_prompt = prompt.replace('\n', ' ').replace('\r', ' ')
            cleaned_prompt = ' '.join(cleaned_prompt.split())
            cleaned_prompt = cleaned_prompt[:200]

            cached_path = get_cached_image(cleaned_prompt, width, height)
            if cached_path:
                print(f"🔄 Using cached keyframe from: {cached_path}")
                import shutil
                shutil.copy2(cached_path, output_path)
                return True

            encoded_prompt = urllib.parse.quote(cleaned_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&nologo=true&seed={random.randint(1, 10000)}"

            base_delay = 2

            for attempt in range(max_retries):
                try:
                    print(f"📥 Attempt {attempt + 1}/{max_retries}: Fetching keyframe...")
                    response = requests.get(image_url, timeout=60)

                    if response.status_code == 429:
                        retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
                        print(f"⏳ Rate limit. Waiting {retry_after}s...")
                        time.sleep(retry_after)
                        continue

                    response.raise_for_status()

                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(response.content)

                    cache_image(cleaned_prompt, response.content, width, height)

                    return True

                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
                    continue
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429 and attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)
                        time.sleep(delay)
                        continue
                    raise

            return False

        except Exception as e:
            print(f"❌ Error fetching keyframe: {e}")
            return False

    def interpolate_frames(self, keyframe1: np.ndarray, keyframe2: np.ndarray, 
                          num_intermediate: int) -> List[np.ndarray]:
        print(f"🔄 Interpolating {num_intermediate} frames between keyframes...")

        flow = cv2.calcOpticalFlowFarneback(
            cv2.cvtColor(keyframe1, cv2.COLOR_RGB2GRAY),
            cv2.cvtColor(keyframe2, cv2.COLOR_RGB2GRAY),
            None, 0.5, 3, 15, 3, 5, 1.2, 0
        )

        interpolated = []

        for i in range(1, num_intermediate + 1):
            alpha = i / (num_intermediate + 1)

            h, w = keyframe1.shape[:2]
            flow_map = np.zeros((h, w, 2), dtype=np.float32)

            y_coords, x_coords = np.mgrid[0:h, 0:w]
            flow_map[:, :, 0] = x_coords + flow[:, :, 0] * alpha
            flow_map[:, :, 1] = y_coords + flow[:, :, 1] * alpha

            warped1 = cv2.remap(keyframe1, flow_map, None, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            warped2 = cv2.remap(keyframe2, flow_map, None, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

            blended = cv2.addWeighted(warped1, 1 - alpha, warped2, alpha, 0)

            interpolated.append(blended)

        return interpolated

    def initialize_fluid_particles(self, center_x: float, center_y: float, count: int = 100) -> List[Particle]:
        particles = []

        colors = [
            (255, 165, 0),
            (255, 200, 50),
            (255, 140, 0),
            (255, 180, 80)
        ]

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 15)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed

            size = random.uniform(3, 12)
            color = random.choice(colors)
            lifetime = random.uniform(2.0, 5.0)

            p = Particle(center_x, center_y, vx, vy, size, color, lifetime, PhysicsType.FLUID)
            particles.append(p)

        return particles

    def update_particles(self, dt: float) -> None:
        for particle in self.particles:
            particle.update(dt, self.width, self.height, self.obstacles)

        self.particles = [p for p in self.particles if p.lifetime > 0]

    def render_particles(self, frame: np.ndarray) -> np.ndarray:
        for particle in self.particles:
            frame = particle.draw(frame)
        return frame

    def apply_post_processing(self, frame: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        frame = self._apply_motion_blur(frame, frame_num, total_frames)
        frame = self._apply_color_grading(frame)
        frame = self._apply_lens_effects(frame)

        return frame

    def _apply_motion_blur(self, frame: np.ndarray, frame_num: int, total_frames: int) -> np.ndarray:
        if frame_num % 3 != 0:
            return frame

        kernel_size = random.choice([3, 5, 7])
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size) / kernel_size

        blurred = cv2.filter2D(frame, -1, kernel)

        return blurred

    def _apply_color_grading(self, frame: np.ndarray) -> np.ndarray:
        frame = frame.astype(np.float32)

        frame[:, :, 0] = frame[:, :, 0] * 1.05
        frame[:, :, 1] = frame[:, :, 1] * 1.02
        frame[:, :, 2] = frame[:, :, 2] * 0.95

        frame = np.clip(frame, 0, 255)
        frame = frame.astype(np.uint8)

        return frame

    def _apply_lens_effects(self, frame: np.ndarray) -> np.ndarray:
        h, w = frame.shape[:2]

        lens_flare = self._create_lens_flare(w, h)

        frame = cv2.addWeighted(frame, 0.9, lens_flare, 0.1, 0)

        return frame

    def _create_lens_flare(self, width: int, height: int) -> np.ndarray:
        flare = np.zeros((height, width, 3), dtype=np.uint8)

        center_x, center_y = width // 2, height // 3

        for i in range(5):
            radius = random.randint(20, 100)
            alpha = random.randint(10, 50)

            cv2.circle(flare, (center_x, center_y), radius, (255, 255, 200), -1)

        return flare

    def generate_physics_video(self, prompt: str, duration: float = 5.0, fps: int = 30) -> List[np.ndarray]:
        print(f"🎬 Generating physics-based video: {prompt[:100]}...")

        scene_data = self.parse_scene_description(prompt)
        print(f"📊 Scene detected: {scene_data}")

        keyframe_paths = self.generate_keyframe_images(prompt, scene_data, num_keyframes=5)

        if not keyframe_paths:
            print("❌ No keyframes generated")
            return []

        keyframes = []
        for path in keyframe_paths:
            img = Image.open(path)
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            keyframes.append(np.array(img))

        total_frames = int(duration * fps)
        frames_per_keyframe = total_frames // len(keyframes)
        intermediate_frames = frames_per_keyframe - 1

        all_frames = []

        for i in range(len(keyframes)):
            current_keyframe = keyframes[i]
            all_frames.append(current_keyframe)

            if i < len(keyframes) - 1:
                next_keyframe = keyframes[i + 1]
                interpolated = self.interpolate_frames(current_keyframe, next_keyframe, intermediate_frames)
                all_frames.extend(interpolated)

        if PhysicsType.FLUID in scene_data['physics_effects']:
            print(f"💧 Initializing fluid particles...")
            self.particles = self.initialize_fluid_particles(self.width // 2, self.height // 2, count=200)

        for frame_num in range(len(all_frames)):
            dt = 1.0 / fps

            if PhysicsType.FLUID in scene_data['physics_effects']:
                if frame_num == int(total_frames * 0.3):
                    self.particles = self.initialize_fluid_particles(self.width // 2, self.height // 3, count=150)

                self.update_particles(dt)
                all_frames[frame_num] = self.render_particles(all_frames[frame_num])

            all_frames[frame_num] = self.apply_post_processing(all_frames[frame_num], frame_num, total_frames)

            if (frame_num + 1) % 10 == 0:
                print(f"  Progress: {frame_num + 1}/{total_frames} frames")

        for path in keyframe_paths:
            Path(path).unlink(missing_ok=True)

        print(f"✅ Physics video generated: {len(all_frames)} frames")
        return all_frames
