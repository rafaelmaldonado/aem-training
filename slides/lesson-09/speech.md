## Slide 1: Treat every image as content, delivery and accessibility.

Today we are going to treat an image as more than a file placed on a page. In AEM, an authored image creates a contract across three concerns: the managed asset and its references, the bytes delivered to the browser, and the meaning exposed to people who cannot rely on the pixels.

Follow the path on the slide from left to right. A DAM asset is selected through the component, Core Image prepares delivery behavior, the browser requests a source, and the rendered markup carries an accessibility decision. We will inspect each part separately, then reconnect them as evidence for the Week 2 Guide Page practice.

## Slide 2: An authored image is a reference, not a copied binary.

The first distinction is ownership. The asset under `/content/dam` owns the original binary, its renditions and reusable metadata. The Image component on the page is a different Resource under `/content`; it stores a `fileReference` that points back to the asset. It does not copy the image binary into the page content tree.

That separation is useful because one managed asset can be reused across several pages, but it also creates a dependency. If we move, replace, unpublish or delete the asset, every incoming reference may be affected. Before an asset lifecycle change, the safe question is not only “Can I change this file?” but also “Which pages depend on this path?”

Now that the reference boundary is clear, we can decide which component capability should deliver it.

## Slide 3: Use the Core Image capability before custom markup.

The project-owned component can remain intentionally thin. A proxy such as `/apps/wknd/components/guide-image` inherits the installed Core Image v3 capability through `sling:resourceSuperType`. This lets the project keep its own resource type and policy boundary while reusing established authoring, DAM integration, responsive delivery, lazy loading and accessibility behavior.

The policy above the proxy governs choices such as allowed widths and relevant defaults. The Core Component below it owns the complex delivery behavior. Our project should add only what a verified requirement cannot obtain through configuration or supported extension. Copying the product implementation would make every future fix and upgrade our responsibility.

One practical caveat: verify the Core Components version installed in the project before selecting v3. Capability comes from the installed dependency, not from a path we wish existed.

## Slide 4: Alternative text describes purpose in context.

Start at the center of the diagram: what job does this image perform on this page? That question determines the alternative-text strategy. An informative image needs a concise description of its essential meaning. A decorative image needs an explicit empty alternative so assistive technology can ignore it.

If the image is the only content inside a link or control, describe the action or destination. For a complex chart or diagram, a short alternative identifies it, while the detailed equivalent belongs in nearby content. Notice that none of these decisions begin with the filename or with the phrase “image of.”

The important distinction in the warning is that a missing `alt` attribute is not the same as an intentionally empty value. Empty is a deliberate accessibility decision; missing usually means the contract was not completed.

## Slide 5: DAM metadata is a source, not the final decision.

DAM metadata can save authors from repeatedly typing a useful description, but shared metadata cannot know every future page context. Here the same asset begins with a reusable description: “Hikers crossing a suspension bridge.” That description works when the hero image is informative.

The gallery background uses the same pixels only as decoration, so its correct result is an empty alternative. Inside a linked Guide card, the image becomes functional and the alternative should identify the destination or action. The asset is unchanged; the page purpose changed.

This gives us a simple responsibility split. Developers and template authors provide safe controls and sensible defaults. Authors decide what the image means in the current page. Metadata proposes; page purpose decides.

## Slide 6: Responsive delivery lets the browser choose appropriate bytes.

Responsive delivery begins with the widths allowed by the component policy. Core Image exposes candidates such as 480, 768 and 1200 pixels, and the browser selects among them using the actual layout and device density. We should not promise that it always chooses the smallest candidate, because the browser has more context than a simple viewport-width comparison.

The lower rail separates two measurements that are often confused. CSS can render an image at a narrower visual width without changing the source that was transferred. To prove efficient delivery, inspect both the rendered dimensions and the network request. Lazy loading is another delivery decision: it can defer an offscreen request, but it does not replace responsive source selection.

For local practice, the Adaptive Image Servlet and browser developer tools provide enough evidence. Web-Optimized Image Delivery and WebP are useful AEM as a Cloud Service capabilities, but they are not required for this local exercise.

## Slide 7: Verify the Guide Page image contract with evidence.

This matrix is the review checklist for the Week 2 Guide Page. In every row, begin with repository evidence: does `fileReference` resolve to the intended DAM asset? Then inspect the rendered HTML, the accessibility result and the selected network request. A screenshot alone cannot prove those relationships.

For the informative state, we expect a meaningful non-empty alternative. For the decorative state, we expect an explicit empty value. For a missing or invalid authoring state, we expect clear guidance and safe output rather than an omitted `alt` attribute or a broken image contract.

Finally, the maintenance checkpoint extends the review beyond initial authoring. Before changing the asset lifecycle, inspect incoming references. This review can be completed in each developer's local repository and local Author environment; it does not require Cloud Manager or a shared deployment.

## Slide 8: Key takeaways

Use these five checkpoints whenever an image enters an AEM page. First, confirm that the page references a managed DAM asset instead of duplicating it. Second, keep the project component thin by proxying the supported Core Image capability. Third, choose alternative text from the purpose of the image in the current context.

Fourth, verify that responsive delivery offers useful candidates; CSS dimensions alone are not network evidence. Fifth, connect the repository reference, rendered alternative-text state and browser-selected source in one review. The governing principle is worth remembering: the same asset can require different accessible meaning in different page contexts.

## Slide 9: Questions

Let us close by applying the contract to the Guide Page. When is its image informative, and when is it only decorative? What exact repository evidence proves that the component references the intended DAM asset? What would you inspect in the browser to determine whether it received an appropriate responsive candidate?

Use the asset-to-browser path as the discussion map. A strong answer should connect purpose, stored reference and observable delivery evidence rather than naming only a dialog option or showing only the final page.
