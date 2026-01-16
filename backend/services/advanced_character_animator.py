import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter
import math
from pathlib import Path
import librosa
import soundfile as sf
import mediapipe as mp
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class EmotionType(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    FEARFUL = "fearful"
    DISGUSTED = "disgusted"
    EXCITED = "excited"
    CALM = "calm"
    CONFIDENT = "confident"

class ExpressionIntensity(Enum):
    SUBTLE = 0.3
    MODERATE = 0.6
    STRONG = 0.9
    EXTREME = 1.2

@dataclass
class AnimationParams:
    eye_movement: bool = True
    eyebrow_movement: bool = True
    head_movement: bool = True
    breathing: bool = True
    micro_expressions: bool = True
    smooth_transitions: bool = True
    facial_symmetry: bool = True

class AdvancedCharacterAnimator:
    def __init__(self):
        self.width = 1080
        self.height = 1920
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.previous_landmarks = None
        self.emotion_history = []
        self.max_emotion_history = 10
        self.animation_params = AnimationParams()
        
    def analyze_audio_for_expression(self, audio_path: str) -> Dict:
        try:
            y, sr = librosa.load(audio_path)
            
            rms = librosa.feature.rms(y=y)[0]
            pitch = librosa.yin(y, fmin=50, fmax=400)
            pitch = pitch[~np.isnan(pitch)]
            
            energy = np.mean(rms)
            pitch_mean = np.mean(pitch) if len(pitch) > 0 else 150
            pitch_std = np.std(pitch) if len(pitch) > 0 else 20
            
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            
            zero_crossings = np.mean(librosa.feature.zero_crossing_rate(y))
            
            return {
                'energy': float(energy),
                'pitch_mean': float(pitch_mean),
                'pitch_std': float(pitch_std),
                'tempo': float(tempo),
                'sharpness': float(zero_crossings),
                'duration': librosa.get_duration(y=y, sr=sr)
            }
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            return {
                'energy': 0.5,
                'pitch_mean': 150,
                'pitch_std': 20,
                'tempo': 120,
                'sharpness': 0.1,
                'duration': 5.0
            }
    
    def map_audio_to_emotion(self, audio_features: Dict) -> EmotionType:
        energy = audio_features['energy']
        pitch_mean = audio_features['pitch_mean']
        pitch_std = audio_features['pitch_std']
        tempo = audio_features['tempo']
        
        if energy > 0.8 and tempo > 140:
            return EmotionType.EXCITED
        elif energy > 0.7 and pitch_mean > 200:
            return EmotionType.HAPPY
        elif energy < 0.3 and pitch_mean < 120:
            return EmotionType.SAD
        elif energy > 0.9 and pitch_std > 50:
            return EmotionType.ANGRY
        elif pitch_std > 60 and tempo > 130:
            return EmotionType.SURPRISED
        elif energy > 0.6 and pitch_mean > 180:
            return EmotionType.CONFIDENT
        elif energy < 0.5 and tempo < 100:
            return EmotionType.CALM
        else:
            return EmotionType.NEUTRAL
    
    def detect_detailed_landmarks(self, image_array: np.ndarray) -> Optional[Dict]:
        try:
            rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_image)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                h, w = image_array.shape[:2]
                
                def get_point(idx):
                    pt = landmarks.landmark[idx]
                    return (int(pt.x * w), int(pt.y * h))
                
                def get_bbox(idx1, idx2, idx3, idx4):
                    p1 = landmarks.landmark[idx1]
                    p2 = landmarks.landmark[idx2]
                    p3 = landmarks.landmark[idx3]
                    p4 = landmarks.landmark[idx4]
                    x_min = min(p1.x, p2.x, p3.x, p4.x) * w
                    x_max = max(p1.x, p2.x, p3.x, p4.x) * w
                    y_min = min(p1.y, p2.y, p3.y, p4.y) * h
                    y_max = max(p1.y, p2.y, p3.y, p4.y) * h
                    return (int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min))
                
                return {
                    'upper_lip': get_point(13),
                    'lower_lip': get_point(14),
                    'left_lip_corner': get_point(61),
                    'right_lip_corner': get_point(291),
                    'left_eye_center': get_point(468),
                    'right_eye_center': get_point(473),
                    'left_eyebrow_inner': get_point(65),
                    'left_eyebrow_outer': get_point(105),
                    'right_eyebrow_inner': get_point(295),
                    'right_eyebrow_outer': get_point(334),
                    'nose_tip': get_point(1),
                    'nose_bridge': get_point(168),
                    'chin': get_point(152),
                    'jaw_left': get_point(234),
                    'jaw_right': get_point(454),
                    'forehead_center': get_point(10),
                    'left_cheek': get_point(205),
                    'right_cheek': get_point(425),
                    'left_eye_bbox': get_bbox(33, 133, 468, 473),
                    'right_eye_bbox': get_bbox(362, 263, 473, 468),
                    'mouth_bbox': get_bbox(61, 291, 13, 14),
                    'face_bbox': get_bbox(234, 454, 10, 152),
                    'all_landmarks': landmarks
                }
            
            return None
            
        except Exception as e:
            print(f"Error detecting landmarks: {e}")
            return None
    
    def generate_per_frame_audio_intensity(self, audio_path: str, fps: int = 30) -> np.ndarray:
        try:
            y, sr = librosa.load(audio_path)
            duration = librosa.get_duration(y=y, sr=sr)
            total_frames = int(duration * fps)
            
            hop_length = int(sr / fps)
            rms = librosa.feature.rms(y=y, hop_length=hop_length)[0]
            
            pitch = librosa.yin(y, fmin=50, fmax=400)
            pitch = pitch[~np.isnan(pitch)]
            
            rms_normalized = rms / (np.max(rms) + 1e-6)
            
            if len(rms_normalized) < total_frames:
                rms_normalized = np.pad(rms_normalized, (0, total_frames - len(rms_normalized)))
            else:
                rms_normalized = rms_normalized[:total_frames]
            
            return rms_normalized
        except Exception as e:
            print(f"Error generating audio intensity: {e}")
            return np.ones(150) * 0.5
    
    def animate_mouth_advanced(self, image_array: np.ndarray, landmarks: Dict, 
                              audio_intensity: float, emotion: EmotionType) -> np.ndarray:
        if landmarks is None:
            return image_array
        
        h, w = image_array.shape[:2]
        
        upper_lip = landmarks['upper_lip']
        lower_lip = landmarks['lower_lip']
        left_corner = landmarks['left_lip_corner']
        right_corner = landmarks['right_lip_corner']
        chin = landmarks['chin']
        mouth_bbox = landmarks['mouth_bbox']
        
        emotion_intensity = self._get_emotion_intensity(emotion)
        base_opening = audio_intensity * 15 * emotion_intensity
        
        mouth_opening = int(base_opening)
        if mouth_opening < 1:
            return image_array
        
        mouth_width = right_corner[0] - left_corner[0]
        mouth_aspect_ratio = audio_intensity
        
        lower_lip_y, chin_y = lower_lip[1], chin[1]
        
        lower_face_start = lower_lip_y
        lower_face_end = min(chin_y + mouth_opening, h)
        
        if lower_face_end <= lower_face_start:
            return image_array
        
        lower_face = image_array[lower_face_start:lower_face_end, :].copy()
        if lower_face.shape[0] < 5:
            return image_array
        
        vertical_stretch = 1.0 + (mouth_opening / lower_face.shape[0]) * 0.5
        new_height = int(lower_face.shape[0] * vertical_stretch)
        
        if new_height <= 0:
            return image_array
        
        lower_face_resized = cv2.resize(lower_face, (lower_face.shape[1], new_height))
        
        target_end_y = lower_face_start + new_height
        if target_end_y > h:
            lower_face_resized = lower_face_resized[:h - lower_face_start]
            target_end_y = h
        
        if lower_face_resized.shape[0] < 1:
            return image_array
        
        current_lower_face = image_array[lower_face_start:target_end_y, :]
        
        alpha = np.linspace(0.7, 1.0, min(current_lower_face.shape[0], lower_face_resized.shape[0])).reshape(-1, 1, 1)
        alpha = alpha.astype(np.float32)
        
        blended = (current_lower_face.astype(np.float32) * alpha + 
                 lower_face_resized[:current_lower_face.shape[0]].astype(np.float32) * (1 - alpha)).astype(np.uint8)
        
        image_array[lower_face_start:target_end_y, :] = blended
        
        return image_array
    
    def _get_emotion_intensity(self, emotion: EmotionType) -> float:
        intensity_map = {
            EmotionType.NEUTRAL: 1.0,
            EmotionType.HAPPY: 1.2,
            EmotionType.SAD: 0.8,
            EmotionType.ANGRY: 1.3,
            EmotionType.SURPRISED: 1.4,
            EmotionType.EXCITED: 1.5,
            EmotionType.CALM: 0.9,
            EmotionType.CONFIDENT: 1.1
        }
        return intensity_map.get(emotion, 1.0)
    
    def animate_eyes(self, image_array: np.ndarray, landmarks: Dict, 
                    frame_num: int, emotion: EmotionType) -> np.ndarray:
        if landmarks is None or not self.animation_params.eye_movement:
            return image_array
        
        left_eye_center = landmarks['left_eye_center']
        right_eye_center = landmarks['right_eye_center']
        left_eye_bbox = landmarks['left_eye_bbox']
        right_eye_bbox = landmarks['right_eye_bbox']
        
        eye_movement_freq = 0.15
        eye_movement_amp = 3
        
        eye_offset_x = int(math.sin(frame_num * eye_movement_freq) * eye_movement_amp)
        eye_offset_y = int(math.cos(frame_num * eye_movement_freq * 0.7) * eye_movement_amp * 0.5)
        
        for eye_bbox in [left_eye_bbox, right_eye_bbox]:
            x, y, bw, bh = eye_bbox
            x = max(0, x + eye_offset_x)
            y = max(0, y + eye_offset_y)
            
            x2 = min(image_array.shape[1], x + bw)
            y2 = min(image_array.shape[0], y + bh)
            
            if x2 > x and y2 > y:
                eye_region = image_array[y:y2, x:x2]
                
                emotion_brightness = self._get_emotion_brightness(emotion)
                eye_region = eye_region.astype(np.float32) * emotion_brightness
                eye_region = np.clip(eye_region, 0, 255).astype(np.uint8)
                
                image_array[y:y2, x:x2] = eye_region
        
        return image_array
    
    def _get_emotion_brightness(self, emotion: EmotionType) -> float:
        brightness_map = {
            EmotionType.HAPPY: 1.15,
            EmotionType.SAD: 0.85,
            EmotionType.ANGRY: 0.95,
            EmotionType.SURPRISED: 1.2,
            EmotionType.EXCITED: 1.25,
            EmotionType.CALM: 1.0,
            EmotionType.NEUTRAL: 1.0,
            EmotionType.CONFIDENT: 1.1
        }
        return brightness_map.get(emotion, 1.0)
    
    def animate_eyebrows(self, image_array: np.ndarray, landmarks: Dict, 
                       frame_num: int, emotion: EmotionType) -> np.ndarray:
        if landmarks is None or not self.animation_params.eyebrow_movement:
            return image_array
        
        left_inner = landmarks['left_eyebrow_inner']
        left_outer = landmarks['left_eyebrow_outer']
        right_inner = landmarks['right_eyebrow_inner']
        right_outer = landmarks['right_eyebrow_outer']
        
        eyebrow_movement = self._get_eyebrow_movement(emotion)
        
        freq = 0.08
        offset_y = int(math.sin(frame_num * freq) * eyebrow_movement)
        
        for eyebrow in [(left_inner, left_outer), (right_inner, right_outer)]:
            inner, outer = eyebrow
            y_min = min(inner[1], outer[1]) + offset_y
            y_max = max(inner[1], outer[1]) + offset_y + 5
            x_min = min(inner[0], outer[0]) - 5
            x_max = max(inner[0], outer[0]) + 5
            
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = min(image_array.shape[1], x_max)
            y_max = min(image_array.shape[0], y_max)
            
            if x_max > x_min and y_max > y_min:
                eyebrow_region = image_array[y_min:y_max, x_min:x_max]
                eyebrow_region = cv2.GaussianBlur(eyebrow_region, (3, 3), 0)
                image_array[y_min:y_max, x_min:x_max] = eyebrow_region
        
        return image_array
    
    def _get_eyebrow_movement(self, emotion: EmotionType) -> float:
        movement_map = {
            EmotionType.SURPRISED: 5.0,
            EmotionType.ANGRY: 3.0,
            EmotionType.SAD: -2.0,
            EmotionType.HAPPY: 1.0,
            EmotionType.NEUTRAL: 0.0,
            EmotionType.CALM: 0.5,
            EmotionType.CONFIDENT: 1.5,
            EmotionType.EXCITED: 2.0
        }
        return movement_map.get(emotion, 0.0)
    
    def animate_head(self, image_array: np.ndarray, frame_num: int, 
                    emotion: EmotionType, landmarks: Dict = None) -> np.ndarray:
        if not self.animation_params.head_movement:
            return image_array
        
        head_movement_intensity = self._get_head_movement_intensity(emotion)
        
        wobble_freq_x = 0.05
        wobble_freq_y = 0.03
        rotation_freq = 0.04
        
        head_wobble_x = math.sin(frame_num * wobble_freq_x) * 3 * head_movement_intensity
        head_wobble_y = math.sin(frame_num * wobble_freq_y) * 2 * head_movement_intensity
        rotation = math.sin(frame_num * rotation_freq) * 1.5 * head_movement_intensity
        
        center_x, center_y = image_array.shape[1] // 2, image_array.shape[0] // 2
        
        M = cv2.getRotationMatrix2D((center_x, center_y), rotation, 1.0)
        rotated = cv2.warpAffine(image_array, M, (image_array.shape[1], image_array.shape[0]), 
                                flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        
        M_translate = np.float32([[1, 0, head_wobble_x], [0, 1, head_wobble_y]])
        translated = cv2.warpAffine(rotated, M_translate, (image_array.shape[1], image_array.shape[0]), 
                                  borderMode=cv2.BORDER_REFLECT)
        
        return translated
    
    def _get_head_movement_intensity(self, emotion: EmotionType) -> float:
        intensity_map = {
            EmotionType.EXCITED: 1.5,
            EmotionType.HAPPY: 1.2,
            EmotionType.ANGRY: 1.3,
            EmotionType.SURPRISED: 1.4,
            EmotionType.CALM: 0.6,
            EmotionType.SAD: 0.5,
            EmotionType.NEUTRAL: 0.8,
            EmotionType.CONFIDENT: 0.9
        }
        return intensity_map.get(emotion, 0.8)
    
    def apply_breathing(self, image_array: np.ndarray, frame_num: int, 
                       landmarks: Dict = None) -> np.ndarray:
        if not self.animation_params.breathing:
            return image_array
        
        breathing_freq = 0.12
        breathing_amp = 0.003
        
        scale = 1.0 + math.sin(frame_num * breathing_freq) * breathing_amp
        
        h, w = image_array.shape[:2]
        center = (w // 2, h // 2)
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        resized = cv2.resize(image_array, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        
        x1 = (new_w - w) // 2
        y1 = (new_h - h) // 2
        
        if x1 >= 0 and y1 >= 0:
            resized = resized[y1:y1 + h, x1:x1 + w]
        
        return resized
    
    def add_micro_expressions(self, image_array: np.ndarray, frame_num: int, 
                             emotion: EmotionType, landmarks: Dict = None) -> np.ndarray:
        if not self.animation_params.micro_expressions:
            return image_array
        
        micro_freq = 0.3
        micro_amp = 0.02
        
        micro_scale = 1.0 + math.sin(frame_num * micro_freq) * micro_amp
        
        h, w = image_array.shape[:2]
        
        if landmarks:
            face_bbox = landmarks['face_bbox']
            fx, fy, fw, fh = face_bbox
            
            face_region = image_array[fy:fy + fh, fx:fx + fw].copy()
            
            face_region = cv2.resize(face_region, None, fx=micro_scale, fy=micro_scale, 
                                    interpolation=cv2.INTER_LINEAR)
            
            if face_region.shape[0] <= fh and face_region.shape[1] <= fw:
                image_array[fy:fy + face_region.shape[0], fx:fx + face_region.shape[1]] = face_region
        
        return image_array
    
    def animate_character(self, base_image_path: str, audio_path: str, 
                         frame_num: int, total_frames: int, 
                         emotion: EmotionType = EmotionType.NEUTRAL) -> np.ndarray:
        try:
            base_img = Image.open(base_image_path)
            base_img = base_img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            
            if base_img.mode != 'RGB':
                base_img = base_img.convert('RGB')
            
            image_array = np.array(base_img)
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            
            landmarks = self.detect_detailed_landmarks(image_array)
            
            audio_intensity = 0.3
            
            image_array = self.animate_mouth_advanced(image_array, landmarks, audio_intensity, emotion)
            image_array = self.animate_eyes(image_array, landmarks, frame_num, emotion)
            image_array = self.animate_eyebrows(image_array, landmarks, frame_num, emotion)
            image_array = self.animate_head(image_array, frame_num, emotion, landmarks)
            image_array = self.apply_breathing(image_array, frame_num, landmarks)
            image_array = self.add_micro_expressions(image_array, frame_num, emotion, landmarks)
            
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            
            return image_array
            
        except Exception as e:
            print(f"Error animating character: {e}")
            return np.zeros((self.height, self.width, 3), dtype=np.uint8)
    
    def create_animated_video(self, base_image_path: str, audio_path: str, 
                             output_path: str, emotion: EmotionType = EmotionType.NEUTRAL,
                             duration: float = 5.0, fps: int = 30) -> str:
        try:
            print(f"🎬 Creating advanced character animation...")
            
            audio_features = self.analyze_audio_for_expression(audio_path)
            print(f"📊 Audio features: {audio_features}")
            
            detected_emotion = self.map_audio_to_emotion(audio_features)
            print(f"😊 Detected emotion: {detected_emotion.value}")
            
            if emotion == EmotionType.NEUTRAL:
                emotion = detected_emotion
            
            audio_intensity = self.generate_per_frame_audio_intensity(audio_path, fps)
            
            frames = []
            total_frames = int(duration * fps)
            
            print(f"🎬 Creating {total_frames} frames with {emotion.value} emotion...")
            
            for frame_num in range(total_frames):
                intensity = audio_intensity[min(frame_num, len(audio_intensity) - 1)]
                
                img = self.animate_character(
                    base_image_path, 
                    audio_path, 
                    frame_num, 
                    total_frames, 
                    emotion
                )
                
                frames.append(img)
                
                if (frame_num + 1) % 10 == 0:
                    print(f"  Progress: {frame_num + 1}/{total_frames} frames")
            
            from moviepy.editor import ImageSequenceClip
            from moviepy.audio.io.AudioFileClip import AudioFileClip
            from moviepy.audio.fx.all import audio_loop
            
            print(f"🎬 Creating video from {len(frames)} frames...")
            
            clip = ImageSequenceClip(frames, fps=fps)
            
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
                preset='ultrafast',
                threads=1,
                logger=None
            )
            
            clip.close()
            audio_clip.close()
            final_clip.close()
            
            print(f"✅ Advanced character animation created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating advanced animation: {e}")
            import traceback
            traceback.print_exc()
            raise
