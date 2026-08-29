# Class 17 · Sling Models: adaptables, injection, delegation and JSON

**Date:** Tuesday, September 8, 2026  
**Audience:** frontend-oriented developers beginning AEM backend work  
**Duration:** 30 minutes online  
**Deck goal:** teach developers to turn AEM resource context into a small, explicit view contract for HTL, extend Core Component behavior through delegation and recognize when that same contract can be exposed through Model Exporter.  
**Scope boundary:** build on Class 16 Java, OSGi and Resource API foundations without teaching OSGi configuration, servlet implementation or JUnit yet.  
**Required source images:** none; adaptable choice, injection, delegation and export flow will use technical diagrams.  
**Output:** PNG/HTML slides and detailed speaker notes only; no PPTX.

## Slide 1 — Sling Models: adaptables, injection, delegation and JSON

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 17 · Week 4 · Day 17 · September 8, 2026.
- Sling Models: adaptables, injection, delegation and JSON.
- Today: adaptable choice, injection contracts and Core Component delegation.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for adaptable choice, injection contracts and Core Component delegation.

## Slide 2 — A Sling Model turns AEM context into a view contract.

**Role:** end-to-end mental model  
**Intent:** establish what a Sling Model is responsible for before introducing annotations.

- A Sling Model is a Java object created by adapting supported AEM or Sling context.
- The Models Adapter Factory coordinates model creation and injector resolution.
- The model prepares values and state that a view can consume directly.
- HTL reads the model contract to render server-side markup.
- An eligible model may also expose that contract through a registered exporter.

**Visual idea:** adaptable → Models Adapter Factory + injectors → typed getters → HTL, with a conditional branch to JSON.

## Slide 3 — The adaptable defines the context a model can use.

**Role:** adaptable decision  
**Intent:** teach developers to choose the narrowest context that supplies the model's real inputs.

- A Resource adaptable supplies properties, children, resource type and resource-based injection.
- A request adaptable adds request-specific context such as bindings, attributes and request objects.
- Prefer Resource when the model only needs content; it can be reused inside and outside a request.
- Choose a request only when request-specific context is part of the requirement.
- An annotation that needs unavailable context cannot inject its value successfully.

**Visual idea:** a decision fork: “content only?” routes to Resource; “request context required?” routes to request, with the extra context shown explicitly.

## Slide 4 — Model creation is a runtime contract.

**Role:** registration and adaptation  
**Intent:** show that a compiled class is not automatically discoverable or adaptable as a Sling Model.

- `@Model` declares supported adaptables and, when needed, the component resource type.
- Build tooling registers model packages in bundle metadata for runtime discovery.
- The actual adaptable must match one declared by the model.
- Required injections must resolve before model creation succeeds.
- `adaptTo(...)` may return `null`; `ModelFactory` can provide a more explicit creation failure during diagnosis.

**Visual idea:** four gates—package registration, adaptable match, resource type and required injection—before a model instance becomes available.

## Slide 5 — Injection should name its source and optionality.

**Role:** injection contract  
**Intent:** make model inputs readable and prevent silent ambiguity about where values come from.

- Prefer source-specific annotations such as `@ValueMapValue`, `@ChildResource`, `@OSGiService`, `@Self` and request-only `@ScriptVariable`.
- Source-specific annotations communicate the dependency better than generic `@Inject`.
- Injection is required by default unless the model or field explicitly says otherwise.
- Use `Optional<T>` when absence is legitimate and useful to callers.
- Do not make every field optional; missing required data should remain visible as a broken contract.

**Visual idea:** labeled injector ports enter a model; required ports use solid connectors and legitimate optional ports use dashed connectors.

## Slide 6 — Fallbacks and derived values belong in the model.

**Role:** data preparation  
**Intent:** move repository-specific decisions out of HTL while keeping model behavior small and predictable.

- Read configured content first, then a deliberate legacy property if compatibility requires it.
- Apply one safe fallback only when the view can render a meaningful result.
- Normalize and derive presentation-ready values once instead of repeating logic in HTL.
- Expose explicit state such as `isEmpty()` when the view must decide whether markup exists.
- Keep getters deterministic and free of hidden queries or expensive repeated work.

**Visual idea:** a priority chain—configured → legacy → safe fallback—feeds prepared getters and an explicit empty-state signal.

## Slide 7 — The model owns data preparation; HTL owns markup.

**Role:** view boundary  
**Intent:** define a stable contract that keeps templates readable without turning the model into a rendering engine.

- Model getters expose typed, presentation-ready values and explicit state.
- HTL selects elements, attributes and conditional markup from those values.
- Repository traversal, fallback precedence and formatting rules stay out of the template.
- HTML escaping remains contextual and automatic unless the output contract requires otherwise.
- A small view contract makes rendered behavior easier to inspect and test later.

**Visual idea:** a clean seam: Resource details remain on the Java side; values and state cross the contract; semantic HTML remains on the HTL side.

## Slide 8 — Delegate Core Component behavior instead of copying it.

**Role:** safe extension pattern  
**Intent:** show how a project component can add behavior while preserving the Core Component implementation path.

- Start from a project proxy component whose resource supertype references the Core Component.
- Inject the public Core Component model contract with `@Self` and `@Via(ResourceSuperType.class)`.
- Add or override only the behavior owned by the project requirement.
- Delegate the remaining contract so upstream behavior and fixes remain available.
- Avoid copying private Core Component implementation classes or markup into the project.

**Visual idea:** a project model wraps a delegated Core Component model; one highlighted getter is project-owned while the rest pass through.

## Slide 9 — The model coordinates the view; services own reusable work.

**Role:** responsibility boundary  
**Intent:** prevent both oversized models and speculative service layers.

- Keep component-specific value preparation and view state in the Sling Model.
- Put reusable queries, integrations or multi-step orchestration behind an OSGi service.
- Inject a real service dependency with `@OSGiService` when the model needs that capability.
- Do not create a service that merely forwards one property or getter.
- Service configuration and lifecycle are the focus of Class 18.

**Visual idea:** a model sits at the view boundary; a service sits behind it only for shared or external work, with a clear ownership label on each side.

## Slide 10 — Model Exporter can expose an existing model contract.

**Role:** exported representation  
**Intent:** explain `.model.json` without implying that every Sling Model automatically has a JSON endpoint.

- An exporter-enabled model declares an exporter and an applicable resource type.
- A request such as `/content/example.model.json` resolves the resource and its component type.
- Sling adapts the resource or request to the eligible model.
- The exporter serializes the exposed model contract, commonly through Jackson.
- Inspect the existing exported contract before creating a custom servlet or a second data model.

**Visual idea:** `.model.json` request → resource type → generated exporter servlet → Sling Model → Jackson → JSON response, with an eligibility gate before the flow.

## Slide 11 — Key takeaways

**Role:** summary  
**Intent:** consolidate the decisions developers should carry into implementation and the following backend sessions.

- Choose the narrowest adaptable that supplies the context the model actually needs.
- Use source-specific injection annotations and make optionality deliberate.
- Keep fallback and derived-value logic in a small model contract, not in HTL.
- Delegate public Core Component behavior instead of copying implementations.
- Use a service only for genuinely reusable work; use Model Exporter only when the model is an eligible JSON contract.

**Visual idea:** five contract checkpoints connect adaptable, injection, view model, delegation and export; close with “MAKE THE CONTRACT EXPLICIT.”

## Slide 12 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close without adding another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** quiet closing composition using the resource → model → HTML/JSON motif and generous open space.

## Session use

- **Retrieval:** When should a Sling Model adapt from a Resource instead of a request?
- **Demo:** implement a Guide Card model that prepares a calculated label with configured, legacy and safe fallback paths; render it in HTL and inspect its eligible `.model.json` contract.
- **Assignment:** connect a Sling Model to Guide Card HTL, add one derived value and compare the rendered HTML with the exported model representation.
- **Acceptance:** configured, missing and legacy content render without exceptions; adaptable and injection choices are explainable; delegated behavior is not copied; the exported contract is inspected rather than assumed.

## Source anchors

- [Apache Sling Models](https://sling.apache.org/documentation/bundles/models.html)
- [Customizing Core Components — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/customizing)
- [Core Components Guidelines — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-core-components/using/developing/guidelines)
- [Understand Sling Model Exporter — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-sling-model-exporter)
- [Develop Sling Model Exporter — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/develop-sling-model-exporter)
- Course sequence in `AEM-COURSE-TOPICS.md`, `reference/eight-week-syllabus.html` and `reference/slide-ready-lessons.html`.
