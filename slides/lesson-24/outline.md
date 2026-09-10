# Class 24 · Content Fragments and Experience Fragments

September 17, 2026 · 30 minutes · English slides; Spanish summary and simple Author examples.
Continue established style and built-in image workflow without intermediate confirmations. No speech or PPTX.
Style reference: ../lesson-23/origin_image/slide_07.png.

## Slide 1 · Content Fragments and Experience Fragments
- Class 24 · Week 5 · September 17, 2026 · Juan Maldonado
- Structured content · Composed experiences · References · Publication
- Layout: Cover: title and metadata, two simple visual motifs for fields and a composed page block. No teaching panels.

## Slide 2 · Choose what should be reused
- Content Fragment: reusable structured content.
- Experience Fragment: reusable components, content and layout.
- A guide fact sheet fits fields; a shared notice fits a composed block.
- The consuming Sites page still needs the appropriate component.
- Layout: Two-column comparison: Guide fact sheet with heading and summary fields versus a Shared notice composed from Title and Text. These are illustrative designs, not screenshots.

## Slide 3 · A Content Fragment Model defines the fields
- A model defines field names, data types and validation.
- An enabled model can be allowed on an Assets folder.
- Each fragment supplies values for that model.
- Changing a shared model can affect existing fragments.
- Layout: Model schema heading: Single line text, summary: Multi line text → fragment values heading: Trail information, summary: Bring water. Distinguish field label from property name. No JSON or APIs.

## Slide 4 · Content is separate from its page presentation
- The fragment stores authored field values.
- A Sites component selects the fragment, variation and elements.
- The component and page styles determine the presentation.
- Reusing a fragment does not require copying its text into each page.
- Layout: One Content Fragment referenced by two different page renderings, labelled Page A and Page B. Reference arrows point FROM consuming page TO fragment. No layout stored inside CF; no headless architecture.

## Slide 5 · Content Fragment variations are authored alternatives
- Main content is the starting content.
- A variation provides an alternative set of values.
- The page component explicitly selects the required variation.
- A variation is not automatically a translation or a synchronized copy.
- Layout: Main summary Bring water and wear comfortable shoes; short variation Bring water. Label authored alternative and explicit selection. No automatic-sync arrows.

## Slide 6 · An Experience Fragment reuses a composed block
- An editable template supplies structure and allowed components.
- Authors compose content and layout inside a variation.
- A Sites Experience Fragment component references that variation.
- Example: one Title and one Text reused as a shared notice.
- Layout: Experience Fragment variation contains Title and Text; two Sites pages reference it. All reference arrows point FROM pages TO variation. No copied content or invented screenshots.

## Slide 7 · Locate the fragment and its definition
- Content Fragment assets live under /content/dam.
- Content Fragment Models live under /conf.
- Experience Fragment content lives under /content/experience-fragments.
- Editable templates and policies live under /conf.
- Layout: Repository map with separate CF and XF branches: definition /conf and authored content paths. /conf boxes must be distinct model versus editable template/policy; not one shared schema. Read-only inspection; no path editing instructions.

## Slide 8 · References share a source; copies create another source
- Two pages can reference the same fragment or variation.
- Editing that source can affect both pages when rendered.
- Copying creates separate content with a separate lifecycle.
- Check references before moving, deleting or changing shared content.
- Layout: Comparison: two pages with references to one shared notice versus two separate copied notices. Reference arrows FROM pages TO sources. Publication/cache can delay visible changes; no instant propagation promise.

## Slide 9 · Author preview does not prove Publish completeness
- Inspect the consuming page, selected fragment and referenced assets.
- Verify required model or template dependencies on the target.
- Publishing one item does not prove every dependency is available.
- Check the target page and its delivery cache after publication.
- Layout: Dependency checklist graph rooted in consuming page referencing fragment, model/template and assets. Author and Publish separate boundaries, explicit Verify target; not automatic replication of all dependencies. No publishing root folders.

## Slide 10 · Two simple examples in local Author
- Content Fragment: create heading and summary, then render them in Sites.
- Experience Fragment: compose a Title and Text, then reference its variation.
- Edit the source and refresh the consuming page to observe reuse.
- If a selector is empty, inspect allowed models, templates or components.
- Layout: Two short numbered example routes, no assignments, acceptance criteria or new Java. Exact example names Training fact sheet and Training notice. Mention detailed steps in HTML, no placeholder code.

## Slide 11 · Key takeaways
- Choose structured fields or a composed experience.
- Separate model/template, fragment and consuming component.
- Reference shared content and manage the impact of changes.
- Verify dependencies and output on the target instance.
- Layout: Four numbered concise takeaways with icons separated by rules, no causal arrows between unrelated concepts.

## Slide 12 · Questions / Thank you
- Questions
- Thank you.
- Layout: Passive closing ONLY Questions, Thank you. and small 12. No recap or footer claim.
