# GOVERNANCE.md — the vz Codex

The rules that keep this repo correct. Every entry is a **Gate** or a **Nudge**,
decided by the **Gate Test**. No third kind; "rule" is too vague to use.

## Principle 0 — the Gate Test (meta-rule; classifies every entry)
- **Can a dumb computer decide it for certain — yes/no, no judgment?**
  - **Yes → Gate.** Write a hook that blocks. Never let it slip.
  - **No → Nudge.** Needs a mind; surface as a reminder, never auto-block.
- Prevents two failures:
  - **Gate left as a Nudge** — a provable thing left to memory, so it slips (was: "forgot to rebuild").
  - **Nudge faked as a Gate** — a judgment call wired into a dumb script.
- Adding anything → apply the Gate Test first, then file it.

## Definitions
- **Gate** — a check a dumb computer decides for certain (string==string, diff touches a file, n>m, pattern match). Enforced by a **hook that blocks**. Binary, no judgment. If it needs a human/AI to "look and decide", it's not a Gate.
- **Nudge** — a check needing judgment (compact? right abstraction? SP fair? whole bug-class fixed?). Enforced by a **reminder only**. Never auto-blocked.
- *Modern AI names (if useful):* Gate ≈ verifier / verifiable reward · Nudge ≈ LLM-as-judge / reward model · this whole file ≈ a constitution.

## Gates (deterministic → hook; each should become a hook)
- **G1** `index.html` == `build_site.py` output → block · *TODO hook*
- **G2** `index.html` never hand-edited (diff touches index w/o template) → block · *TODO*
- **G3** version badge == latest `VERSIONS` entry → block · *TODO*
- **G4** `template.html` changed ⇒ badge bumped → block · *TODO*
- **G5** new `VERSIONS` entry has a numeric SP → block · *TODO*
- **G6** embedded JS valid (`node --check`) → block · *TODO*
- *TODO = agreed, hook not written yet. A Gate with no hook is a Nudge in disguise — writing the hooks is the next job.*

## Nudges (judgment → reminder only, never auto-block)
- **N1** is the SP estimate fair? (effort-vs-value, not measurable)
- **N2** is the design compact / on-brand? (taste)
- **N3** fixed the whole bug *class*, not just the shown case?
- **N4** terminology right? (turnover vs revenue)

## Adding to the Codex
- One line → apply the Gate Test → file as **Gate** (+hook TODO) or **Nudge**.
- A Gate isn't done until its hook exists.
