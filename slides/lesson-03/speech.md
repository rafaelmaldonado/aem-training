# Class 3 · Speaker notes

## Slide 1 · Read AEM as a resource tree

Today we will trace one authored page from what an author sees to what AEM stores and what the application renders. By the end, you should be able to name the path you are inspecting, distinguish structure from values, and identify whether the owner is content, configuration or code.

## Slide 2 · JCR stores a hierarchy, not a table of pages

JCR gives AEM an addressable hierarchy. A path identifies a node in that hierarchy. Nodes create structure, while properties store values on those nodes. This resembles a tree in a repository browser, but we should not reduce it to folders and files: nodes also have types and repository behavior.

## Slide 3 · A node holds structure; properties hold values

Select `jcr:content` and separate what appears in the hierarchy from what appears in the property table. A child component is another node. `jcr:title` is a property. `cq:tags` can be multi-value without becoming several child nodes. `jcr:primaryType` tells us the primary type of the selected node.

## Slide 4 · One page has two important layers

The page path usually identifies a `cq:Page` container. Its `jcr:content` child stores page metadata and the authored component hierarchy. That distinction matters when debugging: seeing a page in Sites does not mean every value lives directly on the page container. Also keep the browser URL separate from the repository path, even when they describe the same experience.

## Slide 5 · Sling exposes repository content as resources

Application code usually works with Sling Resources. A Resource provides a path, children and adaptable access to properties such as a `ValueMap`. `sling:resourceType` connects a content resource to rendering capability. JCR remains the persistence model, but the Resource API is normally the cleaner application abstraction unless the requirement is specifically JCR-level.

## Slide 6 · Content, configuration and code have different owners

Use the path to ask three different questions. `/content` answers what authors manage. `/conf` answers how the site is configured through templates and policies. `/apps` answers how the application works through components, dialogs, HTL and client libraries. Their ownership and change lifecycles are intentionally different.

## Slide 7 · Trace one Guide Page without changing it

This trace is read-only and can use a supplied screenshot. Start at the Guide Page under `/content`, open `jcr:content`, select one component instance and read its authored properties. Then use `sling:resourceType` to locate the implementation under `/apps`. Finally, identify the template or policy under `/conf` that governs what the author can place or configure.

## Slide 8 · Key takeaways

Retrieve the model in four steps: hierarchy, page anatomy, Resource abstraction and repository boundaries. Ask the group to explain one arrow using an exact path or property rather than a general description.

## Slide 9 · Questions

What path is still unclear? Which property would you inspect first? Which repository boundary needs another example? Keep this close focused on questions; no live demonstration is required.
