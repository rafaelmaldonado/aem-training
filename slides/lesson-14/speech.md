# Class 14 · Detailed speaker notes

## How to use these notes

- Keep one Guide Card as the thread across width, zoom, keyboard and empty-state checks.
- Describe observable behavior before discussing implementation details.
- Separate Author guidance from Publish output every time.
- Close with audience questions only; do not turn the final slide into an exercise.

## Slide 1: Responsive, accessible and empty states

Introduce the session’s three threads: reflow under real constraints, native keyboard behavior, and intentional states for authors and visitors. Identify Class 14, Week 3, Day 14, September 3, 2026, Juan Maldonado and the 30-minute scope.

The Guide Card is complete only when it remains usable outside the ideal screenshot. Today we will change width, zoom, input method and content state, then observe what the browser and AEM editor actually do.

## Slide 2: Responsive means behavior under constraints

Use the four frames to make one distinction clear: responsive quality is preserved information and functionality, not a set of device screenshots. The same title, action and reading order must survive a narrower container, enlarged content and a longer localized label.

Test narrow width and 200% zoom independently. A layout can fit a small viewport yet fail when browser zoom changes available CSS pixels or enlarges text. Look for overlap, clipping, hidden actions and page-level horizontal scrolling, then verify that the project’s clientlib solves the behavior in the actual page context.

## Slide 3: Native semantics provide behavior before ARIA

Read the native path first: a heading structures the card, a link navigates and a button performs an action. These elements already participate in focus order, expose platform semantics and provide their expected keyboard interaction.

The generic-element path must reconstruct those guarantees with roles, focusability and JavaScript. An ARIA role is a promise to implement the full interaction model; it does not create that behavior. Start with native HTML and add ARIA only for relationships or states the native language cannot express.

## Slide 4: Keyboard operation is an end-to-end contract

Follow the Tab path from the previous page element through the Guide Card and onward to the next control. The order should match the visual and reading sequence. At every stop, focus must remain visible and must not be hidden by sticky content or overlap.

Activate the link and button with their expected keys, verify that focus does not jump unexpectedly, and confirm there is a safe exit from the component. The meaningful test is the complete task with the mouse untouched, not an isolated `:focus-visible` rule in DevTools.

## Slide 5: Empty states serve authors and visitors differently

Start from the shared Guide Card Resource and the single `isEmpty` decision. In Author edit or preview mode, an otherwise invisible component needs a useful `cq-placeholder` so the author can find, select and configure it.

Publish has a different responsibility. It should omit the author placeholder and avoid broken links, empty headings or wrappers with no meaning. Verify configured Author, empty Author and empty visitor output as separate states even though they share one emptiness contract.

## Slide 6: Test content extremes, not only the happy path

Read the matrix by row and then by constraint. Configured and empty content are only the beginning; long titles, localized labels and unexpected values expose fixed-height, nowrap and assumption-heavy implementations quickly.

When one intersection fails, record the DOM and interaction evidence, fix the narrowest responsible layer, and rerun that same check. A screenshot alone cannot prove focus order, activation or clean visitor markup. Acceptance should include keyboard, zoom, long-title and empty-state evidence.

## Slide 7: Key takeaways

Use the five bullets as the review checklist. Responsive quality preserves information and functionality under width, zoom and content pressure. Native semantics give the component the correct interaction foundation. Keyboard testing covers order, visible focus, activation and a safe exit.

Keep author placeholders useful and keep them out of Publish. Finally, test configured, empty, long and localized content with browser-visible evidence. The governing principle is: test behavior, not screenshots.

## Slide 8: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce prompts, a review activity, practice or an assignment.
