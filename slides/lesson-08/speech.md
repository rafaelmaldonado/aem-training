## Slide 1: Design the storage contract before adding dialog fields.

A dialog field is not only a control on a screen. Its name becomes part of the stored-content contract that code, migrations and future dialog versions must understand. Today we will follow one value from a Granite UI field, through Sling POST, into a component Resource and finally into the rendered browser output.

The main question is not simply whether an author can enter a value. It is whether the value is stored predictably and whether configured, legacy and empty component instances remain safe after the code changes.

## Slide 2: One component spans code, authoring UI and stored content.

Keep these three Resources separate. The component definition under `/apps` identifies the rendering capability. Its `cq:dialog` child defines the editing interface. An authored instance below `/content` stores the values entered for one use of the component.

The authored Resource carries `sling:resourceType`, which connects it back to the implementation. HTL or a model then reads the instance properties. It does not read `fieldLabel`, `required` or entered values from the dialog definition. The dialog influences submission; the persisted Resource is the runtime input.

## Slide 3: Granite UI renders the dialog from a Resource tree.

The dialog is itself a Sling Resource tree. At the root, `cq:dialog` is an `nt:unstructured` node. Its `sling:resourceType` selects the authoring dialog shell. Nested `content/items` Resources define layout, containers and individual fields.

For the Title field, the textfield resource type supplies the control, while properties such as `fieldLabel`, `name`, `required`, `emptyText` and `maxlength` configure its behavior. AEM renders these Resources server-side as Granite UI components; we are describing a resource structure, not writing the visitor-facing form markup by hand.

## Slide 4: The field name defines the persistence target.

Read this trace from left to right. The field name is `./title`. Dot-slash means that the property path is relative to the component Resource targeted by the form. When the author saves “My first AEM project,” the submitted parameter carries the same relative name and value.

Sling POST writes a `title` property on the selected component Resource. The Resource keeps its `sling:resourceType`, which remains the link to the Guide Card implementation. HTL then reads `${properties.title}`. The key point is location: the value belongs to the component instance below `/content`, not to the dialog definition below `/apps`.

## Slide 5: A field change can become a content migration.

Suppose the original dialog writes `./title` and Page A already stores a `title` property. A later dialog version writes `./heading`. That change only affects future submissions. It does not rename the property on Page A.

If new code reads only `heading`, Page A now looks empty even though its content still exists. A safe rollout reads the new property first, temporarily falls back to the legacy property, migrates stored content and verifies the result before removing the fallback. The same reasoning applies when a single property becomes multi-valued or moves into a nested structure.

## Slide 6: Validation guides authors but does not guarantee stored content.

Properties such as `required`, `maxlength` and `emptyText` make the authoring experience clearer. A named validator can prevent a known invalid value from being submitted through the current dialog. Good labels and descriptions also explain the intent of the field instead of forcing authors to infer it.

Those controls do not prove that every stored Resource satisfies the latest rules. Content may predate the validation, arrive through a package or API, or be created by other tooling. Runtime code must still handle missing, malformed and legacy values. Stored content is input, not evidence that the current dialog validation ran.

## Slide 7: Verify configured, legacy and empty states end to end.

Review three states. In the configured state, the current `heading` property renders the intended heading. In the legacy state, the old `title` property still renders through the temporary compatibility rule. In the empty state, neither property is usable.

Visitor markup should not contain an empty heading or broken control. In edit or preview mode, however, an empty component needs an author-visible placeholder so it remains selectable. The evidence should connect the field definition, POST name, stored Resource, resolution decision and observable output for every row.

## Slide 8: Key takeaways

There are five contracts to remember. Component definition, dialog and instance are separate Resources. Granite UI renders the dialog from a resource-type-driven tree. A relative field name controls persistence. Changing the stored name or shape requires an explicit compatibility decision. Runtime behavior must cover configured, legacy and empty states.

Every field creates authoring and compatibility cost. The smallest useful property set is usually easier to explain, migrate, test and support than a dialog filled with speculative options.

## Slide 9: Questions

Use these questions to check the complete mental model. What does `name="./title"` create, and relative to which Resource? Which dialog changes are harmless presentation edits, and which ones change the stored schema? Finally, what evidence shows that an empty component is still authorable without producing unsafe visitor markup?

The goal is to review the whole storage contract, not only whether the dialog opens and saves once.
