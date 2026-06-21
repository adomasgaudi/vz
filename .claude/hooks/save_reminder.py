#!/usr/bin/env python3
# Stop hook: at end of turn, remind to Save (REPO-01) if the git working tree
# is dirty or main isn't pushed to origin. Non-blocking reminder; silent when
# the tree is clean and pushed.
#
# Mechanistically, step by step:
#
# 1. Claude Code runs this script when the main agent finishes responding (the
#    Stop event) and pipes the hook JSON to stdin. We don't need the payload —
#    we ask git directly about the repo state.
# 2. `git status --porcelain` lists uncommitted/untracked changes; non-empty
#    output means the tree is DIRTY.
# 3. `git rev-list --count origin/main..HEAD` counts local commits not on
#    origin/main; > 0 means there are UNPUSHED commits. (No network fetch — it
#    compares against the last-known origin/main ref, which is enough to catch
#    "you committed but didn't push".)
# 4. If either is true, print a JSON object whose
#    hookSpecificOutput.additionalContext nudges to commit + push. Claude Code
#    injects that string into context. Clean + pushed -> print nothing.
#
# It cannot block: no exit 2, no decision:block. It only informs (Schema.md:
# hooks here are aggressive context, not gates). Any git/parse error -> exit 0
# silently so a non-repo or odd state never disrupts the turn.
import json, sys, subprocess

def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          timeout=8).stdout.strip()

try:
    json.load(sys.stdin)  # drain stdin; payload unused
except Exception:
    pass

try:
    dirty = bool(git("status", "--porcelain"))
    try:
        unpushed = int(git("rev-list", "--count", "origin/main..HEAD") or "0")
    except ValueError:
        unpushed = 0
except Exception:
    sys.exit(0)

if not dirty and unpushed == 0:
    sys.exit(0)

bits = []
if dirty:
    bits.append("uncommitted changes in the working tree")
if unpushed:
    bits.append(f"{unpushed} commit(s) not pushed to origin/main")

msg = ("REPO-01 (Save) reminder: " + " and ".join(bits) +
       ". The owner only sees the live site — commit + push to main before "
       "ending, then send the rebuilt index.html if it changed.")

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": msg,
}}))
sys.exit(0)
