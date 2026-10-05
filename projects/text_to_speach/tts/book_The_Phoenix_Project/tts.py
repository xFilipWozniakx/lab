import argparse
import asyncio
from pathlib import Path
import edge_tts

"""
python tts.py \
    cleaned/chapter01.txt \
    audio/chapter01.mp3
"""


VOICE = "en-US-GuyNeural"

# Speech rate.
# Examples:
# "-10%" = slower
# "-5%"  = slightly slower
# "+0%"  = normal
RATE = "-5%"

VOLUME = "+0%"
PITCH = "+0Hz"


async def generate_audio(
    input_file: Path,
    output_file: Path,
):
    text = input_file.read_text(
        encoding="utf-8",
    )

    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate=RATE,
        volume=VOLUME,
        pitch=PITCH,
    )

    await communicate.save(
        str(output_file),
    )


async def main():
    parser = argparse.ArgumentParser(
        description="Convert a text file to speech using Edge TTS."
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input text file",
    )

    parser.add_argument(
        "output",
        type=Path,
        help="Output MP3 file",
    )

    args = parser.parse_args()

    if not args.input.exists():
        parser.error(f"Input file does not exist: {args.input}")

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(f"Reading: {args.input}")
    print(f"Generating: {args.output}")
    print(f"Voice: {VOICE}")
    print(f"Rate: {RATE}")

    await generate_audio(
        args.input,
        args.output,
    )

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
