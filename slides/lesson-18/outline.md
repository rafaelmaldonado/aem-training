# Class 18 · OSGi services, configuration and servlet boundaries

**Date:** Wednesday, September 9, 2026  
**Audience:** frontend-oriented developers beginning AEM backend work  
**Duration:** 30 minutes online  
**Deck goal:** teach developers to introduce one reusable OSGi capability, configure it safely for AEM as a Cloud Service and choose the smallest delivery surface that serves a real consumer.  
**Scope boundary:** build on Class 17 Sling Models and Model Exporter without teaching JUnit, AEM Mocks, custom authentication schemes or Cloud Manager operations.  
**Required source images:** none; service lifecycle, configuration resolution and request boundaries will use technical diagrams.  
**Output:** PNG/HTML slides and detailed speaker notes only; no PPTX.

## Slide 1 — OSGi services, configuration and servlet boundaries

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 18 · Week 4 · Day 18 · September 9, 2026.
- OSGi services, configuration and servlet boundaries.
- Today: reusable services, typed configuration and endpoint decisions.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for reusable services, typed configuration and endpoint decisions.

## Slide 2 — Create a service only for a reusable capability.

**Role:** responsibility boundary  
**Intent:** prevent speculative service layers while giving shared or external work one explicit owner.

- Start with a real consumer and one named capability.
- Use a service for reusable queries, integrations or multi-step orchestration.
- Keep component-specific presentation logic in the Sling Model.
- Define a small interface when multiple consumers need the same capability.
- Do not create a service that only forwards one getter.

**Visual idea:** a decision fork routes view-specific preparation to a Sling Model and shared Guide URL resolution to one OSGi service used by two real consumers.

## Slide 3 — Declarative Services owns the runtime lifecycle.

**Role:** runtime contract  
**Intent:** show how a service implementation becomes available and why consumers should depend on its capability rather than construct it.

- `@Component(service = GuideUrlService.class)` registers the capability.
- The DS runtime creates, activates and deactivates the component.
- `@Reference` declares a real service dependency for another component.
- A required unsatisfied reference prevents activation instead of producing a partial object.
- Runtime component state is stronger evidence than source inspection alone.

**Visual idea:** implementation class → bundle metadata → DS component → service registry → two consumers, with a required-reference gate before activation.

## Slide 4 — Typed configuration documents an operational contract.

**Role:** configuration anatomy  
**Intent:** connect Metatype definitions to a readable, typed service configuration.

- `@ObjectClassDefinition` names the configuration contract.
- Configuration methods declare property names, Java types and defaults.
- `@AttributeDefinition` adds operator-facing names and descriptions when needed.
- `@Designate` connects the component PID to the typed definition.
- Activation receives one typed configuration object instead of parsing loose strings.

**Visual idea:** one annotated configuration interface feeds generated Metatype metadata, a PID and a typed activation object.

## Slide 5 — Effective configuration is selected per PID.

**Role:** run-mode resolution  
**Intent:** explain AEM as a Cloud Service configuration selection without Java environment conditionals.

- Store project OSGi configuration under the project’s code package.
- Use supported `author` or `publish` and `dev`, `stage` or `prod` run modes.
- The configuration with the most matching run modes wins for the entire PID.
- A more specific PID file replaces, rather than merges with, a less specific one.
- AEM as a Cloud Service does not support custom run modes.

**Visual idea:** four candidate configuration folders compete for one PID; matching run modes select one complete effective document.

## Slide 6 — Values vary by environment; secrets stay out of Git.

**Role:** value classification  
**Intent:** separate versioned configuration shape from deploy-time values and credentials.

- Commit stable configuration and placeholder names with the code.
- Use `$[env:GUIDE_BASE_URL]` for non-secret environment-specific values.
- Use `$[secret:GUIDE_API_TOKEN]` for secret values.
- Never commit, log or capture the resolved secret in screenshots.
- Do not use environment variables to override Adobe-owned OSGi configuration.

**Visual idea:** a versioned JSON configuration accepts two deploy-time inputs through distinct ENV and SECRET channels; only the resolved service receives both.

## Slide 7 — Missing configuration must fail safely and visibly.

**Role:** safe activation decision  
**Intent:** avoid insecure fallbacks and silent partial behavior when required configuration is absent or invalid.

- Classify each property as required, optional with a safe default or capability-enabling.
- Validate URLs, ranges and allowed values at activation.
- Reject activation when continuing would expose data or corrupt behavior.
- Otherwise disable the capability and emit a useful diagnostic without secret values.
- Keep the previous valid runtime contract until a valid replacement is available.

**Visual idea:** validation gate routes valid configuration to ACTIVE, optional absence to DISABLED WITH DIAGNOSTIC and unsafe input to ACTIVATION REJECTED.

## Slide 8 — Verify the effective runtime value, not only the file.

**Role:** operational evidence  
**Intent:** teach developers to prove which configuration and component state the runtime actually applied.

- Locally, inspect Components and Configuration in the AEM SDK Web Console.
- In cloud environments, use the Developer Console status dumps.
- Match the component or configuration PID before comparing properties.
- Confirm Author and Publish independently when their values differ.
- Redact secret values from evidence and troubleshooting notes.

**Visual idea:** source configuration and runtime status converge in an evidence checklist: PID, tier, component state and non-secret effective values.

## Slide 9 — Choose the minimum delivery surface for the consumer.

**Role:** surface decision ladder  
**Intent:** make “no new servlet” the default unless the requirement needs a separate HTTP contract.

- Use HTL when the browser needs server-rendered component markup.
- Use a Sling Model when HTL needs prepared values and state.
- Reuse an existing Core Component or Model Exporter contract when it already fits.
- Add a servlet only for a distinct HTTP consumer and response contract.
- Every new endpoint adds validation, authorization, caching and compatibility work.

**Visual idea:** a descending decision ladder stops at HTL, Sling Model, existing exporter or, only after three failed gates, a servlet.

## Slide 10 — If a servlet is required, bind and constrain it explicitly.

**Role:** request boundary  
**Intent:** define the smallest safe servlet registration and the evidence needed to operate it.

- Prefer resource-type registration over path binding.
- Declare the exact methods, selectors and extensions the consumer needs.
- Use a safe-method base class for read-only requests.
- Validate inputs, set an explicit content type and return deliberate status codes.
- Verify permissions, cache behavior and the resolved servlet for the exact request.

**Visual idea:** request decomposition—resource path, selector, extension and method—passes through registration and security gates before reaching one resource-type servlet.

## Slide 11 — Key takeaways

**Role:** summary  
**Intent:** consolidate the ownership, configuration and delivery decisions developers should carry into implementation.

- Introduce a service only for one reusable capability with a real consumer.
- Let Declarative Services own lifecycle and required dependencies.
- Treat typed configuration as an operational contract selected per PID.
- Separate versioned shape, environment values and secrets; fail safely when invalid.
- Prefer an existing rendering or export surface before creating a constrained servlet.

**Visual idea:** five checkpoints connect consumer, service, typed configuration, effective runtime evidence and minimum delivery surface; close with “ADD ONLY THE BOUNDARY THE CONSUMER NEEDS.”

## Slide 12 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close without adding another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** quiet closing composition using the configured-service path and a closed servlet decision gate with generous open space.

## Session use

- **Retrieval:** Which values may vary by environment without changing application code?
- **Demo:** configure a Guide URL service, inspect its effective local configuration, then compare HTL, `.model.json` and a servlet proposal for the same consumer need.
- **Assignment:** implement one typed Guide URL configuration and document the minimum delivery surface for a named consumer.
- **Acceptance:** the service has one reusable capability; environment values and secrets are classified safely; missing or invalid configuration has deliberate behavior; runtime evidence identifies the effective PID and tier; the endpoint decision names its consumer, contract, validation, permission and cache surface.

## Source anchors

- [Configuring OSGi for AEM as a Cloud Service — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/deploying/configuring-osgi)
- [Environment Variables in Cloud Manager — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/environment-variables)
- [Web Console — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/web-console)
- [Servlets and Scripts — Apache Sling](https://sling.apache.org/documentation/the-sling-engine/servlets.html)
- [OSGi Metatype Service Specification](https://docs.osgi.org/specification/osgi.cmpn/8.1.0/service.metatype.html)
- Course sequence in `reference/aem-course-topics.html`, `reference/eight-week-syllabus.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
