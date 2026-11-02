"""
speak.py - turns Tita's review into an MP3 using edge-tts (free, no API key).

Usage:
    python speak.py "Hay nako, hijo..." --out tita_review.mp3
    python speak.py --file script.txt
    python speak.py --list-voices        # see available Filipino voices

Needs internet (edge-tts uses Microsoft's online voices).
"""

import argparse
import asyncio
import re
import sys

import edge_tts

# Filipino female voice. Run --list-voices to see other options.
DEFAULT_VOICE = "fil-PH-BlessicaNeural"

# Tech words a Filipino voice tends to mispronounce.
# Key = how it's written, value = how it should sound. Add your own!
PRONUNCIATION = {
    "useEffect": "yus ee-fekt",
    "useState": "yus steyt",
    "console.log": "konsol log",
    "npm": "en pee em",
    "API": "ey pee ay",
    "CI/CD": "see ay, see dee",
    "TypeScript": "tayp skript",
    "JavaScript": "jaba skript",
    "GitHub": "git hab",
    "README": "rid mi",
}


def clean_for_speech(text: str) -> str:
    """Remove markdown/code bits and swap in phonetic spellings."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # code blocks
    text = re.sub(r"`([^`]*)`", r"\1", text)                # inline code
    text = re.sub(r"[*_#>]", "", text)                      # markdown symbols
    for word, sound in PRONUNCIATION.items():
        text = text.replace(word, sound)
    return " ".join(text.split())


async def list_filipino_voices():
    voices = await edge_tts.list_voices()
    for v in voices:
        if v["Locale"].startswith("fil"):
            print(v["ShortName"], "-", v["Gender"])


async def speak(text: str, voice: str, out: str, rate: str, pitch: str):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out)
    print(f"Saved: {out}")


def main():
    p = argparse.ArgumentParser(description="Speak a tita review aloud.")
    p.add_argument("text", nargs="?", help="Text to speak")
    p.add_argument("--file", help="Read text from a file instead")
    p.add_argument("--out", default="tita_review.mp3")
    p.add_argument("--voice", default=DEFAULT_VOICE)
    # A bit faster and slightly higher = more dramatic tita energy.
    p.add_argument("--rate", default="+8%")
    p.add_argument("--pitch", default="+5Hz")
    p.add_argument("--list-voices", action="store_true")
    args = p.parse_args()

    if args.list_voices:
        asyncio.run(list_filipino_voices())
        return

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            raw = f.read()
    elif args.text:
        raw = args.text
    else:
        sys.exit("Give me text or --file, hijo.")

    text = clean_for_speech(raw)
    try:
        asyncio.run(speak(text, args.voice, args.out, args.rate, args.pitch))
    except Exception as e:
        sys.exit(f"Voice failed (no internet?): {e}")


if __name__ == "__main__":
    main()