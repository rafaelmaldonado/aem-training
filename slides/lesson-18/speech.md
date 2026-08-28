# Class 18 · OSGi services, configuration and servlet boundaries

## Slide 1: OSGi services, configuration and servlet boundaries

Today we continue from the Sling Model boundary. A model can prepare one component view, but shared behavior needs a different owner. The path on this cover starts with a real consumer, reaches one configured OSGi service and then stops at the smallest delivery surface that satisfies the requirement.

The emphasis is on restraint. We will not create a service merely to add a layer, and we will not create a servlet merely because Java can return JSON. By the end, we should be able to name the reusable capability, explain its effective configuration and justify whether HTL, a Sling Model, an existing exporter or a servlet owns the output.

## Slide 2: Create a service only for a reusable capability.

Begin with the consumer rather than the annotation. If one Guide Card needs a formatted label or an empty-state decision, that is still view preparation and belongs naturally in its Sling Model. Moving that work into a service would add a second abstraction without creating reuse.

The service branch becomes useful when the capability has an identity of its own. A Guide URL policy might normalize external and internal URLs for several models, or an integration might retrieve data used by multiple consumers. In those cases, a small `GuideUrlService` gives the shared behavior one owner and one contract.

The crossed-out pass-through service is the warning. An interface and implementation that only return one property do not protect a meaningful boundary. Name the capability first; introduce the service only when that name describes reusable work.

## Slide 3: Declarative Services owns the runtime lifecycle.

Read the pipeline from left to right. The implementation class is compiled into a bundle, and build tooling generates Declarative Services metadata from `@Component`. When the bundle resolves, the DS runtime can create the component and register its `GuideUrlService` capability in the service registry.

Consumers depend on that capability rather than constructing the implementation. A declared `@Reference` tells DS which service dependency must exist. If a required reference cannot be satisfied, the component remains unsatisfied instead of becoming a partially initialized object that fails later in a request.

This gives us operational evidence. A class in source control proves intent; the Components view proves whether DS discovered it, satisfied its references and activated it. We will apply the same distinction between source intent and effective runtime state to configuration.

## Slide 4: Typed configuration documents an operational contract.

`@ObjectClassDefinition` describes the configuration as a typed contract. Its methods become properties with Java types and optional defaults. `@AttributeDefinition` is useful when operators need a clearer name, description or constrained choice; it is not required on every method merely for decoration.

`@Designate` connects that definition to the Declarative Services component PID. At build time, tooling creates the Metatype metadata that consoles and configuration tooling can understand. At activation, the component receives a typed `GuideUrlConfig` object instead of manually parsing unrelated strings.

Treat this as an operational API. Property names, types, defaults and descriptions affect how another person safely configures the service. Renaming or changing their meaning deserves the same care as changing a Java contract used by another module.

## Slide 5: Effective configuration is selected per PID.

The runtime on this slide is Author plus dev. Four folders contain candidates for the same PID. The base `config` candidate is generally applicable, `config.author` matches one active run mode, `config.author.dev` matches both and `config.publish` does not apply to this runtime.

The most specific matching configuration wins for the entire PID. The runtime does not take one property from `config.author` and another from `config.author.dev`; the selected, more-specific document replaces the less-specific candidate. That is why each environment-specific PID file must be complete for the behavior it configures.

AEM as a Cloud Service supports the defined service and environment run modes—Author or Publish and dev, stage or prod. Custom run modes are not the extension mechanism. Values that genuinely vary between cloud environments belong in environment variables, which is our next boundary.

## Slide 6: Values vary by environment; secrets stay out of Git.

The project should version the stable configuration shape: the PID, normal non-varying values and placeholder names. A non-secret value such as the Guide base URL can use `$[env:GUIDE_BASE_URL]`. A credential or token uses the separate `$[secret:GUIDE_API_TOKEN]` form.

Only the runtime needs the resolved values. Git, logs, screenshots and troubleshooting notes should never contain the secret. Even when the value is hidden correctly, avoid logging the entire configuration object because a future property may become sensitive.

There is also an ownership limit: environment variables are for configuration properties belonging to custom project code, not a mechanism for overriding Adobe-owned OSGi configuration. Version the contract, supply the environment-specific value through the approved channel and keep the resolved secret at the runtime boundary.

## Slide 7: Missing configuration must fail safely and visibly.

Not every missing value has the same meaning. An optional display setting may have a safe default. An `enabled` flag may deliberately disable a capability. A required endpoint or secret may make activation unsafe. Classifying properties before coding prevents one generic fallback from hiding several different states.

Validate the contract when configuration enters the component. For this service, that might mean requiring HTTPS, checking a bounded timeout or allowed value and confirming that a required secret is present without logging it. A valid contract reaches the active state.

If absence is an expected operational state, disable the capability and emit a useful non-secret diagnostic. If continuing would expose data or produce corrupt behavior, reject activation. The important rule is to avoid silent partial behavior: operators should be able to distinguish active, intentionally disabled and invalid configuration.

## Slide 8: Verify the effective runtime value, not only the file.

Source inspection tells us which configuration was intended, but it does not prove which PID and values the runtime selected. In the local SDK, use the Web Console Components and Configuration views to inspect component state, references and effective non-secret properties.

In AEM as a Cloud Service, use Developer Console status dumps for Components and Configurations. Match the exact PID, then note the tier or pod, component state and non-secret effective values. Verify Author and Publish separately when their configuration differs; one successful tier does not prove the other.

Capture only the evidence required to explain the result. Redact secrets rather than trying to prove them with screenshots. A useful record states the PID, target tier, observed state, safe values and the next test if the result is wrong.

## Slide 9: Choose the minimum delivery surface for the consumer.

Walk down this ladder and stop at the first surface that fits. If the browser needs server-rendered component markup, HTL already owns the output. If HTL needs prepared values or state, a Sling Model supplies that contract without creating a separate HTTP endpoint.

Before adding anything new, inspect existing Core Component behavior and any eligible Model Exporter contract. An existing `.model.json` representation may already provide the data shape the consumer needs. Reusing it avoids a second implementation and a second compatibility promise.

A servlet is justified only when a distinct HTTP consumer needs a separate request and response contract. That final rung carries validation, authorization, cache behavior and compatibility responsibilities. This is why the best servlet may be no servlet: absence of a new endpoint can be the correct design outcome.

## Slide 10: If a servlet is required, bind and constrain it explicitly.

This request is decomposed into resource, selector, extension and method. A resource-type servlet participates in Sling resolution for that content type and can declare the exact `guides` selector, `json` extension and `GET` method it supports. This keeps the endpoint connected to the resource model rather than mounting an opaque global path.

Path binding is discouraged because it loses several advantages of resource-based resolution and access control. Whichever registration is used, declare only the methods and request shapes the consumer genuinely needs. A read-only contract should use the safe-method servlet base rather than accepting write methods accidentally.

Selection is only the first gate. Validate request inputs, confirm permissions, define cache behavior, set the response content type and return deliberate status codes. Then verify the exact request resolves to the intended servlet. A servlet is complete only when its operational surface is as explicit as its Java implementation.

## Slide 11: Key takeaways

The center of this recap is the consumer-driven backend contract. First, create a service only for a reusable capability that a real consumer needs. Second, let Declarative Services own component lifecycle and required dependencies rather than manually constructing the implementation.

Third, describe configuration as a typed operational contract and understand that AEM selects one complete document per PID. Fourth, separate versioned configuration, environment values and secrets, then make missing or invalid states visible and safe. Fifth, stop at HTL, a Sling Model or an existing exporter whenever that surface already satisfies the consumer.

The implementation test is simple: another developer should be able to name the consumer, capability, effective PID and delivery contract from the evidence. Add only the boundary the consumer needs.

## Slide 12: Questions

Thank you. I will leave this slide open for questions from the group. I will not introduce another prompt or exercise here; the session ends with the questions participants want to raise about service ownership, configuration resolution or servlet boundaries.
