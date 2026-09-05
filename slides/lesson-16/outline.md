# Class 16 · Java, OSGi and Resource API foundations in AEM

**Guía de preparación en español:** [Abrir en el navegador](../../reference/session-16-study-guide.html) · [Resumen en Markdown](../../reference/session-16-study-guide.md).

**Date:** Monday, September 7, 2026  
**Audience:** frontend-oriented developers beginning AEM backend work  
**Duration:** 30 minutes online  
**Deck goal:** give developers a usable mental model for tracing Java source from the `core` module into an active AEM runtime capability, then show how that code should read content through the Resource API.  
**Scope boundary:** introduce the runtime vocabulary required for Class 17 without teaching Sling Model injection, Model Exporter, OSGi configuration, servlet implementation or JUnit yet.  
**Required source images:** none; project structure, bundle metadata, runtime states and repository objects will use technical diagrams.  
**Output:** PNG/HTML slides and detailed speaker notes only; no PPTX.

## Slide 1 — Java, OSGi and Resource API foundations in AEM

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 16 · Week 4 · Day 16 · September 7, 2026.
- Java, OSGi and Resource API foundations in AEM.
- Today: the core module, the OSGi runtime and the Resource API.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact visual anchors for the core module, the OSGi runtime and the Resource API.

## Slide 2 — Java crosses several boundaries before AEM can use it.

**Role:** end-to-end mental model  
**Intent:** prevent “the class compiled” from being treated as proof that AEM can execute it.

- Java source lives in the Maven `core` module.
- Compilation produces bytecode; bundle packaging adds OSGi metadata.
- AEM installs the bundle into Apache Felix and resolves its package dependencies.
- Declarative Services creates eligible components and binds required references.
- Application code then consumes AEM or Sling objects such as a `Resource`.

**Visual idea:** Source → Compile → Bundle JAR → Felix resolution → DS component → Resource-backed behavior, with one evidence artifact below each stage.

## Slide 3 — An OSGi bundle is a managed JAR.

**Role:** packaging anatomy  
**Intent:** distinguish a normal JAR from a module whose runtime contracts are enforced by OSGi.

- The bundle manifest gives the JAR a symbolic name, version and lifecycle identity.
- `Import-Package` declares Java packages the bundle needs at runtime.
- `Export-Package` publishes only packages intended for other bundles.
- Maven compilation can succeed while Felix still cannot resolve an unavailable or incompatible import.
- Keep implementation packages private unless another bundle has a real contract to consume.

**Visual idea:** open one `core` bundle as a cutaway: classes and resources inside, manifest headers outside, required package providers connected at runtime.

## Slide 4 — Bundle, component and service are different runtime objects.

**Role:** vocabulary comparison  
**Intent:** establish the three concepts developers must keep separate when diagnosing backend behavior.

- A bundle is the deployable module and class-loading boundary.
- A component is an object whose creation and lifecycle are managed by Declarative Services.
- A service is a capability a component may register for consumers.
- One bundle can contain many components; a component may publish zero, one or several service contracts.
- A plain Java class inside a bundle is not automatically an OSGi component or service.

**Visual idea:** nested but non-equivalent layers: bundle contains classes and component descriptors; a managed component may publish a service into the registry.

## Slide 5 — Declarative Services activates only satisfied components.

**Role:** lifecycle and dependency flow  
**Intent:** explain why application code should declare runtime collaboration instead of manually constructing container-managed objects.

- `@Component` declares a class for OSGi Declarative Services.
- `@Reference` expresses a dependency on a service contract.
- Required references and configuration must be satisfied before activation.
- Activation and deactivation belong to the container lifecycle, not request code.
- Keep activation fast and avoid storing durable business state in the component instance.

**Visual idea:** a component descriptor waits at a gate until service references are satisfied, then moves through activate → available → deactivate.

## Slide 6 — Runtime state tells you which boundary failed.

**Role:** diagnostic matrix  
**Intent:** turn bundle and component states into evidence-driven troubleshooting.

- `Installed` commonly points to unresolved package requirements.
- `Resolved` means the bundle’s wiring is available but the bundle is not active.
- `Active` confirms bundle lifecycle, not that every contained component is satisfied.
- An unsatisfied component points to a missing reference or required configuration.
- Inspect the local SDK Web Console; use the read-only Developer Console for cloud runtime evidence.

**Visual idea:** symptom → evidence → likely owner matrix, with separate Bundle and Component state rails plus Local SDK and Cloud inspection points.

## Slide 7 — The Resource API is the default content boundary.

**Role:** content abstraction anatomy  
**Intent:** connect Java runtime foundations to the object frontend-oriented developers will use in the next session.

- A `Resource` represents an addressable item in Sling’s resource tree.
- It exposes path, name, resource type, properties and children without requiring direct JCR `Node` use.
- `ValueMap` provides typed property access with explicit defaults.
- Child navigation keeps code aligned with known content structure.
- `adaptTo(...)` bridges to supported higher-level abstractions when the contract requires one.

**Visual idea:** one Guide Card resource with path, `sling:resourceType`, `ValueMap`, child resources and an adaptation port.

## Slide 8 — Choose the highest useful API.

**Role:** API decision ladder  
**Intent:** avoid coupling ordinary component code to lower-level repository or container APIs.

- Prefer an AEM product abstraction when it directly models the requirement.
- Otherwise prefer Sling resources and requests for resource-based application work.
- Use JCR APIs only for genuinely JCR-specific capabilities.
- Use OSGi APIs for container concerns such as components, services and lifecycle.
- Never use administrative repository access; background work requires a scoped service user and a properly closed resolver.

**Visual idea:** decision ladder AEM → Sling → JCR → OSGi, with examples and an explicit “use the highest layer that expresses the requirement” rule.

## Slide 9 — Trace one capability from content to runtime.

**Role:** integrated case study  
**Intent:** combine the session into one evidence path that can be repeated in the WKND project.

- Start with a Guide Card content resource and record its path and resource type.
- Locate the Java consumer in `core` and identify the Resource API values it reads.
- Find the bundle symbolic name and verify its package wiring and state.
- Identify any DS component descriptor, service contract and required references.
- Explain the behavior using repository, source, bundle and component evidence—not a successful build alone.

**Visual idea:** synchronized repository, IDE, bundle manifest and runtime console inspectors connected by one numbered evidence trace.

## Slide 10 — Key takeaways

**Role:** summary  
**Intent:** consolidate the minimum backend vocabulary and diagnostic habits needed for subsequent sessions.

- `core` source becomes usable only after compilation, bundle resolution and component activation.
- Bundle, component and service describe different runtime responsibilities.
- Declarative Services owns lifecycle and reference binding.
- Runtime state narrows the failing boundary before code is changed or redeployed.
- Prefer AEM and Sling abstractions; use the Resource API for ordinary content access.

**Visual idea:** five checkpoints connect source, bundle, component, diagnostics and resource access; close with “TRACE THE RUNTIME, DO NOT GUESS.”

## Slide 11 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close without adding another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** quiet closing composition using the source → bundle → resource motif and generous open space.

## Session use

- **Retrieval:** What must happen after Java compilation before a class becomes an active AEM capability?
- **Demo:** trace one WKND content resource to the Java class that reads it, the `core` bundle that contains the class and the runtime state that proves availability.
- **Assignment:** map three project Java classes to their bundle, Resource API inputs and OSGi role; label plain class, managed component and published service correctly.
- **Acceptance:** each map identifies the resource boundary, source class, bundle identity, component or service role and runtime evidence without confusing build success with activation.

## Source anchors

- [AEM API Reference Materials — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/reference-materials)
- [Java API Best Practices in AEM — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/foundation/development/understand-java-api-best-practices)
- [AEM as a Cloud Service Web Console — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developer-tools/web-console)
- [AEM as a Cloud Service Developer Console — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/debugging/debugging-aem-as-a-cloud-service/developer-console)
- [JCR Integration Best Practices — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-65-lts/content/implementing/developing/bestpractices/jcr-integration)
- Course sequence in `AEM-COURSE-TOPICS.md`, `reference/eight-week-syllabus.html` and `reference/slide-ready-lessons.html`.
