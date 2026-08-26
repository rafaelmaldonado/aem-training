# Class 9 · Assets and accessible images

**Date:** Thursday, August 27, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how an authored image connects a DAM asset, a Core Image proxy, responsive delivery and context-specific alternative text, then define the evidence needed to review that contract on the Week 2 Guide Page.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–8.  
**Required source images:** none. Asset references, responsive candidates, alternative-text decisions and review evidence will be represented as precise technical diagrams.

## Slide 1 — Assets, Core Image and accessible delivery

**Role:** opening overview
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 9 · Week 2 · Day 9 · August 27, 2026.
- Assets, Core Image and accessible delivery.
- Today: managed DAM references, context-specific alternatives, and responsive browser delivery.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for DAM ownership, accessible meaning and responsive delivery.

## Slide 2 — An authored image is a reference, not a copied binary.

**Role:** repository anatomy  
**Intent:** separate the managed asset from the component instance that uses it.

- The binary, renditions and reusable metadata belong to a DAM asset below `/content/dam/...`.
- The page's Image component is a separate Resource below `/content/.../jcr:content/...`.
- Its `fileReference` points to the DAM asset path; the page component does not duplicate the binary.
- Context-specific properties remain on the component instance while shared metadata remains with the asset.
- Moving, replacing, unpublishing or deleting an asset can affect every incoming reference.

**Visual idea:** a DAM asset inspector and a page-component inspector are connected by one highlighted `fileReference`, with downstream pages exposing the dependency radius.

## Slide 3 — Use the Core Image capability before custom markup.

**Role:** capability stack  
**Intent:** show the smallest project-owned implementation that retains product-provided behavior.

- A project proxy can declare `sling:resourceSuperType="core/wcm/components/image/v3/image"`.
- The Core Image Component supplies authoring behavior, DAM integration, adaptive delivery, responsive candidates, lazy loading and accessibility controls.
- The template author configures allowed widths and relevant defaults in the component policy or design dialog.
- Verify the installed Core Components version before selecting a component version.
- Extend only for a verified requirement gap; do not copy the Core Component implementation into the project.

**Visual idea:** a thin project proxy sits above the Core Image v3 capability stack and below the Guide Page policy, making ownership boundaries explicit.

## Slide 4 — Alternative text describes purpose in context.

**Role:** accessibility decision tree  
**Intent:** choose alternative-text behavior from the image's job on the page, not from its filename.

- Informative image: provide concise text that conveys the essential information.
- Decorative image: render an explicit empty value, `alt=""`, so assistive technology can ignore it.
- Functional or linked image: describe the action or destination, not the image's appearance.
- Complex image: provide a short alternative and a detailed equivalent in nearby content.
- A filename or the phrase “image of” is not a meaningful default description.

**Visual idea:** one question—“What purpose does the image serve here?”—branches into informative, decorative, functional and complex outcomes with exact rendered-alt examples.

## Slide 5 — DAM metadata is a source, not the final decision.

**Role:** context comparison  
**Intent:** distinguish reusable asset metadata from the meaning required by a particular page.

- The same asset can be informative in one context, decorative in another and functional inside a link.
- “Get alternative text from DAM” can provide a reusable default when the asset metadata is meaningful.
- The page context may require an author override because shared metadata cannot know the image's local purpose.
- A decorative choice must produce `alt=""`; omitting the `alt` attribute is a different and unsafe state.
- Developers and template authors provide safe controls and defaults; authors confirm the contextual meaning.

**Visual idea:** one Guide asset branches into a hero, a decorative gallery tile and a linked card, each with a different but valid alternative-text result.

## Slide 6 — Responsive delivery lets the browser choose appropriate bytes.

**Role:** delivery pipeline  
**Intent:** connect policy widths, generated candidates and the request selected by the browser.

- The component policy defines the allowed image widths available for responsive delivery.
- Core Image v3 supplies multiple width candidates and lets the browser select among them for the current layout and device density.
- Lazy loading can defer an offscreen request until the image approaches the viewport.
- CSS changes rendered dimensions; by itself, it does not reduce the bytes downloaded.
- Web-Optimized Image Delivery can add WebP delivery on AEM as a Cloud Service; local verification can rely on the Adaptive Image Servlet and the browser network trace.

**Visual idea:** one asset becomes 480, 768 and 1200 pixel candidates; a browser request selects one while a separate CSS box makes the distinction between layout size and transfer size visible.

## Slide 7 — Asset references turn maintenance into a dependency decision.

**Role:** lifecycle dependency radius
**Intent:** give reference impact the dedicated treatment required by asset moves, replacement and publication.

- Every `fileReference` creates an incoming dependency on the managed DAM asset.
- Replacing an asset can change every consuming page even when their component content remains unchanged.
- Moving, unpublishing or deleting an asset can break references or public delivery.
- Inspect incoming references and affected publication state before a lifecycle change.
- Record the impacted pages and verification plan as part of the change evidence.

**Visual idea:** one DAM asset sits at the center of a dependency-radius map; several consuming pages expose the impact of replace, move, unpublish and delete operations.

## Slide 8 — Verify the Guide Page image contract with evidence.

**Role:** practice evidence matrix  
**Intent:** turn the session into a repeatable review of the Week 2 practice without depending on a live demo.

- Repository evidence: the component's `fileReference` resolves to the intended DAM asset.
- Informative state: the rendered element has a meaningful, non-empty `alt` value.
- Decorative state: the rendered element has an explicit `alt=""` value.
- Missing or invalid state: authoring guidance and rendering produce a safe, observable result rather than a missing `alt` attribute.
- Delivery evidence: browser markup and the network request show the available candidates, selected source and rendered dimensions.
- Maintenance evidence: incoming references are inspected before an asset is moved, replaced, unpublished or deleted.

**Visual idea:** a three-row informative/decorative/missing-state matrix crosses repository reference, rendered HTML, accessibility result and network evidence.

## Slide 9 — Key takeaways

**Role:** summary
**Intent:** consolidate the five review rules for managed, accessible and efficiently delivered images.

- Store a `fileReference` to the managed DAM asset instead of copying the binary.
- Start with a project proxy to Core Image before custom delivery markup.
- Choose alternative-text behavior from the image purpose in its page context.
- Verify responsive candidates and the selected request, not only rendered CSS size.
- Inspect incoming references and publication state before asset lifecycle changes.

**Visual idea:** five concise checkpoints connect DAM ownership, Core Image, contextual alternatives, responsive evidence and lifecycle safety.

## Slide 10 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close the session without introducing another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** a quiet closing composition with a subtle asset-to-browser line motif and generous open space; no prompts, numbered questions or technical callouts.

## Source anchors

- Adobe Experience Manager Core Components: Image Component.
- Adobe Experience Manager as a Cloud Service: Web-Optimized Image Delivery.
- Adobe Experience Manager as a Cloud Service: Manage Digital Assets.
- W3C Web Accessibility Initiative: Images Tutorial.
- Course syllabus and Week 2 Guide Page practice in `reference/aem-course-topics.html` and `reference/wknd-project-backlog.html`.
