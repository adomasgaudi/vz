#!/usr/bin/env python3
"""Block direct git push/commit to main; remind Claude to use the session feature branch."""
import json, sys, re

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

# Detect: git push ... main (or origin main)
push_to_main = bool(re.search(r'\bgit\s+push\b.*\bmain\b', cmd))
# Detect: git commit while on main (catch force-adds to main too)
commit_on_main = bool(re.search(r'\bgit\s+commit\b', cmd))

if push_to_main or commit_on_main:
    import subprocess
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    ).stdout.strip()

    if branch == "main":
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "block",
                "permissionDecisionReason": (
                    "RULE REPO-02/REPO-05 VIOLATION: You are on 'main' and tried to commit or push directly. "
                    "Always work on a feature branch and merge to main immediately after. "
                    "If this is a web/remote session, check the session instructions for the designated branch name."
                )
            }
        }))
        sys.exit(0)

# Allow everything else
print(json.dumps({}))
