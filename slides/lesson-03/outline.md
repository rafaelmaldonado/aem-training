# Class 3 · JCR, resources and repository boundaries

Date: Wednesday, August 19, 2026  
Audience: frontend-oriented developers learning AEM from the ground up  
Duration: 30 minutes online + guided inspection using a supplied snapshot or local Author if available  
Observable outcome: each developer can inspect an AEM page, distinguish nodes from properties, and explain whether an item belongs to `/content`, `/conf` or `/apps`.

## Slide 1 · Cover — Read AEM as a resource tree

- Class 3 · Week 1 · Day 3 · August 19, 2026
- JCR, resources and repository boundaries
- From an authored page to the code that renders it
- Presenter: Juan Maldonado
- Visual: one page branching into `/content`, `/conf` and `/apps`
- Role: cover; establish the inspection path used throughout the session

## Slide 2 · JCR stores a hierarchy, not a table of pages

- A repository is an addressable tree
- Nodes create structure and paths
- Properties store values on nodes
- Node types describe the node's intended shape and behavior
- Visual: annotated tree with paths, nodes and properties clearly separated
- Role: concept explanation; replace the file-folder and relational-table mental models

## Slide 3 · A node holds structure; properties hold values

- Child nodes represent nested structure
- Properties can be scalar or multi-value
- `jcr:primaryType` identifies the node's primary type
- A path identifies the node; a property name identifies a value on it
- Visual: repository inspector close-up with node, child and property callouts
- Role: vocabulary; give the group precise terms for repository inspection

## Slide 4 · One page has two important layers

- The page container is commonly a `cq:Page` node
- `jcr:content` stores the page's authored content and metadata
- Component instances appear below `jcr:content`
- The browser URL and repository path describe related but different views
- Visual: page anatomy from `cq:Page` to `jcr:content` and component descendants
- Role: architecture; connect the Sites console to stored page content

## Slide 5 · Sling exposes repository content as resources

- A Sling Resource has a path, properties and children
- `ValueMap` provides a convenient view of resource properties
- `sling:resourceType` connects content to rendering capability
- Prefer the Resource API unless the requirement is specifically JCR-level
- Visual: JCR node view translated into a Sling Resource view
- Role: translation; connect repository storage to application code

## Slide 6 · `/content`, `/conf` and `/apps` answer different questions

- `/content`: what authors manage — pages, assets and component instances
- `/conf`: how a site is configured — editable templates, policies and contextual configuration
- `/apps`: how the application works — project components, dialogs, HTL and client libraries
- The boundary communicates ownership, mutability and deployment lifecycle
- Visual: three responsibility lanes with example paths and owners
- Role: comparison; prevent content, configuration and code from being treated as interchangeable

## Slide 7 · Trace one Guide Page without changing it

- Start at a supplied `/content/.../guide` page path
- Inspect `jcr:content` and a component's authored properties
- Read its `sling:resourceType`
- Locate the matching component under `/apps`
- Identify the related template or policy under `/conf`
- Visual: evidence chain `/content` → resource type → `/apps`, with `/conf` supplying policy
- Role: worked example; usable from a static snapshot, with local Author optional

## Slide 8 · Key takeaways

- AEM content is an addressable hierarchy of nodes and properties
- `cq:Page` and `jcr:content` describe different parts of a page
- Sling Resources are the application-facing view of repository content
- `/content`, `/conf` and `/apps` separate authored content, configuration and code
- Visual: compact four-point recap around a single repository tree
- Role: summary; retrieval checkpoint before questions

## Slide 9 · Questions

- What path is still unclear?
- Which property would you inspect first?
- Which repository boundary needs another example?
- Visual: restrained question markers connected to the three repository branches
- Role: questions-only close; no live demo dependency or assignment handoff

## Practice concept

Annotate a supplied Repository Browser or CRXDE snapshot and trace one page across `/content`, `/conf` and `/apps`. A local instance may be used if available, but the session does not depend on it.

## Required source images

None. After outline approval, reuse the approved Lesson 2 slide 7 visual system as a style-only reference.
