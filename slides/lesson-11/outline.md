# Class 11 · Safe and readable HTL

**Date:** Monday, August 31, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** establish HTL as the markup-focused view layer, use expressions and block statements for clear rendering, keep preparation logic behind a small model boundary, and verify context-aware output for configured and missing Guide Card data.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–9.  
**Required source images:** none. HTL source, prepared values, rendered DOM and escaping behavior will be represented as precise technical diagrams.

## Slide 1 — Safe and readable HTL

**Role:** opening overview
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 11 · Week 3 · Day 11 · August 31, 2026.
- Safe and readable HTL.
- Today: the view boundary, structural HTL statements, and context-aware output.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for prepared values, readable template structure and safe browser output.

## Slide 2 — Keep the template boundary narrow.

**Role:** responsibility boundary  
**Intent:** separate data preparation from direct markup production.

- HTL owns elements, attributes, conditional structure and iteration.
- Resource properties and simple model getters provide values to the template.
- A Sling Model or service owns complex preparation, orchestration and business rules.
- HTL should reveal the rendered contract without forcing a reviewer to decode hidden control flow.
- Moving logic out of HTL is useful only when the view would otherwise become hard to explain or repeat.

**Visual idea:** three responsibility lanes—Resource/model data, thin HTL view and browser DOM—with complex orchestration rejected from the view lane.

## Slide 3 — Expressions read values where the markup needs them.

**Role:** expression anatomy  
**Intent:** teach concise value access while keeping names aligned with the rendered HTML.

- `${properties.title}` reads a property from the current Resource.
- `${card.title}` reads a prepared getter exposed through `data-sly-use`.
- Text nodes, ordinary attributes and URI attributes are different output contexts.
- Use meaningful identifiers such as `card`, `title` and `link`; avoid opaque aliases.
- Prefer a direct expression over a temporary variable that adds no clarity.

**Visual idea:** one Guide Card fragment annotates each expression with its source value, inferred output context and final DOM value.

## Slide 4 — Conditions and lists should make every state visible.

**Role:** rendering-state flow  
**Intent:** use HTL block statements for structure while defining the missing-data outcome explicitly.

- `data-sly-test` keeps or removes an element from the rendered output.
- `data-sly-list` repeats markup for a collection without Java scriptlets.
- Attach a block statement to an existing semantic element when possible; use `<sly>` only when no suitable element exists.
- A configured Guide Card renders its link, image and title.
- Missing required data produces a safe visitor result and an author-visible empty state.

**Visual idea:** one decision splits the same HTL fragment into configured, empty-author and empty-visitor DOM results.

## Slide 5 — Templates and calls reuse small markup contracts.

**Role:** reuse comparison  
**Intent:** prevent repetition without creating a private component framework inside HTL.

- `data-sly-template` declares a reusable markup fragment with explicit parameters.
- `data-sly-call` invokes that fragment with named values.
- Reuse a template when repeated markup has one stable purpose and a small input contract.
- Keep page or component responsibilities visible at the call site.
- Prefer repeated simple markup when an abstraction would make the output harder to trace.

**Visual idea:** two repeated metadata rows converge on one small named template, contrasted with a crossed-out chain of nested generic templates.

## Slide 6 — Trace one Guide Card from Resource to DOM.

**Role:** end-to-end code trace  
**Intent:** combine prepared values, conditions, attributes and the empty state in one inspectable example.

- The authored component Resource provides title, link and image reference data.
- `data-sly-use.card` exposes a small view contract when preparation is required.
- `data-sly-test` selects configured or empty output.
- The link URI and visible text are rendered in their correct contexts.
- Evidence connects stored properties, model getters, HTL source and final DOM.

**Visual idea:** a four-column trace—Resource, view contract, HTL fragment and rendered DOM—using the same Guide Card values throughout.

## Slide 7 — Output context is part of the security contract.

**Role:** context-aware escaping matrix  
**Intent:** show what HTL infers automatically and where an explicit display context is mandatory.

- HTL automatically applies context-aware escaping to expressions in HTML text and attribute values.
- URI attributes such as `href` and `src` use URI validation rather than plain text escaping.
- Expressions inside JavaScript or CSS require an explicit context such as `scriptString` or `styleString`; otherwise HTL suppresses their output.
- `context='html'` filters markup and is not a substitute for a trustworthy content contract.
- Do not use `context='unsafe'` to silence an escaping problem.

**Visual idea:** text, attribute, URI, script and style rows show input, required context and safe output, with `unsafe` isolated as a prohibited shortcut.

## Slide 8 — Key takeaways

**Role:** summary  
**Intent:** retrieve the five rules for maintainable HTL.

1. HTL renders the view; models and services prepare complex values.
2. Direct expressions keep the source-to-markup relationship visible.
3. Conditions and lists must include a deliberate empty outcome.
4. Templates reuse small markup contracts, not speculative frameworks.
5. Output context is a security decision and must match where the value is rendered.

**Visual idea:** five checkpoints connect Resource input to a readable template and verified DOM.

## Slide 9 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close the session without introducing another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** a quiet closing composition with a subtle Resource-to-DOM line motif and generous open space; no prompts, numbered questions or technical callouts.

## Session use

- **Retrieval:** Which layer should prepare data, and which layer should render it?
- **Demo:** render Guide Card properties, a condition and an empty state.
- **Assignment:** create safe HTL for configured and missing data.
- **Acceptance:** valid markup, no business orchestration in HTL and correct output contexts.

## Source anchors

- [Getting Started with HTL — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-htl/content/getting-started)
- [HTML Template Language Specification — Adobe](https://github.com/adobe/htl-spec/blob/master/SPECIFICATION.md)
- [Core Components development guidelines — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/guidelines)
- Course syllabus and Week 3 Guide Card practice in `reference/aem-course-topics.html` and `reference/wknd-project-backlog.html`.
