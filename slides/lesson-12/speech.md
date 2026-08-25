# Class 12 · Detailed speaker notes

## How to use these notes

- Keep one CSS change as the thread from frontend source to the browser request.
- Separate source, generated output, AEM clientlib and delivered response every time.
- Treat category names and dependency relationships as runtime contracts.
- Close with audience questions only; do not turn the final slide into an exercise.

## Slide 1: Client Libraries and frontend workflow

Introduce the session’s three threads: category contracts, the source-to-clientlib build, and browser-delivery debugging. Identify Class 12, Week 3, Day 12, September 1, 2026, Juan Maldonado and the 30-minute scope. Keep this slide orienting; the technical model begins on Slide 2.

## Slide 2: A clientlib category is the runtime contract

A client library is included by category, not by its repository folder name. Show how `cq:ClientLibraryFolder`, `categories`, `css.txt` and `js.txt` work together: the folder defines the clientlib, the category identifies it to consumers, and the text files define ordered content.

Emphasize that a category rename changes every include, dependency or embed that names it. Verify the exact category in the page output before changing source code.

## Slide 3: Source and generated clientlib output are different artifacts

Follow the pipeline from `ui.frontend/src/main/webpack` through the frontend build, `ui.frontend/dist`, the clientlib generator and the packaged clientlib under `ui.apps`. Source and build configuration are edited and versioned; generated artifacts are replaced by the next build.

The debugging question is: which stage failed to carry the change forward? A correct source edit is only the first checkpoint.

## Slide 4: Dependencies load; embeds combine

Contrast the two graph edges. `dependencies` cause another category to be requested alongside the current one. `embed` copies another category’s content into the current clientlib output. Both affect order, duplication and cache behavior, but they produce different network evidence.

Use the smallest relationship that satisfies the delivery contract. Verify the resulting requests rather than reasoning from configuration alone.

## Slide 5: Load shared assets once; scope component assets narrowly

Start with ownership. Shared site foundations belong in the site category and should be included once. Component-specific behavior should remain narrow unless it truly participates in every page.

Broad inclusion makes every page pay for a local feature; duplicate inclusion creates ordering and cache ambiguity. The goal is not the maximum number of clientlibs—it is one clear owner for each asset and one intended delivery path.

## Slide 6: Debug the artifact the browser actually received

Walk the evidence ladder in order: confirm the page includes the intended category, inspect the clientlib request, verify status and response content, map that response back to generated output, then trace the generated output to source and build logs. Use the browser console only for runtime failures after delivery is proven.

This order avoids editing configuration while the browser is receiving a cached or different artifact. A source diff is evidence of intent; the response body is evidence of delivery.

## Slide 7: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce prompts, a review activity, practice or an assignment.
