# Class 8 · Dialogs and property persistence

**Date:** Wednesday, August 26, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** explain how a component dialog is represented as a Granite UI resource tree, trace one field from its relative name through Sling POST persistence to JCR and rendering, and design for validation, schema evolution and empty or legacy content.  
**Visual direction:** reuse the approved sober, detailed technical-atlas style from Days 6–7.  
**Required source images:** none. Dialog resources, POST parameters, JCR properties and rendering states will be represented as precise technical diagrams.

## Slide 1 — Design the storage contract before adding dialog fields.

**Role:** cover  
**Intent:** position a dialog change as a content-schema decision, not merely a form-layout task.

- Class 8 · Week 2 · Day 8 · August 26, 2026.
- Dialogs, Granite UI and property persistence.
- Dialog field → POST parameter → JCR property → rendered output.
- Juan Maldonado.

**Visual idea:** one field travels through four technical layers while a storage-contract boundary encloses the complete path.

## Slide 2 — One component spans code, authoring UI and stored content.

**Role:** component anatomy  
**Intent:** separate the component definition, its edit dialog and one authored component instance.

- The component definition lives below `/apps/wknd/components/...` and identifies the resource type and rendering capability.
- `cq:dialog` is a child of the `cq:Component` definition and describes the editing interface.
- An authored instance lives below `/content/.../jcr:content/...` with its own properties and `sling:resourceType`.
- HTL or a model reads the instance's properties; it does not read values from the dialog definition.
- A dialog controls how authors submit content, but the persisted Resource is the runtime contract.

**Visual idea:** three linked repository inspectors—component definition, `cq:dialog` and authored instance—feed one rendered result without merging their responsibilities.

## Slide 3 — Granite UI renders the dialog from a Resource tree.

**Role:** repository anatomy  
**Intent:** make the dialog inspectable as server-rendered Sling Resources rather than client-side form markup.

- `cq:dialog` is an `nt:unstructured` node below the component.
- Its dialog shell uses `sling:resourceType="cq/gui/components/authoring/dialog"`.
- Nested `content/items/...` Resources define layout, tabs, containers and fields.
- A text field uses `granite/ui/components/coral/foundation/form/textfield`.
- Properties such as `fieldLabel`, `name`, `required`, `emptyText`, `maxlength` and `validation` configure the authoring control.

**Visual idea:** a repository tree on the left resolves through `sling:resourceType` into the rendered dialog on the right, with exact field properties between them.

## Slide 4 — The field name defines the persistence target.

**Role:** end-to-end persistence trace  
**Intent:** answer exactly what a field named `./title` creates and where it is stored.

- Dialog field: `name="./title"`.
- The dot-slash makes the name relative to the component Resource targeted by the form submission.
- Sling POST receives `./title=Weekend in Mérida`.
- The component Resource gains `title = "Weekend in Mérida"` while retaining its `sling:resourceType`.
- HTL reads `${properties.title}` and renders the stored value.

**Visual idea:** a five-stage trace from Granite field node to author input, POST parameter, selected JCR Resource and browser output, using the exact same value throughout.

## Slide 5 — A field change can become a content migration.

**Role:** compatibility timeline  
**Intent:** show why renaming or reshaping a field affects content that already exists.

- Existing pages keep the properties written by the previous dialog version.
- Renaming `./title` to `./heading` does not rename existing `title` properties.
- A renderer that reads only `heading` makes legacy instances appear empty.
- Safe rollout: read the new property, fall back to the legacy property, migrate content, then retire the fallback after verification.
- Changing a single property into a multi-value or nested structure requires the same explicit compatibility decision.

**Visual idea:** old and new component instances move through a deployment timeline; a compatibility adapter prevents the old instance from disappearing.

## Slide 6 — Validation guides authors but does not guarantee stored content.

**Role:** defense layers  
**Intent:** distinguish helpful dialog constraints from runtime validation and compatibility responsibilities.

- `required`, `maxlength`, `emptyText` and named validators improve the authoring experience.
- Field labels and descriptions should explain intent, expected format and consequence.
- Existing content may predate the rule; packages, APIs or other tooling may create values without using the current dialog.
- Rendering and model code must still handle missing, malformed or legacy values safely.
- Treat stored content as input, not as proof that the latest dialog validation ran.

**Visual idea:** an authoring-validation gate reduces preventable errors, while a separate runtime-resilience gate protects rendering from stored-state variation.

## Slide 7 — Verify configured, legacy and empty states end to end.

**Role:** review evidence matrix  
**Intent:** turn the session into an observable field-to-browser review that does not require a live demo.

- Configured state: current property exists and renders the intended DOM.
- Legacy state: previous property still produces a supported fallback during migration.
- Empty state: no usable property produces safe markup and an author-visible placeholder in edit or preview mode.
- Evidence connects dialog field definition, POST name, JCR property, HTL or model access and rendered result.
- The reviewer should be able to explain what changes in each state and what remains stable.

**Visual idea:** a three-row state matrix crosses source definition, persisted Resource, rendering decision, author view and visitor DOM.

## Slide 8 — Key takeaways

**Role:** summary  
**Intent:** retrieve the five contracts required to change an AEM dialog safely.

1. A component definition, dialog and authored instance are separate Resources.
2. Granite UI renders `cq:dialog` from a `sling:resourceType`-driven Resource tree.
3. A relative field name determines where Sling POST persists the value.
4. Renaming or reshaping a stored field is a compatibility and migration decision.
5. Dialog validation helps authors; runtime code still handles configured, legacy and empty states.

**Visual idea:** five linked checkpoints from component definition to resilient browser output.

## Slide 9 — Questions

**Role:** Q&A  
**Intent:** close without requiring a live demonstration.

- What exactly does `name="./title"` create?
- Which dialog change would require a content migration?
- What evidence proves that an empty component remains authorable and safe?

**Visual idea:** a simplified dialog-to-browser trace with three highlighted decision points and generous discussion space.

## Source anchors

- Adobe Experience Manager as a Cloud Service: Components Reference Guide.
- Adobe Experience Manager as a Cloud Service: Components Overview.
- Granite UI: Form and TextField component reference.
- Apache Sling: Manipulating Content with the SlingPostServlet.
- Course syllabus and the Week 2–3 authoring practices in `reference/aem-course-topics.html` and `reference/wknd-project-backlog.html`.
