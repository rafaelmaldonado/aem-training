# Class 11 · Detailed speaker notes

## How to use these notes

- Keep one Guide Card instance and one empty instance as the running example.
- Read each HTL fragment from stored value to rendered DOM rather than explaining syntax in isolation.
- Ask for the responsible layer before suggesting a Sling Model or service.
- Spend extra time on Slides 4, 6 and 7; they contain the state and security decisions participants must demonstrate.

## Slide 1: Safe and readable HTL

Introduce the session’s three threads: the HTL responsibility boundary, explicit rendering states and context-aware output. Identify Class 11, Week 3, Day 11, August 31, 2026, Juan Maldonado and the 30-minute scope before entering the technical detail.

Preview the flow from prepared values through HTL to browser markup. A configured Guide Card produces semantic markup; missing required data produces a deliberate empty outcome. Keep this as an orientation slide and defer the responsibility model to Slide 2.

Ask: “If a value requires several repository lookups or business decisions, should that work happen inside this template?” Use the answer to move into the responsibility boundary.

## Slide 2: Keep the template boundary narrow

Start with the middle lane. HTL owns direct markup decisions: which element appears, which attribute is written, whether a block is present and how a collection repeats. Those responsibilities are visible in the final DOM and belong close to the markup.

The left lane prepares values. Direct Resource properties are sufficient when the mapping is already clear. A Sling Model or service becomes useful when the value requires normalization, fallback rules, orchestration or business behavior. The point is not to move every expression into Java; that only replaces readable HTL with unnecessary code.

Use one test: can a reviewer explain the rendered contract by reading the template? If control flow or repeated transformations hide the result, prepare a clearer view value before HTL. Next, inspect the smallest unit in the view: an expression.

## Slide 3: Expressions read values where the markup needs them

Read the annotated fragment in place. `${properties.title}` makes the direct relationship to the current Resource explicit. `${card.title}` says that a small view contract prepared the value. Neither form is universally better; choose the one that communicates the real ownership.

Now separate where the values land. Visible title text is an HTML text node. A tooltip is an ordinary attribute. The Guide link is a URI attribute. Those positions look similar in a template, but HTL does not treat their output identically. That distinction becomes important on Slide 7.

Push against temporary variables with no purpose. A name helps when it expresses a condition or reused concept; an alias that merely renames `properties.title` adds another hop. The next slide uses names for a real purpose: making rendering states explicit.

## Slide 4: Conditions and lists should make every state visible

Begin at the decision: does the Guide Card have the data required for a meaningful link? `data-sly-test` should make the configured path easy to follow. It keeps or removes the annotated element; it is not a place to hide a business workflow.

Follow the missing branch twice. In edit mode, the author needs a visible and actionable placeholder. For the visitor, incomplete data must not emit a broken anchor or image. These are two distinct outcomes from the same stored state, and both belong in acceptance evidence.

The list rail shows a separate structural job: repeat the same semantic markup for each Guide tag. Annotate an existing list item whenever possible. Use `<sly>` only when no suitable element can carry the block statement. Close by asking participants to name the configured, empty-author and empty-visitor evidence they would capture.

## Slide 5: Templates and calls reuse small markup contracts

The useful abstraction here is intentionally small. Duration and Region share one stable metadata-row structure, so a template with `label` and `value` parameters makes that contract visible. Each `data-sly-call` still tells the reviewer what is being rendered.

Contrast that with the rejected branch. A generic template that accepts many optional values, calls another template and hides the final element structure creates a private rendering framework. It is harder to trace than the repeated markup it replaced.

Use the lazy threshold: extract a template when repeated markup has one nameable purpose and a small input contract. If the abstraction needs a long explanation, leave the simple markup in place. Next, combine the session's pieces in one complete trace.

## Slide 6: Trace one Guide Card from Resource to DOM

Start with the exact component Resource. Identify the stored title, link and image reference, then carry those same values through every column. This prevents a common review mistake: discussing source, model and browser output as unrelated screenshots.

The view contract exposes only what the template needs. `data-sly-use.card` names that contract, and `data-sly-test` selects the configured or empty path. In the DOM column, verify that the link contains meaningful content and that the URI and visible title landed in their intended contexts.

Then run the trace with one required value removed. The empty rail should change predictably without producing broken visitor markup. A complete review artifact connects stored properties, getters, HTL source and DOM evidence. The next slide examines the security rule operating at each output position.

## Slide 7: Output context is part of the security contract

Read the matrix by row. HTML text is encoded as text. An ordinary attribute is encoded for an attribute value. A known URI attribute such as `href` receives URI validation, so an unsafe value can disappear rather than becoming an executable link.

JavaScript and CSS are the exception that developers must state explicitly. HTL cannot safely infer the grammar inside those blocks, so an expression requires a display context such as `scriptString` or `styleString`. Without the required context, output is suppressed.

Call out both warnings. `context='html'` filters allowed markup; it does not create a trustworthy content contract by itself. `context='unsafe'` disables the protection and must never be used merely to make missing output appear. Ask the group to classify the Guide Card title, link and any inline-script value before showing the summary.

## Slide 8: Key takeaways

Use the five checkpoints as a review order. First identify the view boundary. Then trace direct expressions to their source. Confirm configured and empty outcomes. Extract only small, stable markup templates. Finally, verify the output context where each value lands.

Ask participants to state one piece of evidence for each checkpoint: the Resource or getter, the HTL expression, the empty DOM result, the template call and the context-sensitive output. This turns the summary into a reusable PR-review sequence rather than a list to memorize.

Close on the governing principle: prepared values in; semantic and context-safe HTML out. Then move to the final slide and leave the floor open for questions from participants.

## Slide 9: Questions

That completes the session. Thank the audience and leave the floor open for questions they want to raise. Do not introduce review prompts or another exercise.
