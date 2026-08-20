# Class 6 · Detailed speaker notes

## How to use these notes

- Keep the central question visible throughout the session: **who owns this element, and should later template changes update existing pages?**
- Spend about 60–90 seconds on Slides 1–6, two minutes on the worked classification in Slide 7, and use Slides 8–9 for retrieval.
- Point to the paths on the slide before naming concepts. The repository location makes ownership concrete.
- Avoid demonstrating template creation as a click sequence. The lesson is about lifecycle and responsibility, not memorizing the editor UI.

## Slide 1: Design the authoring contract before the page

- **What it means**
  - An editable template is a reusable authoring contract, not a finished page or a visual mockup.
  - It defines the shared structure, starting content and governed authoring areas used by future pages.
- **How to present it**
  - Follow the diagram from template type → editable template → page instances.
  - Pause at each arrow and name whether it represents creation, reuse or ongoing connection.
- **Say explicitly**
  - “We are deciding what every Guide Page starts with and what authors may change.”
  - “A template reduces repeated author decisions; it does not own every value forever.”
- **Ask the group**
  - “What would become inconsistent if every author built the page skeleton manually?”
- **Common confusion**
  - Do not call the template a page renderer. Rendering comes from the page resource type.
- **Transition**
  - “To keep those responsibilities separate, inspect the two references stored on a page.”

## Slide 2: A page instance points to both template and renderer

- **What it means**
  - `cq:template` records the authoring contract used by the page.
  - `sling:resourceType` selects the page component that renders the request.
- **How to present it**
  - Start at `/content/.../jcr:content`; then point separately to `/conf` and `/apps`.
  - Use two questions: “How was this page governed?” and “What renders this Resource?”
- **Say explicitly**
  - “The page can keep the same template while its rendering component evolves.”
  - “Following `cq:template` to explain HTL execution is the wrong trace.”
- **Ask the group**
  - “If the page renders incorrectly but the authoring options are correct, which property do we follow first?”
- **Common confusion**
  - `/conf` stores template configuration; it is not a replacement for the component under `/apps`.
- **Transition**
  - “Now go one step earlier: where did the editable template itself come from?”

## Slide 3: A template type seeds the editable template once

- **What it means**
  - A template type supplies the approved starting definition when an editable template is created.
  - Existing editable templates do not continuously inherit later template-type changes.
- **How to present it**
  - Treat the arrow as a one-time copy operation.
  - Contrast “created from” with “kept synchronized with.”
- **Say explicitly**
  - “Changing the template type tomorrow does not repair every editable template created yesterday.”
  - “The retained reference describes origin; it is not live inheritance.”
- **Ask the group**
  - “Where would you make a change intended only for the Guide Page template?”
- **Common confusion**
  - Avoid promising propagation from template type to existing templates.
- **Transition**
  - “Once created, the editable template owns several branches with different lifecycles.”

## Slide 4: One editable template has distinct branches

- **What it means**
  - `structure` defines the connected page skeleton.
  - `initial` contains starting content copied into a new page.
  - `policies` connects template locations to design and authoring rules.
- **How to present it**
  - Read the repository tree top to bottom.
  - For each branch, state owner, lifecycle and typical failure symptom.
- **Say explicitly**
  - “These branches appear in one editor, but they are not synchronized in the same way.”
  - “A wrong structure is a shared-page problem; wrong initial content affects newly created pages.”
- **Ask the group**
  - “Which branch would you inspect if a component is missing from the component browser?”
- **Common confusion**
  - Policy configuration is not authored page content even when authors observe its effects.
- **Transition**
  - “The most important contrast is structure versus initial content.”

## Slide 5: Structure remains connected to every page

- **What it means**
  - Structural components remain controlled by the template across page instances.
  - Locking controls whether page authors can change the structural component itself.
- **How to present it**
  - Point to the header fan-out across Page A, B and C.
  - Then point to the unlocked container and explain that its children remain page-owned.
- **Say explicitly**
  - “Locked does not mean invisible; it means the template retains control.”
  - “An unlocked container can stay structural while the content placed inside it belongs to each page.”
- **Ask the group**
  - “Should an author be able to delete the site header? Should they be able to add content in the main container?”
- **Common confusion**
  - Do not say that every descendant of structure is automatically shared content.
- **Transition**
  - “For values that should only help a page get started, use initial content instead.”

## Slide 6: Initial content is copied only when the page is created

- **What it means**
  - Initial content becomes page-owned at creation time.
  - Later edits affect only pages created afterward.
- **How to present it**
  - Walk through T0–T3 slowly and ask the group to predict Page A before revealing Page B.
  - Emphasize that the two pages can legitimately contain different starter values.
- **Say explicitly**
  - “Initial content is a default, not a synchronization mechanism.”
  - “Updating existing pages requires an explicit content change or migration.”
- **Ask the group**
  - “Why would silently overwriting Page A be dangerous?”
- **Common confusion**
  - Authors often expect a template edit to update existing page content; show why that would destroy ownership.
- **Transition**
  - “We can now classify the real Guide Page requirements using lifecycle rather than visual position.”

## Slide 7: Classify the Guide Page contract by lifecycle

- **What it means**
  - Header: locked structure because it must remain shared.
  - Main container: unlocked structure because every page needs the region but owns its children.
  - Introductory placeholder: initial content because it should become page-owned.
  - Allowed components and defaults: policy.
  - Guide title, image and metadata: authored content under `/content`.
- **How to present it**
  - Reveal or discuss one row at a time.
  - For every row, ask “owner?” and “future propagation?” before naming the branch.
- **Say explicitly**
  - “Where something appears on screen does not determine where it belongs in the repository.”
  - “Lifecycle is the deciding rule.”
- **Ask the group**
  - “Where would a default Title belong if authors must be able to replace it independently?”
- **Common confusion**
  - Do not put authored metadata into template structure simply because every page needs metadata.
- **Transition**
  - “The classification gives us five statements worth retaining.”

## Slide 8: Key takeaways

- **What it means**
  - Page content, rendering component, template type, structure and initial content have different ownership.
- **How to present it**
  - Ask participants to complete each statement before showing or reading it.
  - Reconnect each takeaway to one repository path: `/content`, `/apps` or `/conf`.
- **Say explicitly**
  - “Structure stays connected; initial content is copied.”
  - “`cq:template` explains governance; `sling:resourceType` explains rendering.”
- **Quick check**
  - Give one item—header, empty main container or starter text—and ask where it belongs.
- **Transition**
  - “Use the remaining questions to expose any ownership boundary that is still unclear.”

## Slide 9: Questions

- **Use the slide as retrieval, not as a new lecture**
  - Ask one person to explain the difference between structure and initial content without notes.
  - Ask another person to trace `cq:template` and `sling:resourceType` from a page Resource.
- **Good follow-up prompts**
  - “Should this update existing pages? Why?”
  - “Which exact repository path would you inspect?”
  - “Is the problem authoring governance or rendering?”
- **Close with**
  - “When placement is unclear, decide owner and propagation first; the repository branch follows from that decision.”
