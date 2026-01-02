from zhipuai import ZhipuAI
import os
from typing import Optional

client = ZhipuAI(api_key=os.getenv("ZHIPU_API_KEY", "your-zhipu-api-key-here"))

def generate_tiktok_script(topic: str, duration: int = 15) -> str:
    prompt = f"""Generate a viral TikTok script about "{topic}" that is exactly {duration} seconds long when spoken at a normal pace.

Requirements:
- MUST be {duration} seconds total (approximately {duration * 2.5} words)
- Start with a strong hook in the first 2 seconds
- Have 3-4 key points in the body
- End with a clear call-to-action
- Use energetic, engaging language
- Make it sound natural when spoken aloud
- Avoid complex vocabulary
- Use short, punchy sentences

Format the script as spoken text only, no labels or stage directions.

Script:"""

    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a viral TikTok content creator. You write engaging, short scripts optimized for 15-second videos."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.9,
            max_tokens=200
        )
        
        script = response.choices[0].message.content.strip()
        
        word_count = len(script.split())
        estimated_seconds = word_count / 2.5
        
        if estimated_seconds > duration * 1.2:
            sentences = script.split('. ')
            trimmed_script = '. '.join(sentences[:len(sentences) - 1])
            script = trimmed_script + '.'
        
        return script
        
    except Exception as e:
        print(f"Error generating script: {e}")
        print("Using fallback script template...")
        fallback_scripts = {
            "default": f"Want to learn about {topic}? Here's a quick guide. First, start with the basics. Second, practice every single day. Third, share your progress with others. Follow for more tips!",
            "tech": f"Tech tip about {topic} coming right up. First, understand the core concept. Second, apply it to your daily workflow. Third, measure your results. Like and follow for more!",
            "life": f"Here's how {topic} can change your life. Start small and stay consistent. Build habits that stick. Celebrate your wins. Save this and follow for more content!",
            "business": f"Want to master {topic} for your business? First, research your market. Second, create a simple plan. Third, execute and iterate. Subscribe for more business tips!"
        }
        
        for category, script in fallback_scripts.items():
            if category != "default":
                words = len(script.split())
                if words <= duration * 2.5:
                    return script
        
        return fallback_scripts["default"]
