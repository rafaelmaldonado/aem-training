# Class 14 · Responsive, accessible and empty states

**Date:** Thursday, September 3, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** show how to test the Guide Card as behavior under real constraints, start from native semantics, verify complete keyboard operation and separate useful author placeholders from visitor output.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–13.  
**Required source images:** none. Responsive states, semantic controls, focus paths, author placeholders and evidence matrices will be represented as precise technical diagrams.  
**Output:** PNG/HTML slides and speaker notes only; no PPTX.

## Slide 1 — Responsive, accessible and empty states

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 14 · Week 3 · Day 14 · September 3, 2026.
- Responsive, accessible and empty states.
- Today: reflow under constraints, native keyboard behavior and author-versus-visitor states.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for responsive reflow, keyboard focus and an author/visitor state split.

## Slide 2 — Responsive means behavior under constraints.

**Role:** constraint comparison  
**Intent:** replace device-screenshot thinking with observable behavior across width, zoom and content pressure.

- A component passes when information and functionality remain available as its container narrows.
- Test a narrow viewport and 200% text or browser zoom as separate constraints; one does not prove the other.
- Text and controls should reflow without overlap, clipping or page-level two-dimensional scrolling.
- Long words, localized labels and enlarged text must not hide actions or change their meaning.
- Core Component client libraries are a starting point; the project owns detailed responsive behavior in context.

**Visual idea:** one Guide Card flows through normal width, narrow width, 200% zoom and long localized content; every state keeps the same title, action and reading order.

## Slide 3 — Native semantics provide behavior before ARIA.

**Role:** semantic comparison  
**Intent:** connect correct HTML elements to built-in roles, names and interaction behavior.

- Use headings for structure, links for navigation and buttons for actions.
- Native controls already provide focusability, keyboard behavior and platform semantics.
- An ARIA role is a promise; adding `role="button"` to a `div` does not create button behavior.
- The accessible name must describe the visible action and remain meaningful out of context.
- Add ARIA only when native HTML cannot express the required relationship or state.

**Visual idea:** compare a native Guide Card link/button path with a warning path built from generic `div` elements and compensating ARIA/JavaScript.

## Slide 4 — Keyboard operation is an end-to-end contract.

**Role:** interaction trace  
**Intent:** define the evidence required to operate the component without a pointer.

- Every interactive element must enter a logical sequential focus order.
- Focus must remain visible and not be hidden by sticky or overlapping content.
- Native links activate with Enter; native buttons support their expected keyboard interaction.
- Focus must not become trapped or jump unexpectedly after activation.
- Test the full task with the mouse untouched, not only individual selectors in DevTools.

**Visual idea:** a numbered Tab path crosses the Guide Card title link and action button, showing visible focus, activation and a safe exit to the next page element.

## Slide 5 — Empty states serve authors and visitors differently.

**Role:** dual-state architecture  
**Intent:** separate editor discoverability from clean Publish output while keeping one emptiness contract.

- An empty component must remain visible and selectable to an author in edit or preview mode.
- AEM’s author placeholder convention uses `cq-placeholder` and a useful `data-emptytext` label.
- The backing model or view contract should expose one explicit `isEmpty` decision.
- Publish should omit the author placeholder and avoid broken links, empty headings or meaningless wrappers.
- Verify configured author, empty author and empty visitor states separately.

**Visual idea:** a split screen shows the same empty Guide Card Resource in Author with a labeled placeholder and on Publish with no meaningless visitor markup.

## Slide 6 — Test content extremes, not only the happy path.

**Role:** evidence matrix  
**Intent:** turn responsive and accessibility expectations into a compact repeatable verification set.

- Exercise configured, empty, long, localized and unexpected-value states.
- Cross those states with narrow width, 200% zoom, keyboard-only operation and visible focus.
- Check the rendered DOM and interaction result, not only screenshots or CSS declarations.
- Record the first failing state, fix the narrowest responsible layer and rerun the same check.
- Acceptance requires keyboard, zoom, long title and empty-state evidence for the Guide Card.

**Visual idea:** a state-by-constraint matrix highlights pass/fail evidence and traces one failure to a narrowly scoped CSS, HTL or author-state correction.

## Slide 7 — Key takeaways

**Role:** summary  
**Intent:** consolidate the five rules for resilient component behavior.

- Responsive quality is preserved information and functionality under real constraints.
- Native semantics provide the correct starting roles and keyboard behavior.
- Keyboard testing covers order, visible focus, activation and escape from every control.
- Empty author placeholders must remain useful without leaking into Publish output.
- Test configured, empty, long and localized content with browser-visible evidence.

**Visual idea:** five concise bullet checkpoints connect reflow, semantics, focus, dual empty states and an evidence matrix.

## Slide 8 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close the session without introducing another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** a quiet closing composition with a subtle viewport-to-focus-to-state motif and generous open space; no prompts, numbered questions or technical callouts.

## Session use

- **Retrieval:** Which component state is visible to an author before any content is configured?
- **Demo:** test the Guide Card with keyboard only, a narrow viewport, 200% zoom, a long localized title and no content.
- **Assignment:** record and fix the highest-risk failure.
- **Acceptance:** keyboard, 200% zoom, long title and empty author/visitor states pass with observable evidence.

## Source anchors

- [Responsive Design of the Core Components — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/responsive)
- [Component Placeholders — Adobe Experience Manager Components: The Basics](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/implementing/developing/components/components-basics#component-placeholders)
- [WKND Custom Component: conditionally displaying the placeholder — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/custom-component)
- [Understanding WCAG 2.2 Success Criterion 1.4.10: Reflow — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)
- [Understanding WCAG 2.2 Success Criterion 1.4.4: Resize Text — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/resize-text)
- [Understanding WCAG 2.2 Success Criterion 2.4.7: Focus Visible — W3C WAI](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible)
- [ARIA Authoring Practices: Read Me First — W3C WAI](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/)
- Course syllabus and Week 3 Guide Card practice in `reference/aem-course-topics.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
