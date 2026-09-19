# Class 26 · Tags and bounded content queries

September 21, 2026 · 30-minute core, optional extension to 60 minutes.

New-calendar scope confirmed by the user. Style-only reference: Class24 slide02. Built-in image generation; PNG slides and HTML, no PPTX or speech.

## Slide 1: Tags and bounded content queries

- Class 26 · Week 6 · September 21, 2026
- Juan Maldonado
- Taxonomy · QueryBuilder · JCR-SQL2 · Pagination

Visual: Large title; simple taxonomy-to-filter-to-results motif. No instructional panels.

## Slide 2: Define what Guide List returns

- Include: pages below the selected root with the hiking tag.
- Exclude: cycling, untagged pages and content outside the root.
- Return two results at a time, ordered by title.
- Author results describe the current repository and identity.

Visual: Selection funnel and five named candidates: 01 Forest trail and 02 River trail included, 03 City ride and 04 Visitor notes excluded, 05 Outside trail excluded by path. Synthetic teaching fixture.

## Slide 3: A tag ID is different from its title

- Namespace: training
- Tag ID: training:activity/hiking
- Display title: Hiking
- Page assignments live in jcr:content/cq:tags.

Visual: Side-by-side taxonomy /content/cq:tags/training/activity/hiking and page assignment cq:tags contains training:activity/hiking; no arrow. Distinguish namespace, ID and display title.

## Slide 4: Two ways to express a repository query

- QueryBuilder: a map of predicates.
- JCR-SQL2: a declarative query statement.
- QueryBuilder typically produces XPath, not SQL2.
- Oak executes the query against repository content.

Visual: Parallel routes QueryBuilder predicates → XPath → Oak and JCR-SQL2 → Oak, converging to readable results. Do not connect QueryBuilder directly to SQL2.

## Slide 5: Start with path, type and property

- path=/content/wknd/us/en/training-search
- type=cq:Page
- property=jcr:content/cq:tags
- property.value=training:activity/hiking

Visual: Four exact monospace lines on left; on right four annotations: subtree boundary, page nodes, relative property, exact stored tag ID. Bottom: All conditions must match. This is selection only; pagination comes next.

## Slide 6: Read the same selection in JCR-SQL2

- SELECT * FROM [cq:Page] AS page
- WHERE ISDESCENDANTNODE(page,
-   '/content/wknd/us/en/training-search')
- AND page.[jcr:content/cq:tags] =
-   'training:activity/hiking'

Visual: Render five lines as one exact SQL code block. Small annotations link type, descendant path and exact tag property. Footer: Same selection; apply ordering and limits separately. No LIMIT clause added.

## Slide 7: Bound and order each result window

- orderby=@jcr:content/jcr:title
- orderby.sort=asc
- p.limit=2
- p.offset=0
- p.guessTotal=true

Visual: Code settings left; diagram first window offset 0, next window offset 2 right. Callouts: Fixture titles are unique. Keep content unchanged while comparing pages. Limit bounds returned hits, not all repository work. guessTotal may be a lower bound.

## Slide 8: Full-text adds a different condition

- fulltext=Forest
- fulltext.relPath=jcr:content
- Keep the existing path, type and tag predicates.
- Expected fixture match: 01 Forest trail.

Visual: Compare exact tag membership with indexed text terms. Show base two results reduced to Forest. Caveat: Tokenization, indexed fields and index freshness affect matches. Do not imply substring matching or tag hierarchy expansion.

## Slide 9: Read the response before drawing conclusions

- hits: results in this window.
- offset: how many matches were skipped.
- more: additional results remain.
- total with guessTotal can be a lower bound.

Visual: Clearly labelled synthetic JSON fragment {"offset":0,"more":false,"total":2}; two result rows 01 Forest trail and 02 River trail. Caveat: An Author hit does not prove publication or visitor access.

## Slide 10: Follow one small example in local Author

- Create tags and five supplied example pages.
- Paste the bounded query into QueryBuilder Debugger.
- Compare offset 0, offset 2 and the Forest filter.
- Read the equivalent SQL2 query in CRXDE Lite.

Visual: Four numbered steps with local Author boundary. Footer: Step-by-step setup and copyable queries are in the lesson. No homework, no deliverables, no Cloud Manager. Index diagnosis continues in Class 27.

## Slide 11: Key takeaways

- Tags classify content through stable IDs.
- Path, type and properties define the selection.
- Order, limit and offset define a result window.
- Exact tag matching and full-text solve different needs.
- Results depend on repository state and read permissions.

Visual: Five concise numbered takeaways with small technical icons, no causal arrows.

## Slide 12: Questions / Thank you

- Questions
- Thank you.

Visual: Passive closing: only Questions and Thank you. No other teaching text or metadata.

## Slide numbering

All 12 PNG images include their two-digit slide number (01–12) in the top-left header margin, including the cover and closing.
