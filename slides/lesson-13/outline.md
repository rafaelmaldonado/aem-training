# Class 13 · Core Components, proxy pattern and Data Layer

**Date:** Wednesday, September 2, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how a project-owned proxy reuses a versioned Core Component through `sling:resourceSuperType`, how to choose the narrowest viable customization point, and how to preserve observable markup and Adobe Client Data Layer contracts.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–12.  
**Required source images:** none. Component inheritance, extension cost, upgrade boundaries and browser evidence will be represented as precise technical diagrams.  
**Output:** PNG/HTML slides and speaker notes only; no PPTX.

## Slide 1 — Core Components, proxy pattern and Data Layer

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 13 · Week 3 · Day 13 · September 2, 2026.
- Core Components, proxy pattern and Data Layer.
- Today: production capabilities, thin project proxies and observable runtime contracts.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three connected layers labeled Core capability, project ownership and browser contract.

## Slide 2 — Core Components are versioned production capabilities.

**Role:** capability map  
**Intent:** establish what the project receives before any custom implementation is considered.

- Core Components package tested authoring dialogs, Sling Models, HTL markup, accessibility and client-side behavior.
- Their public component versions protect existing sites when a newer implementation changes markup or behavior.
- Policies and the Style System often satisfy variation requirements without an implementation override.
- Begin each request by inspecting the installed component version, its documented features and its rendered contract.
- Custom code must justify what the existing capability cannot provide.

**Visual idea:** a versioned component capsule exposes five production surfaces—authoring, model, markup, accessibility and behavior—while a small inspection gate precedes custom code.

## Slide 3 — A proxy gives the site ownership.

**Role:** ownership architecture  
**Intent:** distinguish the project resource type that content references from the reusable product implementation.

- Content points to a stable site-specific `sling:resourceType`, not directly to `/apps/core/...`.
- The proxy owns the author-facing title, component group and project policy surface.
- Different sites can evolve their proxies independently while sharing the same Core Component implementation.
- A fully inherited proxy can remain almost empty; project code appears only for a stated requirement.
- This boundary avoids later content refactoring when one site needs different behavior.

**Visual idea:** authored content connects to `/apps/wknd/components/guide-card`; that thin project node owns authoring identity while delegating implementation downstream.

## Slide 4 — `sling:resourceSuperType` delegates implementation.

**Role:** inheritance trace  
**Intent:** make the runtime lookup explicit and contrast delegation with copying product code.

- The proxy declares an explicit versioned parent such as `core/wcm/components/teaser/v2/teaser`.
- Sling resolves missing scripts and resources through the super-type chain.
- The project reuses the Core Component implementation without duplicating it beneath `/apps/wknd`.
- Inherited behavior can continue to receive compatible product fixes and maintenance.
- Copying the product implementation creates a fork that the project must understand, secure and upgrade itself.

**Visual idea:** a vertical resolution chain runs from content resource to WKND proxy to versioned Core Component, with inherited assets flowing upward and a copied-code fork shown as maintenance debt.

## Slide 5 — Customize at the narrowest extension point.

**Role:** decision ladder  
**Intent:** order common extension mechanisms by responsibility and maintenance cost.

- Use template policy or Style System configuration when the need is an allowed option or visual variation.
- Extend the dialog only for author input the component truly needs.
- Add scoped CSS before changing semantic markup; add JavaScript only for behavior native HTML and CSS cannot provide.
- Use Sling Model delegation when business data changes but the inherited contract should remain intact.
- Override HTL only when the required markup cannot be achieved at an earlier point, and own the resulting upgrade comparison.

**Visual idea:** an ascending cost ladder moves from policy and style through dialog, scoped assets, model delegation and finally HTL override; a stop marker sits at the first rung that meets the requirement.

## Slide 6 — A version upgrade is a contract change to test.

**Role:** compatibility boundary  
**Intent:** connect explicit component versioning to evidence-based upgrades.

- The proxy pins the site to a specific Core Component resource type version.
- Changing that super type can alter dialogs, model output, markup, CSS hooks, client behavior or Data Layer values.
- Compare the current and target component documentation before changing the parent version.
- Test configured and empty states, authoring, accessibility, responsive behavior and clientlib integration.
- Keep the project diff small so inherited changes and local responsibility remain easy to distinguish.

**Visual idea:** two versioned component contracts sit on either side of an upgrade gate; six observable surfaces form the gate's test checklist.

## Slide 7 — Keep the Data Layer contract observable.

**Role:** browser evidence trace  
**Intent:** show how to verify that proxy customization preserves analytics-ready component data.

- Core Components integrate with the Adobe Client Data Layer to expose standardized component data and events.
- When enabled, rendered component markup identifies the Data Layer payload available in the browser.
- A proxy should preserve inherited identifiers, semantic markup and supported component data unless a requirement deliberately changes them.
- Inspect the rendered element, its Data Layer attribute and the corresponding browser state instead of assuming inheritance worked.
- Add custom tracking data only when the requirement needs it and document the new contract.

**Visual idea:** trace one Guide Card from rendered component ID and Data Layer attribute into the browser's `adobeDataLayer` state, ending in a compact evidence panel.

## Slide 8 — Key takeaways

**Role:** summary  
**Intent:** consolidate the five rules for safe Core Component reuse.

- Verify the existing Core Component capability and version before writing custom code.
- A proxy gives the project a stable resource type without copying product implementation.
- `sling:resourceSuperType` makes reuse and the inherited version explicit.
- Customize at the narrowest extension point and test upgrades as contract changes.
- Preserve observable markup, accessibility, client behavior and Data Layer evidence.

**Visual idea:** five concise checkpoints connect capability, ownership, delegation, extension and observable evidence.

## Slide 9 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close the session without introducing another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** a quiet closing composition with a subtle proxy-to-browser line motif and generous open space; no prompts, numbered questions or technical callouts.

## Session use

- **Retrieval:** What is lost when product component code is copied into the project?
- **Demo:** inspect a WKND proxy, its explicit super type, rendered markup and Data Layer state.
- **Assignment:** implement the Guide Card with the smallest viable extension.
- **Acceptance:** no copied product implementation; the chosen customization is justified and the inherited runtime contract remains observable.

## Source anchors

- [Component Guidelines — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/guidelines)
- [Using Core Components — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/get-started/using)
- [Customizing Core Components — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/customizing)
- [Using the Adobe Client Data Layer with the Core Components — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/data-layer/overview)
- [AEM WCM Core Components — Adobe GitHub](https://github.com/adobe/aem-core-wcm-components)
- Course syllabus and Week 3 Guide Card practice in `reference/aem-course-topics.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
