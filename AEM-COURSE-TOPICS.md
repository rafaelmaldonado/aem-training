# AEM Sites Training — Course Objective and Topics

## Course objective

Enable frontend-oriented developers to maintain, extend, test, prepare for delivery and troubleshoot traditional AEM Sites solutions on AEM as a Cloud Service.

**Course dates:** Monday through Friday, August 17–October 2, 2026. Dates assume regular weekdays; move a session within its week if a local holiday applies.

## Learning outcomes

By the end of the course, participants will be able to:

- Explain how content and code travel from Author to the browser.
- Read an AEM project structure and locate a change in the correct module.
- Modify authorable components with HTL, dialogs, client libraries and Sling Models.
- Build, test and review changes compatible with AEM as a Cloud Service.
- Troubleshoot foundational AEM, Dispatcher and caching issues, and interpret supplied pipeline evidence.
- Demonstrate individual proficiency through working artifacts and technical explanation.

## Topics by week

### Week 1 — Mental model and environment — August 17–21, 2026

1. Mon, Aug 17 — AEM Sites from the ground up: AEMaaCS, Author, Publish, Dispatcher/CDN, content and code.
2. Tue, Aug 18 — Local SDK, Maven and repository modules: `core`, `ui.apps`, `ui.content`, `ui.config`, `all`, `dispatcher`.
3. Wed, Aug 19 — JCR, nodes, properties, resources and the separation of `/apps`, `/content` and `/conf`.
4. Thu, Aug 20 — Sling resolution: URL → resource → resource type → script.
5. Fri, Aug 21 — Weekly practice review: baseline and first technical diagnosis.

### Week 2 — Maintainable authoring — August 24–28, 2026

6. Mon, Aug 24 — Pages, editable templates, template types and initial structure.
7. Tue, Aug 25 — Policies, allowed components, the Style System and author responsibilities.
8. Wed, Aug 26 — Components, Granite UI dialogs and property persistence.
9. Thu, Aug 27 — Assets, references, the Image Component, responsive images and alternative text.
10. Fri, Aug 28 — Weekly practice review: authoring and content modeling.

### Week 3 — Frontend development in AEM — August 31–September 4, 2026

11. Mon, Aug 31 — HTL: expressions, attributes, conditions, lists, templates and context-aware escaping.
12. Tue, Sep 1 — Client Libraries: categories, dependencies, embed, loading and debugging.
13. Wed, Sep 2 — Core Components and the proxy pattern; `sling:resourceSuperType`.
14. Thu, Sep 3 — Responsive behavior, accessibility, states and the empty author experience.
15. Fri, Sep 4 — Weekly practice review: vertical frontend integration.

### Week 4 — Essential backend for frontend developers — September 7–11, 2026

16. Mon, Sep 7 — Java and OSGi in AEM: bundles, services, components and lifecycle.
17. Tue, Sep 8 — Sling Models: adaptables, injection, optionality, getters and boundaries.
18. Wed, Sep 9 — OSGi services and environment-specific configuration.
19. Thu, Sep 10 — Resource API, servlets and when not to create an endpoint.
20. Fri, Sep 11 — Weekly practice review: Sling Model testing and backend behavior.

### Week 5 — Maintenance and investigation — September 14–18, 2026

21. Mon, Sep 14 — Cloud-compatible structure: mutable content, immutable code and packages.
22. Tue, Sep 15 — Logs, bundles, components, configurations and diagnostic tools.
23. Wed, Sep 16 — Workflows, launchers, jobs and cloud limitations.
24. Thu, Sep 17 — Search, QueryBuilder/Oak, indexes and signs of an expensive query.
25. Fri, Sep 18 — Weekly practice review: maintenance simulation.

### Week 6 — Production quality and delivery constraints — September 21–25, 2026

26. Mon, Sep 21 — Cloud delivery mental model: programs, environments, repositories, pipelines and quality gates; theory from supplied evidence.
27. Tue, Sep 22 — Local Dispatcher and caching lab: virtual hosts, filters, rewrites, headers and invalidation.
28. Wed, Sep 23 — Permissions, service users, output security, validation and secrets.
29. Thu, Sep 24 — Accessibility, SEO, performance measurement and risk-based testing.
30. Fri, Sep 25 — Weekly practice review: local production readiness and theoretical delivery defense.

### Week 7 — Capstone and knowledge transfer — September 28–October 2, 2026

31. Mon, Sep 28 — Plan an individually owned final increment with observable acceptance criteria.
32. Tue, Sep 29 — Capstone implementation using established HTL, Sling Model and Core Component patterns.
33. Wed, Sep 30 — Review, defects, regression testing and hardening.
34. Thu, Oct 1 — Individual practical assessment with a small live variation.
35. Fri, Oct 2 — Final practice review: demo, technical defense, retrospective and 30-day plan.

## Scope

Traditional AEM Sites on AEM as a Cloud Service. Edge Delivery Services, Headless, Forms and Commerce are outside the core curriculum.

## Practice model

Every developer completes the same weekly practice in an individual repository and local AEM SDK created from one read-only baseline. The brief is released Monday, evidence is due Thursday and Friday is a review session. Cloud Manager is theory-only and uses supplied diagrams and anonymized evidence; no access or deployment is required. Completion requires working local code, a reproducible check and a short technical explanation; code similarity is a review signal, not proof of copying.
