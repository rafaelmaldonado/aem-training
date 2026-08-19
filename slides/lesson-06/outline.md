# Class 6 · Pages and editable templates

**Date:** Monday, August 24, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how an editable template defines the authoring contract for new pages, distinguish template type, structure, initial content, policies and page-owned content, and prepare developers to begin the Week 2 Guide Page practice.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 3–4.  
**Required source images:** none. Repository paths and console states will be represented as precise technical diagrams.

## Slide 1 — Design the authoring contract before the page.

**Role:** cover  
**Intent:** position the editable template as a reusable authoring contract, not a visual screenshot.

- Class 6 · Week 2 · Day 6 · August 24, 2026.
- Pages and editable templates.
- Template type → editable template → page instance.
- Juan Maldonado.

**Visual idea:** a template blueprint produces several page instances while retaining shared structure and separating page-owned content.

## Slide 2 — A page instance points to both template and renderer.

**Role:** page anatomy  
**Intent:** connect Day 4 request resolution to the authoring model without confusing the template with the rendering component.

- Page content lives below `/content/wknd/.../<page>/jcr:content`.
- `cq:template` identifies the editable template used to create the page.
- `sling:resourceType` identifies the page component used for rendering.
- Example template: `/conf/wknd/settings/wcm/templates/guide-page`.
- Example renderer: `wknd/components/page`.

**Visual idea:** one selected `jcr:content` Resource with two explicit property arrows: authoring contract under `/conf` and page component under `/apps`.

## Slide 3 — A template type seeds the editable template once.

**Role:** lifecycle process  
**Intent:** explain creation-time reuse without implying ongoing inheritance from the template type.

- A developer or qualified template author defines an approved template type.
- The template type supplies a starting structure, initial content and page component resource type.
- Creating `guide-page` copies that starting definition into the editable template.
- After creation, the template can evolve independently.
- The remaining template-type reference is informational, not dynamic inheritance.

**Visual idea:** a copy-at-creation checkpoint separates `/template-types/page` from `/templates/guide-page`; later edits clearly diverge.

## Slide 4 — One editable template has distinct branches.

**Role:** repository anatomy  
**Intent:** make the template definition inspectable as a repository structure rather than an abstract console object.

- Template root: `/conf/wknd/settings/wcm/templates/guide-page`.
- `jcr:content` stores metadata and lifecycle status such as draft, enabled or disabled.
- `structure/jcr:content` defines the shared page structure.
- `initial/jcr:content` defines the starting content copied to new pages.
- `policies/jcr:content` connects design rules; policy behavior is covered in Day 7.

**Visual idea:** a repository tree with four color-coded branches, owners and lifecycle labels.

## Slide 5 — Structure remains connected to every page.

**Role:** synchronization model  
**Intent:** show which template changes continue to affect existing pages.

- Structure defines components and layout shared by pages using the template.
- Locked structure components cannot be moved or deleted by page authors.
- An unlocked container exposes an authoring area inside the shared skeleton.
- Later structure changes are reflected on existing pages created from the template.
- Use structure only for elements that must remain consistent across instances.

**Visual idea:** one template structure fans out to three existing pages; a locked header update propagates while page-owned areas remain unchanged.

## Slide 6 — Initial content is copied only when the page is created.

**Role:** before-and-after timeline  
**Intent:** prevent initial content from being mistaken for a synchronization or migration mechanism.

- Initial content gives a new page an editable starting point.
- At page creation, initial content is merged with structure and copied below the new page.
- Page authors can edit or remove eligible copied content.
- Changing template initial content affects future pages, not existing pages.
- Use an explicit migration when existing page content must change.

**Visual idea:** a timeline with Page A created before an initial-content change and Page B created after it; only Page B receives the new default.

## Slide 7 — Classify the Guide Page contract by lifecycle.

**Role:** decision exercise  
**Intent:** bridge the mental model into the Week 2 individual practice.

- Shared, locked site header → template structure.
- Main authoring container → template structure, unlocked for page authors.
- Editable introductory placeholder → initial content.
- Allowed components and design defaults → content policy, introduced in Day 7.
- Guide-specific text, images and metadata → page content under `/content`.

**Visual idea:** a Guide Page wireframe connected to five repository destinations, each justified by owner and change frequency.

## Slide 8 — Key takeaways

**Role:** summary  
**Intent:** retrieve the five distinctions needed before developers begin the Guide Page practice.

1. The page stores content; the page component renders it.
2. The editable template governs how pages begin and what remains shared.
3. The template type is copied at template creation; it is not dynamic inheritance.
4. Structure stays connected; initial content is copied once.
5. Choose structure, initial content, policy or page content by lifecycle and owner.

**Visual idea:** five connected lifecycle cards from template type through page-owned content.

## Slide 9 — Questions

**Role:** Q&A  
**Intent:** close without requiring a live demonstration.

- Which Guide Page element is hardest to classify?
- What should update existing pages when the template changes?
- Which value controls rendering, and which value records the template?

**Visual idea:** a page blueprint with three highlighted decision points and no additional task instructions.

## Source anchors

- Adobe Experience Manager as a Cloud Service: Editable Templates.
- Adobe Experience Manager Sites: Templates Console and Page Editor template documentation.
- Adobe WKND tutorial: Pages and Templates.
- Course syllabus and Week 2 Guide Page practice in `reference/aem-course-topics.html` and `reference/wknd-project-backlog.html`.
