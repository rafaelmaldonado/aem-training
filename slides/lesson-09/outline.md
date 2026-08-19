# Class 9 · Assets and accessible images

**Date:** Thursday, August 27, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how an authored image connects a DAM asset, a Core Image proxy, responsive delivery and context-specific alternative text, then define the evidence needed to review that contract on the Week 2 Guide Page.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–8.  
**Required source images:** none. Asset references, responsive candidates, alternative-text decisions and review evidence will be represented as precise technical diagrams.

## Slide 1 — Treat every image as content, delivery and accessibility.

**Role:** cover  
**Intent:** frame an image as a complete delivery contract rather than a decorative binary.

- Class 9 · Week 2 · Day 9 · August 27, 2026.
- Assets, Core Image and accessible delivery.
- DAM reference → responsive source → accessible meaning.
- Juan Maldonado.

**Visual idea:** one DAM asset flows through a component contract into three observable outcomes: the browser request, the rendered image and the accessibility tree.

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

## Slide 7 — Verify the Guide Page image contract with evidence.

**Role:** practice evidence matrix  
**Intent:** turn the session into a repeatable review of the Week 2 practice without depending on a live demo.

- Repository evidence: the component's `fileReference` resolves to the intended DAM asset.
- Informative state: the rendered element has a meaningful, non-empty `alt` value.
- Decorative state: the rendered element has an explicit `alt=""` value.
- Missing or invalid state: authoring guidance and rendering produce a safe, observable result rather than a missing `alt` attribute.
- Delivery evidence: browser markup and the network request show the available candidates, selected source and rendered dimensions.
- Maintenance evidence: incoming references are inspected before an asset is moved, replaced, unpublished or deleted.

**Visual idea:** a three-row informative/decorative/missing-state matrix crosses repository reference, rendered HTML, accessibility result and network evidence.

## Slide 8 — Key takeaways

**Role:** summary  
**Intent:** retrieve the five decisions required for a reliable and accessible image implementation.

1. Page components reference DAM assets; they do not copy the managed binary.
2. Proxy the Core Image Component instead of rebuilding proven image behavior.
3. Alternative text follows the image's purpose in the current context.
4. Responsive delivery requires multiple candidates; CSS sizing alone does not reduce transfer bytes.
5. Verify the repository reference, rendered alternative-text state and browser-selected source.

**Governing principle:** the same asset can require different accessible meaning in different page contexts.

**Visual idea:** five linked checkpoints move from managed asset to component capability, contextual meaning, responsive request and review evidence.

## Slide 9 — Questions

**Role:** Q&A  
**Intent:** close with discussion prompts and no dependency on a live demonstration.

- When is the Guide Page image informative rather than decorative?
- Which evidence proves that the page references the intended DAM asset?
- What shows that the browser received an appropriate responsive candidate?

**Visual idea:** a simplified asset-to-browser path with the accessibility, reference and delivery decisions highlighted and generous space for discussion.

## Source anchors

- Adobe Experience Manager Core Components: Image Component.
- Adobe Experience Manager as a Cloud Service: Web-Optimized Image Delivery.
- Adobe Experience Manager as a Cloud Service: Manage Digital Assets.
- W3C Web Accessibility Initiative: Images Tutorial.
- Course syllabus and Week 2 Guide Page practice in `reference/aem-course-topics.html` and `reference/wknd-project-backlog.html`.
