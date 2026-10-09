# Session 41 · Make asynchronous work retryable

**Monday, October 12, 2026 · Week 9 · 30 minutes**

Ten English PNG slides with Spanish presenter notes in [the lesson page](../../lessons/0041-retryable-asynchronous-work.html#slide-deck). Render them with `python3 slides/lesson-41/render_slides.py` from the repository root. Slides 2–6 teach the concepts; slide 7 applies them in the [local Author SDK demo](../../reference/examples/session-41/README.md); slide 8 connects loop prevention to that setup. The illustrated console panels echo Author, CRXDE Lite and `error.log` without claiming to be SDK screenshots. The demo injects one controlled `FAILED` result after persisting `guide-a`.

| Slide | Purpose |
| --- | --- |
| 01 | State the goal: make asynchronous work safe to retry. |
| 02 | Distinguish launcher, workflow and Sling Job responsibilities. |
| 03 | Explain at-least-once delivery and the effect/acknowledgement gap. |
| 04 | Define idempotency through a stable business key and state check. |
| 05 | Explain `OK`, `FAILED`, `CANCEL` and queue retry policy. |
| 06 | Show durable progress across small batches. |
| 07 | Apply the concepts in the local two-Guide demo: `FAILED`, retry and replay. |
| 08 | Prevent loops by separating trigger and write paths. |
| 09 | Summarize the five key takeaways. |
| 10 | Passive Questions / Thank you closing. |
