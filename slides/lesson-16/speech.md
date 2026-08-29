# Class 16 · Detailed speaker notes

## How to use these notes

- Keep one Guide Card resource as the thread from repository content to Java source and runtime evidence.
- Define each OSGi term before showing its console state; do not use bundle, component and service interchangeably.
- Treat compilation, bundle resolution and component activation as separate checkpoints.
- Introduce only the Resource API concepts needed before Class 17; leave injection and Model Exporter for that session.
- Use the final slide only for questions raised by the audience.

## Slide 1: Java, OSGi and Resource API foundations in AEM

Introduce Class 16, the 30-minute scope and the session’s three threads: the `core` module, the OSGi runtime and the Resource API.

Keep the opening at overview level. The next slide begins the detailed source-to-runtime trace.

## Slide 2: Java crosses several boundaries before AEM can use it

Read this pipeline from left to right. A `.java` file in `core` first passes the compiler and becomes bytecode. Packaging then adds the OSGi metadata that turns an ordinary JAR into a managed module. When AEM receives that bundle, Apache Felix must resolve every required package against a compatible provider. Only then can Declarative Services evaluate component descriptors and bind required references.

Each stage has different evidence. Source and compiler output prove syntax and type compatibility. `MANIFEST.MF` proves declared runtime contracts. Bundle state and package wiring prove Felix can load the module. Component state proves the container could create a specific managed object. Finally, a Resource path and properties prove what content entered the application behavior.

The important diagnostic habit is to stop saying “the Java works” as one undifferentiated claim. We should be able to say which checkpoint works and which one does not. The next slide opens the artifact that connects compilation to the AEM runtime: the OSGi bundle.

## Slide 3: An OSGi bundle is a managed JAR

The bundle contains familiar Java classes, but its manifest changes how the runtime treats them. `Bundle-SymbolicName` gives the module a stable identity, and `Bundle-Version` participates in compatibility. `Import-Package` lists packages this bundle expects another bundle to provide. `Export-Package` lists packages that this bundle intentionally makes available to others.

The right-side comparison explains a common surprise. Maven can compile because a dependency is present on the build classpath, while Felix still marks the deployed bundle as unresolved because the corresponding package is unavailable at runtime or its version range does not match. Rebuilding the same JAR does not repair that contract. We inspect the unresolved import and its expected provider.

Exporting everything is not a solution. Implementation packages should remain private unless another bundle has a real reason to compile against a supported contract. A narrow export surface reduces accidental coupling. With the module boundary established, we can now separate it from the managed objects and capabilities that live inside it.

## Slide 4: Bundle, component and service are different runtime objects

This distinction is the vocabulary foundation for the rest of the week. The bundle on the left is the deployable module and class-loading boundary. It can contain ordinary Java classes, component descriptors and other resources. Installing one bundle does not mean every class inside it becomes a managed object.

The center panel is a component. Declarative Services creates it and owns its lifecycle because the class was declared with `@Component`. The component may perform internal work without publishing anything. If it exposes a capability to other managed consumers, that capability appears in the service registry as shown on the right. Consumers bind to the service contract rather than constructing the provider directly.

The relationship rail is worth stating precisely: one bundle may contain many components, and one component may publish zero, one or several services. When debugging, ask whether the failure concerns module resolution, component activation or service availability. Those questions lead to different evidence. Next we look at the gate that determines whether a component can activate.

## Slide 5: Declarative Services activates only satisfied components

Here `@Component` tells Declarative Services that `GuideCatalog` is container-managed. The `@Reference` does not mean “create a new repository object.” It declares that this component requires a service matching the `GuideRepository` contract. While that reference is unavailable, the component remains unsatisfied. When a matching service is registered, the container can bind it and activate the component.

This is why request code should not manually call `new GuideCatalog()` for a container-managed class. Manual construction bypasses reference binding, lifecycle callbacks and service registration. The container owns activation and deactivation, and the component should perform only the setup and cleanup appropriate to that lifecycle.

Keep activation fast. It is not the place for a large repository scan or a remote synchronization. Also avoid treating component fields as durable business storage. AEM instances restart and scale, so instance memory cannot be the system of record. Configuration will receive its own treatment in Class 18; for now, remember only that a required input can block activation just like a missing service reference.

## Slide 6: Runtime state tells you which boundary failed

The top rail shows bundle evidence. `Installed` commonly means Felix could not resolve one or more required packages. `Resolved` means the package wiring is available, although the bundle is not active. `Active` confirms the bundle lifecycle, but it does not certify every component descriptor inside the bundle.

That is why the component rail is separate. An unsatisfied component points us toward missing service references or required configuration. An active component tells us that Declarative Services created that managed object with its mandatory inputs. This separation prevents a common loop where developers repeatedly reinstall an active bundle even though the actual problem is one unsatisfied component.

Locally, the AEM SDK Web Console exposes bundles, components, services and configuration for development inspection. In AEM as a Cloud Service environments, use Developer Console for read-only runtime evidence. Production code and configuration are deployed through the delivery pipeline rather than changed ad hoc in the running environment. We have now traced Java into the container; next we connect it to content.

## Slide 7: The Resource API is the default content boundary

The central object is one Guide Card `Resource`. Its path identifies its location in the Sling resource tree, and its resource type tells Sling which application behavior is associated with it. The Resource API also provides the name, properties and child resources without forcing ordinary component code to work directly with a JCR `Node`.

Use `getValueMap()` for typed property access. The example `valueMap.get("title", "Untitled guide")` makes both the requested type and fallback visible in application code. Use `getChild("items")` when the content contract defines a known child structure. Use `adaptTo(...)` when a supported higher-level abstraction is appropriate; adaptation is a contract and can return no result, so callers must handle that possibility.

The goal is not to hide that AEM stores content in a JCR. The goal is to start at the abstraction that matches resource-based application work and drop to lower-level repository APIs only for a specific reason. That decision becomes clearer on the API ladder.

## Slide 8: Choose the highest useful API

Start at the top of the ladder. If AEM provides a product abstraction such as `Page` or `PageManager` that directly models the requirement, use it. Otherwise Sling’s `Resource`, `ValueMap` and request abstractions are the normal choice for component-oriented work. JCR `Session` and `Node` belong to requirements that are genuinely repository-specific. OSGi APIs belong to container concerns such as component declaration, service registration and lifecycle.

This order is a preference, not a ban. The responsible choice is the highest layer that expresses the requirement without awkward workarounds. What we should avoid is broad, habitual use of lower-level APIs because they happen to expose everything.

The bottom strip covers an important trust boundary. Administrative repository access is not acceptable. Background work uses a scoped service user with the minimum permissions required, obtains a `ResourceResolver`, and closes a resolver it owns—preferably with try-with-resources. Request-provided resolvers follow request ownership and are not closed by application code. The final technical slide combines these choices into one trace.

## Slide 9: Trace one capability from content to runtime

Begin in the repository inspector and record the Guide Card path and resource type. Move to the IDE and locate the Java consumer in `core`. Identify exactly which Resource API calls read the content instead of assuming that every property on the resource matters.

Then open the bundle evidence. The symbolic name tells us which deployed module contains the class, and package wiring explains whether its runtime dependencies resolved. The component inspector shows whether Declarative Services recognized the descriptor, satisfied its references and activated the managed object. The console state is not a substitute for source or repository inspection; it is another link in the same evidence chain.

The complete explanation should sound like this: this content resource enters this Java boundary, that class is packaged in this bundle, this component or service is active with these required references, and these artifacts prove the result. “The build passed” explains only the second stage. This trace is the foundation we will reuse when Sling Models become the view-facing Java contract in Class 17.

## Slide 10: Key takeaways

Use the five checkpoints as the review path for any new AEM Java class. First, locate the source and the bundle that packages it. Second, name its runtime role correctly: ordinary class, Declarative Services component or published service. Third, verify who owns lifecycle and reference binding instead of constructing managed objects manually.

Fourth, inspect runtime evidence before editing or redeploying. Bundle state and component state answer different questions. Finally, start content access with the highest useful AEM or Sling abstraction; for ordinary component content, that normally means `Resource` and `ValueMap` rather than direct JCR access.

The governing habit is the same one used in the frontend sessions: trace the runtime, do not guess. A precise trace identifies the responsible boundary and makes the next correction smaller and safer.

## Slide 11: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce prompts, a review exercise, practice instructions or another backend concept on this closing slide.
