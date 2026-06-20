#!/usr/bin/env python3
# PostToolUse hook: non-blocking reminder when template.html is edited. Silent for any other file.
import sys, json, os
try:
    fp = (json.load(sys.stdin).get("tool_input") or {}).get("file_path", "")
except Exception:
    sys.exit(0)
if os.path.basename(fp.replace("\\", "/")).lower() == "template.html":
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
        "additionalContext": "template.html changed — bump the version badge in the <h1>, add a VERSIONS entry with SP, rebuild (python3 build_site.py), then send index.html."}}))
