#!/usr/bin/env python3
"""UserPromptSubmit hook: when the prompt is about adding/changing a project
rule, inject Schema.md's hook-vs-context decision framework into context so the
AI decides *how* to add the rule (build a Hook vs. write advisory Context).

Mechanistically, step by step:

1. Claude Code runs this script *before the AI reads your prompt* and pipes the
   hook JSON to stdin. `json.load(sys.stdin)` parses it; on any parse error,
   `sys.exit(0)` (exit 0, no output -> hook does nothing, prompt passes through).
2. `data.get("prompt")` is your raw message; `.lower()` makes the matching
   case-insensitive.
3. The trigger is two regexes ANDed, plus an OR escape hatch:
   - `has_rule`  -> `\brules?\b` matches the word "rule"/"rules" (word
     boundaries so "ruler" doesn't count).
   - `has_verb`  -> matches an add/change verb (add, new, create, make,
     introduce, enforce, change, modify, update, write, define, set up).
   - `mentions_nonneg` -> the literal "non-negotiable"/"nonnegotiable".
   Fires only if `(has_rule AND has_verb) OR mentions_nonneg`. Anything else ->
   `sys.exit(0)`, silent. Kept tight on purpose: a false *miss* costs only a bit
   of context, but a false *fire* injects a wall of text on unrelated prompts.
4. Locates Schema.md relative to THIS file (`__file__` -> `.claude/hooks/`, so
   `../../Schema.md` is the repo root). Read failure -> `sys.exit(0)`.
5. Slices Schema.md from the `# hooks vs context` marker to EOF, so only the
   decision framework is injected, not the whole event/permission map. If the
   marker is absent it falls back to the entire file.
6. Prepends a short "apply the hook test" instruction, then `print`s a JSON
   object. Claude Code injects `hookSpecificOutput.additionalContext` into the
   model's context for this turn — that string is the entire effect.

It cannot block or force anything: no `exit 2`, no `decision: block`. It only
injects context — the AI may still ignore it.
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
