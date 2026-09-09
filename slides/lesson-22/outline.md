# Class 22 · Cloud-compatible structure

Approved outline · September 15, 2026 · 30 minutes · English slides, Spanish study guide.
Outputs: PNG images and HTML lesson. No PPTX or speech.
Style reference: ../lesson-21/origin_image/slide_07.png (style only; no required source figures).

## Slide 1 · Cloud-compatible structure
- Class 22 · Week 5 · September 15, 2026 · Juan Maldonado.
- Mutable content · Immutable code · Packages · Import filters.
- Layout: restrained cover, repository boundary motif.

## Slide 2 · A local edit is not a deployment strategy
- An SDK may allow a change that Cloud runtime rejects.
- Code changes travel through Git, build and deployment.
- Author changes travel through authoring and publication.
- Layout: two distinct paths from source to running instance.

## Slide 3 · Repository location defines the boundary
- /apps and /libs are immutable at Cloud runtime; never customize /libs.
- /content and /conf are mutable, but permissions and ownership still apply.
- /oak:index is a special case: managed and deployed with code.
- Layout: annotated repository tree with boundary and exception.

## Slide 4 · Give each module one responsibility
- core: Java bundle; ui.apps: HTL, components and clientlibs.
- ui.config: OSGi configuration deployed as code.
- ui.content: intended mutable baseline; all: deployment container.
- dispatcher: delivery configuration outside the JCR content package.
- Layout: module-to-artifact map.

## Slide 5 · Separate packages; assemble one application
- application packages carry immutable code/configuration.
- content packages carry mutable content; do not mix /apps and /content in one payload package.
- all embeds subpackages and bundles at declared install locations.
- Dependencies and filters make installation intent explicit.
- Layout: container diagram with separate code and content payloads.

## Slide 6 · A filter is an import boundary
- META-INF/vault/filter.xml chooses root, includes, excludes and mode.
- Use /content/aem-training-package-lab, not a site-wide /content root.
- A ZIP entry alone does not explain the effective import scope.
- Inspect the built archive, not only the source tree.
- Layout: source, filter and destination comparison.

## Slide 7 · Predict property changes before installation
- replace: replace covered state; omitted covered content can disappear.
- merge_properties: keep existing properties; add missing state.
- update_properties: replace supplied properties; retain omitted state.
- Legacy merge/update differ by serialization; do not equate them with the newer modes.
- Layout: matrix for existing title, new property and omitted local property; ordinary nt:unstructured nodes only.

## Slide 8 · Mutable does not mean owned by the build
- Authors can change values after initial installation.
- Reinstalling a package can overwrite those values even with update_properties.
- Limit baseline paths; agree who owns each property.
- A repeated deployment is a content test case.
- Layout: timeline from baseline to author edit to redeployment.

## Slide 9 · Local lab: install, edit, reinstall
- Use an isolated /content/aem-training-package-lab branch.
- Build and inspect a content ZIP; install on local Author.
- Change title and add localOnly; predict and compare three import modes.
- Restore the same starting state before each comparison.
- Layout: lab procedure with before/after evidence table.

## Slide 10 · Diagnose the artifact before the instance
- Build fails: inspect package type, filters and validator output.
- Missing content: inspect ZIP paths, effective filter and install log.
- Lost author value: compare import mode, payload and ownership.
- Local success does not prove Cloud compatibility or publication.
- Layout: symptom-to-evidence decision tree.

## Slide 11 · Key takeaways
- Separate runtime-mutable content from deployed code.
- Give every package a clear type and narrow scope.
- Predict import behavior on an already-authored repository.
- Inspect the built ZIP and compare before/after evidence.
- Layout: four linked checkpoints.

## Slide 12 · Questions / Thank you
- Questions.
- Thank you.
- Layout: passive closing; no extra exercise or recap.

## Sources
- https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-project-content-package-structure
- https://jackrabbit.apache.org/filevault/filter.html
- https://jackrabbit.apache.org/filevault/importmode.html
- https://jackrabbit.apache.org/filevault/apidocs/org/apache/jackrabbit/vault/fs/api/ImportMode.html
