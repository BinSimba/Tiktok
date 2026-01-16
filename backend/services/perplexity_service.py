import os
import httpx
from typing import Dict, List, Optional
import json

class PerplexityService:
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.base_url = "https://api.perplexity.ai"
        
    async def enhance_video_prompt(self, prompt: str, mode: str = "physics") -> str:
        """
        Enhance video generation prompt using Perplexity AI
        """
        if not self.api_key:
            print("⚠️  Perplexity API key not found, using original prompt")
            return prompt
        
        try:
            system_prompt = self._get_system_prompt(mode)
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Enhance this video generation prompt: '{prompt}'"
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
            enhanced_prompt = result["choices"][0]["message"]["content"].strip()
            print(f"🎯 Original prompt: {prompt[:100]}...")
            print(f"✨ Enhanced prompt: {enhanced_prompt[:100]}...")
            return enhanced_prompt
            
        except Exception as e:
            print(f"❌ Perplexity API error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"❌ Response: {e.response.text}")
            print("⚠️  Falling back to original prompt")
            return prompt
    
    def _get_system_prompt(self, mode: str) -> str:
        """Get system prompt based on video generation mode"""
        
        if mode == "physics":
            return """You are an expert at enhancing video generation prompts for physics-based AI video generators. Your task is to improve prompts to include:
- Detailed physics terminology (fluid dynamics, gravity, particle systems)
- Camera movement descriptions (slow motion, tracking, panning)
- Lighting and atmosphere details
- Visual style descriptors (cinematic, photorealistic, 8K)
- Temporal details (progression, timing, motion)
- Color grading and post-processing effects

Keep the enhanced prompt under 400 characters and focus on creating dynamic, realistic motion. Return ONLY the enhanced prompt, no explanations."""

        elif mode == "advanced":
            return """You are an expert at enhancing prompts for advanced AI video generators. Your task is to improve prompts to include:
- Visual style and aesthetic details
- Camera techniques and movements
- Lighting and color grading
- Composition and framing
- Emotional tone and atmosphere
- Technical quality specifications (8K, photorealistic, cinematic)

Keep the enhanced prompt under 400 characters. Return ONLY the enhanced prompt, no explanations."""

        else:
            return """You are an expert at enhancing video generation prompts. Your task is to improve prompts to include:
- More detailed visual descriptions
- Better composition and framing
- Enhanced lighting and atmosphere
- Professional terminology
- Cinematic quality indicators

Keep the enhanced prompt under 400 characters. Return ONLY the enhanced prompt, no explanations."""
    
    async def research_physics_scene(self, scene_description: str) -> Dict[str, str]:
        """
        Research physics and fluid dynamics for a scene
        """
        if not self.api_key:
            return {
                "physics_terms": "",
                "lighting": "",
                "camera": "",
                "atmosphere": ""
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a physics and cinematography expert. Research the given scene and provide:
1. Physics terminology (fluid dynamics, gravity, collisions, etc.)
2. Lighting recommendations (golden hour, studio lighting, etc.)
3. Camera movements (tracking, panning, slow motion, etc.)
4. Atmosphere and mood

Return as JSON with keys: physics_terms, lighting, camera, atmosphere. Keep each under 100 characters."""
                    },
                    {
                        "role": "user",
                        "content": f"Research this scene: '{scene_description}'"
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.5
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
            content = result["choices"][0]["message"]["content"]
            
            try:
                research_data = json.loads(content)
                return {
                    "physics_terms": research_data.get("physics_terms", ""),
                    "lighting": research_data.get("lighting", ""),
                    "camera": research_data.get("camera", ""),
                    "atmosphere": research_data.get("atmosphere", "")
                }
            except json.JSONDecodeError:
                print("⚠️  Could not parse Perplexity response as JSON")
                return {
                    "physics_terms": "",
                    "lighting": "",
                    "camera": "",
                    "atmosphere": ""
                }
            
        except Exception as e:
            print(f"❌ Perplexity research error: {e}")
            return {
                "physics_terms": "",
                "lighting": "",
                "camera": "",
                "atmosphere": ""
            }