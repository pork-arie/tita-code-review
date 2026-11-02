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

Options: `--voice`, `--rate` (default `+8%`), `--pitch` (default `+5Hz`).

To teach it how to say more tech words, add them to the `PRONUNCIATION` dict in `speak.py`.

## License

MIT
