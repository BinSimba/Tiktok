import edge_tts
import asyncio
from pathlib import Path
import gtts

async def generate_audio_async(text: str, output_path: str, voice: str = "en-US-AriaNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def generate_audio(text: str, output_path: str, method: str = "gtts") -> str:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if method == "edge":
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(generate_audio_async(text, str(output_path)))
                loop.close()
            else:
                import nest_asyncio
                nest_asyncio.apply()
                loop.run_until_complete(generate_audio_async(text, str(output_path)))
        else:
            tts = gtts.gTTS(text=text, lang='en', slow=False)
            tts.save(str(output_path))
        
        if output_path.exists() and output_path.stat().st_size > 0:
            return str(output_path)
        else:
            raise Exception("Audio file was not created or is empty")
            
    except Exception as e:
        print(f"Error generating audio with {method}: {e}")
        raise
