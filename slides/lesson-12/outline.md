# Class 12 · Client Libraries and frontend workflow

**Date:** Tuesday, September 1, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how AEM client libraries turn versioned frontend source into browser-delivered CSS and JavaScript, distinguish categories, dependencies and embeds, and debug the Guide Card asset path from source through build and page delivery.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–11.  
**Required source images:** none. Repository nodes, build stages, category graphs and browser evidence will be represented as precise technical diagrams.

## Slide 1 — Client Libraries and frontend workflow

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 12 · Week 3 · Day 12 · September 1, 2026.
- Client Libraries and frontend workflow.
- Today: category contracts, source-to-clientlib builds, and browser-delivery debugging.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for categories, the frontend build and browser evidence.

## Slide 2 — A clientlib category is the runtime contract.

**Role:** concept anatomy  
**Intent:** separate a category name from its repository location and generated files.

- A client library is a `cq:ClientLibraryFolder` that organizes CSS, JavaScript and supporting resources.
- `categories` gives the library one or more logical names that a page or another clientlib can request.
- The consumer references a category, not an implementation file path inside `/apps`.
- A clientlib stored under `/apps` uses `allowProxy=true` so public requests can be served through `/etc.clientlibs/`.
- `css.txt` and `js.txt` define which files belong to the delivered CSS and JavaScript output.

**Visual idea:** dissect one WKND clientlib node into category, proxy setting, CSS/JS manifests and the public request it produces.

## Slide 3 — Source and generated clientlib output are different artifacts.

**Role:** build pipeline  
**Intent:** make the full-stack WKND asset path explicit and establish which files developers should edit.

- Developers change Sass, TypeScript, CSS or JavaScript beneath `ui.frontend/src`.
- Webpack compiles and optimizes those sources into `ui.frontend/dist`.
- `aem-clientlib-generator` transforms the build output into `clientlib-site` and `clientlib-dependencies` beneath `ui.apps`.
- Maven orchestrates the frontend build and packages the generated clientlibs for deployment to AEM.
- Version the source and build configuration; do not hand-edit generated clientlib output that the next build will replace.

**Visual idea:** a five-stage artifact pipeline labels source, compiler, generated output, deployable package and browser-delivered file, with an edit boundary around source only.

## Slide 4 — Dependencies load; embeds combine.

**Role:** relationship comparison  
**Intent:** distinguish two clientlib graph operations and their effect on browser delivery.

- `dependencies` declares categories that must be loaded for the current category to work.
- `embed` copies the selected libraries' content into the current clientlib output.
- Use a dependency when the other category should remain an independently delivered runtime contract.
- Use an embed when one owning clientlib intentionally assembles a consolidated delivery unit.
- Keep the graph small and intentional; careless relationships create duplicate code, hidden ordering and difficult cache behavior.

**Visual idea:** side-by-side graphs show category A loading category B as a separate request versus category A delivering B inside its own output.

## Slide 5 — Load shared assets once; scope component assets narrowly.

**Role:** inclusion and ownership architecture  
**Intent:** connect category inclusion to the narrowest owner of each frontend responsibility.

- In the WKND archetype, site and dependency categories are included through the editable template's Page Policy.
- HTL can also use AEM's clientlib helper to request CSS, JavaScript or both by category.
- Site shell, typography and shared design tokens belong in the site-level bundle.
- Guide Card selectors should start from a project-owned component class and avoid leaking into unrelated markup.
- A component should not emit repeated global tags; add isolated JavaScript only when native HTML and CSS are insufficient.

**Visual idea:** several Guide Card instances converge on one page-level category while concentric ownership zones separate the site bundle, scoped component CSS and optional instance-safe JavaScript.

## Slide 6 — Debug the artifact the browser actually received.

**Role:** evidence ladder  
**Intent:** provide a repeatable diagnostic path for a source change that does not appear in the page.

- Confirm the intended source file changed and is imported by the frontend entry point.
- Inspect compiled output and the generated clientlib before changing AEM configuration.
- Verify the expected category is included by the page policy or HTL call.
- Inspect page source and the Network panel for the actual `/etc.clientlibs/` CSS or JavaScript request.
- Check response content, status, cache behavior and browser console before editing another layer.

**Visual idea:** an evidence ladder moves from Git source to import, build artifact, installed category, page request and browser result; each rung has a pass/fail observation.

## Slide 7 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close the session without introducing another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** a quiet closing composition with a subtle frontend-delivery line motif and generous open space; no prompts, numbered questions or technical callouts.

## Session use

- **Retrieval:** Why can a CSS source change exist in Git but not appear in the browser?
- **Demo:** change WKND frontend source, run the build and find the resulting clientlib request.
- **Assignment:** add Guide Card styling through the existing frontend pipeline.
- **Acceptance:** source is versioned, generated output is not, and the browser receives one intended asset.

## Source anchors

- [Client libraries and front-end workflow — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/client-side-libraries)
- [Review the full-stack AEM project's ui.frontend module — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/enable-frontend-pipeline-devops/review-uifrontend-module)
- [Using Client-Side Libraries — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/implementing/developing/introduction/clientlibs)
- [WKND ui.frontend module — Adobe GitHub](https://github.com/adobe/aem-guides-wknd/blob/main/ui.frontend/README.md)
- Course syllabus and Week 3 Guide Card practice in `reference/aem-course-topics.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
