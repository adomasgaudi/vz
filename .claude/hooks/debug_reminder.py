#!/usr/bin/env python3
"""UserPromptSubmit hook: when the owner types a debug tag (#debug / #max-debug /
#max / #super-persistent), remind the AI that "#debug" is a MODE, not a strong
word — it changes how the AI works for this turn.

Why: the owner observed the AI treating "#debug" as mere emphasis and carrying on
with the original plan. "#debug" actually means: STOP trying to land the fix,
SIMPLIFY the task, and pour on-screen instrumentation over the failing flow until
the root is visible on the phone (the owner has no devtools — DATA-51). Made
durable as a hook per PROC-01 (a rule that keeps slipping gets a machine check,
not more prose).

Like the other hooks here it only injects context (never blocks): on any parse
error or no match, exit 0 silently.
"""
import sys
import json

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = (data.get("prompt") or "").lower()

debug_tags = ("#debug", "#max-debug", "#maxdebug", "#max", "#super-persistent")
if not any(tag in prompt for tag in debug_tags):
    sys.exit(0)

msg = (
    "DEBUG MODE (the owner typed a debug tag). '#debug' is a MODE, not emphasis — "
    "it OVERRIDES the current plan. For this turn:\n"
    "1. ABANDON / SIMPLIFY the main task — do NOT keep trying to land the fix. The "
    "goal now is to SEE what is happening, not to ship.\n"
    "2. 10x the ON-SCREEN logging (DATA-51): the owner is on a phone with no "
    "devtools, so instrument EVERY step of the failing flow into a visible "
    "on-screen panel (a fixed-position debug console), not console.log. Stamp the "
    "version in it so a stale-cache deploy is obvious.\n"
    "3. Smallest increments, ONE step at a time (DBG-01); debug by contrast vs a "
    "sibling that works (DBG-02). Leave the on-screen diagnostics in until the "
    "ROOT is confirmed, then remove them.\n"
    "4. Do not claim it's fixed — claim what the on-screen logs PROVE, and ask the "
    "owner to screenshot the panel."
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": msg,
    }
}))

sys.exit(0)
