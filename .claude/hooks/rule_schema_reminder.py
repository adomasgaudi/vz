#!/usr/bin/env python3
"""UserPromptSubmit hook: when the prompt is about adding/changing a project
rule, inject Schema.md's hook-vs-context decision framework into context so the
AI decides *how* to add the rule (build a Hook vs. write advisory Context).

Reads the hook JSON from stdin. If the user's prompt looks like a request to
add/change a rule, it reads Schema.md and prints a JSON object whose
hookSpecificOutput.additionalContext is injected into Claude's context. For any
other prompt it prints nothing and exits 0 — never fires where it doesn't apply,
never blocks (no exit 2, no decision:block).
"""
import os
import re
import sys
import json

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = (data.get("prompt") or "").lower()

# Trigger only when the prompt is about a *rule* + an add/change verb,
# or explicitly mentions a non-negotiable. Non-blocking, so a stray miss
# only costs a little context — but keep it tight to avoid noise.
has_rule = re.search(r"\brules?\b", prompt) is not None
has_verb = re.search(
    r"\b(add(ing|ed)?|new|creat\w*|make|making|introduc\w*|"
    r"enforc\w*|chang\w*|modify|modifying|updat\w*|writ\w*|"
    r"defin\w*|set up|setup)\b",
    prompt,
) is not None
mentions_nonneg = "non-negotiable" in prompt or "nonnegotiable" in prompt

if not ((has_rule and has_verb) or mentions_nonneg):
    sys.exit(0)

# Schema.md lives at the repo root; this script lives in .claude/hooks/.
schema_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "Schema.md")
)
try:
    with open(schema_path, encoding="utf-8") as fh:
        schema = fh.read()
except Exception:
    sys.exit(0)

# Inject only the decision framework — from "# hooks vs context" to EOF.
marker = "# hooks vs context"
idx = schema.find(marker)
framework = schema[idx:] if idx != -1 else schema

msg = (
    "You're about to add or change a project rule. Before writing it, apply "
    "the hook test from Schema.md (the project's rule-governance doc): can a "
    "program decide it for certain (binary, no judgment)? Yes -> build a Hook "
    "in .claude/settings.json (enforced). No -> it can only be Context "
    "(advisory text the model may forget). Decide which BEFORE you write the "
    "rule, and put it in the right place. Decision framework from Schema.md "
    "follows; full doc: Schema.md.\n\n" + framework
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": msg,
    }
}))

sys.exit(0)
