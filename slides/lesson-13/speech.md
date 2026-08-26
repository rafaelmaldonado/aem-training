# Class 13 · Detailed speaker notes

## How to use these notes

- Keep one Guide Card proxy as the thread from authored content to the Core Component and browser evidence.
- Separate project ownership from product implementation every time.
- Treat component versions, rendered markup and Data Layer output as contracts to verify.
- Close with audience questions only; do not turn the final slide into an exercise.

## Slide 1: Core Components, proxy pattern and Data Layer

Introduce the session’s three threads: Core Components as production capabilities, project ownership through a thin proxy, and runtime contracts that remain observable in the browser. Identify Class 13, Week 3, Day 13, September 2, 2026, Juan Maldonado and the 30-minute scope.

Use the Guide Card as the continuing example. The goal is not to build a component from zero; it is to own the project-facing resource type while reusing the strongest existing implementation.

## Slide 2: Core Components are versioned production capabilities

Begin with the capability that already exists. A Core Component packages more than visible markup: it includes an authoring surface, a model contract, HTL, accessibility decisions and browser behavior. Its public component version gives the site a stable implementation boundary.

Before writing custom code, inspect the installed version, the documented feature set and the rendered output. A template policy or Style System option may already satisfy the requirement with less code and a smaller upgrade burden.

## Slide 3: A proxy gives the site ownership

Follow the content resource to the project proxy. Authored content references the WKND resource type, so the site owns a stable identity even though the implementation comes from a reusable product component. The proxy also owns the author-facing title, group and policy surface.

That separation matters when two sites need different policies or behavior. Each site can evolve its proxy without rewriting existing content or changing the shared implementation for everyone else.

## Slide 4: sling:resourceSuperType delegates implementation

Read the inheritance chain from the content resource to `/apps/wknd/components/guide-card` and then to the explicit versioned parent. `sling:resourceSuperType` tells Sling where to resolve scripts or resources the proxy does not define.

This is delegation, not duplication. The thin proxy can inherit compatible maintenance and fixes from the Core Component. Copying the product implementation creates a fork whose security, behavior and future upgrades become project responsibilities.

## Slide 5: Customize at the narrowest extension point

Walk upward through the ladder. Start with policy or Style System configuration, then add only the required dialog input. Prefer scoped CSS and native browser behavior before JavaScript. Use Sling Model delegation when data changes but the inherited public contract should remain stable.

An HTL override is the last rung because the project now owns markup comparison during upgrades. The point is not that every request climbs to the top; it is to understand the full cost ladder and stop at the first extension point that actually meets the requirement.

## Slide 6: A version upgrade is a contract change to test

Changing a proxy from one versioned parent to another is more than editing a string. The target version may change the authoring dialog, model output, semantic markup, CSS hooks, client behavior or Data Layer values.

Compare the current and target documentation, then test configured and empty states across the observable surfaces. A small project diff makes it easier to separate inherited changes from local responsibility and to explain why the upgrade is safe.

## Slide 7: Keep the Data Layer contract observable

Trace one component from rendered markup into browser state. When the Adobe Client Data Layer is enabled, supported Core Components expose standardized data and events. The rendered component identifier and `data-cmp-data-layer` payload provide the bridge to the matching object available through `adobeDataLayer`.

Verify that evidence after proxy customization instead of assuming inheritance preserved it. Keep identifiers, semantics and supported component values intact unless the requirement deliberately extends the contract. Add custom tracking data only when there is a named consumer and a documented need.

## Slide 8: Key takeaways

Use the five bullets as the review checklist. Inspect existing capability and version first. Give the project a stable proxy without copying implementation. Make delegation explicit with `sling:resourceSuperType`. Choose the narrowest extension point and treat version changes as contract changes.

Finally, preserve what users and integrations can observe: markup, accessibility, client behavior and Data Layer evidence. The governing principle is: own the proxy; preserve the contract.

## Slide 9: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce prompts, a review activity, practice or an assignment.
