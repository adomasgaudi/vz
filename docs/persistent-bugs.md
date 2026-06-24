# Persistent bugs (PB-n)

Recurring bugs — fixed before, came back. Log device+browser, prior failed fixes, the real root,
and leave a `PB-n` comment at the fix site. Read this before touching an area with a `PB-n`.

---

## PB-1 — Chart axis numbers are arbitrary / change on pan-zoom
- **Recurrences:** 2 (line engine, then bar engine)
- **Seen on:** Android / Brave (owner's phone), money-flow + rankings charts.
- **Symptom:** axis tick labels are non-round (€-0.19M, €1.47M, €3.12M…) and CHANGE to different
  arbitrary values when the chart is panned/zoomed, instead of round numbers (€0M, €1M, €2M…) that
  stay put and just slide.
- **Root cause:** ticks computed as `min + k·span/N` (evenly divides the *current view*), so every
  pan re-derives ugly values. Fix = "nice" ticks at `1/2/5 × 10ⁿ` multiples of a step, which are
  round and only move position as you pan.
- **Fixes:**
  - `drawFinSvg` (line/bar-line engine) — niceTicks added earlier (y-axis).
  - `drawBarsSvg` (horizontal rank bars) — niceTicks added v0.1.181 (x-axis). *(was missed when the
    line engine was fixed — same class, different function.)*
- **Guard against re-introduction:** any new chart axis MUST use a niceTicks-style round-step
  generator, never `min + k·span/N`. Both engines now share the same logic; copy it for any new one.
