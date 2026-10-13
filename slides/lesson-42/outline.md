# Session 42 · Call an external service safely

**Tuesday, October 13, 2026 · Week 9 · 30 minutes**

Eleven English PNG slides follow the Session 37 presentation style: one teaching object per slide, concrete examples, and short conclusions. The detailed reasoning stays in the [Spanish study guide](../../reference/session-42-study-guide.md); [the lesson](../../lessons/0042-external-http-integration.html#slide-deck) contains Spanish presenter notes and source links.

Edit `deck_content.json` for titles, takeaways and notes, and `render_slides.py` for visual layouts. Then run `python3 slides/lesson-42/render_slides.py` and inspect the PNGs at presentation size.

| Slide | Teaching object |
| --- | --- |
| 01 | Cover: contract, wait and recovery. |
| 02 | Common needs: commerce data, CRM lead and translation job. Check existing AEM integrations first. |
| 03 | Workflow → OSGi service → provider, with a sample HTTP exchange and response contract. |
| 04 | Cloud Manager secret value → OSGi reference → outbound header, plus handling rules. |
| 05 | Illustrative page latency beside separate connection and read limits. |
| 06 | Four expected local log results and the next action for each. Revisit during the demo. |
| 07 | Finite retry budget and a conceptual remote write with a lost response. |
| 08 | Real client excerpt and the limits of this status probe. |
| 09 | Local versus Cloud network paths and diagnostic order. |
| 10 | Five bullet takeaways. |
| 11 | Questions / Thank you. |

The commerce, CRM and translation requests are illustrative provider contracts, not features of the supplied probe. The retry budget, global deadline and POST idempotency sequence are design examples, not implemented by the supplied GET probe. The local log lines are expected evidence, not screenshots of Author SDK.
