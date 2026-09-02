# Class 19 · Testing Sling Models and services with JUnit 5 and AEM Mocks

**Date:** Thursday, September 10, 2026  
**Audience:** frontend-oriented developers beginning AEM backend testing  
**Duration:** 30 minutes online  
**Deck goal:** teach developers to protect one observable Sling Model or service contract with focused JUnit 5 tests, representative AEM Mocks state and visible red → green regression evidence.  
**Scope boundary:** build on Classes 17–18 without teaching broad test-driven development, exhaustive Mockito techniques, integration testing against a running SDK or coverage targets.  
**Required source images:** none; test anatomy, mock context and state coverage will use technical diagrams and compact code excerpts.  
**Output:** PNG/HTML slides and detailed speaker notes only; no PPTX.

## Visual revision requirements

- Render a visible two-digit slide number (`01`–`12`) in the same fixed top-left position on every slide, including the cover and Q&A.
- Keep the title visually dominant, but use the remaining canvas for concrete technical evidence rather than decorative whitespace.
- Every instructional slide must contain the full learning payload: a labeled process, matrix, decision path or architecture plus concise explanatory annotations.
- Include exact AEM/JUnit terms, representative paths, annotations, method names, state values or Maven commands wherever the slide topic supports them.
- Use subordinate footer notes only when they add a boundary or caveat; never turn the footer into a second title.
- Prefer information-rich technical courseware with readable grouping over sparse poster-style compositions.

## Slide 1 — JUnit 5 and AEM Mocks: protect observable behavior

**Role:** opening overview  
**Intent:** identify the session, presenter and date while previewing the three learning threads.

- Class 19 · Week 4 · Day 19 · September 10, 2026.
- Testing Sling Models and services with JUnit 5 and AEM Mocks.
- Today: behavior contracts, representative AEM context and red → green evidence.
- 30-minute technical session.
- Juan Maldonado.

**Visual idea:** a strong title block with presenter and date, plus three compact anchors for a public contract, an in-memory AEM context and a red-to-green test result.

## Slide 2 — A unit test protects behavior, not implementation shape.

**Role:** testing boundary  
**Intent:** anchor every test in an externally observable contract that may regress.

- Start with one behavior a consumer depends on.
- Supply the smallest representative input that can prove it.
- Execute the public model or service contract.
- Assert the returned value, state or failure that the consumer observes.
- Avoid assertions about private methods, field layout or call order without a contract reason.

**Visual idea:** a consumer contract encloses INPUT → PUBLIC API → OBSERVABLE RESULT while private implementation gears remain outside the assertion boundary.

## Slide 3 — Arrange, act and assert one behavior per failure.

**Role:** test anatomy  
**Intent:** make a failing test small enough to diagnose without introducing a custom testing abstraction.

- Arrange representative content, configuration and dependencies.
- Act once through the public contract under test.
- Assert the result and include the business expectation in the test name.
- Keep shared setup limited to state every test genuinely needs.
- Prefer a few explicit tests over one scenario with many unrelated assertions.

**Visual idea:** a three-column test specimen labels ARRANGE, ACT and ASSERT, ending in one readable JUnit failure message.

## Slide 4 — JUnit 5 owns lifecycle, execution and assertions.

**Role:** framework map  
**Intent:** introduce only the JUnit Jupiter pieces needed for a focused AEM unit test.

- `@Test` marks an executable behavior check.
- `@BeforeEach` prepares fresh common state before every test.
- `@ExtendWith(AemContextExtension.class)` connects the AEM mock lifecycle.
- Use direct assertions such as `assertEquals`, `assertTrue` and `assertThrows`.
- Test isolation matters more than clever fixtures or inheritance.

**Visual idea:** JUnit invokes extension setup → `@BeforeEach` → `@Test` → assertion → cleanup for two independent test methods.

## Slide 5 — AEM Mocks supplies only the AEM boundary the test needs.

**Role:** mock-context architecture  
**Intent:** distinguish a fast in-memory unit-test environment from a running AEM instance.

- `AemContext` exposes mock resource, request, response and OSGi facilities.
- Load only the content tree required by the behavior.
- Register only the models, services or adapters the unit consumes.
- Choose one resource-resolver mock type that fits the contract.
- A passing mock test does not prove browser, deployment or full-runtime integration.

**Visual idea:** a test class enters one bounded `AemContext` containing mock content, a resource resolver, model registration and an OSGi registry; a full AEM SDK remains visibly outside.

## Slide 6 — Build a Sling Model test from representative content.

**Role:** model test flow  
**Intent:** connect test JSON and model registration to a diagnosable model instance and public getter.

- Register `GuideCardImpl` when classpath model discovery is not available to the test.
- Load minimal JSON content under a stable test path.
- Select the current resource that represents the component state.
- Prefer `ModelFactory.createModel(...)` when adaptation failures need an exception instead of `null`.
- Assert the view-ready getter or explicit empty state consumed by HTL.

**Visual idea:** `GuideCardImplTest.json` → mock resource → registered model → `ModelFactory` → `GuideCard` contract → focused assertion.

## Slide 7 — Test configured, missing and invalid content as separate contracts.

**Role:** state-by-expectation matrix  
**Intent:** protect the authoring fallbacks and validation decisions that keep rendering safe.

- Configured content returns the authored, normalized value.
- Missing optional content returns the documented fallback or empty state.
- Invalid content is rejected, normalized or disabled according to the production contract.
- Legacy content stays safe only when backward compatibility is intentional.
- Name each state in its test so a failure identifies the broken contract immediately.

**Visual idea:** a four-row matrix maps CONFIGURED, MISSING, INVALID and LEGACY inputs to explicit expected Guide Card outcomes, with no generic “happy path” row.

## Slide 8 — Exercise an OSGi service through activation and its public capability.

**Role:** service test flow  
**Intent:** test configuration and required dependencies without bypassing the Declarative Services boundary.

- Register required collaborator services in the mock OSGi registry.
- Supply typed activation properties that represent one real environment state.
- Use `registerInjectActivateService(...)` to inject, activate and register the component.
- Retrieve the service through its public interface.
- Assert capability output and deliberate disabled or rejected behavior for bad configuration.

**Visual idea:** mock collaborator + typed properties → DS activation gate → registered `GuideUrlService` → public result, with invalid configuration routed to the expected safe state.

## Slide 9 — Mock the platform boundary, not the code under test.

**Role:** test-double decision  
**Intent:** prevent brittle tests that merely replay implementation calls.

- Use real value objects and production code whenever they run cheaply in memory.
- Use AEM Mocks for Sling, repository and OSGi boundaries it implements.
- Use a small stub or Mockito only for an external or unsupported collaborator.
- Stub the collaborator’s public result, not the service’s internal sequence.
- Move to an integration test when the behavior depends on a real repository, HTTP stack or deployed runtime.

**Visual idea:** a decision ladder stops at REAL OBJECT, then AEM MOCK, then SMALL TEST DOUBLE, and finally INTEGRATION TEST when fidelity exceeds the unit boundary.

## Slide 10 — Red → green proves the regression check.

**Role:** regression evidence loop  
**Intent:** show that the focused test detects the missing behavior before it certifies the fix.

- Run one named test with a focused Maven command.
- Remove or bypass the Guide Card fallback and capture the expected failure.
- Restore the minimum behavior and rerun the same command green.
- Read the first useful assertion or model-creation failure before changing code.
- Rerun the complete `core` test suite after the focused regression passes.

**Visual idea:** `mvn -pl core -Dtest=GuideCardImplTest test` moves through RED evidence → minimum fix → GREEN evidence → full core test gate.

## Slide 11 — Key takeaways

**Role:** summary  
**Intent:** consolidate the testing decisions developers should carry into Week 4 practice.

- Protect one observable behavior through the public contract.
- Keep arrange, act and assert explicit and independently diagnosable.
- Build the smallest representative AEM context for each state.
- Exercise Sling Models and services through their real adaptation or activation boundaries.
- Show the test failing for the missing behavior before accepting green output as regression evidence.

**Visual idea:** five checkpoints connect consumer contract, focused JUnit test, AEM context, model or service boundary and red-to-green proof; close with “TEST THE CONTRACT THAT MUST NOT REGRESS.”

## Slide 12 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close without adding another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** quiet closing composition using a completed green test path and generous open space.

## Session use

- **Retrieval:** Which observable behavior should fail when a Sling Model fallback is removed?
- **Demo:** write and run a failing AEM Mocks test for the Guide Card fallback, restore the minimum implementation and rerun the same test green.
- **Assignment:** test configured, missing and invalid Guide Card input; add a focused service test only if the practice includes environment-dependent behavior.
- **Acceptance:** focused JUnit 5 tests pass; representative AEM Mocks state is explicit; at least one test is shown failing without the protected behavior; assertions target public output rather than private implementation shape.

## Source anchors

- [Unit testing — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-learn/getting-started-wknd-tutorial-develop/project-archetype/unit-testing)
- [AEM Mocks usage — wcm.io](https://wcm.io/testing/aem-mock/usage.html)
- [Sling Mocks — Apache Sling](https://sling.apache.org/documentation/development/sling-mock.html)
- [Sling Models — Apache Sling](https://sling.apache.org/documentation/bundles/models.html)
- [JUnit User Guide](https://docs.junit.org/current/user-guide/)
- Course sequence in `AEM-COURSE-TOPICS.md`, `reference/eight-week-syllabus.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
