# Class 4 · How Sling resolves a request

Date: Thursday, August 20, 2026  
Audience: frontend-oriented developers learning AEM from the ground up  
Duration: 30 minutes online + a read-only request trace using supplied evidence or local Author if available  
Observable outcome: given one Sling request, each developer can identify the resolved resource, decompose the request information, follow the resource type hierarchy and justify which script or servlet handles the response.

## Slide 1 · Cover — Follow the request, not a guess

- Class 4 · Week 1 · Day 4 · August 20, 2026
- How Sling resolves a request
- URL → resource → resource type → script or servlet → response
- Presenter: Juan Maldonado
- Visual: one browser request crossing five evidence checkpoints
- Role: cover; establish the repeatable trace used throughout the session

## Slide 2 · Sling resolves a resource before rendering code

- The request URI is resolved against Sling's resource tree
- The resolved Resource becomes the subject of the request
- Its resource type guides script or servlet selection
- Rendering code is chosen after resource resolution, not before it
- Visual: ordered pipeline with the Resource checkpoint visually dominant
- Role: concept explanation; replace the controller-route-first mental model

## Slide 3 · The resource path determines how the URL is decomposed

- Example request: `/content/wknd/us/en/guide.print.a4.html/chapter-1`
- Resource path: `/content/wknd/us/en/guide`
- Selectors: `print.a4`; extension: `html`; suffix: `/chapter-1`
- HTTP method such as `GET` is separate request information
- The resource path is the longest resolvable match; do not assume it ends at the first dot
- Visual: one URL ruler split into resource path, selectors, extension and suffix
- Role: anatomy; make `RequestPathInfo` observable without memorizing a fragile string rule

## Slide 4 · `sling:resourceType` names rendering capability

- The property belongs to the resolved content Resource
- A relative type such as `wknd/components/guide` is resolved through Sling search paths
- Project component implementation normally lives under `/apps/wknd/components/guide`
- The content path and implementation path remain separate responsibilities
- Visual: selected content Resource connected by its exact property value to a component under `/apps`
- Role: translation; connect authored content to project-owned rendering code

## Slide 5 · Resource super types delegate instead of copying

- A project component can declare `sling:resourceSuperType`
- Resolution can continue through the resource type hierarchy
- A WKND proxy can inherit Core Component behavior while owning project configuration
- Override only the behavior the project actually needs
- Visual: child resource type → super type → inherited capability, with one narrow project override
- Role: architecture; explain reuse without copied product implementation

## Slide 6 · Request details narrow the script or servlet candidates

- Resource type and its hierarchy define where Sling looks
- Selectors and extension describe the requested representation
- HTTP method distinguishes read rendering from write or action handling
- The most specific matching candidate wins; fallback follows the type hierarchy
- A plain HTML component request commonly resolves to the component's HTL script
- Visual: candidate-resolution board using type, selectors, extension and method as evidence filters
- Role: process; explain selection without presenting a misleading fixed filename formula

## Slide 7 · Use one repeatable, read-only trace

- Request: `GET /content/wknd/us/en/guide/jcr:content/root/container/guide.html`
- Resolved Resource: `/content/wknd/us/en/guide/jcr:content/root/container/guide`
- Request information: no selectors, extension `html`, method `GET`
- Property: `sling:resourceType = wknd/components/guide`
- Component: `/apps/wknd/components/guide`
- Handler: the matching HTL script or inherited candidate produces the response
- Visual: six numbered checkpoints with exact paths, properties and observable evidence
- Role: worked example; usable from a supplied snapshot with local Author optional

## Slide 8 · Key takeaways

- Sling resolves the Resource before selecting rendering code
- URL decomposition depends on the resolved resource path
- `sling:resourceType` and its super type hierarchy connect content to capability
- Resource type, selectors, extension and method participate in handler resolution
- Every transition in a useful trace has a path, property or request value as evidence
- Visual: compact five-link resolution chain with one evidence tag per link
- Role: summary; retrieval checkpoint before questions

## Slide 9 · Questions

- Which checkpoint is still unclear?
- Which request value would you inspect first?
- Where could resolution fall back to inherited behavior?
- Visual: a request path bending into a technical question mark with three evidence markers
- Role: questions-only close; no live demo dependency or assignment handoff

## Practice concept

Annotate one supplied Sling request trace. Record the request URL and method, resolved resource path, selectors, extension, suffix if present, `sling:resourceType`, resource super type if present, selected handler and one piece of evidence for every transition. Local Author may be used, but the exercise must work from supplied screenshots and repository paths.

## Required source images

None.

## Technical references

- Apache Sling · URL decomposition: https://sling.apache.org/documentation/the-sling-engine/url-decomposition.html
- Apache Sling · Servlets and Scripts: https://sling.apache.org/documentation/the-sling-engine/servlets.html
- Apache Sling · Sling Scripting: https://sling.apache.org/documentation/bundles/scripting.html
