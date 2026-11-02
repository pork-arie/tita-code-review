# Tita Code Review

An AI agent skill that reviews your code like a dramatic, loving Filipino tita at a family reunion: Taglish, "hijo/hija", and comparisons to your overachieving pinsan. The feedback is still real. Every joke points at an actual problem and how to fix it.

It can also read the review aloud in a Filipino voice as an MP3.

> "Hay nako, hijo, si pinsan mo may CI/CD na. Ikaw, may console.log pa rin."

## What's inside

```
SKILL.md                    # the skill: persona, rules, review structure
references/tita-phrases.md  # phrase bank the agent draws from
scripts/speak.py            # text-to-speech with edge-tts (free, no API key)
```

## How it works

1. **Triggering.** Your agent only sees the `name` and `description` in `SKILL.md` until a request matches, such as "tita review this file". Then it loads the full skill.
2. **Reviewing.** `SKILL.md` tells the agent to find real problems first (bugs, missing error handling, no tests), then rewrite each one in Tita's voice. Every review follows the same structure: an opener, up to 5 issues (each with the joke, a plain explanation and the fix), a compliment, and the one thing to fix first.
3. **Phrases.** The agent reads `references/tita-phrases.md` only while writing, and varies the lines so reviews don't repeat.
4. **Voice.** If you ask for audio, the agent writes a short spoken script with no code or symbols and passes it to `speak.py`. The script cleans out leftover markdown, respells tech words the way they should sound (`API` → "ey pee ay"), and generates an MP3 with Microsoft's Filipino voice `fil-PH-BlessicaNeural`.

## Install

### Claude Code

Clone into your personal skills folder:

```bash
git clone https://github.com/pork-arie/tita-code-review ~/.claude/skills/tita-code-review
```

Or, for a single project, clone into `<project>/.claude/skills/tita-code-review`.

### Claude.ai / Claude desktop

Download this repo as a ZIP and upload it under **Settings → Capabilities → Skills**.

### Voice (optional)

```bash
pip install -r requirements.txt
```

This needs internet access, because edge-tts uses Microsoft's online voices.

## Usage

Ask your agent:

- "tita review this file"
- "roast my code tita-style, with voice"

Or run the voice script yourself:

```bash
python scripts/speak.py "Hay nako, hijo, bakit walang README ang GitHub mo?" --out tita.mp3
python scripts/speak.py --file script.txt
python scripts/speak.py --list-voices
```

Options: `--out` (default `tita_review.mp3`), `--voice` (default `fil-PH-BlessicaNeural`), `--rate` (default `+8%`), `--pitch` (default `+5Hz`).

To teach it how to say more tech words, add them to the `PRONUNCIATION` dict in `speak.py`.

## License

MIT
