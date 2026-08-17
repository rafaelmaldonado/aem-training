# Class 2 · Local SDK and WKND project structure

Audience: frontend-oriented developers learning AEM from the ground up  
Duration: 30 minutes online + 60–90 minutes individual practice  
Observable outcome: each contributor can explain the local development system, locate a change in the correct WKND module, and distinguish validation from installation.

## Slide 1 · Cover — Know where a change belongs

- Class 2 · Week 1 · Day 2
- Local SDK and WKND project structure
- From source folder to running AEM
- Presenter: Juan Maldonado
- Visual: project tree converging on a local Author runtime
- Role: cover; establish the practical question for the session

## Slide 2 · Local development has three moving parts

- WKND source project: the versioned implementation
- AEM SDK: the local Author runtime
- Dispatcher Tools: the local delivery model, introduced but not required today
- Visual: three connected cards with the responsibility of each part
- Role: concept explanation; prevent “the SDK is the project” confusion

## Slide 3 · Maven coordinates one product

- The root POM defines modules, versions and build order
- A reactor build validates the coordinated project
- A failure in one module prevents a trustworthy complete package
- Visual: root `pom.xml` orchestrating a module pipeline
- Role: process; explain why the repository is not a collection of unrelated folders

## Slide 4 · Code changes live in focused modules

- `core`: Java, Sling Models and OSGi services
- `ui.apps`: components, dialogs, HTL and clientlib definitions
- One visible component can cross both modules
- Visual: a Guide Card split into server logic and AEM presentation files
- Role: comparison; connect runtime behavior to repository ownership

## Slide 5 · Content, configuration and delivery have different lifecycles

- `ui.content`: sample or project-managed content packages
- `ui.config`: environment-aware OSGi configuration
- `dispatcher`: filters, rewrites, virtual hosts and cache rules
- `all`: deployable aggregation of the application
- Visual: four lanes labelled by ownership and deployment responsibility
- Role: architecture; show why location communicates lifecycle

## Slide 6 · Verify first, install second

- `mvn clean verify` compiles, tests and packages the reactor
- The repository-approved install profile deploys to local Author
- `BUILD SUCCESS` proves the build, not that the page behaves correctly
- The repository README overrides generic command examples
- Visual: two gates, Verify → Install → Runtime check
- Role: process; make validation and deployment distinct actions

## Slide 7 · Route the change before opening the editor

- Java formatting rule → `core`
- Dialog field or HTL markup → `ui.apps`
- Environment-specific endpoint → `ui.config`
- Dispatcher filter → `dispatcher`
- Complete deployable package → `all`
- Visual: five change cards routed into the correct modules
- Role: application; prepare the live demo and asynchronous exercise

## Slide 8 · Key takeaways

- Local development combines source, runtime and delivery tooling
- Maven coordinates and validates the complete project
- Module boundaries express responsibility and lifecycle
- Build success, installation and functional verification are separate evidence
- Visual: compact four-point recap around the question “Where does this change belong?”
- Role: summary; retrieval checkpoint before questions

## Slide 9 · Questions

- What is still unclear?
- Which module boundary needs another example?
- What would you verify first?
- Visual: three restrained technical question markers with generous whitespace
- Role: questions-only close; no demo, assignment, command or acceptance content

## Required source images

None. Reuse the approved detailed repository-atlas visual system from `origin_image/slide_07.png` as style reference only.
