# Tita Code Review

An AI agent skill that reviews your code like a dramatic, loving Filipino tita at a family reunion: Taglish, "hijo/hija", and comparisons to your overachieving pinsan. The feedback is still real. Every joke points at an actual problem and how to fix it.

It can also read the review aloud in a Filipino voice as an MP3.

> "Hay nako, hijo, si pinsan mo may CI/CD na. Ikaw, may console.log pa rin."

## What's inside

```
SKILL.md                    # the skill: persona, rules, review structure
references/tita-phrases.md  # phrase bank the agent draws from
scripts/speak.py            # text-to-speech with edge-tts (free, no API key)
hooks/commit-msg            # git hook entry point, calls tita_hook.py
hooks/tita_hook.py          # Tita checks your commit messages
assets/voice/               # pre-made voice lines for the hook
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

## Commit hook

Tita can also check your commit messages, out loud.

```
$ git commit -m "fix"

  Tita Baby: Fix? Anong fix? Ano'ng inayos mo, ang buhay mo? Sabihin mo nang maayos!

  Try something like:
    fix: crash when cart is empty
    docs: add install steps to README
```

| Message | Tita's verdict |
|---|---|
| Vague or too short (`fix`, `update`, `wip`, `asdf`) | Scolds you and **blocks the commit** |
| Clear but not [Conventional Commits](https://www.conventionalcommits.org/) | Lets it through, suggests `feat:` / `fix:` |
| `feat: add login screen` | Proud of you |
| Any commit between midnight and 5 AM | Tells you to go to sleep |

Merge, revert, `fixup!` and `squash!` messages are skipped.

The voice lines are already in `assets/voice/`, so the hook plays instantly and works offline. Playback runs in the background and never slows down the commit.

### Turn it on

In any repo where you want Tita watching:

```bash
git config core.hooksPath ~/.claude/skills/tita-code-review/hooks
```

Use the path where you cloned this repo. Note that `core.hooksPath` replaces that repo's `.git/hooks` folder, so if the repo already uses other hooks (husky, pre-commit), wire `hooks/commit-msg` into those instead.

To turn it off: `git config --unset core.hooksPath`

### Options

```bash
git commit --no-verify -m "..."             # skip Tita for one commit
TITA_MUTE=1 git commit -m "..."             # text only, no voice
TITA_WARN_ONLY=1 git commit -m "..."        # scold, but never block
python hooks/tita_hook.py --test "fix"      # try a message without committing
python hooks/tita_hook.py --build-voices    # regenerate missing voice lines (needs internet)
```

If you edit or add lines in `LINES` in `tita_hook.py`, delete the matching MP3s in `assets/voice/` and run `--build-voices`.

## License

MIT
