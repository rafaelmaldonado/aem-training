# Class 17 · Sling Models: adaptables, injection, delegation and JSON

## Slide 1: Sling Models: adaptables, injection, delegation and JSON

Today we connect the Resource API from the previous class to the objects HTL actually consumes. The path on the slide starts with component content, passes through a Sling Model, and ends in rendered HTML. A second branch shows JSON, but that branch is deliberately conditional: a model must participate in an exporter contract before `.model.json` exists.

The goal is not to memorize annotations. By the end of the session, we should be able to explain why a model adapts from a Resource or a request, where every injected value comes from, what logic belongs in the model, and when delegation or Model Exporter prevents us from duplicating an existing implementation. We will begin with the role of the model itself.

## Slide 2: A Sling Model turns AEM context into a view contract.

Read this flow from left to right. The adaptable is the runtime object we already have—usually a Resource or a request. The Models Adapter Factory finds a compatible model definition and asks registered injectors to resolve the model’s declared inputs. If those runtime contracts are satisfied, it creates the Java object that HTL can use.

The important output is not “a class with annotations.” It is a typed view contract: values such as a display title, a link and an explicit empty state that the template can consume without understanding repository storage. This is why Sling Models are useful at the Java-to-HTL seam.

Also keep the identity strip in mind. A Sling Model is an adapted view object; it is not an OSGi service by default. It can consume a service, and an eligible model can be exported, but those are separate capabilities. Next we choose the context from which that object should adapt.

## Slide 3: The adaptable defines the context a model can use.

Start with the question in the center: what context does this model genuinely need? If the answer is properties, child resources and resource type, use a Resource adaptable. That choice makes the model useful in more places because it does not depend on an active HTTP request.

A request adaptable is justified when the requirement includes request-specific information: Sling bindings, request attributes or objects tied to the current request. `@ScriptVariable`, for example, depends on Sling bindings and belongs on this branch. A request may still expose resource-backed values, but that does not mean every component model should require one.

The narrowest adaptable is usually the clearest contract. It limits the available context to what the model actually uses, improves reuse, and makes failures easier to explain. After choosing the adaptable, the runtime still needs to discover and construct the model correctly.

## Slide 4: Model creation is a runtime contract.

Compilation is only the starting point. `@Model` declares which adaptable the class supports and may associate the model with a component resource type. The bundle build must also register the model package so the Models Adapter Factory can discover it at runtime. A valid Java class that is missing this registration is still not an available Sling Model.

Then follow the four gates. The runtime object must match a declared adaptable. A declared resource type must apply to the resource being adapted. Every required injection must resolve. Only after these checks can Sling return a model instance.

The diagnostic rail explains a common source of confusion. `adaptTo(...)` follows the Sling Adapter contract and may return `null`, so it proves that creation failed but does not necessarily explain why. `ModelFactory#createModel(...)` can surface a more explicit exception when we need evidence about the failing gate. That brings us to the model inputs most likely to open or close the final gate.

## Slide 5: Injection should name its source and optionality.

Each port around the model names a different source. `@ValueMapValue` reads a property, `@ChildResource` adapts a child, `@OSGiService` requests a registered service, `@Self` uses the current adaptable or a model derived from it, and `@ScriptVariable` reads a Sling binding from request context. Source-specific annotations make the dependency visible to the next developer and reduce injector ambiguity.

The solid connectors matter: injection is required by default. If a value is essential to a valid model, leaving it required makes a missing dependency fail at model creation instead of producing a partially initialized object. That failure is useful evidence.

Use `Optional<T>` when absence is a legitimate state that callers need to handle. It communicates optionality in the Java type and still allows Sling to attempt injection. Avoid making the entire model optional merely to prevent failures; optional everywhere can hide a broken dialog, wrong property name or incompatible adaptable. Once the inputs are explicit, the model can prepare a stable result.

## Slide 6: Fallbacks and derived values belong in the model.

This Guide Card uses a deliberate precedence chain. We first read the current `title` property. If the component must support older content, we then check the documented legacy property `heading`. Only when neither contains a meaningful value do we apply the safe fallback `Untitled guide`. The order is part of the component contract, not a template convenience.

The model also normalizes the chosen value once and exposes `getDisplayTitle()`. If the component can become non-renderable, it exposes that state through `isEmpty()` rather than forcing HTL to reconstruct the decision from several raw fields. HTL receives prepared values and state, not repository compatibility rules.

Keep getters predictable. A getter should not hide a new query or repeat expensive integration work each time HTL accesses it. Calculate stable derived values once during model initialization when appropriate. The next slide draws the ownership boundary around that principle.

## Slide 7: The model owns data preparation; HTL owns markup.

On the Java side, the model owns Resource and ValueMap access, fallback precedence, normalization, derived values and explicit state. Only the small contract in the center crosses into the template: here that means `displayTitle`, `link` and `empty`. This keeps repository details from leaking into markup.

On the HTL side, the template owns semantic elements, attributes and conditional rendering. `data-sly-test` can decide whether an `<article>` or `<h2>` is emitted, but it should not walk deep repository structures or repeat a legacy-property decision. Contextual escaping also remains part of normal HTL output behavior; bypassing it is not a substitute for preparing the right value.

The reverse boundary matters too. Java should not construct HTML strings that the template then injects. When each side owns the correct concern, the contract remains readable, the markup remains accessible, and later tests can validate behavior without duplicating rules. We can apply the same ownership thinking when extending an existing Core Component.

## Slide 8: Delegate Core Component behavior instead of copying it.

Begin on the left with the proxy component. Its `sling:resourceSuperType` points to the versioned Core Component, so the project participates in the supported inheritance path instead of copying the Core Component into `/apps`. That preserves access to upstream implementation fixes.

In the center, the project model injects the public `Title` contract with `@Self` and `@Via(type = ResourceSuperType.class)`. The `ResourceSuperType` strategy asks Sling for the model associated with the inherited component behavior. The project now has an object to which unchanged methods can be delegated.

The project owns only its additional requirement, represented here by `getEyebrowText()`. Existing contract members such as `getText()`, `getType()` and `getLink()` continue through the delegate. In real code, a delegation helper may reduce boilerplate, but the design rule remains the same: override only the behavior the project owns and preserve the public contract for everything else.

Copying a private implementation creates a fork that drifts during upgrades. Delegation keeps the customization narrow and makes ownership visible. A similar ownership question tells us when work should move out of the model entirely.

## Slide 9: The model coordinates the view; services own reusable work.

Use the spectrum rather than a rule that every model needs a service. Component-specific fallback, formatting and empty-state decisions belong naturally in the Sling Model because they prepare one view contract. Moving each of those operations behind a service adds ceremony without creating reuse.

The service boundary becomes useful when the work is shared or external: a reusable query, an integration, or multi-step orchestration used by several models or other consumers. The model can declare that real dependency with `@OSGiService` and remain focused on adapting the service result for its view.

The crossed-out pass-through service is the warning. A service whose only method forwards one property does not create a useful boundary. We will examine service lifecycle and environment-specific configuration in Class 18; for now, the decision is simply whether a reusable capability actually exists.

## Slide 10: Model Exporter can expose an existing model contract.

Follow the request from left to right. The `.model.json` URL first resolves an AEM Resource and its `sling:resourceType`. An eligible Sling Model declares an exporter for that component type, and the Model Exporter integration registers the servlet behavior associated with the `model` selector and `json` extension.

When that eligibility gate is satisfied, Sling adapts the resource or request to the model. The configured exporter—commonly Jackson—serializes the exposed model contract into the JSON response. This is reuse of an existing model contract, not a separate endpoint implementation for the same component data.

Two cautions matter. Not every Sling Model has `.model.json`; the exporter and resource-type contract must exist. Also, exported getters form an API surface, so inspect the actual JSON shape, names and optional values instead of assuming it matches the rendered HTML. Before writing a custom servlet, check whether the existing exporter already provides the required representation. Custom servlet boundaries belong in the next class.

## Slide 11: Key takeaways

The center of this recap is the view contract. First, choose the narrowest adaptable that provides the required context. Second, name each injection source and make absence deliberate rather than globally optional. Third, keep repository fallback and value preparation on the model side of the HTL boundary.

Fourth, delegate the public Core Component contract when the project changes only part of existing behavior. Fifth, introduce a service or exporter only when there is a genuine reusable or external contract. None of these mechanisms is valuable merely because an annotation is available.

The practical test is whether another developer can read the model and explain its inputs, fallbacks, outputs and ownership boundaries. Make the contract explicit, then use runtime evidence when creation or output does not match that contract.

## Slide 12: Questions

Thank you. I will leave this slide open for questions from the group. I will not introduce another prompt or exercise here; the session ends with the questions participants want to raise about Sling Models, delegation or exported contracts.
