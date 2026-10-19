import asyncio
from pathlib import Path
import edge_tts

VOICE = "en-US-AriaNeural"


async def main():
    for chapter in sorted(Path(".").glob("Chapter_*")):
        output = chapter.with_suffix(".mp3")

        text = chapter.read_text(encoding="utf-8")

        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(str(output))

        print(f"Done: {chapter} -> {output}")


asyncio.run(main())
