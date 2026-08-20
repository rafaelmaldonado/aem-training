# Class 7 · Detailed speaker notes

## How to use these notes

- Keep returning to one distinction: **the component defines capability; the policy governs how that capability is used in a template context**.
- Use one real container from the Guide Page throughout the deck so policy mapping does not feel abstract.
- When explaining a failure, trace `/conf` before suggesting changes to HTL, Java or clientlibs.
- Spend extra time on Slides 3, 4 and 6; they contain the diagnostic and implementation chains.

## Slide 1: Govern authoring choices without changing component code

- **What it means**
  - Component code can remain reusable while different page types expose different author choices.
  - The policy is the governance layer between installed capability and author action.
- **How to present it**
  - Read the slide from component → policy → author.
  - Explain what each participant owns: developer, template author and content author.
- **Say explicitly**
  - “A policy narrows or configures capability; it does not implement the component.”
  - “Different authoring contracts do not automatically require different component code.”
- **Ask the group**
  - “If Guide Pages allow Image but Article Pages do not, should we fork the Image component?”
- **Common confusion**
  - A policy is not an ACL. It controls the authoring contract, not repository authorization.
- **Transition**
  - “The same component can therefore behave differently by template context.”

## Slide 2: A policy configures capability by context

- **What it means**
  - One component implementation can be referenced by different policies.
  - A shared policy change affects every template location that consumes it.
- **How to present it**
  - Start with the single component on the left.
  - Follow each branch and compare the options shown to Guide and Article authors.
- **Say explicitly**
  - “The implementation is shared; configuration is contextual.”
  - “Before editing a policy, identify all of its consumers.”
- **Ask the group**
  - “When is sharing one policy desirable, and when would it create accidental coupling?”
- **Common confusion**
  - Do not describe a policy as a per-page value; it normally governs a reusable template context.
- **Transition**
  - “To discover that context, follow the stored policy mapping.”

## Slide 3: Follow the policy mapping before editing code

- **What it means**
  - The template policy tree mirrors the component location in template structure.
  - `cq:policy` is the link from that location to the actual policy definition under `/conf`.
- **How to present it**
  - Trace left to right: template component path → `cq:policy` → policy definition.
  - Point to the matching relative path; this is the evidence that the mapping belongs to that component location.
- **Say explicitly**
  - “The value is a reference, not the complete policy object.”
  - “A missing or stale mapping can produce correct rendering but incorrect editor choices.”
- **Diagnostic sequence**
  - Confirm the editable template.
  - Confirm the component’s relative path inside it.
  - Read `cq:policy`.
  - Open the resolved definition and inspect its values.
- **Ask the group**
  - “Which evidence would prove that the wrong policy—not the wrong component—was selected?”
- **Transition**
  - “One of the most visible policy decisions belongs to the layout container.”

## Slide 4: Allowed Components belongs to the container policy

- **What it means**
  - Deployment makes a component available to AEM.
  - The current container policy determines whether authors may insert it at that location.
- **How to present it**
  - Point first to all installed components, then to the policy filter, then to the smaller editor list.
  - Demonstrate one positive and one negative case.
- **Say explicitly**
  - “Installed does not mean authorable everywhere.”
  - “Title appearing proves the allow rule; Carousel being absent proves the boundary.”
- **Ask the group**
  - “If Carousel is missing only on Guide Pages, which layer is the first suspect?”
- **Common confusion**
  - Do not immediately reinstall the component or modify its group when one template context hides it.
- **Transition**
  - “Policies also carry defaults, but those defaults are not the same as authored values.”

## Slide 5: Policy defaults are not authored instance values

- **What it means**
  - Policy values under `/conf` configure reusable behavior for a template context.
  - Instance values under `/content` describe one authored component.
- **How to present it**
  - Compare scope: one policy may affect many instances; one instance edit affects one component.
  - Give an example: permitted image widths versus the asset selected by an author.
- **Say explicitly**
  - “A default can influence an instance without becoming authored content on every instance.”
  - “Changing a shared policy is a broad change and needs consumer evidence.”
- **Ask the group**
  - “Does alternative text belong to the reusable policy or to the image’s use on this page?”
- **Common confusion**
  - Avoid storing business content in policy simply to avoid adding a dialog field.
- **Transition**
  - “The Style System is another chain where policy exposes intent and code supplies implementation.”

## Slide 6: Style System maps semantic choices to deployed CSS

- **What it means**
  - The policy exposes an author-friendly style name.
  - AEM stores/applies the mapped CSS class; a clientlib must implement the actual visual behavior.
- **How to present it**
  - Trace Style Name → CSS class → component wrapper → clientlib selector → visual result.
  - Show the selected class in browser markup, not only the author dropdown.
- **Say explicitly**
  - “AEM applies the class; AEM does not invent the CSS.”
  - “Use semantic labels such as Featured, not visual labels such as Blue Border.”
- **Ask the group**
  - “What evidence separates a broken policy mapping from missing CSS?”
- **Common failure modes**
  - Style appears in editor but has no matching clientlib rule.
  - CSS targets the component’s inner element while AEM applies the class to the wrapper.
  - A renamed class leaves existing authored selections without behavior.
- **Transition**
  - “Now reduce these mechanics to the smallest useful Guide Page contract.”

## Slide 7: Define a small Guide Page authoring contract

- **What it means**
  - The Guide Page container permits only Title, Text and Image.
  - Carousel remains intentionally unavailable.
  - Standard and Featured express stable author intent.
- **How to present it**
  - Treat the slide as acceptance criteria, not a wish list.
  - For each item, name the evidence required in editor, repository and browser.
- **Say explicitly**
  - “Every author choice becomes something the team must explain, test and preserve.”
  - “Small is a governance advantage, not a limitation.”
- **Ask the group**
  - “Which additional option has a real author requirement today?”
- **Evidence to request**
  - Allowed component visible.
  - Disallowed component absent.
  - Style class present in DOM.
  - CSS effect visible.
  - Relevant `/conf` paths recorded.
- **Transition**
  - “The takeaway is a five-link control chain.”

## Slide 8: Key takeaways

- **How to present it**
  - Ask participants to rebuild the chain: code → `cq:policy` mapping → policy definition → editor choice → rendered result.
  - Require one observable artifact for each link.
- **Say explicitly**
  - “Capability comes from code; permission to insert comes from the container policy.”
  - “Policy defaults are contextual configuration; instance values remain content.”
  - “Style System needs deployed CSS to produce a visible outcome.”
- **Quick check**
  - Ask where to look when a component exists but is missing only from one template.
- **Transition**
  - “Use the final questions to test whether we can diagnose by evidence instead of guessing.”

## Slide 9: Questions

- **Ask in this order**
  - “Which Guide capability belongs in policy rather than code?”
  - “Which path and property prove the selected policy?”
  - “Which two observations prove an Allowed Components rule?”
  - “Where would you look if a style is selectable but visually unchanged?”
- **Push vague answers**
  - If someone says “check the template,” ask for the exact component path and `cq:policy` value.
  - If someone says “check CSS,” ask whether the expected class is present in the DOM first.
- **Close with**
  - “Use the smallest policy that lets authors succeed consistently; add another choice only when a real requirement needs it.”
