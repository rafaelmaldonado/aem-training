# Class 19 · Testing Sling Models and services with JUnit 5 and AEM Mocks

## Slide 1: JUnit 5 and AEM Mocks: protect observable behavior

Introduce Class 19 and the session’s three threads: observable behavior contracts, representative AEM state in memory and red-to-green regression evidence. The goal is not to learn every testing feature. It is to leave with one repeatable path for protecting a Sling Model or service behavior that HTL or another consumer depends on.

Classes 17 and 18 gave the behavior an owner. Today we prove that the owner keeps its promise when content is configured, missing or invalid. We begin with the boundary a useful unit test should protect.

## Slide 2: A unit test protects behavior, not implementation shape.

Start inside the boundary. A consumer supplies an input, calls a public model or service contract and observes a result. That result is what must remain stable through refactoring. For a Guide Card, it might be the title returned when the authored title is absent. For a URL service, it might be the resolved safe URL.

Private methods, field layout and incidental call order sit outside the contract. A test coupled to those details can fail even when the consumer still receives correct behavior. We may inspect implementation details to construct a realistic AEM test, but the assertion should explain the public promise that regressed.

Once the contract is named, the body of the test can stay deliberately simple: arrange the state, act through the contract and assert the result.

## Slide 3: Arrange, act and assert one behavior per failure.

Read this test from left to right. Arrange selects representative content where the optional title is absent. Act creates the `GuideCard` through its public model boundary. Assert compares the returned title with the documented fallback.

The method name, `returnsFallbackWhenTitleMissing`, carries the business state and expectation. If it fails, we know which contract broke before opening the implementation. Shared setup is useful only for state every test genuinely needs; hiding each scenario behind a large fixture builder makes failures harder to read.

JUnit 5 supplies the lifecycle around this small test. We only need a few Jupiter concepts to keep each execution isolated.

## Slide 4: JUnit 5 owns lifecycle, execution and assertions.

The extension prepares and cleans the AEM mock context. Before each `@Test`, `@BeforeEach` establishes fresh common state for that execution. The test performs its action and uses a direct assertion such as `assertEquals`, `assertTrue` or `assertThrows` to express the expected contract.

Notice that the two test runs do not share mutable content or registered services. Isolation prevents one test from passing only because another test happened to run first. A non-static `AemContext` managed by the extension is the straightforward default for this course.

The next slide opens that context and shows which AEM boundaries it can represent—and which ones remain outside a unit test.

## Slide 5: AEM Mocks supplies only the AEM boundary the test needs.

Inside `AemContext` we have mock content, a resource resolver, request and response objects, Sling Model registration and an OSGi service registry. This is enough to exercise a large amount of project Java quickly without starting the AEM SDK.

The discipline is to load only the tree and register only the collaborators required by the behavior. A complete copy of production content is slower to understand and usually hides which property actually drives the result. Choose one resource-resolver mock type that provides the semantics the test needs rather than multiplying every project test across implementations.

The muted outer strip is the fidelity limit. This unit test does not prove Dispatcher rules, browser behavior, package deployment or every repository feature. When the requirement crosses that boundary, it needs a different level of test. First, let us use the in-memory boundary to create a Sling Model.

## Slide 6: Build a Sling Model test from representative content.

The pipeline begins with a small JSON fixture stored under test resources. Loading it creates a representative component resource at a stable path. Register `GuideCardImpl` when test-time classpath discovery is not available, then select the exact resource for the scenario.

For tests, `ModelFactory.createModel` is often more diagnostic than `adaptTo`. An adaptation can return `null` when model creation fails, which hides the cause behind the next null dereference. `createModel` throws a model-creation exception that points closer to a missing required injection, registration problem or failing initialization step.

The final assertion still targets the public `GuideCard` contract. With the harness in place, separate fixtures can prove the configured, missing, invalid and intentionally supported legacy states.

## Slide 7: Test configured, missing and invalid content as separate contracts.

Read the matrix row by row. Configured content should return the authored value after any documented normalization. Missing optional content should produce the explicit fallback or empty state that keeps HTL safe. Invalid content must follow the production decision: reject it, normalize it or disable the capability rather than silently inventing a value.

Legacy content is not automatically a requirement. Support an old property only when compatibility is intentional and covered by a named test; otherwise the test suite can preserve obsolete behavior forever. Each row deserves its own method name and expectation so a failure identifies the broken state immediately.

The same public-contract principle applies to an OSGi service, but the arrangement now includes service dependencies and activation properties.

## Slide 8: Exercise an OSGi service through activation and its public capability.

Begin by registering the collaborator that the component genuinely requires. Then supply representative activation properties and call `registerInjectActivateService`. This asks the mock OSGi environment to inject dependencies, run activation and register the resulting service instead of letting the test construct a partial implementation directly.

Retrieve `GuideUrlService` through its public interface and assert the resolved URL. A second focused state can supply an invalid base URL and assert the deliberate disabled or rejected outcome. The test should reflect the component’s real activation contract without leaking secret material into fixtures or failure output.

This arrangement still does not justify mocking everything around the service. The next decision ladder shows when a real object, AEM Mock, small test double or integration test is the smallest truthful choice.

## Slide 9: Mock the platform boundary, not the code under test.

Start at the top and stop at the first rung that works. Use the real object when it is fast and deterministic in memory. Use AEM Mocks when the behavior crosses a supported Sling, repository or OSGi boundary. Add a small stub or Mockito only when an external or unsupported collaborator prevents the unit from running.

Stub the collaborator’s public result, not a long sequence of internal calls. A test that mocks the class under test or verifies every method invocation usually proves that the test copied the implementation, not that the consumer contract works.

When the behavior depends on a real repository implementation, HTTP stack, Dispatcher or deployed runtime, stop calling it a unit test and use the appropriate integration evidence. Whatever level we choose, the regression check is credible only after we see it detect the missing behavior.

## Slide 10: Red → green proves the regression check.

Run the named Guide Card test with the focused Maven command shown here. With the fallback removed or bypassed, the expected assertion should fail for the reason the test claims. That red output proves the check can detect the regression; it is temporary evidence, not a state to commit or ship.

Restore the minimum fallback behavior and run the same command again. Green now means the protected contract is satisfied. If the first useful failure is a model-creation exception rather than the expected assertion, fix the test harness or model boundary before changing unrelated production code.

After the focused regression passes, run the complete `core` test suite. The narrow loop gives fast feedback; the broader gate checks that the minimum change did not break neighboring behavior.

## Slide 11: Key takeaways

Carry these five checkpoints into the Week 4 practice. Name one public behavior a consumer relies on. Express it in a focused Arrange-Act-Assert test. Build only the representative AEM context needed by that state. Exercise the real model adaptation or service activation boundary rather than bypassing it.

Finally, prove the check red when the behavior is absent and green after the minimum implementation restores it. Coverage numbers may help locate untested code, but this evidence explains which real contract the test protects.

The assignment applies the sequence to configured, missing and invalid Guide Card content. We will close here and leave the remaining time for questions.

## Slide 12: Questions

Thank you. I will leave this slide open for questions from the group. I will not add another prompt or recap; the session ends with the questions participants want to raise about JUnit lifecycle, AEM mock fidelity, Sling Model creation, service activation or red-to-green evidence.
