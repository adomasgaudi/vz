#!/usr/bin/env python3
# PostToolUse hook: after any Edit/Write, remind the AI to bump the version
# badge + log SP + rebuild — but only when the edited file was template.html.
# Non-blocking reminder; silent for every other file.

# Mechanistically, step by step:

# 1. Claude Code runs this script after an Edit/Write tool call (matcher
#    `Edit|Write` in settings.local.json) and pipes the tool's JSON to stdin.
# 2. `json.load(sys.stdin)` parses that payload. The edited file's path is at
#    `tool_input.file_path`. The `(... or {})` guards the case where `tool_input`
#    is missing/null so `.get` never crashes. Any parse error -> `sys.exit(0)`
#    (exit 0 = success, no output = no context injected = hook does nothing).
# 3. `fp.replace("\\", "/")` normalises Windows backslashes to forward slashes so
#    `os.path.basename` reliably extracts the filename; `.lower()` makes the
#    compare case-insensitive. We compare basename only, so the hook fires
#    regardless of which directory template.html sits in.
# 4. Only if that filename == "template.html" do we `print(...)` a JSON object.
#    Claude Code reads `hookSpecificOutput.additionalContext` from stdout and
#    injects that string into the model's context — that's the whole effect.
#    Printing nothing (any other file) means nothing is injected.

# It cannot block or force anything: no `exit 2`, no `decision: block`. It only
# injects context — the AI may still ignore it. (See Schema.md: hooks here are
# aggressive *context*, not gates.)
import sys, json, os
try:
    fp = (json.load(sys.stdin).get("tool_input") or {}).get("file_path", "")
except Exception:
    sys.exit(0)
if os.path.basename(fp.replace("\\", "/")).lower() == "template.html":
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
        "additionalContext": "template.html changed — bump the version badge in the <h1>, add a VERSIONS entry with SP, rebuild (python3 build_site.py), then send index.html."}}))
