# Text-to-TikTok Video Generator

Generate AI-powered TikTok videos from text descriptions!

## Quick Start on Mac

Double-click the `start-app.command` file to launch both servers.

Or open Terminal and run:
```bash
cd "/Volumes/DOCK/IA/Glm Vibe coding /backend"
source venv/bin/activate
python main.py
```

In a new terminal:
```bash
cd "/Volumes/DOCK/IA/Glm Vibe coding /frontend"
npm run dev
```

Then open http://localhost:3000 in your browser.

## Use on iPhone

Make sure your iPhone and Mac are on the same Wi-Fi network, then open Safari and go to:
```
http://192.168.1.169:3000
```

## Features

- Generate AI videos from text (uses Replicate Stable Video Diffusion)
- Custom text input support
- AI-generated images matching your text
- Dynamic Ken Burns animation
- Voiceover with text-to-speech
- Beautiful glassmorphism UI

## Setup

The app is already configured with:
- Backend: FastAPI
- Frontend: Next.js + Tailwind CSS
- AI Script Generation: GLM-4.7 (ZhipuAI)
- AI Video Generation: Replicate API
- AI Image Generation: Pollinations AI
- TTS: Edge-TTS

## API Keys Needed

The ZhipuAI key is already configured in `.env`.

To use AI video generation, add your Replicate API token:
```
REPLICATE_API_TOKEN=your_token_here
```

Get a free token at: https://replicate.com/account/api-tokens

## Project Structure

```
/backend
  /models - Script generation logic
  /services - TTS, video assembly, AI image/video generation
  main.py - FastAPI backend server

/frontend
  /app - Next.js pages
  /components - React components
```

## Tips

- Video generation takes 1-3 minutes
- Works best with descriptive prompts like "monkey on bike pedaling away from police"
- Falls back to AI images if video generation fails
- Both Mac and iPhone use the same codebase!
