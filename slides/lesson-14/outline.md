# Class 14 · Responsive layout in AEM

**Date:** Thursday, September 3, 2026
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations
**Duration:** 30 minutes online
**Deck goal:** trace how templates, Layout Containers, breakpoints, Layout Mode, responsive-grid output, project CSS and Core Image delivery cooperate to produce a responsive AEM page.
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–13.
**Required source images:** none. AEM editor states, repository nodes, DOM classes, CSS breakpoints and browser requests will be represented as precise technical diagrams.
**Output:** PNG/HTML slides and detailed speaker notes only; no PPTX.

## Slide 1 — Responsive layout in AEM

**Role:** opening overview
**Intent:** identify the session, presenter and date while previewing the AEM-specific responsive path.

- Class 14 · Week 3 · Day 14 · September 3, 2026.
- Responsive layout in AEM.
- Today: Layout Container, Layout Mode, breakpoints and browser delivery.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus a compact left-to-right path from the AEM editor to responsive grid output and the browser.

## Slide 2 — Responsiveness has several owners.

**Role:** responsibility architecture
**Intent:** prevent one layer from becoming responsible for every responsive decision.

- The template enables the Layout Container and defines the page structure authors may use.
- Breakpoint configuration gives the editor and emulator shared device-width names.
- Layout Mode lets authors place, resize or hide components for an available breakpoint.
- The responsive grid turns persisted layout choices into browser-visible classes.
- Component CSS and Core Components preserve behavior and efficient delivery inside that layout.

**Visual idea:** a responsibility chain maps Template → Layout Container → Breakpoints / Layout Mode → persisted layout → responsive-grid DOM → component CSS and browser result.

## Slide 3 — Layout Container creates the responsive grid.

**Role:** AEM structure anatomy
**Intent:** connect template configuration, repository structure and the browser grid.

- A Layout Container is a grid paragraph system, not just another visual wrapper.
- It can be the page’s main content container, an authorable component, or both.
- The Container Component uses `layout = responsiveGrid` when it owns responsive layout behavior.
- Grid columns provide placement and width; nested grids should remain exceptional and as flat as possible.
- Enabling a container in policy does not replace configuring the page template and responsive CSS.

**Visual idea:** three synchronized inspectors show a template structure, a `responsiveGrid` container resource and the resulting `aem-Grid` / `aem-GridColumn` DOM.

## Slide 4 — Layout Mode authors a layout per breakpoint.

**Role:** editor workflow
**Intent:** demonstrate how an author changes component placement and width without rewriting component markup.

- Select a configured breakpoint in the emulator, then enter Layout Mode.
- Resize and place components with horizontal snap-to-grid behavior.
- Define when components sit side by side, stack or remain hidden for that layout.
- A desktop layout does not automatically prove the intended tablet or phone result.
- Preview and Publish verification must follow the authoring change.

**Visual idea:** one page moves through Desktop → Tablet → Phone editor frames; the same Teaser and Guide Card change grid spans and stack order while content remains the same.

## Slide 5 — Breakpoint configuration and CSS must agree.

**Role:** configuration alignment
**Intent:** show why editor behavior and browser behavior drift when breakpoint contracts differ.

- AEM breakpoint nodes name device groups and define the widths used by the page editor.
- Project responsive-grid CSS must implement matching media-query boundaries.
- The emulator is an authoring tool; the browser and CSS remain the runtime authority.
- Changing only the emulator configuration produces a misleading authoring preview.
- Record breakpoint ownership and test immediately below, at and above each boundary.

**Visual idea:** align `cq:responsive/breakpoints` values with a clientlib breakpoint rail; highlight a mismatch that produces different editor and browser layouts.

## Slide 6 — Persisted layout becomes DOM evidence.

**Role:** repository-to-browser trace
**Intent:** make an authoring change observable outside the editor.

- A layout choice is stored with responsive metadata for the component resource.
- Rendered grid classes expose breakpoint, width and offset decisions to the browser.
- DevTools should connect the selected component to its grid-column classes and active CSS rule.
- Inspect the exact persisted and rendered evidence before adding a compensating override.
- A correct trace is Author action → repository state → DOM class → CSS rule → rendered layout.

**Visual idea:** a five-stage evidence trace follows one Guide Card from the resize handle through repository responsive data to `aem-GridColumn` classes and the computed layout.

## Slide 7 — Components must cooperate with the grid.

**Role:** frontend implementation checklist
**Intent:** separate page-layout responsibility from internal component responsiveness.

- The grid controls the component’s available column; component CSS controls behavior inside that space.
- Avoid fixed widths and heights that contradict the authored span or content pressure.
- Flex and grid children often need `min-width: 0`, wrapping and fluid media to shrink correctly.
- Scope project CSS to the component contract instead of overriding global AEM grid classes.
- Core Component client libraries are a starting point; the project still owns behavior in its page context.

**Visual idea:** compare one Guide Card that cooperates with 12-, 8- and 4-column spans against a failing card with fixed width, overflow and a global grid override.

## Slide 8 — Layout width and image delivery are related, not identical.

**Role:** responsive-media integration
**Intent:** connect this session to the established Core Image contract without repeating Class 9.

- The authored grid span determines the rendered image box, not the transferred bytes by itself.
- Core Image policy defines available widths and delivery options.
- Core Image v3 exposes browser-native responsive candidates; the browser selects a source.
- Local evidence can use the Adaptive Image Servlet; cloud projects may enable Web-Optimized Image Delivery.
- Verify grid width, rendered dimensions and the selected Network request together.

**Visual idea:** responsive grid span → rendered image box → Core Image candidate widths → selected browser request, with CSS size and transfer size clearly separated.

## Slide 9 — Key takeaways

**Role:** summary
**Intent:** consolidate the AEM-specific responsive layout contract.

- Templates and policies enable the responsive authoring boundary.
- Layout Container, breakpoints and Layout Mode control authored page composition.
- Persisted responsive state must be traceable to DOM grid classes and active CSS.
- Components cooperate with the grid instead of overriding it globally.
- Image efficiency requires both layout evidence and the selected Network request.

**Visual idea:** five numbered checkpoints connect template, editor, repository, browser layout and image delivery; end with the principle “TRACE THE LAYOUT, DO NOT GUESS.”

## Slide 10 — Questions

**Role:** Q&A
**Intent:** invite questions raised by participants and close the session without introducing another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** a quiet closing composition with a subtle editor-to-grid-to-browser motif and generous open space; no prompts, numbered questions or technical callouts.

## Session use

- **Retrieval:** Which layer owns the page grid, and which layer owns behavior inside a component’s assigned columns?
- **Demo:** resize a Guide Card and Core Image in Layout Mode, then trace the persisted layout, rendered grid classes, computed CSS and selected image request.
- **Assignment:** configure and verify one two-column desktop layout that stacks intentionally at a narrower breakpoint.
- **Acceptance:** editor and browser layouts agree at the tested boundaries; the component has no global grid override; repository, DOM, CSS and Network evidence explain the result.

## Source anchors

- [Configuring the Layout Container and Layout Mode — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/site-creation/responsive-layout)
- [Responsive Layout for content authors — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/authoring/page-editor/responsive-layout)
- [Responsive Design for AEM developers — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/full-stack/responsive-design)
- [Responsive breakpoints — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/sites/developing/responsive-breakpoints)
- [Core Image Component — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/wcm-components/image)
- [Web-Optimized Image Delivery — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/web-optimized-image-delivery)
- Course syllabus and Week 3 Guide Card practice in `reference/aem-course-topics.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
