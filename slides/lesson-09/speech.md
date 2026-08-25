# Class 9 · Detailed speaker notes

## How to use these notes

- Keep one image selected in a Guide Page throughout the session so the repository, markup and Network evidence refer to the same instance.
- Repeat the three-part contract: managed asset, delivered bytes and accessible meaning.
- Avoid presenting accessibility as a dialog checkbox or responsive behavior as a CSS-only concern.
- Spend extra time on Slides 4–7; they contain the decisions participants must demonstrate.

## Slide 1: Assets, Core Image and accessible delivery

- **What it means**
  - Introduce the session’s three threads: managed DAM references, Core Image delivery and accessible meaning in context.
  - Identify the class, date, presenter and 30-minute scope before examining evidence.
- **How to present it**
  - Preview the pipeline: DAM asset → Image component → browser request → accessible DOM.
  - Name the three topics without expanding the evidence matrix yet.
- **Say explicitly**
  - “The image is not finished when it looks correct.”
  - “We must verify what is referenced, what bytes were sent and what meaning was exposed.”
- **Ask the group**
  - “Which of those three concerns can a screenshot prove?”
- **Common confusion**
  - Do not combine the asset path, rendered URL and alternative text into one vague concept called ‘the image.’
- **Transition**
  - “Start with ownership: the page references the asset; it does not own the binary.”

## Slide 2: An authored image is a reference, not a copied binary

- **What it means**
  - `/content/dam/...` owns the original file, renditions and reusable metadata.
  - The page component stores `fileReference` pointing to that asset.
- **How to present it**
  - Point first to the DAM path, then to the component instance and its property.
  - Explain the lifecycle consequence of one asset being referenced by many pages.
- **Say explicitly**
  - “Replacing or moving the DAM asset can affect every incoming reference.”
  - “The component instance stores a pointer, not another copy of the binary.”
- **Ask the group**
  - “What should we inspect before deleting or moving this asset?”
- **Evidence to show**
  - `fileReference` value.
  - Asset existence and metadata.
  - References view or known consuming pages.
- **Transition**
  - “Once the reference is correct, use the existing delivery capability before writing custom markup.”

## Slide 3: Use the Core Image capability before custom markup

- **What it means**
  - A project proxy preserves site ownership while delegating delivery behavior to Core Image.
  - Policy configures supported behavior such as widths without copying implementation.
- **How to present it**
  - Trace project resource type → `sling:resourceSuperType` → installed Core Image version.
  - Separate proxy identity, policy configuration and inherited implementation.
- **Say explicitly**
  - “The project owns the proxy; Adobe’s Core Component owns the complex image behavior.”
  - “Verify the installed version before selecting a versioned super type.”
- **Ask the group**
  - “Which verified requirement cannot be met by Core Image and policy?”
- **Common confusion**
  - Do not promise a feature because a documentation path exists; the dependency must be installed and compatible.
  - Do not copy Core Image HTL merely to change a policy-controlled option.
- **Transition**
  - “Delivery capability cannot decide what the image means in this page context.”

## Slide 4: Alternative text describes purpose in context

- **What it means**
  - Informative images need a concise equivalent of their essential meaning.
  - Decorative images need an explicit empty alternative.
  - Functional images need text describing the action or destination.
  - Complex images need a short identifier plus a nearby detailed equivalent.
- **How to present it**
  - Start with purpose, not with the pixels.
  - Give the same image four contexts and ask how the alternative changes.
- **Say explicitly**
  - “Missing `alt` and `alt=""` are not equivalent.”
  - “Avoid filenames and ‘image of’; describe the useful meaning.”
- **Ask the group**
  - “If this image is the only content in a link to the Guide, what should the accessible name communicate?”
- **Common confusion**
  - Empty alternative is correct only when the image adds no information or function in that context.
- **Transition**
  - “DAM metadata can suggest text, but it cannot know every page purpose.”

## Slide 5: DAM metadata is a source, not the final decision

- **What it means**
  - Shared metadata can provide a reusable description.
  - The authored page context determines whether that description is appropriate, empty or action-oriented.
- **How to present it**
  - Reuse the same suspension-bridge asset in hero, decorative background and linked-card contexts.
  - Emphasize that the binary and metadata remain unchanged while the required accessible result changes.
- **Say explicitly**
  - “Metadata proposes; page purpose decides.”
  - “A safe default reduces work but does not remove author responsibility.”
- **Ask the group**
  - “Which of these three uses can safely inherit the DAM description unchanged?”
- **Responsibility split**
  - Developer: safe component behavior.
  - Template author: governed defaults and options.
  - Content author: meaning in the current page.
- **Transition**
  - “Now verify that the browser also receives appropriate bytes.”

## Slide 6: Responsive delivery lets the browser choose appropriate bytes

- **What it means**
  - Component policy defines useful candidate widths.
  - Markup exposes candidates; the browser selects using layout and device density.
  - Rendered CSS width and transferred source size are different measurements.
- **How to present it**
  - Show the candidate widths first.
  - Then compare rendered dimensions in Elements with the selected request in Network.
  - Resize once and observe whether the selected candidate changes.
- **Say explicitly**
  - “CSS can display a large downloaded image at a small size.”
  - “Lazy loading changes when a request happens; responsive selection changes which source is requested.”
- **Ask the group**
  - “What browser evidence proves we avoided transferring the largest rendition?”
- **Scope boundary**
  - Use Adaptive Image Servlet and local browser evidence for the exercise.
  - Mention Web-Optimized Image Delivery as cloud capability, not a requirement for the local lab.
- **Transition**
  - “Combine repository, DOM and Network evidence in one review matrix.”

## Slide 7: Asset references turn maintenance into a dependency decision

- **What it means**
  - Moving, replacing, unpublishing or deleting a DAM asset can affect every page that references it.
  - Lifecycle decisions should begin with incoming-reference evidence and end with consumer verification.
- **How to present it**
  - Follow the reference from one DAM asset to multiple Guide Pages.
  - Compare the safe sequence—inspect, assess, change and verify—with a direct destructive change.
- **Say explicitly**
  - “The asset path is a dependency contract, not just a filing location.”
  - “Reference inspection reduces risk; consumer verification proves the change.”
- **Transition**
  - “Now combine ownership, accessibility and delivery in one evidence matrix.”

## Slide 8: Verify the Guide Page image contract with evidence

- **What it means**
  - Each state must connect stored reference, rendered alternative, browser-selected source and author behavior.
- **How to present it**
  - Walk informative, decorative and missing/invalid rows separately.
  - Require an artifact for every column instead of accepting “it looks right.”
- **Say explicitly**
  - “A correct `fileReference` does not prove correct alternative text or efficient delivery.”
  - “An Author preview does not prove the asset and required rendition are available on Publish.”
- **Evidence to request**
  - Component `fileReference` and asset path.
  - Rendered `alt` state.
  - Selected image request and dimensions.
  - Safe empty or invalid state.
- **Transition**
  - “That completes the session. I’ll leave the final slide open for your questions.”

## Slide 9: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce review prompts or another exercise.
