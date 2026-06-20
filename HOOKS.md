# HOOKS.md — what runs automatically in vz (plain English, for humans)

Hooks = small scripts the AI's tool (Claude Code) runs **automatically** at fixed
moments (chat start · your message · AI reply-end). Nobody types them; they fire on
their own. They live in `.claude/settings.json`.

## vz hooks right now: NONE
- ❌ no `.claude/` folder · ❌ no `settings.json` · ❌ no hook scripts.
- **Nothing runs automatically here.** Every vz change happens only because the AI was asked.

## "But I see pop-ups / reminders in chats…"
- Those come from the **Data repo** (`adomasgaudi/data`, a separate project) — its hooks fire when both repos share a chat.
- They influence the AI's behaviour (e.g. the multiple-choice pop-ups) but **never edit vz**. Documented in Data, not here.

## The 3 moments a hook *can* fire (reference)
- **SessionStart** — once, when a chat begins (load rules, run a startup check, print standing permissions).
- **UserPromptSubmit** — every time you send a message, before the AI reads it (inject a reminder).
- **Stop** — when the AI finishes a reply (check uncommitted work, verify version sync, print cost).

## If vz gets hooks later
- This file gets the list — **one plain-English bullet per hook**, e.g.:
  - **Stop → "check version badge":** read badge in `template.html` → compare to latest `VERSIONS` → warn if they mismatch.
- Until then: **vz runs no hooks.**
