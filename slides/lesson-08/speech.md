# Class 8 · Detailed speaker notes

## How to use these notes

- Keep one field—`./title` or `./heading`—as the thread through all eight slides.
- Separate three Resources verbally every time: component definition, dialog definition and authored instance.
- Present the dialog as a storage contract, not as a collection of UI widgets.
- Spend extra time on Slides 4–7; that is where persistence, compatibility and runtime safety become concrete.

## Slide 1: Dialogs, Granite UI and property persistence

- **What it means**
  - Introduce the session’s three threads: Granite UI Resource trees, field-to-property persistence and safe evolution of stored content.
  - Identify the class, date, presenter and 30-minute scope before following the technical trace.
- **How to present it**
  - Preview one value moving from author input → Sling POST → JCR property → rendered output.
  - Name the three topics without teaching the full pipeline yet.
- **Say explicitly**
  - “The field label is presentation; the field name is storage behavior.”
  - “A dialog that saves once is not enough evidence of a safe content contract.”
- **Ask the group**
  - “Who will still depend on this property name two years from now?”
- **Common confusion**
  - Do not treat the dialog definition itself as the runtime content source.
- **Transition**
  - “First separate the three Resources involved.”

## Slide 2: One component spans code, authoring UI and stored content

- **What it means**
  - `/apps/.../component` defines capability.
  - `/apps/.../component/cq:dialog` defines the editor interface.
  - `/content/.../instance` stores values for one authored use.
- **How to present it**
  - Point to each path and ask who changes it: developer or author.
  - Follow `sling:resourceType` from the content instance back to the implementation.
- **Say explicitly**
  - “HTL reads the authored Resource; it does not read values from `cq:dialog`.”
  - “The dialog controls submission, while stored content controls runtime behavior.”
- **Ask the group**
  - “If the dialog label changes, should existing rendered pages change?”
- **Common confusion**
  - `fieldLabel`, `required` and `emptyText` configure authoring UI; they are not automatically persisted as component values.
- **Transition**
  - “The dialog itself is also rendered from a Sling Resource tree.”

## Slide 3: Granite UI renders the dialog from a Resource tree

- **What it means**
  - Granite UI fields and containers are server-side components selected through `sling:resourceType`.
  - Nested `content/items` nodes describe layout and controls.
- **How to present it**
  - Read the tree from `cq:dialog` to the specific textfield.
  - Separate the field’s component type from its configuration properties.
- **Say explicitly**
  - “We configure a tree of authoring Resources; we do not hand-code the resulting Coral UI markup.”
  - “The field resource type creates the control; properties configure that control.”
- **Ask the group**
  - “Which property changes the stored target, and which property changes only the visible label?”
- **Common confusion**
  - Avoid mixing Granite UI resource types with visitor-facing component resource types.
- **Transition**
  - “The most consequential field property is `name`.”

## Slide 4: The field name defines the persistence target

- **What it means**
  - `name="./title"` submits a property relative to the selected component Resource.
  - Sling POST writes `title` on that instance below `/content`.
- **How to present it**
  - Trace the exact string `./title` across dialog definition, request parameter, stored property and HTL expression.
  - Show where the dot-slash resolves; do not describe it as a global repository path.
- **Say explicitly**
  - “The name is relative to the form’s target Resource.”
  - “The authored value is stored beside `sling:resourceType`, not under `/apps`.”
- **Ask the group**
  - “What exact property should appear after saving ‘My first AEM project’?”
- **Evidence to show**
  - Dialog field definition.
  - POST parameter in Network tools when practical.
  - JCR property on the instance.
  - HTL or model consumer.
- **Transition**
  - “Because code depends on that name, renaming it is a schema change.”

## Slide 5: A field change can become a content migration

- **What it means**
  - Changing `./title` to `./heading` affects future saves only.
  - Existing content continues storing `title` until explicitly migrated or re-authored.
- **How to present it**
  - Compare Page A before and after deployment; keep the old property visible.
  - Then show the safe sequence: read new → fallback old → migrate → remove fallback after verification.
- **Say explicitly**
  - “Deploying a new dialog does not rewrite stored content.”
  - “A silent field rename can make valid legacy content appear empty.”
- **Ask the group**
  - “What would fail if the new HTL reads only `heading`?”
- **Common migration cases**
  - Rename a property.
  - Change scalar to multi-value.
  - Move a property into a child Resource.
  - Change the expected type or format.
- **Transition**
  - “Dialog validation helps new authoring, but it cannot guarantee old content.”

## Slide 6: Validation guides authors but does not guarantee stored content

- **What it means**
  - `required`, `maxlength`, labels and validators improve the current authoring path.
  - Stored content may bypass those controls or predate them.
- **How to present it**
  - Separate authoring-time prevention from runtime resilience.
  - Give three bypass examples: old content, package import and API/tooling.
- **Say explicitly**
  - “Dialog validation is not a repository constraint.”
  - “Authenticated author input is still runtime input and must be handled safely.”
- **Ask the group**
  - “Can the runtime assume `required=true` has always been enforced?”
- **Common confusion**
  - A mandatory UI field does not make model injection safely mandatory for every existing Resource.
- **Transition**
  - “The acceptance cases must therefore include configured, legacy and empty content.”

## Slide 7: Verify configured, legacy and empty states end to end

- **What it means**
  - Configured state uses the current property.
  - Legacy state uses a temporary compatibility path.
  - Empty state renders safe visitor output while remaining selectable in author mode.
- **How to present it**
  - Walk one matrix row at a time from stored properties to rendered result.
  - Ask the group to predict the output before revealing it.
- **Say explicitly**
  - “Visitor safety and author usability are different empty-state requirements.”
  - “A placeholder can appear in edit mode without leaking meaningless markup to Publish.”
- **Evidence to request**
  - Stored current/legacy properties.
  - Resolution or fallback rule.
  - Author placeholder.
  - Visitor DOM without empty heading or broken control.
- **Common confusion**
  - Do not verify only the configured happy path.
- **Transition**
  - “These states summarize the complete storage contract.”

## Slide 8: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce review prompts or another exercise.
