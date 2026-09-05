# Class 21 · Multi-Site Management foundations

**Date:** Monday, September 14, 2026  
**Audience:** frontend-oriented developers maintaining traditional AEM Sites implementations  
**Duration:** 30 minutes online  
**Deck goal:** teach developers to trace an MSM relationship from a same-language source to a Live Copy, predict what a synchronization action will change and preserve one deliberate local override.  
**Scope boundary:** introduce language masters, Live Copy sources, blueprint configurations, inheritance and standard synchronization operations without designing a production MSM topology, customizing rollout actions, configuring translation connectors or covering Assets MSM.  
**Required source images:** none; site trees, live relationships, inheritance states and synchronization actions will use precise technical diagrams.  
**Output:** PNG/HTML slides and detailed speaker notes only; no PPTX.

## Visual revision requirements

- Render a visible two-digit slide number (`01`–`12`) in the same fixed top-left position on every slide, including the cover and Q&A.
- Keep the title visually dominant, but use the remaining canvas for concrete technical evidence rather than decorative whitespace.
- Every instructional slide must contain the full learning payload: a labeled relationship, state matrix, decision path or action flow plus concise annotations.
- Include exact AEM terms, representative WKND paths, inheritance states and author actions wherever the topic supports them.
- Use subordinate footer notes only when they add a boundary or caveat; never turn the footer into a second title.
- Prefer information-rich technical courseware with readable grouping over sparse poster-style compositions.

## Slide 1 — Multi-Site Management foundations

**Role:** opening cover  
**Intent:** present the session topic, presenter, date and the four main subtopics.

- Class 21 · Week 5 · Day 21 · September 14, 2026.
- Multi-Site Management foundations.
- Live relationships · Inheritance · Synchronization · Local ownership.
- Juan Maldonado.

**Visual idea:** a clean title composition with one restrained line of four subtopics and a subtle source-to-Live-Copy relationship motif; no paths, component states or explanatory cards.

## Slide 2 — Reuse requires a live relationship, not a similar path.

**Role:** core mental model  
**Intent:** establish the smallest truthful definition of MSM before introducing its vocabulary.

- MSM reuses page content in another site location through a maintained Live Copy relationship.
- The source remains the origin for inherited content.
- The Live Copy can receive later source changes through synchronization.
- A copied page without relationship metadata is only an independent copy.
- Diagnose origin and inheritance before comparing rendered output.

**Visual idea:** contrast SOURCE → LIVE RELATIONSHIP → LIVE COPY with SOURCE → ONE-TIME COPY; show that visually identical pages can have different future behavior.

## Slide 3 — Source, blueprint configuration and Live Copy are distinct objects.

**Role:** vocabulary architecture  
**Intent:** prevent the common mistake of treating every source page or language master as a blueprint configuration.

- A Live Copy source is the page or branch from which content is inherited.
- A blueprint configuration names a source site and supplies site-creation and rollout capabilities.
- A Live Copy is the target branch whose pages retain relationships to equivalent source pages.
- A `LiveRelationship` connects one target resource to its source counterpart.
- A Live Copy can use a regular source, but a blueprint configuration enables the full authoring workflow.

**Visual idea:** four labeled layers—source tree, blueprint configuration, Live Copy tree and per-resource live relationship—with arrows that distinguish configuration from content.

## Slide 4 — Language structure separates language from market reuse.

**Role:** site-structure map  
**Intent:** place language masters and country sites in one concrete WKND-style structure without merging MSM and translation.

- A language root identifies the language of one content branch.
- The language master is the primary authored source for that language.
- Example source: `/content/wknd/language-masters/en`.
- Same-language market sites such as `/content/wknd/us/en` and `/content/wknd/ca/en` can be Live Copies of the English source.
- Keep the relationship direction visible: language source → same-language market variants.

**Visual idea:** a repository tree highlights `language-masters/en` as source and connects it to `us/en` and `ca/en`; French branches remain in a separate lane.

## Slide 5 — Inheritance can stop at one component and continue elsewhere.

**Role:** inheritance-state model  
**Intent:** show how a market takes deliberate ownership of one value without disconnecting the entire page.

- A Live Copy page and its components inherit while their live relationships remain active.
- Cancel inheritance on the narrowest component that requires a local value.
- The local component then stops receiving source updates while sibling components continue inheriting.
- Re-enabling inheritance restores the relationship but does not synchronize automatically.
- Record who owns the local value and why the exception exists.

**Visual idea:** one page with Header, Hero and Offer components; Header and Offer remain linked, while Hero changes from INHERITED to LOCAL for Canada.

## Slide 6 — Inspect relationship evidence before changing content.

**Role:** diagnostic workflow  
**Intent:** give developers an evidence-first path for locating source, status and configuration.

- Begin from the Live Copy page or its source in the Sites console.
- Inspect the Live Copy tab for source path, inheritance and rollout configuration.
- Use References → Live Copies → Live Copy Overview to compare the blueprint tree and target structure.
- Check relationship status at the exact page or component that appears stale.
- Treat path similarity and visual equality as clues, not proof.

**Visual idea:** a five-checkpoint trace from target path to Live Copy properties, source path, relationship status and configured synchronization behavior.

## Slide 7 — Synchronize pulls one Live Copy; rollout pushes from the source.

**Role:** action-direction comparison  
**Intent:** make direction, starting point and scope predictable before an author executes either action.

- Synchronize starts on a Live Copy and pulls eligible changes from its source.
- Rollout starts on a blueprint source and pushes changes to one or more Live Copies.
- Both use the synchronization actions selected by the effective rollout configuration.
- Inheritance cancellations protect deliberate local component values from ordinary synchronization.
- Name the source, target, scope and expected changed fields before execution.

**Visual idea:** a split diagram shows LIVE COPY → SYNCHRONIZE → SOURCE lookup → selected target update beside BLUEPRINT → ROLLOUT → multiple Live Copies.

## Slide 8 — A rollout configuration defines trigger plus actions.

**Role:** synchronization contract  
**Intent:** explain enough configuration to predict behavior without teaching custom MSM extensions.

- The standard rollout configuration runs on an explicit Rollout or Synchronize request.
- Its actions can create, update, delete and reorder content and update references.
- Other configurations may react to activation, deactivation or source modification.
- `On Modification` can affect performance and should not become the default shortcut.
- Prefer installed behavior; introduce a custom rollout configuration only for a proven requirement.

**Visual idea:** TRIGGER → ROLLOUT CONFIGURATION → ACTION SET → TARGET RESULT, with the standard explicit trigger emphasized and automatic triggers shown as guarded alternatives.

## Slide 9 — Choose the least destructive relationship action.

**Role:** author-action decision matrix  
**Intent:** separate local component ownership from page suspension, reset and permanent detachment.

- Cancel component inheritance for one deliberate local override; re-enable it when source ownership should return.
- Suspend a page relationship temporarily; resume it when propagation should continue.
- Reset removes inheritance cancellations and restores the Live Copy to source state, overwriting local changes.
- Detach permanently removes the live relationship and cannot be reversed.
- Preview scope and preserve evidence before Reset or Detach.

**Visual idea:** a matrix compares Cancel/Re-enable, Suspend/Resume, Reset and Detach by granularity, reversibility, local-change impact and future source updates.

## Slide 10 — MSM distributes content; translation changes language.

**Role:** localization boundary  
**Intent:** prevent stale or incorrect language issues from being diagnosed in the wrong AEM subsystem.

- Use MSM to distribute translated source content to country sites within the same language.
- Use AEM translation projects and connectors to create and maintain content across languages.
- Use i18n dictionaries for component-interface strings, not authored page copy.
- A local market override is a content-ownership decision, not automatically a translation decision.
- Diagnose the layer first: relationship, translated page content or UI dictionary.

**Visual idea:** three parallel lanes map MSM to `language-masters/en → us/en`, translation to `en → fr`, and i18n to a component label such as “Read more.”

## Slide 11 — Key takeaways

**Role:** summary  
**Intent:** consolidate the decisions developers should carry into the Week 5 practice.

- Prove the live relationship; do not infer it from paths or matching content.
- Distinguish the source page, blueprint configuration, Live Copy and per-resource relationship.
- Cancel inheritance at the narrowest component that truly needs local ownership.
- Predict trigger, direction, scope and action set before Synchronize or Rollout.
- Keep MSM, translation and component i18n in their separate responsibility lanes.

**Visual idea:** five checkpoints connect relationship evidence, object vocabulary, component ownership, synchronization prediction and localization boundary; close with “SOURCE → INHERITANCE → ACTION → RESULT.”

## Slide 12 — Questions

**Role:** Q&A  
**Intent:** invite questions raised by participants and close without adding another exercise.

- Questions.
- Thank you.
- No scripted prompts or review exercise.

**Visual idea:** quiet closing composition using one source-to-Live-Copy relationship with a protected local component and generous open space.

## Session use

- **Retrieval:** Which value is inherited from the language master, and which value belongs only to the Live Copy?
- **Demo:** trace `/content/wknd/language-masters/en` to one same-language country Live Copy, cancel inheritance on one component, update the source and run a controlled synchronization.
- **Assignment:** record source, inherited or local state, selected action and observed result for one page and one component.
- **Acceptance:** the intended inherited value changes; the deliberate local override remains intact; the developer identifies the relationship, effective action direction and result with evidence.

## Source anchors

- [Reusing Content: Multi Site Manager and Live Copy — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/overview)
- [Creating and Synchronizing Live Copies — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/creating-live-copies)
- [Configuring Live Copy Synchronization — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-sync-config)
- [Live Copy Overview Console — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/live-copy-overview)
- [MSM Best Practices — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm/best-practices)
- [Multi Site Manager and Translation — Adobe Experience League](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/sites/administering/reusing-content/msm-and-translation)
- Course sequence in `reference/eight-week-syllabus.html`, `reference/slide-ready-lessons.html` and `reference/wknd-project-backlog.html`.
