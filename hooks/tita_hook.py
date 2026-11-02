"""
tita_hook.py - Tita Baby checks your commit messages.

Git calls this through hooks/commit-msg with the path to the message file.
  exit 0 -> commit goes through
  exit 1 -> commit is blocked

Other commands:
  python hooks/tita_hook.py --build-voices   # pre-make all voice lines (needs internet, once)
  python hooks/tita_hook.py --test "fix"     # try a message without committing

Settings (environment variables):
  TITA_MUTE=1       no voice, text only
  TITA_WARN_ONLY=1  never block, just scold
Skip Tita for one commit:  git commit --no-verify
"""

import asyncio
import datetime
import os
import random
import re
import subprocess
import sys

HOOK_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HOOK_DIR)
VOICE_DIR = os.path.join(ROOT, "assets", "voice")

# Windows terminals sometimes choke on non-ASCII; never crash a commit over it.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- the lines
# Each line has an id so its MP3 can be cached in assets/voice/<id>.mp3
LINES = {
    "bad": [
        ("bad1", "Hay nako hijo! Ano 'yang commit message mo? Paano malalaman ng kasama mo kung ano ginawa mo?"),
        ("bad2", "Fix? Anong fix? Ano'ng inayos mo, ang buhay mo? Sabihin mo nang maayos!"),
        ("bad3", "Si pinsan mo, malinaw ang commit messages. Ikaw, parang text ng ex mo. Ayusin mo 'yan."),
        ("bad4", "Hijo, hindi 'yan tatanggapin ni Tita. Isulat mo kung ano talaga ang binago mo."),
    ],
    "meh": [
        ("meh1", "Pwede na, hijo. Pero mas maganda kung may feat o fix sa unahan, para propesyonal."),
        ("meh2", "Okay na 'yan, pero subukan mo ang format na feat, colon, tapos ang ginawa mo. Para pang-Japan."),
    ],
    "good": [
        ("good1", "Ay, ang ganda ng commit mo! Ipagmamalaki kita sa reunion."),
        ("good2", "Very good, hijo! Ganyan dapat. Kumain ka na ba?"),
        ("good3", "Wow, malinaw! Ikaw ba talaga gumawa nito?"),
    ],
    "late": [
        ("late1", "Hijo! Alas dos na ng madaling araw! Matulog ka na, bukas mo na ituloy 'yan!"),
        ("late2", "Ang puyat mo, anak. Ang code, maghihintay. Ang kalusugan mo, hindi."),
    ],
}

VAGUE = {
    "fix", "fixed", "fixes", "update", "updated", "updates", "changes", "change",
    "stuff", "wip", "test", "asdf", "commit", "edit", "edits", "done", "final",
    "minor", "misc", "temp", "save", "ok", "okay", "new", "work", "bug", "bugs",
}

CONVENTIONAL = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([\w\-./ ]+\))?!?: .+"
)

GOOD_EXAMPLES = [
    "feat: add login screen with Supabase auth",
    "fix: crash when cart is empty",
    "docs: add install steps to README",
    "refactor: split checkout into smaller functions",
]

# ---------------------------------------------------------------- checking
def read_message(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = [l for l in f.read().splitlines() if not l.startswith("#")]
    return "\n".join(lines).strip()


def judge(message):
    """Return 'skip', 'bad', 'meh' or 'good' for a commit message."""
    subject = message.splitlines()[0].strip() if message else ""

    # Leave git's own automatic messages alone.
    if subject.startswith(("Merge ", "Revert ", "fixup!", "squash!", "amend!")):
        return "skip"
    if not subject:
        return "skip"  # git aborts empty messages by itself

    words = re.findall(r"[a-zA-Z]+", subject.lower())
    meaningful = [w for w in words if w not in VAGUE]

    if len(subject) < 10 or not meaningful:
        return "bad"
    if re.fullmatch(r"(.)\1+", subject.replace(" ", "")):  # "aaaaaaaaaa"
        return "bad"
    if not CONVENTIONAL.match(subject):
        return "meh"
    return "good"


def is_late_night():
    return 0 <= datetime.datetime.now().hour < 5


# ---------------------------------------------------------------- voice
def voice_path(line_id):
    return os.path.join(VOICE_DIR, f"{line_id}.mp3")


def play(path):
    """Play an MP3 in the background so the commit doesn't wait for Tita."""
    if os.environ.get("TITA_MUTE") == "1" or not os.path.exists(path):
        return
    try:
        if sys.platform == "win32":
            ps = (
                "Add-Type -AssemblyName presentationCore;"
                "$p = New-Object System.Windows.Media.MediaPlayer;"
                f"$p.Open([uri]'{path}');"
                "$p.Play(); $t = 0;"
                "while (-not $p.NaturalDuration.HasTimeSpan -and $t -lt 50) { Start-Sleep -Milliseconds 100; $t++ };"
                "if ($p.NaturalDuration.HasTimeSpan) { Start-Sleep -Seconds ([math]::Ceiling($p.NaturalDuration.TimeSpan.TotalSeconds)) }"
            )
            subprocess.Popen(
                ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
                creationflags=0x00000008,  # DETACHED_PROCESS
            )
        elif sys.platform == "darwin":
            subprocess.Popen(["afplay", path])
        else:
            for player in (["mpg123", "-q"], ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]):
                try:
                    subprocess.Popen(player + [path])
                    break
                except FileNotFoundError:
                    continue
    except Exception:
        pass  # a missing speaker should never block a commit


def build_voices():
    """Generate every line once with speak.py so hooks play instantly and offline."""
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    from speak import DEFAULT_VOICE, clean_for_speech, speak

    os.makedirs(VOICE_DIR, exist_ok=True)
    for group in LINES.values():
        for line_id, text in group:
            out = voice_path(line_id)
            if os.path.exists(out):
                print(f"exists: {line_id}")
                continue
            asyncio.run(speak(clean_for_speech(text), DEFAULT_VOICE, out, "+8%", "+5Hz"))


# ---------------------------------------------------------------- main
def react(message):
    """Print and speak Tita's reaction. Returns the exit code."""
    verdict = judge(message)
    if verdict == "skip":
        return 0

    line_id, text = random.choice(LINES[verdict])
    print(f"\n  Tita Baby: {text}")

    if verdict == "bad":
        print("\n  Try something like:")
        for ex in random.sample(GOOD_EXAMPLES, 2):
            print(f"    {ex}")
        print("\n  (Skip Tita once: git commit --no-verify)\n")
    elif verdict == "meh":
        print(f"  Example: {random.choice(GOOD_EXAMPLES)}\n")

    if is_late_night():
        late_id, late_text = random.choice(LINES["late"])
        print(f"  Tita Baby: {late_text}\n")
        line_id = late_id  # the sleep scolding wins

    play(voice_path(line_id))

    if verdict == "bad" and os.environ.get("TITA_WARN_ONLY") != "1":
        return 1
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("Usage: tita_hook.py <commit-msg-file> | --test \"message\" | --build-voices")
    if args[0] == "--build-voices":
        build_voices()
        return
    if args[0] == "--test":
        sys.exit(react(" ".join(args[1:])))
    sys.exit(react(read_message(args[0])))


if __name__ == "__main__":
    main()