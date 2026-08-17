# Speaker notes · Class 2

## Slide 1: Know where a change belongs.

Today we move from the AEM delivery map into the developer's workspace. The practical question for this session is simple: before we open an editor, what tells us where a change belongs?

The repository, the build and the runtime are one system, but they have different responsibilities. By the end of the session, you should be able to look at a change request, choose the owning module and explain what evidence proves the change reached local AEM.

## Slide 2: Local development has three moving parts.

Start on the left with the WKND source project. This is what we edit, review and version in Git. In the center, the AEM SDK runs a local Author instance where we install and exercise the application. On the right, Dispatcher Tools model the delivery configuration that sits in front of Publish in a cloud environment.

These parts collaborate, but they are not interchangeable. The SDK is not the source project, and Dispatcher Tools are not another AEM instance. For today's exercise, source and Author are required; Dispatcher Tools are part of the map but not a prerequisite for completing the build.

## Slide 3: Maven coordinates one product.

The root `pom.xml` is the build coordinator. It declares the modules, aligns versions and gives Maven the order needed to build a coherent application. When we run the reactor, we are not building unrelated folders independently; we are asking Maven to validate one product assembled from several responsibilities.

Follow the graph from the root POM through the modules to the final package. If one required module fails, the trustworthy result stops there. A partial collection of artifacts is not equivalent to a successful complete build. That is why the first evidence we want is a clean reactor result, not a package copied from an earlier run.

## Slide 4: One component can cross two code modules.

Use the Guide Card as a concrete slice. The dialog and HTL belong to `ui.apps` because they define the AEM component's authoring and rendering surface. If the requirement needs server-side preparation, a Sling Model or service belongs in `core`.

Read the center trace in order: the author configures a property, the model may prepare the value, and HTL renders the result. The boundary matters, but Java is not mandatory for every component. If HTL can safely render the stored value without business logic, adding a model would be extra code without extra value.

## Slide 5: Location communicates lifecycle.

These modules do more than organize files. Each one declares a lifecycle. `ui.content` carries project-managed content, while `ui.config` carries runtime configuration that can vary by environment. The `dispatcher` module owns delivery behavior such as filters and rewrites. The `all` module brings the application artifacts together for deployment.

Trace each lane from source path to the area it affects. A technically valid file placed in the wrong module can produce the wrong deployment behavior. The folder decision is therefore an operational decision, not a formatting preference.

## Slide 6: Verify first. Install second.

There are three evidence gates. First, `mvn clean verify` compiles, tests and packages the reactor. Second, the repository-approved install profile deploys the assembled result to local Author. Third, we check the actual behavior in AEM.

Keep the evidence separate. `BUILD SUCCESS` proves that the build completed; it does not prove that the package installed, that the component is available or that the page behaves correctly. Also notice that I am not inventing an install command here: the project's README is the authority for the profile and local assumptions.

## Slide 7: Route the change before opening the editor.

Now apply the model. I will read each change on the left; choose the owner before following the branch. A Java rule routes to `core`. Dialog and HTL work route to `ui.apps`. Environment-aware service configuration routes to `ui.config`. A delivery filter routes to `dispatcher`. The assembled deployable result comes from `all`.

The goal is not memorizing colored columns. Name what is changing, identify who owns its lifecycle and then verify that the assembled package contains the intended result. That reasoning scales better than searching the repository by filename.

## Slide 8: Key takeaways

Reconstruct the session from the center line. Local development combines a versioned source project, a running SDK and a separate delivery model. Maven coordinates the modules as one product. Module boundaries encode ownership and lifecycle. Build, installation and runtime behavior require different evidence.

If you remember one routine, use this: name the change, find its owner and verify the assembled result. That routine is the bridge from today's repository tour to every implementation and diagnosis later in the course.

## Slide 9: Questions & next move

Before the demo, answer the retrieval question: when a Java class changes, which flow changes—content or code? Use the answer to explain why publishing a page cannot deliver that Java change.

Next I will run the WKND build and locate the `all` package. Your individual practice is to route six change scenarios to modules and justify each choice. Completion requires `BUILD SUCCESS` and at least five justified routes. If setup blocks you, capture the exact command and error; that is better evidence than saying the environment does not work.
