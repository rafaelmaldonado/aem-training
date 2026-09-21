# Class 27 · Diagnosing costly queries

September 22, 2026 · 12 slides · English · 30-minute core, expandable to 60.

Established workflow: complete numbered PNGs, HTML lesson and Spanish HTML/Markdown guide; no speech or PPTX. Style reference: lesson26 slide04 (style only). Prior continuation waiver persists.

## 01. Diagnosing costly queries
- Class 27 · Week 6 · September 22, 2026
- Juan Maldonado
- Explain · Selectivity · Ordering · Indexes
- Visual: Large editorial title left, repository-to-magnifier-to-query-plan motif right. No instructional cards.

## 02. Two hits do not mean two reads
- A small response can hide a large scan.
- Filtering and sorting may happen after index access.
- A low limit bounds output, not all the work.
- Compare scanned rows, returned results and ordering.
- Visual: Oversized 2 HITS on right. A funnel from many candidate page icons through filter and sort to two pages. No invented measurements; label candidate count unknown.

## 03. How Oak chooses a plan
- The planner compares estimated access costs.
- An index supplies candidates; remaining checks may follow.
- Repository traversal reads the subtree without a suitable index.
- Estimated cost is not elapsed milliseconds.
- Visual: Flow query → cost-based planner; two alternative branches Index access and Repository traversal; converge to Remaining filters / ACL checks, then Results. Small separate note: Ordering may require reading candidates before a window can be returned. Simplified single-selector model, no promise that sorting always happens last.

## 04. Read more than the index name
- Identify the selected index or traversal plan.
- Check node type and path restrictions.
- Check which property filters reach the index.
- Check whether the index supplies the requested order.
- Visual: Four numbered inspection rows beside a conceptual plan with highlighted labels: access path, type + path, property, ordering. Label the diagram Conceptual plan — not SDK output. Footer: An indexed query can still scan too much.

## 05. Correct the query contract first
- Root: /content/wknd/us/en/training-search
- Type: cq:Page; tag: training:activity/hiking
- Order: jcr:content/jcr:title, ascending
- Window: p.limit=2; p.offset=0; p.guessTotal=true
- Visual: Compare Too broad /content/wknd/us/en versus Intended root /content/wknd/us/en/training-search in two clear code-like panels. Show Outside trail excluded by corrected path. Below show other key_points. Footer: Narrowing the path restores the intended selection; it changes results.

## 06. EXPLAIN and MEASURE answer different questions
- EXPLAIN: inspect the plan without running the result query.
- MEASURE: execute and report scanCount by selector.
- EXPLAIN MEASURE: plan plus estimated cost.
- Execution options in the AEM tool may run the query.
- Visual: Three horizontal contrasting lanes EXPLAIN, MEASURE, EXPLAIN MEASURE; icons plan / counter / estimate. Warning footer: Use MEASURE only on the small prepared local fixture. Do not conflate estimated cost, scanCount and duration.

## 07. Inspect one query in local Author
- Prepare the supplied five-page fixture.
- Explain the broad and bounded SQL2 queries.
- Inspect the selected index and covered restrictions.
- Run the bounded query; compare paths and recorded counts.
- Visual: Four-step path with local Author boundary and file icons. Footer: Exact index names and counts depend on your SDK. Small supporting note: Full setup and copyable queries are in the study guide.

## 08. Compare evidence under the same conditions
- Keep content, identity, query and window comparable.
- Confirm the returned paths before judging speed.
- Look for fewer unnecessary scans and supported ordering.
- Repeat observations; one duration is not a benchmark.
- Visual: Large table explicitly labelled Synthetic teaching example — not measured in SDK. Columns Observation / Case A / Case B. Rows: Uses an index / Yes / Yes; Scanned candidates / 8400 / 2; Returned results / 2 / 2; Ordering / Outside index / In index. Footer: These cases illustrate possible work, not a promised improvement from changing one setting.

## 09. Read the definition behind the plan
- type=lucene; compatVersion=2
- Path support: evaluatePathRestrictions
- Exact tag condition: propertyIndex=true
- Title ordering: ordered=true on a single-valued property
- Visual: Annotated minimal tree /oak:index/<selected-index> → indexRules → cq:Page → properties. Leaves tags: name=jcr:content/cq:tags, propertyIndex=true; title: name=jcr:content/jcr:title, ordered=true, type=String. Footer: Inspect the actual definition; do not edit it during this demo. Keep all paths legible.

## 10. An index change needs evidence
- Check query scope and existing index coverage first.
- For cq:Page, prefer extending an appropriate existing index.
- Review and version the definition in source control.
- Cloud Manager deploys the change through its pipeline.
- Visual: Evidence → Query correction → Coverage gap? decision diamond. No branch: Retest. Yes branch: Versioned index change → Pipeline → Verify. Small boundary note: Today: local inspection and documented Cloud workflow. No live Cloud deployment or manual production reindex.

## 11. Key takeaways
- Few results do not prove low query cost.
- Read restrictions and ordering inside the plan.
- Separate estimated cost, scans and elapsed time.
- Correct the query while preserving its intended contract.
- Justify index changes with repeatable evidence.
- Visual: Five wide concise takeaway rows, small specific icons, balanced whitespace. Each takeaway appears exactly once.

## 12. Questions / Thank you.
- Questions
- Thank you.
- Visual: Passive closing with question bubble and handshake. Render ONLY Questions, Thank you. and small slide number 12. No other titles, subtitles, metadata or footer.
