# the vz constitution

The principles that keep this repo correct — named the way AI systems are actually
governed. Every principle is one of two kinds, sorted by the **verifiability test**.
(*constitution* = a governing set of principles, after Constitutional AI.)

## The verifiability test (meta-principle; sorts every principle)
- **Can a program decide it for certain — binary, no judgment?**
  - **Yes → a deterministic guardrail.** Back it with a **verifier** (a hook that checks and blocks). Reliable, cheap, every run.
  - **No → a guideline.** Needs judgment; at most an **LLM-as-judge** can grade it. Surface as a reminder, never auto-block.
- Why this split (from the research):
  - **Verifiable rewards (RLVR)** beat learned judges on reliability + cost — *deterministic verifiers, binary feedback, less reward hacking.* So verify whenever you can.
  - **LLM-as-judge** carries verbosity/position/self-enhancement bias (~65% expert agreement) → a model-graded rule is a hint, not an enforcement.
  - **Reward hacking** caveat: even a verifier gets gamed if its check is loose — pin the real goal, not a proxy.

## The two kinds
- **Deterministic guardrail (verifier)** — a program decides it for certain (`string==string`, diff touches a file, `n>m`, `node --check`). Enforced by a **hook that blocks**. Binary, no judgment.
  - AI term: *verifier / verifiable check (RLVR)* · eng term: *error-level lint rule / CI gate*.
- **Guideline (LLM-as-judge)** — needs judgment (compact? right abstraction? SP fair? whole bug-class fixed?). Graded at most by an **LLM-as-judge**, else a human call. Reminder only, never auto-blocked.
  - AI term: *LLM-as-judge / reward model* · eng term: *warning / code smell*.

## Deterministic guardrails (verifiers — each should become a hook)
- **V1** `index.html` == `build_site.py` output → block · *no hook yet*
- **V2** `index.html` never hand-edited (diff touches index w/o template) → block · *no hook yet*
- **V3** version badge == latest `VERSIONS` entry → block · *no hook yet*
- **V4** `template.html` changed ⇒ badge bumped → block · *no hook yet*
- **V5** new `VERSIONS` entry has a numeric SP → block · *no hook yet*
- **V6** embedded JS valid (`node --check`) → block · *no hook yet*
- *No hook yet = verifier agreed, unwritten. An unenforced verifier is just a guideline — writing the hooks is the next job.*

## Guidelines (LLM-as-judge / human call — reminder only)
- **G1** is the SP estimate fair? (effort-vs-value, not measurable)
- **G2** is the design compact / on-brand? (taste)
- **G3** fixed the whole bug *class*, not just the shown case?
- **G4** terminology right? (turnover vs revenue)

## Adding a principle
- One line → apply the verifiability test → file as a **deterministic guardrail** (+ hook to write) or a **guideline**.
- A guardrail isn't real until its verifier (hook) exists.
