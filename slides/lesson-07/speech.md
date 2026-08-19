## Slide 1: Govern authoring choices without changing component code.

Today we add the control layer that sits between a reusable component and the choices an author sees. The component defines the full technical capability. The content policy narrows and configures that capability for a specific template context. The author then works inside that approved boundary.

That separation matters because we should not fork or rewrite component code just to give two page types different authoring choices. We will follow the chain from component capability, through policy mapping, to the visible result in the Page Editor.

## Slide 2: A policy configures capability by context.

Start on the left with one component implementation. Its code is identical in both branches. The Guide Page and Article Page can still expose different options because each template location resolves to its own content policy.

This is configuration by context, not duplicated implementation. It also introduces a governance concern: if several template locations reference one shared policy, changing that policy changes the authoring contract for every consumer. Before editing it, we need to know its scope.

## Slide 3: Follow the policy mapping before editing code.

Read this diagram from left to right. First locate the component inside the editable template's policy tree. At the same relative component path, AEM stores a `cq:policy` property. That value is a relative reference, which resolves to the actual policy definition below the site's policies root under `/conf`.

This trace is a useful diagnostic habit. If a component is missing from the editor or exposes the wrong choices, confirm the template location, the `cq:policy` value and the resolved definition before changing HTL, Java or JavaScript. Rendering code may be working correctly while the authoring contract is incomplete.

## Slide 4: Allowed Components belongs to the container policy.

An installed component is only a candidate. The policy on the current layout container decides whether the author can insert it there. In this example, Title, Text and Image pass through the Guide Page policy and appear in the component browser. Carousel exists in the deployment but remains outside this container's contract.

Test both sides of the rule. Showing that Title is available proves the intended capability. Showing that Carousel is unavailable proves the boundary is actually enforced. A component missing from the selector therefore points first to the container policy and its mapping, not automatically to a deployment or rendering defect.

## Slide 5: Policy defaults are not authored instance values.

The left side describes reusable configuration for a template context. A policy can define design choices and defaults for a component, and that configuration belongs below `/conf`. The right side describes one authored instance. Values such as an asset reference or alternative text belong to that component instance below `/content`.

The practical distinction is scope. Editing one instance affects one piece of content. Editing a reused policy may affect many pages and template locations. Before changing a policy default, identify its consumers and decide whether the change is intentionally shared.

## Slide 6: Style System maps semantic choices to deployed CSS.

The author should see a meaningful label such as Featured, not an implementation token. The template author maps that Style Name to a CSS class in the content policy. The developer implements the class in a client library, and the content author selects the approved option in the Page Editor.

AEM applies the selected class to the component decoration wrapper, but it does not generate the CSS. If the class is configured but the client library is missing or the selector is wrong, the author can select a style with no visible result. That is why the whole chain must be implemented and tested.

## Slide 7: Define a small Guide Page authoring contract.

For the Guide Page practice, keep the contract intentionally small. The responsive main container allows Title, Text and Image. An unrelated Carousel stays unavailable. Add one policy default whose effect can be shown, and expose only two semantic styles: Standard and Featured.

The evidence should connect the editor result to the repository configuration. Show an allowed component, a disallowed component, the selected style and the relevant locations under `/conf`. During review, explain who owns each part: developers provide proxy components and CSS, template authors configure policies, and content authors select from the approved choices.

## Slide 8: Key takeaways

The system has five control points. Code defines capability. `cq:policy` connects a template location to its policy definition. The container policy controls insertion. Policy defaults configure reusable context rather than individual content. The Style System exposes semantic choices backed by deployed and tested CSS.

The governing principle is simple: fewer meaningful choices are easier to explain, test and maintain. A policy is successful when authors can create the intended page without needing access to every technical option the component supports.

## Slide 9: Questions

Use these questions to test the boundary between implementation and configuration. Which Guide Page capability belongs in policy rather than code? If a component is missing from the editor, what repository and editor evidence would you inspect? Which style choices express durable intent and justify their testing cost?

The goal is not to find the largest possible policy. It is to define the smallest authoring contract that supports the Guide Page reliably.
