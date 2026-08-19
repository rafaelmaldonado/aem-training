# Class 7 · Content policies and the Style System

**Date:** Tuesday, August 25, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how content policies govern component capability by template context, trace the policy mapping under `/conf`, distinguish policy defaults from authored values, and define a small, testable authoring contract for the Week 2 Guide Page practice.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 3–4 and Day 6.  
**Required source images:** none. Repository mappings, authoring states and responsibility boundaries will be represented as precise technical diagrams.

## Slide 1 — Govern authoring choices without changing component code.

**Role:** cover  
**Intent:** frame policies as the layer that turns reusable components into a controlled authoring experience.

- Class 7 · Week 2 · Day 7 · August 25, 2026.
- Content policies, Allowed Components and Style System.
- Component capability → content policy → author choice.
- Juan Maldonado.

**Visual idea:** one component implementation passes through a policy control layer and emerges as a focused set of choices in the Page Editor.

## Slide 2 — A policy configures capability by context.

**Role:** conceptual model  
**Intent:** separate technical component capability from the configuration permitted in one template location.

- Component code defines what is technically possible.
- A content policy defines what is available or configured in a specific template context.
- The same component type can use different policies in different templates or locations.
- Content authors use the resulting choices without editing component code.
- Changing a shared policy can affect every template location that references it.

**Visual idea:** one component implementation feeds two template contexts; each policy exposes a different, deliberately limited authoring contract.

## Slide 3 — Follow the policy mapping before editing code.

**Role:** repository trace  
**Intent:** make policy resolution concrete enough to diagnose a missing or unexpectedly configured component.

- Start with the component's relative path inside the editable template.
- Inspect the matching location below `/conf/wknd/settings/wcm/templates/guide-page/policies/jcr:content/...`.
- Its `cq:policy` property stores a relative reference to the policy definition.
- Follow that reference into `/conf/wknd/settings/wcm/policies/...`.
- If authoring behavior is wrong, verify this mapping before blaming rendering code.

**Visual idea:** a repository inspector trace from the template component path to `cq:policy`, then to the resolved policy definition, with each handoff labeled.

## Slide 4 — Allowed Components belongs to the container policy.

**Role:** authoring control  
**Intent:** explain why an installed component may still be unavailable in the component browser.

- A layout container's policy controls which components authors may insert there.
- Installed and rendered successfully does not mean allowed in the current container.
- Prefer a small, purpose-specific set instead of exposing an entire component group.
- A component missing from the selector is commonly a policy or mapping issue, not a rendering defect.
- Validate both states: an intended component is available and an unrelated component remains unavailable.

**Visual idea:** a container-policy funnel admits Title, Text and Image while an unrelated component remains visibly outside the authoring boundary.

## Slide 5 — Policy defaults are not authored instance values.

**Role:** configuration comparison  
**Intent:** distinguish reusable design configuration from content stored on an individual component instance.

- Component-specific design properties and defaults can be stored in a policy.
- Examples include permitted image widths, lazy-loading behavior and container layout settings.
- Policy values configure a template context; dialog values belong to an authored component instance.
- Reuse a policy instead of copying the same default to every node below `/content`.
- Check policy reuse before changing a default because multiple template locations may share it.

**Visual idea:** a split repository view compares policy defaults under `/conf` with per-instance authored properties under `/content`.

## Slide 6 — Style System maps semantic choices to deployed CSS.

**Role:** end-to-end pipeline  
**Intent:** show every dependency between an author-facing style name and the rendered result.

- The template author configures a readable Style Name and its CSS class in the component policy.
- Example: `Featured` → `cmp-guide--featured`.
- The developer implements that class in a deployed client library; optional behavior may require JavaScript.
- The content author selects the approved style in the Page Editor.
- AEM applies the class to the component decoration wrapper; the Style System does not create the CSS implementation.

**Visual idea:** a five-stage chain from Style Name to policy mapping, client library, author selection and rendered wrapper class.

## Slide 7 — Define a small Guide Page authoring contract.

**Role:** practice specification  
**Intent:** translate policy mechanics into evidence developers can implement and explain this week.

- Main content container: responsive layout with only Title, Text and Image available.
- Policy default: one intentional component behavior that is visible and explainable.
- Style choices: `Standard` and `Featured`, named by intent rather than visual appearance.
- Developer owns proxy components and CSS; template author owns policy choices; content author selects from the approved menu.
- Evidence must show one allowed component, one disallowed component, one style choice and the corresponding repository locations.

**Visual idea:** a Guide Page contract sheet connects each authoring choice to its owner, repository location and visible verification evidence.

## Slide 8 — Key takeaways

**Role:** summary  
**Intent:** retrieve the five distinctions developers need before completing the Guide Page practice.

1. Component code defines capability; policy configures it by template context.
2. `cq:policy` connects a template location to a policy definition under `/conf`.
3. A container policy controls which components authors can insert.
4. Policy defaults differ from values authored on individual content instances.
5. Expose a few semantic style choices backed by deployed, tested CSS.

**Visual idea:** five linked control points from component implementation to a safe authoring choice.

## Slide 9 — Questions

**Role:** Q&A  
**Intent:** close without requiring a live demonstration.

- Which Guide Page capability belongs in policy rather than component code?
- What evidence would explain a component missing from the editor?
- Which semantic style choices are worth supporting and testing?

**Visual idea:** a policy map with three highlighted diagnostic decision points and no assignment instructions.

## Source anchors

- Adobe Experience Manager as a Cloud Service: Editable Templates.
- Adobe Experience Manager Sites: Templates and the Allowed Components policy configuration.
- Adobe Experience Manager Sites: Style System authoring documentation.
- Adobe WKND tutorial: Pages and Templates.
- Adobe Experience Manager Learn: Style System technical implementation and best practices.
- Course syllabus and Week 2 Guide Page practice in `reference/aem-course-topics.html` and `reference/wknd-project-backlog.html`.
