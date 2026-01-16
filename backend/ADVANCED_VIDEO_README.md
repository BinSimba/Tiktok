# Advanced AI Video Generation System

## Overview

This advanced AI video generation system is designed to compete with top-tier video generation platforms like Luma AI, Pika, and Gemini Pro 3. It provides professional-grade video creation capabilities with advanced features including:

- **8+ Video Styles**: Cinematic, Anime, Realistic, Abstract, Vintage, Neon, Noir, Watercolor
- **3 Video Generation Modes**: Cinematic, Character, Hybrid
- **Advanced Camera Movements**: Static, Slow Zoom In/Out, Pan Left/Right, Tilt Up/Down, Orbit, Dolly, Crane
- **4 Quality Presets**: Speed (720p), Balanced (1080p), Quality (1080p), Ultra (4K)
- **Emotion-Based Animation**: 10 emotion types (Neutral, Happy, Sad, Angry, Surprised, Fearful, Disgusted, Excited, Calm, Confident)
- **Temporal Consistency**: Optical flow-based frame interpolation for smooth motion
- **Dynamic Lighting & Atmospheric Effects**: Real-time lighting adjustments and fog/atmosphere effects
- **Advanced Character Animation**: MediaPipe-based facial landmark detection with realistic lip-sync, eye movement, eyebrow animation, head movement, and breathing effects

## Architecture

### Core Components

1. **advanced_video_engine.py** - Main video generation engine
   - Style transfer algorithms (vintage, noir, neon, watercolor, anime filters)
   - Optical flow calculation and temporal smoothing
   - Camera movement simulation (zoom, pan, tilt, rotation)
   - Dynamic lighting and atmospheric effects
   - Scene interpolation and transitions

2. **advanced_character_animator.py** - Character animation system
   - MediaPipe Face Mesh integration (478 facial landmarks)
   - Audio-driven emotion detection
   - Advanced mouth animation with realistic deformation
   - Eye movement, eyebrow animation, head wobble
   - Breathing and micro-expression effects
   - Emotion-intensity mapping

3. **unified_video_generator.py** - Unified API wrapper
   - Cinematic video generation
   - Character-based video generation
   - Hybrid (character + background) video generation

4. **main.py** - API endpoints
   - `/generate-advanced-video` - Advanced video generation endpoint

## Video Generation Modes

### 1. Cinematic Mode
Generates cinematic-style videos with professional visual effects:
- Style transfer application
- Camera movements
- Dynamic lighting
- Atmospheric effects
- Optical flow smoothing

### 2. Character Mode
Generates character-focused videos with advanced animation:
- Audio-driven emotion detection
- Realistic facial animation (mouth, eyes, eyebrows)
- Head movement and breathing
- Multiple character types (person, monkey, anime, cartoon, robot, animal, fantasy, cyborg)

### 3. Hybrid Mode
Combines character and background elements:
- Character overlay on dynamic background
- Blended composition with masks
- Synchronized animations

## Video Styles

| Style | Description |
|-------|-------------|
| Cinematic | Film grain, professional lighting, depth of field, HDR |
| Anime | Vibrant colors, clean lines, Studio Ghibli inspired |
| Realistic | Photorealistic, ultra detailed, 8K, sharp focus |
| Abstract | Abstract art, surreal, geometric shapes, artistic |
| Vintage | Vintage film, sepia tones, film grain, retro |
| Neon | Cyberpunk, neon lights, glowing, futuristic |
| Noir | Film noir, black and white, high contrast |
| Watercolor | Watercolor painting, soft edges, hand-painted |

## Camera Movements

- **Static** - No camera movement
- **Slow Zoom In** - Gradual zoom towards subject
- **Slow Zoom Out** - Gradual zoom away from subject
- **Pan Left** - Camera moves left
- **Pan Right** - Camera moves right
- **Tilt Up** - Camera tilts upward
- **Tilt Down** - Camera tilts downward
- **Orbit** - Camera rotates around subject
- **Dolly** - Dolly movement (zoom in then out)
- **Crane** - Crane movement (up then down)

## Quality Presets

| Preset | FPS | Resolution | Bitrate |
|--------|-----|------------|---------|
| Speed | 15 | 720x1280 | 2000k |
| Balanced | 24 | 1080x1920 | 4000k |
| Quality | 30 | 1080x1920 | 8000k |
| Ultra | 30 | 2160x3840 | 16000k |

## Emotion Types

The system automatically detects emotion from audio and applies appropriate animations:
- **Neutral** - Default calm state
- **Happy** - Elevated energy, upward eyebrows, smiling
- **Sad** - Lowered energy, downward eyebrows
- **Angry** - High intensity, furrowed brows
- **Surprised** - Wide eyes, raised eyebrows
- **Excited** - High energy, dynamic movements
- **Calm** - Relaxed, subtle movements
- **Confident** - Upright posture, steady gaze

## API Usage

### Generate Advanced Video

```bash
POST /generate-advanced-video

{
  "text": "Your script here",
  "is_custom": false,
  "video_type": "cinematic",
  "style": "cinematic",
  "character_type": "person",
  "emotion": "neutral",
  "quality": "balanced",
  "camera_movement": "slow_zoom_in",
  "duration": 5.0
}
```

### Parameters

- **text** (string, required): Script or prompt for video generation
- **is_custom** (boolean, optional): Use text as-is (true) or generate AI script (false, default)
- **video_type** (string, optional): "cinematic", "character", or "hybrid" (default: "cinematic")
- **style** (string, optional): Video style (default: "cinematic")
- **character_type** (string, optional): "person", "monkey", "anime", "cartoon", "robot", "animal", "fantasy", "cyborg" (default: "person")
- **emotion** (string, optional): Target emotion (default: "neutral", auto-detected from audio if character mode)
- **quality** (string, optional): "speed", "balanced", "quality", or "ultra" (default: "balanced")
- **camera_movement** (string, optional): Camera movement type (default: "static")
- **duration** (float, optional): Video duration in seconds (default: 5.0)

### Response

```json
{
  "script": "The generated or custom script",
  "video_url": "http://localhost:8000/videos/session_id_video.mp4"
}
```

## Technical Details

### Optical Flow
Uses Farneback algorithm for dense optical flow calculation:
- Pyramid scale: 0.5
- Levels: 3
- Window size: 15
- Iterations: 3
- Poly expansion: 5
- Poly sigma: 1.2

### MediaPipe Face Mesh
- 478 facial landmarks
- Static image mode: false (for tracking)
- Max faces: 1
- Refine landmarks: true
- Detection confidence: 0.5
- Tracking confidence: 0.5

### Animation Smoothing
- Mouth movement smoothing factor: 0.7
- Exponential moving average for smooth transitions
- Micro-expression frequency: 0.3 Hz
- Breathing frequency: 0.12 Hz
- Head wobble frequency: 0.05 Hz (X), 0.03 Hz (Y)

### Style Transfer Algorithms

**Vintage Filter**
- Sepia color transformation
- Contrast enhancement (1.2x)
- Brightness reduction (0.9x)
- Film grain noise addition

**Noir Filter**
- Grayscale conversion
- Contrast enhancement (1.5x)
- Brightness reduction (0.8x)
- Histogram equalization

**Neon Filter**
- HSV saturation boost (1.5x)
- Value boost (1.2x)
- Gaussian blur glow effect
- 70% original, 30% glow blend

**Watercolor Filter**
- Bilateral smoothing
- Edge-preserving filter
- Non-local means denoising
- Stylization filter

**Anime Filter**
- Canny edge detection
- Bilateral filter smoothing
- 90% smoothed, 10% edges blend

## Performance Considerations

### Rendering Time
- Speed preset: ~30-60 seconds for 5-second video
- Balanced preset: ~60-120 seconds for 5-second video
- Quality preset: ~120-240 seconds for 5-second video
- Ultra preset: ~240-480 seconds for 5-second video

### Hardware Requirements
- CPU: Multi-core processor recommended
- RAM: 8GB minimum, 16GB recommended
- GPU: CUDA-capable GPU (optional, for PyTorch acceleration)
- Storage: 1GB free space for temporary files

### Memory Usage
- Per frame: ~10-30MB depending on resolution
- Optical flow cache: ~50-200MB
- Style transfer model: ~100MB (if loaded)

## Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic>=2.6.0
zhipuai==2.1.5.20250825
moviepy==1.0.3
Pillow>=10.4.0
gTTS==2.4.0
edge-tts==6.1.9
nest-asyncio==1.5.8
pydub==0.25.1
aiofiles==23.2.1
python-dotenv==1.0.0
imageio-ffmpeg>=0.5.1
requests>=2.31.0
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.8.0
mediapipe>=0.10.0
librosa>=0.10.0
soundfile>=0.12.0
numpy>=1.24.0
```

## Example Use Cases

### 1. Cinematic Product Video
```json
{
  "text": "Discover the future of technology with our revolutionary AI-powered devices",
  "video_type": "cinematic",
  "style": "cinematic",
  "camera_movement": "slow_zoom_in",
  "quality": "quality",
  "duration": 8.0
}
```

### 2. Character Storytelling
```json
{
  "text": "Once upon a time, in a magical forest far away...",
  "video_type": "character",
  "character_type": "anime",
  "style": "anime",
  "emotion": "excited",
  "quality": "balanced",
  "duration": 10.0
}
```

### 3. Hybrid Tutorial Video
```json
{
  "text": "Learn how to master the art of video editing",
  "video_type": "hybrid",
  "character_type": "person",
  "style": "realistic",
  "camera_movement": "pan_left",
  "quality": "quality",
  "duration": 15.0
}
```

## Future Enhancements

- [ ] Deep learning-based style transfer (neural style transfer)
- [ ] 3D character models with rigging
- [ ] Text-to-speech with emotion modulation
- [ ] Multi-character scenes with interaction
- [ ] Background music generation
- [ ] Sound effects synchronization
- [ ] Real-time preview rendering
- [ ] Batch video generation
- [ ] Video editing capabilities (trim, splice, merge)
- [ ] Export to multiple formats and platforms

## Troubleshooting

### Common Issues

**Out of Memory Error**
- Reduce quality preset to "speed" or "balanced"
- Reduce duration
- Close other applications

**Slow Rendering**
- Reduce quality preset
- Reduce camera movement complexity
- Disable atmospheric effects

**Face Detection Failure**
- Ensure character image has clear, visible face
- Try different character type or prompt
- Check MediaPipe installation

**Audio Sync Issues**
- Verify audio file format (MP3 recommended)
- Check audio duration matches video duration
- Regenerate audio with different TTS settings

## License

This advanced video generation system is provided as-is for educational and commercial use.
