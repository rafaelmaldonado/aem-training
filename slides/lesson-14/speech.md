# Class 14 · Detailed speaker notes

## How to use these notes

- Keep one Guide Page with a Teaser, Guide Card and Core Image as the thread through the session.
- Explain each AEM responsibility before showing its repository or browser evidence.
- Distinguish authoring configuration from runtime CSS and browser behavior every time.
- Use the final slide only for questions raised by the audience.

## Slide 1: Responsive layout in AEM

Today we are narrowing the word responsive to the mechanisms that AEM actually gives us. This is not another general introduction to media queries. We will follow a page from the template and Layout Container, through the author’s Layout Mode choices, into the grid classes and browser requests that prove the result.

The important idea is that no single file controls the whole experience. A template enables the structure, an author chooses a composition, AEM persists that choice, client libraries implement the grid, and each component must behave inside the width it receives. By the end, you should be able to trace a layout instead of guessing which CSS rule to change. We will use the same Guide Page throughout so every diagram refers to one observable implementation.

## Slide 2: Responsiveness has several owners

Start at the left and read this as a responsibility chain. The template decides whether the page has a responsive authoring boundary. The Layout Container supplies the grid paragraph system. Breakpoint configuration and Layout Mode give the author named views in which components can be positioned and resized. Those choices then become persisted responsive state and rendered grid classes.

Only after that handoff does project CSS take responsibility for the behavior inside a component. This distinction prevents two common mistakes: trying to repair a missing page-grid configuration inside a component clientlib, or overriding global AEM grid classes because one card has a fixed-width child. Ask which artifact would prove each stage: template structure, editor behavior, repository state, DOM classes, computed CSS or Network request. The next slide starts with the structural owner of the page grid: the Layout Container.

## Slide 3: Layout Container creates the responsive grid

A Layout Container is more than a wrapper around child markup. It provides a paragraph system whose children participate in an AEM responsive grid. Depending on the page design, it can be the main content container built into the template, an additional component authors can insert, or both. For the Core Container Component, `layout = responsiveGrid` is the key choice that makes the container own responsive-layout behavior.

Follow the same object across the three inspectors. The template establishes the container, content resources sit below it, and the rendered browser output adds `aem-Grid` and `aem-GridColumn` classes that describe placement. Enabling the component in a policy is necessary for authoring but does not configure the whole mechanism by itself. Also call out the nesting warning: nested grids can be valid, but every level increases the layout contract developers and authors must understand. Keep the structure flat unless the requirement truly needs another grid.

## Slide 4: Layout Mode authors a layout per breakpoint

This is the author-facing workflow. First select a breakpoint that the project has configured, then enter Layout Mode. The resize handles snap components to the grid, so the author changes placement and span without changing the Teaser or Guide Card content. In the illustrated desktop layout the two components use an eight-plus-four split; tablet uses two equal spans; phone stacks both components at full width.

The exact device names and boundaries belong to the project, so treat the numbers on this sample as an implementation example, not an AEM global standard. The key behavior is that each configured view can have an intentional composition. After authoring, leave Layout Mode and verify Preview and Publish. A clean editor canvas does not prove that the runtime clientlib, nested content or component CSS will behave the same way. That runtime agreement depends on the breakpoint contract shown next.

## Slide 5: Breakpoint configuration and CSS must agree

There are two rails on this slide because two systems must describe the same boundary. The `cq:responsive/breakpoints` configuration gives the Page Editor and emulator the project’s device groups. The responsive-grid clientlib supplies the CSS media queries that actually rearrange the browser output. These values are project examples; there is no universal tablet width that every AEM site must copy.

Use the orange mismatch to explain a common failure. If the editor changes from desktop to tablet at one width but the CSS changes at another, authors see a composition that visitors cannot reproduce at the same viewport. Fixing only the emulator or only the stylesheet leaves the contract split. Record who owns these values and test on both sides of each boundary: just below it, exactly at it and just above it. Once the boundaries align, we can trace one authored resize into repository and DOM evidence.

## Slide 6: Persisted layout becomes DOM evidence

Here we take one concrete author gesture—a Guide Card resized to four of twelve columns—and follow it to the browser. The editor gesture is only the start. AEM stores responsive metadata with the component resource. During rendering, that state contributes grid-column classes such as `aem-GridColumn--default--4`, and the active responsive-grid CSS turns the class into an actual span.

In DevTools, select the component’s outer grid item rather than only its internal `.cmp-` markup. Confirm the breakpoint-specific class, any offset, the matching CSS rule and the computed width. This evidence tells us whether the problem is missing author state, unexpected rendered classes, an unloaded grid clientlib or internal component CSS. Do not add a high-specificity override until this chain is intact. The preferred diagnostic is always Author action → repository state → DOM class → active CSS → rendered layout.

## Slide 7: Components must cooperate with the grid

The page grid controls how much space a component receives; it does not guarantee that everything inside the component can shrink. Compare the same Guide Card inside twelve, eight and four columns. The passing version uses fluid media, wrapping and a shrinkable content area. In flex or grid layouts, `min-width: 0` is often the small missing rule that allows a child to become narrower than its intrinsic content.

The failing version encodes assumptions such as `width: 680px`, a fixed height or an unbreakable label. Those decisions contradict the authored span. The worst repair is a global override against `.aem-GridColumn`, because it changes every component sharing the grid contract. Scope the correction to the project component and preserve the AEM layout output. Core Component client libraries provide a useful starting point, but the project still owns how its composition behaves with real content in the actual page.

## Slide 8: Layout width and image delivery are related, not identical

This slide reconnects the layout lesson to the Core Image work from Class 9. A four-column span determines the rendered image box, but CSS width alone does not determine how many bytes the browser transfers. The Image Component policy defines candidate widths, and Core Image v3 exposes browser-native responsive sources so the browser can select an appropriate candidate for layout size and device density.

Read the chain from left to right: authored span, rendered box, configured candidates and selected Network request. The example shows a 360-pixel box and a 640-pixel candidate, but the exact selection depends on browser conditions; do not teach “always choose the smallest.” In the local SDK, the Adaptive Image Servlet provides useful request evidence. In AEM as a Cloud Service, Web-Optimized Image Delivery may be enabled through policy. In either case, record both rendered dimensions and the transferred source.

## Slide 9: Key takeaways

Use these five bullets as the review path for any responsive AEM change. First, verify that the template and policy expose the intended authoring boundary. Second, confirm that Layout Container, configured breakpoints and Layout Mode produce the required composition. Third, trace the persisted choice into grid classes and active browser CSS instead of judging only the editor screenshot.

Then review the component boundary. Internal CSS must cooperate with its assigned columns and should never repair a local defect by overriding the global AEM grid. Finally, treat responsive media as a separate but connected proof: the page layout determines the rendered box, while Core Image and the browser determine the requested source. The governing habit is simple: trace the layout, do not guess. That trace tells you which layer owns the correction and what evidence proves it.

## Slide 10: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce prompts, a review exercise, practice instructions or another technical concept on this closing slide.
