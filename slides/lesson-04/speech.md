# Class 4 · Speaker notes

## Slide 1: Follow the request, not a guess

Today we will use one repeatable trace for Sling requests. We will not begin by guessing which HTL file runs. We will start with the request, resolve the Resource, inspect the request information, follow the resource type and only then identify the handler that creates the response.

The goal is evidence, not memorization. At every arrow, we should be able to point to a URL segment, a Resource path, a property or a selected script or servlet.

## Slide 2: Sling resolves a Resource before rendering code

Sling is resource-first. The request URI is resolved against a resource tree through a ResourceResolver. The resulting Resource becomes the subject of the request, and its type guides the next resolution step.

This is different from starting with a controller route that directly names a handler. In Sling, the URL does not simply point to an HTL file. First prove which Resource was resolved; then explain why a particular handler is eligible.

## Slide 3: The resource path determines URL decomposition

Read this URL from left to right, but do not split it mechanically at the first dot. Sling first finds the longest part that resolves to a Resource. Once that boundary is known, the remaining request path can be described as selectors, extension and suffix.

In this example, the resource path ends at `guide`, the selector string is `print.a4`, the extension is `html` and the suffix is `/chapter-1`. The HTTP method is important for handler resolution, but it is separate from RequestPathInfo.

## Slide 4: sling:resourceType names rendering capability

Now select the resolved content Resource and read its `sling:resourceType`. The value `wknd/components/guide` is a relative resource type, not an absolute `/apps` path stored in content.

Sling uses that type through its search paths to find project capability such as `/apps/wknd/components/guide`. The authored instance and the implementation remain separate: one stores content; the other defines how that content can render or behave.

## Slide 5: Resource super types delegate instead of copying

A project proxy can declare `sling:resourceSuperType` and reuse a Core Component through the resource type hierarchy. That gives the project a stable component identity while delegating established behavior.

The practical rule is to override only what the project needs. Copying the parent implementation creates code that the project must maintain and disconnects it from upstream fixes. Delegation keeps the ownership boundary explicit.

## Slide 6: Request details narrow the handler candidates

Handler resolution considers several pieces of evidence together. The resource type and its hierarchy define the search space. Selectors and extension describe the requested representation. The HTTP method distinguishes ordinary read rendering from other request behavior.

There can be multiple eligible scripts or servlets. Sling favors the most specific matching candidate and can continue through the resource type hierarchy when the direct type does not provide one. The useful question is not “what filename always runs?” but “which candidate matches this Resource and this request most closely?”

## Slide 7: Follow one Sling request with evidence

Walk through the checkpoints in order. The request includes `.html`; the resolved Resource path does not. RequestPathInfo shows no selectors, the `html` extension and no suffix, while the method remains the separate value `GET`.

The Resource exposes `sling:resourceType = wknd/components/guide`. That points us to the project component under `/apps`, where `guide.html` is the direct candidate shown here. If no direct candidate matched, the next investigation would follow `sling:resourceSuperType`. This entire trace can be taught from a supplied snapshot; no repository change is required.

## Slide 8: Key takeaways

Keep the order intact: resolve the Resource, decompose the request, follow the resource type hierarchy, explain handler selection and observe the response. Skipping a checkpoint turns a diagnosis into a guess.

Ask someone to choose one arrow and name the evidence that proves it. If the answer is only “AEM normally does that,” the trace is not complete yet.

## Slide 9: Questions

Which checkpoint is still unclear? Which request value would you inspect first? Where could resolution fall back to inherited behavior?

Use the questions to revisit a specific arrow or value. No live demonstration is required to close the session.
