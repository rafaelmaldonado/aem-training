# Class 6 · Speaker notes

## Slide 1: Design the authoring contract before the page

Today we move from request resolution into authoring design. An editable template is not a screenshot of a finished page. It is a contract that determines how a page starts, which parts stay shared and where authors are allowed to work.

Follow the sequence on the slide: a template type gives us an approved starting definition, an editable template turns that definition into a site-specific contract, and page instances use that contract while owning their individual content.

## Slide 2: A page instance points to both template and renderer

Start in the center with the page’s `jcr:content` Resource. Two properties answer two different questions. `cq:template` tells us which editable-template contract was used. `sling:resourceType` tells Sling which page component provides rendering capability.

The paths reinforce the ownership boundary. The page instance is under `/content`, the authoring contract is under `/conf`, and the project page component resolves under `/apps`. Do not use the template path to explain rendering; use the resource type.

## Slide 3: A template type seeds the editable template once

A template type is a starting definition for creating an editable template. It can provide the initial structure, initial content and page component resource type expected by the project.

The important boundary is the copy operation. Once `guide-page` is created, it can evolve as its own editable template. A later edit to the template type does not flow automatically into that existing template. Treat the remaining reference as informational, not as a dynamic inheritance chain.

## Slide 4: One editable template has distinct branches

Read the repository tree from the template root. Its `jcr:content` holds metadata and lifecycle status. The `structure` branch defines the shared skeleton. The `initial` branch defines the editable starting content copied to new pages. The `policies` branch connects design rules.

These branches may appear together in the Template Editor, but they have different synchronization and ownership behavior. Today we establish that boundary; tomorrow we will go deeper into policies and allowed components.

## Slide 5: Structure remains connected to every page

Structure is for elements that must stay consistent across page instances. A locked site header cannot be moved or deleted by page authors. An unlocked main container creates a controlled area in which each page can own different content.

Now follow the fan-out to Page A, Page B and Page C. A later structural header change is reflected across those pages because the structure remains connected. That does not mean the template overwrites the content authors placed inside the unlocked areas.

## Slide 6: Initial content is copied only when the page is created

Use the timeline. At T0 the template contains the starting value `Start here`. Page A is created and receives a page-owned copy. At T2 the template’s initial value changes to `Updated starter`, but Page A remains unchanged. Page B, created afterward, receives the new default.

This is why initial content is useful for a starting experience but not for synchronization. When existing page content must change, use an explicit migration or another governed update mechanism rather than expecting the template default to rewrite authored content.

## Slide 7: Classify the Guide Page contract by lifecycle

Apply the model to the Guide Page. A shared site header belongs in locked structure. The main authoring container also belongs to structure, but it must be unlocked so page authors can work inside it. An editable introductory placeholder is initial content because it should be copied and then owned by each page.

Allowed components and design defaults belong to policy, which we will configure in Day 7. Guide-specific text, images and metadata belong to the page under `/content`. The decision rule is ownership plus synchronization behavior, not visual position on the screen.

## Slide 8: Key takeaways

Keep the five distinctions together. The page stores authored content and the page component renders it. The editable template controls how pages begin and which structure stays shared. The template type seeds the editable template once.

Structure remains connected, while initial content is copied at creation. When an element is difficult to place, ask who owns it and whether existing pages should receive future changes.

## Slide 9: Questions

Which part of the Guide Page contract still feels ambiguous? If a template changes tomorrow, which pages and which parts should update? And if we need to explain rendering, which property do we follow instead of the template reference?

Use the questions to revisit one concrete path or lifecycle decision. No live environment is required to close the session.
