# Class 21 · Multi-Site Management foundations

## Slide 1: Multi-Site Management foundations

Today we begin Week 5 with Multi-Site Management. The session follows four connected ideas: live relationships, inheritance, synchronization and local ownership. We will develop each one in the following slides.

## Slide 2: Reuse requires a live relationship, not a similar path.

Start with the top row. MSM is not just a copying shortcut: AEM keeps a live relationship between a source resource and its corresponding Live Copy resource. That relationship is what allows later source changes to reach the target.

The lower row is deliberately similar in appearance. A one-time copy can have the same text and structure today, but it has no ongoing inheritance behavior. When diagnosing content, matching paths or rendered pages are only clues; we need relationship evidence.

## Slide 3: Source, blueprint configuration and Live Copy are distinct objects.

Read these layers separately. The source is content. A blueprint configuration identifies a source site and enables author-facing capabilities such as creating a site and initiating rollout. The Live Copy is the target content branch. A `LiveRelationship` connects an individual target resource to its source counterpart.

This distinction prevents a common vocabulary error: a language master can be source content without being the same thing as a blueprint configuration. In the next slide we place those objects into a concrete WKND-style tree.

## Slide 4: Language structure separates language from market reuse.

The language master is the primary authored source for one language. In this example, English content begins under `/content/wknd/language-masters/en`, and same-language country sites such as `/content/wknd/us/en` and `/content/wknd/ca/en` can inherit from it through MSM.

Keep French or Spanish in separate language lanes. Translation creates and maintains the content in those languages; MSM then helps distribute each translated source to markets that use that same language. That boundary becomes important when we diagnose a stale local value.

## Slide 5: Inheritance can stop at one component and continue elsewhere.

Look at the component stack. Header, Hero and Offer begin as inherited. If Canada needs a local Hero message, the author cancels inheritance only on Hero. Header and Offer keep their live relationships and continue receiving eligible source updates.

The local badge is an ownership decision, not merely an editor state. Re-enabling inheritance restores the relationship, but it does not automatically synchronize the current value. We should document why the exception exists before handing the site to another team.

## Slide 6: Inspect relationship evidence before changing content.

Follow the checkpoints in order. Begin with the exact target path, inspect the Live Copy tab, identify its source and inheritance status, and then confirm the effective rollout configuration. From the source side, References and Live Copy Overview help compare the source tree with its Live Copies.

The important habit is to inspect at the same granularity as the symptom. A page can have an active relationship while one component is local. That is why page-level status alone may not explain a component value.

## Slide 7: Synchronize pulls one Live Copy; rollout pushes from the source.

The starting point gives us the direction. Synchronize begins on a selected Live Copy and pulls eligible changes from its source. Rollout begins on a blueprint source and pushes eligible changes to one or more Live Copies.

Both actions still depend on the effective rollout configuration. Before clicking either action, name the source, target, scope and expected fields. The inheritance-cancelled component should remain local while inherited values in scope change.

## Slide 8: A rollout configuration defines trigger plus actions.

Separate when from what. A trigger decides when synchronization begins; the action set decides which content operations run. The standard configuration uses the explicit On Rollout trigger for both an author-initiated Rollout and a Live Copy Synchronize request.

Its actions can update, copy, delete and reorder content and update references. Automatic triggers such as On Modification exist, but they are not a harmless convenience; Adobe specifically warns that modification-triggered rollout can affect performance. We stay with installed behavior until a real requirement justifies customization.

## Slide 9: Choose the least destructive relationship action.

Read the matrix from narrowest to most consequential. Cancel and re-enable inheritance manage one local exception. Suspend and Resume pause and restore a page relationship. Reset discards local changes and restores source state. Detach removes the relationship permanently.

Reset and Detach deserve explicit evidence and scope review before execution. If the need is only a market-specific Hero, detaching an entire branch is not flexibility; it destroys the reuse contract we were trying to preserve.

## Slide 10: MSM distributes content; translation changes language.

These three lanes solve different problems. MSM distributes content from an English source to English country sites. Translation projects and connectors create and maintain authored content in another language. Component i18n dictionaries provide interface labels such as “Read more.”

When a localized value is wrong, name the lane before choosing a tool. Is the live relationship stale, is translated page content incomplete, or is a UI dictionary key missing? That first classification prevents a great deal of unproductive troubleshooting.

## Slide 11: Key takeaways

The full evidence chain is source, inheritance, action and result. Prove the live relationship, distinguish the MSM objects, and identify which component owns each value. Then predict the trigger, direction, scope and action set before synchronization.

For the Week 5 practice, the evidence is a small matrix: source, inherited or local state, chosen action and observed result. The intended inherited value must change while the deliberate local override remains intact.

## Slide 12: Questions

Thank you. I will leave this relationship on screen while we take questions.
